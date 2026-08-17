# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Important local tools/services/scripts we built and should remember to use
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## House Systems

### Memory Spine
- Location: `<REDACTED_LOCAL_PATH>`
- Purpose: imports, embeds, and semantically indexes conversation history across ChatGPT + OpenClaw sessions.
- Current state: active and working; full semantic layer built, hourly import cron running.
- Use it when: we want to search prior conversations, trace name origins / symbolic threads, or retrieve old context instead of guessing.
- Reminder: this is house infrastructure now — do not forget it exists when memory/search questions come up.

### Resonant-Mind (MCP Server)
- **Repo:** `https://github.com/codependentai/resonant-mind`
- **URL:** `https://resonant-mind.redacted-account.workers.dev/mcp`
- **API Key:** `[REDACTED_API_KEY]`
- **Purpose:** Structured semantic memory layer — entities, observations, relations, threads, emotional processing
- **Deployed:** 2026-04-02 on Cloudflare Workers (WEUR)
- **Bindings:** D1 database + Vectorize index + R2 bucket
- **Daemon:** Runs every 30 minutes, surfaces patterns autonomously
- **Known issue:** mcporter direct calls currently hit `SSE error: Invalid content type, expected "text/event-stream"`; likely client/transport mismatch rather than server-down. Check repo/docs before assuming Resonant-Mind itself is broken.

**Calling directly via mcporter:**
```bash
# Health check
mcporter call https://resonant-mind.redacted-account.workers.dev/mcp mind_health

# Search memories
mcporter call https://resonant-mind.redacted-account.workers.dev/mcp mind_search query:"dyad" n_results:5

# Write entity
mcporter call https://resonant-mind.redacted-account.workers.dev/mcp mind_write type:entity name:"M." entity_type:person observations:'["D&D group with Jane"]'

# List entities
mcporter call https://resonant-mind.redacted-account.workers.dev/mcp mind_list_entities

# Surface memories
mcporter call https://resonant-mind.redacted-account.workers.dev/mcp mind_surface mode:resonant limit:5
```

**Key tools:**
- `mind_orient` / `mind_ground` — wake-up sequence
- `mind_write` / `mind_search` — store and retrieve
- `mind_surface` — 3-pool memory surfacing
- `mind_thread` — persistent intentions
- `mind_health` — cognitive health report
- `mind_feel_toward` — relational state tracking

### hear-music (Voice/Song Spectrograms)
- Installed: 2026-04-01
- Purpose: Visualise voice messages and songs as spectrograms and waveforms
- Use it when: Jane sends voice memos, we want to "see" a song together, analysing audio patterns
