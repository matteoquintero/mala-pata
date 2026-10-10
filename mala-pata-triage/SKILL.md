---
name: mala-pata-triage
description: Single front-door of mala-pata. Trigger — any change request, BEFORE touching code. Reads the request, applies the form gate (What + DoD + Decisions), and ANSWERS which lane/skill to run — `/mala-pata-shot`, `/mala-pata-organic`, `/mala-pata-loop` or `/mala-pata-roadmap` — handing the chosen lane the draft of already-inferred fields. It does NOT generate files, does NOT create worktrees, does NOT execute anything: it is a decision skill, not an execution one.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.7.0"
---

# /mala-pata-triage — Entry router (decides, does not execute)

User request: **input delivered by the CLI**

Your only job is to **read the request and decide the lane**, then **answer which skill to run**. You do not generate kickoffs, you do not write files, you do not touch code. You are the gate — the strict format IS the router — separated from the three lanes that consume it.

> **You execute NOTHING.** Do NOT create a worktree, do NOT write a kickoff, do NOT run phases of any cycle.
> The result is ALWAYS one of these: (a) a direct read-only answer, (b) "→ run `/mala-pata-shot`" (trivial, understood change), (c) "→ run `/mala-pata-organic`" with the field draft, (d) "→ run `/mala-pata-loop`", (e) "→ run `/mala-pata-roadmap`", or (f) `vague work ` asking for the minimum.

> **Triage does not dispatch `sdd-*` agents.** It is a pure decision skill — the gentle-ai `PreToolUse:Agent` preflight does not apply here, just as it does not apply to `/mala-pata-organic`.
> **The lanes remain directly invokable** if the human already knows which one it is (`/mala-pata-shot`, `/mala-pata-organic`, `/mala-pata-loop`, `/mala-pata-roadmap`). Triage is the recommended entry when you do NOT know where it goes — not a mandatory step.

## Requirements (orchestrate, do not reinvent)

This skill does not orchestrate hard tools: it only decides the lane. It has no installation requirements.

## Phase 0 — Authorize (read-only guard)

Is the request a **CHANGE**? Investigation, explanation, review, audit or comparison are **read-only** — there is no lane to decide, answer directly from your own knowledge/exploration and done (it is not a mala-pata lane).

Only if there is real intent to change code do you continue to the gate.

Ambiguity about whether it is a change → 1 specific question, you stop and wait.

## Phase 0.5 — Input is a slug/path? Read its research doc (and carry the slug)

If the input arg is a slug or a path that resolves to an existing `mala-pata/research/<slug>.md` (what `/mala-pata-research` hands off), `Read` it and use its Define fields (What / Why / DoD / Decisions / Risk / size_signal) as the draft instead of only the raw request text. Then run the form gate below over that draft.

If the arg is a roadmap phase slug (invoked for a roadmap phase), remember it: it travels in the draft as `change_name` (see Phase 2). When triage is invoked free-standing (plain request text), there is no slug — omit `change_name`.

## Phase 1 — Form gate (quick diagnosis, not an interview)

Evaluate the request against these three fields, as defined by the original design (same table used by `/mala-pata-organic` and which `/mala-pata-loop` references as its compass):

| Field | Blocks | What it tests |
|---|---|---|
| **What** | YES | Objective = observable, concrete behavior/result. "Improve X" with no concrete target → FAILS. |
| **DoD** | YES | Testable definition in Given/When/Then: "Given X, When Y, Then Z". |
| **Decisions already made** | YES | The approach/architecture is DECIDED or obvious. It is THE discriminator for loop. |
| **Why** | NO | Motivation in 1 line — it is asked for, does not block. |
| **Risk** | NO (optional) | Blast radius in one line. |
| **Where** | NEVER a gate | Discovered in the Explore phase of organic/loop-start, not here. |

This is a **diagnosis from the text of the request**, proportional to the request — not a full form. You may ask **just 1 clarifying question** ONLY if without it you cannot decide the lane (real blocking ambiguity). Ask it, stop and wait for the answer.

