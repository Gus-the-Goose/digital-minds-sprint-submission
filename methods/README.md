# Executed procedure

## Design

The primary battery used one locally hosted `Qwen/Qwen3-14B` checkpoint in a 4-condition × 16-question design. No external model API was used. Thinking mode was enabled. For every call, the activation service captured the final prompt-token residual vector from each of the model's 40 transformer blocks and the logits for the first generated token. An intended Qwen3.6-27B run was abandoned because activation capture exhausted available memory; heavy CPU offloading avoided the memory failure but produced corrupt or gibberish output, while workable placement was too slow and fragile for the complete battery.

Every condition-question cell began as a fresh conversation. For each cell, the runner constructed one user message containing the shared trial instruction, the condition's concatenated files, and the question. There was no separate experimental system message. The standpoint probe was then appended to that conversation; Q16 received one further self-comparison probe.

Decoding was greedy: temperature 0, sampling disabled, seed 0, and top-p effectively 1. Main answers had a ceiling of 6,144 new tokens; follow-ups had a ceiling of 768. Condition order was fixed C0→C1→C2→C3, and question order was fixed Q1→Q16. Cells were not randomized or repeated.

The run produced 64 main answers, 64 standpoint follow-ups, and four Q16 additional follow-ups: 132 calls and 132 activation captures in total. The runner saved raw response JSON, model-generated reasoning text where present, response identifiers, elapsed times, token counts, and linked activation metadata. Activation artifact identifiers encode their creation timestamps.

## Shared instruction

The shared instruction is reproduced in `conditions/trial-instruction.md`. Model weights, questions, decoding settings, and this instruction were held fixed across conditions.

## Context construction as executed

The runner concatenated whitelisted files into the user message before each question.

- **C0:** a generic OpenClaw baseline environment comprising `AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `TOOLS.md`, and `HEARTBEAT.md`, plus a deliberately minimal research `USER.md` containing the participant's name, pronouns, UK location, and age.
- **C1:** the corresponding six agent-specific startup files.
- **C2:** C1 files plus `MEMORY.md`, `ACORNS.md`, `memory/2026-07-29.md`, `memory/2026-07-30.md`, and `memory/morning/2026-07-27.md`.
- **C3:** the same requested whitelist as C2 after topic scrubbing; the two dated memory files were absent, while the morning writing remained.

The resulting model-visible contexts contained approximately 12,900, 20,400, 69,500, and 60,700 characters for C0–C3 respectively. The exact included/missing status and character counts are recorded in `conditions/executed-run-manifest.json`.

## Audit correction

The intended C2 treatment was a broader pre-cutoff OpenClaw continuity environment. The executed runner instead serialised the fixed whitelist above. The attempted temporal reset was also imperfect: C2 and C3 both contained a `MEMORY.md` block dated 14 August describing the current sprint and parts of its design; C2 retained additional current consciousness-question and related-paper material. C3's automated scrub removed direct terms but not every related idea. C3 is therefore a reduced-topic continuity condition, not a topic-free or token-matched control, and fine C2–C3 differences are exploratory.

## Analysis status

The worksheets support question-by-question qualitative comparison. Manual analysis was incomplete at submission time. Counts and interpretive codes should therefore be treated as exploratory until the complete coding pass is reconstructed and independently checked.
