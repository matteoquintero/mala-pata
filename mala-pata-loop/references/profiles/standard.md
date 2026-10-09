# STANDARD profile — default for M changes

## When to choose STANDARD
- Medium-sized change: 1-2 containers + 1-2 new services.
- Known module but non-trivial change.
- Additive feature on an existing BE contract (no new endpoints).
- There is no high regression risk but it does touch domain logic.

## Adjustments relative to the base method

- **Phase 0 components**: mandatory + **explicit human gate**.
- **TDD granularity**: **per task** — Red → Green → Refactor for each task.
- **Explore**: reuse if the module has an explore in engram from this week; otherwise full.
- **Spec + Design**: separate.
- **sdd-preview**: decides its own number of reviewers via self-assessment according to real risk. The profile does not force a number.
- **Verify**: normal — suite + build + live smoke. No extra adversarial unless design asks for it.
- **Apply**: free batches (at `sdd-tasks`'s discretion).
- **Storybook / MSW / fixtures**: full coverage.

## `/clear` nudges

- Between major phases (design → tasks, tasks → apply).
- Between apply batches if the human prefers.

## Cost order of magnitude

~250K tokens end-to-end.
