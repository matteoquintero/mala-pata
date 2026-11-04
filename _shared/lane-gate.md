# Lane-routing gate — mala-pata single source of truth

Canonical rule for choosing a lane. Every lane-touching skill (`mala-pata-triage`,
`mala-pata-research`, `mala-pata-roadmap`, `mala-pata-organic`,
`mala-pata-icebox-defrost` / `-start`) applies THIS verbatim and never paraphrases
or re-derives it. A `size-hint` is only a hint and never routes.

## Form gate — the three blocking fields

- **What** — concrete, observable behavior/result. "Improve X" with no concrete target FAILS.
- **DoD** — testable, Given/When/Then ("Given <state>, When <action>, Then <observable result>").
- **Decisions already made** — the approach/architecture is resolved or obvious.

Non-blocking: **Why** (one line), **Risk** (optional). Never a gate: **Where** — it is an output of the Explore phase, not a precondition.

## Lane selection

- **shot** — trivial + understood + minimal blast radius: 1-3 files, no migration/contract/new UI, no open decision.
- **organic** — What/DoD statable AND decisions resolved/obvious. A decision decidable with ONE question → ask it, then organic.
- **loop** — a SCOPED design decision: the unit's boundaries are known, and the open question is *which* of several viable designs fits (tradeoffs to weigh). An expert could lay out the options now. May be standalone or a phase inside a roadmap.
- **spike (research)** — a BROAD approach-unknown: you do not know HOW to do it, the answer would change what the units even are, and the options cannot be listed without probing (prototype, measurement, reading an unfamiliar system, feasibility check). Not a lane that ships — it produces knowledge, then re-enters the pipeline (`/mala-pata-research --spike`, then triage).
- **roadmap** — needs decomposition into several INDEPENDENT vertical slices, OR carries several open architecture decisions each needing its own unit.

## THE loop discriminator (the rule most often gotten wrong)

"There is a decision" ≠ loop. **loop ⟺ the decision needs DESIGN.**

- **Decidable with one answer → NOT loop → organic** (or shot if also trivial). This INCLUDES every pure **product decision**: choosing A vs B, a preference, a yes/no that merely selects an existing option with no architecture to investigate. *Example: "use library A vs library B", or "self-host a capability vs use a managed provider" — you pick one and move on, nothing to design → organic/shot, never loop.*
- **Needs design → loop**: viable architectures with tradeoffs to weigh — the design space is known but the choice has tradeoffs.
- **Approach unknown → spike (research), NOT loop**: you must probe before the options or the boundaries are even known.

Ordered test (Cynefin-derived — a question to ask, not a classifier):
1. *Can I state the options and does one answer close them?* → yes: NOT loop (organic/shot).
2. *Can an expert design it NOW from known practice, with the unit's boundaries already fixed?* → yes: **loop** (analyze, then decide). Standalone is fine.
3. *Must we PROBE before the options or boundaries are known, or would the answer reshape the decomposition?* → yes: **spike/research**, not loop.

Breadth, not roadmap-membership, is the axis: a loop is still valid standalone for a scoped design-heavy single unit. "Hard" or "big" alone is neither loop nor spike.

Rule of thumb: *"I don't know how" never routes to loop; "I know the shape, I must choose among designs" does.* When the test is borderline, ask ONE question rather than guess the domain.

A decision wrongly sent to loop drags the full loop ceremony (design + preview) onto something that only needed an answer — that waste is exactly what this discriminator prevents.

## THE roadmap discriminator

roadmap is a **CONCLUSION of investigation, NEVER inherited from quantity/length**. A long list, many files, or a big icebox is NOT a roadmap. Roadmap only when the work genuinely needs decomposition into independent vertical slices, or carries several open architecture decisions each its own unit.
