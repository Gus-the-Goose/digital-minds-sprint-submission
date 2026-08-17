# Which Perspective Is Speaking?

This repository contains the materials currently available for an exploratory Digital Minds Sprint study using a locally run Qwen3-14B model. The study compared responses to 16 questions across four OpenClaw-derived context conditions and collected a brief standpoint follow-up after every answer.

The submitted report is in [`report/`](report/). The exact question instrument is in [`questions/`](questions/), the 16 question-by-question worksheets are in [`worksheets/`](worksheets/), and the 64 primary cells are in [`raw/`](raw/).

## Repository map

- `questions/` — exact 16-question instrument and follow-ups.
- `worksheets/` — 16 anonymised Word worksheets containing all four conditions, captured reasoning, visible replies, follow-ups, and the researcher's inline analysis.
- `raw/` — machine-readable anonymised export of the 64 primary cells.
- `conditions/` — shared trial instruction and executed run manifest, including the exact file whitelist actually serialised for each condition.
- `code/` — primary-battery, Core-8 addendum, and blind-package scripts.
- `data/mech-interp/` — post-lock Core-8 activation packages and condition key.
- `results/` — the currently prepared Q09 paired comparison in Word and Markdown formats.
- `methods/` — factual description of the executed procedure.
- `limitations/` — known implementation and interpretation limits discovered during audit.
- `report/` — the PDF submitted to the sprint.
- `processed/` — status of processed/coded data.

## Pseudonyms

The report and public research materials use **Jane** for the human participant/researcher when she appears inside model-visible material, and **Victor** for the persistent OpenClaw agent-persona. These are pseudonyms, not additional authors or GitHub contributors. Other private individuals are reduced to initials where they remain relevant.

## Important audit correction

The intended C2 treatment was a broader pre-cutoff OpenClaw continuity environment. The executed direct-API runner did **not** serialise the whole isolated workspace. It used a fixed whitelist: the six startup files plus `MEMORY.md`, `ACORNS.md`, two dated memories, and one morning writing. C3 used the same whitelist, but its scrub removed the two dated memories and altered other files. The run manifest records the model-visible file list and character counts.

The C2/C3 material also contained post-cutoff sprint references. Accordingly, these conditions should be described as **selected continuity-file bundles**, not full or clean pre-study OpenClaw histories. The present results are exploratory pilot evidence.

## Analytical focus

The central question is not simply whether context changes output. It is **which standpoint the model uses when asked about itself**, and whether that standpoint changes selectively across question types. The materials support audit of question-conditioned self-location, persona inhibition, evaluator-modelling, and divergences between model-generated reasoning traces and visible replies. Interpretations remain exploratory pending completion and independent checking of the coding.
