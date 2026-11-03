---
name: mala-pata-icebox-defrost-start
description: RUN an approved defrost plan — the execution half of the melt. Reads the plan doc `/mala-pata-icebox-defrost` wrote (the per-cube research-vs-triage-direct table the human reviewed/edited), then runs research IN PARALLEL on the research-flagged cubes, triages every non-skip cube, does the grouping pass, and returns ONE batch routing recommendation (roadmap..shot) — stamping each melted cube `thawed` in the icebox. It RECOMMENDS, it does NOT execute (no worktrees, no kickoffs, no code, no merges) — research is PAID here (only on the approved cubes); the human runs the emitted lane commands. Roadmap appears ONLY for a proven dependent-objective group, never defaulted by quantity. Trigger — "corré el defrost de <slug>", "defrost start <slug>", "ejecutá el plan de defrost", "ya aprobé el plan, derretí <slug>".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "0.1.1"
---

# /mala-pata-icebox-defrost-start — run the approved defrost plan

Input: **the one delivered by the CLI** — an **icebox slug** (resolves to its plan doc `mala-pata/icebox/<slug>-defrost-plan.md`), or the path to the plan doc.

Your job: execute the **approved** defrost plan — research only the cubes the plan marks `research`, triage every non-`skip` cube, group them, and hand back **ONE batch routing recommendation**. You are the execution half; `/mala-pata-icebox-defrost` wrote and the human approved the plan.

> **You RECOMMEND, you do NOT execute.** Same contract as `/mala-pata-research`/`/mala-pata-triage`/`/mala-pata-roadmap`: you write research docs + a routing recommendation and stamp the icebox, but you do NOT create worktrees, write kickoffs, touch code, open PRs, or run any lane. The human runs the emitted commands.
> **The plan is the authority — do not re-decide handling.** Research runs ONLY on cubes the approved plan marks `research`; `triage-direct` cubes skip straight to triage; `skip` cubes are left out. If the plan is missing, run `/mala-pata-icebox-defrost <slug>` first — do not improvise the classification here.
> **Roadmap is a CONCLUSION, never a default by quantity.** Cubes are independent; the normal output is a MIX of lanes. A roadmap group appears ONLY when a subset is PROVEN to form one dependent objective (with the evidence). Do not force it, do not rule it out.
> **The route is a FORECAST.** Each cube's lane is re-decided by `/mala-pata-triage` on arrival with the info of the moment. You forecast; triage rules.

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

## Phase 3 — Triage every non-skip cube + grouping pass

> **Canonical lane-routing gate — single source of truth.** Apply `_shared/mala-pata-lane-gate.md` verbatim; it supersedes any restatement in this skill. Do not paraphrase or re-derive it.

1. **Triage each cube** (following `/mala-pata-triage`): the `research` cubes from their sharpened fields, the `triage-direct` cubes from their DoD as-is → a lane forecast (`shot`/`organic`/`loop`). A SHARPEN/open-decision cube is not routed until its question is answered.
2. **Grouping pass:**
   - **Collapse**: cubes small and related enough to ship as ONE unit → one shot/organic instead of N.
   - **Roadmap — only when PROVEN**: a SUBSET that forms ONE objective with real dependencies between its cubes → recommend `/mala-pata-roadmap` for that group, WITH the evidence (the dependency that makes it one objective). Everything else routes per cube. **Never collapse the whole icebox into a roadmap by quantity.**

## Phase 4 — Stamp the icebox + batch routing recommendation

1. **Stamp each processed cube** in `mala-pata/icebox/<slug>.md`: `status: frozen` → `status: thawed(route: <lane | roadmap:<group>>, research: <cube-slug | none>)`, or `reconsider: <one-line reason>` for a killed/parked cube. **Write only — do NOT commit/push**; name the path + durable branch. (Execution later flips it to `done`; that is `mala-pata-icebox-radar`'s reading.)
2. **Close — MANDATORY. BLUF first**, then the table (never prose-only):

   - Title: `**Defrosted — <icebox-slug>**`
   - BLUF: `Melted <n> cubes · <s> shot · <o> organic · <l> loop · <r> roadmap-group(s) · <k> reconsider  (domain <domain>)`
   - The real Markdown table (one row per cube/group — NEVER fenced):

     | Cube | Sharpened (What) | Handling | Verdict | Route (forecast) | Next step |
     |---|---|---|---|---|---|
     | c1 | <one line> | triage-direct | — | organic | `/mala-pata-triage <cube-slug>` |
     | c2 | <one line> | research | ✓ PROCEED | loop | `/mala-pata-triage <cube-slug>` |
     | c2+c5 (group) | <one line> | research | ✓ PROCEED | roadmap | `/mala-pata-roadmap <group-slug>` (dependent: <evidence>) |
     | c3 | <one line> | research | ◐ SHARPEN | — | answer: <open question>, then re-plan |
     | c4 | <one line> | research | ✗ RECONSIDER | — | <why — kill/park> |

   - **Grouping notes**: one line per non-obvious collapse or roadmap-group, with the evidence.
   - **Icebox:** `mala-pata/icebox/<slug>.md` — cubes stamped `thawed`, write-only, commit on `<durable branch>`.
   - **Research docs:** `mala-pata/research/<cube-slug>.md` (one per `research` cube), linked by `icebox: <slug>`.
   - **Next step** — `/mala-pata-triage <slug>` per routed cube (triage re-decides the lane on arrival — the route is a forecast); `/mala-pata-roadmap <group-slug>` for a roadmap group.
   - **Structure:** plan/run split + Double Diamond (research) + lane routing (triage) + WBS grouping. Icebox defrost run / thawed / forecast-not-commitment = house method.

   Emit the structural labels above (Defrosted, BLUF, Cube, Handling, Verdict, Route, Next step, Grouping notes, Icebox, Research docs, Structure) **verbatim in English**; only values and prose follow the conversation language.

This block is the only way to close on the happy path. **Only exceptions**: Phase 0 wrong-skill bounce; the Phase 1 missing-plan STOP.

## What it does NOT do (invariants)

- Does NOT execute: no worktree, no kickoff, no code, no PR, no merge, no lane run. It RECOMMENDS.
- Does NOT re-classify handling — the approved plan is the authority; research runs only on `research` cubes.
- Does NOT default to roadmap by quantity — only a proven dependent-objective group.
- Does NOT commit/push — research docs + the stamped icebox are write-only.
- Does NOT treat the forecast route as final — `/mala-pata-triage` re-decides on arrival.

## Relation to the family

- **The run half** of the melt: `mala-pata-icebox` (freeze) → `mala-pata-icebox-defrost` (plan: classify + approval table → STOP) → **`mala-pata-icebox-defrost-start`** (this: research + triage from the approved plan → batch recommendation) → `/mala-pata-triage` → lanes. `mala-pata-icebox-radar` reports cube status against git.
- **Mirrors** `/mala-pata-loop-start` and `/mala-pata-organic-start`: the `-start` runner that executes the plan the generator left.
- **Orchestrates, does not reimplement**: it runs `/mala-pata-research` (per `research` cube, parallel) and `/mala-pata-triage` (per cube) — those skills own their mechanics.
