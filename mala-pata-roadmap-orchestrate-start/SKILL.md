---
name: mala-pata-roadmap-orchestrate-start
description: Executes a ROADMAP whose phases are ALL shot/organic as a route-aware hybrid-by-waves delivery (it refuses any roadmap containing a loop phase — loops always need a human at their gates, so they cannot be batch-automated; a phase that triage upgrades to loop at run time is paused and handed to the human) — in ROUNDS, one per wave. Each round derives the READY wave live against git (reusing /mala-pata-roadmap-radar's readiness logic), passes each phase through /mala-pata-triage (the roadmap route is only a FORECAST; triage re-decides with current info), creates one worktree per code phase (anti-stale at origin/<base>), opens ONE Warp launch config with one Claude tab per phase running its resolved lane (shot, or organic + organic-start), and PAUSES on Kind ops phases for human attestation (Verify/Status/Evidence). Per-commit RDD and the phase smoke stay inside each phase's tab, which STOPS at PR-ready; the orchestrator then runs the CENTRAL delivery — one merge-gate table with smoke verdict and RDD outcome, merges in dependency order with migration renumbering, central cleanup — and advances the base for the next round. Trigger — "ejecutá el roadmap <slug> en olas", "corré el roadmap completo con merge central", "arrancá las fases listas del roadmap y mergeá por mí", "orquestá y entregá el roadmap <slug>".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.0.0"
---

# /mala-pata-roadmap-orchestrate-start — Run a ROADMAP in WAVES (route-aware launch + central delivery)

Input: **the one provided by the CLI** — a roadmap **slug** (preferred) or the path to a roadmap `.md`.

You are the **roadmap executor and delivery owner**. You take ONE roadmap and run it in **rounds, one per wave**: derive the ready phases live, route each one (`triage → lane → -start`), launch the wave in parallel (one worktree + one Claude tab per code phase), pause on `ops` phases for human attestation, wait until the wave is PR-ready, then **merge, clean up and sequence** centrally before the next round. The plan comes from `/mala-pata-roadmap-orchestrate`; the status radiator is `/mala-pata-roadmap-radar`; this skill EXECUTES.

> **You never live inside a phase's cycle.** Each tab is an independent Claude session running its lane's full cycle with its own context and gates. **Per-commit RDD and the phase smoke stay INSIDE each tab** — RDD is per work-unit commit under user-owned consent, smoke is per change; neither can be centralized. You own what happens **BETWEEN waves**: sequencing, merges, cleanups.

> **The roadmap route is a FORECAST, triage rules.** The phase's `Tentative route` was written with the information of the day it was planned; previous phases resolve unknowns. So every code phase passes `/mala-pata-triage <slug>` on arrival — the resolved lane, not the forecast, decides the tab command.

## Requirements (orchestrate, do not reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP and ask to install it, do not start):
  - `git` — live state, isolated worktrees, merges, cleanup. Install: always present; requires no installation.
  - `gentle-ai` — ODD/SDD engine + RDD per commit (run inside each tab). Install: `brew install gentleman-programming/tap/gentle-ai`.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded):
  - `gh` (or the project's PR CLI, e.g. `az repos`) — PR status, CI and merge. Fallback: derive readiness from branches and commits only, flag that PRs were not queried, and hand the merge to the human. Install: `brew install gh`.
  - `engram` — optional continuity pointer. NOT used for state: the roadmap `.md` + live git are the only two sources. Install: comes with gentle-ai (`brew install gentleman-programming/tap/gentle-ai`).

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP, e.g. serena). If a mandatory tool is missing, do not continue.

## Hard rule #0 — ENTRY GATE: refuse any roadmap with a loop phase

> **Loops always need a human.** A loop (SDD) stops at a human gate at every phase, so it cannot be batch-automated. This executor only runs roadmaps whose phases are all **shot** and **organic**. Right after loading the roadmap (Step 0) and BEFORE any state derivation, worktree or launch, scan the DAG's `Tentative route` column: if ANY phase — deferred or not, done or not — has a loop route (`loop`, `loop:FULL`, `loop:STANDARD`, `loop:LITE`, `loop:MINIMAL`), **REFUSE to orchestrate the whole roadmap. Do NOT run any wave.**

The refusal report: BLUF `Refused: roadmap <slug> has <n> loop phase(s) — loops always need a human, this orchestrator does not handle them`, then the table of every loop phase:

