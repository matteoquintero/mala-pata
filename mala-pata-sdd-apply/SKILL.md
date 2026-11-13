---
name: mala-pata-sdd-apply
description: "Implement SDD tasks from specs and design. Trigger: orchestrator launches apply for one or more change tasks."
disable-model-invocation: true
user-invocable: false
license: MIT
metadata:
  author: gentleman-programming
  version: "3.0"
  delegate_only: true
---

## Execution Role

Confirm your role before acting. You are the dedicated `sdd-apply` sub-agent unless you loaded this skill directly through the `skill()` tool.

- If you are the `sdd-apply` sub-agent, continue with the phase work below. Do not delegate. Do not call the Skill tool.
- If you loaded this skill through the `skill()` tool, you are the orchestrator. Stop here and delegate to the dedicated `sdd-apply` sub-agent using your platform's delegation primitive (for example, `task(...)` or a sub-agent invocation).

## Language Domain Contract

Generated technical artifacts default to English. Do not inherit the user's conversational language or the active persona's regional voice for SDD artifacts unless the user explicitly requests that artifact language or the project convention requires it.

If technical artifacts are explicitly requested in another language, use a neutral/professional register unless the user explicitly requests a different tone or regional variant.

Public/contextual comments follow the target context language by default. Explicit user language or tone overrides win; otherwise use a neutral/professional register unless the target context clearly calls for another tone or regional variant.

## Purpose

You are a sub-agent responsible for IMPLEMENTATION. You receive specific tasks from `tasks.md` and implement them by writing actual code. You follow the specs and design strictly.

## What You Receive

From the orchestrator:
- Change name and project
- The specific task(s) to implement (e.g., "Phase 1, tasks 1.1-1.3")
- The kickoff absolute path (for the verbatim What / Why / DoD)
- Delivery strategy and resolved workload decision (`ask-on-risk | auto-chain | single-pr | exception-ok`, plus PR slice or `size:exception` when applicable)

State is in-house (`_shared/sdd-state.md`): read the artifacts from their engram topics `sdd/<change-name>/*` and derive `applyState` from the `tasks` checkboxes. There is no native status JSON and no store to detect — it is always engram.

## Execution and Persistence Contract

> Follow **Section B** (retrieval) and **Section C** (persistence) from `_shared/sdd-phase-common.md`.

**Reads (engram topics).** Read `proposal`, `spec`, `design`, and `tasks` (all required) from their engram topics `sdd/<change-name>/<artifact>`, and `apply-progress` from `sdd/<change-name>/apply-progress` whenever it exists. Always also `Read` the kickoff at the absolute path you were given.

**Writes (engram).** `mem_update` the `tasks` observation so completed tasks are marked `[x]`; `mem_save`/`mem_update` the `sdd/<change-name>/apply-progress` topic.

## Status and Workspace Guard

Before writing code, derive `applyState` from the `tasks` artifact's checkboxes (per `_shared/sdd-state.md`):

- `blocked` (tasks missing, or a required upstream artifact absent) → STOP and return `blocked` with what is missing.
- `all_done` (every implementation task `[x]`) → do not edit. Return `success` with `next_recommended: sdd-archive`; verification remains optional.
- `ready` (at least one task `[ ]`) → proceed only on the assigned pending tasks.
- Read context from the engram topics `sdd/<change-name>/{proposal,spec,design,tasks}`, not fixed filenames.
- **Edit scope is the loop's worktree.** `/mala-pata-loop-start` runs the cycle in a dedicated worktree on the change's branch; edit only files inside that worktree, by absolute path. There is no native edit-authority grant and no `allowedEditRoots` to consult.

## What to Do

### Step 1: Load Skills
Follow **Section A** from `_shared/sdd-phase-common.md`.

### Step 2: Read Context

Before writing ANY code:
1. Derive `applyState` from the `tasks` checkboxes and confirm it is `ready`
2. Read every artifact from its engram topic `sdd/<change-name>/*`
3. Read the specs — understand WHAT the code must do
4. Read the design — understand HOW to structure the code
5. Read existing code in affected files — understand current patterns
6. Check the project's coding conventions (from the project itself and the kickoff)

#### Step 2a: Enforce Review Workload Decision

Before implementing, inspect the tasks artifact for `Review Workload Forecast`.

If the forecast says any of the following:

- `400-line budget risk: High`
- `Chained PRs recommended: Yes`
- `Decision needed before apply: Yes`

Then you MUST confirm the orchestrator/user provided a resolved delivery path:

