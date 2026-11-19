# SDD State — in-house state model (mala-pata, self-contained)

Mala-pata-owned replacement for gentle-ai's retired `sdd-status-contract.md` and the native `gentle-ai.sdd-status/v2` engine. The mala-pata loop derives SDD state ITSELF, from three sources it already owns — no `gentle-ai sdd-status`, no `sdd-continue`, no `StatusV2Projection`, no native dispatcher.

> **Why this exists.** gentle-ai 4.x retired SDD. The loop lane survives as a mala-pata-owned pipeline. This file is the contract every loop phase and `/mala-pata-loop-start` reads so state is derived the same way everywhere, from in-house sources, the same way `/mala-pata-roadmap-radar` and `/mala-pata-radar` already derive status from git.

## The three state sources

1. **Engram topics** `sdd/<change-name>/<artifact-type>` — the artifacts themselves (`explore`, `proposal`, `spec`, `design`, `tasks`, `apply-progress`, `verify-report`). Presence of a topic = that artifact exists. Store is always engram (OpenSpec/hybrid retired).
2. **The kickoff file** `mala-pata/kickoffs/<change-name>.md` (resolved from the repo root, `git rev-parse --show-toplevel`) — the verbatim What / Why / DoD / Decisions / `tdd_mode` / `base`. The kickoff is the source of truth for the change's intent; `/mala-pata-loop` wrote it.
3. **Git reality** — via `_shared/git-truth.md`. The branch, the worktree, what is actually committed/merged. Never trust a cached claim of done over git.

State is never a native JSON projection. It is DERIVED from these three on every read, live.

## Change selection

- A change-name (slug) is passed by `/mala-pata-loop-start`. Use it as-is; it matches the kickoff filename and the engram topic prefix.
- If no slug is passed and exactly one kickoff with `route: loop` is active → use it. If several match or it is unclear → ask the user to choose; do not guess.
- If nothing resolves → report that no loop change is active and point to `/mala-pata-loop <objective>`.

## Phase order (the loop pipeline)

`explore → propose → spec → design → tasks → preview → apply → verify → archive`

Spec and design run sequentially (design AFTER spec, never in parallel). Preview is a mandatory human gate between tasks and apply.

## Deriving artifact + dependency + apply state

Derive each on read — do not persist a status projection:

- **Artifact state** per phase: `done` if its engram topic exists and reads back non-empty; `missing` otherwise. (`partial` only if a phase explicitly persisted an incomplete marker.)
- **Dependency gate**: a phase is `ready` only when every upstream artifact it needs exists.
  - `propose` needs `explore` (explore optional for a trivial change — the kickoff carries enough; loop-start decides).
  - `spec` needs `proposal`. `design` needs `proposal` (+ `spec`, runs after it). `tasks` needs `spec` + `design`.
  - `apply` needs `tasks` (and preview approved — a human gate, not an artifact). `verify` needs `apply-progress`. `archive` needs `verify-report` green (or an explicit human decision to close incomplete).
- **Apply state** (from the `tasks` artifact's checkboxes):
  - `blocked`: `tasks` missing, or task selection ambiguous.
  - `ready`: `tasks` exists and at least one implementation task is unchecked `[ ]`.
  - `all_done`: `tasks` exists and every implementation task is checked `[x]`.
- **Blockers vs notes**: a genuine blocker (a missing required upstream artifact) stops the pipeline — report it and stop. An informational diagnostic is a note, never a blocker.

## Edit scope (no native edit-authority)

gentle's `actionContext` / `allowedEditRoots` / `consent` / `sdd-attempt grant` edit-authority machinery is RETIRED and not replaced. The loop's edit scope is simply **its own worktree**: `/mala-pata-loop-start` runs the cycle in a dedicated worktree on the change's branch (same discipline as `/mala-pata-organic-start`). Every phase edits only inside that worktree, referenced by absolute path. There is no per-change edit-authority grant and no consent envelope to relay.

## What each phase reads / writes

| phase | reads | writes (engram topic) |
|---|---|---|
| explore | kickoff | `sdd/<change>/explore` |
| propose | explore (optional) + kickoff | `sdd/<change>/proposal` |
| spec | proposal | `sdd/<change>/spec` |
| design | proposal + spec | `sdd/<change>/design` |
| tasks | spec + design | `sdd/<change>/tasks` |
| preview | tasks + design + spec + proposal + real code | `sdd/<change>/preview` (optional) |
| apply | tasks + spec + design + apply-progress (if exists) | `sdd/<change>/apply-progress` |
| verify | spec + tasks + apply-progress | `sdd/<change>/verify-report` |
| archive | all artifacts | `sdd/<change>/archive-report` |

Retrieval and persistence mechanics are in `_shared/sdd-phase-common.md` (sections B and C).

## No RDD inside the loop

The loop does not run RDD/native review — that belongs to the organic/ODD lane. There is no review-mode read, no consent gate, no receipt here. Delivery (PR/merge) follows ordinary repository policy, decided by the human at the loop's close.
