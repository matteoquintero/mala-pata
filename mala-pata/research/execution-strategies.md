---
idea_slug: execution-strategies
project: mala-pata-skills
domain: mala-pata-suite
roadmap: none
verdict: PROCEED
created_at: 2026-11-04T17:33:58-0500
next: /mala-pata-triage (one unit, organic; touches 3 skill files + 1 new shared ref; or /mala-pata-skill directly since it is suite authoring)
size_signal: one-unit
---
# Research: "Execution strategies" (within-lane mode by the nature of the work)

## Verdict: PROCEED
The concept is real, small, and has an exact in-house precedent (`tdd_mode`). Ship ONE strategy first (`interface-first`, whose visual case is UI-first); treat every other strategy as speculative until a real change demands it. One decision is the human's (see Open decisions: naming and the two meanings of "interface").

## Raw idea (what you asked)
Introduce "execution strategies": modes applied INSIDE a lane depending on the NATURE of the work. First instance: when an `organic` is very VISUAL, use Interface-Driven (UI/interface-first).

## 1. Interface-Driven Development (IDD-interface)

### Standalone definition
Design and agree the interface (the contract: signatures, inputs/outputs, error cases, responsibilities) BEFORE writing the implementation, then implement behind it. Callers and implementers can proceed independently because both depend on the contract, not on each other.

Four older ideas that all point the same way:

| Idea | What it contributes | Source | Quality |
|---|---|---|---|
| Program to an interface, not an implementation | Depend on abstractions; swap implementations freely | Gamma, Helm, Johnson, Vlissides, *Design Patterns* (GoF, 1994), intro principle | Strong, canonical book |
| Design by Contract | Interface = preconditions / postconditions / invariants | B. Meyer, *Object-Oriented Software Construction* (1988/1997) | Strong, canonical book |
| Responsibility-Driven Design | Discover objects by the responsibilities and collaborations they need, interface first | Wirfs-Brock and McKean, *Object Design* (2002) | Strong book |
| Outside-in development | Start from the outermost consumer of the system (a user action or an acceptance test), and let the needed inner interfaces fall out as you go; mocks stand in for what is not built yet | Freeman and Pryce, *Growing Object-Oriented Software, Guided by Tests* (2009) | Strong book; the "mockist / London school" lineage |
| Interface-based programming | Wikipedia article on the technique | https://en.wikipedia.org/wiki/Interface-based_programming | Encyclopedic, secondary |

"Interface-Driven Development" as a named workflow is the weak part. The sources I could point to are practitioner articles (a DZone introduction and a t3n/format-d piece, cited in `idd-as-mala-pata-method.md`), not a standard. Treat the NAME as informal; the underlying principles are solid.

### The UI-first / visual-first reading
For very visual work, the "interface" that matters first is the screen itself: build the visible surface (layout, states, copy, interaction) against stubbed/fixture data before wiring real logic or persistence behind it. Reasons it works: the visual is the part a human must JUDGE, and it is only judgeable when rendered; it surfaces the real data shape the UI needs (so the backend contract is driven by the consumer, outside-in); and it gives the human an early, cheap review point.

Grounding for this reading (all informal or adjacent, none a standard):
- Outside-in (Freeman and Pryce) is the principled version: start from the consumer. Strong, but it is about test-driven design of objects, not about screens specifically.
- Component-Driven Development (build UI bottom-up in isolation, in a component workbench, then compose pages): community methodology popularized around Storybook, https://www.componentdriven.org (practitioner source). Note this is bottom-up (components first), a slightly different cut than "screen first, wire later".
- Atomic Design (B. Frost, 2013-2016): shared vocabulary for composing UI. Already referenced by `mala-pata-art`.
- "UI-first", "frontend-first with mocked API", "prototype-first": folk practice, no authoritative definition. Honest flag: this is the least-sourced part; it is mostly consensus among practitioners.

### The bridge to walking skeleton / tracer bullet
Two related ideas keep this from being "build the whole UI, then discover the backend does not fit":
- Tracer bullet (Hunt and Thomas, *The Pragmatic Programmer*, 1999): a thin, end-to-end, production-quality slice that proves the path, kept and grown rather than thrown away. Strong source.
- Walking skeleton (Cockburn, 2004; popularized by Freeman and Pryce): the smallest end-to-end implementation of the architecture, built first. Strong source.

