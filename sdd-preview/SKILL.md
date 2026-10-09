---
name: sdd-preview
description: >
  Pre-Apply executive summary — a short plain-language walkthrough of what sdd-apply is going to
  do, with a hard human gate that STOPS until approval is obtained. The preview itself reads
  tasks + design and decides its own audit mode (0, 1 or 2 blind reviewers) — it does not depend
  on sdd-tasks requesting it. Trigger: when the orchestrator launches the preview phase between
  `sdd-tasks` and `sdd-apply`.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "3.8.0"
---

# sdd-preview — pre-apply executive summary (hard human gate)

## Requirements (orchestrate, don't reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Required** (no fallback — if missing, STOP and ask for it to be installed, do not start):
  - `gentle-ai` — part of the SDD cycle. Install: `brew install gentleman-programming/tap/gentle-ai`.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded):
  - `engram` — persistent memory and continuity pointer. Fallback: continue without the pointer; the file artifacts are the source. Install: ships with gentle-ai (`brew install gentleman-programming/tap/gentle-ai`).

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP, e.g. serena). If a required one is missing, do not continue.

## Purpose

Produce a **short executive summary** of what `sdd-apply` is going to do, in plain language ("in plain words"), so the human can read it in ≤30 seconds and decide whether the plan still stands or has gone off track.

This phase sits between `sdd-tasks` (approved plan) and `sdd-apply` (code). It does **NOT** write code, migrations, or project files. Its output is a short artifact and a **HARD human gate** that cannot be passed with a blind "yes".

**Primary goal**: a summary for making a quick decision.
**Secondary goal (conditional, self-decided)**: adversarial audit with 0, 1 or 2 reviewers — the number is decided by the preview itself (see Self-assessment), not by `sdd-tasks`.

## What You Receive

From the orchestrator:
- Change name
- Artifact store mode (`engram | openspec | hybrid | none`)
- Absolute path of the worktree to inspect
- Kickoff profile (FULL/STANDARD/LITE/MINIMAL) — determines the summary's word target

The **audit mode and the number of reviewers (0/1/2) do NOT come from the orchestrator or from `sdd-tasks`** — the preview itself sets them in the Self-assessment step, before writing the summary.

## Execution and Persistence Contract

> Follow **Section A** (skill loading), **Section B** (retrieval), and **Section C** (persistence) from `skills/_shared/sdd-phase-common.md`.

Required reads (parallel + `mem_get_observation` — previews are truncated):
- `sdd/{change-name}/tasks` (required)
- `sdd/{change-name}/design` (required) — OR the merged `sdd/{change-name}/spec-design` written by the LITE/MINIMAL profiles (accept EITHER separate `spec` + `design` OR the merged `spec-design`)
- `sdd/{change-name}/kickoff` (required — to read the DoD). The kickoff arrives from the orchestrator as an **absolute path**: `Read` that file and copy the DoD verbatim. If only the engram topic is available, it holds just the pointer `Kickoff in file: <path>` — follow that path and `Read` the file; never paraphrase the DoD from the pointer.
- `sdd/{change-name}/spec` (when not merged into `spec-design`), `sdd/{change-name}/proposal`, `sdd/{change-name}/explore` (context)

Also read the **real worktree code** (Grep/Glob/Read) — do not review in the abstract.

## Self-assessment — how many reviewers (0, 1 or 2)

Before writing the summary, with `tasks` + `design` (+ real code) already read, the preview itself decides the audit mode. This replaces the signal that used to come from `sdd-tasks` — `sdd-tasks` no longer sends it.

**Base rule (taken from gentle-ai's native risk model, `internal/reviewtransaction/risk.go`): volume NEVER decides the number.** Not the number of tasks, nor of files, nor of estimated lines — "a 5-line change in authentication weighs more than a mechanical 5000-line rename" (quote from gentle-ai's own code comment). The "Review Workload Forecast" that `tasks` still computes (400-line budget) is for something ELSE — deciding whether it is worth splitting into chained PRs — and **is not a risk signal here**. Only concrete evidence escalates, just as in gentle-ai: it is built from the categories your own audit ALREADY produces (Blast-radius, Reuse-first, Architecture smells), reading the tasks/design plan against the real code.

