# LITE profile — S/M in a known module

## When to choose LITE
- Small or medium change.
- Hot module (worked on this week or recently).
- Adapts existing atoms/molecules (does not create genuinely new components).
- Extends an existing service (does not create a new service).
- No regression risk in critical flows.

## Adjustments relative to the base method

- **Phase 0 components**: mandatory — the REUSA/ADAPTA/NUEVO audit is **NOT skipped**. Difference from FULL/STANDARD: the human gate is **auto-approve if the audit marks 0 NEW components**; if there is ≥1 NEW, the human gate is explicit.
- **TDD granularity**: **per feature** — group related tasks (service + selector + container wiring) and write tests when closing the group. Exception: pure logic (VOs, selectors, algorithms) stays per task.
- **Explore**: reuse previous explores of the same module if they exist in engram; otherwise minimal explore (grep-first).
- **Spec + Design**: **merged** into a single artifact `sdd/<change>/spec-design`. `sdd-design` includes scenarios that in STANDARD would go in spec.
- **sdd-preview**: decides its own self-assessment; for LITE typically 0 unless some real risk signal appears.
- **Verify**: light — suite + build + live smoke. No adversarial. (Default by size: rises to normal if `sdd-preview` detected risk signals — see `_base.md`.)
- **Apply**: free batches.
- **Storybook / MSW / fixtures**: only critical new variants.

## `/clear` nudges

- Between spec-design and apply.
- At the human's discretion for the rest.

## Cost order of magnitude

~120K tokens end-to-end.