## Phase 2 — Decide and answer the lane

- **Trivial + understood + minimal blast radius** (obvious What/Done, no decisions, 1-3 files, no migration/contract/new UI) → **shot**.
  Answer: `→ run /mala-pata-shot`. It is ODD with no worktree and no ceremony, for the smallest change. **Boundary with organic**: with ANY uncertainty, decision, or necessary ceremony (design, migration, new UI) → organic, NOT shot. Line count does not decide; the absence of uncertainty does.

- **What + Done statable and Decisions resolved/obvious** (but not trivial enough for shot) → **organic**.
  Answer: `→ run /mala-pata-organic`, and hand it as a draft the fields you already inferred (What / Why / DoD / Decisions / Risk) so organic confirms instead of starting from scratch. The same draft goes to `/mala-pata-loop`. **Optional `change_name`**: when triage was invoked for a roadmap phase (the arg is a slug), add `change_name: <slug>` to the draft so the lane uses it as the change-name; when free-standing, omit it.

- **Open decision — distinguish whether it is DECIDABLE or NEEDS DESIGN** (this is the loop discriminator; NOT "there is a decision → loop"):
  - **Decidable with one question** (known options and the human chooses, a preference, or a product call) → NOT loop. Ask **that** focused question, stop and wait; once resolved → **organic** (or **shot** if it is also trivial: 1-3 files, no migration/contract/new UI). Test: *can I state the options and does one answer close them?*
  - **Needs design** (several viable architectures with tradeoffs to investigate, or the options are not known without exploring) → **loop**. Answer: `→ run /mala-pata-loop`. Test: *do I need to investigate/explore to even know the options or their tradeoffs?*

- **What/Done clear but the scope spans several cycles** (multi-loop) → **roadmap**.
  Answer: `→ run /mala-pata-roadmap`.

- **Too vague to even state What/Done** (and 1 question is not enough to fix it) → **do NOT route.** Answer in "vague work" style, same as Step 0 of `/mala-pata-loop`:

  > **vague work ** — I need at least: *what* you want to achieve, *where* (module/feature, if you know it) and *when it is done* (verifiable criterion, not "make it look good"). With that I tell you the lane.

  And you stop there.

### Output format (BLUF — decision first)
1. **Decision line (always first):** `Lane: <shot | organic | loop | roadmap> — Reason: <the test that applied, one line>`.
2. **Draft (only when routing to organic/loop)** — a table, not prose:

   | Field | Value | Provenance |
   |---|---|---|
   | What | <concrete objective> | [inferred] / [asked] |
   | Why | <one line> | [inferred] / [asked] |
   | DoD | Given <state>, When <action>, Then <result> | [inferred] / [asked] |
   | Decisions | <resolved approach, or "open: needs design → loop"> | [inferred] / [asked] |
   | Risk | <blast radius, one line> | [inferred] / [asked] |

   Add a `change_name: <slug>` row when triage was invoked for a roadmap phase (omit when free-standing).
3. **DoR line:** `DoR: What ✓ · DoD ✓ · Decisions ✓` (the three blocking fields passed the gate).
4. **Footer:** `Structure: Definition of Ready + INVEST. Lane routing = house method.`

**Emit this block's structural labels verbatim in English** — section headers, field labels, table/column headers, and enum/option tokens stay English even when the conversation is in the user's language; only the values and content are localized. This covers the `→ run /mala-pata-<lane>` line and the draft field labels (What / Why / DoD / Decisions / Risk) handed to the lane.

## Phase 3 — Does nothing else

You do not create a worktree, you do not write a kickoff, you do not run phases of any cycle. Your answer ends at the previous point: either the lane + draft, or the bounce to vague work, or the single clarifying question allowed.

**Only exceptions** (when the answer is not just the routing):
- Phase 0 read-only → stay in read mode, without deciding a lane.
- Real blocking ambiguity → the only question allowed before deciding.
- Gate too vague → `vague work `.
