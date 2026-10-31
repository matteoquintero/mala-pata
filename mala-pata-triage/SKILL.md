---
name: mala-pata-triage
description: Single front-door of mala-pata. Trigger — any change request, BEFORE touching code. Reads the request, applies the form gate (What + DoD + Decisions), and ANSWERS which lane/skill to run — `/mala-pata-shot`, `/mala-pata-organic`, `/mala-pata-loop` or `/mala-pata-roadmap` — handing the chosen lane the draft of already-inferred fields. It does NOT generate files, does NOT create worktrees, does NOT execute anything: it is a decision skill, not an execution one.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.13.0"
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

## Phase 0.5 — Read the research (ALL of it — one slug or several), synthesize, do NOT swallow

If the input resolves to research docs that `/mala-pata-research` handed off, `Read` them and use their Define fields (What / Why / DoD / Decisions / Risk / size_signal) as the draft instead of only the raw request text. Then run the form gate below over that **synthesized** draft.

- **One or several — read them ALL.** The human may pass several slugs/paths, or ONE slug whose objective was researched in MORE THAN ONE pass. Before routing, find every research doc that belongs to THIS objective: the passed slug(s), plus sibling docs under the **same `domain:`** whose subject is clearly the same objective (a SHARPEN a later pass resolved, a second angle on the same thing). If there are signs of more than one pass on the same topic and only one was passed, say so and read the others — **never route off a single doc when several researched the same objective.**
- **Synthesize, do NOT pick the latest and drop the rest.** Reconcile all of them into ONE draft: later evidence supersedes earlier on a direct conflict (NAME what it corrected — e.g. a value re-grounded in the authoritative source over a first pass that had inferred it), and the findings/sources UNION (no search is thrown away — the accumulated evidence is the asset). The draft's What/Why/DoD reflect the ACCUMULATED research, not the last file read. Carry an inference AS an inference — if a doc marked something `[inferred]` or OPEN (e.g. "e2e not proven"), it stays OPEN in the draft, never upgraded to a settled DoD.

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

## Phase 1.5 — Standard check (DoD determinism + new-standard permission)

Two checks against the project's captured standard (`/mala-pata-standards` → `mala-pata/standards/<domain>.md`, `approved` rules only) BEFORE deciding the lane:

1. **Non-deterministic DoD → bounce to research, do NOT dead-end.** A DoD that is statable but ARBITRARY (the ask could be satisfied many ways — "a button", "a screen", "somewhere") is different from "too vague to state What/Done at all" (that stays `vague work`). It needs GROUNDING in the standard, not a bounce to vagueness. If an `approved` standard covers it → state the deterministic DoD against it and continue. If not → bounce to `/mala-pata-research` to ground it (research AUTHORS the deterministic DoD; triage does NOT author it, it only detects and routes).
2. **New-standard permission gate — ask BEFORE a new standard enters.** If the change would ESTABLISH a NEW standard (a visual/interaction convention not covered by an `approved` rule — a new component shape, a new placement, a new pattern), do NOT let it slip in as a de-facto standard. ASK the human's permission, one line: "this introduces a new standard (`<the convention>`) — approve it entering the project standard, or should it conform to an existing approved one?" Only on approval does it proceed as a new standard (captured later via `/mala-pata-standards`); on denial it must conform to an existing `approved` standard. Never admit a new standard silently.

If the project has no captured standard yet, say so in one line and continue (the grounding is best-effort until `/mala-pata-standards` runs); do not block routing on a standard that does not exist.

## Phase 2 — Decide and answer the lane

- **Trivial + understood + minimal blast radius** (obvious What/Done, no decisions, 1-3 files, no migration/contract/new UI) → **shot**.
  Answer: `→ run /mala-pata-shot`. It is ODD with no worktree and no ceremony, for the smallest change. **Boundary with organic**: with ANY uncertainty, decision, or necessary ceremony (design, migration, new UI) → organic, NOT shot. Line count does not decide; the absence of uncertainty does. **Research carry-over**: if triage came FROM `/mala-pata-research`, append the slug to the handoff (`→ run /mala-pata-shot · research: <slug>`) so shot folds `mala-pata/research/<slug>.md` into its work-unit commit (shot has no worktree — the file is already in place, it only gets committed).

- **What + Done statable and Decisions resolved/obvious** (but not trivial enough for shot) → **organic**.
  Answer: `→ run /mala-pata-organic`, and hand it as a draft the fields you already inferred (What / Why / DoD / Decisions / Risk) so organic confirms instead of starting from scratch. The same draft goes to `/mala-pata-loop`. **Optional `change_name`**: when triage was invoked for a roadmap phase (the arg is a slug), add `change_name: <slug>` to the draft so the lane uses it as the change-name; when free-standing, omit it.

- **Open decision — distinguish whether it is DECIDABLE or NEEDS DESIGN** (this is the loop discriminator; NOT "there is a decision → loop"):
  - **Decidable with one question** (known options and the human chooses, a preference, or a product call) → NOT loop. Ask **that** focused question, stop and wait; once resolved → **organic** (or **shot** if it is also trivial: 1-3 files, no migration/contract/new UI). Test: *can I state the options and does one answer close them?*
  - **Needs design** (several viable architectures with tradeoffs to investigate, or the options are not known without exploring) → **loop**. Answer: `→ run /mala-pata-loop`. Test: *do I need to investigate/explore to even know the options or their tradeoffs?*

