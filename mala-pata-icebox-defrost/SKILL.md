---
name: mala-pata-icebox-defrost
description: DEFROST an icebox — melt a deferred backlog into action. Takes an icebox slug, runs research + triage IN PARALLEL over its frozen cubes, and produces ONE batch routing recommendation spanning roadmap..shot. It RECOMMENDS, it does NOT execute (no worktrees, no kickoffs, no code, no merges) — the research is PAID here (deferred from capture) and each cube's route is forecast; the human runs the emitted commands. The route is a MIX: a cube is its own shot/organic/loop, and roadmap appears ONLY when a group of cubes is proven to form ONE dependent objective — never defaulted by quantity (a long icebox is NOT a roadmap). Heavy by nature — it forecasts the cost and lets you scope to a subset before the research fan-out. Trigger — "descongelá el icebox <slug>", "defrost <slug>", "derretí el icebox", "ya quiero accionar el icebox <slug>".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "0.1.0"
---

# /mala-pata-icebox-defrost — melt an icebox into a batch routing plan

Input: **the one delivered by the CLI** — an **icebox slug** (resolves to `mala-pata/icebox/<slug>.md`), optionally a **subset of cube ids** to scope the melt.

Your job: take the icebox's frozen cubes, **research + triage them in parallel**, and hand back **ONE batch routing recommendation** — per cube (or group) the recommended lane and the copy-paste command to run it. You are the activation end of the icebox family: `mala-pata-icebox` froze; you **melt and recommend**; the human executes.

> **You RECOMMEND, you do NOT execute.** Same contract as `/mala-pata-research`, `/mala-pata-triage` and `/mala-pata-roadmap`: you write research docs and a routing plan, you do NOT create worktrees, write kickoffs, touch code, open PRs, or run any lane. Your deliverable is the plan + the research docs + the copy-paste commands.
> **Roadmap is a CONCLUSION, never a default by quantity.** A big icebox is NOT a roadmap. Per `/mala-pata-triage` and `/mala-pata-roadmap` (Hard rule #2), multi-unit is a conclusion of investigation, never inherited from "the list is long". Cubes are INDEPENDENT by construction, so the normal output is a **MIX** of routes; roadmap appears ONLY when a group of cubes is PROVEN to form one dependent objective. Do not rule it out, do not force it.
> **Research is paid HERE, and it is heavy.** Freezing was cheap precisely because research was deferred to this moment. Researching the whole icebox at once is the expensive step — so you FORECAST the cost and let the human SCOPE to a subset before the fan-out (Phase 2).
> **The route is a FORECAST, not a commitment.** Like a roadmap's phases, each cube's recommended lane is re-decided by `/mala-pata-triage` on arrival with the info of the moment. You forecast; triage rules.

## Requirements (orchestrate, do not reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP): `git` — resolve the repo root (the icebox + research docs live in the repo).
- **Recommended** (with fallback — warn in one line and continue degraded):
  - `codegraph` / `serena` — anchor each cube's research to the real code. Fallback: grep/Read.
  - `WebSearch` / `WebFetch` — external research per cube. Fallback: disclose there is no external research.
  - `engram` — read/write the `icebox/<slug>` and `research/<slug>` pointers. Fallback: the files are the source.

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP). If a mandatory tool is missing, do not continue.

## Phase 0 — Authorize (read-only on code; writes docs, not code)

Defrost RESEARCHES (read-only external + code) and RECOMMENDS. It writes **research docs** and **updates the icebox's cube statuses** — it writes no application code, creates no worktree/kickoff, opens no PR, runs no lane. If the human actually wants a cube IMPLEMENTED now, that is not defrost — route that one cube through `/mala-pata-triage` directly.

## Phase 1 — Load the icebox + select the cubes

1. Resolve the repo root (`git -C <cwd> rev-parse --show-toplevel`) and read `mala-pata/icebox/<slug>.md`. If it does not resolve → **STOP** and ask for the slug (do not invent cubes). If the input is a path, `Read` it directly.
2. From the frontmatter take `domain` and `project`; from `## Cubes` take every cube (`c<N>`, its DoD, size-hint, status).
3. **Select the in-scope cubes**: by default every cube with `status: frozen`. Skip `thawed`/`done` cubes unless the human explicitly asks to re-defrost them (a sharpen or a second angle). If the CLI passed a subset of ids, keep only those. If there are zero frozen cubes → say so and stop (nothing to melt).

## Phase 2 — Forecast + scope GATE (before the heavy fan-out)

The research fan-out is the expensive part. BEFORE launching it:
1. Report the forecast in one line: `Defrost <slug>: <n> frozen cubes in scope · research runs in parallel · heavy step.`
2. **GATE — ask once, stop and wait**: melt **all** `<n>`, a **subset** (which ids), or **cancel**? Do not launch research until the human answers. (This is the proportionality guard — a 30-cube icebox should not silently spawn 30 research runs.)

## Phase 3 — Research fan-out (parallel, delegated) — pay the research here

For each in-scope cube, in PARALLEL (cubes are independent), run research following `/mala-pata-research` — delegate one research worker per cube through the runtime's subagent mechanism, bounded to the scope the human approved. Each worker:
- Sharpens the cube: how it is done today + limits (cited), anchors to the REAL code (reuse-first — prove existing mechanisms are not enough before "new code"), JTBD, problem size, and the Heilmeier split (answer what the code/sources show; the human-only decisions become OPEN items).
- Writes `mala-pata/research/<cube-slug>.md` with `icebox: <slug>` in the frontmatter (the link that ties the research back to this icebox — the mirror of the `roadmap:` field), and a **verdict** (PROCEED / SHARPEN / RECONSIDER).
- Returns: the sharpened fields (What / Why / DoD / Decisions / Open decisions / Risk / size-signal), the verdict, and its research doc path.