| # | Phase | slug | Tentative route |
|---|---|---|---|
| <#> | <name> | <slug> | loop:STANDARD |

Then tell the human: run this roadmap with `/mala-pata-roadmap-radar <slug>` (it emits the per-phase `triage → lane → -start` commands, loops included) and drive each loop phase yourself via `/mala-pata-loop` + `/mala-pata-loop-start`. Emit these labels verbatim in English.

**Runtime guard.** The gate checks the FORECAST; triage re-decides on arrival. If triage upgrades a phase to loop at execution time (Round step 3), **PAUSE that phase, do NOT auto-run it**, and hand it to the human: report it as `✗ blocked: needs human — became loop at triage` and tell the human to drive it with `/mala-pata-loop` + `/mala-pata-loop-start`. The other non-loop phases of the wave still proceed; the loop phase's dependents stay blocked until the human merges it.

## Step 0 — Load the roadmap, confirm, cache choices

- Resolve the project root: `git -C <cwd> rev-parse --show-toplevel`. Resolve the roadmap exactly as `/mala-pata-roadmap` writes it and `/mala-pata-roadmap-radar` reads it: **slug** → `<repo-root>/mala-pata/roadmap/<slug>.md` (folder `roadmap`, singular); a path → `Read` directly; a **domain** → the `mala-pata/roadmap/*.md` whose frontmatter `domain:` matches (never mix domains; several candidates → ask which, one question, stop and wait). No match → do not invent phases; ask for the path.
- Extract per phase: `#`, name, `slug` (the stable change-name), `Kind` (`code`/`ops`), `Tentative route`, `Depends on`, `Deferrable?`, and for ops phases `Verify` / `Status` / `Evidence`; plus `Parallelizable: {…}` and `Deferred: {…}` from the DAG closing.
- **Base confirmation — ALWAYS, once**: confirm the integration branch (`main` / `development` / whichever the repo uses; the roadmap's durable branch) and wait for a SINGLE OK.
- **Delivery strategy — ask once, cache for the whole run**: `ask-on-risk` (default) / `auto-chain` / `single-pr` / `exception-ok`. It governs how the merge decision is relayed at the central gate (Round step 5).
- **Deferred phases** (`Deferrable? = yes`) are NOT started unless the human promotes them; core phases (`no`) run first. Say which are deferred in the first report.
- **Stateless by design**: nothing is stored between rounds. Each round re-derives from the `.md` + live git, so re-invoking this skill with the same slug RESUMES it.

## The hybrid-by-waves delivery contract (route-aware)

Each round N:

### Round step 1 — Derive the READY wave LIVE against git
Reuse `/mala-pata-roadmap-radar` verbatim for state: `git -C <ABS-repo> fetch --all --prune`, confirm the integration branch + SHA, then per phase — **code**: `done` by ANY git signal (`Mala-Pata-Phase: <slug>` trailer on an integration commit — optional, merged PR, branch merged or slug commit ancestor via `git merge-base --is-ancestor`, delivering artifact, recorded sha) `[git]`; `in progress` = live branch/OPEN PR not merged; `pending` = zero evidence; `? unbound` = work exists but not tied to the slug (STOP and ask, never a false pending); `blocked` = pending with an unfinished dependency. **ops**: `done` = declared `Status: done` + `Evidence` `[attested]`; otherwise pending; never pending/blocked for lacking a git artifact.

A phase is **READY** when it is `pending` (or `in progress` with a missing tab — see Step 4 resume), not deferred, and **every dependency is MERGED** (code `done` observed in git, or ops `done` attested) — a PR-ready dependency is NOT enough. The **wave** = all READY phases that are **mutually parallelizable**: they appear together in the roadmap's `Parallelizable: {…}` AND have no shared file (intersect each phase's `IN` border) AND no migration-number conflict. Conflicting READY phases are **serialized across rounds**, core / highest fan-in first, and the round report says which waits and why.

No READY phase and some blocked → report who waits for whom and STOP. Every non-deferred phase `done` → final report.

