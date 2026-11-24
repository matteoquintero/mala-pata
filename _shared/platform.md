# Platform primitives — macOS + Linux (single source of truth)

Every mala-pata skill that runs an OS-dependent command names a PRIMITIVE from this file instead of
hard-coding one platform's command. Detect the platform ONCE per run with `uname -s`:

- `Darwin` → macOS column.
- `Linux` → Linux column (validated target: Ubuntu).
- anything else → unsupported: do not guess; print the exact manual commands for the human.

> **Linux branch status: PROVISIONAL** for the Warp rows (`<warp-open>`, `<warp-tab-dir>`) until a
> human probe on Ubuntu confirms them (see "Linux probe" below). The other rows use standard tools.

## Primitives

| Primitive | macOS (`Darwin`) | Linux (`Linux`) |
|---|---|---|
| `<opener>` — open a folder, file or URI | `open <target>` | `xdg-open <target>` |
| `<warp-open>` — open a Warp URI | `open "<warp-uri>"` | `xdg-open "<warp-uri>"` |
| `<warp-tab-dir>` — Warp tab-config folder | `~/.warp/tab_configs/` | `${XDG_DATA_HOME:-$HOME/.local/share}/warp-terminal/tab_configs/` (`warp-terminal-preview` for preview builds) |
| `<terminal-fallback>` — run `$CMD` in a new native terminal window | `osascript -e 'on run argv' -e 'tell application "Terminal" to do script (item 1 of argv)' -e 'end run' "$CMD"` | first available: `gnome-terminal -- bash -lc "$CMD; exec bash"`, else `x-terminal-emulator -e bash -lc "$CMD; exec bash"`; none → skip to the manual step |
| `<proc-cwd> <pid>` — a process's working directory | `lsof -a -p <pid> -d cwd -Fn` (line starting `n`) | `readlink /proc/<pid>/cwd` |
| `<toml-check> <file>` — parse-validate a TOML file | `python3 -c 'import tomllib,sys; tomllib.load(open(sys.argv[1],"rb"))' <file>` | same; needs Python ≥ 3.11 (`tomllib`). On older Python try `tomli` (`import tomli as tomllib`); if neither imports, STOP and report "TOML validation unavailable — install Python ≥ 3.11 or `pip install tomli`". Never open an unvalidated config. |
| `<install> <pkg>` — install a CLI dependency | `brew install <pkg>` | `brew install <pkg>` with Homebrew on Linux (the `gentleman-programming/tap/gentle-ai` formula ships `linux_amd64` / `linux_arm64` builds), or the distro package (`sudo apt install gh`) |

Tool facts both columns rely on: `open` / `xdg-open` exit 0 even when nothing opens, so their exit code
is never proof of anything; `pgrep`, `readlink`, `bash`, `git`, `rsync` exist on both.

## Rules

- A skill writes the primitive name (`<opener> <ABS-path>`), never `open`, `xdg-open`, `osascript`,
  `~/.warp`, `lsof` or `/proc` directly. The ONLY file allowed to spell those is this one.
- A `brew install <pkg>` line in a skill's Requirements is acceptable on both platforms (Homebrew runs on
  Linux); the Linux alternative is listed here, not repeated per skill.
- When a report hands the human a copy-paste command, emit the RESOLVED command for the detected
  platform (e.g. `xdg-open /abs/path` on Linux), not the primitive name.

## Concurrency lock — atomic `mkdir` (both platforms)

A shared action only ONE actor may do at a time (a per-worktree merge/cleanup, the single central
suite-run owner, a sub-agent dedup slot) uses an ATOMIC lock, NEVER an advisory check-then-act (a
sentinel + `lsof` heuristic races in the window between the check and the act). `mkdir` is atomic on
macOS and Linux: it either creates the dir (you hold the lock) or fails because it exists (another
holds it) — one syscall, no window.

| Primitive | Both platforms |
|---|---|
| `<lock-acquire> <lockdir>` | `mkdir "<lockdir>" 2>/dev/null` — exit 0 = ACQUIRED; non-zero = held by another. On acquire, write `<lockdir>/owner` = `<pid> <ISO-8601> <run-token>`. |
| `<lock-release> <lockdir>` | `rm -rf "<lockdir>"` — only the holder releases; never release a lock you did not acquire (check `<lockdir>/owner` carries your `run-token` first). |
| `<lock-stale?> <lockdir>` | reclaimable when the owner pid is dead (`kill -0 <pid>` fails) OR the lock is older than its TTL (`owner` mtime + TTL < now). Reclaim with `rm -rf`, then retry `<lock-acquire>` ONCE. |

Rules:
- NEVER check-then-mkdir ("if not exists, mkdir") — that reintroduces the race. The `mkdir` IS the test.
- The lockdir lives beside the resource it guards (`<ABS-worktree>/mala-pata/.lock-<action>`), is
  transient (never committed; excluded like `.phase-status.json`), and names the action.
- `run-token` is unique per run (`date +%s`-`$$`-`$RANDOM`) so an owner proves a lock is its own before
  releasing, and a reclaimed-then-reacquired lock is distinguishable.
- A crashed holder leaves a stale lock; the `<lock-stale?>` reclaim (dead pid OR TTL) prevents a
  permanent wedge. Default TTL = the action's generous expected max (minutes), never seconds.

## Linux probe (human-run, once per machine; flips the PROVISIONAL status)

On Ubuntu with Warp installed and one Warp window open:

1. Write `<warp-tab-dir>mpl-probe.toml` with `name = "mpl-probe"`, `color = "red"`, one `[[panes]]`
   whose `commands = ["touch /tmp/mpl-probe.started"]`; validate it with `<toml-check>`.
2. `xdg-open "warp://tab_config/mpl-probe"` → expect a NEW TAB in the ACTIVE window, red, and the
   sentinel `/tmp/mpl-probe.started` within ~60s.
3. Repeat with `?new_window=true` → expect a new window.
4. Run the `<terminal-fallback>` with `CMD='touch /tmp/mpl-probe.fallback'` → expect the file.
5. Delete the probe files. Record the result (date + Warp version) in the commit that removes the
   PROVISIONAL marker.
