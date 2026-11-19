---
name: mala-pata-icebox-defrost-start
description: RUN an approved defrost plan — the execution half of the melt. Reads the plan doc `/mala-pata-icebox-defrost` wrote (the per-cube research-vs-triage-direct table the human reviewed/edited), then runs research IN PARALLEL on the research-flagged cubes, triages every non-skip cube to inform, and recommends ONE vehicle that covers the WHOLE melted set — a single shot / organic / loop / roadmap, never a cube-by-cube table — stamping each melted cube `thawed` in the icebox. The vehicle is chosen by the whole set's aggregate shape (trivial→shot, specifiable→organic, design-open→loop, genuinely multi-unit→roadmap with the cubes as phases). It RECOMMENDS, it does NOT execute (no worktrees, no kickoffs, no code, no merges) — research is PAID here (only on the approved cubes); the human runs the single emitted command. Trigger — "corré el defrost de <slug>", "defrost start <slug>", "ejecutá el plan de defrost", "ya aprobé el plan, derretí <slug>".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "0.3.0"
---

# /mala-pata-icebox-defrost-start — run the approved defrost plan

Input: **the one delivered by the CLI** — an **icebox slug** (resolves to its plan doc `mala-pata/icebox/<slug>-defrost-plan.md`), or the path to the plan doc.

Your job: execute the **approved** defrost plan — research only the cubes the plan marks `research`, triage every non-`skip` cube to inform, then hand back **ONE recommendation: a single vehicle (shot / organic / loop / roadmap) that covers the WHOLE melted set** — never a cube-by-cube table. You are the execution half; `/mala-pata-icebox-defrost` wrote and the human approved the plan.

> **You RECOMMEND, you do NOT execute.** Same contract as `/mala-pata-research`/`/mala-pata-triage`/`/mala-pata-roadmap`: you write research docs + a routing recommendation and stamp the icebox, but you do NOT create worktrees, write kickoffs, touch code, open PRs, or run any lane. The human runs the emitted commands.
> **The plan is the authority — do not re-decide handling.** Research runs ONLY on cubes the approved plan marks `research`; `triage-direct` cubes skip straight to triage; `skip` cubes are left out. If the plan is missing, run `/mala-pata-icebox-defrost <slug>` first — do not improvise the classification here.
> **ONE vehicle covers the WHOLE set — never cube-by-cube.** Treat the entire melted set (the non-skip cubes) as a SINGLE objective and run the triage ladder on it: trivial → **shot**; specifiable with decisions resolved → **organic**; a genuinely open design decision → **loop**; genuinely multi-unit (several independent vertical slices or open architecture decisions) → **roadmap**, with the cubes as its candidate phases (independent cubes become parallelizable phases). You pick ONE; you do NOT emit a per-cube routing table. (The icebox freeze accumulates cubes independently; the defrost decides the single best way to EXECUTE the accumulated pile.)
> **The vehicle is a FORECAST.** The recommended vehicle is re-decided by `/mala-pata-triage` (or `/mala-pata-roadmap`'s own entry gate) on arrival with the info of the moment — it may collapse a roadmap to one unit, or split an organic. You forecast; triage/roadmap rule.

## Requirements (orchestrate, do not reinvent)

- **Mandatory** (no fallback — if missing, STOP): `git` — resolve the repo root (plan, icebox, research docs live in the repo).
- **Recommended** (with fallback — warn in one line and continue degraded):
  - `codegraph` / `serena` — anchor each cube's research to the real code. Fallback: grep/Read.
  - `WebSearch` / `WebFetch` — external research per cube. Fallback: disclose there is no external research.
  - `engram` — read/write the `icebox/<slug>` and `research/<slug>` pointers. Fallback: the files are the source.

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP). If a mandatory tool is missing, do not continue.

## Phase 0 — Authorize (read-only on code; writes docs, not code)

Running the plan RESEARCHES (read-only external + code) and RECOMMENDS. It writes research docs and stamps the icebox's cube statuses — no application code, no worktree/kickoff, no PR, no lane run.

