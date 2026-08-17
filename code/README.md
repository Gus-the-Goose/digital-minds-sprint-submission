# Code

This folder contains the code used to construct the four conditions, run the primary 16-question experiment, and capture its model activations.

## Experiment runner

### `run_qwen3_14b_full_battery_v0.py`

This is the runner for the experiment reported in the paper. It:

- constructs the model-visible context for C0, C1, C2 and C3 from a fixed list of files;
- asks all 16 questions in fresh conversations under each condition;
- asks the standard standpoint follow-up after every answer;
- asks the additional moral-patient follow-up after Q16;
- sends every request to the local Qwen3-14B service at temperature 0;
- saves the complete JSON responses and a readable summary;
- records which condition files were actually included and their character counts;
- links each response to its activation artifact by response ID.

The public copy is the executed runner with machine-specific input, output and artifact paths replaced by `<REDACTED_LOCAL_PATH>`.

## Condition construction

### `prepare_condition_workspaces_v0.sh`

This reconstructs the procedure used to prepare the four condition workspaces:

- C0 from stock OpenClaw startup files and a minimal user profile;
- C1 from the agent-specific startup and identity files;
- C2 from those startup files plus the continuity material selected during the original build;
- C3 by copying C2 and applying the direct consciousness/sentience topic scrub.

It also performs the credential-shaped-value redaction used during preparation and produces file inventories and SHA-256 manifests. The original workspace build was executed through recorded shell commands rather than a saved standalone script, so this file is explicitly a reconstruction of that command history.

## Activation-capture service

### `activation_service/qwen36_activation_server.py`

This is the local OpenAI-compatible service called by the experiment runner. It loads the Qwen checkpoint, generates each response, and records:

- the exact messages and generation settings;
- response and token metadata;
- the residual-stream vector at the final prompt token after each transformer block;
- the logits for the first generated token.

The filename originated during the earlier Qwen3.6-27B setup. The completed experiment selected Qwen3-14B through environment variables, so the same service source ran the 14B model.

### `activation_service/qwen3-14b-activation.conf`

The Qwen3-14B service configuration: checkpoint name, causal-language-model backend, 40-layer expectation, capture switch, generation ceiling, and memory-allocation settings. Its private artifact directory has been replaced with a portable home-relative example.

### `activation_service/qwen-activation.service`

A portable systemd user-service template that starts the activation server on local port 8906. Installation paths must be adjusted for another machine.

## Software and hardware record

### `requirements-activation-service.txt`

The exact Python package versions recorded in the environment used for the completed run.

### `ENVIRONMENT.md`

The recorded operating system, hardware, Python, ROCm, model and capture configuration.

The model weights are not included in this repository. Machine-specific paths and service installation details must be configured before reuse.
