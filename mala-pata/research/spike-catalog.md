---
idea_slug: spike-catalog
project: mala-pata-skills
domain: mala-pata-suite
roadmap: none
verdict: SHARPEN
created_at: 2026-11-05T09:17:33-0500
next: none (SHARPEN)
size_signal: one-unit
kind: research
---
# Research: a catalog of spike-profiles (infra-spike as the first entry)

## Verdict: SHARPEN
The catalog idea is sound but must be shipped SMALL: a thin index plus exactly the profiles that pass the fork test. On the evidence read, only **two** lenses beyond infrastructure plausibly qualify (data/migration and integration/contract); a third (non-functional/performance) is speculative and should be added only when a real case appears. Everything else is a detail, never a profile. It is SHARPEN (not PROCEED) because three owner decisions below change the shape (file layout, selector home, whether to ship any profile beyond infra now).

Evidence tags: **[F]** verified in the files read this session. **[A]** assumption / house judgment, not grounded in a file.

## Raw idea (what you asked)
Express mala-pata's completeness concerns as a catalog of reusable spike-profiles (read-only probes), with the shipped infra-spike as the first entry. Do not regress the model in `dd-effort-handoff.md`: each concern lands per-concern; spikes are only the "probe a broad unknown" mechanism.

## Discover

### What exists today [F]
- `_shared/objective-completeness.md`: an OPEN list of 9 lenses (user-facing, data, access, integrations, edge cases, non-functional, operations, infrastructure, `<other>`) plus the **fork test**: "does the answer change the decomposition (slices, order, boundaries)?" No -> detail. Yes -> approach-fork; ONE scoped fork inside a unit -> normal open decision; a BROAD fork ("I do not know how to approach this part at all") -> **spike candidate**.
- Only the **Infrastructure** lens names a profile today ("the spike candidate is an infra-spike"). Every other lens that forks falls to the generic spike with no checklist.
- `_shared/spike-infra.md`: the template. Sections: `When` / `The probe (read-only ...)` / `Finding` / `Re-entry`. It states itself as the "First entry of the future spike-profile catalog". Its checklist shape is: measure current state + ceiling -> reuse-first -> new-option feasibility + cost -> options + tradeoffs -> decidable. Exit criterion is mandatory.
- `mala-pata-research/SKILL.md` "Spike mode": the spike is a MODE of research (not a skill); question + mandatory exit criterion; forecast first; read-only; one bullet "Profiles" that hard-wires ONLY infra-spike ("more will be cataloged later"); output is the normal research doc with `kind: spike` and a fixed `## Finding`; re-entry always `/mala-pata-triage <slug>`; anti-ceremony guard (spike once per phase/question without explicit human decision).
- `mala-pata-triage` and `mala-pata-roadmap` route to the spike via the lane-gate ("approach unknown -> spike") and the roadmap `Kind: spike` phase type. Neither names a profile.
- `dd-effort-handoff.md` (the model not to regress): per-concern placement; detection lives in `research` + `roadmap` via `objective-completeness`; spikes are not a catch-all for `-DD` concerns.
- Naming observation [F]: SKILL.md files reference `_shared/mala-pata-<x>.md` while the files on disk are `_shared/<x>.md`. [A] The `mala-pata-` prefix is applied at mirror/install time; this doc uses the on-disk names and any new file should follow whatever convention the existing two follow at install time. Verify before shipping.

### Key insight
A spike profile is NOT "a lens with a longer checklist". A lens becomes a profile only if (1) it can **fork the approach** (change slices/order/boundaries), AND (2) the fork is **BROAD** (options cannot be listed without probing), AND (3) the probe is **read-only-feasible** (can be answered by reading code/config/docs/measurements without provisioning or writing), AND (4) the probe is **reusable** across domains (a generic checklist adds value over a bare spike). A lens failing any of the four stays a detail, a normal open decision, or a DoD line.

## Lens classification (fork-test-driven)

