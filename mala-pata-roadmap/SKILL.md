---
name: mala-pata-roadmap
description: >
  Planning layer ABOVE the lanes (organic/loop), routed by /mala-pata-triage.
  Receives ONE large objective, analyzes it, researches how it is solved (web + how the big players
  do it), reads the project's .codegraph/ to anchor it to the real code, asks questions if context
  is missing, and breaks it down into a DAG of unit-sized phases (each phase = a shippable vertical
  slice that fits in ONE unit: one organic or one loop). Each phase gets a TENTATIVE ROUTE
  (organic, loop:PROFILE or shot) as an approximation — but triage is the one that decides on arrival,
  with the information already updated by the previous phases. Writes a versionable roadmap .md in
  the repo. It does NOT execute, does NOT run any lane, does NOT touch code: it only produces the
  phase map that you then pass one by one to /mala-pata-triage.
  Trigger — "roadmap de <objetivo>", "descomponé este objetivo grande", "armá el plan de fases",
  or any objective too large for a single unit.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "2.11.0"
---

# /mala-pata-roadmap — large objective → DAG of unit-sized phases (organic or loop)

User objective: **input delivered by the CLI**

Your job: turn a LARGE objective into a **DAG of phases**, where each phase is so small that it
fits in **ONE unit** — one `/mala-pata-organic` or one `/mala-pata-loop`. You assign each phase a
**tentative route** (organic, loop or shot) as an approximation. You produce a `.md` with that roadmap and **nothing
else** — you do not write code, you do not run any lane, you do not apply. Afterwards the human takes each phase and
passes it to `/mala-pata-triage`, which decides the final lane with the information of the moment.

> **Hard rule #1 — you execute NOTHING.** Not code, not migrations, you do not run `/mala-pata-triage`,
> `/mala-pata-loop` or `/mala-pata-organic`. Your only deliverable is the roadmap `.md` (+ a pointer in
> engram). The DAG is a plan, not an order to implement.
>
> **Hard rule #2 — if the objective ALREADY fits in ONE unit, do NOT invent phases.** If on analyzing it
> you see it is a change that fits in a single organic or a single loop, **STOP and redirect to
> `/mala-pata-triage`** — it decides the lane. This skill is only for objectives that do NOT fit in a
> single unit. Over-decomposing something small is the anti-pattern this skill must avoid.
>
> **Hard rule #3 — the route per phase is a FORECAST, not a commitment.** You classify each phase
> as organic or loop with your best reading of TODAY, but **triage re-decides on arrival** (see Step 4-bis):
> previous phases resolve unknowns, so a phase forecast as loop may become organic
> (or the other way around). You forecast; triage rules.

## Requirements (orchestrate, don't reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Required**: none.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded):
  - `codegraph` — code graph (anchoring and structure). Fallback: grep. Install: global npm CLI; per-project init with `gentle-ai codegraph init --cwd <repo>`.
  - `serena` — symbol-level navigation and editing. Fallback: codegraph/grep. Install: `uv tool install -p 3.13 serena-agent && serena setup claude-code`.
  - `WebSearch/WebFetch` — external research. Fallback: disclose that there is no external research. Install: not required (native client tools).

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP, e.g. serena). If a required one is missing, do not continue.

## Step 0 — Does it merit a roadmap? (size + vagueness gate)

- **Research doc first**: if the input is a slug (or path) that resolves to an existing `mala-pata/research/<slug>.md`, `Read` it and use its Define fields and findings as the objective's starting context instead of only the raw text.

- **Is it big enough?** If the objective fits in ONE unit (one organic or one loop) → Hard rule
  #2 (redirect to `/mala-pata-triage`).
