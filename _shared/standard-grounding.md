# Canonical standard-grounding rule (advisory) — single source of truth

Apply this verbatim wherever a mala-pata skill references it. It is the ADVISORY posture the suite takes toward the project's captured standard (`/mala-pata-standards`). It does not replace the stronger, skill-specific grounding that `mala-pata-art`, `mala-pata-research` and `mala-pata-triage` already apply.

## The posture — a nudge, not a gate

When a skill produces a **DoD**, a **kickoff**, an **implementation**, or a **QA scenario**, it should **prefer the project's captured standard** where it applies — so the output conforms to how the project already does things instead of re-inventing a convention.

- **Resolve the standard** under `mala-pata/standards/`: the two-level structure via the root `_index.md` → the relevant `<area>` → its `<sub-facet>` leaves; **legacy fallback**: the flat `mala-pata/standards/<domain>.md` if the project has not migrated to the two-level structure.
- **`approved` rules only.** A `proposed` or `OPEN` rule is NOT yet a standard: do not conform to it, and do not treat it as authoritative.
- **Advisory, not a gate.** This is a nudge: it does not block or add a ceremony. If no `approved` standard covers the case, proceed best-effort — do not invent one and do not stall.
- **A NEW convention still goes through the permission gate.** If the work would ESTABLISH a new convention not covered by an `approved` rule, that is `/mala-pata-triage`'s new-standard permission gate — do not let a new de-facto standard slip in silently here; it is captured later via `/mala-pata-standards`.
- **No captured standard yet?** Say so in one line and continue; grounding is best-effort until `/mala-pata-standards` runs.

This advisory makes the whole suite *aware of* and *biased toward* the captured standard without turning every lane into a conformance gate. Hardening a specific skill into a real conformance check is a separate, deliberate change.