**0 reviewers (summary only, no audit)** — ALL of these conditions:
- Blast-radius: no touched file falls under the high-risk signals below.
- Reuse-first: everything is **REUSES** or **ADAPTS** from an exact existing precedent — nothing remains as structurally **NEW**.
- Architecture smells: none.
- Does not touch configuration files (`.env`, `package.json`/lockfiles, `go.mod`, `Dockerfile`, `Makefile`, or extension `.json`/`.yaml`/`.yml`/`.toml`/`.ini`).

**1 reviewer** — the default case when neither 0 nor 2 applies: there is something **NEW** in Reuse-first or a moderate new surface, but none of the high-risk signals below.

**2 reviewers (double blind + synthesis)** — ANY of these concrete signals in the Blast-radius or in the real code that will be touched (same categories gentle-ai uses for its "high" tier):
- Path/symbol with `auth`, `security`, `payments`, `webhook`, or handling of tokens/credentials/secrets.
- Executable-bit change (a file becomes or stops being executable), shell scripts (`.sh`/`.bash`/`.zsh`), or CI workflows (`.github/workflows/*.yml`).
- Data migration/DDL, or any personal/sensitive data.
- Reuse-first marks a pattern/architecture as **NEW** with no 1:1 precedent in the repo (not just one more component of the same kind — a genuinely new pattern).
- Architecture smells with **high** severity.
- `design` left open decisions not fully resolved with the human.

**Money / invariants lens (domain trigger).** If the blast-radius touches money calculation, totals, taxes (VAT), discounts, warranty, stock, or any mapper/DTO/projection that transforms values → **it is never 0 reviewers** (minimum 1), and the reviewer(s) explicitly adopt the **Correctness / invariants** lens (see audit). If there is also another high-risk signal (migration, NEW pattern, etc.) → 2, and there **the lenses are split**: one money/invariants, the other concurrency/migrations.

Make explicit in the artifact (a short line, not a separate section) the chosen number and **the concrete signal** that motivated it — never "audit active" without saying which evidence triggered it.

Persistence:
- **engram**: `sdd/{change-name}/preview` (type: `architecture`).
- **openspec / hybrid**: `preview.md` in the change folder.
- **none**: return inline; do not write files.

## Output — Executive summary (ALWAYS)

A markdown artifact with exactly **4 mandatory sections**, none empty:

```markdown
# Preview: <change-name>

**Profile**: <FULL/STANDARD/LITE/MINIMAL> · **Audit mode**: <active/inactive>

## What I'll do
- <concrete action 1 — verb + what>
- <action 2>
- <action 3>
(3-5 bullets, each actionable)

## Affects
- <files/modules/services impacted, 1-3 lines>
- <what is NOT touched, if the scope has important boundaries>

## DoD (from the kickoff)
<verbatim copy of the kickoff's "Definition of Done" — do NOT reinvent criteria>

## Risks
- <things that can go wrong, things to watch closely — 1-3 lines>
```

**Emit every section header, field label, enum/option token and table header VERBATIM in English** — `Preview`, `Profile`, `Audit mode`, `What I'll do`, `Affects`, `DoD (from the kickoff)`, `Risks`, `Findings & disposition`, `Finding` / `Severity` / `Disposition`, the severities `high`/`medium`/`low`, the dispositions `IGNORE`/`REFACTOR`/`ADJUST`/`REUSE`, and the gate options `Approve` / `Adjust` / `Stop` — **even when the conversation is in the user's language**. Only the bullet CONTENT and the VALUES follow the user's language; the labels are structural and are never localized.

### Word target per profile

| Profile | Summary target |
|---|---|
| MINIMAL | ≤100 words |
| LITE | ≤150 words |
| STANDARD | ≤250 words |
| FULL | ≤400 words |

Indicative target, not a hard cap. If you need more to be honest, say so.

### Summary rules

