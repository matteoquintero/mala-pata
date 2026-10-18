---
name: mala-pata-gaps
description: READ-ONLY completeness auditor for a DOMAIN — given one or several roadmaps of the same domain + the real CODE, it finds what is missing to cover the total objective and classifies each gap by disposition — `open` (attack now), `deferred` (parked behind an explicit gate), or `closed` (already absorbed). Even if all phases are finished, something may be missing. It cross-checks 3 sources — the total objective (roadmaps), the follow-ups already NOTED (Level-2 / deferred / extra proposals not done / TODO-FIXME in code) and the gaps INFERRED from the code (codegraph/serena, anchored to evidence). Each gap comes out with a disposition (open/deferred/closed), tagged [noted] or [inferred], with evidence (file:line or the annotation); deferred gaps name the gate that parks them. It does NOT look only at the .md — it analyzes the code. It does NOT execute phases or touch code — it leaves its report in mala-pata/gaps/<domain>.md (versioned) + an engram pointer, and suggests routing. Different from mala-pata-roadmap-radar (that one is phase status vs git; this one is completeness of the objective). Trigger — "tenemos follow ups", "gaps de <dominio>", "qué falta del dominio <X>", "qué falta para cubrir <objetivo>".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.9.3"
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
- **Disposition `open` / `deferred` / `closed`** per gap — the axis is the GATE, NOT whether it is "actionable" (everything is, eventually). `open` = in the active backlog, nothing stops it. `deferred` = parked on purpose behind an explicit external gate or decision (an ADR, a roadmap gate-phase it depends on, a `¿Diferible?` marker, a `estado: follow-up` / `bloqueado_por` frontmatter) — it carries `Blocked by: <gate>`. `closed` = already absorbed by other work. A gap is `deferred` ONLY with evidence of the parking decision; without it → `open`; if the disposition is genuinely ambiguous it goes to Questions, never guessed. A `deferred` gap is a follow-up that is not ready to route.
- **Release blocking `Must` / `Should` / `Could`** per gap — a SEPARATE axis from disposition and from severity; it answers *can we ship without this?* (go-live), decided by the **workaround test** (MoSCoW, Clegg/DSDM): a gap is `Must` ONLY if without it the release fails its DoD/core job OR causes harm with **no workaround** (data loss, wrong money, security/legal, a user-facing path broken with no manual mitigation). If ANY workaround or manual mitigation exists → `Should` (real pain, ships) or `Could` (cosmetic), never `Must`. Every `Must` names WHY no workaround exists; every `Should` names the workaround. The question is asked of EVERY gap but the answer is trivial off `open`: a `deferred` gap is `out of this release` (scoped out) EXCEPT the red flag `✗ Must-but-deferred` (a blocker was parked → the release is NOT actually viable — surface it); a `closed` gap is N/A. Keep `Must` ≤ ~60% or it is scope creep (MoSCoW guardrail).
- **Severity (`▲●▼`) is harm, NOT blocking** — `▲●▼` = how much harm IF it happens; blocking = whether we can ship without it. A high-severity gap WITH a workaround does NOT block. They are different axes; do not conflate them.
- **Read-only on the code/project.** It does NOT execute phases, does NOT touch code, does NOT create a kickoff/roadmap. But it DOES leave its **own report** in `mala-pata/gaps/<domain>.md` + an engram pointer (like research/roadmap) — for traceability. It suggests routing and ends.
- **Over-discover, the human trims.** Better to propose one gap too many (marked `[inferred]`) than to stay silent. But never invented.

## Phase 0 — Resolve the domain and its roadmaps

1. Project root: `git -C <cwd> rev-parse --show-toplevel`.
2. Resolve the domain's roadmaps:
   - If the input is a **list of slugs** → those `.md` files in `mala-pata/roadmap/`.
   - If it is a **domain/keyword** → list `mala-pata/roadmap/*.md` and keep those that belong to that domain (by slug/objective). If there is ambiguity about which ones are included, list them and ask for confirmation (one question).
3. If no roadmaps match → say so and STOP; do not invent the objective.

## Phase 1 — TOTAL objective of the domain

Merge the **desired state** of all the domain's roadmaps: their "## Large objective" + the axes of the **coverage table** — read each roadmap's `## Objective coverage` section (MECE desired state). That set of axes is the **completeness contract** you will measure against. If two roadmaps overlap on an axis, it is a single one (MECE).

## Phase 2 — The 3 sources of gaps

**(a) Follow-ups already NOTED** (collect them, do not invent them):
- **Level 2** checklist of each roadmap — read its `## Level 2 — broad domain not covered` section.
- Axes marked **deferred** or **extra-proposal** (status column of `## Objective coverage`) that were NOT done.
- `TODO` / `FIXME` / notes in the domain's **code** (grep/codegraph).
- **Capture the GATE when a source parks an item** — an ADR/decision, a roadmap gate-phase it depends on, a `¿Diferible?`=yes marker, a `estado: follow-up` / `bloqueado_por` frontmatter. The gate drives the `deferred` disposition and the `Blocked by` field. No explicit parking evidence → the gap is `open`.

