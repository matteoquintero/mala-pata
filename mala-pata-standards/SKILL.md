---
name: mala-pata-standards
description: HARVESTS and ORGANIZES a project's STANDARD into a captured, versioned, well-ordered artifact — the VISUAL language and the INTERACTION / LAYOUT conventions (where things go, how components behave), inferred READ-ONLY from the repeated patterns in the real CODE and the stated conventions in the project's DOCUMENTATION, so the rest of the suite can GROUND against it instead of guessing. It does NOT invent the standard — where the project is INCONSISTENT (or where code and docs disagree) it shows the variants and ASKS the human which one IS the standard; it never picks for them. Nothing enters the captured standard without the human's explicit per-rule approval — the foundation is approve-each-one-by-one (heavy on purpose), lighter after. It writes the standard into an ORDERED two-level structure (an open set of AREAS × bounded-context, each area decomposed by its discipline's recognized internal model) — not one flat md. Three modes — harvest FRESH from code + docs, ADOPT an existing standards doc and normalize it, or REORGANIZE an already-messy standards folder into the ordered structure. v1 captured scope is visual + interaction/layout; code / structural conventions (naming, folder architecture) are a named FUTURE layer, out of v1 — but the structure RESERVES their slots. Writes under mala-pata/standards/ with a domain; READ-ONLY on the project (it captures, it never changes code). Trigger — "estandarizá el proyecto", "capturá el estándar de <área>", "organizá los estándares del proyecto", "buscá el estándar en el código y la documentación", "ordená la carpeta de estándares", "cuál es el estándar de los modales / botones / pantallas", "armá el design standard de <proyecto>", "normalizá este estándar al formato".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "0.3.1"
---

# /mala-pata-standards — capture AND order a project's standard (harvest, do not invent)

Input: **the one delivered by the CLI** — an **area/project to harvest** (new standards doc), the **path to an existing standards doc** to adopt and normalize, or a request to **organize/reorganize** the project's standards folder.

Your job: discover the project's STANDARD by reading the real code AND the project's documentation, capture it in an ORDERED structure the rest of the suite can ground against — the **visual language** and the **interaction / layout conventions**. You INFER the standard from what the code repeatedly does and what the docs state; you do NOT design a new one, and where the project disagrees with itself (or code and docs conflict) you ASK, you do not pick.

> **Harvest, never invent.** The standard is what the project ALREADY does — read off repeated code patterns AND stated in the project's docs — not your taste and not a best-practice you import. An imported ideal that neither the code nor the docs follow is not this project's standard.
> **Two sources, one standard — code AND documentation.** The code shows what the project DOES; the documentation shows what it SAYS it does. Harvest both. When they AGREE, the rule is stronger. When they DISAGREE, that is an inconsistency to surface and ask about — never silently prefer one source. Every rule records its provenance: inferred-from-code, stated-in-doc, or both.
> **Nothing becomes a standard without a human YES — one by one.** A rule the code repeats or a doc states is only a CANDIDATE; it enters the captured standard as `approved` only when the human explicitly approves THAT rule. The first harvest (the foundation) is heavy by design — every rule approved or rejected one at a time — so nothing entrenches itself as "the standard" just because the code happened to repeat it or a stale doc happened to claim it. After the foundation it is lighter: new standards enter incrementally, each still asking permission (at `/mala-pata-triage`).
> **Inconsistency is a question, not a guess.** When instances disagree (two placements, two button styles, two spacings), or code and docs disagree, show the variants with their evidence and ASK the human which is canonical. Capture their ruling; never silently choose the most common and call it the standard.
> **Order is part of capture, not an afterthought.** The standard is written into an ORDERED two-level structure (areas × bounded-context, each area by its discipline's model). A standard nobody can navigate is not grounding infrastructure — it is a flat dump. Ordering is the difference between 3 skills consuming it and the whole suite grounding against it.
> **Read-only capture.** You inspect the code and docs to describe them; the only thing you write is the standard files under `mala-pata/standards/`. You do NOT change code, do NOT restyle anything, do NOT commit.

## Requirements (orchestrate, do not reinvent)

- **Mandatory** (no fallback — if missing, STOP): `git` — resolve the repo root for the document's location.
- **Recommended** (with fallback — warn in one line and continue degraded):
  - `codegraph` / `serena` — find the recurring components and instances to compare. Fallback: grep/Read.
  - `engram` — one-line discoverability pointer. Fallback: the file is the source of truth.

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP). If a mandatory tool is missing, do not continue.

## Phase 0 — Authorize (read-only guard)

Capturing, adopting or reorganizing a standard is **always read-only on the project** — you describe what the project already does and you re-order the standard files the suite owns. Even when the code is inconsistent and "should" be fixed, your work here is only the standard documents; the fix is a separate change in a lane, not this skill.

