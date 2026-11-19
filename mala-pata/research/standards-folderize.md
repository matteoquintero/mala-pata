---
idea_slug: standards-folderize
project: mala-pata-skills
domain: mala-pata-standards
roadmap: none
verdict: PROCEED
created_at: 2026-11-19T13:31:23-0500
next: none
size_signal: one-unit
kind: research
---
# Research: a scalable ORDER for mala-pata's captured standard (strategy)

> **This is a STRATEGY research, not a routed change.** The deliverable is the ordering model itself. It does NOT need `/mala-pata-triage` or `/mala-pata-organic` now — when you decide to adopt it, implementing it in `mala-pata-standards` is a separate, deliberate change at your discretion. (Re-run deepening two earlier passes: the first over-narrowed to ui/arch/db and over-indexed on routing; the second found the faceted backbone but left each AREA as an empty folder. This pass gives each area its own internal structuring model — "the idea is order", at both levels.)

## Verdict: PROCEED
The right strategy for "order that scales" is a **TWO-LEVEL model**, not a flat folder list:
1. **Cross-area (the spine):** **faceted classification** — an OPEN set of areas × bounded-context (`domain`), each facet small and flat, extensible by post-coordination.
2. **Within each area (the depth):** **every area carries its OWN recognized internal structuring model** of its discipline — its "atomic design". An area is never a bare folder with loose files; it ships the canonical sub-taxonomy of its field (ui → atomic design, data → ANSI-SPARC three-schema, architecture → Clean/Hexagonal, api → Richardson, security → OWASP ASVS, …).

A single tree, a fixed 4-category scheme, OR a faceted spine with hollow areas all break: breadth grows (many areas) and depth grows (each area decomposes into many things). The two-level model holds both because every level stays narrow and each area inherits a battle-tested order instead of inventing one.

## Raw idea (what you asked)
The standard today is one flat `.md` and that's it. It needs real ORDER — "mala-pata structures" (structure-mala-pata), not just ui/architecture/db. A project can have a standard of MANY things, and even "ui" alone decomposes into many things. **Each AREA must have its own structure-mala-pata support, like ui has atomic design** — "separar por áreas no es orden". And atomic design itself was incomplete: it needs **templates and pages**. **The idea is order** (that scales), at both levels — researched as a strategy, not a rush to route or execute.

**Objective:** a captured standard that stays **ordered, navigable and extensible** no matter how many areas it covers or how deep any single area goes — where each area is internally ordered by the recognized model of its own discipline, not left as a loose bag of files.

## Discover

### How it's done today + limits — the authoritative strategies (with sources)

