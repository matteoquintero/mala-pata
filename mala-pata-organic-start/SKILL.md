---
name: mala-pata-organic-start
description: Runs the ODD (Organic Driven Development) CYCLE from the path of the kickoff that `/mala-pata-organic` left — worktree+base → explore (this is where the Where is discovered) → resolve uncertainty → classify → (feature-doc if substantial) → implement task-by-task (work-unit commit + RDD per commit) → close (PR/CI/cleanup) → table. The init (`sdd-init`) is guaranteed by `/mala-pata-organic` (once per project). Uses ODD workers (direct/delegated), NEVER `sdd-*` agents — the gentle-ai `PreToolUse:Agent` preflight hook does not apply here. For small work, the phases run in a single pass; the separate kickoff exists for review/handoff, same as in the loop/loop-start pair.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.6.0"
---

# /mala-pata-organic-start — Runs the ODD CYCLE from a kickoff file

Kickoff: **input delivered by the CLI** (absolute path to the `.md` file left by `/mala-pata-organic`)

Your job: read the kickoff and run the **native gentle-ai ODD cycle**, organized into the mala-pata flow — isolated worktree, human gates where appropriate, final table. It is to ODD what `/mala-pata-loop-start` is to SDD: **you do not reimplement ODD — you orchestrate it.**

> **The ODD protocol is the source of truth.** Its 7 steps (Authorize → Explore → Resolve → Classify → Track → Implement → Close), the feature-doc, the work-unit commits, the RDD evaluation per commit and the delivery slicing live in your **global CLAUDE.md** (`## Implementation Routing → ### ODD protocol`). This skill follows them and adds the mala-pata layer. If the CLAUDE.md and this skill differ on ODD mechanics, **the CLAUDE.md wins**.

> **Uses ODD workers (direct inline / delegated direct), NEVER `sdd-*` agents.** The gentle-ai `PreToolUse:Agent` preflight (`gentle-ai sdd-preflight-hook`) only intercepts `sdd-*` dispatches — it does not apply to this skill. Do not ask the canonical 3-question preflight here: it does not exist for this lane.

> **Proportionality**: for a small, already-understood change, the phases below run in a single pass (explore → implement → close) without ceremonial pauses — the kickoff/start separation exists to give a review/handoff point between "what is going to be done" and "doing it", same as in the `mala-pata-loop`/`mala-pata-loop-start` pair, not to force bureaucracy on small things.

## Requirements (orchestrate, do not reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP and ask to install it, do not start):
  - `gentle-ai` — ODD engine + RDD per commit. Install: `brew install gentleman-programming/tap/gentle-ai`.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded):
  - `codegraph` — code graph (anchoring and structure). Fallback: grep/Read. Install: global npm CLI; per-project init with `gentle-ai codegraph init --cwd <repo>`.
  - `serena` — explore and edit code. Fallback: codegraph/grep. Install: `uv tool install -p 3.13 serena-agent && serena setup claude-code`.
  - `engram` — persistent memory and continuity pointer. Fallback: continue without a pointer; the kickoff file is the source. Install: comes with gentle-ai (`brew install gentleman-programming/tap/gentle-ai`).

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP, e.g. serena). If a mandatory tool is missing, do not continue.

## Hard rules

> **#1 — ALWAYS your own worktree + your own new branch. It is NOT negotiable and the kickoff CANNOT override it.** organic runs in a worktree DEDICATED to this change, on a NEW branch `<type>/<change-name>` created off the `base`. **NEVER work in-place on an integration/shared branch nor reuse another feature's worktree — even if the kickoff says `branch: <integration>` or `worktree: <reuse/existing>`.** If the kickoff says that, it is WRONG: derive `<type>/<change-name>` off the declared base, create a fresh worktree of your own, and say in one line that you corrected the kickoff. The **base** does come from the kickoff as-is (it may be `main`/`development` or a feature in progress — you branch off it and consolidate at merge on close; what is NEVER reused is the working worktree/branch). **Resume exception**: if ESTE change's OWN worktree (same change-name) already exists from a previous run, reuse THAT one. If the kickoff does not carry a complete `base`, STOP and ask the orchestrator for it.
> **#2 — RDD lives here, per work-unit commit.** After each commit, if RDD is on, run `gentle-ai review assess` and follow the native plan (see ODD protocol). It is NOT a gate at the end — it is **per-commit**.
> **#3 — Absolute paths ALWAYS** (the cwd resets between commands to your base dir, which is usually the main repo): `git -C <ABS-worktree> …`, never bare commands; before ANY write/commit, `git -C <ABS-worktree> rev-parse --show-toplevel` must return the worktree, not main.
> **#4 — Do not implement before Exploring and Classifying.** The phase plan below goes in order: worktree → explore → classify → (track if substantial) → implement. Do not jump to writing code "to figure it out as you go" before those steps, even if the change seems small and obvious.

