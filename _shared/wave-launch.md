# Wave launch — Warp tab configs, validated and verified (single source of truth)

Canonical procedure to open one agent session per wave item (phase or kickoff), each in its own
worktree, on macOS or Linux. Consumers: `mala-pata-roadmap-orchestrate-start`,
`mala-pata-organic-orchestrate-start`. Each consumer keeps ONLY its per-tab specifics (which prompt
each tab runs) and points here. Every OS-dependent command below is a primitive from
`platform.md` (`<warp-open>`, `<warp-tab-dir>`, `<terminal-fallback>`, `<proc-cwd>`, `<toml-check>`);
detect the platform once with `uname -s` and resolve them there.

Why tab configs and not launch configurations: the legacy launch-configuration YAML silently drops
the whole config when the YAML is invalid (an unquoted `exec:` value containing `: ` starts a new key),
and the opener still exits 0, so nothing opens and the caller cannot tell. Tab configs are TOML, the
format Warp recommends (https://docs.warp.dev/terminal/windows/tab-configs), and this procedure keeps
prompt text OUT of the file entirely, validates before opening, and verifies after. Never write a
launch-configuration YAML.

> `<warp-open>` ALWAYS exits 0. The exit code is never proof of launch — only the sentinel (step 5) is.

## Agents (command + tab color)

The tab runs ONE agent CLI, chosen by `<agent>` (default `claude`; the consumer passes the agent the
orchestrator itself runs on). The tab color identifies the agent, never the wave, lane or phase:

| Agent | Tab command (`<agent-cmd>`) | Process match (late-start guard) | Tab `color` |
|---|---|---|---|
| `claude` | `claude --model <model> "$(cat '<prompt-file>')"` | `pgrep -x claude` | `red` |
| `codex` | `codex -c model_reasoning_effort=<effort> "$(cat '<prompt-file>')"` | `pgrep -f codex` (the cwd check filters false hits) | `white` |

`<model>` (Claude) / `<effort>` (Codex) is resolved from the item's phase TIER per `model-policy.md`
(project `model_tiers` override → shipped default). If the consumer cannot resolve a tier for an item,
it passes NO model/effort for that item and the flag is OMITTED entirely (the tab runs on the agent's
own session default) — fail-open, never guess a model.

An agent not in this table → skip this procedure and return the per-worktree commands. Warp accepts
only `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white` as `color` (the shade comes
from the active theme; no hex, no per-tab background); never write any other value.

## Inputs (from the consumer)

Per item: `<slug>`, `<worktree>` (ABSOLUTE path, never the main repo), the prompt text the tab runs, and
`<model>`/`<effort>` resolved from the item's phase tier (per `model-policy.md`; omit when the tier is
unknown). Plus `<agent>` (default `claude`) and one `<run-id>` for the round, UNIQUE per orchestration run
(e.g. `<roadmap-or-batch-slug>-r<N>-<epoch-seconds>`), so concurrent runs, or same-slug phases from
different repos, never share a file name.

## Procedure

1. **Prompt + sentinel files, outside every worktree.** Create `${TMPDIR:-/tmp}/mala-pata-launch/<run-id>/`.
   Write each tab's prompt verbatim to `<slug>.prompt`. The sentinel path is `<slug>.started` (not created
   yet). No prompt text is ever embedded in TOML — this removes the quoting bug class.
2. **Write the run-scoped tab config** `<warp-tab-dir>mpl-<run-id>-<slug>.toml` (create the dir if
   missing). Every path ABSOLUTE; no `[params]` table (it opens a modal); `color` from the Agents table:
   ```toml
   name = "mpl-<run-id>-<slug>"
   title = "<slug>"
   color = "<agent-color>"

   [[panes]]
   id = "main"
   type = "terminal"
   directory = "<worktree>"
   commands = ["touch '<sentinel>' && <agent-cmd>"]
   ```
   `<agent-cmd>` keeps its inner double quotes escaped inside the TOML string, e.g. for claude:
   `commands = ["touch '<sentinel>' && claude --model <model> \"$(cat '<prompt-file>')\""]`
   (omit `--model <model>` when no tier resolved; the codex row uses `-c model_reasoning_effort=<effort>`).
3. **Validate BEFORE opening**, per file: `<toml-check> <file>`. On a parse failure: STOP, show the
   parser error, open nothing. Validation unavailable (no `tomllib`/`tomli`) is also a STOP.
4. **Open serially**, short pause (~2s) between tabs: `<warp-open> "warp://tab_config/mpl-<run-id>-<slug>"`.
   Default target is a new tab in the ACTIVE window; `?new_window=true` opens a new window instead.
5. **Verify each tab**: poll for `<sentinel>` up to a generous timeout (default ~60s; a cold Warp start
   can be slow). Optional extra evidence, never required: `warpctrl --output-format json tab list` (only
   if the user has Warp's control CLI; it is not generally available).
6. **Late-start guard, then fallback per missing tab.** A timeout is NOT proof the tab failed to start.
   RIGHT BEFORE each fallback attempt (every one of (a), (b), (c) below), re-check BOTH: (i) the sentinel
   now exists, and (ii) a live agent process has the worktree as its cwd (for each pid of the agent's
   process match: `<proc-cwd> <pid>` equals `<worktree>`). If either is true, mark the tab started
   (late), record the evidence, and do NOT fall back. NEVER relaunch into a worktree with a live
   session — two sessions in one worktree corrupt it. Only when both are false, in order:
   (a) retry once with `<warp-open> "warp://tab_config/mpl-<run-id>-<slug>?new_window=true"`;
   (b) `<terminal-fallback>`, with every path single-quoted exactly like the primary TOML command. Build
   the shell command in a variable and pass it as ONE argument, so no escaping of paths or quotes for the
   terminal is ever needed:
   ```
   CMD="cd '<worktree>' && touch '<sentinel>' && <agent-cmd>"
   ```
   with `<agent-cmd>` written as `claude \"\$(cat '<prompt-file>')\"` (or the codex row). A path
   containing a single quote is written `'\''` inside the single-quoted segment. The prompt never
   appears in the command (it is read from `<prompt-file>`). No native terminal available → (c);
   (c) report the exact command for the human to paste.
7. **Cleanup**: after verification delete ONLY this run's `<warp-tab-dir>mpl-<run-id>-*.toml`
   files (one-shot; keeps the Tab Config menu clean and never touches another run's files). Keep the
   prompt and sentinel files until the wave closes.
8. **Report** one row per tab, labels verbatim in English (rule: `structural-labels.md`):

   | Slug | Worktree | Launch | Evidence |
   |---|---|---|---|

   `Launch` ∈ `warp-tab | warp-window | terminal | manual`. `Evidence` = `sentinel` (+ extra if any;
   `sentinel (late)` or `<agent> cwd (late)` when step 6 caught a late start) or `none — paste command`.

## Rules

- Frozen label set for the report: `Slug`, `Worktree`, `Launch`, `Evidence`; enum `warp-tab`, `warp-window`, `terminal`, `manual`.
- A tab is launched only after its TOML parsed. A tab is reported launched only after its sentinel exists.
- Tab color = the agent (Agents table), nothing else. One agent per tab.
- Agent not in the Agents table, terminal not Warp, or platform neither macOS nor Linux: skip this
  procedure; return the per-worktree commands.
- On Linux the Warp rows of `platform.md` are PROVISIONAL until its Linux probe passes; the sentinel
  check still decides every launch, so an unconfirmed path degrades to the fallback, never to a silent
  failure.
