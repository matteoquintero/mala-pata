# Spike-profile catalog — mala-pata single source of truth

The index of **spike profiles** for `/mala-pata-research --spike`. A spike is the read-only,
scope-boxed probe for a BROAD approach-unknown; a **profile** is the assessment checklist it
applies when the unknown belongs to a known concern. Spikes stay per-concern: a profile never
turns research into the home of design, verification or execution — it only probes.

## Catalog
| Profile | Lens that forks to it | File | Use when the approach is unknown because of… |
|---|---|---|---|
| `infra` | Infrastructure | `_shared/mala-pata-spike-infra.md` | new provisioning or a capacity ceiling |
| `data` | Data | `_shared/mala-pata-spike-data.md` | schema shape, volume/legacy reality, migration or backfill strategy |
| `integration` | Integrations | `_shared/mala-pata-spike-integration.md` | an external system's contract, limits or failure semantics |
| `generic` | any other / `<other>` | (this file) | no profile matches |

**Never a profile** (they fail the fork test or are not read-only-probable): user-facing, access,
edge cases, operations — these are details, DoD lines, a scoped design decision, or a `Kind: ops`
phase.
**Not a profile — performance:** the decisive evidence is load measurement, which is not read-only;
its capacity-ceiling half is already step 1 of the infra profile. Add one only on a real case
(see Promotion).

## Selection rule
1. **Detection names the profile.** The completeness sweep annotates a broad fork as
   `fork: <lens> -> spike-<profile>`; no new gate, only a name on the existing annotation.
2. **Triage and roadmap carry it.** The spike answer / a roadmap `Kind: spike` phase records the
   profile (e.g. `spike (data)`).
3. **Research `--spike` applies it.** Load this index, pick the profile by that name (or by the
   lens of the unknown if unnamed), apply that profile's `The probe` checklist verbatim, and set
   `profile: <name>` in the spike frontmatter.
4. **No match → generic spike.** Run only the spike-mode rules (question, exit criterion,
   forecast, read-only, `## Finding`) with this default probe: *state the unknown precisely →
   list the sources that can answer it read-only → gather evidence → lay options side by side*.
   Record `profile: generic` so repeated generics are countable.
5. **Several lenses fork at once → one spike per concern**, in dependency order; never a
   mega-spike. The anti-ceremony guard (one spike per question without an explicit human
   decision) applies to each.

## Promotion rule
A generic spike becomes a profile only when (a) the same lens forced a broad, read-only-probable
unknown in **at least two real cases**, AND (b) its checklist differs materially from the generic
four steps, AND (c) the owner approves. The threshold triggers the proposal; the owner is the gate.
A new profile = one new `_shared/spike-<x>.md` (same section shape as the infra profile) + one
row above.
