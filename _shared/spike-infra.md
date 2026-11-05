# Infra-spike — mala-pata single source of truth

The **infra-spike** profile of `/mala-pata-research --spike`: the read-only probe to run when a
change is blocked by INFRASTRUCTURE — it needs new provisioning (object storage, a queue, an
external integration) or would hit a capacity ceiling (connection pool, workers, rate/storage
limits). It is a normal spike (read-only, scope-boxed, produces a `## Finding`, re-enters via
triage); this file is its assessment checklist. **First entry of the future spike-profile catalog.**

## When
A phase/objective whose approach is unknown BECAUSE of infra: "can we deliver N×M at volume?",
"do we need object storage / a queue / an external integration?", "does this fit under the
current pool/worker ceiling?". Detected when the objective-completeness **Infrastructure lens
forks** the approach. It is NOT a lane — it produces a decision, then the real work routes by
size × uncertainty.

## The probe (read-only — measure and check, NEVER provision)
1. **Current capacity + the ceiling.** Measure what existing infra handles and where it caps:
   connection pool size, worker/queue capacity, storage/rate limits, timeouts — with evidence
   (config, code, metrics). State the ceiling as a number whenever you can.
2. **Reuse-first.** Does existing infra already cover the need? Prove it is insufficient against
   that ceiling BEFORE proposing anything new.
3. **New-infra feasibility + cost.** For each candidate (object storage, queue, external
   integration, …): is it already in the stack? what would adding it take (provisioning,
   credentials, ops/maintenance)? rough effort + recurring cost. A candidate that needs
   credentials or ops nobody owns is a red flag — name it.
4. **Options + tradeoffs.** Lay the viable infra options side by side (capacity headroom, effort,
   cost, ops burden, blast radius) so the decision becomes decidable.

## Finding (the deliverable)
`## Finding`: **recommended infra approach** · **rejected options** (with the ceiling / cost
evidence) · **residual unknowns** (what still needs measuring, e.g. in prod) · **effect on
decomposition** (does it add a provisioning phase? change the slices or their order?).
**Exit criterion:** *"we can name the infra approach and the slices it implies"* OR *"infeasible
within the current infra budget"* (→ RECONSIDER). Refuse an infra-spike with no exit criterion.

## Re-entry
`/mala-pata-triage` reads the finding: approach now known → the phase routes organic/loop;
decomposition changed (e.g. a provisioning phase) → roadmap; infeasible → RECONSIDER.
