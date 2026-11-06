# Route resolution: actual route + per-phase gate partition — single source of truth

Canonical rule for how a roadmap orchestrator decides, per phase, which lane a
NOT-done phase will really take, and which phases it can batch-automate vs. which
need a human. Consumers (`mala-pata-roadmap-orchestrate`,
`mala-pata-roadmap-orchestrate-start`) apply THIS verbatim and never re-derive it.

## Principle

Loops always need a human at their gates, so a loop phase cannot be batch-automated.
That is a property of the PHASE, not of the roadmap: a roadmap is never refused as a
whole. The gate is **per phase**, runs AFTER live state derivation, and looks only at
phases that are NOT `done`. A roadmap's `Tentative route` is a FORECAST (triage
re-decides on arrival); the gate prefers evidence of the re-decided route.

## Order (never reorder)

1. Derive every phase's live state first (`_shared/mala-pata-git-truth.md`).
2. Drop `done` phases from planning. They stay as rows and still satisfy dependents.
3. Resolve the ACTUAL route of each remaining `code` phase (tiers below).
4. Partition, then plan waves over the orchestrable set only.

## Route resolution tiers (cheapest first; NEVER run triage in a planner)

1. **Kickoff exists**: read `mala-pata/kickoffs/<slug>.md` from the integration branch (read-only, `git show <integration>:mala-pata/kickoffs/<slug>.md`) AND, best-effort, from the phase branch (`git show <branch>:mala-pata/kickoffs/<slug>.md`). **Precedence: when both exist and disagree, the PHASE BRANCH wins** (it holds the latest re-triage); a single copy is used as is. Tag `Route source = kickoff` either way and, on a disagreement, say so in the row's Note (`kickoff differs: integration=<route>, phase branch=<route>`). Frontmatter `route: organic` → `organic`. A `profile:` field with no `route:` → `loop` (genuine loop). A kickoff carrying NEITHER `route:` NOR `profile:` is treated as NO kickoff: fall to tier 2 (forecast, provisional) and flag it in the Note (`kickoff has no route/profile`).
2. **No kickoff anywhere**: use the roadmap's forecast and tag the `Route source` as `forecast`. A `forecast` route is PROVISIONAL by definition (the value stays exactly `forecast`; provisional-ness lives in this rule, not in the value). Forecast `organic` / `shot` → plannable. Forecast `loop*` → `loop?` (unconfirmed loop).
3. `ops` phases have no route (`—`); they are never partitioned as loop.

A phase's `Route source` (`kickoff` | `forecast`) is always shown. The planner's route is advisory: the
executor re-runs `/mala-pata-triage` per READY code phase and re-decides.

## Partition

| Set | Members | Treatment |
|---|---|---|
| orchestrable | `organic` / `shot` code phases, plus `ops` attestation rows | planned into waves |
| needs-human | `loop` (kickoff `profile:`) and `loop?` (forecast loop, no kickoff) | EXCLUDED from waves, flagged `⚑ needs a human` |

- A `loop?` is excluded and flagged `forecast loop, not yet triaged`. Hint: `/mala-pata-triage <slug>` first (it may re-decide to organic; the next run then sees the kickoff), then `/mala-pata-loop` + `/mala-pata-loop-start` if it stays loop.
- A needs-human phase is not `done`, so its dependents are `✗ blocked` with Note `waits for phase <n>`. They stay in the DAG; independent branches still orchestrate.
- A needs-human phase that is also `deferred` stays `deferred` (deferral wins).
- Round forecast stops at the first chain that goes through a needs-human phase; state `rounds beyond <N> require phase <n> (human)`.

## Outcomes (never "Refused")

- Zero non-done phases → the existing all-done report.
- At least one orchestrable phase → the normal wave plan / run, with needs-human phases listed as warnings.
- Orchestrable set empty AND needs-human set non-empty → the all-need-a-human report (`Needs you`): nothing to orchestrate, no executor handoff. Phases that are only `ops` or blocked-on-ops are the normal plan, not this case.

## Runtime guard (executor)

A phase resolved as orchestrable that triage upgrades to loop at execution time is
PAUSED, never auto-run, and reported `⚑ needs a human` (Note `became loop at triage`).
Other orchestrable phases proceed; its dependents stay blocked until the human lands it.