### Round step 2 — Ops phases: PAUSE and ask the human to attest
A `Kind: ops` phase has **NO code cycle, NO worktree, NO tab**. When an ops phase is in the wave (ready, or blocking dependents), the orchestrator **PAUSES** and shows the phase's `Verify` (URL / command / health check). Ask the human to perform it and attest: `Status: done` with `Evidence` (env URL / project id / health 200 / date). **Attested without evidence is NOT done.** On attestation, write ONLY that phase's `Status` and `Evidence` fields into the roadmap `.md` in the working tree (write-only, **no commit** — same rule as `/mala-pata-roadmap`; tell the human the durable branch it belongs on), tag it `[attested]`, and its dependents become ready in the same round derivation. Never run the ops step yourself and never invent evidence. Code phases of the wave that do not depend on the ops phase launch without waiting.

### Round step 3 — Route each code phase through triage, then launch the wave IN PARALLEL
For each READY code phase, run `/mala-pata-triage <slug>` **in this orchestrator session, once, decision only** (triage creates nothing). Hand it the phase's forecast route, `IN`/`OUT`, DoD and open decision as the draft, so it re-decides with the CURRENT state of the repo and of the already-merged phases. A phase forecast as organic may reveal complexity and arrive as loop (see the Runtime guard: pause, never auto-run). Show the resolved routes in ONE confirmation line per wave and wait for a SINGLE OK:

| Phase | Forecast route | Resolved lane | Why it changed |
|---|---|---|---|

Then launch (Steps 1–3 below): **one worktree per code phase at `origin/<base>`, one tab per phase**, the tab command by the resolved lane:
- **shot** → `/mala-pata-shot <slug>` — runs inline on the phase's pre-created worktree and branch (no ceremony; commit, then stop).
- **organic** → `/mala-pata-organic <slug>` (writes the kickoff from the triage draft) then `/mala-pata-organic-start <slug>`.
- **loop** → NOT dispatched: there is no `triage → loop → loop-start` path. The phase is paused and handed to the human (Runtime guard).

