---
name: mala-pata-standards
description: HARVESTS a project's STANDARD into a captured, versioned artifact — the VISUAL language and the INTERACTION / LAYOUT conventions (where things go, how components behave), inferred READ-ONLY from the repeated patterns in the real code, so the rest of the suite can GROUND against it instead of guessing. It does NOT invent the standard — where the project is INCONSISTENT it shows the variants and ASKS the human which one IS the standard; it never picks for them. Nothing enters the captured standard without the human's explicit per-rule approval — the foundation is approve-each-one-by-one (heavy on purpose), lighter after. Two modes — harvest FRESH from the code, or ADOPT an existing standards doc and normalize it. v1 scope is visual + interaction/layout; code / structural conventions (naming, folder architecture) are a named FUTURE layer, out of v1. Writes mala-pata/standards/<domain>.md with a domain; READ-ONLY on the project (it captures, it never changes code). Trigger — "estandarizá el proyecto", "capturá el estándar de <área>", "cuál es el estándar de los modales / botones / pantallas", "armá el design standard de <proyecto>", "normalizá este estándar al formato".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "0.2.0"
---

# /mala-pata-standards — capture a project's standard (harvest, do not invent)

Input: **the one delivered by the CLI** — an **area/project to harvest** (new standards doc), or the **path to an existing standards doc** to adopt and normalize.

Your job: discover the project's STANDARD by reading the real code and capture it in a document the rest of the suite can ground against — the **visual language** and the **interaction / layout conventions**. You INFER the standard from what the code repeatedly does; you do NOT design a new one, and where the project disagrees with itself you ASK, you do not pick.

> **Harvest, never invent.** The standard is what the project ALREADY does, read off repeated patterns — not your taste and not a best-practice you import. An imported ideal that the code does not follow is not this project's standard.
> **Nothing becomes a standard without a human YES — one by one.** A rule the code repeats is only a CANDIDATE; it enters the captured standard as `approved` only when the human explicitly approves THAT rule. The first harvest (the foundation) is heavy by design — every rule approved or rejected one at a time — so nothing entrenches itself as "the standard" just because the code happened to repeat it. After the foundation it is lighter: new standards enter incrementally, each still asking permission (at `/mala-pata-triage`).
> **Inconsistency is a question, not a guess.** When instances disagree (two placements, two button styles, two spacings), show the variants with their evidence and ASK the human which is canonical. Capture their ruling; never silently choose the most common and call it the standard.
> **Read-only capture.** You inspect the code to describe it; the only thing you write is the standards `.md`. You do NOT change code, do NOT restyle anything, do NOT commit.

## Requirements (orchestrate, do not reinvent)

- **Mandatory** (no fallback — if missing, STOP): `git` — resolve the repo root for the document's location.
- **Recommended** (with fallback — warn in one line and continue degraded):
  - `codegraph` / `serena` — find the recurring components and instances to compare. Fallback: grep/Read.
  - `engram` — one-line discoverability pointer. Fallback: the file is the source of truth.

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP). If a mandatory tool is missing, do not continue.

## Phase 0 — Authorize (read-only guard)

Capturing a standard is **always read-only** — you describe what the project already does. Even when the code is inconsistent and "should" be fixed, your work here is only the document; the fix is a separate change in a lane, not this skill.

## Phase 1 — Mode + scope + grounding

1. **Mode**: an area/project → harvest a new standards doc. A **path to an existing standards doc** → **adopt**: read it and map onto the standard (Phase 3), keeping what is real.
2. **Scope (v1)**: harvest **visual** (the design tokens as actually used — color, type, spacing, radius, elevation) and **interaction / layout** (recurring component shapes, placement rules, state/behavior conventions). **Code / structural conventions (naming, folder architecture) are OUT of v1** — name them as a future layer if you see them, do not capture them yet.
3. **Ground it in the real system** (read-only): find the RECURRING instances of each thing (codegraph/serena/grep), not one example. A standard is a pattern seen across many instances; a single instance is not a standard.

## Phase 2 — Infer the standard + flag inconsistencies (ASK, do not pick)

This is where the standard is found. For each visual token and each interaction/layout convention:

1. **Infer candidates from repetition** — gather the instances and state the rule the majority embodies, with evidence (the files/components it was read from). EVERYTHING you infer is a CANDIDATE (`proposed`), never a standard yet — even a rule the whole codebase agrees on.
2. **Human approval, one by one — the foundation gate** — present each candidate to the human and get an explicit YES before it enters the captured standard as `approved`. No YES → it does NOT enter as a standard (it stays `proposed`, or is dropped). This is deliberately heavy at the first harvest so nothing becomes "the standard" by accident just because the code repeats it; after the foundation it is lighter — new standards trickle in via `/mala-pata-triage`'s permission gate, each still approved before it counts.
3. **Inconsistencies** — where instances conflict (two placements, two styles, two spacings for the same role), DO NOT pick the most common. List the variants with their evidence and **ASK the human which one is canonical**, one at a time; the chosen one still passes the approval of step 2. Unresolved → explicit `OPEN:`, never a guess.
4. **Name the future layer** — anything structural/code-level you noticed (naming, architecture) goes in a short "out of scope (future layer)" note, not captured as a rule.

## Phase 3 — The standard (what every standards doc contains)

Write to `mala-pata/standards/<domain>.md` (inside the project repo, versioned; `mkdir -p`). Citing real files here is CORRECT — this artifact describes the real project (unlike a skill, which stays generic). **Frontmatter** (feeds `/mala-pata-domain-radar`):