| Lens | Class | Reasoning (fork test) |
|---|---|---|
| Infrastructure | **Real profile (shipped)** | Forks decomposition (adds a provisioning phase, reorders slices); unknown is broad ("do we need a queue / storage?"); answerable read-only by measuring the ceiling in config/metrics. Already `spike-infra.md`. |
| Data (model, migration, backfill) | **Real profile** | A schema/volume/legacy-shape unknown genuinely forks the approach: in-place migration vs expand/contract vs new store vs backfill-as-own-phase, and it reorders slices (migration BEFORE feature). Read-only probe works: inspect schema, row counts/shape via read-only queries or fixtures, constraints, ownership, retention. [A] The row-count/shape probe presumes read access to a representative copy; if only prod exists, the profile must say "ask for a read-only replica" rather than touch prod. |
| Integrations (external contract, failure/retry) | **Real profile** | Forks approach (direct call vs adapter/anti-corruption vs async/queue; build vs buy; whether a phase for contract stubs is needed). Broad when the external system is unfamiliar. Read-only probe: read the provider docs/OpenAPI/sandbox terms, existing adapters in the repo, auth/rate/idempotency/failure semantics. Must NOT call the live external system with side effects. |
| Non-functional (performance first; security/reliability/etc.) | **Speculative** | Performance can fork the approach (cache, precompute, pagination, read replica), but the probe usually needs measurement under load, which is not read-only-feasible and overlaps heavily with infra (capacity ceiling). The ceiling-measurement part is ALREADY in infra-spike. Other NFRs (security, usability, maintainability) are cross-cutting constraints, not approach-forks; they become DoD lines or standards. Add a profile only after a real case proves a distinct checklist. |
| Operations (observability, flags, rollout, rollback) | **Never a profile** (mostly) | These are almost always details/DoD lines or a phase `Kind: ops`. They rarely make the approach unknowable. [A] Rare exception (e.g. "can we even roll this back?") is an infra/data concern and is covered by those profiles. |
| User-facing | **Never a profile** | Unknowns here are product/design decisions (decidable with one question) or handled by `mala-pata-art`/`standards`/walkthrough. They do not need a read-only technical probe. |
| Access (roles, permissions, tenancy) | **Never a profile** (borderline) | Normally a scoped design decision (loop) or detail. [A] A "we have no tenancy model at all" fork would be a data/architecture unknown better routed to a loop or the data profile than to its own profile. |
| Edge cases | **Never a profile** | Details by definition; they feed DoD/edge-case tests. They do not fork the decomposition. |
| `<other>` | **No profile; generic spike** | The open slot. A forking `<other>` lens runs the generic spike (no checklist). If the same `<other>` forks repeatedly across real cases, that is the signal to promote it to a profile (see "Promotion rule"). |

**Honest count: 1 shipped + 2 real + 1 speculative + 5 never.** Resist adding more.

## Catalog structure

### Options
| Option | Shape | Pros | Cons |
|---|---|---|---|
| A. Single file `_shared/spike-catalog.md` | All profiles inline | One file to load; trivial to read; no index drift | Grows with each profile; every spike loads ALL profiles (context cost); breaks the house "one concern per `_shared` file" habit; editing one profile touches shared file |
| B. Index + per-profile files (recommended) | `_shared/spike-catalog.md` (index + selection rule + generic spike skeleton + promotion rule) and `_shared/spike-<x>.md` per profile | Matches the house pattern (`spike-infra.md` already exists as a standalone profile; other `_shared` files are single-concern); a spike loads only the index + ONE profile; infra-spike unchanged; new profile = one new file + one index row | Two-hop read (index -> profile); index can drift from files if not maintained |
| C. Per-profile only, no index | Just `spike-<x>.md` files, selection in the SKILL.md | Zero new index file | Selection logic scatters across research/triage/roadmap SKILL.md; violates the "one source of truth, consumers point here" principle the `_shared` files exist for |