Practical consequence for the strategy: UI-first must END with the wiring step. The UI against fixtures is a milestone, not the finish line. That is the guardrail against the known failure mode (a polished UI over a contract the real system cannot honor).

### Naming collision (important)
"IDD" is already ambiguous in this suite (Intent-, Issue-, Interface-Driven; see `idd-as-mala-pata-method.md`). "Interface" itself has two meanings here: the code/contract meaning (an API a caller depends on) and the visual meaning (a screen). To avoid inheriting that ambiguity, name the strategy by its action, not the acronym: `interface-first`, and say that for visual work it means UI-first.

## 2. The concept: "execution strategy"

Definition: a within-lane mode, chosen by the NATURE of the work, that changes the ORDER in which you build and which artifact you stabilize first. It does not change the lane, the lane's gates, or the test discipline.

The three orthogonal dials:

| Dial | Question it answers | Chosen by | Values (examples) | Where carried today |
|---|---|---|---|---|
| Lane | How big / how uncertain is this change? | triage (size x uncertainty) | shot, organic, loop, roadmap, spike | `route:` in kickoff |
| `tdd_mode` | What test discipline applies? | `sdd-init` (project setting) | strict, standard | `tdd_mode:` in kickoff |
| Execution strategy | What SHAPE of work is this, i.e. what do we stabilize first? | the kickoff author, confirmed by the human | none, interface-first, (data-first, contract-first: speculative) | proposed: `execution_strategy:` in kickoff |

One line: lane = how big/uncertain, tdd_mode = how you test, execution strategy = what you build first given what kind of work it is.

Why it is genuinely a third dial and not a new lane or a sub-case of an existing one:
- It does not change size or uncertainty: a visual organic is still an organic.
- It does not change test discipline: strict TDD and UI-first coexist (logic behind the UI is test-first; the visual surface is judged by a human, see walkthrough/smoke), so they can vary independently.
- It is per-change, unlike `tdd_mode` which is per-project. That is the one real difference from the precedent: `tdd_mode` comes from the live project setting; `execution_strategy` is a property of THIS change's nature.

Neighbors it must not be confused with:
- `mala-pata-art`: a visual-judgment guide (HOW to improve how something looks). It is a skill the work may load; the strategy only fixes ORDER. They compose: a visual change with `execution_strategy: interface-first` may well load `mala-pata-art` while building the surface. No overlap in responsibility.
- `smoke_test`: a verification gate after apply. Visual work often needs it set to yes, but the strategy does not set it; keep them separate fields.

## 3. Where it lives (reuse-first)

What the live skills show:
- `mala-pata-organic/SKILL.md` carries `tdd_mode: <strict|standard>` and `smoke_test: {needed: auto|yes|no, data}` in the kickoff frontmatter. `smoke_test` defaults to `auto`: organic-start proposes, the human confirms.
- `mala-pata-organic-start/SKILL.md` Step 1 reads these fields, Step 6 (implement) applies "the project's TDD mode" and forwards it to writers.
- The house pattern for rules needed by several skills is a canonical `_shared/` file ("single source of truth, apply verbatim, supersedes any restatement"): `test-db-guard.md`, `git-truth.md`, `lane-gate.md`, `domain-rule.md`.
- `_shared/lane-gate.md` decides routing only; it has no concept of in-lane modes. Do not put the strategy there, since that would mix dial 1 with dial 3.

Options:

| Option | For | Against |
|---|---|---|
| A. Kickoff frontmatter field only | Matches `tdd_mode` / `smoke_test`; trivial to carry and forward | Definition of each strategy would be restated in organic, organic-start, later loop: drift |
| B. `_shared/execution-strategies.md` only | Single source of truth; one place to add strategy #2 | Nothing selects a strategy per change; the kickoff cannot carry the choice |
| C. Both: field selects, shared ref defines | Follows the house split exactly: data in the kickoff, rules in `_shared`, each skill adds one line | Slightly more files (1 new + 3 one-line edits) |

