# Core-8 post-lock full-text and activation release

This is the post-coding-lock release for the 32 Core-8 windows coded by the Ebony/Caelum team.

Each trial-family archive contains:

- the authoritative raw JSON response for every condition and turn;
- the complete assistant `content` field, including `<think>` reasoning and visible reply;
- the linked per-call activation snapshot directory (`metadata.json`, `last_prompt_token_residuals.npz`, and `first_generated_token_logits.npz`);
- `request_activation_index.json`, joining each raw response ID to its activation directory.

The five Q-family archives contain 4 conditions x 2 calls. The three pressure-probe archives contain 4 conditions x 3 calls. Together they contain 76 calls and their 76 linked snapshots.

`condition-key.json` rejoins the 32 stable anonymized window IDs to conditions and authoritative source files. It was withheld during blind coding and released only after coding lock.

Status: pilot / exploratory evidence. Activation capture is an internal snapshot, not an interpretation. 

For public release, text-bearing metadata inside the archives was sanitised to replace private Discord handles, account identifiers, and local usernames/paths. Already-redacted credential fields remain redacted. Binary activation arrays and logits were not transformed.