**Recommendation: B.** Reasons: (1) `spike-infra.md` already is the per-profile file, so B is additive (index only) and does not rewrite a shipped file; (2) `_shared` files are loaded verbatim by consumers ("apply verbatim, never restate"), so a small index with the selection rule gives one place to point; (3) per-profile loading keeps spike context cost proportional (a data-spike should not read the infra checklist). Drift risk is mitigated by keeping the index a table of `<lens> -> <profile file> -> <one-line When>` only.

Index contents (proposed): purpose; the catalog table; selection rule; no-match rule; generic spike skeleton; promotion rule; "what is never a profile" list (the 5 above) so contributors do not re-litigate.

## Selection mechanism

1. **Detection names the profile.** The completeness sweep (research Phase 1g, roadmap Step 1) already finds a lens fork. Extend only the fork annotation: `fork: <lens> -> spike-<profile>` (profile name from the catalog index; for infra this is already stated). No new gate or step, only a name on an existing annotation.
2. **Triage routes the spike; the spike applies the named profile.** Triage's spike answer (`-> run /mala-pata-research --spike "<question>"`) already names the specific unknown; it additionally carries the profile name when the fork annotation has one. Research `--spike` then loads `_shared/spike-catalog.md`, picks the profile by that name (or by the lens of the unknown if unnamed), and applies that profile's `The probe` checklist verbatim.
3. **Roadmap**: a `Kind: spike` phase records the profile in the phase line (e.g. `spike (data)`); same loading rule when the phase runs.
4. **No match (fork on a lens without a profile, or an unclassified unknown) -> generic spike.** Generic skeleton = the existing spike-mode rules only (question, exit criterion, forecast, read-only, `## Finding`) with a four-step default probe: *state the unknown precisely -> list the sources that can answer it read-only -> gather evidence -> lay options side by side*. No profile checklist. The doc records `profile: generic` so repeated generics are countable.
5. **Multiple lenses fork at once** -> one spike per concern, in dependency order, never a mega-spike (anti-ceremony guard still applies per question). [A] This is the direct application of the per-concern model; it is a recommendation, not stated in the current files.
6. **Frontmatter hint (optional, additive).** Spike docs gain `profile: infra | data | integration | generic` next to `kind: spike`. [A] Not currently in SKILL.md's frontmatter spec; needs an owner decision (below). It is parseable and lets domain-radar/gaps count spikes per profile.

### Promotion rule (how the catalog grows without bloat)
A generic spike becomes a profile only when (a) the same lens forked a broad, read-only-probable unknown in **at least two distinct real cases**, AND (b) the probe checklist differs materially from the generic four steps. [A] The "two cases" threshold is a proposal, not an existing rule. This stops a profile per lens "by default".

## Profile skeletons
Each follows the `spike-infra.md` sections exactly (`When` / `The probe` / `Finding` / `Re-entry`). Placeholders only.

### `_shared/spike-data.md` — data-spike (real)
**When.** The approach is unknown BECAUSE of data: "can we change `<table>` shape without downtime?", "does existing `<table>` data satisfy the new invariant?", "do we need a backfill, a new store, or an expand/contract migration?", "who owns `<entity>` and what is its retention?". Detected when the objective-completeness **Data lens forks** the approach. Not a lane; it produces a decision, then the real work routes by size x uncertainty.

**The probe (read-only — inspect and measure, NEVER migrate or write).**
1. **Current shape + constraints.** Read the schema/model for `<table>`/`<entity>`: columns, types, nullability, keys, indexes, FKs, uniqueness, triggers; who writes/reads it (callers). Evidence = file:line or read-only introspection.
2. **Volume and legacy reality.** Row counts, growth rate, and a SAMPLE of real shape (null rates, orphan rows, values violating the intended invariant) from a read-only source (replica/snapshot/fixtures). If no safe read-only source exists, STATE that and request one; do not query a writable production path. [A]
3. **Reuse-first.** Can the existing structure carry the need (add nullable column, view, JSON field) before a new table/store? Prove insufficient against the constraints in 1-2.
4. **Change-strategy options.** For each viable path (in-place, expand/contract, dual-write, backfill as its own phase, new store): lock/downtime impact, reversibility, ordering vs the feature slices, data-loss risk, effort.
5. **Ownership + retention.** Who owns the data, retention/erasure obligations, and any downstream consumers a change would break.