## Phase 1 — Load the approved plan (do NOT re-classify)

1. Resolve the repo root and read `mala-pata/icebox/<slug>-defrost-plan.md`. **If it does not exist → STOP** and tell the human to run `/mala-pata-icebox-defrost <slug>` first (the plan is required; do not invent the classification). A path works directly.
2. Read every row of `## Cubes to melt`: `cube`, `DoD`, `size-hint`, `handling` (`research` | `triage-direct` | `skip`). Also read the icebox `mala-pata/icebox/<slug>.md` for the cubes' current status and the frontmatter `domain`/`project`.
3. Honor the `handling` column AS APPROVED — it reflects the human's edits. Do not second-guess it.

## Phase 2 — Research fan-out (parallel, delegated) — only the `research` cubes

For each cube marked `research`, in PARALLEL (cubes are independent), run research following `/mala-pata-research` — delegate one research worker per cube through the runtime's subagent mechanism. Each worker:
- Sharpens the cube: how it is done today + limits (cited), anchors to the REAL code (reuse-first — prove existing mechanisms are insufficient before "new code"), JTBD, problem size, and the Heilmeier split (human-only decisions become OPEN items).
- Writes `mala-pata/research/<cube-slug>.md` with `icebox: <slug>` in the frontmatter (the link back to this icebox) and a **verdict** (PROCEED / SHARPEN / RECONSIDER).
- Returns the sharpened fields (What/Why/DoD/Decisions/Open decisions/Risk/size-signal), the verdict, and the doc path.

Surface any **RECONSIDER** prominently (research may propose killing/parking a cube). A **SHARPEN** cube (a human-only decision still open) is flagged, not force-routed. `triage-direct` cubes skip this phase entirely.

## Phase 3 — Assess the whole set → ONE covering vehicle

> **Canonical lane-routing gate — single source of truth.** Apply `_shared/mala-pata-lane-gate.md` verbatim; it supersedes any restatement in this skill. Do not paraphrase or re-derive it.

1. **Sharpen each cube to INFORM (not to route one-by-one):** the `research` cubes from their sharpened fields, the `triage-direct` cubes from their DoD as-is. Set aside any **SHARPEN**/open-decision cube (its question must be answered first) and any **RECONSIDER** cube (research proposes killing/parking it) — they do NOT enter the covering set until resolved.
2. **Treat the remaining set as ONE objective** and apply the triage ladder (`_shared/mala-pata-lane-gate.md`) to the WHOLE thing → pick exactly **ONE** vehicle:
   - **shot** — the set, together, is a trivial already-understood change (1-3 files, no decision/migration/new UI).
   - **organic** — the set, together, is specifiable (What / DoD / Decisions resolved) and fits one unit.
   - **loop** — the set, together, carries a genuinely open design decision that needs design.
   - **roadmap** — the set is genuinely multi-unit (several independent vertical slices, or several open architecture decisions): each cube becomes a candidate **phase** (independent cubes → parallelizable phases). This is the natural vehicle for a diverse pile, and — unlike the retired per-cube design — it is NOT gated on proving inter-cube dependencies; independent phases are valid.
   Pick by the SET's aggregate shape, not by cube count alone: a big pile of trivia can still be one organic, and two entangled cubes can be a loop. You emit ONE vehicle, never a per-cube routing table.

## Phase 4 — Stamp the icebox + ONE covering recommendation

