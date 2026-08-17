# Execution environment

The primary battery was executed locally through the OpenAI-compatible activation-capture service in `activation_service/`.

## Recorded runtime

- Host OS: Ubuntu Linux, x86-64
- Kernel at audit: `7.0.0-29-generic`
- CPU/APU: AMD Ryzen AI Max+ 395 with Radeon 8060S
- Logical CPUs: 32
- Accelerator: AMD Radeon 8060S Graphics
- ROCm/HIP runtime used by PyTorch: 7.2
- Python: 3.13.14
- Model checkpoint: `Qwen/Qwen3-14B`, loaded from the local Hugging Face cache
- Model backend: `AutoModelForCausalLM`
- Transformer layers: 40
- Service endpoint: `http://127.0.0.1:8906/v1/chat/completions`

Exact Python package versions are in `requirements-activation-service.txt`. The PyTorch wheel was the ROCm 7.2 build and may require installation from the appropriate PyTorch/ROCm package index rather than ordinary PyPI.

## Capture configuration

The Qwen3-14B systemd drop-in set:

- thinking disabled at the chat-template switch;
- activation capture enabled;
- temperature controlled by the requesting runner (the primary battery used 0);
- a maximum service generation allowance of 8,192 tokens;
- 60 GiB accelerator-memory and 1 GiB CPU-memory limits for model placement;
- an expected 40-block transformer stack.

For each request, the service stored the exact messages and generation metadata, the residual-stream vector at the last prompt token after every transformer block, and the first generated-token logits.

Machine-specific paths in the public service and runner files have been replaced with configurable or redacted paths. The model weights are not redistributed in this repository.