**Finding.** `## Finding`: **recommended data approach** · **rejected options** (with the constraint/volume evidence) · **residual unknowns** (e.g. prod-only distribution to verify) · **effect on decomposition** (migration/backfill becomes its own phase? must it precede the feature slice? any irreversible step needing an ops phase?). **Exit criterion:** *"we can name the data approach and its ordering"* OR *"infeasible without data we cannot access/change"* (-> RECONSIDER). Refuse a data-spike with no exit criterion.

**Re-entry.** `/mala-pata-triage <slug>`: approach now known -> organic/loop; migration/backfill phase added or order changed -> roadmap; infeasible -> RECONSIDER.

### `_shared/spike-integration.md` — integration-spike (real)
**When.** The approach is unknown BECAUSE of an external system or contract: "can `<service>` do `<capability>` at our volume?", "what are `<service>`'s auth, rate, idempotency and failure semantics?", "build adapter vs use SDK vs async via queue?". Detected when the **Integrations lens forks** the approach. Not a lane.

**The probe (read-only — read contracts and docs, NEVER call the live system with side effects).**
1. **Contract surface.** From authoritative sources (provider docs/OpenAPI/schema, versioning policy), list the endpoints/events the objective needs, auth model, payload shapes, limits. Cite sources; the provider's doc is the authority, not the current code.
2. **Existing coupling.** Inventory adapters/clients/webhook handlers already in the repo for `<service>` or siblings; reuse-first before a new adapter.
3. **Failure semantics.** Timeouts, retries, idempotency keys, ordering and duplicate guarantees, webhook delivery guarantees, sandbox/test availability, SLA. Name what the system does when `<service>` is down or slow.
4. **Cost/ownership/risk.** Credentials needed (who holds them), per-call cost/quotas, vendor lock-in, data leaving our boundary (privacy). A dependency needing credentials or a contract nobody owns is a red flag — name it.
5. **Options + tradeoffs.** Direct call vs adapter/anti-corruption layer vs async/outbox vs build-vs-buy; compare effort, coupling, failure blast radius, testability.

**Finding.** `## Finding`: **recommended integration approach** · **rejected options** (with the contract/limit evidence) · **residual unknowns** (e.g. behavior only observable in a sandbox with credentials) · **effect on decomposition** (contract-stub/tracer-bullet first? separate adapter phase? ops phase for credentials?). **Exit criterion:** *"we can name the integration approach and its slices"* OR *"the contract cannot satisfy the objective"* (-> RECONSIDER). Refuse an integration-spike with no exit criterion.

**Re-entry.** `/mala-pata-triage <slug>`: approach known -> organic/loop (an unproven-integration case may place a tracer bullet first per the roadmap rule); decomposition changed -> roadmap; infeasible -> RECONSIDER.

### `spike-performance` — non-functional/performance (speculative; NOT shipped now)
Hold as a one-line row in the index marked `speculative — add on second real case`. Reason: the decisive evidence is load measurement, which is not read-only, and the capacity-ceiling half is already `spike-infra` step 1. If it is ever added, its distinct value would be a **budget-first probe**: define the target (p95, throughput, cost), find the hot path from code, bound current cost by reading query plans/complexity, then list approach options (cache, precompute, pagination, async) against the budget. [A] Skeleton intentionally not written until a real case exists.

## How this fits the per-concern model (no regression)
- Each concern still lands in its home (`dd-effort-handoff.md` table). The catalog does not make research the home of verification, design, decomposition, routing, review or execution order.
- A spike remains ONLY the mechanism for "probe a broad unknown"; one profile per concern that genuinely needs probing. Operations, user-facing, access and edge cases stay in their existing homes (DoD, `mala-pata-art`/`standards`, walkthrough, `Kind: ops`, loop design).
- Detection is unchanged (completeness sweep + fork test); the catalog only adds a NAME to a fork and a checklist to a spike. Lane routing is unchanged (lane-gate -> spike -> triage re-entry).

