# mala-pata-notify

Agent-agnostic desktop notifications for AI coding CLIs. One shared entrypoint
every CLI calls from its own hook/notify mechanism, so you get the **same**
overlay + sound whether the agent is Claude Code, Codex, Kimi Code, Gemini or
OpenCode — on two events:

- **finished** — the agent ended its turn (sound: `Frog`).
- **waiting** — the agent is blocked waiting on you: a permission/approval
  prompt or review consent (sound: `Funk`).

## Why

Most CLIs notify on "done" but not on "waiting for you". A review-consent prompt
(e.g. gentle-ai RDD) blocks mid-turn and never fires a "finished" hook, so you
sit unaware. This wires the **waiting** event too, across every agent.

## Layout

| Path | What |
|---|---|
| `mala-pata-notify` | the entrypoint (python) — the source of truth |
| `adapters/opencode/mala-pata-notify.ts` | OpenCode plugin shim (no declarative hook) |
| `snippets/` | per-agent config fragments for manual install |
| `install.sh` | copies the entrypoint and wires every detected CLI (idempotent) |

## Install

```bash
./install.sh
```

It installs `mala-pata-notify` to `~/.mala-pata/bin/` and wires each CLI it
finds. Re-running is safe — already-wired agents are skipped.

## How it works

```
<agent hook/plugin>  →  mala-pata-notify --event finished|waiting --agent <x>  →  overlay + sound
```

The entrypoint:

- reads the agent's payload from **stdin JSON** (or `--argv-json '<json>'` for
  Codex's legacy notify / OpenCode's shim);
- prints **nothing** to stdout and **always exits 0**, so it never pollutes a
  host that parses hook stdout (Gemini, Kimi) nor blocks a blockable Stop hook;
- fires the overlay + sound **detached** (`start_new_session`) so they survive
  the hook process exiting.

**Identity** (what the overlay shows):

- *Universal fallback* (works for every agent, since every payload carries
  `cwd`): `basename(cwd)` + git branch + agent + `HH:MM`.
- *Per-agent enricher*: `claude-code` reuses the existing
  `malapata_session_name.py` for its richer line (session name + last prompt).
  Other agents can get their own enricher later.

## Per-agent wiring

| Agent | Config | finished | waiting | Input |
|---|---|---|---|---|
| Claude Code | `~/.claude/settings.json` | `Stop` | `Notification` | stdin JSON |
| Codex | `~/.codex/hooks.json` | `Stop` | `PermissionRequest` | stdin JSON |
| Kimi Code | `~/.kimi-code/config.toml` | `Stop` | `PermissionRequest` | stdin JSON |
| Gemini | `~/.gemini/settings.json` | `AfterAgent` | `Notification` | stdin JSON |
| OpenCode | plugin `mala-pata-notify.ts` | `session.idle` | `permission.asked` | argv-json (shim) |

## Caveats

- **Codex** — editing `hooks.json` changes its `trusted_hash`; Codex may prompt
  to re-trust the hooks on next launch. Until approved, they do not run.
- **Gemini** — has no generic "idle" event. `waiting` fires on **any**
  `Notification`, not only tool-permission, so it can over-fire.
- **OpenCode** — needs the JS plugin shim (no declarative command hook).
- **Hard floor** — a CLI that emits no hook/notify/event cannot be wired.

## Prerequisite: the overlay

The entrypoint shells out to an overlay binary + a session-name resolver. By
default:

- `MALAPATA_OVERLAY_BIN` → `~/.claude/hooks/malapata_overlay`
- `MALAPATA_SND_FINISHED` → `/System/Library/Sounds/Frog.aiff`
- `MALAPATA_SND_WAITING` → `/System/Library/Sounds/Funk.aiff`

All overridable via env. Without the overlay binary, the entrypoint is a safe
no-op (it never errors). macOS only (`afplay` + a Mach-O overlay).