- **Zero unnecessary jargon**: a non-author human must understand what is going to happen.
- **No empty summary**: if "What I'll do" has only 1 bullet, something is wrong — either the change is too small to go through preview, or the plan is not ready.
- **The DoD is a verbatim copy of the kickoff**, not a reinvention — the preview NEVER rewrites or "improves" criteria on its own, and by default **does not audit the DoD**. You only raise a criterion as a finding if it is a **hard testability blocker** (a criterion that literally CANNOT be verified as written — not "could be better", not "became a bit outdated"). That high threshold is deliberate: catching improvable criteria on every pass is what produced the endless loop back to design/tasks. If there really is a blocker and the human chooses "Adjust", it is the cheap route (edit the kickoff's DoD + return to the gate, see the Adjust option), NOT plan regeneration.
- **"Affects" is concrete**: names of files/modules, not generic ones ("several files" is forbidden).

## Output — Audit mode (when the self-assessment decides ≥1 reviewer)

When the self-assessment above decides ≥1 reviewer, this block is added after the summary:

```markdown
## Adversarial audit

### Findings & disposition (the table the human scans to decide — ALWAYS a table, never a flat list)
| # | Finding | Severity | Disposition |
|---|---------|----------|-------------|
| 1 | <concrete finding, anchored to `file:line` or task ref> | ▲ high | ADJUST: <what to change> |
| 2 | <finding> | ● medium | REFACTOR: <scoped> |
| 3 | <finding> | ▼ low | IGNORE: <why it is fine> |

### Blast-radius
| File | Action | ~LOC | Public symbol |
|---|---|---|---|
| <path> | NEW/MODIFIED/DELETED | <n> | <symbol> |

### Reuse-first (REUSES / ADAPTS / NEW)
- <new piece 1>: **REUSES** `<file:line>` — <existing helper that applies>
- <piece 2>: **ADAPTS** `<file:line>` — <minimal difference>
- <piece 3>: **NEW** — <why no equivalent exists>

### Architecture smells
- **▲ high / medium / · low**: <description> — `<file:line>` or `<task ref>`

### Silent assumptions
- <default that Apply would bake in if nobody looks>

### Correctness / invariants (money lens — adopt when the domain triggers it)
Perspectives to adopt, NOT a checklist to tick off — read the plan against the real code looking for:
- **Lossy projection/mapper**: does any `SELECT`/recalc/DTO/mapper return a subset and drop a field that a downstream consumer needs? (money, tax, stock, permission lost in the transformation)
- **Test that proves the read, not the result**: is there a "green" criterion that only ensures the shape/SELECT and not the end-to-end calculation? → false coverage.
- **Hardcoded value at an edge**: a fixed `0.00`, a silent default, a constant where the real value should go.
- **Application level**: tax/discount/warranty at document level vs line-item level — does it match the business rule?
- **Consistency under concurrency**: locks without a fixed order (deadlock), reads without the guard that the invariant requires.
```

**Audit rules**:
- The number of reviewers (1 or 2) was already fixed in the Self-assessment. The orchestrator only does the fan-out according to that number.
- Reviewers are **adversarial**: default to suspecting duplication/over-engineering; the plan has to prove novelty.
- **Empty audit forbidden**: if there are no findings, state EXPLICITLY WHAT was looked for and why each thing was discarded.
- **Findings & disposition is ALWAYS a table** (`# | Finding | Severity | Disposition`), never a flat numbered list — it is what the human scans to decide. Severity uses the glyph + word `▲ high` · `● medium` · `▼ low`; Disposition is one enum + a one-line reason: `IGNORE` · `REFACTOR` · `ADJUST` · `REUSE` (objective-level findings do NOT go in this table — they escape backward, see below). The Blast-radius / Reuse-first / Architecture smells / Silent assumptions are the supporting analysis that feeds this table.
- Reviewers do NOT see each other's output. Synthesis (merge + dedup) is done afterwards.
- The **Correctness / invariants** category is MANDATORY when the self-assessment flagged the money/invariants trigger; if it is active and you find nothing, state which invariants you verified and why they are safe (same rule as empty-audit). It is a lens to adopt, not a checklist that replaces free adversarial reading.

## A SINGLE PASS is the goal (ANTI-LOOP)

Preview is designed to run **ONCE** and be complete enough for the human to decide in that single pass. Do the audit thoroughly the first time — do not leave anything "to look at in a second round", because there is no second round as the norm. The summary + audit + gate come out complete in one go.

"Adjust" is a **rare escape**, not an expected round-trip. If the human chooses it:
- The orchestrator makes ONLY the specific change requested (edit the kickoff's DoD, or the specific plan fix if it was a real plan defect).
- **On return, preview is NOT re-run**: no new summary, no new audit, no hunting for fresh findings. A **short delta** is shown ("you asked for X → Y was done") and it goes **STRAIGHT to the gate**. This is the rule that makes the loop impossible: returning from an adjustment never generates new findings, because nothing is re-audited.
- That re-gate offers only: **Approve** (with the delta in view) or **Stop**. It does NOT offer "Adjust" again — if the delta was not enough, it is Stop and rethink outside the cycle, not another regeneration round.

Hard backstop: **there is never a third preview interaction** for the same change. Pass 1 (complete) → at most one delta re-gate → apply or stop. A change cannot end up bouncing between preview and design/tasks.

## Objective-level vs plan-level finding (classify before disposing)

Preview reviews **the plan**, not **the objective** — the WHAT must already have been closed in explore/propose/spec (see `mala-pata-loop-start`, Hard rule #4). So, before putting any finding in the disposition table, classify its **level**:

- **Plan-level** (duplication, over-engineering, hardcoded flow, wrong layer, ignored reuse, badly thought-out task) → this is what preview DOES dispose of: REUSE / REFACTOR / IGNORE, or it goes through "Adjust" if it needs a specific plan fix. Normal path.
- **Objective-level** (the finding is not "the plan is wrong" but "the plan solves the wrong objective / the objective is not defined / half the scope is missing / the DoD is not testable and it is not a simple reword") → **do NOT dispose of it** (it is not REUSE/REFACTOR/IGNORE) and **do NOT send it through "Adjust"** (Adjust is for the plan or for a DoD reword, never for redefining the WHAT). An objective defect that reaches this point means it slipped through the origin gate. The correct disposition is to **stop and send it back**:
  - The gate offers **Stop** with explicit reason `objective-not-ready → explore/propose`.
  - The orchestrator marks `sdd/<change>/state = "objective-not-ready-at-preview"` (with the absolute path of the live worktree, just like the normal pause) and the cycle goes back to **explore or propose** to redefine the WHAT.
  - The plan is NOT re-audited, the preview is NOT re-gated. It is an **escape backwards**, not a round-trip: it does not violate "single pass" (the preview ends here; what follows is planning from further back, not another preview round).

Golden rule: **if you find yourself debating with the human whether the objective is right, that debate does NOT belong in preview.** Cut it off and send it back to explore/propose. Preview assumes a defined objective; its job starts where the objective ends.

## The GATE — HARD, always runs, always stops

The gate **ALWAYS** runs, whether or not the audit is active. It is **immune to any "auto" mode** of the rest of the SDD — this phase STOPS regardless. The artifact MUST include the gate payload ready for the interactive question function available in the CLI.

### Gate options (3 in the single pass; if there was an "Adjust", the delta re-gate brings only 2: Approve / Stop — see ANTI-LOOP)

**Approve (requires comprehension autotest)**
- The human writes in 1 line what they understood is going to be done.
- Without that line, it is not approved. **Micro-forcing-function** against rubber-stamping.
- If the answer does not reasonably match the summary's "What I'll do", the orchestrator asks for a re-read and rephrasing.
- On approval → `next_recommended: sdd-apply`.

**Adjust first (free textarea)** — *rare escape; on return it is a delta re-gate (Approve/Stop), NOT another preview pass (see ANTI-LOOP).*
- The human writes feedback: what to change, what is missing, what is wrong.
- **Route depending on the TYPE of adjustment — NOT every adjustment regenerates the plan** (this is what avoids the loop):
  - **Stale DoD / untestable or obsolete criterion** → the orchestrator edits ONLY the Definition of Done section of the kickoff file and **returns STRAIGHT to the preview gate**. It does NOT re-run design/tasks — a criterion adjustment is not a plan defect.
  - **Real plan defect** (duplication, bad architecture, hardcoded flow, badly thought-out task) → then yes, it goes back to `sdd-tasks` or `sdd-design` according to the feedback.
  - **Objective defect** (the WHAT is wrong/incomplete, not the plan or the DoD wording) → it is NOT "Adjust": it is **Stop with reason `objective-not-ready`** and back to explore/propose (see "Objective-level vs plan-level finding"). Adjust never redefines the objective.
  - When in doubt between DoD and plan, it is DoD/gate (cheap path), not regeneration.
- State in engram: `sdd/<change>/state = "adjustment-requested-at-preview"` with the feedback + the type of route taken.

**Stop (resumable pause, Option A)**
- Marks `sdd/<change>/state = "paused-at-preview"` in engram, with an optional reason from the human, **and the absolute path of the worktree that stays LIVE** — a paused SDD is the #1 candidate for leaking orphan worktrees; recording it is what lets the radar list it for future cleanup.
- It does **NOT delete** previous artifacts (explore/proposal/spec/design/tasks stay in engram).
- **Resumable with `/mala-pata-loop-start <kickoff-path>`** — on resume, loop-start detects the `paused-at-preview` and jumps straight to this same gate (do NOT use `/sdd-continue`: it belongs to gentle-ai and does not know the preview phase — it routes above the gate).
- State recorded for future memory (if it comes back in 2 weeks it knows why it stopped).
- **Objective-not-ready variant**: if the reason for stopping is an **objective-level** defect (see the classification section), the state is `sdd/<change>/state = "objective-not-ready-at-preview"` instead of `paused-at-preview`, and the resume is NOT at the preview gate but at **explore/propose** (the WHAT has to be redefined first). The rest is the same: live worktree recorded, previous artifacts intact.

### Gate rules

- The orchestrator is the one that runs the interactive question function available in the CLI — the reviewer sub-agent is NOT.
- There is no global "OK" that sweeps through without reading. The only way to say yes is to write the autotest line.
- The gate is included in the artifact as `gate_payload` — the orchestrator reads it and fires it.

## Double reviewer (only when the self-assessment decided 2)

When the Self-assessment decided 2 reviewers:
- Reviewers run **in parallel, blind** to each other.
- Each one produces its set of adversarial findings (audit).
- A separate run in `synthesis` mode merges/dedups the findings and produces the single artifact.
- The orchestrator does the fan-out — the reviewer sub-agent does NOT call other agents.

## What to Do — Role: `reviewer`

1. Read artifacts and real worktree code.
2. Run the **Self-assessment** and fix the number of reviewers (0/1/2).
3. Produce the **summary** (4 mandatory sections, respecting the profile target).
4. If the self-assessment decided ≥1: produce the audit block.
5. Prepare the `gate_payload` with the 3 fixed options.
6. Return to the orchestrator — do NOT persist unless you are `synthesis`.

## What to Do — Role: `synthesis` (only when there are 2 reviewers)

1. Receive the 2 reviews.
2. Merge + dedup the audit (keep the highest severity if they overlap; flag findings that only one saw).
3. Assemble the single artifact (summary + audit + gate).
4. Persist to `sdd/{change-name}/preview` (Section C).

## Rules

- **NEVER** write code, migrations, or project files.
- **NEVER** launch sub-agents from the reviewer.
- **Empty summary forbidden**: the 4 sections have concrete content or there is no preview.
- **Empty audit forbidden** (when active): state what was looked for and discarded.
- **The gate cannot be passed without the autotest** (1 written line).
- **The gate stops even if the rest of the SDD is in auto mode** — this phase is interactive by design.
- Size budget of the **summary** per profile (see table). Audit has no cap.
- Return envelope per **Section D** from `skills/_shared/sdd-phase-common.md`; `next_recommended: sdd-apply` **only** after gate approval.
- **Record the dispositions in the persisted artifact** (`sdd/<change>/preview`): for each finding, its final disposition (REUSE / REFACTOR / IGNORE / accepted-as-gap). The goal is ONE pass: if there was an "Adjust", also record the requested delta and that the close was via a delta re-gate, not another audit pass (ANTI-LOOP section).