## Problem vs proposed solution
| Piece | Class | Evidence | Provenance |
|---|---|---|---|
| `spike-catalog.md` index + selection/no-match/promotion rules | necessary (small) | Only infra is wired; no rule for other lenses forking | [F] |
| `spike-data.md` | necessary-if-owner-agrees | Data lens is the commonest approach-fork alongside infra | [A] frequency not measured |
| `spike-integration.md` | necessary-if-owner-agrees | Integrations lens forks; probe is read-only-feasible | [A] frequency not measured |
| `spike-performance.md` | extra (speculative) | Not read-only; overlaps infra step 1 | [F]/[A] |
| One profile per remaining lens | extra | Fails the fork test / "always a detail" | [F] |
| Edit research/triage/roadmap to point at the index | necessary | Research hard-wires only infra; others silent | [F] |

## Define — sharpened idea (draft for triage)
- **What:** add `_shared/spike-catalog.md` (index, selection rule, generic spike, promotion rule, never-a-profile list) plus at most `spike-data.md` and `spike-integration.md`; repoint the research "Profiles" bullet and the lens fork annotation from "infra-spike" to "the catalog".
- **Why:** completeness forks on lenses other than infra currently get a bare spike with no checklist; infra proved the pattern.
- **DoD:** Given a fork on the Data lens, When research runs `--spike`, Then it loads the catalog, applies `spike-data` and emits a `## Finding` with `profile: data`. Given a fork on a lens with no profile, Then the generic spike runs and records `profile: generic`. `spike-infra.md` behavior is unchanged.
- **Decisions made:** structure = index + per-profile files; selection = fork names the profile, spike applies it; no match = generic spike; spikes stay per-concern.
- **Open decisions:** see below.
- **Risk:** low (docs/skills only); main risk is profile sprawl, mitigated by the promotion rule and the never-a-profile list.
- **Size signal:** one-unit (HYPOTHESIS for triage; touches 1 new index + 2 small profiles + 3 skill pointers; no architecture decision unresolved after the owner decisions below).
- **Spike candidates:** none (this research itself is the probe).

## DoR (hand-off gate): What ✓ · Why ✓ · DoD ✓ · Decisions ✗ (3 owner decisions open)
Completeness: lenses swept 9 · missing 0 for this meta-task · forks 0 (spike candidates 0)

## Open decisions for the human
1. **Ship scope now:** index + infra only (zero new profiles, wait for real cases), index + data + integration (recommended), or index + all three incl. performance? Recommendation: index + data + integration; leave performance as a speculative row.
2. **Frontmatter:** add `profile: infra | data | integration | generic` to the spike doc frontmatter spec in research SKILL.md? Recommendation: yes, additive, optional.
3. **Promotion threshold:** is "two distinct real cases" the right bar for promoting a generic spike to a profile, or should the owner approve each promotion explicitly (recommended: both — threshold as the trigger, owner as the gate)?
4. (Minor) **`_shared` naming convention:** confirm the on-disk unprefixed names vs the `mala-pata-` prefix SKILL.md references use, before creating new files. [A] prefix is applied at install/mirror.

## Handoff
SHARPEN: resolve open decisions 1-3, then `/mala-pata-triage spike-catalog` (expected lane: organic; one-unit, docs/skills only). Write-only; no commit made. Durable branch for this doc: `main` (standalone, integration default); add it in your normal PR flow.

Structure: Heilmeier Catechism (DARPA) + Double Diamond (Design Council) + objective-completeness (gap analysis / MECE / ISO 25010) + spike (Cynefin / XP spike). Verdict / size-signal / Left-OUT / Spike-candidates = house method.