**(b) Current state of the CODE** (measure, do not assume): for each axis of the objective (Phase 1), what is already implemented and what is not — with `codegraph_explore` / serena / grep. Anchor to `file:line`.

**(c) INFERRED gaps**: where the objective implies something the code does NOT do. E.g.: "the objective says that EVERY invoice error type must be actionable, but in code these 2 types have no action handler (`file:line`)". Reasoned from objective + code, never from nothing.

## Phase 3 — Gap analysis (desired state vs current state)

Same framework as the Gap Analysis of `/mala-pata-roadmap` (Step 4-ter), but **post-hoc and against the live code**: **desired state** (total objective, Phase 1) **minus** **current state** (code, Phase 2b) = **the gaps**. Add the noted (2a) and the inferred (2c). Deduplicate.

## Phase 4 — Output (fixed format, read-only)

Banner (plain text, fenced):

```
Domain gaps: <domain>  ·  roadmaps: <slug, slug, …>  ·  repo: <name>  ·  <date-time>
Source: mala-pata/ roadmaps + live code
```

**Release line** (plain text, the HEADLINE — immediately below the banner, before the Bottom line — this is the go/no-go answer the human reads first):

`Release: <GO | NO-GO | GO-with-conditions> · <b> Must (blockers) · <s> Should · <cc> Could · <x> deferred-but-Must`

NO-GO iff there is ≥1 `Must` OR ≥1 `deferred-but-Must`; GO-with-conditions iff no `Must` but ≥1 `Should`; GO iff neither. (go/no-go release readiness.)

**BLUF line** (plain text, immediately below the Release line — carries the word next to each number):

`Bottom line: <n> gaps · <o> open · <d> deferred · <c> closed · across <m>/<M> axes covered`

**Coverage table** (MECE — a REAL Markdown table, NEVER fenced; one row per objective axis of the domain, each appears EXACTLY once — this is the anti "all good" proof):

| Objective axis | Verified | Gaps found | Status |
|---|---|---|---|
| <axis> | <what proves it covered, or what is missing> | <count> | ✓ covered · ◐ partial · ✗ gap |

`MECE check: axes total: <M> · axes in table: <M> · overlaps: none · gaps: <n> (= Open <o> + Deferred <d> + Closed <c>) · mapping: axis-mapped <x> + off-axis <y> = <n>`

**Reconcile or STOP**: the `<n>` here MUST equal the `<n>` in the `Bottom line` AND the total rows across the three findings tables; and `axis-mapped + off-axis` MUST equal `<n>`. If any of these do not balance, a gap is counted but not listed (or listed but not counted) — **STOP and fix before emitting**. This is the guard that makes a dropped finding impossible (a per-axis coverage count alone does NOT catch it).

**Findings — split by disposition** (REAL Markdown tables, NEVER fenced; each ordered by `Severity`). Every gap lands in EXACTLY ONE of the three. This split IS the point of the skill — do not collapse it back into one list. Emit EXACTLY these tables (reason first, render the tables last); never prose/paragraphs, never vertical `Field:/Value:` blocks; one line per cell (long detail like `file:line` or the gate stays in its own column, never a multi-sentence cell).

> **Off-axis gaps are first-class.** A finding that maps to NO objective axis (a failure mode no roadmap planned — duplicate send, out-of-order, lost-without-trace) is legitimate: put `off-axis` in its `Objective axis` column, never drop it and never force it into a wrong axis. These are the point of failure-mode hunting, not a coverage defect — they are exactly the gaps the per-axis coverage table cannot see. Every finding row is either `axis-mapped` (names a real axis) or `off-axis`; the two counts sum to the total gaps (see the MECE check).

**Open gaps — attack now** (nothing parks them):

| # | Missing (what) | Objective axis | Blocking | Severity | Evidence | Tag |
|---|---|---|---|---|---|---|
| 1 | <what is missing, concrete> | <axis> | Must · Should · Could | ▲ high · ● medium · ▼ low | <file:line or annotation/roadmap> | [noted] · [inferred] |

- A `Must` row names WHY no workaround exists; a `Should` row names the workaround (in the Missing/Evidence text). Sort by `Blocking` first (Must → Should → Could), then by `Severity`.

**Deferred gaps — gated** (parked behind an explicit gate; NOT routed until it opens):

| # | Missing (what) | Objective axis | Blocking | Severity | Blocked by (gate) | Evidence | Tag |
|---|---|---|---|---|---|---|---|
| 1 | <what is missing, concrete> | <axis> | out of this release · ✗ Must-but-deferred | ▲ high · ● medium · ▼ low | <the gate: ADR / external like SPP / gate-phase> | <file:line or annotation> | [noted] · [inferred] |

