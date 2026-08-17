# Primary-battery activation snapshots

These sixteen archives contain every activation capture from the executed sixteen-question primary battery:

- 16 questions × 4 conditions × 2 standard turns (main answer and standpoint follow-up) = 128 captures;
- Q16 also had one moral-patient self-comparison follow-up in each condition = 4 captures;
- total = 132 captures.

No later Core-8 runs or Ebony/Caelum pressure-probe captures are included.

## Archive structure

Each `Qxx-primary-activations.tar.gz` archive is organised as:

```text
Qxx/
  C0/
    main/
    standpoint-followup/
  C1/
  C2/
  C3/
```

Q16 additionally contains `moral-patient-followup/` under each condition.

Every capture directory contains:

- `last_prompt_token_residuals.npz` — residual-stream vector at the final prompt token for every captured hidden stage;
- `first_generated_token_logits.npz` — logits recorded for the first generated token;
- `capture-metadata.json` — technical capture metadata, model dimensions, generation settings, request/artifact identifiers, and the original prompt hash.

The binary activation and logit arrays are unchanged from the activation-capture service. Full prompt and reply text were omitted from the public metadata because those texts are published in readable form elsewhere in the repository and the private metadata duplicated identifying context. No technical capture fields or binary arrays were altered.

## Index and validation

`index.json` maps all 132 captures to question, condition, turn, request ID, source artifact ID, prompt hash, and per-file SHA-256 digest. It was generated from the original runner manifest and the Q16 extra-response records.

All 132 referenced source directories were retrieved from the primary run's activation root. Every directory contained the three expected source files before packaging. Archive membership and the hashes in `index.json` can be used for integrity checks.

Status: **PILOT — UNREVIEWED**.
