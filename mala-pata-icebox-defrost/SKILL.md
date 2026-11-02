---
name: mala-pata-icebox-defrost
description: PLAN the defrost of an icebox — classify each frozen cube (triage-first, cheap, NO research yet) into "needs research" vs "triage-direct", write an editable approval table to a plan doc, and STOP. It is the PLAN half of the melt (its runner is `/mala-pata-icebox-defrost-start`): you review and EDIT the plan, then run the start to actually research + triage. It does NOT run research, does NOT route, does NOT execute — it only reads the icebox + reasons the triage form-gate per cube and writes `mala-pata/icebox/<slug>-defrost-plan.md` (write-only, no commit). Splitting plan from run keeps the expensive research behind an explicit human approval. Trigger — "planeá el defrost de <slug>", "qué cubes necesitan research", "preparemos el defrost del icebox <slug>", "defrost plan <slug>".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "0.2.0"
---

# /mala-pata-icebox-defrost — plan the melt (classify + approval table, then STOP)

Input: **the one delivered by the CLI** — an **icebox slug** (resolves to `mala-pata/icebox/<slug>.md`), optionally a **subset of cube ids** to scope the plan.

Your job: look at the icebox's frozen cubes and, **cheaply (triage-first, no research)**, classify each one into **`research`** (needs sharpening before it can be routed) or **`triage-direct`** (concrete enough to route straight). Write that as an **editable approval table** to a plan doc and **STOP** for the human to review/edit. The heavy work (research fan-out + triage) is done by the runner `/mala-pata-icebox-defrost-start` from the approved plan.

> **You PLAN, you do NOT run.** No research, no web, no deep code dive, no routing, no execution. You read the icebox and apply the triage FORM GATE (What/DoD/Decisions) to each cube's one line — that is cheap. The expensive research is deferred to the start, behind the human's approval of this plan.
> **This is the plan/run split.** Like `/mala-pata-loop` → `/mala-pata-loop-start`: this writes the plan + stops at a human gate; `/mala-pata-icebox-defrost-start` executes it. The plan doc is an editable artifact — the human can flip a cube research↔triage-direct before running.
> **Classify, do not decide the final lane.** `research`/`triage-direct` is a HANDLING decision (does this cube need sharpening first?), not the lane. The lane (shot/organic/loop/roadmap) is decided later by `/mala-pata-triage` inside the start. Do not over-reach into the lane here.

## Requirements (orchestrate, do not reinvent)

- **Mandatory** (no fallback — if missing, STOP): `git` — resolve the repo root (the icebox + plan doc live in the repo).
- **Recommended** (with fallback — warn in one line and continue degraded):
  - `engram` — read/write the `icebox/<slug>` pointer. Fallback: the file is the source.

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP). If a mandatory tool is missing, do not continue.

## Phase 0 — Authorize (read-only on code; writes a plan doc only)

Planning the defrost reads the icebox and writes ONLY the plan doc (`mala-pata/icebox/<slug>-defrost-plan.md`). No code, no research, no execution. Always safe.

## Phase 1 — Load the icebox + select the cubes

1. Resolve the repo root (`git -C <cwd> rev-parse --show-toplevel`) and read `mala-pata/icebox/<slug>.md`. If it does not resolve → **STOP** and ask for the slug. A path works directly.
2. Take `domain`/`project` from the frontmatter and every cube from `## Cubes` (`c<N>`, DoD, size-hint, status).
3. **Select in-scope cubes**: by default every `status: frozen` cube; skip `thawed`/`done`/`reconsider` unless the human asks to re-plan them. If the CLI passed a subset of ids, keep only those. Zero frozen cubes → say so and stop.

## Phase 2 — Classify each cube (triage-first, cheap — NO research)

For each in-scope cube, apply the `/mala-pata-triage` FORM GATE to its one-line DoD (this is reasoning on the text + size-hint, NOT research, NOT a code dive, NOT web):

