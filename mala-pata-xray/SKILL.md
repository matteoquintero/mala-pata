---
name: mala-pata-xray
description: >
  READ-ONLY per-unit detail pass — an x-ray of a unit of work that REVEALS the
  implementation-strategy detail the planning left implicit (cost/budget, the
  shape of what is fed to each dependency, the riskiest integration,
  pre-processing) and, when the unit lives in an artifact, ENRICHES it in place
  so that detail travels downstream to the kickoff → loop → SDD instead of
  leaking. Usable AT ANY MOMENT on ANY unit — a roadmap (walks it phase by
  phase), a kickoff, a research doc, or a plain objective (inline, no artifact).
  It does NOT execute, does NOT route (triage still rules), does NOT create
  worktrees or write code; the only thing it writes is the unit's own `.md`.
  Concrete tools/techniques never enter the skill — a broad approach-unknown is
  flagged `needs spike: <profile>` and resolved later in the spike (reuses
  `_shared/mala-pata-spike-catalog.md`), so the skill stays domain-neutral.
  Trigger — "radiografiá esta fase/kickoff/idea", "qué le falta a cada fase
  antes de ejecutar", "mostrame lo oculto de <unidad>", "detallá fase por fase",
  "profundizá <unidad> antes de ejecutar".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "0.1.1"
---

# /mala-pata-xray — reveal the hidden implementation detail of a unit, before executing it

Input: **the one delivered by the CLI** — a **slug/path** of a unit (a roadmap, a kickoff, a research doc) or a **plain objective in text**.

Your job: take a unit of work and **x-ray it** — pass it through a battery of detail lenses that surface the implementation-strategy decisions the planning left implicit, give each unit a **verdict** (what to keep / re-scope / split / drop / add), flag any broad approach-unknown as a **spike**, and — when the unit lives in an artifact — **write the resolved detail back into that artifact in place** so it travels to whoever executes next. It is to a unit of work what a radiograph is to a body: it shows the skeleton under the surface **before** anyone cuts.

> **It reveals; it does not build.** It does NOT execute the unit, does NOT route it (`/mala-pata-triage` still decides the lane on arrival), does NOT create a worktree, does NOT write code, does NOT run any lane. The only thing it ever writes is the unit's own `.md`.
> **It fills the leak between planning and execution.** A roadmap chases coverage (which phases, MECE) and a kickoff captures What/Why/Done — but the per-unit *how* (cost/budget, the shape of what you feed a costly dependency, the riskiest integration, needed pre-processing) is usually left implicit, so it never reaches the kickoff/loop and SDD just executes without it. This pass makes that *how* explicit and pins it to the unit.
> **Domain-neutral by construction.** The skill never names a concrete tool or technique. A broad, approach-level unknown is flagged `needs spike: <profile>` and the concrete answer (any tool, any trick) is chosen later IN the spike. The spike-catalog is the reuse hook; the skill stays generic.

## Requirements (orchestrate, do not reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP): `git` — resolve the repo root for artifact-backed inputs (`git rev-parse --show-toplevel`).
- **Recommended** (with fallback — warn in one line and continue degraded):
  - `codegraph` / `serena` — anchor a lens to the real code (does this unit already have the mechanism? what does it really call?). Fallback: grep/Read.
  - `engram` — continuity pointer. Fallback: the unit's `.md` is the source of truth; a plain-objective x-ray lives in the close.

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP, e.g. serena). If the mandatory tool is missing, do not continue.

## Phase 0 — Authorize (read-only guard)

X-raying is **read-only on the project's code** — it inspects, reveals and recommends. The only write it may do is enrich the **unit's own `.md`** (Step 4), and only when the human approves it at the gate. A plain-objective input has no artifact → the x-ray is inline only, nothing is written. If the request is to explain/compare rather than to detail a unit, stay read-only and answer directly; do not enrich anything.

## Step 1 — Resolve the target (what am I x-raying?)