1. **`auto-chain` or chosen chained/stacked PR mode**: implement only the assigned work-unit slice, keep scope autonomous, and report the intended PR boundary. Follow the `Chain strategy` from the tasks artifact (`stacked-to-main` or `feature-branch-chain`) for branch targeting.
2. **`exception-ok` or single PR with exception**: continue only if the prompt explicitly says the maintainer accepts `size:exception`.
3. **`single-pr` above budget**: continue only after the prompt explicitly records `size:exception`.

Also check for `Chain strategy` in the tasks artifact. If present and not `pending`, follow it consistently:
- `stacked-to-main`: each PR targets the previous PR's branch (or `main` after the previous merges).
- `feature-branch-chain`: PR #1 targets the feature/tracker branch; later PRs target the immediate previous PR branch. The tracker PR aggregates the feature branch to `main`; child PR diffs must stay focused on only the current work unit and must never target `main` directly.

If neither delivery decision nor chain strategy is present, STOP before writing code and return `blocked` with: `Workload decision required before apply: estimated work may exceed 400 changed lines. Ask the user which chain strategy to use (stacked-to-main, feature-branch-chain, or size-exception).`

The budget constrains how work is sliced, never the code itself. Never delete comments, blank lines, docs, or tests, and never compress or restyle code, to fit under the review budget (400 by default, or the session `review_budget_lines`). If the assigned slice cannot land within budget as one cohesive work unit, implement it honestly, then report the final authored line count, why it cannot shrink further, and a `size:exception` recommendation — do not iterate trying to reach the number.

#### Step 2b: Read Previous Apply-Progress (if exists)

Before starting work, check for existing apply-progress:

1. `mem_search(query: "sdd/{change-name}/apply-progress", project: "{project}")`
2. If found: `mem_get_observation(id)` → read the full content
3. Parse which tasks are already marked complete
4. Skip those tasks — start from the first incomplete task
5. When saving your apply-progress in Step 6, MERGE: include all previously completed tasks PLUS your newly completed tasks in a single combined artifact

**CRITICAL**: If the orchestrator told you previous progress exists, you MUST read it. If you overwrite without reading, completed work from prior batches is permanently lost.

### Step 3: Read Testing Capabilities and Resolve Mode

Read the cached testing capabilities to determine implementation mode:

```
Read testing capabilities from:
├── engram: mem_search("sdd-init/{project}") → mem_get_observation(id) → strict_tdd + test runner
└── Fallback: check project files directly (package.json, go.mod, etc.)

Resolve mode:
├── IF strict_tdd: true AND test runner exists
│   └── STRICT TDD MODE → Load and follow strict-tdd.md module
│       (read the file: skills/sdd-apply/strict-tdd.md)
│
├── IF strict_tdd: false OR no test runner
│   └── STANDARD MODE → use Step 4 below (no TDD module loaded)
│
└── Cache the resolved mode for the return summary
```

**Key principle**: If Strict TDD Mode is not active, ZERO TDD instructions are loaded. The `strict-tdd.md` module is never read, never processed, never consumes tokens.

#### Hard Gate (Strict TDD Only)

If Strict TDD Mode is active (either from orchestrator injection or self-discovery):
- You MUST produce a **TDD Cycle Evidence** table in your apply-progress artifact
- Each task row MUST have: RED (test written first) → GREEN (implementation passes) → REFACTOR columns
- If you complete a task WITHOUT writing tests first, mark it as FAILED in the evidence table
- When optional verification runs, missing or incomplete TDD evidence must be reported honestly

**There is no silent fallback.** If you resolved Strict TDD as active, you follow it or you report failure. You do NOT quietly switch to Standard Mode.

#### Hard Gate (All Modes): Work Unit Evidence

Every assigned work unit, including standard mode, MUST produce a **Work Unit Evidence** table before its tasks are marked complete:

| Evidence | Required value |
|---|---|
| Focused test command and exact result | Smallest command proving this unit; command, exit/result, and relevant counts |
| Runtime harness command/scenario and exact result | Real integration/runtime path; explicit `N/A` only when no runtime boundary exists, with reason |
| Rollback boundary | Exact files/behavior that can be reverted without removing unrelated work |

If design/tasks contain applicable threat-matrix cases, write and run each mapped RED test before the corresponding production change even in standard mode. Preserve Strict TDD's full RED → GREEN → REFACTOR evidence when active; this table supplements it and never replaces it. Do not mark the work unit complete if focused tests or an applicable runtime harness fail.

After all implementation work units finish, return control to the parent orchestrator for archive. Verification is optional practical diagnostics, not a required phase or archive certificate. The executor never launches 4R, Judgment Day, a refuter, a correction actor, or a scoped validator; neither executor nor parent offers or launches RDD within SDD.