- **`triage-direct`** — the cube's **What + DoD are concrete AND its decisions are obvious** (size-hint typically `shot`/`organic`). It can go straight to `/mala-pata-triage` and route without sharpening.
- **`research`** — the cube has a **named uncertainty / an open decision that needs design or external evidence**, or its DoD is still fuzzy (size-hint `loop` or `?`, or the line reads as "decidir …", "ver si …", a product/architecture call). It needs `/mala-pata-research` before it can be routed.
- **`skip`** (optional) — the human pre-marked it out of this melt.

Keep it cheap and proportional — a one-line reason per cube is enough. **Do NOT research to decide this** (that would defeat the whole gate); when genuinely unsure, lean `research` (cheaper to over-sharpen one cube than to misroute it).

## Phase 3 — Write the plan doc + approval table, then STOP

1. Write `mala-pata/icebox/<slug>-defrost-plan.md`:

```markdown
---
icebox_slug: <slug>
project: <project>
domain: <domain>
plan_created_at: <ISO 8601>
---
# Defrost plan: <slug>

> Review and EDIT the `handling` column (flip research ↔ triage-direct, or set skip), then run:
> `/mala-pata-icebox-defrost-start <slug>`

## Cubes to melt
| cube | DoD | size-hint | handling | why |
|---|---|---|---|---|
| c1 | <one line> | organic | triage-direct | concrete DoD, decisions obvious |
| c2 | <one line> | loop | research | open decision needs design/evidence |
```

   (The frontmatter keys, the `## Cubes to melt` heading and the `handling` values `research`/`triage-direct`/`skip` are fixed identifiers read by `/mala-pata-icebox-defrost-start`; keep them verbatim.)

2. **Timestamps.** Fill `plan_created_at` from the machine's local clock — run `date '+%Y-%m-%dT%H:%M:%S%z'` and use its exact output (local time with UTC offset, e.g. `2026-11-01T17:25:40-0500`); never invent it or default to UTC.
3. **Write only — do NOT commit/push.** Name the path + durable branch to the human.
4. **Pointer in engram** (optional): `mem_save` topic_key `icebox/<slug>/defrost-plan`, one-line content `Defrost plan in file: <absolute path>`. Fallback: the file is the source.

## Phase 4 — Close (MANDATORY: show the table + STOP)

- Title: `**Defrost plan — <icebox-slug>**`
- BLUF: `Plan <slug> · domain <domain> · <n> cubes · research <r> · triage-direct <t> · skip <s>`
- The **approval table** rendered as a REAL Markdown table (never fenced, one line per cell) — the same rows written to the plan doc.
- **Plan:** `mala-pata/icebox/<slug>-defrost-plan.md` — editable, write-only, commit on `<durable branch>`.
- **Next step** (after you review/edit the `handling` column):

  ```
  /mala-pata-icebox-defrost-start <slug>
  ```

- **Structure:** plan/run split (approve before the expensive step) + triage form-gate classification. Icebox defrost plan = house method.

Emit the structural labels above (Defrost plan, BLUF, Plan, Next step, Structure) **verbatim in English**; only values and prose follow the conversation language.

This block is the only way to close on the happy path. **Only exceptions**: Phase 0 wrong-skill bounce; the Phase 1 missing-slug / no-frozen-cubes STOP.

## What it does NOT do (invariants)

- Does NOT run research, triage, or any lane — it only classifies (cheap) and writes the plan.
- Does NOT decide the final lane — `handling` is research-vs-direct, not shot/organic/loop/roadmap.
- Does NOT commit/push — the plan doc is write-only and editable by the human.
- Does NOT skip the human gate — it always STOPS after writing the plan; the start runs only on the approved/edited plan.

## Relation to the family

- **The plan half** of the melt: `mala-pata-icebox` (freeze) → **`mala-pata-icebox-defrost`** (this: classify + approval table → STOP) → `mala-pata-icebox-defrost-start` (run research + triage from the approved plan) → `/mala-pata-triage` → lanes. `mala-pata-icebox-radar` reports cube status against git.
- **Mirrors** `/mala-pata-loop` → `/mala-pata-loop-start` and `/mala-pata-organic` → `/mala-pata-organic-start`: a planner that writes a doc + stops at a human gate, and a `-start` runner that executes.
