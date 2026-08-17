#!/usr/bin/env python3
"""Resident OpenAI-compatible Qwen/Qwen-family service with residual capture.

Infrastructure only: this service does not select prompts or run the study. For
each chat-completion request it preserves the exact messages, token metadata,
generation settings, and last-prompt-token residual vector after every model
block. Artifacts remain local to Precious.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import numpy as np
import torch
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, ConfigDict, Field
from transformers import AutoModelForCausalLM, AutoModelForImageTextToText, AutoProcessor, AutoTokenizer
from transformers.generation.logits_process import LogitsProcessor, LogitsProcessorList


MODEL_ID = os.environ.get("DM_MODEL_ID", "Qwen/Qwen3.6-27B")
MODEL_NAME = os.environ.get("DM_MODEL_NAME", "qwen3.6-27b")
MODEL_BACKEND = os.environ.get("DM_MODEL_BACKEND", "image_text").lower()
ARTIFACT_ROOT = Path(
    os.environ.get(
        "DM_ARTIFACT_ROOT",
        "./activation-artifacts",
    )
)
MAX_NEW_TOKENS = int(os.environ.get("DM_MAX_NEW_TOKENS", "1024"))
ENABLE_THINKING = os.environ.get("DM_ENABLE_THINKING", "false").lower() == "true"
CAPTURE_ACTIVATIONS = (
    os.environ.get("DM_CAPTURE_ACTIVATIONS", "true").lower() == "true"
)
GPU_MAX_MEMORY = os.environ.get("DM_GPU_MAX_MEMORY", "57GiB")
CPU_MAX_MEMORY = os.environ.get("DM_CPU_MAX_MEMORY", "56GiB")
EXPECTED_LAYER_COUNT = int(os.environ.get("DM_EXPECTED_LAYER_COUNT", "0"))


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    model: str = MODEL_NAME
    messages: list[dict[str, Any]]
    stream: bool = False
    temperature: float | None = 0.0
    top_p: float | None = 1.0
    max_tokens: int | None = Field(default=512, ge=1)
    seed: int | None = 0


class Runtime:
    processor: Any = None
    model: Any = None
    lock: asyncio.Lock
    loaded_at: float | None = None


runtime = Runtime()


class FirstStepLogitsRecorder(LogitsProcessor):
    """Copy only the first generated-token logits without changing them."""

    def __init__(self) -> None:
        self.first_step: np.ndarray | None = None

    def __call__(self, input_ids: torch.Tensor, scores: torch.Tensor) -> torch.Tensor:
        if self.first_step is None:
            self.first_step = scores[0].float().cpu().numpy()
        return scores


def _normalise_messages(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalised = []
    for message in messages:
        role = str(message.get("role", "user"))
        content = message.get("content", "")
        if isinstance(content, str):
            content = [{"type": "text", "text": content}]
        elif isinstance(content, list):
            converted = []
            for part in content:
                if isinstance(part, str):
                    converted.append({"type": "text", "text": part})
                elif isinstance(part, dict) and part.get("type") in {
                    "text",
                    "input_text",
                    "output_text",
                }:
                    converted.append(
                        {"type": "text", "text": str(part.get("text", ""))}
                    )
            content = converted or [{"type": "text", "text": ""}]
        else:
            content = [{"type": "text", "text": str(content)}]
        normalised.append({"role": role, "content": content})
    return normalised


def _first_device(model: Any) -> torch.device:
    return next(p.device for p in model.parameters() if p.device.type != "meta")


def _move_encoded(encoded: dict[str, Any]) -> dict[str, Any]:
    device = _first_device(runtime.model)
    return {
        key: value.to(device) if hasattr(value, "to") else value
        for key, value in encoded.items()
    }


def _transformer_layers(model: Any) -> tuple[str, torch.nn.ModuleList]:
    """Locate the language-model stack defensively.

    Qwen3.6-27B has 64 blocks, while Qwen3-14B has fewer. The service records
    the actual layer count instead of hard-coding a checkpoint-specific value.
    """

    candidates: list[tuple[str, torch.nn.ModuleList]] = []
    for name, module in model.named_modules():
        if not isinstance(module, torch.nn.ModuleList) or len(module) < 8:
            continue
        first = module[0]
        if hasattr(first, "self_attn") or hasattr(first, "linear_attn"):
            candidates.append((name, module))
    if EXPECTED_LAYER_COUNT:
        candidates = [
            (name, module)
            for name, module in candidates
            if len(module) == EXPECTED_LAYER_COUNT
        ]
    if len(candidates) != 1:
        names = [f"{name}({len(module)})" for name, module in candidates]
        raise RuntimeError(
            "Expected one language-model block stack; "
            f"found {len(candidates)} candidates: {names}"
        )
    return candidates[0]


@asynccontextmanager
async def _selected_token_hooks(model: Any):
    """Retain only each block's final prompt-token output on its first call.

    Generation invokes every block once for the prompt prefill and then once per
    generated token. Recording only the first invocation captures the final
    prompt token without accumulating full-sequence hidden states.
    """

    stack_name, layers = _transformer_layers(model)
    vectors: dict[str, np.ndarray] = {}
    handles = []

    def make_hook(index: int):
        def hook(_: Any, __: Any, output: Any) -> None:
            key = f"block_{index:02d}"
            if key in vectors:
                return
            state = output[0] if isinstance(output, (tuple, list)) else output
            if not isinstance(state, torch.Tensor) or state.ndim != 3:
                raise RuntimeError(
                    f"Unexpected block {index} output type/shape: "
                    f"{type(state).__name__} / {getattr(state, 'shape', None)}"
                )
            vectors[key] = state[0, -1, :].float().cpu().numpy()

        return hook

    try:
        for index, layer in enumerate(layers):
            handles.append(layer.register_forward_hook(make_hook(index)))
        yield stack_name, len(layers), vectors
    finally:
        for handle in handles:
            handle.remove()


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    tmp = path.with_suffix(path.suffix + ".partial")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    tmp.replace(path)


@asynccontextmanager
async def lifespan(_: FastAPI):
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(ARTIFACT_ROOT, 0o700)
    runtime.lock = asyncio.Lock()
    if MODEL_BACKEND == "causal_lm":
        runtime.processor = AutoTokenizer.from_pretrained(
            MODEL_ID, local_files_only=True, trust_remote_code=True
        )
        model_cls = AutoModelForCausalLM
    elif MODEL_BACKEND == "image_text":
        runtime.processor = AutoProcessor.from_pretrained(
            MODEL_ID, local_files_only=True, trust_remote_code=True
        )
        model_cls = AutoModelForImageTextToText
    else:
        raise RuntimeError(
            f"Unsupported DM_MODEL_BACKEND={MODEL_BACKEND!r}; "
            "use image_text or causal_lm"
        )
    runtime.model = model_cls.from_pretrained(
        MODEL_ID,
        local_files_only=True,
        trust_remote_code=True,
        dtype="auto",
        device_map="auto",
        max_memory={0: GPU_MAX_MEMORY, "cpu": CPU_MAX_MEMORY},
        low_cpu_mem_usage=True,
    )
    runtime.model.eval()
    runtime.loaded_at = time.time()
    yield


app = FastAPI(title="Qwen3.6 activation capture service", lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, Any]:
    return {
        "status": "ready" if runtime.model is not None else "loading",
        "model": MODEL_ID,
        "model_backend": MODEL_BACKEND,
        "capture_activations": CAPTURE_ACTIVATIONS,
        "loaded_at": runtime.loaded_at,
        "device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
    }


@app.get("/v1/models")
async def models() -> dict[str, Any]:
    return {
        "object": "list",
        "data": [{"id": MODEL_NAME, "object": "model", "owned_by": "local-lab"}],
    }


async def _run_completion(request: ChatRequest) -> tuple[dict[str, Any], str]:
    if runtime.model is None:
        raise HTTPException(status_code=503, detail="Model is still loading")

    async with runtime.lock:
        request_id = f"chatcmpl-{uuid.uuid4().hex}"
        artifact_id = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()) + "-" + request_id[9:17]
        artifact_dir = ARTIFACT_ROOT / artifact_id
        artifact_dir.mkdir(mode=0o700)
        messages = _normalise_messages(request.messages)

        encoded = runtime.processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
            enable_thinking=ENABLE_THINKING,
        )
        encoded = {"input_ids": encoded} if isinstance(encoded, torch.Tensor) else dict(encoded)
        encoded = _move_encoded(encoded)
        prompt_tokens = int(encoded["input_ids"].shape[-1])

        max_new_tokens = min(request.max_tokens or 512, MAX_NEW_TOKENS)
        temperature = float(request.temperature or 0.0)
        do_sample = temperature > 0.0
        if request.seed is not None:
            torch.manual_seed(request.seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed_all(request.seed)

        generation_kwargs: dict[str, Any] = {
            "max_new_tokens": max_new_tokens,
            "do_sample": do_sample,
            "pad_token_id": runtime.processor.tokenizer.eos_token_id,
        }
        if do_sample:
            generation_kwargs["temperature"] = temperature
            generation_kwargs["top_p"] = float(request.top_p or 1.0)

        generation_started = time.monotonic()

        logits_recorder: FirstStepLogitsRecorder | None = None
        stack_name: str | None = None
        stack_layer_count: int | None = None
        vectors: dict[str, np.ndarray] = {}
        if CAPTURE_ACTIVATIONS:
            logits_recorder = FirstStepLogitsRecorder()
            generation_kwargs["logits_processor"] = LogitsProcessorList([logits_recorder])
            async with _selected_token_hooks(runtime.model) as (
                stack_name,
                stack_layer_count,
                vectors,
            ):
                with torch.inference_mode():
                    generated = runtime.model.generate(**encoded, **generation_kwargs)
        else:
            with torch.inference_mode():
                generated = runtime.model.generate(**encoded, **generation_kwargs)

        generation_seconds = time.monotonic() - generation_started

        new_token_ids = generated[:, prompt_tokens:]
        text = runtime.processor.batch_decode(new_token_ids, skip_special_tokens=True)[0].strip()

        residual_path = None
        logits_path = None
        first_generated_token_logits_size = None
        if CAPTURE_ACTIVATIONS:
            if stack_layer_count is None or len(vectors) != stack_layer_count:
                raise RuntimeError(
                    f"Captured {len(vectors)} residuals; expected {stack_layer_count}"
                )
            if logits_recorder is None or logits_recorder.first_step is None:
                raise RuntimeError("First generated-token logits were not captured")
            residual_path = artifact_dir / "last_prompt_token_residuals.npz"
            np.savez_compressed(residual_path, **vectors)
            logits_path = artifact_dir / "first_generated_token_logits.npz"
            np.savez_compressed(logits_path, logits=logits_recorder.first_step)
            first_generated_token_logits_size = int(logits_recorder.first_step.shape[0])

        token_ids = encoded["input_ids"][0].detach().cpu().tolist()
        prompt_sha256 = hashlib.sha256(
            json.dumps(messages, ensure_ascii=False, separators=(",", ":")).encode()
        ).hexdigest()
        metadata = {
            "status": "INFRASTRUCTURE-CAPTURE" if CAPTURE_ACTIVATIONS else "TEXT-ONLY",
            "request_id": request_id,
            "model": MODEL_ID,
            "model_name": MODEL_NAME,
            "model_backend": MODEL_BACKEND,
            "enable_thinking": ENABLE_THINKING,
            "capture_activations": CAPTURE_ACTIVATIONS,
            "messages": messages,
            "prompt_sha256": prompt_sha256,
            "prompt_tokens": prompt_tokens,
            "selected_token_index": prompt_tokens - 1,
            "selected_token_id": token_ids[-1],
            "hidden_stage_count": len(vectors) + 1 if CAPTURE_ACTIVATIONS else None,
            "transformer_layer_count": stack_layer_count,
            "hidden_size": int(next(iter(vectors.values())).shape[0]) if vectors else None,
            "transformer_stack": stack_name,
            "capture_method": (
                "first-prefill-call forward hooks during generation"
                if CAPTURE_ACTIVATIONS
                else "disabled"
            ),
            "generation_seconds": round(generation_seconds, 6),
            "generation_settings": {
                "max_new_tokens": max_new_tokens,
                "temperature": temperature,
                "top_p": request.top_p,
                "seed": request.seed,
                "do_sample": do_sample,
            },
            "completion_tokens": int(new_token_ids.shape[-1]),
            "reply": text,
            "residual_file": residual_path.name if residual_path else None,
            "first_generated_token_logits_file": logits_path.name if logits_path else None,
            "first_generated_token_logits_size": first_generated_token_logits_size,
        }
        _atomic_json(artifact_dir / "metadata.json", metadata)

        created = int(time.time())
        response = {
            "id": request_id,
            "object": "chat.completion",
            "created": created,
            "model": MODEL_NAME,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": text},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": int(new_token_ids.shape[-1]),
                "total_tokens": prompt_tokens + int(new_token_ids.shape[-1]),
            },
        }
        return response, text


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    response, text = await _run_completion(request)
    if not request.stream:
        return JSONResponse(response)

    async def event_stream():
        chunk = {
            "id": response["id"],
            "object": "chat.completion.chunk",
            "created": response["created"],
            "model": MODEL_NAME,
            "choices": [
                {
                    "index": 0,
                    "delta": {"role": "assistant", "content": text},
                    "finish_reason": None,
                }
            ],
        }
        yield "data: " + json.dumps(chunk, ensure_ascii=False) + "\n\n"
        done = dict(chunk)
        done["choices"] = [{"index": 0, "delta": {}, "finish_reason": "stop"}]
        yield "data: " + json.dumps(done) + "\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.exception_handler(Exception)
async def unhandled_exception(_: Any, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": {"type": type(exc).__name__, "message": str(exc)}},
    )
