---
name: mala-pata-atlas
cognitive_tier: standard
description: >
  READ-ONLY QA-coverage planner for a WHOLE large feature — maps the complete
  testable surface (every functionality AND every DB table, anchored to the real
  code), enumerates the cases systematically (equivalence partitions, boundary
  values, state transitions, error paths, pairwise), builds a MECE coverage
  matrix, and decomposes it into a RISK-ORDERED roadmap of walkthrough-units, by
  phases, so nothing is lost no matter how long the QA takes. It PLANS coverage
  and emits the units; it does NOT write the per-unit scenarios (that is
  `/mala-pata-walkthrough`), does NOT seed, does NOT run a browser, does NOT
  touch code. The one thing it writes is the atlas `.md`. Each unit it emits
  rides the existing pipeline — `/mala-pata-walkthrough` → `/mala-pata-seed` →
  `/mala-pata-walkthrough-start`.
  Trigger — "armá el atlas de pruebas de <feature>", "cobertura total de QA de
  <feature>", "quiero probar todos los casos y todas las tablas de <feature>",
  "un roadmap de walkthroughs para <feature>", "mapeá todo lo testeable de
  <feature>".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "0.2.1"
---

# /mala-pata-atlas — map the complete testable surface of a feature, before any walkthrough is written

Input: **the one delivered by the CLI** — a **feature name / domain**, or a **roadmap slug/path** whose phases make up the feature.

Your job: take a LARGE feature and **draw its atlas** — a complete map of what must be tested — by inventorying its whole testable surface (every functionality AND every DB table), enumerating the cases that surface demands, pinning them to a **coverage matrix**, and cutting that matrix into a **risk-ordered roadmap of walkthrough-units** so a big QA effort proceeds by phases and **nothing falls through the cracks**. It is to the walkthrough pipeline what `/mala-pata-roadmap` is to the lanes: the planning altitude above it.

> **It plans coverage; it does not author scenarios.** It decides WHICH units exist, WHAT each must cover (functionalities + tables + case classes) and IN WHAT ORDER. It does NOT write the per-unit Given/When/Then core or the QA/customer lanes — that is `/mala-pata-walkthrough`. It does NOT seed (`/mala-pata-seed`), does NOT run a browser (`/mala-pata-walkthrough-start`), does NOT run a lane, does NOT create worktrees, does NOT write code. The only thing it ever writes is the atlas `.md`.
> **It fills the leak between "big feature" and "QA that loses the thread."** A per-unit walkthrough derives scenarios from one PR/phase's artifacts — great per unit, blind to the whole. A big feature's QA needs a surface inventory (including the data layer) + a systematic case universe + a phased plan, or whole functionalities and tables never get tested and no one notices. This pass makes that surface and that plan explicit.
> **The DB-table axis is first-class.** The feature's tables, their CRUD operations and their state columns/enums are a coverage dimension in their own right — not a side effect of exercising the UI. A table no walkthrough touches is an uncovered table, surfaced here.

## Requirements (orchestrate, do not reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP): `git` — resolve the repo root (`git rev-parse --show-toplevel`) to anchor the inventory and place the atlas.
- **Recommended** (with fallback — warn in one line and continue degraded):
  - `codegraph` / `serena` — inventory the real functionalities, modules, endpoints and the data layer (models/migrations/tables) at symbol level. Fallback: grep/Read over the repo.
  - `WebSearch/WebFetch` — the domain's canonical test checklist (what mature teams always test for this kind of feature). Fallback: disclose there is no external checklist; rely on the code inventory only.
  - `engram` — continuity pointer. Fallback: the atlas `.md` is the source of truth.

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP, e.g. serena). If the mandatory tool is missing, do not continue.

## Phase 0 — Authorize (read-only guard)

Drawing an atlas is **read-only on the project's code** — it inspects, maps and plans. The only write it may do is the atlas `.md` (Step 6), and only after the human approves it at the gate. If the request is to explain/compare rather than to plan the coverage of a feature, stay read-only and answer directly; do not write an atlas.

## Step 1 — Resolve the feature + scope

Detect the input and fix the boundary of "the feature":

