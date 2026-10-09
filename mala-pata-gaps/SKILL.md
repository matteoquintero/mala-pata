---
name: mala-pata-gaps
description: READ-ONLY completeness auditor for a DOMAIN — given one or several roadmaps of the same domain + the real CODE, it finds what is missing to cover the total objective (follow-ups). Even if all phases are finished, something may be missing. It cross-checks 3 sources — the total objective (roadmaps), the follow-ups already NOTED (Level-2 / deferred / extra proposals not done / TODO-FIXME in code) and the gaps INFERRED from the code (codegraph/serena, anchored to evidence). Each gap comes out tagged [noted] or [inferred] with evidence (file:line or the annotation). It does NOT look only at the .md — it analyzes the code. It does NOT execute phases or touch code — it leaves its report in mala-pata/gaps/<dominio>.md (versioned) + an engram pointer, and suggests routing. Different from mala-pata-roadmap-radar (that one is phase status vs git; this one is completeness of the objective). Trigger — "tenemos follow ups", "gaps de <dominio>", "qué falta del dominio <X>", "qué falta para cubrir <objetivo>".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.2.0"
---

# /mala-pata-gaps — what is missing to cover a domain's objective (against the code)

Input: **the CLI's** — a **domain** (keyword, e.g. `facturacion`) or a **list of roadmap slugs** of the same domain.

Your job: say **what is missing to cover the TOTAL objective** of a domain — the follow-ups. This is not the phase status (that is `mala-pata-roadmap-radar`); it is **completeness**: even if all phases are "finished", is anything of the objective left uncovered? You answer it by cross-checking the domain's roadmaps with the **real code**.

> **This is not `mala-pata-roadmap-radar`.** radar tells you where the declared phases are (git). This one tells you **what is NOT declared/done and is needed** for the domain's objective. They complement each other.

## Requirements (orchestrate, do not reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP):
  - `git` — locate the repo and the real state. Always present.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded):
  - `codegraph` / `serena` — measure the real state of the code (what of the objective already exists, what does not) at symbol level. Fallback: grep/Read (coarser, say so).
  - `engram` — pointer to the domain's roadmaps. Fallback: list `mala-pata/roadmap/*.md`.

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP, e.g. serena). If a mandatory tool is missing, do not continue.

## Hard principles

- **Anchored to evidence, NEVER invented.** Each gap comes from a real annotation or from a reading of the code with `file:line`. If you cannot anchor it, it is not a gap — it is a question, mark it separately.
- **`[noted]` vs `[inferred]`** for each gap: noted = it was already written (Level-2, deferred, TODO); inferred = the model detected it by cross-checking objective + code. The human trusts each differently — like the `[rule/judgment]` of the other skills.
- **Read-only on the code/project.** It does NOT execute phases, does NOT touch code, does NOT create a kickoff/roadmap. But it DOES leave its **own report** in `mala-pata/gaps/<dominio>.md` + an engram pointer (like research/roadmap) — for traceability. It suggests routing and ends.
- **Over-discover, the human trims.** Better to propose one gap too many (marked `[inferred]`) than to stay silent. But never invented.

## Phase 0 — Resolve the domain and its roadmaps

1. Project root: `git -C <cwd> rev-parse --show-toplevel`.
2. Resolve the domain's roadmaps:
   - If the input is a **list of slugs** → those `.md` files in `mala-pata/roadmap/`.
   - If it is a **domain/keyword** → list `mala-pata/roadmap/*.md` and keep those that belong to that domain (by slug/objective). If there is ambiguity about which ones are included, list them and ask for confirmation (one question).
3. If no roadmaps match → say so and STOP; do not invent the objective.

## Phase 1 — TOTAL objective of the domain

Merge the **desired state** of all the domain's roadmaps: their "## Large objective" + the axes of the **coverage table** (MECE desired state). That set of axes is the **completeness contract** you will measure against. If two roadmaps overlap on an axis, it is a single one (MECE).

## Phase 2 — The 3 sources of gaps

**(a) Follow-ups already NOTED** (collect them, do not invent them):
- **Level 2** checklist of each roadmap (broad domain not covered).
- Axes marked **deferred** or **extra-proposal** that were NOT done.
- `TODO` / `FIXME` / notes in the domain's **code** (grep/codegraph).

**(b) Current state of the CODE** (measure, do not assume): for each axis of the objective (Phase 1), what is already implemented and what is not — with `codegraph_explore` / serena / grep. Anchor to `file:line`.

**(c) INFERRED gaps**: where the objective implies something the code does NOT do. E.g.: "the objective says that EVERY invoice error type must be actionable, but in code these 2 types have no action handler (`file:line`)". Reasoned from objective + code, never from nothing.

## Phase 3 — Gap analysis (desired state vs current state)

Same framework as the Gap Analysis of `/mala-pata-roadmap` (Step 4-ter), but **post-hoc and against the live code**: **desired state** (total objective, Phase 1) **minus** **current state** (code, Phase 2b) = **the gaps**. Add the noted (2a) and the inferred (2c). Deduplicate.

## Phase 4 — Output (fixed format, read-only)

```
Domain gaps: <domain>  ·  roadmaps: <slug, slug, …>  ·  repo: <name>  ·  <date-time>
Source: mala-pata/ roadmaps + live code

| # | Missing (what) | Objective axis | Evidence | Tag |
|---|-------------|------------------|-----------|-----|
| 1 | <what is missing, concrete> | <axis> | <file:line or annotation/roadmap> | [noted] / [inferred] |

Questions (not gaps, evidence was missing to confirm them): <or "none">
Routing suggestion (I do NOT execute): <gap> → /mala-pata-research or /mala-pata-triage
```

- **One row per gap**, concrete, with real evidence. No evidence → it does not go in the table (it goes to "Questions").
- **Mandatory tag** `[noted]` or `[inferred]` per row.
- If there are no gaps: say so explicitly + **which axes you verified** and why they are covered (like preview's empty-audit — not a bare "all good").

## Phase 5 — Persist the report (traceability)

Write the Phase 4 report to **`mala-pata/gaps/<dominio>.md`** (inside the repo, versioned; `mkdir -p` if it does not exist; `<dominio>` = the keyword, or a composite slug of the analyzed roadmaps). If it already exists, **update** that file — gaps is a **living backlog** of the domain, not an endless append nor a new file per run. Lightweight pointer in engram: `mem_save` topic_key `gaps/<dominio>`, one-line content `Gaps in file: <absolute path>` (do not duplicate the content — the file is the source). If engram is not available, the file is the source; warn in one line.

After persisting, you close: you suggest routing, **you do not execute phases or touch code**.

## Rules

- **Read-only on the code/project.** It does not execute phases, does not touch code, does not create a kickoff/roadmap. It DOES write its own report in `mala-pata/gaps/<dominio>.md` + engram pointer (its artifact, like research/roadmap).
- **Never invent.** Every gap anchored to an annotation or `file:line`. What cannot be anchored goes as a "Pregunta", not as a gap.
- **Does not overstep `mala-pata-roadmap-radar`** (phase status) — this one is completeness of the objective.
- **Fixed format** always.
- **No data**: if there are no roadmaps for the domain or no accessible code, ask for it; do not guess the objective or the gaps.

## What it does NOT do

- Does NOT execute or offer to execute a phase/lane.
- Does NOT create a kickoff, roadmap, research or code.
- Does NOT invent gaps — only noted or inferred-with-evidence.
- Does NOT dispatch `sdd-*` agents.
