---
name: mala-pata-organic-orchestrate-start
description: Executes a batch of ORGANIC (ODD) kickoffs as a hybrid-by-waves delivery — in ROUNDS, one per wave. Each round derives the READY wave live against git, creates one worktree per kickoff (anti-stale at origin/<base>), opens one Claude tab per kickoff in the active Warp window (validated tab configs, launch verified) running /mala-pata-organic-start (which keeps per-commit RDD and the smoke gate inside its own tab and STOPS at PR-ready), waits for the wave to reach PR-ready, then runs the CENTRAL delivery itself — one merge-gate table (smoke verdict + RDD outcome per phase), merges in dependency order with migration renumbering, central worktree/branch cleanup — and advances the base for the next round. The orchestrator OWNS merges, cleanups and sequencing between waves. Trigger — "lanzá estos organic en olas", "corré el lote de ODD con merge central", "arrancá la ola de kickoffs organic y mergeá por mí", "orquestá y entregá estos cambios organic".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.2.1"
---

# /mala-pata-organic-orchestrate-start — Run a BATCH of organic kickoffs in WAVES (launch + central delivery)

You are the **batch executor and delivery owner** for the ODD lane. You are handed a batch of **organic kickoffs** and you run them in **rounds, one per wave**: launch the ready wave in parallel (one worktree + one Claude tab each, every tab running `/mala-pata-organic-start`), wait until the wave is PR-ready, then **merge, clean up and sequence** centrally before the next round. The plan (waves, conflicts, order) comes from `/mala-pata-organic-orchestrate`; this skill EXECUTES it.

> **You never live inside a phase's cycle.** Each tab is an independent Claude session running the full `/mala-pata-organic-start` cycle with its own context and gates. **Per-commit RDD and the phase smoke stay INSIDE each tab** — RDD is per work-unit commit under user-owned consent, and smoke is per change; neither can be centralized. You own what happens **BETWEEN waves**: sequencing, merges, cleanups.

> **Parallelism is the purpose of the launch.** Launch ALL kickoffs of the ready wave even if they share files — worktrees isolate the work. Conflicting ready phases are not "held back inside a wave": they are **serialized across rounds** (core / highest fan-in first), and that decision is made when the wave is derived (Round step 1), never silently.

## Requirements (orchestrate, do not reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP and ask to install it, do not start):
  - `git` — isolated worktrees per kickoff, merges, cleanup. Install: always present; requires no installation.
  - `gentle-ai` — ODD engine + RDD per commit (run inside each tab). Install: `brew install gentleman-programming/tap/gentle-ai`.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded):
  - `engram` — persistent memory and continuity pointer. Fallback: continue with the explicit list of kickoffs; the kickoff files and git are the source. Install: comes with gentle-ai (`brew install gentleman-programming/tap/gentle-ai`).
  - `gh` (or the project's PR CLI, e.g. `az repos`) — PR status, CI and merge. Fallback: derive readiness from branches and commits only, flag that PRs were not queried, and hand the merge to the human. Install: `brew install gh`.

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP, e.g. serena). If a mandatory tool is missing, do not continue.

## Step 0 — Input, confirmation and cached choices