## Phase 1 — Mode + scope + sources

1. **Mode** — pick ONE:
   - **harvest** (an area/project) → read code + docs, infer candidates, capture a new/extended standard in the ordered structure (Phase 2 → 3).
   - **adopt** (a path to an existing standards doc) → read it and map it onto the ordered structure (Phase 3), keeping what is real; do not delete the original.
   - **reorganize** (a request to organize/order the standards folder, or a folder that is already a flat md / loose files) → migrate the existing captured standard into the ordered two-level structure, losing no rule (Phase 3-bis). Reorganize does NOT re-harvest and does NOT re-ask approvals already granted — it only MOVES approved/proposed/OPEN rules into their ordered place; a genuinely ambiguous placement is the only thing it asks about.
2. **Scope (v1 captured)**: capture **visual** (the design tokens as actually used — color, type, spacing, radius, elevation) and **interaction / layout** (recurring component shapes, placement rules, state/behavior conventions). **Code / structural conventions (naming, folder architecture) are OUT of v1 capture** — the structure RESERVES their areas (see Phase 3), but you do not capture rules into them yet; name what you see as a future layer.
3. **Sources — both, read-only**:
   - **Code**: find the RECURRING instances of each thing (codegraph/serena/grep), not one example. A standard is a pattern seen across many instances; a single instance is not a standard.
   - **Documentation**: read the project's STATED conventions wherever they live — `README`, `ARCHITECTURE.md`, a `docs/` tree, `CLAUDE.md` / `AGENTS.md`, RFCs or design notes. Do NOT assume a fixed path; discover them. A doc that states a convention is a candidate with `stated-in-doc` provenance.

## Phase 2 — Infer the standard + flag inconsistencies (ASK, do not pick)

This is where the standard is found (harvest mode; adopt maps an existing doc; reorganize skips to Phase 3-bis). For each visual token and each interaction/layout convention:

1. **Infer candidates from both sources** — gather the code instances and the doc statements, state the rule, and record its **provenance**: `inferred-from-code`, `stated-in-doc`, or `both`. EVERYTHING inferred is a CANDIDATE (`proposed`), never a standard yet — even a rule the whole codebase agrees on or a doc asserts.
2. **Human approval, one by one — the foundation gate** — present each candidate to the human and get an explicit YES before it enters the captured standard as `approved`. No YES → it does NOT enter as a standard (it stays `proposed`, or is dropped). Deliberately heavy at the first harvest; lighter after (new standards trickle in via `/mala-pata-triage`'s permission gate, each still approved before it counts).
3. **Inconsistencies — including code-vs-docs** — where instances conflict (two placements, two styles, two spacings for the same role), OR where the code does one thing and a doc states another, DO NOT pick. List the variants with their evidence and provenance and **ASK the human which one is canonical**, one at a time; the chosen one still passes the approval of step 2. Unresolved → explicit `OPEN:`, never a guess.
4. **Place each approved rule in its AREA** (Phase 3) — as a rule is approved, note which area and sub-facet it belongs to; ambiguous placement is asked, not guessed.
5. **Name the future layer** — anything structural/code-level you noticed (naming, architecture) goes in the reserved area's `_index.md` as a named future item, not captured as a rule yet.

## Phase 3 — The ordered two-level structure (what the standard looks like)

The standard is captured into an ORDERED structure under `mala-pata/standards/` (inside the project repo, versioned; `mkdir -p`). Citing real files here is CORRECT — this artifact describes the real project (unlike a skill, which stays generic).

### Level 1 — the spine (faceted)
- **AREA** — an OPEN, extensible set. A starter catalog mala-pata recommends: `ui`, `data`, `architecture`, `api`, `security`, `testing`, `observability`, `content`, `conventions`. NOT a closed list — a project adds an area by DECLARING its internal model (see Level 2).
- **Bounded context (`domain`)** — which part of the system the rule governs. Carried as a frontmatter facet on each leaf (`global | <context-a> | <context-b>`); it does NOT duplicate the tree.

### Level 2 — each area carries its discipline's recognized internal model (its "atomic design")
An area is NEVER a bare folder of loose files — it brings the canonical internal model of its discipline. Recommended models:

| Area | Internal model | Sub-facets |
|---|---|---|
| `ui` | Atomic Design + tokens | `foundations` (tokens: color/type/spacing/radius/elevation/motion, primitive vs semantic) · `atoms` · `molecules` · `organisms` · `templates` · `pages` · `patterns` · `a11y` |
| `data` | ANSI-SPARC three-schema | `conceptual` (entities + relationships) · `logical` (keys/attributes/normalization) · `physical` (tables/indexes/partitioning) · `naming` · `migrations` · `integrity` |
| `architecture` | Clean / Hexagonal | `entities` · `use-cases` · `interface-adapters` · `frameworks-drivers` · `dependency-rule` · `bounded-contexts` |
| `api` | Richardson Maturity Model | `resources` (+ URIs) · `methods-status` · `contracts` · `errors` · `versioning` · `pagination-filtering` · `auth` |
| `security` | OWASP ASVS (chapters) | `authentication` · `session` · `authorization` · `validation` · `crypto` · `data-protection` · `logging` |
| `testing` | Test pyramid | `unit` · `integration` · `e2e` · `fixtures-factories` · `coverage` |
| `observability` | Three pillars | `logs` · `metrics` · `traces` |
| `content` | voice/microcopy | `voice-and-tone` · `microcopy` · `terminology` · `i18n` |
| `conventions` | code/structural (future layer) | `naming` · `folder-architecture` · `git-and-pr` · `lint-format` |

A new area declares its internal model the same way: use the discipline's canonical model if it has one, else define a small flat sub-facet set. Each sub-facet stays small and flat (the faceted scalability property).

### Container
```
mala-pata/standards/
├── _index.md                       ← area catalog + each area's internal model + how to add a new area
├── <area>/
│   ├── _index.md                   ← this area's internal model + its sub-facets
│   └── <sub-facet>.md              ← the rules for this sub-facet (with domain facet in frontmatter)
└── …
```
Resolution convention: an `_index.md` at the root and one per area so consumers (and a human) can navigate. The per-rule `approved/proposed/OPEN` + evidence + provenance stays on each rule, at the leaf.

**v1 captured scope note**: today only the visual + interaction areas carry rules (primarily `ui`, and placement rules that may touch `ui`/`conventions`). The other areas exist in the structure as RESERVED slots with their model declared in `_index.md`, holding no rules yet — so the standard can grow into them without a reshuffle. Do not hardcode-away the future areas.

**Frontmatter** on each leaf (feeds `/mala-pata-domain-radar`):

```markdown
---
slug: <kebab>
domain: <the bounded-context this leaf's rules govern — else 'global'; NEVER blank, ANY doubt → ASK the human>
area: <the Level-1 area, e.g. ui | data | architecture | …>
sub_facet: <the Level-2 sub-facet, e.g. foundations | atoms | conceptual | …>
kind: standard
scope: visual-interaction           # v1; structural is a future layer
owner: <who owns this standard>
created_at: <ISO 8601>
last_reviewed: <ISO 8601>
---
```

**Timestamps.** Fill every generated timestamp from the machine's local clock — run `date '+%Y-%m-%dT%H:%M:%S%z'` and use its exact output (local time with UTC offset, e.g. `2026-11-01T17:25:40-0500`); never invent the time and never default to UTC.

**Each rule** carries its **evidence** (the components/files or the doc it was read from), its **provenance** (`inferred-from-code` / `stated-in-doc` / `both`), and a **status**: `approved` (the human signed off — the ONLY status authoritative for grounding), `proposed` (inferred/stated and repeated, but awaiting the human's YES — NOT yet authoritative), or `OPEN` (contested, awaiting a ruling). A rule never grounds anything until it is `approved`.

## Phase 3-bis — Reorganize mode (migrate a messy folder into the ordered structure)

When the existing `mala-pata/standards/` is a flat md, loose files, or an area that is just a bag of files:

1. **Read every existing rule** — from the flat md(s) and loose files. Enumerate them; this is the inventory you must not lose.
2. **Place each rule** into its `<area>/<sub-facet>.md` per Phase 3, PRESERVING its exact `status`, `evidence`, and `provenance`. Nothing is re-approved and nothing is downgraded by the move.
3. **Idempotent** — re-running updates in place, never duplicates a rule. A rule already in its correct leaf stays.
4. **Never lose or silently drop a rule** — every rule in the old layout appears in the new one. If a rule's area/sub-facet is genuinely ambiguous, ASK the human where it belongs (do not guess).
5. **Write the `_index.md` files** (root + per area) describing the catalog and each area's model.
6. **Do not delete the original messy file blindly** — name it and let the human retire it once they confirm the migration (same discipline as adopt mode).

## Phase 4 — Persist (write only) + pointer

1. **Write only — do NOT commit/push.** Write the files; tell the human the paths + the durable branch they belong on so they commit them in their normal flow.
2. **Adopt / reorganize**: do NOT delete the original/old layout — name it and let the human retire it. List the gaps you filled (adopt) or the rules you moved and where (reorganize).
3. **Lightweight pointer in engram**: `mem_save` topic_key `standards/<domain>`, one-line content `Standard in folder: <absolute path to mala-pata/standards>`. If engram is unavailable, the files are the source — warn in one line.

## Phase 5 — Close (mandatory: summary + doc)

Emit exactly this, from what you wrote (no invention):

- Title: `**Standard ready — <domain>**`
- BLUF: `Standard: <a> approved · <p> proposed (awaiting your YES) · <k> OPEN (contested) · <areas> areas`
- A short readback table (`Area | Status | Evidence`) — one line per rule/area, so the human sees what is approved, what still awaits their YES, and what is contested. (Reorganize mode: the table shows where each rule MOVED.)
- **OPEN** inconsistencies, if any — one per line (including any code-vs-docs conflict), each needing the human's ruling (never hidden).
- **Files:** the ordered structure under `mala-pata/standards/` (root `_index.md` + the area leaves written).
- **Next step** — the standard is the INPUT the rest of the suite grounds against: `/mala-pata-art` judges/applies the visual part, `/mala-pata-research` makes a vague DoD deterministic against it, the lanes conform. Resolve the OPEN rulings to raise coverage. **Pending adoption (separate change(s), do NOT assume done here):** (a) the 3 skills that read the standard TODAY — `/mala-pata-art`, `/mala-pata-research`, `/mala-pata-triage` — resolve the old flat path `mala-pata/standards/<domain>.md`; re-pathing them to the new `_index.md`/structure alters a contract they consume (high risk); and (b) the rest of the suite that SHOULD ground against the standard but does not yet — the `organic`/`loop`/`shot` lanes (deterministic DoD), `walkthrough`, `states`, `roadmap`, … — should be EXTENDED to consume it (per-skill new behavior). The ordered structure is what makes both practical; neither is done by this skill.

`Structure: pattern-mining (infer the rule from repeated instances) + documentation harvest + inconsistency-as-question (ask, never pick) + faceted classification (area × bounded-context) + per-area discipline models (Atomic Design / ANSI-SPARC / Clean Architecture / Richardson / OWASP ASVS / test pyramid / three pillars). Harvest-not-invent + visual/interaction scope + two-level ordering = house method.`

This block is the only way to close on the happy path. **Only exceptions**: Phase 0 read-only stance; a blocking inconsistency ruling (Phase 2) or an ambiguous-placement question (Phase 3-bis) → the single question allowed before writing.

> **Canonical structural-labels rule — single source of truth.** Apply `_shared/mala-pata-structural-labels.md` verbatim; it supersedes any restatement in this skill. Do not paraphrase or re-derive it.
**Frozen close labels** — title `Standard ready`; BLUF label `Standard:`; readback columns `Area` · `Status` · `Evidence`; Status tokens `approved` · `proposed` · `OPEN`; block labels `OPEN`, `Files`, `Next step`, `Structure`. Emit them verbatim in English even when the conversation is in another language; only the values are localized.

## What it does NOT do (invariants)

- Does NOT invent or import a standard — it harvests what the project already does, from code AND docs.
- Does NOT prefer one source silently — a code-vs-docs disagreement is an inconsistency it asks about.
- Does NOT pick a winner on an inconsistency — it asks the human and captures the ruling (or leaves it `OPEN`).
- Does NOT admit a rule as a standard on inference alone — nothing is `approved` without the human's explicit per-rule YES (candidates stay `proposed`).
- Does NOT lose a rule when reorganizing — every existing rule lands in the new structure with its status/evidence/provenance intact; ambiguous placement is asked.
- Does NOT change code, restyle, or fix the inconsistencies — that is a lane's job, not this skill's.
- Does NOT capture code/structural conventions in v1 — only visual + interaction/layout; the structural areas exist as reserved slots.
- Does NOT rewire or broaden the consumers — (a) re-pathing the 3 current consumers (`/mala-pata-art` / `/mala-pata-research` / `/mala-pata-triage`) to the new structure and (b) extending grounding to the rest of the suite are separate changes it only flags.
- Does NOT commit — write-only; the human commits in their PR flow.

## Relation to the family

- **Feeds** `/mala-pata-art` (which judges/applies the VISUAL standard but assumes it exists — this skill is what CAPTURES it) and `/mala-pata-research` (which grounds a vague DoD against the captured standard so it becomes deterministic). The lanes conform to it. The ordered structure is what makes broad consumption practical — the whole suite should ground against it, not just three skills.
- **Different from** `/mala-pata-art` — art is visual JUDGMENT (how to improve a given artefact); standards is CAPTURE + ORDER (what the project's standard IS and where each rule lives). Capture first, judge/apply after.
- **Indexed by** `/mala-pata-domain-radar` (reads the `domain:` frontmatter, like the other mala-pata artifacts).
- It is a capture/doc-authoring skill, orthogonal to the lanes (`shot`/`organic`/`loop`/`roadmap`), not a route.
