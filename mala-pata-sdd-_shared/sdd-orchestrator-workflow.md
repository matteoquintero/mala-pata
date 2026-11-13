# Mala Pata SDD — Orchestrator Manual (owned, self-contained)

The SDD lane of the mala-pata suite is the **loop**. It is fully mala-pata-owned and runs with NO gentle-ai SDD engine (gentle-ai 4.x retired SDD). This file is the lazy-load orchestration surface the global `~/.claude/CLAUDE.md` points at; the authoritative, executable detail lives in the loop skills below — this manual only indexes them.

## The lane

- `/mala-pata-loop` writes the kickoff (the brief) → `mala-pata/kickoffs/<change-name>.md`.
- `/mala-pata-loop-start` runs the cycle from the kickoff, one phase at a time, interactive with a gate per phase.
- Routing into the lane: `/mala-pata-research` → `/mala-pata-triage` (SDD = the loop lane, chosen when design is genuinely open). The ODD lane (`/mala-pata-organic`) is separate.

## Phases (order)

`explore → propose → spec → design → tasks → preview → apply → verify → archive`

Spec and design run sequentially (design AFTER spec). **Preview** is a mandatory human gate between tasks and apply (native phase, `sdd-preview`).

## Executors (dedicated registered agents)

Each phase is a mala-pata-owned agent dispatched by `subagent_type`:
`mala-pata-sdd-{explore,propose,spec,design,tasks,apply,verify,archive}` + `sdd-preview` for preview. Each agent's `agent.md` carries that phase's tool/model scoping and loads its `~/.agent-skills/mala-pata-sdd-<phase>/SKILL.md` + `~/.agent-skills/_shared/sdd-phase-common.md`. Agents are registered as symlinks in `~/.claude/agents/`. There are NO gentle `sdd-*` agents and NO `PreToolUse:Agent` preflight hook.

## State (in-house, no native engine)

State is derived from engram topics `sdd/<change-name>/*` + the kickoff file + git — see `~/.agent-skills/_shared/sdd-state.md`. Retrieval, persistence and the return envelope: `~/.agent-skills/_shared/sdd-phase-common.md`. Store is **engram-only** (no OpenSpec, no hybrid). There is NO `gentle-ai sdd-status` / `sdd-continue` / `sdd-archive-compose` / `sdd-task-result` / `sdd-preflight-hook`; apply/archive/verify derive `applyState` and dependencies from the `tasks` checkboxes + topic presence + git.

## Topic keys

`sdd/<change>/{kickoff,explore,proposal,spec,design,tasks,preview,apply-progress,verify-report,archive-report}` · `sdd-init/<project>` · `sdd/<project>/testing-capabilities`.

## Model assignments

Per the **Model Assignments** table in `~/.claude/CLAUDE.md` (overriding each agent's default when they differ). The preview phase uses `opus` (the most judgment-heavy phase).

## Strict TDD

Resolved by `/mala-pata-loop`'s init guard (`sdd-init/<project>` + `sdd/<project>/testing-capabilities`) and forwarded to apply/verify. When active: RED → GREEN → REFACTOR, with observed evidence.

## Delivery

PR / merge-to-feature / fast-forward-to-umbrella is decided at the loop's close (`/mala-pata-loop-start` Step 4). RDD does NOT run in the SDD lane — it belongs to the ODD/organic lane.
