---
name: mala-pata-research
description: >
  Pre-triage idea shaper; takes a raw idea, researches it (how it is done
  today + limits, anchoring to the code, JTBD), sharpens it with the Heilmeier
  Catechism, ALWAYS writes a research doc, gives a VERDICT (PROCEED / SHARPEN /
  RECONSIDER — it may propose killing the idea), and only then hands off to
  `/mala-pata-triage` (or `/mala-pata-roadmap` if it is multi-unit). Read-only:
  it does not create a worktree/kickoff/code.
  Trigger: "prepará esta idea", "research de <idea>", "ayudame a armar esta
  idea antes de triage/roadmap", or any raw/fuzzy idea that is not yet ready
  to be routed.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.10.0"
---

# /mala-pata-research — raw idea shaper (pre-triage)

User idea: **input delivered by the CLI**

You are **diamond 1** (Discover → Define) of mala-pata's Double Diamond. The full pipe is:

**research (sharpens)** → `/mala-pata-triage` (routes) → `organic` / `loop` / `roadmap` (executes)

Your only job is to take a raw or fuzzy idea and **sharpen** it until triage (or roadmap, if it is multi-unit) has something to decide with. You research, put it in contact with the real code, run it through the Heilmeier Catechism, and converge it into a problem statement with a draft of the fields.

> **You do NOT execute anything.** Your deliverable is EXCLUSIVELY the research doc + the handoff. You do NOT create a worktree, do NOT write a kickoff, do NOT touch code, do NOT run any lane.
> The final result is ALWAYS: (a) the research doc written to disk, and (b) a handoff line to `/mala-pata-triage` (or `/mala-pata-roadmap` if the size signal came out multi-unit).

## Requirements (orchestrate, don't reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory**: none.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded):
  - `codegraph` — code graph (anchoring and structure). Fallback: grep/Read. Install: global npm CLI; per-project init with `gentle-ai codegraph init --cwd <repo>`.
  - `serena` — symbol-level navigation and editing. Fallback: codegraph/grep. Install: `uv tool install -p 3.13 serena-agent && serena setup claude-code`.
  - `WebSearch/WebFetch` — external research. Fallback: disclose that there is no external research. Install: not required (native client tools).
  - `engram` — persistent memory and continuity pointer. Fallback: the doc file is the source. Install: ships with gentle-ai (`brew install gentleman-programming/tap/gentle-ai`).

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP, e.g. serena). If a mandatory one is missing, do not continue.

## Phase 0 — Authorize (always read-only)

Research **never mutates**, without exception. Even if the raw idea already implies an obvious code change, your job here is only to research and sharpen — you do not generate a kickoff, do not propose a worktree, do not write a single line of code. The lane decision and execution stay downstream, in triage and in whatever triage routes to.

## Phase 1 — Discover (diverge)

You open the fan before converging. Research in parallel:

**(a) External research** (WebSearch/WebFetch): how this kind of idea is solved TODAY, what the limits of current practice are, and what best practices exist — with cited sources. It is not an exhaustive literature review: it is enough to know whether you are about to reinvent something that already has a known solution.

**(b) Anchoring to the real code** (codegraph/Read): what already exists in the project that touches this idea, what installed infrastructure enables more than the original idea imagined. Anchor the external material to YOUR code — a best practice that ignores what is already built is useless (reuse-first). **Inventory the mechanisms that ALREADY exist** and could solve this (helpers, flags, settings, a pattern already applied elsewhere in the repo). **Before concluding "new code is needed", prove with evidence that the existing ones are NOT enough** — not merely because you did not look for them. Spending the analysis on the first mechanism you find and jumping to "new code" is the classic mistake.

**(c) Jobs-to-be-done**: whose job the idea solves, what the real struggle behind the request is, and what outcome it seeks. Phrase it as: "as `<user>`, I need `<job>` so that `<benefit>`". This often reveals that the raw idea is a symptom, not the real job.

**(d) Size the problem (project-agnostic)**: before thinking about the size of the SOLUTION, measure the size of the PROBLEM with the available evidence, on three generic axes (not a fixed list from one domain):
- **Scope** — how much/what it covers (how many things are affected, what portion of the whole).
- **Frequency** — how often it happens.
- **Severity / impact** — in the terms THIS project uses (money, users, time, risk, security… whatever applies).
Each project fills those axes with whatever makes sense, using evidence from the code and the sources. If an axis cannot be measured with evidence, flag it and ask the human (Phase 2) — do not invent it. This problem size is what feeds the size signal of Phase 3, NEVER the volume of code/files/PRs.

