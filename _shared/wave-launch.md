# Wave launch — Warp tab configs, validated and verified (single source of truth)

Canonical procedure to open one Claude session per wave item (phase or kickoff), each in its own
worktree. Consumers: `mala-pata-roadmap-orchestrate-start`, `mala-pata-organic-orchestrate-start`.
Each consumer keeps ONLY its per-tab specifics (which prompt each tab runs) and points here.

Why tab configs and not launch configurations: the legacy launch-configuration YAML silently drops
the whole config when the YAML is invalid (an unquoted `exec:` value containing `: ` starts a new key),
and `open` still exits 0, so nothing opens and the caller cannot tell. Tab configs are TOML, the
format Warp recommends (https://docs.warp.dev/terminal/windows/tab-configs), and this procedure keeps
prompt text OUT of the file entirely, validates before opening, and verifies after. Never write a
launch-configuration YAML.

> `open` ALWAYS exits 0. The exit code is never proof of launch — only the sentinel (step 5) is.

## Inputs (from the consumer)

Per item: `<slug>`, `<worktree>` (ABSOLUTE path, never the main repo), and the prompt text the tab
runs. Plus one `<run-id>` for the round, UNIQUE per orchestration run (e.g.
`<roadmap-or-batch-slug>-r<N>-<epoch-seconds>`), so concurrent runs, or same-slug phases from
different repos, never share a file name.

## Procedure

1. **Prompt + sentinel files, outside every worktree.** Create `${TMPDIR:-/tmp}/mala-pata-launch/<run-id>/`.
   Write each tab's prompt verbatim to `<slug>.prompt`. The sentinel path is `<slug>.started` (not created
   yet). No prompt text is ever embedded in TOML — this removes the quoting bug class.
2. **Write the run-scoped tab config** `~/.warp/tab_configs/mpl-<run-id>-<slug>.toml` (create the dir if
   missing). Every path ABSOLUTE; no `[params]` table (it opens a modal):
   ```toml
   name = "mpl-<run-id>-<slug>"
   title = "<slug>"

   [[panes]]
   id = "main"
   type = "terminal"
   directory = "<worktree>"
   commands = ["touch '<sentinel>' && claude \"$(cat '<prompt-file>')\""]
   ```
3. **Validate BEFORE opening**, per file:
   `python3 -c 'import tomllib,sys; tomllib.load(open(sys.argv[1],"rb"))' <file>`.
   On failure: STOP, show the parser error, open nothing.
4. **Open serially**, short pause (~2s) between tabs: `open "warp://tab_config/mpl-<run-id>-<slug>"`.
   Default target is a new tab in the ACTIVE window; `?new_window=true` opens a new window instead.
5. **Verify each tab**: poll for `<sentinel>` up to a generous timeout (default ~60s; a cold Warp start
   can be slow). Optional extra evidence, never required: `warpctrl --output-format json tab list` (only
   if the user enabled Warp scripting and installed its control CLI).
6. **Late-start guard, then fallback per missing tab.** A timeout is NOT proof the tab failed to start.
   RIGHT BEFORE each fallback attempt (every one of (a), (b), (c) below), re-check BOTH: (i) the sentinel
   now exists, and (ii) a live `claude` process has the worktree as its cwd (for each pid of
   `pgrep -x claude`: `lsof -a -p <pid> -d cwd -Fn` shows `n<worktree>`). If either is true, mark the tab
   started (late), record the evidence, and do NOT fall back. NEVER relaunch into a worktree with a live
   session — two sessions in one worktree corrupt it. Only when both are false, in order:
   (a) retry once with `open "warp://tab_config/mpl-<run-id>-<slug>?new_window=true"`;
   (b) Terminal.app, with every path single-quoted exactly like the primary TOML command. Build the
   shell command in a variable and hand it to AppleScript as an ARGUMENT (`on run argv`), so no
   AppleScript string escaping of paths or quotes is ever needed. Exact template:
   ```
   CMD="cd '<worktree>' && touch '<sentinel>' && claude \"\$(cat '<prompt-file>')\""
   osascript -e 'on run argv' -e 'tell application "Terminal" to do script (item 1 of argv)' -e 'end run' "$CMD"
   ```
   A path containing a single quote is written `'\''` inside the single-quoted segment. The prompt
   never appears in the command (it is read from `<prompt-file>`);
   (c) report the exact command for the human to paste.
7. **Cleanup**: after verification delete ONLY this run's `~/.warp/tab_configs/mpl-<run-id>-*.toml`
   files (one-shot; keeps the Tab Config menu clean and never touches another run's files). Keep the
   prompt and sentinel files until the wave closes.
8. **Report** one row per tab, labels verbatim in English (rule: `structural-labels.md`):

   | Slug | Worktree | Launch | Evidence |
   |---|---|---|---|

   `Launch` ∈ `warp-tab | warp-window | terminal | manual`. `Evidence` = `sentinel` (+ extra if any;
   `sentinel (late)` or `claude cwd (late)` when step 6 caught a late start) or `none — paste command`.

## Rules

- Frozen label set for the report: `Slug`, `Worktree`, `Launch`, `Evidence`; enum `warp-tab`, `warp-window`, `terminal`, `manual`.
- A tab is launched only after its TOML parsed. A tab is reported launched only after its sentinel exists.
- Not Claude + Warp (another CLI/terminal): skip this procedure; return the per-worktree commands.