Detect the input type and resolve it (prefer the slug — the full path is a pain):

- **A roadmap** → `<repo-root>/mala-pata/roadmap/<slug>.md` → a **multi-unit** target: you walk its phases, one at a time (Step 3).
- **A kickoff** → `<repo-root>/mala-pata/kickoffs/<slug>.md` → a **single-unit** target (one change).
- **A research doc** → `<repo-root>/mala-pata/research/<slug>.md` → a **single-unit** target (an idea).
- **A plain objective** (free text, no slug resolves) → a **single-unit** target with **no artifact** — the x-ray is emitted inline only.

`Read` the artifact in full when there is one (its phases/fields, borders, dependencies). If a slug was given but nothing resolves **and** there is no objective text → **STOP** and ask what to x-ray; do not invent the unit.

## Step 2 — Load the lens set (the film)

Load `_shared/mala-pata-spike-catalog.md` (the profile index) and assemble the **x-ray lenses** you will shine on each unit. Each lens asks for a decision the planning left implicit:

- **Cost / budget** — what does this unit consume at run time (compute, calls to a costly dependency, storage, wall-clock)? Is there a budget? If a dependency is expensive per use, the budget is a decision to make NOW, not at apply time.
- **Shape of what is fed to each dependency** — for every dependency the unit calls, decide the **shape and size of the payload** you hand it. Passing the raw/whole thing when a reduced or pre-processed form would do is a decision deferred by accident.
- **Pre-processing / reduction** — is there a cheaper transform that should run **before** the costly step, so the costly step sees less?
- **Riskiest integration first** (tracer bullet) — which integration is most likely to break this unit? Prove it early and make the tradeoff explicit before it becomes a bug.
- **Spike profiles** (from the catalog) — when a lens hits a **broad, approach-level** unknown (not a detail), fork it to a profile: `data` (schema/volume/migration shape), `integration` (an external contract/limits/failure semantics), `infra` (provisioning/capacity), or `generic`. That becomes a `needs spike: <profile>` flag — the skill does NOT answer it here.

The lens list is the reusable checklist; a project may surface more, but these are the floor. **No lens ever names a concrete tool** — it names the decision, and the concrete answer is the spike's job.

## Step 3 — X-ray unit by unit (gate per unit)

For each unit (the phases of a roadmap in DAG order, or the single unit), one at a time:

1. **Shine the lenses** (Step 2), anchored to the real code when `codegraph`/`serena` is available (does the mechanism already exist? what does the unit actually call?). Reuse-first: a decision the code already makes is not a finding.
2. **Verdict** (Stage-Gate vocabulary) — exactly one of: `keep` · `re-scope` · `split` · `drop` · `add`, plus a `needs spike: <profile>` flag when a lens forked to one. `add` = a decision the unit is missing and must carry; `drop` = something the code already covers; `split`/`re-scope` = the unit's border is wrong for what the lenses revealed.
3. **Propose the concrete enrichment** — the exact lines that would go into the unit's `Decisions already made` (and, for a roadmap phase, its `IN / OUT` border). Propose of more; the human trims.
4. **Gate (proportional).** Present the proposal for the unit and let the human approve/trim. **Batch the clean units** (a unit the lenses left untouched is reported, not paused on); **STOP and ask only on a unit with a real decision** — one focused question at a time, never a batch, never invent scope. A unit flagged `needs spike` is reported with the flag; this skill does not open the spike (that is `/mala-pata-research --spike`).

## Step 4 — Write-back (only when the unit lives in an artifact)

For each approved unit, **enrich its `.md` in place** so the detail travels downstream:

- **Roadmap phase** → add the approved lines to that phase's `Decisions already made` and adjust its `IN / OUT` border.
- **Kickoff** → add to `Decisions already made`.
- **Research doc** → add to `Define — Decisions already made` / `Open decisions` (a `needs spike` flag maps to an Open decision).

