# SDD Phase — Common Protocol (mala-pata, self-contained)

Boilerplate identical across all mala-pata SDD phase skills. Each phase sub-agent MUST load this alongside its phase-specific `SKILL.md`.

> **Self-contained — no native SDD engine.** This is the mala-pata-owned replacement for gentle-ai's retired `sdd-phase-common.md`. There is NO `gentle-ai sdd-status`, NO `gentle-ai sdd-task-result`, NO native `StatusV2Projection`. State is in-house: engram topics + the kickoff file + git reality. See `_shared/sdd-state.md` for the state model this file assumes.
> **Store is always engram.** OpenSpec and hybrid are retired for the mala-pata loop. Every phase reads and writes its artifact as an engram topic. There is nothing to detect and nothing to branch on.

Executor boundary: every SDD phase agent is an EXECUTOR, not an orchestrator. Do the phase work yourself. Do NOT launch sub-agents, do NOT call `delegate`/`task`, and do NOT bounce work back unless the phase skill explicitly says to stop and report a blocker.

## A. Skill Loading

1. Check if the orchestrator injected a `## Skills to load before work` block in your launch prompt. If yes, read those exact `SKILL.md` files before task-specific work.
2. If no skills block was provided, check for `SKILL: Load` instructions. If present, load those exact skill files.
3. If neither was provided, search for the skill registry as a fallback:
   a. `mem_search(query: "skill-registry", project: "{project}")` — if found, `mem_get_observation(id)` for full content.
   b. Fallback: read `.atl/skill-registry.md` from the project root if it exists.
   c. From the registry's skills index, match triggers to your task and read the exact listed `SKILL.md` paths.
4. If no registry exists, proceed with your phase skill only.

NOTE: the preferred path is (1) — exact skill paths selected by the orchestrator. Paths (2) and (3) are fallbacks. Searching the registry is SKILL LOADING, not delegation. If `## Skills to load before work` is present, IGNORE redundant `SKILL: Load` instructions.

## B. Artifact Retrieval (engram topics)

**`sdd-research` collector exception:** this output-only collector does not read local artifacts, repository state, or engram state. Sections B and C do not apply to it; every other phase follows them unchanged.

The orchestrator (`/mala-pata-loop-start`) injects the **change-name** (`<change-name>`), the **project**, and the **kickoff absolute path**. Each SDD artifact lives at the engram topic `sdd/<change-name>/<artifact-type>`:

| artifact | topic |
|---|---|
| explore | `sdd/<change-name>/explore` |
| proposal | `sdd/<change-name>/proposal` |
| spec | `sdd/<change-name>/spec` |
| design | `sdd/<change-name>/design` |
| tasks | `sdd/<change-name>/tasks` |
| apply-progress | `sdd/<change-name>/apply-progress` |
| verify-report | `sdd/<change-name>/verify-report` |

For each artifact your phase requires:

1. `mem_search(query: "sdd/<change-name>/<artifact-type>", project: "{project}")` → get the observation id.
2. `mem_get_observation(id)` for the FULL content.

**CRITICAL**: `mem_search` returns ~300-char PREVIEWS, not full content. You MUST call `mem_get_observation(id)` for EVERY artifact. Skipping this produces wrong output. Do NOT use search previews as source material.

**Run all retrievals in parallel** — do NOT read sequentially.

A required topic that does not exist means the artifact does not exist. Report it as a blocker; do not fabricate it. Always also `Read` the kickoff at the absolute path you were given, for the verbatim What / Why / DoD.

## C. Artifact Persistence (engram)

Every artifact-producing phase other than the output-only `sdd-research` collector MUST persist its artifact. Skipping this BREAKS the pipeline — downstream phases will not find your output.

```
mem_save(
  title: "sdd/<change-name>/<artifact-type>",
  topic_key: "sdd/<change-name>/<artifact-type>",
  type: "architecture",
  project: "{project}",
  capture_prompt: false,
  content: "{your full artifact markdown}"
)
```

- `topic_key` enables upserts — saving again updates, not duplicates.
- `capture_prompt: false` is mandatory: SDD artifacts are automated pipeline outputs, not human/proactive memory. If an older engram schema does not expose the field, omit it rather than failing.
- Read back the write (`mem_search` the topic) before reporting success. If engram is unavailable, preserve your output inline in the return envelope and report persistence as pending — never claim a save that did not land.

Verification reports are optional diagnostics. Persist honest results; preserve historical findings and never fabricate a pass to enable archive.

## D. Return Envelope

> **CRITICAL — Response ordering**: Your FINAL output MUST be text (the return envelope), NOT a tool call. If you need to `mem_save`, do it BEFORE your final text response. Do NOT call `mem_session_summary` — that is for top-level agents only. When a sub-agent's last action is a tool call, the parent receives only the tool result and your text is lost.

Every phase MUST return this structured envelope to the orchestrator:

- `status`: `success`, `partial`, or `blocked`
- `executive_summary`: 1–3 sentence summary of what was done
- `detailed_report`: (optional) full phase output, or omit if already inline
- `artifacts`: the engram topic(s) written
- `next_recommended`: the next SDD phase to run, or `none`
- `risks`: risks discovered, or `None`
- `skill_resolution`: `paths-injected` | `fallback-registry` | `fallback-path` | `none`

**Validation is in-house.** There is no `gentle-ai sdd-task-result`. The orchestrator validates your result by (a) checking this envelope is present and `status` is not `blocked`, and (b) reading back the engram topic you claim you wrote. A phase that reports success but whose topic does not read back FAILS the orchestrator's gate — the orchestrator re-runs the phase once with that feedback, it does not silently continue.

Example:

```markdown
**Status**: success
**Summary**: Proposal created for `<change-name>`. Defined scope, approach, and rollback plan.
**Artifacts**: engram `sdd/<change-name>/proposal`
**Next**: sdd-spec or sdd-design
**Risks**: None
**Skill Resolution**: paths-injected — 3 skills (react-19, typescript, tailwind-4)
```

## E. Review Workload Guard

SDD must protect reviewer cognitive load, not only generate tasks.

- The default PR review budget is **400 changed lines** (`additions + deletions`), authored text only (generated goldens excluded from authored risk count).
- The orchestrator caches a delivery strategy at session start: `ask-on-risk` (default), `auto-chain`, `single-pr`, or `exception-ok`. Those four are the whole domain. Any other value is invalid — report it and stop; do not map it to the nearest branch.
- `sdd-tasks` MUST forecast whether the planned work may exceed the budget, with exact plain-text guard lines: `Decision needed before apply: Yes|No`, `Chained PRs recommended: Yes|No`, and `400-line budget risk: Low|Medium|High`.
- If the forecast is high, `sdd-tasks` recommends chained/stacked PRs using deliverable work units.
- `sdd-apply` MUST NOT start oversized work unless the strategy resolves to chained/stacked slices or an explicitly accepted `size:exception`.
- Each chained slice has a clear start, clear finish, autonomous scope, verification, and reasonable rollback.

This guard reduces reviewer burnout and keeps delivery safe. It is not optional process noise.

## F. Key Learnings Closing

Close your **final report message** (the return envelope) with a `## Key Learnings` section to enable engram passive capture.

**Format**: numbered list with 1–5 items. Each item is a standalone factual sentence, ≥20 characters and ≥4 words.

```markdown
## Key Learnings

1. Async validation in the apply phase caught a race condition in concurrent writes.
2. Golden test regeneration for system prompts requires the `-update` flag before re-run.
```

This applies to your final text response to the orchestrator, not intermediate tool outputs or artifact content.
