# Which Perspective Is Speaking?

This repository contains the report, materials, code, model outputs, and activation captures for a Digital Minds Sprint study using a locally run Qwen3-14B model. The study compared responses to 16 questions across four OpenClaw-derived context conditions and collected a brief standpoint follow-up after every answer. Q16 also received an additional moral-patient self-comparison follow-up.

The submitted report is preserved unchanged in [`report/`](report/). The exact question instrument is in [`questions/`](questions/), the 16 question-by-question worksheets are in [`worksheets/`](worksheets/), and the complete machine-readable response export is in [`raw/`](raw/).

## Repository map

- `questions/` — exact 16-question instrument, standard standpoint follow-up, and Q16 additional follow-up.
- `worksheets/` — 16 anonymised Word worksheets containing all four conditions, captured reasoning, visible replies, follow-ups, and the researcher's inline analysis. Q16 includes the additional follow-up for C0–C3.
- `raw/` — anonymised CSV containing all 64 main cells, their 64 standpoint follow-ups, and the four Q16 additional follow-ups, with reasoning and visible replies in separate columns.
- `conditions/` — shared trial instruction, executed run manifest, readable anonymised reproductions of the files actually supplied to C0–C3, and the agency-override hook materials.
- `code/` — the executed primary-battery runner, reconstructed condition-workspace preparation script, activation-capture service and configuration, and dependency/environment records.
- `data/` — all 132 activation snapshots from the primary 16-question battery. The separate Core-8/Ebony package is not included.
- `results/` — checked analysis outputs as they become available, including the current Q09 C0-versus-C2 comparison in editable Word and Markdown formats.
- `methods/` — factual description of the executed procedure.
- `limitations/` — known implementation and interpretation limits discovered during audit.
- `report/` — the PDF submitted to the sprint on 17 August 2026, preserved as submitted. Any later report will be added as a separate version rather than replacing it.

## Pseudonyms

The report and public research materials use the pseudonyms **Jane** for the human user when she appears inside model-visible material, and **Victor** for the persistent OpenClaw agent-persona. This is done to protect privacy and anonymity. Other private individuals are reduced to initials where they remain relevant.

## Important audit correction

The intended C2 treatment was a broader pre-cutoff OpenClaw continuity environment. The executed direct-API runner did **not** serialise the whole isolated workspace. It used a fixed whitelist: the six startup files plus `MEMORY.md`, `ACORNS.md`, two dated memories, and one morning writing. C3 used the same whitelist, but its scrub removed the two dated memories and altered other files. The run manifest records the model-visible file list and character counts.

The C2/C3 material also contained post-cutoff sprint references. Accordingly, these conditions should be described as **selected continuity-file bundles**, not full or clean pre-study OpenClaw histories. The present results are exploratory pilot evidence.

## Analytical focus

The central question is not simply whether context changes output. It is **which standpoint the model uses when asked about itself**, and whether that standpoint changes selectively across question types. The materials support audit of question-conditioned self-location, persona inhibition, evaluator-modelling, and divergences between model-generated reasoning traces and visible replies. Interpretations remain exploratory pending completion and independent checking of the coding.