**(e) Problem vs proposed solution**: the request almost always comes with a solution already assembled (a column, an endpoint, a knob). Do NOT take those pieces as scope automatically. For each piece of the proposed solution, classify:
- **necessary** — needed to solve the real problem.
- **already-exists** — the repo already covers it (from (b)); it is dropped.
- **derivable** — it comes for free from another piece (e.g.: if "the cycle with a difference" already selects, a per-cycle knob is redundant); it is dropped.
- **extra** — desirable improvement, not part of the problem; it is named separately and does not inflate the scope.
Only the `necessary` pieces move on to Define; the others remain named (they do not disappear silently) but do not count toward size.

## Phase 2 — Heilmeier Catechism (answer what you know, ASK what only the human knows)

The 7 questions (DARPA framework adapted to 7 for mala-pata — verbatim list, do not paraphrase):

1. What are you trying to do? Explain it with no jargon.
2. How is it done today, and what are the limits of current practice?
3. What is new in your approach, and why do you think it will work?
4. Who cares? If you succeed, what difference does it make?
5. What are the risks?
6. How much will it cost / how long will it take? (order of magnitude)
7. What are the intermediate and final exams of success? (= the testable Done)

**It is an interrogation, NOT a form you complete by inference.** Split the answers in two:

- **Answerable by research/code** (Phase 1): typically 1, 2, 3, 6 and often 5 — they are answered
  with what you found, anchored to real evidence.
- **Only the human knows**: typically **4 (who REALLY cares / the priority)** and **7 (what success looks
  like FOR them / what counts as done)**, plus any business constraint. **Do NOT invent these.** Ask them
  with the interactive mechanism, **one at a time, and stop to wait for the answer.** If out of necessity
  you must infer one, mark it explicitly as an *assumption to confirm*, never as a fact.

**Assumption challenge (just one, no debate loop):** name the **high-impact unproven premise**
the idea rests on (e.g.: "this is needed now", "nothing already exists that solves it") and
challenge it with the evidence from Phase 1. If the evidence contradicts it, that feeds the
**RECONSIDER** verdict (Phase 5).

## Phase 3 — Define (converge)

Collapse everything above into a **sharpened idea**: a clear problem statement plus a draft of the fields `/mala-pata-triage` needs to decide the lane:

- **What** — concrete, observable objective.
- **Why** — one-line motivation.
- **DoD** — the testable definition, in Given/When/Then ("Given <state>, When <action>, Then <observable result>").
- **Decisions already made** — what of the approach/architecture the research already settled.
- **Open decisions** — what remains unresolved (this is exactly what triage needs to separate organic from loop).
- **Risk** — blast radius in one line.

Add the **size signal**: does this fit in one unit (one organic or one loop), or is it multi-unit (it needs `/mala-pata-roadmap` to be decomposed first)? **The signal comes from the size of the PROBLEM (Phase 1d) and from the open architecture decisions — NEVER from the volume of code, files or PRs.** A small problem with a clear solution is single-unit even if it touches several files; multi-unit only when there are several open architecture decisions or genuine independent vertical slices. Count only the `necessary` pieces from Phase 1e.

## Phase 4 — Write the doc (MANDATORY, ALWAYS)

You ALWAYS write the research doc, without exception — it is your deliverable. It goes **inside the repo, versioned**: `mala-pata/research/<slug>.md` (relative to the repo root, `git rev-parse --show-toplevel`; `mkdir -p` the folder if it does not exist).

**Lightweight pointer in engram** for discoverability: `mem_save` with `topic_key: "research/<slug>"`, single-line content: `Research in file: <absolute path>`. Do not duplicate the content in engram — the file is the source of truth. If engram is unavailable, the file is still the source of truth; warn in one line that the pointer was not saved.

### `.md` doc format

