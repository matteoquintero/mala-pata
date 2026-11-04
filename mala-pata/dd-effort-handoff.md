# `-DD` effort — decision log & handoff

Closed, shipped to `main`. This is also the reframe that was meant for the (now-closed) "Main Mala Pata" session.

## Model (the correction)
NOT "all `-DD` are knowledge for research." The correct model is **per-concern placement**: each `-DD` lands in the skill that governs its concern. Research is ONE home (detection), not the only one.

| Concern | Home |
|---|---|
| Detection ("professionally you're missing Y") | `research` + `roadmap` via `_shared/objective-completeness.md` |
| Verification (how you test) | modes: `tdd_mode`; Eval-Driven = detected gap, not a skill |
| Design / architecture | `mala-pata-art` / `standards` / `loop` design / `clean-ddd-hexagonal` |
| Decomposition | `roadmap` (vertical-slice) |
| Routing / intent capture | `triage` |
| Review | RDD (Receipt) switch |
| Execution order (what you build first) | `execution_strategy` dial (per-change) |

## Final dispositions
- SDD=`loop`, ODD=`organic`/`shot`, RDD(Receipt)=review switch, TDD=`tdd_mode`, BDD=`walkthrough`+DoD — already existed.
- EDD-Eval → detected gap in `research` (not a skill). EDD-Example → covered. EDD-Experiment → out of scope. EDD-Event → architecture.
- IDD-Intent → `triage` gate. IDD-Interface → new `execution_strategy: interface-first` (organic+loop). IDD-Issue → NOT a lane; `kind: bug` tag + `_shared/bug-entry-check.md`.
- CDD-Component → `mala-pata-art`. CDD-Contract → detected gap. CDD-Context → suite backbone.
- VSD-Vertical-Slice → already in `roadmap`/`organic`. VSD-Value-Sensitive → `mala-pata-art`. Atomic Design (not -DD) → `mala-pata-art`.

## What shipped (commit d903cff on `main`)
New `_shared/` refs: `objective-completeness.md`, `execution-strategies.md`, `bug-entry-check.md`.
Edited: `lane-gate` (loop-vs-spike/Cynefin), `research` (--spike mode + completeness gate), `triage` (spike outcome + kind:bug), `roadmap` (Kind: spike), `roadmap-radar` (spike status), `organic`/`organic-start`/`loop`/`loop-start`/`shot` (execution_strategy + kind), `mala-pata-art` (+Atomic Design, Component-Driven, Value-Sensitive Design).
Docs: research docs + `skill-structure-index.md`.

## Open follow-up (next)
An **infra capability** ("team de infra") — infra is DETECTED today but not OWNED; it keeps getting deferred and keeps forcing phases to `loop`. To be researched/shaped.