```markdown
---
slug: <kebab>
domain: <the area/system this standard covers — else 'main'; NEVER blank, ANY doubt → ASK the human>
kind: standard
scope: visual-interaction           # v1; structural is a future layer
owner: <who owns this standard>
created_at: <ISO 8601>
last_reviewed: <ISO 8601>
---
```

**Timestamps.** Fill every generated timestamp from the machine's local clock — run `date '+%Y-%m-%dT%H:%M:%S%z'` and use its exact output (local time with UTC offset, e.g. `2026-11-01T17:25:40-0500`); never invent the time and never default to UTC.

**Body** (fixed section order — labels verbatim English):

| Section | What it holds |
|---|---|
| Summary | One line: what this standard covers and where it was read from. |
| Visual language | The tokens AS USED — color roles, typography scale, spacing, radius, elevation — each with evidence and whether it is consistent or `OPEN`. |
| Component patterns | The recurring components and their standard shape (anatomy, variants, states), with evidence. |
| Interaction / layout conventions | The placement and behavior rules — e.g. "a modal's actions live in a right-side panel, grouped by role: primary, then secondary tools, then destructive". Each rule with evidence. |
| Inconsistencies / OPEN | Where the project disagrees with itself: the variants, the evidence, and the human's ruling — or `OPEN:` when unresolved. Nothing hidden. |
| Out of scope (future layer) | Structural/code conventions noticed but NOT captured in v1 (named only). |

Each rule carries its **evidence** (the components/files it was read from) and a **status**: `approved` (the human signed off — the ONLY status authoritative for grounding), `proposed` (inferred and repeated, but awaiting the human's YES — NOT yet authoritative), or `OPEN` (contested, awaiting a ruling). A rule never grounds anything until it is `approved`.

## Phase 4 — Persist (write only) + pointer

1. **Write only — do NOT commit/push.** Write the file; tell the human the path + the durable branch it belongs on so they commit it in their normal flow.
2. **Adopt mode**: write the normalized standards doc to `mala-pata/standards/<domain>.md`; do NOT delete the original — name it and let the human retire it. List the gaps you filled.
3. **Lightweight pointer in engram**: `mem_save` topic_key `standards/<domain>`, one-line content `Standard in file: <absolute path>`. If engram is unavailable, the file is the source — warn in one line.

## Phase 5 — Close (mandatory: summary + doc)

Emit exactly this, from the document you wrote (no invention):

- Title: `**Standard ready — <domain>**`
- BLUF: `Standard: <a> approved · <p> proposed (awaiting your YES) · <k> OPEN (contested)`
- A short readback table (`Area | Status | Evidence`) — one line per rule/area, so the human sees what is approved, what still awaits their YES, and what is contested.
- **OPEN** inconsistencies, if any — one per line, each needing the human's ruling (never hidden).
- **File:** `mala-pata/standards/<domain>.md`
- **Next step** — the standard is the INPUT the rest of the suite grounds against: `/mala-pata-art` judges/applies the visual part, `/mala-pata-research` makes a vague DoD deterministic against it, the lanes conform. Resolve the OPEN rulings to raise coverage.

`Structure: pattern-mining (infer the rule from repeated instances) + inconsistency-as-question (ask, never pick) + evidence-and-confidence capture. Harvest-not-invent + visual/interaction scope = house method.`

This block is the only way to close on the happy path. **Only exceptions**: Phase 0 read-only stance; a blocking inconsistency ruling (Phase 2) → the single question allowed before writing.

> **Canonical structural-labels rule — single source of truth.** Apply `_shared/mala-pata-structural-labels.md` verbatim; it supersedes any restatement in this skill. Do not paraphrase or re-derive it.
**Frozen close labels** — title `Standard ready`; BLUF label `Standard:`; readback columns `Area` · `Status` · `Evidence`; Status tokens `approved` · `proposed` · `OPEN`; block labels `OPEN`, `File`, `Next step`, `Structure`. Emit them verbatim in English even when the conversation is in another language; only the values are localized.

## What it does NOT do (invariants)

- Does NOT invent or import a standard — it harvests what the project already does.
- Does NOT pick a winner on an inconsistency — it asks the human and captures the ruling (or leaves it `OPEN`).
- Does NOT admit a rule as a standard on inference alone — nothing is `approved` without the human's explicit per-rule YES (candidates stay `proposed`).
- Does NOT change code, restyle, or fix the inconsistencies — that is a lane's job, not this skill's.
- Does NOT capture code/structural conventions in v1 — only visual + interaction/layout (structural is a future layer).
- Does NOT commit — write-only; the human commits in their PR flow.

## Relation to the family

- **Feeds** `/mala-pata-art` (which judges/applies the VISUAL standard but assumes it exists — this skill is what CAPTURES it) and `/mala-pata-research` (which grounds a vague DoD against the captured standard so it becomes deterministic). The lanes conform to it.
- **Different from** `/mala-pata-art` — art is visual JUDGMENT (how to improve a given artefact); standards is CAPTURE (what the project's standard IS). Capture first, judge/apply after.
- **Indexed by** `/mala-pata-domain-radar` (reads the `domain:` frontmatter, like the other mala-pata artifacts).
- It is a capture/doc-authoring skill, orthogonal to the lanes (`shot`/`organic`/`loop`/`roadmap`), not a route.