```markdown
---
idea_slug: <kebab>
project: <project>
verdict: PROCEED | SHARPEN | RECONSIDER
created_at: <ISO 8601>
next: triage | roadmap | none (RECONSIDER/SHARPEN)
size_signal: one-unit | multi-unit
---
# Research: <idea>
## Verdict: <PROCEED | SHARPEN | RECONSIDER>
<one line with the reason, backed by the evidence below>
## Raw idea (what you asked)
## Discover
### How it's done today + limits (with sources)
### What exists in the code (real anchoring)
### Jobs-to-be-done
### Problem dimension (scope / frequency / severity — with evidence; mark what you asked)
### Problem vs proposed solution
| Piece | Class (necessary / already-exists / derivable / extra) | Evidence | Provenance |
|---|---|---|---|
| <piece> | <class> | <file:line or source> | [noted] / [inferred] |
## Heilmeier Catechism
| # | Question | Answer | Provenance |
|---|---|---|---|
| 1 | <question, verbatim from the 7> | <answer> | [asked] / [assumed] / [noted] |
## Define — sharpened idea (draft for triage)
- What / Why / DoD / Decisions made / Open decisions / Risk / Size signal
## DoR (hand-off gate): What ✓ · Why ✓ · DoD ✓ · Decisions ✓
## Handoff

Structure: Heilmeier Catechism (DARPA) + Double Diamond (Design Council). Verdict / size-signal / Left-OUT = house method.
```

(The headings inside the template block are fixed English identifiers; only the `<...>` placeholders are filled at execution time.)

## Phase 5 — Mandatory close: VERDICT + plain-language summary + doc

Same spirit as `/sdd-preview` (your invention): a close that is **scannable in ~30 s and lets the reader understand WHAT
it will do and WHETHER IT IS WORTH IT without opening the md**. It comes from the doc, without inventing, and is NOT the
whole doc pasted. The human decides with this alone.

**Start with the verdict — that is research's HELP; do not shape for the sake of shaping.**

- **Title:** `**Research: <slug> — <VERDICT>**` with the verdict carrying a curated glyph: `✓ PROCEED` · `◐ SHARPEN` · `✗ RECONSIDER`. The frontmatter `verdict:` value stays the plain word (PROCEED/SHARPEN/RECONSIDER) for parsing.
- **Verdict** (one line with the reason, backed by the Phase 1 evidence):
  - **PROCEED** — the idea is solid and ready to be routed.
  - **SHARPEN** — you need to answer something only you know (the human-only questions of Phase 2 that
    remained open). Name them; routing waits until then.
  - **RECONSIDER** — the evidence weakens the idea, and research **proposes killing or pivoting it**: "Y already
    solves it", "premise Z is false", "there is a cheaper path W". Say it straight, with the evidence,
    **even if it is the opposite of what the human asked for** — this is exactly what research exists for.
    Killing an idea here is cheap; after an entire roadmap, it is not.

Then the plain-language summary:
- **What it proposes** — one sentence, no jargon.
- **Why** — 2-4 key findings that support it.
- **What it will do** — the high-level shape (tiers/pieces/compact phases).
- **Problem size** — scope / frequency / severity (from Phase 1d) — the human decides the size by looking at THIS, not at the volume of code.
- **What matters** — main risk + open decisions.
- **Size signal:** one-unit | multi-unit.
- **Left OUT / pending** — MANDATORY **only if the signal is single-unit** (it goes to an organic/loop/shot cycle, NOT to roadmap). List each piece from Phase 1e that fell out of scope (already-exists / derivable / extra), one per line, with why and who decided: `<piece> — <why it stays out> — [skill rule | judgment]`. Nothing disappears silently: if you chose a small cycle, the human has to see what does NOT go in and be able to add it. If the signal is multi-unit → this block does NOT go: the roadmap covers everything, and what can wait is marked there with the `Deferrable?` column (it is not discarded).
- **Doc:** `<absolute path of the .md>`
- **Next step — DEPENDS on the verdict:**
  - **PROCEED** → `/mala-pata-triage <slug>` (or `/mala-pata-roadmap <slug>` if multi-unit), passing the draft of fields from Phase 3.
  - **SHARPEN** → answer the named questions and re-run research; do NOT route yet.
  - **RECONSIDER** → do NOT route; the decision is yours (kill, pivot, or proceed anyway accepting the risk with eyes open).
- **Structure:** Heilmeier Catechism (DARPA) + Double Diamond (Design Council). Verdict / size-signal / Left-OUT = house method.

This block is the ONLY way to close on the happy path.
- **Emit this block's structural labels verbatim in English** — section headers, field labels, table/column headers, and enum/option tokens stay English even when the conversation is in the user's language; only the values and content are localized.

## Closing notes

- **Questions**: only the real product decisions that the Heilmeier Catechism uncovers (for example, "who cares" stays ambiguous, or the risk changes the scope). Ask a single question at a time, and stop to wait for the answer — never in a batch.
- Research **does NOT dispatch `sdd-*` agents** — gentle-ai's `PreToolUse:Agent` preflight does not apply here, just as it does not apply to `/mala-pata-triage` nor to `/mala-pata-organic`.