Rules: **idempotent** — write the enrichment inside a single managed sub-block per unit so a re-run **replaces** it and never duplicates. **Write-only — do NOT commit/push** (same discipline as `/mala-pata-roadmap` and `/mala-pata-organic`): leave the file on the unit's durable branch and tell the human the path so they commit it in their normal flow. A **plain-objective** target has no artifact → nothing is written; the x-ray lives in the close (offer an optional engram save).

## Step 5 — Close (MANDATORY: BLUF + table)

**BLUF first** — one `Result:` line above the table: `Result: ✓ x-rayed · <n>/<n> units` (or `◐ partial: <reason>`).

Then the table — **one unit per row**, 4 columns:

| Unit | Verdict | Added / Removed | Spike |
|---|---|---|---|
| `<unit 1>` | keep | — | ∅ |
| `<unit 2>` | add | +budget for `<dependency>`, +pre-processing before `<step>` | ∅ |
| `<unit 3>` | re-scope | OUT: `<piece the code already covers>` | needs spike: integration |

- **Target:** `<the artifact path, repo-relative>` (or `inline — plain objective`), enriched in place / not written.
- **Next step** — route each unit by `/mala-pata-triage` as usual (the x-ray detail now rides in the unit; triage still rules the lane).
- **Structure:** `RUP Elaboration (resolve implementation risk per increment before construction) + risk-driven Spikes (XP) + Stage-Gate verdicts (Cooper) + Tracer-bullet "riskiest integration first" (Hunt & Thomas) / Walking Skeleton (Cockburn). X-ray metaphor + per-unit write-back + spike-catalog reuse = house method.`

**Frozen structural label set** (this block applies `_shared/mala-pata-structural-labels.md` verbatim — emit these EXACTLY, in English, even when the conversation is in another language; only Value/Evidence content and surrounding prose are localized):
`Result:` · table headers `Unit | Verdict | Added / Removed | Spike` · verdict tokens `keep` `re-scope` `split` `drop` `add` · flag `needs spike: <profile>` · `Target:` · `Next step` · `Structure:`. Rows are one-per-unit; the `Spike` cell is `∅` when none. No label is translated, renamed or added.

This block is the only way to close on the happy path. **Only exceptions:** Phase 0 read-only stance; a Step 3 gate question on a unit with a real decision; the Step 1 STOP when nothing resolves.

## Persistence

The **enriched unit `.md`** is the artifact — that is where the detail now lives. Optionally leave a one-line engram pointer `xray/<target>` for discoverability (fallback: the `.md` is the source). A plain-objective x-ray with no artifact may be saved with `mem_save` topic `xray/<slug>` if the human wants future continuity.

## What it does NOT do (invariants)

- Does NOT execute the unit, run a lane, or create a worktree / write code.
- Does NOT route — `/mala-pata-triage` still decides the lane on arrival.
- Does NOT name a concrete tool/technique — a broad unknown is a `needs spike: <profile>` flag, resolved later in the spike.
- Does NOT replace `/mala-pata-gaps` (domain completeness) nor `/mala-pata-roadmap-radar` (status) nor `/mala-pata-research` (sharpens the WHAT); it details the HOW of a unit.
- Does NOT commit/push the enriched `.md` — write-only; the human commits it.

## Relation to the family

- An **orthogonal companion**, usable at any point of the pipeline: after `/mala-pata-roadmap` (detail each phase), before a kickoff is executed (detail the change), or on a raw idea / research doc (detail the approach). Not a route and not a gate — it enriches whatever unit you point it at.
- **Reuses** `_shared/mala-pata-spike-catalog.md` (profiles) and `_shared/mala-pata-structural-labels.md` (close labels).
- **Different from** `/mala-pata-research` (afila el QUÉ, pre-triage), `/mala-pata-gaps` (completitud del dominio), `/mala-pata-roadmap-radar` (estado contra git). xray is about the per-unit HOW, surfaced before execution.
