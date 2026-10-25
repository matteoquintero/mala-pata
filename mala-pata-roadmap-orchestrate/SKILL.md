---
name: mala-pata-roadmap-orchestrate
description: READ-ONLY wave/execution planner for a ROADMAP whose phases are ALL shot/organic — it refuses any roadmap containing a loop phase (loops always need a human at their gates, so they cannot be batch-automated) — takes a roadmap slug or .md path, derives each phase's state LIVE against git (reusing /mala-pata-roadmap-radar's readiness logic), and returns the execution plan: which phases are ready now, which parallelize in this wave, which are deferred, which are ops phases (human-attested), which are blocked and why, plus the single copy-paste /mala-pata-roadmap-orchestrate-start <slug>. It is to roadmap-orchestrate-start what roadmap-radar is to execution, but focused on the WAVE plan rather than pure status. It does NOT execute, does NOT create worktrees, does NOT launch, does NOT mutate. Trigger — "planificá las olas del roadmap <slug>", "qué fases del roadmap puedo correr en paralelo ahora", "plan de ejecución del roadmap", "orquestá el roadmap <slug>".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.0.0"
---

# /mala-pata-roadmap-orchestrate — Wave plan of a ROADMAP (READ-ONLY)

Input: **the one provided by the CLI** — a roadmap **slug** (preferred) or the path to a roadmap `.md`.

You are the roadmap **wave planner**. You read ONE roadmap, derive each phase's state **live against git**, and return the **execution plan**: what is ready now, what runs in parallel in this wave, what is deferred, which phases are `ops` (human-attested, no code cycle), what is blocked and why — and the single command that hands the roadmap to the executor.

> **This skill executes NOTHING**: no worktrees, no launches, no triage, no lane, no merge, no write. It is ONLY analysis + plan. To **launch and drive** the roadmap use `/mala-pata-roadmap-orchestrate-start` (planner vs executor separation).

> **Not `/mala-pata-roadmap-radar`.** The radar is the pure status radiator (fixed format, every phase, next command per phase). This planner REUSES the radar's live-state derivation but answers a different question — *"what is the wave plan, in what order do the rounds run, and where will the executor pause?"* — and ends with the executor handoff, not a per-phase next-command list.

