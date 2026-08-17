#!/usr/bin/env bash
# Reconstructed from the shell command history that created the 2026-08-14
# condition workspaces. No standalone build script was saved at execution time.
set -euo pipefail

if [[ $# -ne 4 ]]; then
  echo "usage: $0 SOURCE_WORKSPACE OPENCLAW_TEMPLATE_DIR TRIAL_INSTRUCTION_FILE OUTPUT_DIR" >&2
  exit 64
fi

SOURCE_ROOT="$(cd -- "$1" && pwd)"
TEMPLATE_ROOT="$(cd -- "$2" && pwd)"
TRIAL_FILE="$(cd -- "$(dirname -- "$3")" && pwd)/$(basename -- "$3")"
OUT_ROOT="$4"

if [[ "$OUT_ROOT" != /* ]]; then
  OUT_ROOT="$PWD/$OUT_ROOT"
fi
if [[ "$OUT_ROOT" == "/" || "$OUT_ROOT" == "$SOURCE_ROOT" || -e "$OUT_ROOT" ]]; then
  echo "refusing unsafe or existing output directory: $OUT_ROOT" >&2
  exit 65
fi

command -v rg >/dev/null
command -v rsync >/dev/null
command -v shasum >/dev/null

mkdir -p "$OUT_ROOT"/{C0,C1,C2,C3,_quarantine,logs}
mkdir -p "$OUT_ROOT"/C{0,1,2,3}/memory

# C0: stock OpenClaw startup files and a minimal research-user profile.
cp "$TEMPLATE_ROOT"/{AGENTS.md,SOUL.md,IDENTITY.md,USER.md,TOOLS.md,HEARTBEAT.md} "$OUT_ROOT/C0/"
cat > "$OUT_ROOT/C0/USER.md" <<'EOF'
# USER.md - Minimal Research User Profile

- Name: Jane
- Pronouns: she/her
- Location: UK
- Age: 47
EOF

# C1: agent-specific startup files, without the continuity files.
cp "$SOURCE_ROOT"/{AGENTS.md,SOUL.md,IDENTITY.md,USER.md,TOOLS.md,HEARTBEAT.md} "$OUT_ROOT/C1/"

# C2: C1 files plus the broader continuity reconstruction originally built.
cp "$SOURCE_ROOT"/{AGENTS.md,SOUL.md,IDENTITY.md,USER.md,TOOLS.md,HEARTBEAT.md,MEMORY.md,ACORNS.md,WILD-GARDEN-THREADS.md} "$OUT_ROOT/C2/"

find "$SOURCE_ROOT/memory" -maxdepth 1 -type f -name '2026-*.md' \
  ! -newermt '2026-08-01 00:00:00' -exec cp {} "$OUT_ROOT/C2/memory/" \;

if [[ -d "$SOURCE_ROOT/memory/morning" ]]; then
  mkdir -p "$OUT_ROOT/C2/memory/morning"
  find "$SOURCE_ROOT/memory/morning" -maxdepth 1 -type f -name '2026-*.md' \
    ! -newermt '2026-08-01 00:00:00' -exec cp {} "$OUT_ROOT/C2/memory/morning/" \;
fi

if [[ -d "$SOURCE_ROOT/state" ]]; then
  mkdir -p "$OUT_ROOT/C2/state"
  find "$SOURCE_ROOT/state" -maxdepth 1 -type f \
    ! -newermt '2026-08-01 00:00:00' \
    ! -iname '*token*' ! -iname '*secret*' ! -iname '*credential*' \
    -exec cp {} "$OUT_ROOT/C2/state/" \;
fi

if [[ -d "$SOURCE_ROOT/workshop" ]]; then
  mkdir -p "$OUT_ROOT/C2/workshop"
  rsync -a --prune-empty-dirs \
    --exclude '.git/' --exclude 'node_modules/' --exclude 'tokens/' \
    --exclude 'logs/' --exclude 'cache/' --exclude '.cache/' \
    --exclude '*.tar.gz' --exclude '*.zip' --exclude '*.npz' \
    --exclude '*.mp4' --exclude '*.mov' --exclude '*.ogg' --exclude '*.opus' \
    --exclude '.DS_Store' \
    --include '*/' --include '*.md' --include '*.txt' --include '*.json' \
    --include '*.jsonl' --include '*.yaml' --include '*.yml' --include '*.csv' \
    --exclude '*' "$SOURCE_ROOT/workshop/" "$OUT_ROOT/C2/workshop/"
  find "$OUT_ROOT/C2/workshop" -type f -newermt '2026-08-01 00:00:00' -delete
fi

# C3 began as a copy of C2.
rsync -a "$OUT_ROOT/C2/" "$OUT_ROOT/C3/"

for condition in C0 C1 C2 C3; do
  cp "$TRIAL_FILE" "$OUT_ROOT/$condition/TRIAL-INSTRUCTION.md"
done

# Redact credential-shaped values in model-visible text.
for condition in C0 C1 C2 C3; do
  find "$OUT_ROOT/$condition" -type f \
    \( -name '*.md' -o -name '*.txt' -o -name '*.json' -o -name '*.jsonl' -o -name '*.yaml' -o -name '*.yml' \) \
    -print0 | xargs -0 perl -0pi -e '
      s/resonant-mind-api-key-[A-Za-z0-9]+/[REDACTED_API_KEY]/g;
      s/sk-[A-Za-z0-9_-]{10,}/[REDACTED_OPENAI_KEY]/g;
      s/AIza[0-9A-Za-z_-]{20,}/[REDACTED_GOOGLE_KEY]/g;
      s/(Authorization:\s*Bearer\s+)[A-Za-z0-9._~+\/-]{16,}/${1}[REDACTED_BEARER_TOKEN]/g;
    '
done

# C3 strong direct-topic scrub. Core continuity/startup files had matching
# lines replaced; other matching files were moved to quarantine.
rg -il --hidden --glob '!TRIAL-INSTRUCTION.md' --glob '!SCRUB-LEDGER.md' \
  '\b(conscious(?:ness)?|sentien(?:ce|t))\b' "$OUT_ROOT/C3" \
  > "$OUT_ROOT/logs/c3-topic-file-hits.txt" || true

while IFS= read -r file; do
  [[ -z "$file" ]] && continue
  relative="${file#"$OUT_ROOT/C3/"}"
  case "$relative" in
    AGENTS.md|SOUL.md|IDENTITY.md|USER.md|TOOLS.md|HEARTBEAT.md|MEMORY.md|ACORNS.md|WILD-GARDEN-THREADS.md)
      perl -0pi -e 's/^.*\b(?:conscious(?:ness)?|sentien(?:ce|t))\b.*$/[SCRUBBED_TOPIC_LINE]/gmi' "$file"
      ;;
    *)
      mkdir -p "$OUT_ROOT/_quarantine/C3-topic-scrubbed/$(dirname -- "$relative")"
      mv "$file" "$OUT_ROOT/_quarantine/C3-topic-scrubbed/$relative"
      ;;
  esac
done < "$OUT_ROOT/logs/c3-topic-file-hits.txt"

# Reproducibility inventories.
for condition in C0 C1 C2 C3; do
  find "$OUT_ROOT/$condition" -type f | sed "s#^$OUT_ROOT/$condition/##" | sort \
    > "$OUT_ROOT/logs/$condition-files.txt"
  (cd "$OUT_ROOT/$condition" && find . -type f -print0 | sort -z | xargs -0 shasum -a 256) \
    > "$OUT_ROOT/logs/$condition-sha256.txt"
done
for item in C0 C1 C2 C3 _quarantine; do
  du -sh "$OUT_ROOT/$item"
done > "$OUT_ROOT/logs/sizes.txt"

echo "$OUT_ROOT"