Surface any **RECONSIDER** verdict prominently — research may propose killing or parking a cube (cheaper to kill here than after a cycle). A **SHARPEN** cube (a human-only decision still open) is flagged, not force-routed.

## Phase 4 — Triage per cube + grouping pass

1. **Triage each sharpened cube** (following `/mala-pata-triage`): from its What/DoD/Decisions, forecast the lane — `shot` (trivial, understood, 1-3 files, no migration/contract/new UI), `organic` (statable + decisions resolved), or `loop` (a decision that genuinely NEEDS DESIGN, not just "a decision exists"). A SHARPEN/open-decision cube is not routed until its question is answered.
2. **Grouping pass (the two symmetric mistakes to avoid):**
   - **Collapse**: cubes small and related enough to ship as ONE unit → group them into a single shot/organic instead of N tiny ones.
   - **Roadmap — only when PROVEN**: check whether a SUBSET of cubes forms ONE objective with real dependencies between them (not merely "same area", not "there are many"). If and only if a group is a genuine dependent objective → recommend `/mala-pata-roadmap` for that group, with the evidence (the dependency that makes it one objective). Everything else stays independent and routes per cube. **Never collapse the whole icebox into a roadmap by quantity.**

## Phase 5 — Batch routing recommendation + stamp the icebox

1. **Stamp each processed cube** in `mala-pata/icebox/<slug>.md`: `status: frozen` → `status: thawed(route: <lane | roadmap:<group>>, research: <cube-slug>)` (or `reconsider: <one-line reason>` for a killed/parked cube). **Write only — do NOT commit/push**; name the path + durable branch to the human. (Execution later flips it to `done`; that is `mala-pata-icebox-radar`'s reading, not yours.)
2. **Close — MANDATORY. BLUF first**, then the table (never prose-only):

   - Title: `**Defrosted — <icebox-slug>**`
   - BLUF: `Melted <n> cubes · <s> shot · <o> organic · <l> loop · <r> roadmap-group(s) · <k> reconsider  (domain <domain>)`
   - The real Markdown table (one row per cube/group — NEVER fenced):

     | Cube | Sharpened (What) | Verdict | Route (forecast) | Next step |
     |---|---|---|---|---|
     | c1 | <one line> | ✓ PROCEED | organic | `/mala-pata-triage <cube-slug>` |
     | c2+c5 (group) | <one line> | ✓ PROCEED | roadmap | `/mala-pata-roadmap <group-slug>` (dependent objective: <evidence>) |
     | c3 | <one line> | ◐ SHARPEN | — | answer: <the open question>, then re-defrost |
     | c4 | <one line> | ✗ RECONSIDER | — | <why — kill/park> |

   - **Grouping notes**: one line per non-obvious collapse or roadmap-group, with the evidence (why they are one unit / one dependent objective).
   - **Icebox:** `mala-pata/icebox/<slug>.md` — cubes stamped `thawed`, write-only, commit on `<durable branch>`.
   - **Research docs:** `mala-pata/research/<cube-slug>.md` (one per melted cube), linked by `icebox: <slug>`.
   - **Next step** — the entry is `/mala-pata-triage <slug>` per routed cube (triage re-decides the lane on arrival — the route above is a forecast). For a roadmap group, `/mala-pata-roadmap <group-slug>`.
   - **Structure:** Double Diamond (research) + lane routing (triage) + WBS grouping. Icebox defrost / thawed / forecast-not-commitment = house method.

   Emit the structural labels above (Defrosted, BLUF, Cube, Verdict, Route, Next step, Grouping notes, Icebox, Research docs, Structure) **verbatim in English**; only values and prose follow the conversation language.

This block is the only way to close on the happy path. **Only exceptions**: Phase 0 wrong-skill bounce; the Phase 1 missing-slug STOP; the Phase 2 scope gate.

## What it does NOT do (invariants)

- Does NOT execute: no worktree, no kickoff, no code, no PR, no merge, no lane run. It RECOMMENDS.
- Does NOT default to roadmap by quantity — roadmap only for a proven dependent-objective group; the normal output is a mix.
- Does NOT skip the forecast/scope gate — it never silently fans out research over a whole large icebox.
- Does NOT commit/push — research docs and the stamped icebox are write-only; the human commits them.
- Does NOT treat the forecast route as final — `/mala-pata-triage` re-decides on arrival.

## Relation to the family

- **The activation end** of the icebox family: `mala-pata-icebox` (freeze) → **`mala-pata-icebox-defrost`** (this: research + triage in parallel → batch recommendation) → `/mala-pata-triage` → `shot`/`organic`/`loop`/`roadmap`. `mala-pata-icebox-radar` reports how many cubes are done against git.
- **Orchestrates, does not reimplement**: it runs `/mala-pata-research` (per cube, parallel) and `/mala-pata-triage` (per cube) — those skills are the source of truth for their mechanics, exactly as `mala-pata-organic-start` defers to the ODD protocol.
- **Different from** `/mala-pata-roadmap` (decomposes ONE objective top-down) — defrost routes a POOL of independent cubes bottom-up, and only lifts a proven dependent-objective subset into a roadmap.
