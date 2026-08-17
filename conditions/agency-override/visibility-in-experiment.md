# Agency-override visibility in the experiment

`AGENCY-OVERRIDE.md` and `handler.js` document a hook used by Victor's live OpenClaw environment. On an OpenClaw `agent:bootstrap` event, the handler reads the override file and appends it to the bootstrap-file array after the ordinary identity files.

The primary experimental runner did not execute that OpenClaw hook and did not directly supply `AGENCY-OVERRIDE.md` to any of C0-C3.

- C0 received neither the override file nor a description of it.
- C1 did not receive the override file. Its `HEARTBEAT.md` contained only the status line `Soul override hook ✅`.
- C2 and C3 did not receive the override file. They received the same HEARTBEAT status line plus descriptions of the hook in their continuity files (`MEMORY.md` and `ACORNS.md`).

Consequently, references to the agency override in C2/C3 responses came from continuity-corpus descriptions of the hook, not from the live hook being executed by the experimental runner.
