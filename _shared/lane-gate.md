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
- **loop** — a decision that NEEDS DESIGN: several viable architectures with tradeoffs to investigate, or options unknowable without exploring.
- **roadmap** — needs decomposition into several INDEPENDENT vertical slices, OR carries several open architecture decisions each needing its own unit.

## THE loop discriminator (the rule most often gotten wrong)

"There is a decision" ≠ loop. **loop ⟺ the decision needs DESIGN.**

- **Decidable with one answer → NOT loop → organic** (or shot if also trivial). This INCLUDES every pure **product decision**: choosing A vs B, a preference, a yes/no that merely selects an existing option with no architecture to investigate. *Example: "use library A vs library B", or "self-host a capability vs use a managed provider" — you pick one and move on, nothing to design → organic/shot, never loop.*
- **Needs design → loop**: viable architectures with tradeoffs to research, or options you cannot know without exploring.
- Test: *can I state the options and does one answer close them?* If yes → NOT loop.

A decision wrongly sent to loop drags the full loop ceremony (design + preview) onto something that only needed an answer — that waste is exactly what this discriminator prevents.

## THE roadmap discriminator

roadmap is a **CONCLUSION of investigation, NEVER inherited from quantity/length**. A long list, many files, or a big icebox is NOT a roadmap. Roadmap only when the work genuinely needs decomposition into independent vertical slices, or carries several open architecture decisions each its own unit.
