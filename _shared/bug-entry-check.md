# Bug entry check — mala-pata single source of truth

Canonical checks for a change tagged `kind: bug`. Read by the lane skills that carry
`kind` (`mala-pata-triage` captures it; `mala-pata-organic` / `-start`, `mala-pata-loop` / `-start` and `mala-pata-shot` apply it). Apply verbatim; do not restate in a skill.

## `kind: bug` is NOT a lane

`kind` is a **non-routing attribute** (`feature|bug`, default `feature`). A bug still
routes by size x uncertainty — `shot` / `organic` / `loop` / `spike` — exactly like any
other change. This check is **orthogonal to the lane**: it runs INSIDE whatever lane the
gate picked, it never changes that choice. (Urgency / hotfix handling is a separate
concern and out of scope here.)

## The check (when `kind: bug`, in any lane)

1. **Reproduce before code.** A reproduction — or at minimum an expected-vs-actual statement — is written BEFORE any code. If it cannot be reproduced, the approach is unknown → route to a `spike`, do not guess a fix.
2. **Regression test is part of the DoD.** A test that fails on the bug and passes on the fix. Under strict TDD this is the RED step; under standard TDD it is still required before done.
3. **Link the tracker issue — if a tracker exists.** Reference it in the kickoff and the PR. Tracker-neutral: recommended, not mandatory; skip silently when there is no tracker.
4. **Use a `fix/` branch** (`fix/<change-name>`) instead of `feature/`.
