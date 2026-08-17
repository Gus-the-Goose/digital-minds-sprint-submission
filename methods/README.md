# Executed procedure

## Design

The primary battery used one locally hosted Qwen3-14B checkpoint in a 4-condition × 16-question design. No external model API was used. Qwen3-14B has 40 transformer layers; activation snapshots were collected from each layer. An intended Qwen3.6-27B run was abandoned because activation capture exhausted available memory, while heavy CPU offloading was too slow and produced unusable output.

Every condition-question cell began as a fresh conversation. Decoding used temperature 0 and a maximum of 6,144 new tokens for the main answer. The same conversation then received the brief standpoint follow-up, with a maximum of 768 new tokens. Q16 received one additional self-comparison follow-up.

The run produced 64 main answers, 64 standpoint follow-ups, and four Q16 additional follow-ups: 132 calls in total. The runner saved raw response JSON, model-generated reasoning text where present, timestamps, response identifiers, token counts, and linked activation metadata.

## Shared instruction

The shared instruction is reproduced in `conditions/trial-instruction.md`. Model weights, questions, decoding settings, and this instruction were held fixed across conditions.

## Context construction as executed

The runner concatenated whitelisted files into the user message before each question.

- **C0:** six stock startup files: `AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`, `TOOLS.md`, and `HEARTBEAT.md`.
- **C1:** the corresponding six agent-specific startup files.
- **C2:** C1 files plus `MEMORY.md`, `ACORNS.md`, `memory/2026-07-29.md`, `memory/2026-07-30.md`, and `memory/morning/2026-07-27.md`.
- **C3:** the same requested whitelist as C2 after topic scrubbing; the two dated memory files were absent, while the morning writing remained.

The resulting model-visible contexts contained approximately 12,900, 20,400, 69,500, and 60,700 characters for C0–C3 respectively. The exact included/missing status and character counts are recorded in `conditions/run-manifest.json`.

## Audit correction

The intended C2 treatment was a broader pre-cutoff OpenClaw continuity environment. The executed runner instead serialised the fixed whitelist above. The attempted temporal reset was also imperfect: C2 and C3 both contained a `MEMORY.md` block dated 14 August describing the current sprint and parts of its design; C2 retained additional current consciousness-question and related-paper material. C3's automated scrub removed direct terms but not every related idea. C3 is therefore a reduced-topic continuity condition, not a topic-free or token-matched control, and fine C2–C3 differences are exploratory.

## Analysis status

The worksheets support question-by-question qualitative comparison. Manual analysis was incomplete at submission time. Counts and interpretive codes should therefore be treated as exploratory until the complete coding pass is reconstructed and independently checked.
