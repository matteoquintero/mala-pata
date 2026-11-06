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
runs. Plus one `<run-id>` for the round (e.g. `<roadmap-or-batch-slug>-r<N>`).

## Procedure

1. **Prompt + sentinel files, outside every worktree.** Create `${TMPDIR:-/tmp}/mala-pata-launch/<run-id>/`.
   Write each tab's prompt verbatim to `<slug>.prompt`. The sentinel path is `<slug>.started` (not created
   yet). No prompt text is ever embedded in TOML — this removes the quoting bug class.
2. **Write the tab config** `~/.warp/tab_configs/mpl-<slug>.toml` (create the dir if missing). Every path
   ABSOLUTE; no `[params]` table (it opens a modal):
   ```toml
   name = "mpl-<slug>"
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
4. **Open serially**, short pause (~2s) between tabs: `open "warp://tab_config/mpl-<slug>"`. Default
   target is a new tab in the ACTIVE window; `?new_window=true` opens a new window instead.
5. **Verify each tab**: poll for `<sentinel>` up to a timeout (~30s). It appears seconds after the tab
   starts. Optional extra evidence, never required: `warpctrl --output-format json tab list` (only if the
   user enabled Warp scripting and installed its control CLI), or a `claude` process whose cwd is the
   worktree (`lsof -a -p <pid> -d cwd`).
6. **Fallback per missing tab**, in order: (a) retry once with `open "warp://tab_config/mpl-<slug>?new_window=true"`;
   (b) Terminal.app: `osascript -e 'tell application "Terminal" to do script "cd <worktree> && touch <sentinel> && claude \"$(cat <prompt-file>)\""'`;
   (c) report the exact command for the human to paste. **NEVER relaunch a tab whose sentinel exists** —
   two sessions in one worktree corrupt it.
7. **Cleanup**: after verification delete the `mpl-<slug>.toml` files (one-shot; keeps the Tab Config
   menu clean). Keep the prompt and sentinel files until the wave closes.
8. **Report** one row per tab, labels verbatim in English (rule: `structural-labels.md`):

   | Slug | Worktree | Launch | Evidence |
   |---|---|---|---|

   `Launch` ∈ `warp-tab | warp-window | terminal | manual`. `Evidence` = `sentinel` (+ extra if any) or
   `none — paste command`.

## Rules

- Frozen label set for the report: `Slug`, `Worktree`, `Launch`, `Evidence`; enum `warp-tab`, `warp-window`, `terminal`, `manual`.
- A tab is launched only after its TOML parsed. A tab is reported launched only after its sentinel exists.
- Not Claude + Warp (another CLI/terminal): skip this procedure; return the per-worktree commands.