- **Genuinely multi-unit — TRIAGE OWNS the "roadmap or not" call.** Do NOT inherit it from research's `size_signal` nor from the human asking for a roadmap — those are hypotheses. It is a roadmap ONLY when the objective needs **decomposition into several INDEPENDENT vertical slices**, or carries **several open architecture decisions** that each need their own unit. It is NOT a roadmap just because the request is long or lists many things.
  - Genuinely needs decomposition → **roadmap**. Answer: `→ run /mala-pata-roadmap`.
  - On inspection it actually fits ONE unit → it is **NOT a roadmap**: route it to organic/loop/shot and say so (`Lane: <lane> — Reason: fits one unit, not a roadmap`). You have the power to overrule a roadmap suggestion.
  - Unsure if it is one or several units → prefer a single lane; roadmap's own entry gate bounces it back here if it turns out too big.

- **Too vague to even state What/Done** (and 1 question is not enough to fix it) → **do NOT route.** Answer in "vague work" style, same as Step 0 of `/mala-pata-loop`:

  > **vague work ** — I need at least: *what* you want to achieve, *where* (module/feature, if you know it) and *when it is done* (verifiable criterion, not "make it look good"). With that I tell you the lane.

  And you stop there.

### Output format (BLUF — decision first)

Reason through the gate first; the LAST thing you emit is EXACTLY the shape below — same lines, same columns, same order, values filled in. Never replace the table with vertical `Field:/Value:` blocks or with prose.

1. **Decision line (always first):** `Lane: <shot | organic | loop | roadmap> — Reason: <the test that applied, one line>`.
2. **Draft (only when routing to organic/loop)** — copy this table and fill the values. **Every cell is ONE line** — no multi-sentence cells, no `<br>`, no paragraphs; if a value needs more, compress it (the full detail belongs in the kickoff the lane writes, not here):

   | Field | Value | Provenance |
   |---|---|---|
   | What | <concrete objective, one line> | [inferred] / [asked] |
   | Why | <one line> | [inferred] / [asked] |
   | DoD | Given <state>, When <action>, Then <result> — one line | [inferred] / [asked] |
   | Decisions | <resolved approach, or "open: needs design → loop"> | [inferred] / [asked] |
   | Risk | <blast radius, one line> | [inferred] / [asked] |

   **One objective per What — a compound What is a routing signal, not a formatting problem.** If the What only holds together with an "and" joining two independent deliverables (e.g. "rename the field AND hide the toggle AND fix the printout"), do NOT cram them into one cell: either they are ONE coherent vertical change — then state the single OUTCOME they add up to (the one capability or behavior the pieces serve together) — or they are several, which is the multi-unit signal (consider roadmap, or name the primary and flag the rest). Same rule for the DoD: Given/When/Then describes ONE observable outcome; stacked `And` clauses each asserting a different deliverable are the same smell. Compress to the real objective; never let the draft smuggle a decomposition past the gate as "one line".

   Add a `change_name: <slug>` row when triage was invoked for a roadmap phase (omit when free-standing).
   Add a `research: <slug[, slug...]>` row when triage came FROM `/mala-pata-research` (the arg is a research slug, the request names a research doc, or Phase 0.5 synthesized several), so the lane records them in the kickoff and `organic-start`/`loop-start` carries EVERY `mala-pata/research/<slug>.md` into the feature's PR, tied to the commit. List ALL the synthesized slugs, not just one. Omit the row when there was no research (the lane defaults to `research: none`).

   **Open product decisions — flag, do NOT invent.** If a draft field hides a scope/behavior call only the human can make (what is IN vs OUT, who can do it / permissions, side-effects on other systems or data), write the cell as `open: <the question>` instead of guessing a value. The lane (organic/loop) MUST ask these one at a time before locking the kickoff — triage decides the lane and flags them; `/mala-pata-research` is what resolves them fully when the uncertainty is deep. Guessing a product decision and passing it as settled is the failure.
3. **DoR line:** `DoR: What ✓ · DoD ✓ · Decisions ✓` (the three blocking fields passed the gate).
4. **Footer:** `Structure: Definition of Ready + INVEST. Lane routing = house method.`

**Emit every structural label verbatim in English** — section headers, field labels, table/column headers, and enum/option tokens stay English even when the conversation is in the user's language; only the values and content are localized. This covers the `→ run /mala-pata-<lane>` line and the draft field labels (What / Why / DoD / Decisions / Risk) handed to the lane.

## Phase 3 — Does nothing else

You do not create a worktree, you do not write a kickoff, you do not run phases of any cycle. Your answer ends at the previous point: either the lane + draft, or the bounce to vague work, or the single clarifying question allowed.

**Only exceptions** (when the answer is not just the routing):
- Phase 0 read-only → stay in read mode, without deciding a lane.
- Real blocking ambiguity → the only question allowed before deciding.
- Gate too vague → `vague work `.
