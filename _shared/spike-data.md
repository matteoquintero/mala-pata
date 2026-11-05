# Data-spike — mala-pata single source of truth

The **data-spike** profile of `/mala-pata-research --spike`: the read-only probe to run when a
change is blocked by DATA — the shape, volume or legacy state of existing data decides whether the
approach is an in-place change, an expand/contract migration, a backfill, or a new store. It is a
normal spike (read-only, scope-boxed, produces a `## Finding`, re-enters via triage); this file is
its assessment checklist. Index: `_shared/mala-pata-spike-catalog.md`.

## When
A phase/objective whose approach is unknown BECAUSE of data: "can we change `<entity>` shape
without downtime?", "does existing `<entity>` data satisfy the new invariant?", "do we need a
backfill, a new store, or an expand/contract migration?", "who owns `<entity>` and what is its
retention?". Detected when the objective-completeness **Data lens forks** the approach. It is NOT
a lane — it produces a decision, then the real work routes by size × uncertainty.

## The probe (read-only — inspect and measure, NEVER migrate or write)
1. **Current shape + constraints.** Read the schema/model for `<entity>`: columns, types,
   nullability, keys, indexes, relations, uniqueness, triggers; who reads and writes it. Evidence
   = code reference or read-only introspection.
2. **Volume and legacy reality.** Row counts, growth rate and a SAMPLE of real shape (null rates,
   orphans, values violating the intended invariant) from a read-only source (replica, snapshot,
   fixtures). If no safe read-only source exists, STATE it and request one — never query a
   writable production path.
3. **Reuse-first.** Can the existing structure carry the need (nullable column, view, flexible
   field) before a new table/store? Prove it insufficient against 1–2.
4. **Change-strategy options.** For each viable path (in-place, expand/contract, dual-write,
   backfill as its own phase, new store): lock/downtime impact, reversibility, ordering vs the
   feature slices, data-loss risk, effort.
5. **Ownership + retention.** Who owns the data, retention/erasure obligations, and the
   downstream consumers a change would break.

## Finding (the deliverable)
`## Finding`: **recommended data approach** · **rejected options** (with the constraint/volume
evidence) · **residual unknowns** (e.g. a distribution only verifiable in prod) · **effect on
decomposition** (does migration/backfill become its own phase? must it precede the feature slice?
is any step irreversible and in need of an ops phase?). **Exit criterion:** *"we can name the data
approach and its ordering"* OR *"infeasible without data we cannot access or change"* (→
RECONSIDER). Refuse a data-spike with no exit criterion.

## Re-entry
`/mala-pata-triage` reads the finding: approach now known → the phase routes organic/loop;
migration/backfill phase added or order changed → roadmap; infeasible → RECONSIDER.