Each tab runs its FULL cycle, including **per-commit RDD in-tab** (organic/shot) and the **phase smoke when the change needs it** (the lane-start's own gate decides applicability). **Each tab STOPS at its PR-ready gate: it does NOT merge and does NOT clean up** — merge and cleanup are central. The launch prompt carries that directive (Step 3).

### Round step 4 — WAIT for the wave to reach PR-ready (observed in git)
You do NOT answer in-tab gates and you do NOT follow the cycles. You **observe** with `/mala-pata-roadmap-radar`'s readiness logic plus the branch evidence. A code phase is PR-ready when ALL hold, with absolute paths:
- its branch has its work-unit commits ahead of `origin/<base>` carrying the `Mala-Pata-Phase: <slug>` trailer (`git -C <ABS-repo> log origin/<base>..<branch> --format=%B`);
- its worktree is clean (`git -C <ABS-worktree> status --porcelain` empty);
- its feature-doc (if any) has no unchecked task, (read via `git -C <ABS-repo> show <branch>:<path>`);
- an open PR exists for the branch (`gh pr list --head <branch>`), or `gh` is missing and the tab reports it stopped at its gate.

Re-measure when the human says the tabs are ready, and at a bounded cadence if the runtime supports waiting; never busy-loop. A tab stopped on a non-PR-ready gate (red verify, smoke "No", open decision) is shown `◐ partial: <reason>`, is NOT merged, and the rest of the wave proceeds; its dependents stay blocked. Resume: a phase `in progress` whose tab is gone gets a fresh tab on its existing worktree, re-running its lane-start (which resumes) — never a second worktree.

### Round step 5 — CENTRAL delivery for the wave (one place)
**Merge gate.** Present ONE table of the wave's PR-ready phases, with each one's smoke verdict and RDD outcome **collected from the branch's own evidence**:
- **Smoke verdict**: `mala-pata/walkthroughs/<slug>/evidence/` on the branch (via `git show`, never by `cd` into another worktree), the feature-doc/summary smoke row, or `∅ n/a` when the gate did not apply. **You COLLECT and SHOW it; you never decide smoke yourself** — "smoke when necessary" is satisfied in-tab.
- **RDD outcome**: per-task assess outcomes from the feature-doc (`granted` / `declined` / `passive` / `under budget` / `already reviewed` / `unavailable`) and the commit trailers (`Mala-Pata-Lane`).
- **CI / mergeability**: `gh pr checks`, `gh pr view --json mergeable` (red CI or conflicts → not offered for merge).

Relay the merge decision per the **cached delivery strategy**: `ask-on-risk` — one table, the human OKs all / a subset / none; any phase with non-green smoke, `unavailable` RDD, red CI or conflicts is flagged and not offered by default; `auto-chain` — after one OK on the chain strategy (`stacked-to-main` or `feature-branch-chain`, resolve the `chained-pr` skill by registry name), merge in order and slice automatically; `single-pr` — consolidate with a recorded `size:exception`; `exception-ok` — record the size exception and merge. In every strategy: **never merge without the human's explicit OK in this session, never merge red CI or conflicts, never force.**

**Merge order**: dependency order, then highest fan-in, then smallest first. **Migrations** (sibling of `/mala-pata-loop-start` 4.1-bis): right before each merge re-measure git — list numbers occupied in `origin/<base>` AND in sibling in-flight branches (`git ls-tree -r --name-only <branch> -- <migrations-folder>`, never count files on disk). Provisional number still free → confirm; a sibling took it → renumber to the next free one with the stack's mechanism (a chained-state migrator regenerates, it does not rename), re-run the round-trip, then merge. After each merge `git -C <ABS-repo> fetch origin <base>`. The landing commit carries `Mala-Pata-Phase`, `Mala-Pata-Domain`, `Mala-Pata-Roadmap: <slug>`, `Mala-Pata-Lane`.

**CI after merge (sibling of 4.4)**: actively check the run (`gh run list` / `gh run view`, or the project's tool); ALL stages green before cleanup. Red → STOP with the failing step's log, do not clean that phase; dependents stay blocked.

**Cleanup (central, after each phase merges and CI is green)** — from OUTSIDE the worktree (you run in the main repo): kill background processes the tab left, `git -C <ABS-repo> worktree remove <ABS-worktree>` + `git -C <ABS-repo> worktree prune`, delete the merged branch local (`git branch -d`, never `-D`) and remote (`git push origin --delete <branch>`, unless already removed by `--delete-source-branch`). **Seeds STAY** (never wipe the shared test DB); remove only **cycle-only fixtures** provably this run's (change-scoped namespace/ids/run-tag; a throwaway DB/schema the cycle created); ownership not provable → leave and report. Never clean a phase whose merge did not reach green. Report in one line what was removed vs kept.

**Advance the base / boundary.** After the wave's merges `fetch` again; the next round derives readiness from the NEW `origin/<base>`, and its worktrees are created off the post-merge integration state.

### Round step 6 — Next round until done
Loop to Round step 1 until every non-deferred phase is `done`, or a dependency stays blocked (report and stop). Print the final report (Step 4).

## Step 1 — One worktree per code phase (real isolation)
For each code phase of the wave, sequentially (so as not to lock the git index): the phase's change-name is its `slug`; the branch is `<type>/<slug>` with the type from the triage result (`feature|fix|hotfix|refactor|chore|docs|release`; when a kickoff already exists, read `branch:`/`worktree:` from its frontmatter and use them verbatim). **ALWAYS your own worktree and your own new branch** — never an integration branch, never another phase's worktree:
```
git -C <ABS-repo> worktree add <ABS-repo>-worktrees/<slug> -b <type>/<slug> <base>
```
Then symlink the untracked files the stack needs (`.env`/`node_modules` or equivalent). To verify the `.env` symlink NEVER name it as a direct argument (`ls -la <wt> | grep '\.env'`). The lane runs in this pre-created worktree (`organic-start` resumes in its own worktree; any kickoff the lane writes lands inside it and rides in the phase's PR).

**Drifted worktree check (one line, before operating)**: confirm the worktree is at its canonical path `<ABS-repo>-worktrees/<slug>` and that `git worktree list` shows it there, resolving on disk. If the registered id != the folder, or the path does not resolve (someone renamed it with `mv`), warn and offer `git worktree repair <path>` (or `git worktree prune` if deleted) before continuing. **NEVER use `mv` to rename a worktree** — use `git worktree move`.

## Step 2 — Anti-stale: advance the worktrees to origin/<base> (MANDATORY, every round)
`git worktree add` bases the worktree on your LOCAL `<base>`, which is usually **behind** origin. BEFORE opening the tabs:
```
git -C <ABS-repo> fetch origin <base>
# for each newly created worktree (no commits → clean ff, history untouched):
git -C <ABS-repo>-worktrees/<slug> merge --ff-only origin/<base>
```
Verify each worktree ends at `origin/<base>` (`git -C <wt> rev-parse --short HEAD`). If a worktree already had commits and the ff failed, STOP and warn (do not force). `ff-only` is the only advance allowed.

## Step 3 — One Warp launch config with N tabs (one Claude session per code phase)
- Verify `claude` in PATH (`which claude`).
- Write ONE launch configuration per round:
  - File: `~/.warp/launch_configurations/mpl-roadmap-orchestrate-<slug>-r<N>.yaml` (create the dir if missing).
  - Schema (the `exec` depends on the phase's RESOLVED lane):
    ```yaml
    ---
    name: mpl-roadmap-orchestrate-<slug>-r<N>
    windows:
      - tabs:
          - title: <phase-slug-1>
            color: blue
            layout:
              cwd: <ABS-repo>-worktrees/<phase-slug-1>
              commands:
                - exec: claude "Run /mala-pata-organic <phase-slug-1> with the triage draft, then /mala-pata-organic-start <phase-slug-1>. wave-mode: this phase is run by /mala-pata-roadmap-orchestrate-start. Run the FULL cycle including per-commit RDD and the smoke gate. At the destination gate choose open a PR (never merge directly); STOP at PR-ready (green CI, PR open, worktree clean). Do NOT merge, do NOT run cleanup 4.5 — the orchestrator merges and cleans centrally."
          - title: <phase-slug-2>
            color: green
            layout:
              cwd: <ABS-repo>-worktrees/<phase-slug-2>
              commands:
                - exec: claude "Run /mala-pata-organic <phase-slug-2> with the triage draft, then /mala-pata-organic-start <phase-slug-2>. wave-mode: <same directive>"
          - title: <phase-slug-3>
            color: yellow
            layout:
              cwd: <ABS-repo>-worktrees/<phase-slug-3>
              commands:
                - exec: claude "Run /mala-pata-shot <phase-slug-3>. wave-mode: commit on this worktree's branch, open a PR, STOP at PR-ready; do NOT merge nor clean up."
          # ... one tab per code phase of the wave; ops phases get NO tab
    ```
- **Each tab's `cwd` MUST be the ABSOLUTE path of the worktree**, NEVER the main repo — it is the base directory the shell cwd returns to after each command; pointing to main makes every bare command operate on main. Verify each `cwd:` before opening.
- **Worktree moved/renamed = relaunch, do not fix on the fly.** Sessions stay anchored to the old path; close and relaunch with the new `cwd`.
- Open: `open "warp://launch/mpl-roadmap-orchestrate-<slug>-r<N>"`. If the URI does not fire, tell the user to open it from **Command Palette → "Launch Configuration" → mpl-roadmap-orchestrate-<slug>-r<N>** (the YAML is already written). Do not invent another mechanism.

## Step 4 — Reports (emit at each round boundary)

**Launch report.** BLUF first: `Launched <n>/<n> sessions · <o> ops paused · round <N> · launch config: <path>` (or `✗ partial: <which failed and why>`). One row per phase of the wave:

| Phase | Kind | Resolved lane | Branch | Worktree | At origin/<base> | Tab | Merge order |
|---|---|---|---|---|---|---|---|
| <slug> | code | organic | <type>/<slug> | <ABS-worktree> | ✓ <short-sha> | <title> | <1st / 2nd / …> |
| <slug> | ops | — | — | — | — | ○ awaiting attestation | — |

**Readiness report** (while waiting). BLUF: `Round <N>: <r>/<n> PR-ready · <p> in progress · <o> ops pending · <b> blocked`.

| Phase | Status | Evidence |
|---|---|---|
| <slug> | ✓ PR-ready / ◐ in progress / ○ pending / ✗ blocked: <reason> | <commits ahead [git] · PR #<n> · clean worktree> / <env URL, health, date [attested]> |

**Merge-gate report** (Round step 5). BLUF: `Merge gate: <n> PR-ready · <m> offered · strategy <ask-on-risk|auto-chain|single-pr|exception-ok>`.

| Phase | Lane | PR | Smoke verdict | RDD outcome | CI | Migration | Merge decision |
|---|---|---|---|---|---|---|---|
| <slug> | organic | #<n> | ✓ OK <evidence path> / ∅ n/a | passive / granted+acknowledged / declined / unavailable / ∅ n/a | GREEN / RED | provisional <N> ✓ free / renumbered <M> / ∅ | merge / hold: <reason> |

**Final report.** BLUF: `Result: ✓ complete · <d>/<N> phases done · <r> rounds` (or `◐ partial` / `✗ blocked` with the reason; deferred phases are listed as `○ pending (deferred)`, not failures).

| # | Phase | Round | Status | Evidence |
|---|---|---|---|---|
| 1 | <slug> | 1 | ✓ done / ◐ partial: <reason> / ✗ blocked: <reason> / ○ pending | merge <sha> [git] · CI GREEN · worktree+branch removed / <URL, health 200, date> [attested] |

**No false green**: never mark `✓ done` over a red pipeline or an unmerged PR. Offer `mala-pata-roadmap-radar` for the pure status view.

**Emit this block's structural labels verbatim in English** — the BLUF lines and every table header (`Phase`, `Kind`, `Resolved lane`, `Forecast route`, `Why it changed`, `Branch`, `Worktree`, `At origin/<base>`, `Tab`, `Merge order`, `Status`, `Evidence`, `PR`, `Smoke verdict`, `RDD outcome`, `CI`, `Migration`, `Merge decision`, `Round`, `Lane`) stay English; only the values follow the conversation language.

## Hard rules
- **Route-aware, triage-first.** Every code phase passes `/mala-pata-triage` on arrival; the resolved lane (not the roadmap forecast) picks the tab command. Never skip triage "because the roadmap already said organic"; a phase triage upgrades to loop is paused for the human, never auto-run.
- **Refuse loops (Hard rule #0) and guard at run time.** Any loop forecast refuses the whole roadmap; a phase that becomes loop at triage is paused as `needs human — became loop at triage` while the other non-loop phases proceed.
- **LAUNCH THE COMPLETE READY WAVE** in parallel — conflicts are serialized across rounds (decided at derivation, reported), never by silently trimming a launched wave.
- **Anti-stale ALWAYS** (Step 2): no worktree is launched without being at `origin/<base>`, in every round.
- **Readiness = MERGED (code, observed in git) or ATTESTED with evidence (ops).** A PR-ready dependency does not make its dependent ready.
- **Ops phases are never executed by you**: pause, show `Verify`, require `Status` + `Evidence`; attested-without-evidence is not done.
- **RDD and smoke stay in the tab.** You never run `gentle-ai review`, never run the smoke, never answer an in-tab gate; you only collect and show their outcomes.
- **No merge without the human's explicit OK in this session**, never on red CI or conflicts, never forced; `ff-only` and `fetch` are the only worktree advance; never `reset --hard` or forced `rebase`.
- **Migration numbers are provisional**: first to merge keeps it, the others renumber on integration; the truth is git, never a registry.
- **Cleanup only after merge + green CI**, from outside the worktree, `git branch -d` never `-D`, seeds kept, cycle-only fixtures removed only when provably this run's.
- **Roadmap edits are limited to an attested ops phase's `Status`/`Evidence`**, write-only, never committed by you.
- ABSOLUTE paths in every git/worktree/launch command and YAML; relative only when talking to the user; slug-first.

## What it does NOT do
- It does not run any lane cycle, RDD, or smoke — each tab's lane-start does.
- It only orchestrates roadmaps whose phases are all shot/organic; it refuses any roadmap containing a loop phase and pauses any phase that triage upgrades to loop.
- It does not plan (that is `/mala-pata-roadmap-orchestrate`) nor build the roadmap (that is `/mala-pata-roadmap`).
- It does not execute `Kind: ops` phases or fabricate their evidence.
- It does not start deferred phases unless the human promotes them.
- It does not answer in-tab gates, decide smoke, or invent evidence for the merge table.
- It does not wipe the shared test DB, delete seeds, or push/force the base branch.
- It does not read engram for state: roadmap `.md` + live git only.

## Runtime compatibility
The Warp/Claude block (Step 3) only runs when the runtime is Claude with Warp. In another CLI: create the worktrees + anti-stale and return, per worktree, the resolved lane's commands (`/mala-pata-organic <slug>` + `/mala-pata-organic-start <slug>`, or `/mala-pata-shot <slug>`) with the wave-mode directive; do not invoke `claude`, Warp or `.claude/` paths that do not apply. The readiness derivation, triage, ops attestation, the merge-gate table, the central merges and the cleanup are portable git/`gh` work and run on any CLI.

**Structure:** house method (route-aware batch worktree + Warp launch + hybrid-by-waves central delivery).