Recommendation: C. Concretely:
1. New `_shared/execution-strategies.md`: defines the dial, the allowed values, and for each strategy its trigger signal, what changes in the ORDER of work, and its guardrail (e.g. interface-first must end with wiring).
2. Kickoff frontmatter (organic): `execution_strategy: <none|interface-first>` with the same `auto` convention as `smoke_test` (the kickoff author proposes from the nature of the work, organic-start confirms with the human in one line). Default `none`, so nothing changes for existing kickoffs.
3. organic-start Step 1 reads it; Step 6 states "apply `_shared/execution-strategies.md` for the declared strategy" and forwards it in writer delegations, the same way `tdd_mode` is forwarded.
4. Scope for now: organic only. `loop` and `roadmap` phases can adopt later; do not generalize ahead of a case. A roadmap phase's tentative route could eventually carry it as a hint, but triage still decides (as with routes).

Do NOT: add it to triage's routing outputs (it is not a lane decision), make it a skill of its own, or let it override the lane gate.

## 4. Initial minimal set

| Strategy | Status | Trigger signal | Order of work | Guardrail |
|---|---|---|---|---|
| `none` | default | not obviously any of the below | the lane's normal flow | n/a |
| `interface-first` (visual reading = UI-first) | PROPOSED, ship this | DoD is mainly about what a human sees or does on a screen; layout/states/copy dominate | 1. agree the interface/contract (the screen states and the data shape it needs); 2. build the visible surface against fixtures; 3. human checkpoint on the surface (the cheap review point); 4. wire real logic/data behind it, test-first per `tdd_mode`; 5. remove fixtures | must finish with the wiring step; fixtures are scaffolding, not deliverable; the contract found in step 2 is written down before step 4 |
| `data-first` | SPECULATIVE, do not ship yet | data-heavy: schema/migration/derivation is the hard part | stabilize the model and its invariants first, then the consumers | no case yet; add only when a real change needs it |
| `contract-first` | SPECULATIVE, do not ship yet | integration-heavy: an external system or another team consumes this | agree the contract (schema/OpenAPI-like) first, stub both sides | closer to the general form of `interface-first`; may simply be its non-visual reading and not a separate strategy |

Observation: `contract-first` is probably the SAME strategy as `interface-first` read for non-visual work. So the honest minimal set may be ONE strategy with two readings (visual: UI-first; non-visual: contract-first), selected by the nature of the work. Decide that when a non-visual case appears; do not pre-split now.

## What I reused
- The `tdd_mode` pattern: a mode forwarded INTO a lane via kickoff frontmatter and applied in organic-start Step 6; orthogonal to the lane.
- The `smoke_test` `auto` convention (author proposes, organic-start confirms with the human).
- The `_shared/` canonical-ref house pattern for the definition.
- The existing sourcing in `idd-as-mala-pata-method.md` and `all-driven-methodologies.md` for the weak "named IDD" part, not re-derived.

## Source quality summary
- Strong (canonical books): GoF 1994, Meyer, Wirfs-Brock, Freeman and Pryce, Hunt and Thomas, Cockburn (walking skeleton, article/book lineage).
- Weak/informal: "Interface-Driven Development" as a named workflow; "UI-first / frontend-first with mocks" (folk practice); component-driven.org (practitioner community). Flagged above.
- Not re-fetched in this run: book claims are from knowledge, not re-verified against the web; treat page-level citations as unconfirmed.
- Speculative by design: `data-first`, `contract-first`, and extending to loop/roadmap.

## Open decisions (human)
1. Name: `interface-first` (recommended, avoids the IDD acronym clash) vs literal "Interface-Driven". Also confirm "execution strategy" as the dial's name.
2. Field name and values: `execution_strategy: none|interface-first`, default `none`, with `auto` proposal by the author/organic-start (like `smoke_test`)?
3. Who sets it: the kickoff author proposes, the human confirms in organic-start (recommended), or purely human-set?
4. Whether `interface-first` should auto-suggest `smoke_test.needed: yes` for visual work (kept as separate fields for now).
5. Scope: organic only first (recommended), or also loop?
