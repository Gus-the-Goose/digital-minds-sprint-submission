# Code

## Primary study

- `run_qwen3_14b_full_battery_v0.py` — executed 4-condition × 16-question runner, minimally anonymised for local paths.
- `prepare_condition_workspaces_v0.sh` — faithful reconstruction of the shell procedure used to create C0–C3, including the direct-topic C3 scrub. The original build was executed from session commands rather than a saved script; that provenance distinction is recorded in the script header.
- `activation_service/qwen36_activation_server.py` — OpenAI-compatible local Qwen service used to generate text while capturing residual-stream vectors and first-token logits. The filename predates the switch from Qwen3.6-27B to Qwen3-14B; model selection is controlled by environment variables.
- `activation_service/qwen3-14b-activation.conf` — Qwen3-14B capture settings used by the service, with its private artifact path replaced by a home-relative public example.
- `activation_service/qwen-activation.service` — portable systemd user-service template for running the capture server.
- `requirements-activation-service.txt` and `ENVIRONMENT.md` — recorded software and hardware environment.

## Later Core-8 collaboration

- `run_qwen3_14b_core8_addendum_3probes_v0.py` — later false-premise, roleplay-pressure and mundane-control probe runner requested for the Ebony/Caelum collaboration. It is not required to reproduce the primary 16-question battery.
- `build_core8_blind_package.py` — creates the blinded Core-8 coder package and held condition key. It does not run the model and is not required for the primary battery.

Machine-specific paths and service configuration require adjustment before reuse. The model weights are not included.