- Default `Blocking` for a deferred gap is `out of this release` (it was scoped out). Use `✗ Must-but-deferred` ONLY when a real blocker was parked — that is a contradiction (the release is not actually viable) and it forces NO-GO on the Release line.

**Closed since last run — absorbed** (was a gap in a previous report, now covered — omit if this is the first run or nothing closed):

| # | Was missing | Now | Evidence |
|---|---|---|---|
| 1 | <the prior gap> | covered / already done | <file:line proving it> |

Then the closing lines (plain text):

`Questions (not gaps, evidence was missing to confirm them): <or "none">`
`Routing suggestion (I do NOT execute): only OPEN gaps route — <open gap> → /mala-pata-research or /mala-pata-triage. Deferred gaps are NOT routed until their gate opens.`
`Structure: gap analysis + MECE / 100% rule + MoSCoW blocking tiers (Clegg/DSDM) + go/no-go release readiness. Workaround-test blocker criterion + deferred-but-Must flag + open/deferred/closed disposition + noted/inferred provenance + 3-source model = house method.`

- **One row per gap**, concrete, with real evidence. No evidence → it does not go in the table (it goes to "Questions").
- **Mandatory tag** `[noted]` or `[inferred]` per row (shared provenance vocabulary).
- **Mandatory `Severity`** per row — `▲ high · ● medium · ▼ low`; sort each findings sub-table by it (highest first) so the backlog is pick-ready for triage.
- **Disposition split is mandatory** — every gap lands in exactly one of Open / Deferred / Closed; never a single merged list and never prose (a finding is a table row). A `deferred` row MUST carry `Blocked by: <gate>`; if nothing parks it, it is `open`. Only `open` gaps are routed.
- **Blocking axis + Release line are mandatory** — every `open` gap carries `Must`/`Should`/`Could` by the workaround test (separate from severity); deferred rows carry `out of this release` or the `✗ Must-but-deferred` red flag; closed is N/A. Emit the `Release: <GO | NO-GO | GO-with-conditions>` headline (NO-GO iff ≥1 `Must` or ≥1 `Must-but-deferred`). A `Must` without a named reason-why-no-workaround is not a `Must`.
- **BLUF + coverage are mandatory** — emit the `Bottom line` count line and the MECE coverage table even when there are zero gaps; the coverage table IS the "which axes verified" proof. The counts MUST reconcile: `gaps` = total findings rows = `axis-mapped + off-axis` (see the MECE check); if they do not balance, STOP and fix.
- If there are no gaps: say so explicitly + **which axes you verified** and why they are covered (like preview's empty-audit — not a bare "all good").
- **Emit this block's structural labels verbatim in English** — section headers, field labels, table/column headers, and enum/option tokens stay English even when the conversation is in the user's language; only the values and content are localized.

## Phase 5 — Persist the report (traceability)

Write the Phase 4 report to **`mala-pata/gaps/<domain>.md`** (inside the repo, versioned; `mkdir -p` if it does not exist; `<domain>` = the keyword, or a composite slug of the analyzed roadmaps). If it already exists, **update** that file — gaps is a **living backlog** of the domain, not an endless append nor a new file per run. Lightweight pointer in engram: `mem_save` topic_key `gaps/<domain>`, one-line content `Gaps in file: <absolute path>` (do not duplicate the content — the file is the source). If engram is not available, the file is the source; warn in one line.

**Branch — DURABLE, never an ephemeral change/worktree branch** (those get deleted in cleanup → the report is stranded): a gaps report for a domain under a feature-in-progress → that **feature base branch**; standalone domain → the integration default (`main`/`development`); ambiguous → ask ONE question `¿En qué rama guardo el reporte de gaps — <feature base> o main?` and wait. **Write only — do NOT commit/push:** write the file; the skill does NOT create a commit (auto-committing diverged local main from the remote and left reports unpushed). Tell the human the path + that durable branch so they add it in their normal PR flow.

After persisting, you close: you suggest routing, **you do not execute phases or touch code**.

## Rules

- **Read-only on the code/project.** It does not execute phases, does not touch code, does not create a kickoff/roadmap. It DOES write its own report in `mala-pata/gaps/<domain>.md` + engram pointer (its artifact, like research/roadmap).
- **Never invent.** Every gap anchored to an annotation or `file:line`. What cannot be anchored goes as a "Pregunta", not as a gap.
- **Does not overstep `mala-pata-roadmap-radar`** (phase status) — this one is completeness of the objective.
- **Fixed format** always.
- **No data**: if there are no roadmaps for the domain or no accessible code, ask for it; do not guess the objective or the gaps.

## What it does NOT do

- Does NOT execute or offer to execute a phase/lane.
- Does NOT create a kickoff, roadmap, research or code.
- Does NOT invent gaps — only noted or inferred-with-evidence.
- Does NOT dispatch `sdd-*` agents.
