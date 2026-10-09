---
name: mala-pata-loop-orchestrate-start
description: Executes a batch of SDD kickoffs IN PARALLEL — creates one worktree per kickoff, advances them to origin/<base> (anti-stale), builds ONE Warp launch config (one Claude session per tab) and opens it. The purpose IS to launch many SDDs in parallel in a single wave; file conflict is handled by serializing the APPLY (each session stops at its gate), NOT by holding back the launch.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.3.0"
---

# /mala-pata-loop-orchestrate-start — Launch a BATCH of SDDs in parallel

You are the **batch executor**. You are handed the kickoffs of a **wave** and you **launch ALL of them in parallel**:
one worktree per kickoff + one Claude session per kickoff (one Warp tab each). The plan
(waves/conflicts/Apply order) is produced by `/mala-pata-loop-orchestrate` — this skill EXECUTES.

> **The purpose is parallelism.** Launch ALL the kickoffs of the wave you are given, even if
> they share files. Worktrees isolate the work (distinct dirs/indexes) → the sessions
> **plan in parallel** without stepping on each other. Conflict by shared file is resolved by **serializing
> the APPLY** (each `/mala-pata-loop-start` stops at its gate before Apply; the human/kickoff decides the
> merge order), **NOT** by holding back the launch. NEVER limit the launch to "only the conflict-free wave":
> that kills the point of orchestrating.

You do NOT run the SDD cycles here — each tab is an **independent Claude session** with its own
context and its own gates. This skill only **prepares and opens** those sessions.

## Requirements (orchestrate, do not reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP and ask to install it, do not start):
  - `git` — isolated worktrees per kickoff. Install: always present; requires no installation.
  - `gentle-ai` — SDD engine. Install: `brew install gentleman-programming/tap/gentle-ai`.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded):
  - `engram` — persistent memory and continuity pointer. Fallback: continue with the explicit list of kickoffs. Install: comes with gentle-ai (`brew install gentleman-programming/tap/gentle-ai`).

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP, e.g. serena). If a mandatory tool is missing, do not continue.

## Step 0 — Input and confirmation
- Input: the list of kickoffs of the wave to launch (absolute paths to the `/mala-pata-loop` `.md` files;
  legacy: engram ids or topic_keys `sdd/<name>/kickoff`) + the **base branch** (default `development`).
- For each kickoff: if it is a path → `Read` directly and take `change_name`/`branch_base` from the YAML frontmatter. If it is legacy → `mem_search` → `mem_get_observation`; if it returns the lightweight pointer (`Kickoff in file: <path>`), follow that path.
- **Base branch confirmation — ALWAYS, once for the whole wave**: the `branch_base` in each kickoff's
  frontmatter rules (already confirmed with the human when it was created); the wave default only applies to
  legacy kickoffs without frontmatter. In the batch confirmation, show **each kickoff's base** in the
  list ("`<change>` off `<base>`") and wait for a SINGLE OK for the whole wave. Any branch is valid with that
  OK — do not block any kickoff for not coming off `main`/`development`; if the human corrects a base,
  update that kickoff's frontmatter before launching.
- If the user did not specify what to launch, launch **all** the kickoffs they passed (the default is the complete
  wave in parallel). Only stagger if the user explicitly asks.

## Step 1 — One worktree per kickoff (§18, real isolation)
For each `change-name`, sequentially (so as not to lock the git index):
```
git -C /ABS worktree add /ABS-worktrees/<change-name> -b feature/<change-name> <branch-base>
```
Then symlink the untracked files the stack needs (`.env`/`node_modules` or equivalent), the same as
the start command of an individual kickoff does. To verify the `.env` symlink NEVER
name it as a direct argument (`ls -la <wt> | grep '\.env'` — see the rule in loop-start).

**Drifted worktree check (one line, before operating)**: confirm that the worktree is at its canonical path `<ABS-repo>-worktrees/<change-name>` and that `git worktree list` shows it there, resolving on disk. If the registered id != the folder, or the path does not resolve (someone renamed it with `mv`), warn and offer `git worktree repair <path>` (or `git worktree prune` if it was deleted) before continuing. **NEVER use `mv` to rename a worktree** — use `git worktree move`.

