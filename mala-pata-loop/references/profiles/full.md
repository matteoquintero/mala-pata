# FULL profile — L / critical SDDs / first step in a module

## When to choose FULL
- Large change: multiple containers + services + types + tests.
- New feature (does not adapt existing code).
- New BE contract (endpoints, migrations, shape change).
- A module you have never worked on (needs explore from scratch).
- Regression risk in critical flows (auth, permissions, PII, money).

## Adjustments relative to the base method

- **Phase 0 components**: mandatory + **explicit human gate** to approve the set of atoms/molecules/organisms before Apply.
- **TDD granularity**: **per task** — Red → Green → Refactor for each individual task.
- **Explore**: full from scratch. Ignore previous explores even if they exist (the module is re-audited).
- **Spec + Design**: separate. They run as distinct phases (`sdd-spec` and `sdd-design`).
- **sdd-preview**: decides its own number of reviewers via self-assessment based on real risk. The profile does NOT impose a number.
- **Verify**: heavy + adversarial. Verifies against all the spec's criteria, runs the full suite + build + live smoke + adversarial checks if they apply.
- **Apply**: small batches (3-4 tasks) + `/clear` nudge between batches.
- **Storybook / MSW / fixtures**: full coverage of new variants.

## `/clear` nudges

- After each major phase (`explore`, `propose`, `spec`, `design`, `tasks`, each `apply` batch, `verify`).
- Before starting Apply.

## Cost order of magnitude

~500K tokens end-to-end.