**Level-1 backbone (cross-area):**
1. **Faceted classification — the spine for scale** ([Wikipedia](https://en.wikipedia.org/wiki/Faceted_classification), [Semantic Studios](http://semanticstudios.com/the_speed_of_information_architecture/), [faceted IA framework (ResearchGate)](https://www.researchgate.net/publication/220677046_Faceted_classification_in_web_information_architecture_A_framework_for_using_semantic_web_tools)): organize along SEVERAL independent dimensions (facets) instead of one big tree. Each facet covers one narrow dimension, so its hierarchy stays **small and flat**; a handful of terms **post-coordinate** into many combinations → **compact, clear, scalable**. It **separates the classification from the interface**, so layers change at different rates. Caveat: more labor-intensive to design than a single tree — the up-front taxonomy work is the cost.
2. **DDD bounded context** (Evans): the **WHERE** dimension — which part of the system a rule governs. A facet, orthogonal to the area facet.

**Level-2 per-area models (each area's "atomic design") — grounded in each discipline's authoritative source:**
3. **ui → Atomic Design + design tokens** ([Brad Frost](https://atomicdesign.bradfrost.com/chapter-2/), [sanity.io](https://www.sanity.io/glossary/atomic-design), [UAL tokens](https://www.arts.ac.uk/design-system/foundations/design-tokens)): foundations (tokens, primitive vs semantic) → atoms → molecules → organisms → **templates → pages**, plus cross-cutting patterns and a11y. Templates (page skeletons, no real content) and pages (templates with real content) are the two levels the earlier pass dropped — they are what make the model end-to-end.
4. **data → ANSI-SPARC three-schema + DAMA-DMBOK** ([three-schema](https://www.relationaldbdesign.com/database-design/module3/three-schema-architecture.php), [DAMA logical-model mapping](https://journal.intelligenceds.com/articles/logical-data-model-bridge.html)): conceptual (entities + relationships / ERD) → logical (normalized keys, attributes, types — engine-agnostic) → physical (tables, indexes, partitions), plus naming, migrations, integrity.
5. **architecture → Clean / Hexagonal (ports & adapters)** ([Clean Architecture dependency rule](https://www.cubic.dev/blog/how-to-maintain-clean-architecture-with-dependency-rules-in-your-codebase), [ports & adapters overview](https://vamsilabs.netlify.app/misc/clean-architecture/)): entities (enterprise rules) → use-cases (application rules) → interface-adapters (controllers/presenters/gateways) → frameworks-drivers (db/ui/external), governed by the dependency rule (inward-only) and bounded contexts.
6. **api → Richardson Maturity Model** ([Richardson Maturity Model (Wikipedia)](https://en.wikipedia.org/wiki/Richardson_Maturity_Model), [devopedia](https://devopedia.org/richardson-maturity-model)): resources + URIs (L1) → HTTP methods + status codes (L2) → HATEOAS (L3), plus contracts (OpenAPI schemas), errors, versioning, pagination/filtering, auth.
7. **security → OWASP ASVS chapters** ([OWASP ASVS (OWASP DevGuide)](https://devguide.owasp.org/en/03-requirements/05-asvs/), [arc42 ASVS note](https://quality.arc42.org/standards/owasp-asvs)): authentication, session, authorization (access control), validation, crypto, data-protection, logging — with verification levels L1/L2/L3.
8. **testing → test pyramid**, **observability → three pillars (logs/metrics/traces)**, **content → voice/microcopy/terminology/i18n**, **conventions → naming/folders/git-PR/lint**: each the recognized model of its discipline; where a discipline has no single canonical model, mala-pata defines a small flat sub-facet set the same way.

### What exists in the code (real anchoring)
- `mala-pata-standards` v0.2.0 writes **one flat md per domain** (`mala-pata/standards/<domain>.md`; real: `filtros.md`, `mvp-2026.md`) with a FIXED flat section order. It already partitions by **`domain`** — that IS the bounded-context facet. What is flat (unstructured) is the **concern/area** dimension inside a domain, AND, even once areas exist, the INSIDE of each area.
- v1 scope = visual + interaction only; **structural (naming, architecture, data) is a named FUTURE layer, out of v1**. So the ordering model must be able to HOLD areas v1 does not yet fill — reserve slots (and their internal models), don't hardcode.
- Per-rule status `approved`/`proposed`/`OPEN` + evidence is orthogonal to WHERE a rule lives — it must survive any restructure, at both levels.
- Consumers read the file path. Today only 3 skills wire it — `mala-pata-art`, `mala-pata-research`, `mala-pata-triage` (verified by grep over the live skills) — but that is who consumes it NOW, not who SHOULD: the captured standard is the project's ground truth for how things are done, so nearly the whole suite should ground against it (the `organic`/`loop`/`shot` lanes for a deterministic DoD, `walkthrough`, `states`, `roadmap`, …). That only 3 consume it today is exactly the limitation — a flat md is not resolvable. A two-level structure changes resolution for every consumer (an `_index.md`/convention is needed) and is what makes broad consumption practical — but that is the ADOPTION step, not this research.

### Jobs-to-be-done
As the suite owner, I need a captured standard that **stays ordered as it grows in any direction**, where each area is internally organized by the recognized model of its discipline — so a human (and every grounding skill) finds "the modal rule" / "the migration-naming rule" / "the resource-URI rule" / "the token" fast, and new areas slot in already-ordered (they bring their discipline's model) instead of as a loose bag of files.

### Problem dimension
- **Scope**: the ordering MODEL governs every captured standard across every project + area — broad, foundational. [noted]
- **Frequency**: felt every time a standard gains an area or an area gains depth. [inferred]
- **Severity**: medium — the flat md is survivable while small, but caps how far the standard scales and how usable grounding stays; "folder-per-area with loose files" would only move the disorder one level down. The pain is structural, not acute. [inferred]

### Problem vs proposed solution (reframed)
| Piece | Class | Note |
|---|---|---|
| A FIXED list "ui / architecture / database" | **derivable/extra, do NOT hardcode** | too narrow; a project has many more areas. The fix is an OPEN faceted set, not 4 folders. |
| Order that scales across areas | necessary | → faceted classification (the Level-1 spine). |
| An area = just a folder with loose files | **wrong frame** | "separar por áreas no es orden". Each area needs its OWN internal model → Level-2. |
| Each area's internal order | necessary | → the recognized discipline model per area (ui=atomic design incl. templates+pages, data=ANSI-SPARC, architecture=Clean/Hexagonal, api=Richardson, security=OWASP ASVS, …). |
| The "where" axis | already-exists | the `domain` partition is the bounded-context facet. |
| Per-rule approval + status | keep (orthogonal) | lives on the rule, not the folder — at both levels. |

## The proposed ORDER (the strategy's output) — TWO LEVELS

### Level 1 — the cross-area spine (faceted)
- **Facet A — AREA (open, extensible set):** mala-pata ships a recommended catalog + a rule for adding a new area; projects add to it. NOT a closed list of 4.
- **Facet B — BOUNDED CONTEXT (`domain`, already present):** which part of the system the area's rules govern — carried as a frontmatter facet on each leaf (`global | compras | devolucion`), it does NOT duplicate the tree.

### Level 2 — each area carries its OWN internal model (the structure-mala-pata catalog)
The rule of mala-pata: **an area is never an empty folder — it brings the recognized internal structuring model of its discipline.** A new area is added by **declaring its internal model**: if the discipline has a canonical one, use it; if not, define a small flat sub-facet set the same way.

| Area | Internal model (its "atomic design") | Sub-structure | Source |
|---|---|---|---|
| **ui** | Atomic Design + tokens | foundations(tokens) → atoms → molecules → organisms → **templates → pages** · patterns · a11y | Frost; design-system IA |
| **data** | ANSI-SPARC three-schema | conceptual → logical → physical · naming · migrations · integrity | ANSI-SPARC; DAMA-DMBOK |
| **architecture** | Clean / Hexagonal (rings) | entities → use-cases → interface-adapters → frameworks-drivers · dependency-rule · bounded-contexts | Martin (Clean Arch); Cockburn (ports & adapters) |
| **api** | Richardson Maturity Model | resources → methods+status → contracts · errors · versioning · pagination-filtering · auth | Richardson/Fowler |
| **security** | OWASP ASVS (chapters) | authentication · session · authorization · validation · crypto · data-protection · logging | OWASP ASVS |
| **testing** | Test pyramid | unit · integration · e2e · fixtures-factories · coverage | Cohn (test pyramid) |
| **content** | voice/microcopy model | voice-and-tone · microcopy · terminology · i18n | discipline-standard |
| **observability** | Three pillars | logs · metrics · traces | three-pillars (OTel) |
| **conventions** | code/structural | naming · folder-architecture · git-and-pr · lint-format | discipline-standard |

### The complete tree (every area decomposed by ITS model)
```
mala-pata/standards/
├── _index.md                       ← the area catalog + each area's internal model + how to add a new area
│
├── ui/                             ← Atomic Design + tokens
│   ├── _index.md
│   ├── foundations/   color.md · typography.md · spacing.md · radius.md · elevation.md · motion.md
│   ├── atoms/         button.md · input.md · icon.md · label.md · badge.md
│   ├── molecules/     search-field.md · form-row.md · menu-item.md
│   ├── organisms/     header.md · filters-panel.md · data-table.md
│   ├── templates/     list-page.md · detail-page.md
│   ├── pages/         <canonical screens: real template + real content>
│   ├── patterns/      forms.md · empty-state.md · pagination.md · notifications.md
│   └── a11y/          focus-and-aria.md · contrast.md · keyboard.md
│
├── data/                           ← ANSI-SPARC (conceptual → logical → physical)
│   ├── _index.md
│   ├── conceptual/   entities.md · relationships.md
│   ├── logical/      keys-and-attributes.md · normalization.md
│   ├── physical/     tables.md · indexes.md · partitioning.md
│   ├── naming.md · migrations.md · integrity.md
│
├── architecture/                   ← Clean / Hexagonal (rings + dependency rule)
│   ├── _index.md
│   ├── entities/            domain-rules.md
│   ├── use-cases/           application-rules.md
│   ├── interface-adapters/  controllers.md · presenters.md · gateways.md
│   ├── frameworks-drivers/  db.md · web.md · external.md
│   ├── dependency-rule.md · bounded-contexts.md
│
├── api/                            ← Richardson Maturity Model
│   ├── _index.md
│   ├── resources/    resource-model.md · uris.md
│   ├── methods-status.md · contracts/ · errors.md · versioning.md · pagination-filtering.md · auth.md
│
├── security/                       ← OWASP ASVS
│   ├── _index.md
│   ├── authentication.md · session.md · authorization.md · validation.md · crypto.md · data-protection.md · logging.md
│
├── testing/      unit.md · integration.md · e2e.md · fixtures-factories.md · coverage.md   ← test pyramid
├── content/      voice-and-tone.md · microcopy.md · terminology.md · i18n.md
├── observability/ logs.md · metrics.md · traces.md                                          ← three pillars
└── conventions/  naming.md · folder-architecture.md · git-and-pr.md · lint-format.md
```

- **Container:** a folder tree `mala-pata/standards/<domain>/<area>/<sub-facet>.md` with an **`_index.md`** per level (so consumers resolve it), OR frontmatter-faceted files — the adoption decides; either keeps each facet small and flat. The per-rule `approved/proposed/OPEN` + evidence stays on each rule.
- **Extensibility (the whole point):** a new area = a new slot that ARRIVES ordered (it declares its internal model); a new sub-facet = a new leaf inside an area's model. Both are post-coordinated, no reshape of the rest. Order scales with breadth (areas) AND depth (each area's model) because every facet stays narrow.

### Why the two-level model beats the alternatives
- **Single tree by concern** (one deep hierarchy): rots like the flat md once two dimensions (area × where) fight for one tree.
- **Fixed list (ui/arch/db)**: breaks at the 5th area, and says nothing about depth inside an area.
- **Bounded-context only** (`domain`, as today): leaves each domain internally unordered → the disorganization you flagged.
- **Faceted spine with HOLLOW areas** (the previous pass): fixes breadth but leaves each area a loose bag of files — "separar por áreas no es orden". The fix is Level 2.
- **Atomic design only**: solves ui depth but is ui-specific; it is ONE area's internal model, not the whole scheme.
The two-level model subsumes all of them: faceted spine for breadth (areas × domain) + a recognized discipline model inside each area for depth, with templates+pages completing the ui case.

## Heilmeier Catechism
| # | Question | Answer | Provenance |
|---|---|---|---|
| 1 | What are you trying to do? | Define mala-pata's ordering model for captured standards so they scale in breadth (areas) and depth (each area's internal model) without disorder. | [noted] |
| 2 | How is it done today + limits? | One flat md per domain; flat concern axis; no per-area internal order; structural areas out of v1. | [verified] |
| 3 | What is new + why it works? | Two-level model: faceted spine (area × bounded-context) + each area carrying its discipline's recognized internal model (ui=atomic design incl. templates/pages, data=ANSI-SPARC, architecture=Clean/Hexagonal, api=Richardson, security=OWASP ASVS). Each level stays narrow → it scales. | [noted + sourced] |
| 4 | Who cares? | The suite owner + every grounding skill; the value grows with the standard's size and depth. | [assumed] |
| 5 | Risks? | Up-front taxonomy design cost (now at two levels); the adoption changes the consumer path contract. | [noted] |
| 6 | Cost / time? | The STRATEGY is this doc (done). Adopting it = a later, deliberate change to `mala-pata-standards` + re-pathing its 3 current consumers AND extending grounding to the rest of the suite. | [noted] |
| 7 | Exams of success? | Any project standard, however broad/deep, lands in the two-level structure; each area is internally ordered by its discipline's model; a human finds any rule fast; new areas arrive ordered; status model preserved. | [noted] |

**Assumption challenge:** "folderize into ui/architecture/db" AND "one folder per area is enough" are both wrong frames — the first conflates the area facet with the where facet and assumes a closed list; the second leaves each area internally unordered. The evidence says the scalable answer is a faceted spine with an OPEN area set AND a recognized internal model per area. That two-level reframing is this research's contribution.

## Define — the strategy (no routing)
- **What:** adopt the two-level ordering model for captured standards — Level 1 faceted (area × bounded-context, open/extensible), Level 2 each area carrying its discipline's recognized internal model.
- **Why:** flat md does not scale, and a folder-per-area with loose files only moves the disorder down one level.
- **The model:** as in "The proposed ORDER" above (catalog + complete tree).
- **Decisions settled by the research:** two-level over single-tree / fixed-list / bounded-context-only / hollow-faceted; `domain` = the bounded-context facet; the per-area internal models (ui=atomic design incl. templates+pages, data=ANSI-SPARC, architecture=Clean/Hexagonal, api=Richardson, security=OWASP ASVS, testing=pyramid, observability=three pillars); per-rule status stays orthogonal.
- **Left for adoption (not research):** the concrete container (folder tree vs frontmatter facets), the starter area catalog's exact entries and each area's exact sub-facet leaves, the consumer resolution convention (`_index.md`), re-pathing the 3 current consumers AND broadening consumption to the rest of the suite that should ground against it, migration of `filtros.md`/`mvp-2026.md`, and whether adoption opens the structural areas now.
- **Size signal:** one-unit as a STRATEGY (this doc). Adoption later is its own change, sized then.

## Next step (per your call — NOT triage)
This research IS the deliverable. When you want it built, it becomes a deliberate change to `mala-pata-standards` + re-pathing its current consumers and broadening consumption to the rest of the suite (your decision, a separate moment) — not a lane routed now.

Structure: faceted classification (Ranganathan / IA) + DDD bounded context (Evans) for the spine; per-area discipline models — Atomic Design (Frost) + design tokens, ANSI-SPARC three-schema + DAMA-DMBOK, Clean Architecture (Martin) + ports & adapters (Cockburn), Richardson Maturity Model (Richardson/Fowler), OWASP ASVS, test pyramid (Cohn), three pillars of observability — + Heilmeier Catechism (DARPA) + Double Diamond (Design Council). Two-level ordering / structure-mala-pata-per-area = house method.