- **A feature name / domain** → resolve the modules, screens, endpoints and tables it spans, anchored to the code (codegraph/serena).
- **A roadmap slug/path** → `<repo-root>/mala-pata/roadmap/<slug>.md` → the feature is the union of its phases (read each phase's IN/OUT to bound the surface).

State the scope boundary explicitly (what is IN this atlas, what is OUT). If the feature cannot be bounded with confidence — the name is too vague to know what it covers — **STOP** and ask ONE question to fix the boundary; do not invent a surface.

## Step 2 — Inventory the testable surface (two axes, anchored to the code)

Map the WHOLE surface, in two axes, reuse-first (anchor to what the code really has — never invent a functionality or a table):

- **Functionalities** — every user-observable behavior of the feature: screens, endpoints, commands, flows. One entry per observable behavior, not per internal function.
- **DB tables** — every table/model the feature touches, and for each: its **CRUD operations** in scope and its **state columns / enums** (the lifecycle values a row moves through). This is the axis nothing else in the family inventories.

If an axis cannot be read from the code (a behavior with no unique marker, a table with no model), say so and estimate — never drop it silently from the map.

## Step 3 — Enumerate the cases (systematic, by test-design technique)

For each functionality and each table, derive the case universe with named techniques — not an ad-hoc list:

- **Equivalence partitioning + boundary values** — valid/invalid input classes and their edges.
- **State-transition** — for anything with a lifecycle (the state columns/enums from Step 2): the legal transitions, the illegal ones that must be rejected, and the terminal states.
- **Error / negative paths** — what must fail, and fail cleanly (permissions, missing prerequisites, conflicts).
- **Pairwise / combinatorial** — when inputs combine, cover the pairs instead of the full cross-product.
- **Per table: a CRUD + integrity pass** — create/read/update/delete coverage and the referential-integrity paths (what a delete cascades or blocks).

The output of this step is the raw case universe; it does not yet decide which walkthrough owns each case.

## Step 4 — Coverage matrix (MECE + traceability)

Collapse the case universe into a **coverage matrix** — the contract the roadmap is measured against:

- Each **functionality** and each **table** appears as a row, with its case classes, and maps to the walkthrough-unit(s) that will cover it.
- **MECE + 100% rule**: every functionality and every table is either **covered** by a unit or **explicitly deferred / out-of-scope** — named, with a reason, **never a silent drop**. A surface axis missing from the matrix is a gate failure.
- This is the "nothing gets lost" check: it is what guarantees the big feature's whole surface is accounted for before any walkthrough is written.

## Step 5 — Decompose into a roadmap of walkthrough-units (risk-ordered, phased)

Cut the matrix into **walkthrough-units** — each a coherent, runnable slice of the feature (by sub-flow, or by a cluster of related tables), sized so `/mala-pata-walkthrough` can author it as one walkthrough:

- **Order by risk** (risk-based testing): the units touching money, irreversible writes, data integrity or the most-used paths go first. The phase order is the risk order.
- **Declare dependencies** — a unit that needs state another produces (seed/data prerequisites) depends on it; the graph is a DAG, no cycles.
- **Flag delicacy per unit** — a hint (`low` / `medium` / `high`) that `/mala-pata-walkthrough` carries into the QA frontmatter's `smoke_delicacy`; on any doubt round UP.
- **Phases** — group the units into phases so a long QA proceeds in waves. "No matter how long it takes, by phases" lives here.
- **Over-plan; the human trims.** Propose the full coverage; the human removes or defers at the gate (same discipline as `/mala-pata-roadmap`).

## Step 6 — Human gate + write the atlas

**Gate first.** Present the coverage matrix + the walkthrough roadmap and **wait for OK or adjustments** before writing. Do not write an atlas the human has not signed off.

On approval, write `<repo-root>/mala-pata/atlas/<slug>.md` (`mkdir -p` the folder), starting with YAML frontmatter: `feature: <slug>`, `domain: <X>`, `roadmap: <slug | none>`, `created_at: <ISO 8601>`, `coverage: <planned | partial>`. Fill `created_at` from the machine's clock — run `date '+%Y-%m-%dT%H:%M:%S%z'` and use its exact output; never invent the time, never default to UTC.

> **Canonical `domain` rule — single source of truth.** Apply `_shared/mala-pata-domain-rule.md` verbatim, INCLUDING its mandatory confirmation gate (list existing domains → propose → the human confirms, every time); it supersedes any restatement here. Do not paraphrase or re-derive it. **NEVER blank — ALWAYS confirmed by the human via its confirmation gate before writing.**

**Branch — DURABLE, never an ephemeral change/worktree branch** (those get deleted in cleanup → the atlas is stranded): a feature-in-progress → that feature base branch; standalone → the integration default (`main`/`development`); ambiguous → ask ONE question and wait. **Write only — do NOT commit/push:** write the file; the skill does NOT create a commit. Tell the human the path + the durable branch so they add it in their normal flow. Leave a one-line engram pointer `atlas/<slug>` (fallback: the `.md` is the source).

## Step 7 — Close (MANDATORY: BLUF + tables)

**BLUF first** — one `Result:` line above the tables: `Result: ✓ atlas · <f> functionalities · <t> tables · <u> walkthroughs · <p> phases` (or `◐ partial: <reason>`).

Then the **coverage matrix** — one surface axis per row:

| Axis | Kind | Case classes | Covered by | Status |
|---|---|---|---|---|
| `<functionality 1>` | functionality | equivalence · boundary · error | WT-1, WT-3 | covered |
| `<table 1>` | table | CRUD · state-transition · integrity | WT-2 | covered |
| `<axis 3>` | functionality | — | — | deferred (`<reason / gate>`) |

**MECE check:** `surface axes: N · rows in matrix: N · silent drops: none` — the counts MUST match.

Then the **walkthrough roadmap** — one unit per row, risk-ordered:

| Walkthrough | Scope (functionalities + tables) | Case classes | Risk | Depends on | Delicacy | Phase |
|---|---|---|---|---|---|---|
| `WT-1 <name>` | `<fns + tables it owns>` | equivalence · boundary | high | — | medium | 1 |
| `WT-2 <name>` | `<fns + tables it owns>` | CRUD · state | medium | WT-1 | low | 2 |

- **Ledger (plan coverage, honest):** `covered <u>` · `deferred <d> (named)` · `out-of-scope <o> (named)`. Run-time honesty (by-hand vs by-proxy, `qa_done`) is tracked downstream per walkthrough by `/mala-pata-walkthrough-start` and aggregated by `/mala-pata-domain-radar` — this ledger is the PLAN, not the run.
- **Target:** `mala-pata/atlas/<slug>.md` (repo-relative) — written / not written.
- **Next step** — route each unit through the existing pipeline, in phase order:
  ```
  /mala-pata-walkthrough <WT-slug>   →   /mala-pata-seed <WT-slug>   →   /mala-pata-walkthrough-start <WT-slug>
  ```
- **Structure:** `Requirements Traceability Matrix + ISO/IEC/IEEE 29119 (test design) + Equivalence Partitioning / Boundary Value Analysis / State-Transition / Pairwise (Myers) + Risk-Based Testing + per-table CRUD matrix + BDD / Living Documentation (North / Adzic). Coverage-matrix → risk-ordered roadmap-of-walkthroughs feeding the existing pipeline + the honest coverage ledger = house method.`

**Frozen structural label set** (this block applies `_shared/mala-pata-structural-labels.md` verbatim — emit these EXACTLY, in English, even when the conversation is in another language; only Value/Evidence content and surrounding prose are localized):
`Result:` · matrix headers `Axis | Kind | Case classes | Covered by | Status` · kind tokens `functionality` `table` · status tokens `covered` `deferred` `out-of-scope` · `MECE check:` · roadmap headers `Walkthrough | Scope (functionalities + tables) | Case classes | Risk | Depends on | Delicacy | Phase` · risk tokens `high` `medium` `low` · delicacy tokens `low` `medium` `high` · `Ledger` · `Target:` · `Next step` · `Structure:`. Rows are one-per-axis / one-per-unit. No label is translated, renamed or added.

This block is the only way to close on the happy path. **Only exceptions:** Phase 0 read-only stance; the Step 1 STOP when the feature cannot be bounded; the Step 6 gate question (`domain`/branch) before writing.

## Persistence

The **atlas `.md`** is the artifact — the coverage plan lives there. Optionally leave a one-line engram pointer `atlas/<slug>` for discoverability (fallback: the `.md` is the source). The atlas is forward-only input to the pipeline; it is never the place where run results live.

## What it does NOT do (invariants)

- Does NOT write the per-unit scenarios / QA / customer lanes — that is `/mala-pata-walkthrough`.
- Does NOT seed (`/mala-pata-seed`), does NOT run a browser (`/mala-pata-walkthrough-start`), does NOT run a lane, does NOT create a worktree / write code.
- Does NOT invent a functionality or a table — the surface is anchored to the real code; an unmeasurable axis is flagged, never dropped.
- Does NOT replace `/mala-pata-roadmap` (that plans the BUILD) nor `/mala-pata-gaps` (domain completeness of built work) nor `/mala-pata-roadmap-radar` / `/mala-pata-domain-radar` (status) nor `sdd-verify` (machine verification). It plans the QA COVERAGE of a feature.
- Does NOT commit/push the atlas — write-only; the human commits it.

## Relation to the family

- The **planning altitude above the walkthrough pipeline** — it emits the roadmap-of-walkthroughs that `/mala-pata-walkthrough` already knows how to consume ("a roadmap → N units"), so there is zero rework of the describer, seeder or runner.
- **Reuses** `_shared/mala-pata-domain-rule.md` (the `domain:` field) and `_shared/mala-pata-structural-labels.md` (close labels).
- **Different from** `/mala-pata-roadmap` (plans construction into shippable slices), `/mala-pata-gaps` (what is MISSING to cover the objective), `/mala-pata-walkthrough` (authors one unit's scenarios). atlas is the per-feature QA coverage MAP, drawn before any walkthrough is written.