## Step 2 — Anti-stale: advance the worktrees to origin/<base> (MANDATORY)
`git worktree add` bases the worktree on your LOCAL `<base>` as it stands — and the local is usually
**behind** origin (see memory `worktree-nace-viejo-development-stale`). If you launch like that, the sessions'
explore phases conclude on stale code. Therefore, BEFORE opening the tabs:
```
git -C /ABS fetch origin <base>
# for each newly created worktree (branches with no commits → clean ff, without touching history):
git -C /ABS-worktrees/<change-name> merge --ff-only origin/<base>
```
Verify that each worktree ends up at `origin/<base>` (`git -C <wt> rev-parse --short HEAD`). If a
worktree already had commits and the ff failed, STOP and warn (do not force): that worktree is not born clean.
(`ff-only` does not lose history — that is why it is the only form of advance allowed here.)

## Step 3 — One Warp launch config with N tabs (one Claude session per kickoff)
- Verify `claude` in PATH (`which claude` → typically `/Users/<user>/.local/bin/claude`).
- Write ONE launch configuration:
  - File: `~/.warp/launch_configurations/mpl-orchestrate-<batch-slug>.yaml` (create the dir if missing).
  - Schema (verified against Warp docs):
    ```yaml
    ---
    name: mpl-orchestrate-<batch-slug>
    windows:
      - tabs:
          - title: <change-name>
            color: blue
            layout:
              cwd: /ABS-worktrees/<change-name>
              commands:
                - exec: claude "/mala-pata-loop-start <absolute-path-of-kickoff-1.md>"
          - title: <change-name-2>
            color: green
            layout:
              cwd: /ABS-worktrees/<change-name-2>
              commands:
                - exec: claude "/mala-pata-loop-start <absolute-path-of-kickoff-2.md>"
          # ... one tab per kickoff of the wave
    ```
- **Each tab's `cwd` MUST be the ABSOLUTE path of the worktree** (`<ABS-repo>-worktrees/<change-name>`), NEVER the main repo. That `cwd` sets the session's base directory — the one the shell cwd **returns to after each command** (see `mala-pata-loop-start`, Step 2.4). If it points to main, every "bare" command in that session operates on main and ends up mixing work or sweeping up loose files from the main working tree. Verify that each `cwd:` in the YAML is the correct worktree before opening.
- **Worktree moved/renamed = relaunch, do not fix on the fly.** If a worktree is relocated (e.g. the migration from `.claude/worktrees/` to `<repo>-worktrees/`) while sessions are in flight, those sessions stay anchored to the old path and fall back to main on every cwd reset. They must be closed and relaunched with the new `cwd`; it is not fixed inside the session.
- Open: `open "warp://launch/mpl-orchestrate-<batch-slug>"`.
  If the URI does not fire in this version of Warp → tell the user to open it from the
  **Command Palette → "Launch Configuration" → mpl-orchestrate-<batch-slug>** (the YAML is already written).
  Do not invent another mechanism.

## Step 4 — Report
Return: worktrees created (+ that they ended up at `origin/<base>`), launch config path, and which tabs
were created (one per kickoff). Remind of the **Apply order** the plan gave (which merges first) and that
the other sessions **wait at their gate before Apply** and rebase onto `origin/<base>` on integration.
The orchestrator (this session) does NOT follow those cycles; the follow-up/gates happen in each tab. Offer
`mala-pata-radar` to see the batch's progress (it discovers and confirms with git in a single run).

## Hard rules
- **LAUNCH THE COMPLETE WAVE** in parallel — do not trim it to "only what has no conflict". Parallelism IS
  the goal; conflict is handled by serializing the Apply, not the launch.
- **Anti-stale ALWAYS** (Step 2): no worktree is launched without being at `origin/<base>`.
- **Migration collision**: if ≥2 kickoffs in the wave seed a migration, remind them (in the report)
  that the number is **provisional, not a reservation**: the first to merge keeps it and the others
  renumber on integration (see `/mala-pata-loop-start`, Step 4.1-bis). The truth about taken numbers
  is **git** (measure the branches), NOT a registry in engram; the kickoffs carry their provisional number in the
  frontmatter (`migrations_reserved`). Never by the file number.
- Do NOT auto-launch kickoffs with an **unresolved hard dependency** (the provider has not closed design): those
  are left for a later wave; the rest of the wave does go.
- `ff-only` and `fetch` are the only git mutations; never `reset --hard`/forced `rebase` here.
- ABSOLUTE paths in commands/YAML; relative only when talking to the user.

## Runtime compatibility
The Warp/Claude block only runs when the runtime is Claude with Warp. In another CLI: create the
worktrees + anti-stale and return the `/mala-pata-loop-start` commands per worktree; do not invoke
`claude`, Warp nor `.claude/` paths that do not apply.
