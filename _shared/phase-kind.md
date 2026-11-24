# Phase kind — mala-pata single source of truth

Canonical for a roadmap phase's **kind** — the NATURE of the work, orthogonal to its **route**
(`shot` / `organic` / `loop`). The route says HOW it is executed; the kind says WHAT it
produces and HOW its completion is PROVEN. A skill that reads or writes a phase kind applies
THIS verbatim (consumers: `/mala-pata-roadmap`, `/mala-pata-roadmap-radar`,
`/mala-pata-roadmap-orchestrate(-start)`, `/mala-pata-research`).

## The kinds (frozen — code | ops | spike)

| Kind | What it produces | How "done" is proven | Radar provenance |
|---|---|---|---|
| `code` | a code change that ships through a lane | **git reality** — merge / PR / slug commit (the `Mala-Pata-Phase` trailer) | `[git]` |
| `ops` | an operational step with no code diff (provision, deploy, config, a manual env action) | **human attestation** — `Verify:` (URL / command / health) · `Status:` pending\|done · `Evidence:` (env URL / id / health 200 / date); git cannot see it | `[attested]` |
| `spike` | a read-only probe of a broad unknown (`/mala-pata-research --spike`) | a **finding** doc with a filled `## Finding`, RE-ENTERED via `/mala-pata-triage`; it ships no code and blocks its dependents until re-entry | `[finding]` |

## The rule

1. **Kind is orthogonal to route.** A `code` phase may be a `shot`, `organic` or `loop`; a
   `spike` phase runs as research, not a lane; an `ops` phase has no lane at all. Never
   conflate the kind column with the route column.
2. **The kind decides how completion is read.** A radar proves a `code` phase from git, an
   `ops` phase from the human-maintained `Verify/Status/Evidence` block, and a `spike` phase
   from the finding doc + its triage re-entry. Reading an `ops` or `spike` phase as "no git
   evidence → pending" is a defect — they are not proven by git.
3. **A `spike` never lands as code.** Its deliverable is the finding; its re-entry is triage.
   A `spike` phase marked `✓ done` means the finding is written AND re-entered, not that code
   shipped.
4. **Default is `code`.** When a phase names no kind, it is `code`. `ops` and `spike` are
   declared explicitly because they change how the phase is proven.