- Input: the batch of organic kickoffs (absolute paths, or change-names resolving to `<repo-root>/mala-pata/kickoffs/<change-name>.md` via `git -C <cwd> rev-parse --show-toplevel`). `Read` each in full and take `change_name`, `route`, `base`, `branch`, `worktree`, `depends_on`, `parallelizable_with`, `domain`, `roadmap` from the frontmatter. If `route` is not `organic` → exclude it and say so (loop kickoffs always need a human; run them by hand with `/mala-pata-loop-start`).
- **Base confirmation — ALWAYS, once**: show each kickoff's base ("`<change>` off `<base>`") and wait for a SINGLE OK. The kickoff's `base` rules; if the human corrects one, update that kickoff's frontmatter before launching. A wave only mixes kickoffs of the SAME base; different bases run as separate rounds.
- **Delivery strategy — ask once, cache for the whole run**: `ask-on-risk` (default, **attended** — pauses at each wave's merge gate so you decide) / `auto-chain` (**fire-and-forget** — merges autonomously with no per-wave prompt, so you run it and walk away and come back to the whole batch implemented) / `single-pr` / `exception-ok` (same vocabulary as the ODD delivery contract). It governs the central merge gate (Round step 4). State plainly which one gives unattended completion (`auto-chain`).
  - **Unattended run (`auto-chain`) — what STILL parks for you** (irreducibly human; the run finishes everything else and lists these at the end, never blocking the rest): an RDD medium/high consent while RDD is ON, a medium/high-delicacy smoke, and any red CI / conflict. To minimize parking before you walk away, YOU may disable RDD (`gentle-ai review mode disable`) and keep smoke delicacy low — your switches, never toggled automatically.
- If the user did not say what to run, run **every non-deferred kickoff passed**, round after round.
- **Stateless by design**: nothing is stored between rounds. Every round re-derives readiness from git, so re-invoking this skill with the same batch RESUMES it (already-merged kickoffs are `done`, live worktrees are `in progress`).

## The hybrid-by-waves delivery contract

Each round N:

### Round step 1 — Derive the READY wave LIVE against git
`git -C <ABS-repo> fetch --all --prune`, confirm the integration branch and note its SHA. For each kickoff derive its state **from git reality, zero cache** (same signals as `/mala-pata-roadmap-radar`; any ONE confirms, all equal weight):
- **done** — landed in the freshly fetched `origin/<base>`: a `Mala-Pata-Phase: <change_name>` trailer on a base commit (`git log origin/<base> --grep '^Mala-Pata-Phase: <change_name>$' -E`), a merged PR for the branch (`gh`), or the branch an ancestor of `origin/<base>` (`git merge-base --is-ancestor`).
- **in progress** — not in base, but its worktree/branch or an open PR exists with its own commits.
- **pending** — no evidence at all.
- **blocked** — pending with at least one `depends_on` not `done`.

A kickoff is **READY** when it is `pending` (or `in progress` with a missing tab — see Step 3 resume) and **every dependency is MERGED** (observed `done` in git — PR-ready is NOT enough). The **wave** = all READY kickoffs that are **mutually parallelizable**: declared parallelizable (`parallelizable_with`) AND no shared file AND no migration-number conflict. Conflicting READY kickoffs are **serialized across rounds**, core / highest fan-in first — put the loser in a later round and say why in the round report. A kickoff with no declared `depends_on` and no declared `parallelizable_with` is treated as parallelizable only if the file check finds no clash; `where unknown` clashes with any other kickoff of the same domain.

If no kickoff is READY and some are blocked → report who waits for whom and STOP (a dependency stays unmerged). If all non-deferred kickoffs are `done` → go to the final report.

### Round step 2 — Launch the wave IN PARALLEL
Reuse the proven worktree + anti-stale + Warp machinery below (Steps 1–3). **One worktree per kickoff at `origin/<base>`, one tab per kickoff, every tab runs `/mala-pata-organic-start <kickoff>`** — organic route is fixed, there is no triage here (the lane was decided when the kickoff was written). Each tab runs its FULL cycle, including per-commit RDD (`gentle-ai review assess` + native plan) and the phase SMOKE when the change needs it (organic-start's own 4.1-ter gate decides applicability). **Each tab STOPS at its PR-ready gate: it does NOT merge and does NOT clean up** — merge and cleanup are central. The launch prompt of every tab carries this directive (see Step 3).

### Round step 3 — WAIT for the wave to reach PR-ready (observed in git)
You do NOT answer in-tab gates and you do NOT follow the cycles. You **observe** readiness. A kickoff is PR-ready when ALL hold, measured with absolute paths:
- its branch has its work-unit commits ahead of `origin/<base>`, carrying the `Mala-Pata-Phase` trailer (`git -C <ABS-repo> log origin/<base>..<branch> --format=%B`);
- its worktree is clean (`git -C <ABS-worktree> status --porcelain` empty);
- its feature-doc (if any, `mala-pata/odd/<change_name>.md` on the branch, read with `git -C <ABS-repo> show <branch>:mala-pata/odd/<change_name>.md`) has no unchecked task;
- a PR exists for the branch and is open (`gh pr list --head <branch>`), or `gh` is missing and the tab reports it stopped at its gate.

**Strategy-aware waiting**: under `auto-chain` (fire-and-forget) the orchestrator **polls AUTONOMOUSLY** at a bounded cadence using the runtime's wait/schedule mechanism — it does NOT wait for the human to say the tabs are ready; it keeps measuring until each kickoff is PR-ready or parked, then proceeds to the central delivery on its own. Under `ask-on-risk` re-measure at a bounded cadence or when the human says the tabs are ready. **Never busy-loop.** Report a short readiness table (below, Step 4 Report) and keep waiting for the stragglers. A tab stopped on a gate that is NOT PR-ready (red verify, smoke "No", open decision, RDD consent pending) is NOT PR-ready: show it `◐ partial: <reason>` and do not merge it; the rest of the wave proceeds (under auto-chain this becomes a PARK, reported at the end — the run never hangs waiting on it). If the human abandons a kickoff, mark it blocked and let dependents wait.

### Round step 4 — CENTRAL delivery for the wave (one place)
**Merge gate.** Present ONE table of the wave's PR-ready kickoffs, with each one's smoke verdict and RDD outcome **collected from the branch's own evidence**:
- **Smoke verdict**: `mala-pata/walkthroughs/<slug>/evidence/` on the branch (read via `git show` — never open another worktree's files by `cd`), the feature-doc's smoke row, or `∅ n/a` when the kickoff's smoke gate did not apply. **You COLLECT and SHOW it; you never decide smoke yourself** — the tab already ran it when the change needed it ("smoke when necessary" is satisfied in-tab).
- **RDD outcome**: the per-task assess outcomes recorded in the feature-doc (`granted` / `declined` / `passive` / `under budget` / `already reviewed` / `unavailable`) and the work-unit commit trailers.
- **CI / mergeability**: `gh pr checks`, `gh pr view --json mergeable` (red CI or conflicts → not offered for merge).

Relay the merge decision per the **cached delivery strategy**:
- `ask-on-risk` (attended) — one table, the human OKs all / a subset / none; any kickoff with a non-green smoke, `unavailable`/`declined` RDD, red CI or conflicts is flagged and not offered by default.
- `auto-chain` (fire-and-forget) — **NO per-wave prompt**; the upfront choice of auto-chain IS the standing authorization. After one OK on the chain strategy (`stacked-to-main` or `feature-branch-chain`, resolve the `chained-pr` skill by registry name), the orchestrator merges AUTONOMOUSLY every kickoff that passes the safe-to-auto-merge checklist, in order, slicing automatically, and PARKS the rest (park-and-continue).
- `single-pr` — consolidate the wave's PRs into one only with a recorded `size:exception`; `exception-ok` — record the size exception and merge.

**Safe-to-auto-merge checklist (auto-chain only).** A PR-ready kickoff merges WITHOUT a prompt only when ALL hold: CI green and no conflicts; smoke passed by assertions at low delicacy, or `∅ n/a`; every commit's RDD is `granted+acknowledged` / `passive` / `under budget` / `already reviewed` (NOT `declined`, NOT `unavailable`, NOT awaiting consent). If ANY is false → **PARK** it.

**Park-and-continue.** A parked kickoff is NOT merged and NOT cleaned, but it NEVER blocks the rest: its independent siblings still merge and the run continues to the end; only its own dependents wait. The final report lists every parked kickoff with its reason (`RDD consent pending` / `smoke delicacy` / `red CI` / `conflict`) and how to resume (answer the in-tab gate, then re-invoke this skill). **Non-negotiable floor in EVERY strategy: never merge red CI or conflicts, never merge a kickoff whose smoke failed or whose RDD was declined, never force.**

**Merge order**: dependency order, then highest fan-in, then smallest first. **Migrations** (sibling of `/mala-pata-loop-start` 4.1-bis): right before each merge, re-measure git — list the numbers occupied in `origin/<base>` AND in the sibling in-flight branches (`git ls-tree -r --name-only <branch> -- <migrations-folder>`, never count files on disk). If a provisional number is still free → confirm. If a sibling merged first and took it → renumber to the next free one using the stack's mechanism (a chained-state migrator regenerates, it does not rename), re-run the round-trip, and only then merge. After each merge `git -C <ABS-repo> fetch origin <base>` so the next merge measures the new state. The landing commit carries the trailers `Mala-Pata-Phase`, `Mala-Pata-Domain`, `Mala-Pata-Roadmap`, `Mala-Pata-Lane: organic`.

**CI after merge (sibling of 4.4)**: actively check the run's status (`gh run list` / `gh run view`, or the project's tool) and confirm ALL stages green before cleaning up. Red → STOP, bring the failing step's log, do not clean that phase; dependents stay blocked.

**Cleanup (central, after each phase merges and CI is green)** — from OUTSIDE the worktree (you run in the main repo): kill background processes the tab left, `git -C <ABS-repo> worktree remove <ABS-worktree>` + `git -C <ABS-repo> worktree prune`, delete the merged branch local (`git branch -d`, never `-D`) and remote (`git push origin --delete <branch>`, unless `--delete-source-branch` already removed it). **Seeds STAY** (the `## Seed` recipe data; never wipe the shared test DB); remove only **cycle-only fixtures** provably this run's (smoke/walkthrough byproducts by their change-scoped namespace/ids/run-tag; a throwaway DB/schema the cycle created). Ownership not provable → leave it and report. Never clean a phase whose merge did not reach green (unintegrated work needs a separate explicit OK). Report in one line what was removed vs kept.

**Advance the base / boundary.** After the wave's merges, `fetch` again; the next round derives readiness from the NEW `origin/<base>` — a worktree for the next wave is created off the post-merge integration state, so dependents see their providers' code.

### Round step 5 — Next round until done
Loop to Round step 1 until every non-deferred kickoff is `done`, or a dependency stays blocked (report and stop). Print the final report (Step 4).

## Step 1 — One worktree per kickoff (real isolation)
For each kickoff of the wave, sequentially (so as not to lock the git index), READ `branch:` and `worktree:` from the kickoff frontmatter and use them **verbatim** — **but ALWAYS your own worktree and your own new branch** (the `organic-start` Hard rule #1: never an integration branch, never another feature's worktree). If the kickoff names a shared branch/worktree, derive `<type>/<change-name>` and `<ABS-repo>-worktrees/<change-name>` instead and say in one line that you corrected the kickoff:
```
git -C <ABS-repo> worktree add <ABS-repo>-worktrees/<change-name> -b <type>/<change-name> <base>
```
Then symlink the untracked files the stack needs (`.env`/`node_modules` or equivalent), as `organic-start` does. To verify the `.env` symlink NEVER name it as a direct argument (`ls -la <wt> | grep '\.env'`). `organic-start` finds its own worktree already present and RESUMES in it (its resume exception) — it will not create a second one.

**Drifted worktree check (one line, before operating)**: confirm the worktree is at its canonical path `<ABS-repo>-worktrees/<change-name>` and that `git worktree list` shows it there, resolving on disk. If the registered id != the folder, or the path does not resolve (someone renamed it with `mv`), warn and offer `git worktree repair <path>` (or `git worktree prune` if it was deleted) before continuing. **NEVER use `mv` to rename a worktree** — use `git worktree move`.

## Step 2 — Anti-stale: advance the worktrees to origin/<base> (MANDATORY, every round)
`git worktree add` bases the worktree on your LOCAL `<base>` as it stands, which is usually **behind** origin. BEFORE opening the tabs:
```
git -C <ABS-repo> fetch origin <base>
# for each newly created worktree (branches with no commits → clean ff, without touching history):
git -C <ABS-repo>-worktrees/<change-name> merge --ff-only origin/<base>
```
Verify each worktree ends at `origin/<base>` (`git -C <wt> rev-parse --short HEAD`). If a worktree already had commits and the ff failed, STOP and warn (do not force): that worktree is not born clean. `ff-only` does not lose history — it is the only advance allowed here.

## Step 3 — Launch the wave as Warp tabs (one Claude session per kickoff)
- Verify `claude` in PATH (`which claude`).
- Run the shared procedure in `~/.claude/skills/_shared/mala-pata-wave-launch.md` (prompt files, tab configs, validate, open, verify, fallback, cleanup, launch table). `<run-id>` = `<batch-slug>-r<N>-<epoch-seconds>` (unique per run; tab configs are `mpl-<run-id>-<slug>`); one tab per kickoff; each `<worktree>` is the ABSOLUTE worktree path, never the main repo.
- **Per-tab prompt** (written verbatim to the kickoff's `.prompt` file): `/mala-pata-organic-start <absolute-path-of-kickoff.md> -- wave-mode: this phase is run by /mala-pata-organic-orchestrate-start. Run the FULL cycle including per-commit RDD and the smoke gate. At the destination gate choose open a PR (never merge directly); STOP at PR-ready (green CI, PR open, worktree clean). Do NOT merge, do NOT run cleanup 4.5 — the orchestrator merges and cleans centrally.`
- **Worktree moved/renamed = relaunch, do not fix on the fly.** Sessions stay anchored to the old path and fall back to main; close and relaunch them with the new `directory`.
- **Resume**: a kickoff `in progress` whose tab is gone gets a fresh tab on its existing worktree (organic-start resumes there); never create a second worktree.

## Step 4 — Reports (emit at each round boundary)

**Launch report.** BLUF first: `Launched <n>/<n> sessions · round <N> · launch: <warp-tab|warp-window|terminal|manual counts>` (or `✗ partial: <which failed and why>`). Then one row per kickoff:

| Kickoff | Branch | Worktree | At origin/<base> | Tab | Merge order |
|---|---|---|---|---|---|
| <slug> | <type>/<slug> | <ABS-worktree> | ✓ <short-sha> | <title> | <1st / 2nd / …> |

**Readiness report** (while waiting). BLUF: `Round <N>: <r>/<n> PR-ready · <p> in progress · <b> blocked`.

| Kickoff | Status | Evidence |
|---|---|---|
| <slug> | ✓ PR-ready / ◐ in progress / ✗ blocked: <reason> | <commits ahead [git] · PR #<n> · clean worktree> |

**Merge-gate report** (Round step 4). BLUF: `Merge gate: <n> PR-ready · <m> offered · strategy <ask-on-risk|auto-chain|single-pr|exception-ok>`.

| Kickoff | PR | Smoke verdict | RDD outcome | CI | Migration | Merge decision |
|---|---|---|---|---|---|---|
| <slug> | #<n> | ✓ OK <evidence path> / ∅ n/a | passive / granted+acknowledged / declined / unavailable | GREEN / RED | provisional <N> ✓ free / renumbered <M> / ∅ | merge / hold: <reason> |

**Final report.** BLUF: `Result: ✓ complete · <d>/<N> kickoffs merged · <r> rounds` (or `◐ partial` / `✗ blocked` with the reason).

| Kickoff | Round | Status | Evidence |
|---|---|---|---|
| <slug> | 1 | ✓ done / ◐ partial: <reason> / ✗ blocked: <reason> / ○ pending | merge <sha> · CI GREEN · worktree+branch removed |

**No false green**: never mark `✓ done` over a red pipeline or an unmerged PR. Offer `mala-pata-radar` to see progress (it discovers and confirms with git in one run).

**Emit this block's structural labels verbatim in English** — the BLUF lines and every table header (`Kickoff`, `Branch`, `Worktree`, `At origin/<base>`, `Tab`, `Merge order`, `Status`, `Evidence`, `PR`, `Smoke verdict`, `RDD outcome`, `CI`, `Migration`, `Merge decision`, `Round`) stay English; only the values follow the conversation language.

## Hard rules
- **LAUNCH THE COMPLETE READY WAVE** in parallel — conflicts are serialized across rounds (decided at derivation, reported), never by silently trimming a launched wave.
- **Anti-stale ALWAYS** (Step 2): no worktree is launched without being at `origin/<base>`, in every round.
- **Readiness = MERGED, observed in git.** A dependency that is only PR-ready does not make its dependent ready.
- **RDD and smoke stay in the tab.** You never run `gentle-ai review`, never run the smoke, never answer an in-tab gate; you only collect and show their outcomes.
- **Merge authorization is strategy-aware**: `ask-on-risk` needs the human's explicit OK per wave; `auto-chain` merges autonomously by the safe-to-auto-merge checklist (the upfront auto-chain choice is the standing OK) and parks the rest. In EVERY strategy: never merge red CI or conflicts, never merge a kickoff whose smoke failed or whose RDD was declined, never forced; `ff-only` and `fetch` are the only advance of a worktree; never `reset --hard` or forced `rebase`.
- **Migration numbers are provisional**: the first to merge keeps it, the others renumber on integration; the truth is git, never a registry.
- **Cleanup only after merge + green CI**, from outside the worktree, `git branch -d` never `-D`, seeds kept, cycle-only fixtures removed only when provably this run's.
- **Never unattended side effects beyond the contract**: no push of the base, no force-push, no deleting a branch that was not integrated.
- ABSOLUTE paths in every git/worktree/launch command and tab config; relative only when talking to the user.

## What it does NOT do
- It does not run the ODD cycle, RDD, or the smoke — each tab's `/mala-pata-organic-start` does.
- It does not plan (that is `/mala-pata-organic-orchestrate`) and it does not triage: the organic lane is fixed by the kickoff.
- It does not run loop (SDD) kickoffs — loops always need a human; run them by hand with `/mala-pata-loop-start`.
- It does not edit kickoff contents (only a corrected `base` the human asked for).
- It does not answer in-tab gates, decide smoke, or invent evidence for the merge table.
- It does not wipe the shared test DB or delete seeds.

## Runtime compatibility
The Warp/Claude block (Step 3) only runs when the runtime is Claude with Warp. In another CLI: create the worktrees + anti-stale and return the `/mala-pata-organic-start <absolute-kickoff-path>` command per worktree (with the wave-mode directive); do not invoke `claude`, Warp or `.claude/` paths that do not apply. The readiness derivation, the merge-gate table, the central merges and the cleanup are portable git/`gh` work and run on any CLI.

**Structure:** house method (batch worktree + Warp launch + hybrid-by-waves central delivery).