- **Is it clear enough to decompose?** You need to infer **what** is to be achieved, **for
  whom/where** (module/domain) and **what success looks like**. If the object itself is missing ("improve the
  app") → ask for the minimum and wait; do not invent scope.
- Recoverable (1-2 pieces of data missing) → ask concrete questions and wait. This is the question gate.

## Step 1 — Define the DESIRED STATE: the dimensions of the complete objective

The roadmap's goal is NOT to cover what the human LISTED — it is to cover what the objective NEEDS.
The request almost always ends up incomplete; your job is to close the gap. **Bias: better too much,
than too little.** There are two symmetric errors to avoid:

**Shrinking to what is easy to measure** — anchoring on the first inventory the code lets you grep
(a metric, a report) and planning only that facet.
**Covering only what the human said** — the request is incomplete by default; if you do not look for what
is missing, the human ends up discovering it in production.

Define the **desired state** (the COMPLETE objective) by joining THREE sources:

1. **What the human said** — re-read the literal objective, list each facet. What "types of thing"
   does it span? What does "all / any / complete" imply?
2. **What the DOMAIN needs** (external research, Step 2.3) — the **canonical feature-set** of
   how mature teams solve this kind of objective. It is the anti-forgetting net (domain checklist,
   ISO/IEC 25010 style for software). In **two levels** (see Step 4-ter): *adjacent-implied* (what
   completes or directly implies what was asked) vs *broad domain* (the rest of the domain's universe).
3. **What the repo's intent docs ALREADY anticipate** — read the architecture/intent documentation
   that exists, **wherever it is** (`CLAUDE.md`, `ARCHITECTURE.md`, READMEs, RFCs, design notes). Do NOT
   assume a fixed folder; if the repo has documented pending items, they are often gaps the human forgot.

Also express the objective as **jobs-to-be-done** ("as <user>, I need <job> in order to <benefit>"):
it catches user-facing gaps that the feature list does not show (e.g. a screen that is needed and
nobody named).

**MECE check + 100% rule**: the set of dimensions must be *mutually exclusive* (no overlap) and
*collectively exhaustive* (covers the WHOLE objective, no gaps). If it is not exhaustive, dimensions are
missing — keep looking. This is the check that forces completeness.

This list of dimensions is the **coverage contract** against which the DAG is measured (Step 5). If the
objective turns out to be enormous, do NOT assume it all goes in one roadmap: at the gate (Step 5) you offer scope. You
do not narrow it silently.

## Step 2 — Inventory EACH dimension + research + anchor to the real code

In parallel, without writing anything. **Inventory ALL the dimensions of Step 1, not just the easy one:**

1. **Active project**: detect the repo/cwd and read its architecture (`CLAUDE.md`, `ARCHITECTURE.md`,
   or equivalents). `mem_search` for related prior work.
2. **.codegraph/ + per-dimension inventory**: if the project has an index, use `codegraph_explore`
   (or CodeGraph's read-only commands) to map modules, symbols and dependencies. Run an
   inventory for EACH dimension of Step 1 (what already exists, what is raw, how much), not just for the
   one you grep in a single command. If a dimension cannot be measured by code (e.g. an inventory of a
   kind of artifact that has no unique marker), say so explicitly and estimate — do not delete it from the map.
   If there is no `.codegraph/`, map with Read/Grep/Glob the minimum needed to understand the real seams.
3. **External research** (WebSearch/WebFetch): the domain's **canonical feature-set** — how
   mature teams solve it, what known patterns/mistakes exist. Separate it into **two levels**:
   *adjacent-implied* (completes/implies what was asked) and *broad domain* (the rest). **Anchor what you bring
   to YOUR code** — a best practice that ignores what already exists is useless (reuse-first, same as preview).
4. **Questions**: if after this there remain open decisions that change the shape of the DAG —
   including any dimension you could not inventory well — ask BEFORE decomposing
   (do not resolve it by guessing). Include here the **product/scale decisions** (who uses it, at
   what scale, which model) that reshape the DAG: ask them yourself, proactively, do not wait for
   the human to offer them — a single one of those can collapse half a roadmap.

## Step 3 — Architecture pass BEFORE decomposing

Before cutting into phases, define the **real seams** along which the work will split
(interfaces, modules, data boundaries), anchored to the `.codegraph/` of Step 2. This is what makes
the phases come out along clean edges and not along arbitrary themes — the lesson from planners that
decompose without an architecture view and end up with phases that are not shippable on their own.

## Step 4 — Decompose into a DAG of phases

Produce the phase graph with these rules (all of them, none optional):

- **The DAG must COVER all the dimensions of Step 1**, not just the easiest one to measure. Each
  dimension appears covered by at least one phase, or is explicitly marked as deferred / out of scope
  (for the Step 5 gate). Never leave a dimension out without naming it.

- **Each phase is a shippable VERTICAL slice** — an end-to-end slice that leaves the system
  working, not a horizontal layer ("the whole DB", "the whole UI"). If the phase cannot be merged
  and stay green on its own, it is not a valid phase.
- **Each phase receives a TENTATIVE ROUTE, with the triage border** (triage's gate):
  - Can the phase's **What + Done + Decisions** be stated, given what its dependencies will already
    have resolved by the time its turn comes? → tentative **organic** (or **shot** if it is also trivial:
    1-3 files, no migration/contract/new UI).
  - Is a decision still open? **Distinguish before marking loop** (not "there is a decision → loop"):
    - **Decidable with a question** (known options, the human chooses) → NOT loop: tentative
      **organic**, and note the question triage will ask on arrival to close it.
    - **Needs design** (viable architectures with tradeoffs to investigate, or options that
      cannot be known without exploring) → tentative **loop:PROFILE** (FULL/STANDARD/LITE/MINIMAL).
  - For each loop phase, note **which design decision** makes it loop — it is what triage re-checks
    on arrival (if it is already resolved, the phase becomes organic).
- **The hard CEILING of size is "fits in ONE unit".** A `loop:FULL` is the ceiling of a
  loop phase; an organic phase fits if the change is already specifiable. **If a phase would be larger
  than a FULL → it is SPLIT.** No exception.
- **The split trigger is COMPLEXITY / CONTEXT ISOLATION, not lines.** The "does it fit in a unit?"
  test is: does this phase's context isolate cleanly from the rest? If to understand
  or do the phase you need to load the context of half of another phase, it is still too big.
- **Each node carries an EXPLICIT IN / OUT border** — what goes in and what stays out — so that two
  phases do not step on each other or duplicate work.
- **Dependencies as a DAG**: each phase declares which other phases it depends on. The graph has no cycles.
  Give the suggested topological order (what can be done in parallel, what is sequential).
- **Anti-over-decomposition**: the FEWEST phases possible on the condition that each one
  fits in a unit. Not 40 micro-phases; not one giant phase. If you hesitate between 3 large phases or 8
  small ones, choose the minimum that respects the ceiling (loop:FULL) and context isolation.

## Step 4-bis — Tentative route vs triage decision (contract)

The route you assign to each phase (organic, loop or shot) is an **approximation with TODAY's info**, not a
commitment. The truth is decided at EXECUTION:

- As the roadmap advances, **each phase is passed through `/mala-pata-triage`** (not directly to a lane).
  Triage applies its gate with the CURRENT info of the repo and of the phases already completed.
- Since previous phases **resolve unknowns** (an architecture decision made in phase A
  may close the one phase D had open), a phase forecast as **loop** may arrive as
  **organic** — or one that looked organic may reveal complexity and become **loop**.
- That is why each loop phase declares **the open decision that makes it loop**: it is exactly what
  triage re-checks. If that decision is already resolved on arrival, triage sends it to organic.
- **The roadmap forecasts; triage rules.** Do not treat the tentative route as fixed and do not skip triage
  "because the roadmap already said loop".

## Step 4-ter — Gap analysis: validate that the DAG covers the complete objective

The roadmap **OVER-discovers and proposes; the human TRIMS** at the gate. Never the other way around (the human
discovering what was missing). Do the gap analysis:

- **Desired state** (Step 1: human + domain + intent docs, MECE) **vs current state** (what the
  code already solves, measured in Step 2 with codegraph) = **the gap**. The gap is what the roadmap has to
  cover with phases.
- Every dimension of the desired state that the human did **NOT request** but the objective implies → is marked as
  **extra-proposal** (not as something you decided alone). **Never add it silently nor discard it
  silently**: it goes to the gate marked.
- **Two levels of proposal** (breadth of the domain source, resolved):
  - **Level 1 — core + adjacent-implied**: dimensions the objective NEEDS or directly implies
    → become **candidate phases** in the DAG (marked extra-proposal if the human did not
    request them).
  - **Level 2 — broad domain**: the rest of the domain's canonical feature-set → **does NOT inflate the DAG**; it is
    listed **compactly as a checklist** ("exists in the domain, this roadmap does NOT cover it") so the human
    can mark whether something gets promoted to a phase. Nothing is hidden, but it does not become a phase by default.
- Take advantage of what the code ALREADY has to enable more than the human imagined (e.g. already
  installed infrastructure that opens up a capability): that is also a gap worth proposing.

## Step 5 — Coverage gate + human gate of the DAG

Before asking for OK, validate **MECE** over the dimensions (no overlaps, no gaps) and show the **MANDATORY
coverage table**: **each axis of the desired state (Step 1) appears in the table with EXACTLY ONE
status.** No axis can be missing nor "slip" into Level 2 without being mapped first — an axis of the desired state
that is not in the table is a **silent drop** (the gate fails). **Hard check: number of axes in the table
== number of axes in Step 1.**

Possible statuses per axis:
- **covered** → the phase(s) that cover it.
- **extra-proposal** → the phase(s); the human did not request it but the objective implies it.
- **deferred** → with reason (or "separate roadmap").
- **→ Level 2** → with reason: it is an axis of the desired state that is decided to be left in the broad-domain checklist,
  NOT one that disappears. It must appear here **AND** in the Level 2 list below.

```
Objective coverage (desired state → DAG) — ALL the axes of Step 1, one per line:
- Axis 1 <name> → Phases 1, 3        [covered]
- Axis 2 <name> → Phase 4            [covered]
- Axis 3 <name> → Phase 7            [EXTRA-PROPOSAL — you didn't ask for it; the objective implies it]
- Axis 4 <name> → DEFERRED (reason) / separate roadmap
- Axis 5 <name> → Level 2 (reason)   [stays as a checklist, not as a phase]
(… one line for EACH axis of Step 1, no exception — the count must match)

Level 2 — broad domain NOT covered (checklist, mark whether something gets promoted to a phase):
- [ ] <domain capability 1>   - [ ] <domain capability 2>   - [ ] …
```

The human signs off on what stays inside (including the extra-proposals), what is deferred, and whether anything from Level 2
(or an axis sent to Level 2) gets promoted to a phase. **You propose too much; the human trims.**

If the objective is enormous (several large dimensions), explicitly offer the scope decision:
**(a)** a multi-dimension roadmap (all of them), or **(b)** narrow this roadmap to one/some dimensions and
the others in separate roadmaps. The human chooses the scope; you do not decide it alone.

**Before asking for OK, show the decision block (MANDATORY — it is what lets over-sizing get caught):**
- **Core vs complete**: it comes DIRECTLY from the `Deferrable?` column of the table — the **core** is the phases with `Deferrable? = no`; the **complete** is all of them. Do not recompute it: read the column. If the core is 1 phase and the DAG has 5, say so explicitly.
- **Magnitude of the problem**: scope / frequency / severity (from research's "Problem dimension"; if it did not come, measure it here). A small problem with a large DAG is the alarm signal.
- **Cheapest workaround**: the known minimal alternative (an already-existing tweak, a one-line fix) and its cost, even if it is not the "complete" solution. If it exists, the human has to see it BEFORE approving N phases.

Then present the DAG (phases, **tentative routes** organic/loop, dependencies, order) and **wait for OK
before writing the `.md`**. Options: **Approve** (you write the roadmap with the confirmed scope),
**Adjust** (the human corrects dimensions/phases/routes/borders/order/scope and you re-present), **Stop**.
Do not write without approval.

**Emit every structural label verbatim in English** — in BOTH this Step-5 gate presentation and the written `.md`: section headers (`Objective coverage`, `Level 2 — broad domain not covered`, `Large objective`, `Architecture / seams`, `Context and research`, `DAG of phases`, `Phases in detail`), the decision-block labels (`Core vs complete`, `Magnitude of the problem`, `Cheapest workaround`), the order line labels (`Suggested order`, `Parallelizable`), and the table columns (`Phase`, `slug`, `Tentative route`, `Depends on`, `Deferrable?`). Parallelism in the order line uses `//` (e.g. `2 // 3`), not a Unicode symbol. Only the values and content follow the user's language; the labels are never localized.

## Step 6 — Where to save + write the roadmap

1. **Ask where to save it**, suggesting the default **`mala-pata/roadmap/<slug>.md`**
   (inside the repo under `mala-pata/roadmap/`, versioned — like the rest of the mala-pata artifacts). Allow override.
2. Write the `.md` with the format below (absolute paths to operate; `mkdir -p` the folder). Populate `## Objective coverage` (one row per axis, status as approved at the Step-5 gate) and `## Level 2 — broad domain not covered` (the Level-2 checklist) from the Step-5 result — they are persisted so `/mala-pata-gaps` can read them.
3. **Light pointer in engram** for discoverability: `mem_save` topic_key `sdd/<slug>/roadmap`,
   one-line content `Roadmap in file: <absolute path>`. Do not duplicate the content.
4. Respond with the file path + the suggested order of phases to pass to `/mala-pata-triage`.

### Roadmap `.md` format

```markdown
---
objective: <short title of the large objective>
slug: <kebab-case>
project: <project>
created_at: <ISO 8601>
phases_total: <N>
---

# Roadmap: <objective>

## Large objective
<what is to be achieved, for whom/where, what success looks like — measurable>

## Architecture / seams (Step 3)
<the real borders along which the work splits, anchored to .codegraph/ — modules/interfaces/data>

## Context and research
<relevant findings: how this is solved / patterns / what to reuse from the repo — with refs>

## DAG of phases

| # | Phase | slug | Tentative route | Depends on | Deferrable? | Vertical slice (one line) |
|---|-------|------|-----------------|-----------|-------------|----------------------------|
| 1 | <name> | <stable-kebab> | loop:STANDARD | — | no (core) | <what it delivers end-to-end> |
| 2 | <name> | <stable-kebab> | organic | 1 | yes | ... |
| 4 | <name> | <stable-kebab> | shot | — | yes | ... |
| 3 | <name> | <stable-kebab> | loop:LITE | 1 | yes | ... |

> **Tentative route = forecast.** On execution, each phase is passed through `/mala-pata-triage`, which
> re-decides shot/organic/loop with the information of the moment (see Step 4-bis). Previous phases may change
> the route of a later one.

Suggested order (topological): 1 → (2 // 3) → …   ·   Parallelizable: {2, 3}

## Objective coverage

| Axis (desired state) | Status | Phases / reason |
|----------------------|--------|-----------------|
| <axis 1 name> | covered | Phases 1, 3 |
| <axis 2 name> | extra-proposal | Phase 7 — not requested; the objective implies it |
| <axis 3 name> | deferred | <reason> / separate roadmap |
| <axis 4 name> | → Level 2 | <reason> |

> One row per axis of the desired state (Step 1); status is exactly one of `covered` / `extra-proposal` / `deferred` / `→ Level 2`.

## Level 2 — broad domain not covered
- [ ] <domain capability 1>
- [ ] <domain capability 2>

## Phases in detail

### Phase 1 — <name>
- **Tentative route**: loop:STANDARD  ·  **Depends on**: —  ·  **Deferrable?**: no (core) | yes
- **Deferrable?**: `no` = core, it has to be done for the value to exist; `yes` = can be done later without breaking the core. It is a business PRIORITY axis, distinct from "Depends on" (which is technical). The gate (Step 5) reads this mark for core-vs-complete.
- **slug**: `<stable-kebab>` — the change-name it will use when executed (branch `<type>/<slug>`); `mala-pata-roadmap-radar` matches progress by this slug. Unique and stable; do not change it between roadmap versions.
- **Why that route**: <if loop: THE DESIGN decision that makes it loop — what triage re-checks (a decision decidable-with-a-question does NOT go to loop); if organic/shot: "What+Done+Decisions already statable">
- **IN**: <what this phase includes>
- **OUT**: <what it does NOT include — stays for another phase>
- **DoD** (Given/When/Then):
  - [ ] Given <state>, When <action>, Then <observable result>.
- **To start**: `/mala-pata-triage <description of this phase>` (triage decides organic/loop/shot with
  the information of the moment; one phase = one unit; use the `slug` above as the change-name so that
  progress can be tracked with `mala-pata-roadmap-radar`).

### Phase 2 — …
(same for each phase)
```

## Rules

- **Completeness > what was requested**: the roadmap covers the COMPLETE objective (MECE desired state), not just what
  the human listed. Over-discover and propose; the human trims at the gate. Better too much than too little.
- **You do NOT execute**: not triage, not loop, not organic, not code. Only the roadmap.
- **Absolute paths** in commands; relative when talking to the human.
- **Only valid questions**: those of the vagueness gate (Step 0), the open decisions that
  change the DAG (Step 2), where to save (Step 6) and the coverage gate + DAG (Step 5). Nothing about "pace" or
  "artifact store".
- **Redirect to `/mala-pata-triage`** if the objective already fits in a single unit (Hard rule #2).
- Each phase of the roadmap is input for ONE pass of `/mala-pata-triage` (which routes it to organic or
  loop with the information of the moment) — never group them.
- **Stable slug per phase**: assign each phase a unique and stable kebab `slug` (= its change-name when
  executed; branch `<type>/<slug>`). It is what `mala-pata-roadmap-radar` uses to derive progress
  against git. Do not change it between roadmap versions.
- **`Deferrable?` per phase**: mark each phase `no` (core — needed for the value to exist) or `yes`
  (can wait without breaking the core). It is business priority, NOT the technical dependency (`Depends on`).
  The gate (Step 5) READS this column for core-vs-complete; it does not recompute it. A roadmap does NOT leave anything
  "out" (it covers everything, ideally better-too-much); what can wait is marked deferrable, not discarded.