## Step 1 — Load the kickoff + engram context

1. The input is an **absolute path to an `.md` file** (the one `/mala-pata-organic` wrote in `mala-pata/kickoffs/<change-name>.md`, inside the repo). If it does not start with `/` or the file does not exist → **STOP** and ask for the correct path. Do not invent the context.
2. `Read` in full: frontmatter (`change_name`, `project`, `route: organic`, `base`, `branch`, `worktree`, `tdd_mode`) and body (What, Why, Done, Decisions already made, Risk, Where-hint).
3. If `route` is not `organic` → **STOP**: this kickoff is not for this skill (it is probably a `/mala-pata-loop` kickoff, which uses `/mala-pata-loop-start`).
4. `mem_search("odd/<change_name>/kickoff")` only to confirm the pointer — it is not blocking if it fails, the file is already the source of truth.

## Step 2 — Worktree + base (ODD Phase 1 of the mala-pata layer — Hard rule #1)

1. **Worktree + branch ALWAYS your own (Hard rule #1) — the kickoff does NOT override it.** The working branch is `<type>/<change-name>` (new, from the change-name; never an integration branch) and the worktree is the dedicated dir `<ABS-repo>-worktrees/<change-name>`. **Does THAT own worktree already exist** (same change-name) from a previous run and are you in it? → resume: skip to point 4. If the kickoff points to a shared worktree/branch (another feature or an integration branch) → ignore it, use your own and say in one line that you corrected the kickoff.
2. If your own worktree does not exist → create it off the kickoff's `base` (the base does come from the kickoff as-is; it may be `main`/`development` or a feature in progress):
   ```bash
   git -C <ABS-repo> worktree add <ABS-repo>-worktrees/<change-name> -b <type>/<change-name> <base-from-kickoff>
   ln -s <ABS-repo>/.env <ABS-repo>-worktrees/<change-name>/.env && ln -s <ABS-repo>/node_modules <ABS-repo>-worktrees/<change-name>/node_modules
   # (ajustar symlinks al stack real del proyecto)
   ```
3. **ABSOLUTE paths ALWAYS** (Hard rule #3) — every `git`/`npm`/read/write references the worktree by absolute path (`git -C <ABS-worktree> …`, `npm --prefix <ABS-worktree> …`). Before any write: `git -C <ABS-worktree> rev-parse --show-toplevel` must return the worktree.
3.5. **Drifted worktree check (one line, before operating)**: confirm that the worktree is at its canonical path `<ABS-repo>-worktrees/<change-name>` and that `git worktree list` shows it there, resolving on disk. If the registered id != the folder, or the path does not resolve (someone renamed it with `mv`), warn and offer `git worktree repair <path>` (or `git worktree prune` if it was deleted) before continuing. **NEVER use `mv` to rename a worktree** — use `git worktree move`.
4. **Init guard**: `mem_search("sdd-init/{project}")` — keep only the EXACT item. If it does not exist → warn the orchestrator; do not run the init here (`/mala-pata-organic` already guarantees it). With the exact item, confirm `strict_tdd` against the kickoff's `tdd_mode` — if they differ, the one from `sdd-init` wins (it is the live source).

## Step 3 — Explore + resolve uncertainty (ODD 2-3 — **this is where the Where is discovered**)

Explore the code and requirements **proportionally to the request** before writing a line. The kickoff carries a `Where (optional hint)` — it may be empty or just a hint; **this step is what confirms or completes it**, never a prior precondition. Record the files/modules touched: they go in the feature-doc (Step 5) if the work is substantial, or stay in the closing summary if it is small.

Optional research only for a **named uncertainty**; 1 question to the human only for a **real product decision** (then stop and wait); at most **one** read-only assumption-challenge for a high-impact premise. Do not invent scope beyond the What/Done/Decisions the kickoff already carries — those already passed the gate in `/mala-pata-organic`.

## Step 4 — Classify (ODD 4)

**Substantial** = 2+ meaningful implementation steps, or progress worth recovering after an interruption. **Small and understood** = stays small, no durable artifacts — go straight on to Step 6.

## Step 5 — Track (ODD 5 — only if substantial)

Before the first write: create `mala-pata/odd/<change_name>.md` + its engram mirror `odd/<change_name>/tasks` (automatic, without asking permission for tasks/storage). **The kickoff's `Why` FLOWS into the feature-doc** (motivation/context section). Say in **1 line** which feature-doc you created and how many tasks it has. (Content and contract of the doc: ODD protocol in the CLAUDE.md.)

## Step 6 — Implement task-by-task (ODD 6)

For each task: the **smallest topology** — direct inline (1-3 already-understood files) / delegated direct (understand 4+ or write 2+ non-trivial) — with the **project's TDD mode** (`strict_tdd` from sdd-init) and the applicable checks. Check off the task only after **observing** its result + checks; update the feature-doc and the mirror.
- **Each task closes with ≥1 work-unit commit on the feature branch**, with tests+docs alongside the behavior, Conventional Commit; record the commit in the feature-doc as evidence.
- **RDD per commit** (Hard rule #2): after each work-unit commit, if RDD is on → `gentle-ai review assess --cwd <ABS-worktree> --agent claude-code --base-ref <last reviewed boundary> --committed-only --json`; read `review_due`; if it is true, run **verbatim** the `next_transition.command` it returns; the boundary advances on acknowledgement. `false` → record `review_due_reason` and continue. **The full detail (tiers, medium/high consent, continuations) lives in the CLAUDE.md ODD protocol — do not reimplement it.**
- **Delivery slicing**: forecast ~400 authored lines; strategy `ask-on-risk` (default) / `auto-chain` / `single-pr`; resolve the `work-unit-commits` and `chained-pr` skills by registry name before building PRs.

## Step 7 — Close (ODD 7 + mala-pata close)

Report the **verified result** + every failed/skipped/pending check + next step. Then, the mala-pata close: reuse from `/mala-pata-loop-start` the sub-phases **4.1 (report), 4.1-bis (re-verify/renumber migration if you touched one), **4.1-ter (smoke test with seeded data — GATE, only if applicable)**, 4.2 (PR/merge destination with GATE), 4.4 (proactive CI), 4.5 (cleanup with GATE)** — **NOT 4.3** (that one no longer exists in the SDD cycle; RDD already ran per commit here, in Step 6). **The kickoff's `Why` FLOWS into the PR body** (motivation section).
**Cleanup exception** if you worked with incremental commits INSIDE the worktree of a feature in progress: that branch/worktree is closed by its own cycle, not organic-start — you only clean up what this skill created.

## Step 8 — Final table (MANDATORY)

Same format as `/mala-pata-loop-start` Step 5: Markdown table, one milestone per row, status (plain text, no emoji) + concrete evidence. Typical rows (only those that apply):

| Milestone | Status |
|---|---|
| Authorization | change authorized / read-only |
| Worktree + base | `<branch>` off `<base>` |
| Explore (Where) | `<n>` files/modules touched |
| Feature-doc (if substantial) | `mala-pata/odd/<change_name>.md` · `<n>` tasks |
| Apply (TDD if applies) | Red-Green-Refactor, `<n>` tests |
| Smoke test (fixtures + confirmation) | functionality OK · or `N/A (did not apply)` |
| Work-unit commits | `<n>` commits · RDD assess: `<granted/passive/…>` |
| PR `#<n>` → `<branch>` | MERGED (merge commit `<sha>`) |
| CI post-merge | GREEN |
| Cleanup (worktree + branch) | Done |

## Persistence

For **substantial** work, the **feature-doc** (`mala-pata/odd/<change_name>.md` + engram mirror `odd/<change_name>/tasks`) IS ODD's persistence. For **small** work with no feature-doc, an optional lightweight close (`mem_save` topic `odd/<change_name>/organic`) if you want future continuity.
