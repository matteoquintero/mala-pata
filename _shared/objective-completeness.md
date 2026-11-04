# Objective completeness — mala-pata single source of truth

Canonical rule for "what is MISSING for the objective to be fully reachable". Applied
VERBATIM by `mala-pata-research` (lightweight sweep) and `mala-pata-roadmap` (Step 1,
desired state). Neither skill restates the dimension list or the fork test; both point
here. This file is rule-only: verdict wiring and routing stay in the consuming skill.

## Dimension sweep (an OPEN list — prompts, not a fixed schema)

For the restated objective, ask of each lens "what is MISSING for the objective to be
fully reachable?" Record ONLY items that are `MISSING` or `unknown`, each with provenance:
`verified` (against the code / an authoritative source) or `inferred`.

- **User-facing** — screens/states (empty, error, loading), copy, journey steps nobody named (Story-Map walk + jobs-to-be-done).
- **Data** — model changes, migrations/backfill, retention, ownership.
- **Access** — roles, permissions, tenancy, audit.
- **Integrations** — external systems, contracts, failure/retry behavior.
- **Edge cases** — concurrency, partial failure, legacy data, limits.
- **Non-functional** (ISO/IEC 25010 as the prompt vocabulary) — performance, security, reliability, compatibility, maintainability, usability.
- **Operations** — observability, config/flags, rollout, rollback, runbooks.
- **Infrastructure** — only if the objective demands it.
- **`<other>`** — the list is explicitly OPEN; add any lens the domain implies.

**No silent drop (MECE).** A lens judged irrelevant is recorded `n/a - <reason>`, NEVER
silently skipped.

## The fork test (the key idea)

For every MISSING/unknown item ask: **"does the answer change the decomposition (the
slices, their order, or their boundaries)?"**

- **No** → a detail. It is a normal open decision or a DoD line.
- **Yes** → an **approach-fork**. Count it and flag it:
  - ONE scoped fork inside a single unit (the options can be listed now) → a normal open decision (candidate loop).
  - A BROAD fork ("I do not know how to approach this part at all") → a **spike candidate**.

## Proportionality (so this never becomes a roadmap by accident)

- **Level 1 — adjacent-implied** (completes or directly implies what was asked) → goes into scope.
- **Level 2 — broad domain** (the rest of the domain's universe) → a compact "not covered" checklist; it does not inflate scope.
- Depth scales with the size of the problem and STOPS when the remaining unknowns cost more to research than to defer (risk-driven stopping).