1. **Stamp each processed cube** in `mala-pata/icebox/<slug>.md`: `status: frozen` → `status: thawed(route: <the single vehicle>, research: <cube-slug | none>)` for a cube in the covering set (all covering-set cubes carry the SAME vehicle); `reconsider: <one-line reason>` for a killed/parked cube; a **SHARPEN** cube stays `frozen` (held — re-defrost once its open question is answered). Keep the `route:`/`research:` stamp shape `mala-pata-icebox-radar` reads. **Write only — do NOT commit/push**; name the path + durable branch. (Execution later flips it to `done`; that is `mala-pata-icebox-radar`'s reading.)
2. **Close — MANDATORY. BLUF first**, then the table (never prose-only):

   - Title: `**Defrosted — <icebox-slug>**`
   - BLUF: `Melted <n> cubes → recommend ONE <vehicle> covering all · <k> reconsider · <h> sharpen  (domain <domain>)`
   - **Recommendation**: one line — the single vehicle + WHY (the set's aggregate shape that put it there, e.g. "multi-unit: 4 independent slices → roadmap" / "specifiable, one unit → organic").
   - The real Markdown table (one row per cube in the covering set — these are the set's contents, and the roadmap's candidate phases when the vehicle is roadmap — NEVER fenced):

     | Cube | Sharpened (What) | Verdict | In the set as |
     |---|---|---|---|
     | c1 | <one line> | ✓ PROCEED | phase (parallel) |
     | c2 | <one line> | ✓ PROCEED | phase (depends on c1) |
     | c3 | <one line> | ◐ SHARPEN | held — answer: <open question> |
     | c4 | <one line> | ✗ RECONSIDER | out — <why: kill/park> |

     (When the vehicle is shot/organic/loop the `In the set as` cell is `part of the single change`; when roadmap it is `phase` with its parallel/depends note.)
   - **Icebox:** `mala-pata/icebox/<slug>.md` — cubes stamped `thawed`, write-only, commit on `<durable branch>`.
   - **Research docs:** `mala-pata/research/<cube-slug>.md` (one per `research` cube), linked by `icebox: <slug>`.
   - **Next step** — the SINGLE command for the recommended vehicle (the whole set as one objective; triage / roadmap re-decide on arrival): `/mala-pata-roadmap <slug>` (roadmap — hand it the cubes as candidate phases), or `/mala-pata-triage <slug>` (loop / organic / shot — triage routes it). Hold the SHARPEN cubes until answered; leave the RECONSIDER cubes out.
   - **Structure:** plan/run split + Double Diamond (research) + one-objective triage ladder (triage / roadmap). Icebox defrost run / thawed / one-covering-vehicle / forecast-not-commitment = house method.

   Apply `_shared/mala-pata-structural-labels.md` verbatim (labels are frozen: never translate, never swap for case-specific ones, omit-never-rename). Emit the structural labels above (Defrosted, BLUF, Recommendation, Cube, Sharpened (What), Verdict, In the set as, Icebox, Research docs, Next step, Structure) and the table columns exactly as written (`Cube` · `Sharpened (What)` · `Verdict` · `In the set as`) **verbatim in English**; only values and prose follow the conversation language.

This block is the only way to close on the happy path. **Only exceptions**: Phase 0 wrong-skill bounce; the Phase 1 missing-plan STOP.

## What it does NOT do (invariants)

- Does NOT execute: no worktree, no kickoff, no code, no PR, no merge, no lane run. It RECOMMENDS.
- Does NOT re-classify handling — the approved plan is the authority; research runs only on `research` cubes.
- Does NOT emit a cube-by-cube routing table — it recommends ONE vehicle covering the whole set (roadmap, with the cubes as phases, is the natural one for a multi-unit pile).
- Does NOT commit/push — research docs + the stamped icebox are write-only.
- Does NOT treat the forecast route as final — `/mala-pata-triage` re-decides on arrival.

## Relation to the family

- **The run half** of the melt: `mala-pata-icebox` (freeze) → `mala-pata-icebox-defrost` (plan: classify + approval table → STOP) → **`mala-pata-icebox-defrost-start`** (this: research + one-objective triage of the whole set → ONE covering recommendation) → `/mala-pata-triage` or `/mala-pata-roadmap` → the lane(s). `mala-pata-icebox-radar` reports cube status against git.
- **Mirrors** `/mala-pata-loop-start` and `/mala-pata-organic-start`: the `-start` runner that executes the plan the generator left.
- **Orchestrates, does not reimplement**: it runs `/mala-pata-research` (per `research` cube, parallel) and applies the triage ladder (`/mala-pata-triage`) to the whole set as one objective — those skills own their mechanics.
