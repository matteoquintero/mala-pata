#!/usr/bin/env bash
#
# mala-pata-notify installer — agent-agnostic desktop notifications.
#
# Installs the shared entrypoint to ~/.mala-pata/bin and wires every AI CLI it
# detects (Claude Code, Codex, Kimi Code, Gemini, OpenCode) to call it on
# "finished" and "waiting" events. Idempotent: safe to re-run — already-wired
# agents are left untouched.
#
# Prerequisite: the overlay binary + session-name resolver. By default the
# entrypoint looks for ~/.claude/hooks/malapata_overlay (override with
# MALAPATA_OVERLAY_BIN). Without it, notifications are silent no-ops.
#
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.mala-pata/bin"
NOTIFY="$BIN_DIR/mala-pata-notify"

echo "mala-pata-notify installer"
echo "→ entrypoint: $NOTIFY"
mkdir -p "$BIN_DIR"
cp "$SRC_DIR/mala-pata-notify" "$NOTIFY"
chmod +x "$NOTIFY"

# --- Claude Code: ~/.claude/settings.json (hooks: Stop + Notification) ---
CLAUDE="$HOME/.claude/settings.json"
if [ -f "$CLAUDE" ]; then
  NOTIFY="$NOTIFY" python3 - "$CLAUDE" <<'PY'
import json, os, sys
p = sys.argv[1]; N = os.environ["NOTIFY"]
d = json.load(open(p)); h = d.setdefault("hooks", {})
def has(ev): return any("mala-pata-notify" in k.get("command", "") for g in h.get(ev, []) for k in g.get("hooks", []))
ch = 0
if not has("Stop"):
    h.setdefault("Stop", []).append({"hooks": [{"type": "command", "command": f"{N} --event finished --agent claude-code"}]}); ch += 1
if not has("Notification"):
    h.setdefault("Notification", []).append({"hooks": [{"type": "command", "command": f"{N} --event waiting --agent claude-code"}]}); ch += 1
if ch:
    json.dump(d, open(p, "w"), indent=2, ensure_ascii=False); open(p, "a").write("\n")
print(f"  claude-code: {'wired ('+str(ch)+')' if ch else 'already wired'}")
PY
else echo "  claude-code: not found (skip)"; fi

# --- Codex: ~/.codex/hooks.json (Stop + PermissionRequest) ---
CODEX="$HOME/.codex/hooks.json"
if [ -f "$CODEX" ]; then
  NOTIFY="$NOTIFY" python3 - "$CODEX" <<'PY'
import json, os, sys
p = sys.argv[1]; N = os.environ["NOTIFY"]
d = json.load(open(p)); h = d.setdefault("hooks", {})
def has(ev): return any("mala-pata-notify" in k.get("command", "") for g in h.get(ev, []) for k in g.get("hooks", []))
ch = 0
if not has("Stop"):
    h.setdefault("Stop", []).append({"hooks": [{"type": "command", "command": f"{N} --event finished --agent codex", "timeout": 5}]}); ch += 1
if not has("PermissionRequest"):
    h.setdefault("PermissionRequest", []).append({"hooks": [{"type": "command", "command": f"{N} --event waiting --agent codex", "timeout": 5}]}); ch += 1
if ch:
    json.dump(d, open(p, "w"), indent=2, ensure_ascii=False); open(p, "a").write("\n")
print(f"  codex: {'wired ('+str(ch)+') — Codex may prompt to trust hooks on next launch' if ch else 'already wired'}")
PY
else echo "  codex: not found (skip)"; fi

# --- Kimi Code: ~/.kimi-code/config.toml (append [[hooks]]) ---
KIMI="$HOME/.kimi-code/config.toml"
if [ -f "$KIMI" ]; then
  if grep -q "mala-pata-notify" "$KIMI"; then
    echo "  kimi: already wired"
  else
    cat >> "$KIMI" <<EOF

[[hooks]]
event = "Stop"
command = "$NOTIFY --event finished --agent kimi"
timeout = 5

[[hooks]]
event = "PermissionRequest"
command = "$NOTIFY --event waiting --agent kimi"
timeout = 5
EOF
    echo "  kimi: wired"
  fi
else echo "  kimi: not found (skip)"; fi

# --- Gemini: ~/.gemini/settings.json (AfterAgent + Notification) ---
GEMINI="$HOME/.gemini/settings.json"
if [ -f "$GEMINI" ]; then
  NOTIFY="$NOTIFY" python3 - "$GEMINI" <<'PY'
import json, os, sys
p = sys.argv[1]; N = os.environ["NOTIFY"]
d = json.load(open(p)); h = d.setdefault("hooks", {})
def has(ev): return any("mala-pata-notify" in k.get("command", "") for g in h.get(ev, []) for k in g.get("hooks", []))
ch = 0
if not has("AfterAgent"):
    h.setdefault("AfterAgent", []).append({"hooks": [{"type": "command", "command": f"{N} --event finished --agent gemini", "timeout": 5000}]}); ch += 1
if not has("Notification"):
    h.setdefault("Notification", []).append({"hooks": [{"type": "command", "command": f"{N} --event waiting --agent gemini", "timeout": 5000}]}); ch += 1
if ch:
    json.dump(d, open(p, "w"), indent=2, ensure_ascii=False); open(p, "a").write("\n")
print(f"  gemini: {'wired ('+str(ch)+')' if ch else 'already wired'}")
PY
else echo "  gemini: not found (skip)"; fi

# --- OpenCode: drop the JS plugin shim ---
OC_PLUGINS="$HOME/.config/opencode/plugins"
if [ -d "$OC_PLUGINS" ]; then
  cp "$SRC_DIR/adapters/opencode/mala-pata-notify.ts" "$OC_PLUGINS/mala-pata-notify.ts"
  echo "  opencode: plugin installed"
else echo "  opencode: not found (skip)"; fi

echo "done."
