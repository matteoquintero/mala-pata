# Phase-status marker — how an orchestrated tab signals it finished

In wave orchestration (`/mala-pata-roadmap-orchestrate-start`, `/mala-pata-organic-orchestrate-start`) each phase runs in its own Claude tab and STOPS at PR-ready. The orchestrator is a SEPARATE session: it cannot read the tab's scrollback. Inferring "done" from git alone is ambiguous (a clean + pushed worktree also looks that way mid-cycle). So each tab drops an explicit **phase-status marker** as its LAST action, and the orchestrator watches for it.

## The marker file

- **Path (per-worktree):** `<ABS-worktree>/mala-pata/.phase-status.json`. For a lane with no worktree (standalone `shot`), `<ABS-repo>/mala-pata/.phase-status.json`.
- **Transient:** it is run-state, NOT part of the change. NEVER include it in a commit pathspec (lanes commit by explicit pathspec, so it is naturally excluded); the orchestrator deletes it in central cleanup.
- **Written only on request:** a lane writes it when its launch prompt says it is an orchestrated phase (the orchestrate-start launch directive asks for it). A standalone run skips it.

## When to write it

As the **LAST action** before the tab stops — at the PR-ready stop (orchestrated tabs do NOT merge/clean up), OR when the phase parks/fails. Write it once; overwrite on a later state change.

## Schema

```json
{
  "phase": "<change-name / slug>",
  "status": "pr-ready | parked | failed",
  "reason": "<one line when parked/failed, else empty>",
  "branch": "<type>/<change-name>",
  "base": "<branch_base / umbrella>",
  "head_sha": "<short sha of the branch tip>",
  "pushed": true,
  "smoke": "pass | fail | needs-human | n/a",
  "rdd": "passive | granted | under_budget | declined | consent-pending | n/a",
  "ci": "green | red | none | pending",
  "evidence": "<ABS path to the evidence folder, or n/a>",
  "handoff": "<the 'For the orchestrator' notes: DB fork, merge-conflict warning, flaky test, etc. — verbatim, the same content the close prints>",
  "parked_decisions": [{"question": "<what was asked>", "options": "<the choices>", "default": "<safe default taken, or \"blocked\" when none>", "blocks": "<what it holds up>"}],
  "finished_at": "<ISO 8601 local time with offset>"
}
```

`status` values:
- **pr-ready** — branch pushed, worktree clean, checks green, smoke pass/n-a, RDD not declined/ pending; safe for the central merge gate.
- **parked** — stopped on a gate that is not PR-ready (red verify/CI, smoke fail/needs-human, open decision, RDD consent pending/declined, triage upgraded to loop). `reason` says which. NOT merged.
- **failed** — the cycle could not complete. `reason` says why.

`parked_decisions[]` (per `_shared/mala-pata-unattended-policy.md`): a run that hit a human gate while `RUN-MODE: unattended` PARKS it here instead of blocking — the orchestrator surfaces the queue once at the end. A non-orchestrated unattended run writes the mirror file `mala-pata/parked-decisions/<change>.md` instead. A consent/destructive decision parks with `default: blocked` (never a silent default).

## Orchestrator side

The orchestrate-start, in its WAIT step, polls each phase's marker at `<ABS-worktree>/mala-pata/.phase-status.json` (bounded cadence, never busy-loop) instead of only inferring from git. A present marker = the tab finished; its `status` + `handoff` drive the merge gate directly (no need for the human to relay the "For the orchestrator" notes). Corroborate `pr-ready` against git (pushed tip + clean) before merging. When every wave phase has a terminal marker (pr-ready/parked/failed), run the central delivery. Report to the human each time a marker lands: `phase <x> <status> · <n>/<total>`.