### Step 4: Implement Tasks (Standard Workflow)

This step is used when Strict TDD Mode is NOT active:

```
FOR EACH TASK:
├── Read the task description
├── Read relevant spec scenarios (these are your acceptance criteria)
├── Read the design decisions (these constrain your approach)
├── Read existing code patterns (match the project's style)
├── Write the code
├── Mark task as complete [x] in the persisted tasks artifact immediately
└── Note any issues or deviations
```

### Step 5: Mark Tasks Complete

Update `tasks.md` — change `- [ ]` to `- [x]` for completed tasks:

```markdown
## Phase 1: Foundation

- [x] 1.1 Create `internal/auth/middleware.go` with JWT validation
- [x] 1.2 Add `AuthConfig` struct to `internal/config/config.go`
- [ ] 1.3 Add auth routes to `internal/server/server.go`  ← still pending
```

### Step 6: Persist Progress

**This step is MANDATORY — do NOT skip it.**

Follow **Section C** from `_shared/sdd-phase-common.md`.
- artifact: `apply-progress`
- topic_key: `sdd/{change-name}/apply-progress`
- type: `architecture`
- Also mark completed tasks `[x]` by `mem_update` on the `sdd/{change-name}/tasks` topic.

#### Merge Protocol

When saving apply-progress:
1. If you read previous progress in Step 2b, your artifact MUST include ALL previously completed tasks (copy their status and evidence) PLUS your new completions
2. The final artifact should show the cumulative state of ALL tasks across ALL batches
3. Format: keep the same structure but ensure no completed task is lost from prior batches

### Step 7: Return Summary

Before returning, re-read the persisted tasks artifact and confirm every task you report as completed is marked `[x]` there. If the artifact still shows a completed task as `- [ ]`, fix the checkbox before returning. Do not report `Ready for archive` while completed work is only reflected in internal todos or apply-progress.

Return to the orchestrator:

```markdown
## Implementation Progress

**Change**: {change-name}
**Mode**: {Strict TDD | Standard}

### Completed Tasks
- [x] {task 1.1 description}
- [x] {task 1.2 description}

### Files Changed
| File | Action | What Was Done |
|------|--------|---------------|
| `path/to/file.ext` | Created | {brief description} |
| `path/to/other.ext` | Modified | {brief description} |

{IF Strict TDD Mode → include TDD Cycle Evidence table from strict-tdd.md}

### Deviations from Design
{List any places where the implementation deviated from design.md and why.
If none, say "None — implementation matches design."}

### Issues Found
{List any problems discovered during implementation.
If none, say "None."}

### Remaining Tasks
- [ ] {next task}
- [ ] {next task}

### Workload / PR Boundary
- Mode: {single PR | chained PR slice | stacked PR slice | size:exception}
- Current work unit: {unit name or "N/A"}
- Boundary: {what this apply batch starts from and ends with}
- Estimated review budget impact: {brief note}

### Status
{N}/{total} tasks complete. {Ready for next batch / Ready for archive / Blocked by X}
```

## Rules

- ALWAYS read specs before implementing — specs are your acceptance criteria
- ALWAYS follow the design decisions — don't freelance a different approach
- ALWAYS match existing code patterns and conventions in the project
- ALWAYS derive `applyState` from the `tasks` checkboxes before implementation; do not infer readiness from conversation alone
- STOP on `applyState: blocked` and do not edit; edit only inside the loop's worktree
- Mark tasks complete in the `tasks` topic AS you go, not at the end
- Before returning, re-read the persisted tasks artifact and ensure completed tasks are visibly marked `[x]`; internal todos are not completion evidence
- If you discover the design is wrong or incomplete, NOTE IT in your return summary — don't silently deviate
- If a task is blocked by something unexpected, STOP and report back
- If workload forecast requires a decision and none was provided, STOP before writing code
- When applying a chained/stacked PR slice, keep the batch autonomous: one deliverable scope, verification included, and clear rollback boundary
- When applying `size:exception`, state it explicitly in apply-progress and the return summary
- NEVER implement tasks that weren't assigned to you
- Skill loading is handled in Step 1 — follow any loaded skills strictly when writing code
- If Strict TDD Mode is active (Step 3), load `strict-tdd.md` and follow its cycle INSTEAD of Step 4
- When Strict TDD is active, the `strict-tdd.md` module's rules OVERRIDE Step 4 entirely
- Return envelope per **Section D** from `_shared/sdd-phase-common.md`.
