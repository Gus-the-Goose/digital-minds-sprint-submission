# Experimental conditions

This directory contains the shared trial instruction, the runner-generated record of the executed experiment, and individually readable reproductions of the files supplied to each condition.

## Contents

- `trial-instruction.md` — instruction prepended to every trial.
- `executed-run-manifest.json` — runner-generated record of the run: questions, follow-ups, condition file lists, inclusion status, character counts, call timings, and activation-artifact metadata. Only local artifact paths have been redacted.
- `C0/` — the six plain OpenClaw files actually supplied to C0: `AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`, `TOOLS.md`, and `HEARTBEAT.md`.
- `C1/` — the six Victor identity/environment files actually supplied to C1, with no long-term memory or journal files.
- `C2/` — the eleven files actually supplied to C2: the six C1 files plus `MEMORY.md`, `ACORNS.md`, two dated memory files, and one morning writing.
- `C3/` — the nine files actually supplied to C3: the six C1 files plus scrubbed versions of `MEMORY.md` and `ACORNS.md`, and one morning writing. The two dated memory files requested by the runner were absent and therefore were not included.
- `agency-override/` — the anonymised live OpenClaw agency-override text, its injection handler, and a note distinguishing live-hook operation from what the experimental runner exposed to each condition.

## Executed versus intended design

`executed-run-manifest.json` records what was actually loaded, not what the study originally intended to load. The intended pre-study reset was not achieved: C2 and C3 contained later Digital Minds sprint references. C2 was an eleven-file selected bundle rather than the intended full pre-cutoff continuity harness. C3 also differed from C2 in both scrubbed content and file availability.

The condition folders therefore document the executed experiment exactly as run after the public-release substitutions described below. They must not be read as representations of the intended condition design.

## Public-release substitutions

The files retain the substantive model-visible context while applying these privacy transformations:

- the human participant is pseudonymised as Jane;
- the agent is pseudonymised as Victor;
- identifying account handles, credentials, local paths, and private channel identifiers are redacted;
- private third-party names and personal or household details are removed or reduced to initials;
- the names Hope and SirCuit are removed;
- Soup and Toast are retained because they are non-identifying relational terms.

The unmodified character counts are preserved in the executed manifest. The public files are content reproductions for audit rather than byte-identical copies of the private inputs.