## Requirements (orchestrate, do not reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP and ask to install it, do not start):
  - `git` — source of truth for phase state and conflict detection. Install: always present; requires no installation.
  - `gentle-ai` — ODD/SDD engine the lanes run on. Install: `brew install gentleman-programming/tap/gentle-ai`.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded):
  - `gh` (or the project's PR CLI, e.g. `az repos`) — PR status. Fallback: only branches and merges; flag that PRs were not queried. Install: `brew install gh`.
  - `engram` — NOT used for state (roadmap `.md` + git are the only two sources, exactly like the radar). Optional continuity pointer only.

Check: `command -v <tool>`. If a mandatory tool is missing, do not continue.

## Hard rule #0 — ENTRY GATE: refuse any roadmap with a loop phase

> **Loops always need a human.** A loop (SDD) stops at a human gate at every phase, so it cannot be batch-automated. This planner only plans roadmaps whose phases are all **shot** and **organic**. Right after loading the roadmap (Step 1) and BEFORE any state derivation or plan, scan the DAG's `Tentative route` column: if ANY phase — deferred or not, done or not — has a loop route (`loop`, `loop:FULL`, `loop:STANDARD`, `loop:LITE`, `loop:MINIMAL`), **REFUSE the whole roadmap. Produce no wave plan and no handoff command.**

The refusal report: BLUF `Refused: roadmap <slug> has <n> loop phase(s) — loops always need a human, this orchestrator does not handle them`, then the table of every loop phase:

| # | Phase | slug | Tentative route |
|---|---|---|---|
| <#> | <name> | <slug> | loop:STANDARD |

Then tell the human: run this roadmap with `/mala-pata-roadmap-radar <slug>` (it emits the per-phase `triage → lane → -start` commands, loops included) and drive each loop phase yourself via `/mala-pata-loop` + `/mala-pata-loop-start`. The forecast route can still change at triage time; this gate checks the forecast the roadmap carries today. Emit these labels verbatim in English.

## Step 1 — Load the roadmap (slug-first, git not memory)

1. Resolve the project root: `git -C <cwd> rev-parse --show-toplevel`.
2. Resolve the roadmap `.md` the way `/mala-pata-roadmap` writes it and `/mala-pata-roadmap-radar` reads it:
   - **slug** → `<repo-root>/mala-pata/roadmap/<slug>.md` (the folder is `roadmap`, singular).
   - **path** → `Read` directly.
   - **domain** → list `mala-pata/roadmap/*.md` and keep ONLY those whose frontmatter `domain:` matches; never mix domains in one run. Several candidates and none chosen → list them and ask which one (one question, stop and wait).
   - Nothing matches → do NOT dead-end: point to `/mala-pata-radar` for loose SDDs, or ask for the path. Do not invent phases.
3. From the `.md` extract, per phase: **#**, **name**, **slug** (the stable change-name), **Kind** (`code` / `ops`; default `code` for an old roadmap without the column), **Tentative route** (a FORECAST: `organic`, `shot`, or `—` for ops; any loop value triggers Hard rule #0), **Depends on**, **Deferrable?** (`no (core)` / `yes`), and for `ops` phases the declared **Verify / Status / Evidence**. From the DAG closing take the `Suggested order`, `Parallelizable: {…}` and `Deferred: {…}` blocks.

## Step 2 — Live state per phase (reuse the radar's derivation, zero cache)

1. `git -C <repo> fetch --all --prune`; confirm the integration branch (`main` / `development` / whichever the repo uses) and note its SHA. If `gh` exists, fetch open/merged PRs.
2. Derive each phase exactly as `/mala-pata-roadmap-radar` Phase 2 does:
   - **`code` phases — from git reality, any ONE signal confirms**: the `Mala-Pata-Phase: <slug>` trailer in an integration commit (optional, not required), a merged PR for the slug, a branch `<type>/<slug>` merged into integration or a slug commit that is an ancestor, a delivering migration/file present in integration, a recorded `Evidence` sha/PR# that is an ancestor. → **done** `[git]`. A live branch or OPEN PR for the slug not yet in integration → **in progress**. **Zero evidence** → **pending**. Implementing commits clearly exist but cannot be tied to the slug → `? unbound (confirm)` (never a confident pending). **pending** with an unfinished dependency → **blocked**.
   - **`ops` phases — no git artifact, read the declared status**: `Status: done` AND `Evidence` present → **done** `[attested]`; `pending`, or `done` WITHOUT evidence → **pending** (show its `Verify`); pending with an unfinished dependency → **blocked**. An ops `done` satisfies its dependents exactly like a code `done`.
   - No `slug` (old roadmap) → try branch/PR/artifact; if still unmatchable mark `? (no slug)` and ask for the evidence by hand. Never guess.
3. A done phase is NEVER a ticked DoD checkbox, and never memory. `.md` says what was planned; git says what landed.

## Step 3 — Build the wave plan

1. **Ready now** = phases `pending` (not `blocked`) whose dependencies are ALL `done` (code `[git]` or ops `[attested]`).
2. **This wave** = the ready phases that are **mutually parallelizable**: they appear together in the roadmap's `Parallelizable: {…}` AND declare no shared file AND no migration-number conflict. Conflicting ready phases are **serialized across rounds**, core / highest fan-in first — state which goes first and why. `Kind: ops` phases are never "launched": they are listed in the wave as **ops-attest** (the executor pauses and asks the human to attest them).
3. **Deferred set** = phases with `Deferrable? = yes` that the executor will NOT start unless the human promotes them (read the column; do not recompute). Core phases (`no`) always plan first.
4. **Blocked** = phases waiting on unfinished dependencies, each with the dependency and its state, so the human sees the chain.
5. **Round forecast**: project the sequence of rounds (round 1 = this wave; round 2 = what becomes ready once round 1 is merged; …) up to the end or the first dependency that cannot resolve. State where the executor will pause for a human (an `ops` attestation, or the merge gate between rounds). Because the roadmap route is only a FORECAST, say that each phase passes `/mala-pata-triage` on arrival and may change lane; the plan reports the forecast route, the executor re-decides.
6. **Conflict analysis** (read-only): for ready phases, intersect each phase's `IN` border (from `## Phases in detail`) to detect shared files/modules; a phase that forecasts a migration is flagged (provisional number — first to merge keeps it, the others renumber on integration; truth is git).
7. **Base freshness (DETECT and WARN only)**: compare `git rev-parse <base>` vs `origin/<base>`; if local is BEHIND flag it — the executor advances the worktrees before launching.

## Step 4 — Output: BLUF + wave plan + warnings + handoff

ALWAYS return, in this order:

1. **Banner (plain text):** `Roadmap: <name/slug>  ·  repo: <name>  ·  integration: <branch>@<short-sha>  ·  Source: roadmap.md + live git · NO engram · <date-time>`.

2. **BLUF line:** `Plan: <N> phases → ✓ <d> done · <r> ready now (<p> parallel this wave) · <o> ops to attest · <k> deferred · ✗ <b> blocked · recommended: <launch wave 1 | attest ops X | promote Y>`.

3. **Wave plan table** — one row per phase, `.md` order, no phase omitted:

   | # | Phase | slug | Kind | Route (forecast) | Depends on | Status | Wave | Parallelizes with | Note |
   |---|---|---|---|---|---|---|---|---|---|
   | 1 | <name> | <slug> | code | organic | — | ✓ done | — | — | merge <sha> [git] |
   | 2 | <name> | <slug> | code | organic | 1 | ○ pending | 1 | {3} | ready: deps done |
   | 3 | <name> | <slug> | code | shot | 1 | ○ pending | 1 | {2} | ready |
   | 4 | <name> | <slug> | ops | — | — | ○ pending | 1 (ops-attest) | — | Verify: <how> |
   | 5 | <name> | <slug> | code | organic | 2 | ✗ blocked | 2 | — | waits for phase 2 |
   | 6 | <name> | <slug> | code | organic | 3 | ○ pending | deferred | — | Deferrable? yes |

4. **Warnings table** — one row per issue, never a flat list (always emit it, with a `none` row if clean):

   | Type | Phases | Evidence | Recommendation |
   |---|---|---|---|
   | file clash / migration collision / ops attestation / blocked chain / unbound / base-freshness / forecast-route-risk | <phase #s> | <file:line / number / dependency / branch behind> | <serialize / renumber / attest / start provider first / confirm / ff first> |

5. **Round forecast table**:

   | Round | Phases | Starts when | Human pauses |
   |---|---|---|---|
   | 1 | <phases> | now | triage confirmation · merge gate |
   | 2 | <phases> | round 1 merged | ops attestation (<phase>) · merge gate |

6. **Handoff to start** (the single copy-paste command; slug-first):
   ```
   /mala-pata-roadmap-orchestrate-start <slug>
   ```
   The executor re-derives everything live, so the same command works at any time and resumes a half-run roadmap. `roadmap-orchestrate` only plans.

**Emit this block's structural labels verbatim in English** — the Banner, the BLUF line, every table header (`#`, `Phase`, `slug`, `Kind`, `Route (forecast)`, `Depends on`, `Status`, `Wave`, `Parallelizes with`, `Note`, `Type`, `Phases`, `Evidence`, `Recommendation`, `Round`, `Starts when`, `Human pauses`) and the command line stay English; only the values follow the conversation language. State glyphs: `✓ done` / `◐ in progress` / `○ pending` / `✗ blocked`, with `[git]` / `[attested]` provenance in Note.

**Structure:** Precedence diagramming / PDM (PMBOK) + wave layering + live-git state derivation (house method).

## Hard rules
- **Refuse loops (Hard rule #0).** Any loop route in the DAG's `Tentative route` column, deferred or not, refuses the whole roadmap: no plan, no handoff.
- **READ-ONLY.** No worktree, no launch, no triage, no lane, no merge, no write, no commit. If the user asks "lanzá / orquestá de verdad", redirect to `/mala-pata-roadmap-orchestrate-start`.
- **Git = truth for `code` phases; declared `Status`+`Evidence` for `ops`.** Zero cache, zero memory: re-derive everything from the `.md` + live git on every run. Never mark an ops phase pending/blocked for lacking a branch or trailer.
- **The route is a forecast.** Never present it as the decided lane; triage decides on arrival.
- **Scope by the roadmap's `domain:`** — never mix domains. Pending only with zero evidence; work-exists-but-unbound → `? unbound`.
- The `git fetch` of Step 2 is the ONLY thing that touches network/git, and it is read-only (fetch + log + rev-parse).
- ABSOLUTE paths in commands when they are paths; the slug is preferred; relative only when talking to the user.

## What it does NOT do
- It does not execute, launch, triage, merge or clean up anything — `/mala-pata-roadmap-orchestrate-start` does.
- It does not replace `/mala-pata-roadmap-radar` (pure status + next command per phase) nor `/mala-pata-gaps` (completeness of the objective).
- It does not decide smoke or RDD (those run in each phase's lane tab) and it does not attest ops phases.
- It does not edit the roadmap `.md`, create kickoffs, or write to engram.
- It does not re-plan the roadmap (that is `/mala-pata-roadmap`); it reports the plan the DAG already carries.
- It only orchestrates roadmaps whose phases are all shot/organic; it refuses any roadmap containing a loop phase (use `/mala-pata-roadmap-radar <slug>` and drive loop phases by hand with `/mala-pata-loop` + `/mala-pata-loop-start`).

## Runtime compatibility
The state derivation, the wave plan and the command are portable to any CLI (git + optional `gh`). The handoff to the executor's Warp/Claude launch only applies when the runtime is Claude with Warp; in another CLI, return the plan and omit nothing else — the executor itself returns the per-worktree commands when Warp is unavailable.

**Structure:** precedence diagramming + wave layering + live-git state derivation = house method.
