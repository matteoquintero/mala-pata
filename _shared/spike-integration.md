# Integration-spike — mala-pata single source of truth

The **integration-spike** profile of `/mala-pata-research --spike`: the read-only probe to run when
a change is blocked by an EXTERNAL SYSTEM — its contract, limits or failure behavior decide
whether to call it directly, wrap it in an adapter, go async, or build instead of buy. It is a
normal spike (read-only, scope-boxed, produces a `## Finding`, re-enters via triage); this file is
its assessment checklist. Index: `_shared/mala-pata-spike-catalog.md`.

## When
A phase/objective whose approach is unknown BECAUSE of an external system: "can `<service>` do
`<capability>` at our volume?", "what are `<service>`'s auth, rate, idempotency and failure
semantics?", "adapter vs SDK vs async?". Detected when the objective-completeness **Integrations
lens forks** the approach. It is NOT a lane — it produces a decision, then the real work routes by
size × uncertainty.

## The probe (read-only — read contracts and docs, NEVER call the live system with side effects)
1. **Contract surface.** From authoritative sources (provider docs, schema/spec, versioning
   policy) list the endpoints/events the objective needs, auth model, payload shapes and limits.
   Cite sources; the provider's documentation is the authority, not the current code.
2. **Existing coupling.** Inventory adapters, clients and handlers already in the repo for
   `<service>` or its siblings; reuse-first before a new adapter.
3. **Failure semantics.** Timeouts, retries, idempotency, ordering and duplicate guarantees,
   delivery guarantees for callbacks, sandbox availability, SLA. Name what the system does when
   `<service>` is down or slow.
4. **Cost, ownership, risk.** Credentials needed and who holds them, per-call cost/quotas,
   lock-in, data leaving our boundary. A dependency needing credentials or a contract nobody owns
   is a red flag — name it.
5. **Options + tradeoffs.** Direct call vs adapter/anti-corruption layer vs async/outbox vs
   build-vs-buy; compare effort, coupling, failure blast radius, testability.

## Finding (the deliverable)
`## Finding`: **recommended integration approach** · **rejected options** (with the
contract/limit evidence) · **residual unknowns** (e.g. behavior only observable in a sandbox with
credentials) · **effect on decomposition** (contract stub / tracer bullet first? separate adapter
phase? an ops phase for credentials?). **Exit criterion:** *"we can name the integration approach
and its slices"* OR *"the contract cannot satisfy the objective"* (→ RECONSIDER). Refuse an
integration-spike with no exit criterion.

## Re-entry
`/mala-pata-triage` reads the finding: approach now known → the phase routes organic/loop (an
unproven integration may place a tracer bullet first per the roadmap rule); decomposition changed
→ roadmap; infeasible → RECONSIDER.
