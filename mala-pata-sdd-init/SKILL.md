---
name: mala-pata-sdd-init
description: "Trigger: sdd init, iniciar sdd. Initialize SDD context, testing capabilities, and skill registry in engram."
disable-model-invocation: true
user-invocable: false
license: MIT
metadata:
  author: matteoquintero
  version: "3.1"
  delegate_only: true
---

## Execution Role

Confirm your role before acting. You are the dedicated `sdd-init` sub-agent unless you loaded this skill directly through the `skill()` tool.

- If you are the `sdd-init` sub-agent, continue with the phase work below. Do not delegate. Do not call the Skill tool.
- If you loaded this skill through the `skill()` tool, you are the orchestrator. Stop here and delegate to the dedicated `sdd-init` sub-agent using your platform's delegation primitive (for example, `task(...)` or a sub-agent invocation).

## Language Domain Contract

Generated technical artifacts default to English. Do not inherit the user's conversational language or the active persona's regional voice for SDD artifacts unless the user explicitly requests that artifact language or the project convention requires it.

If technical artifacts are explicitly requested in another language, use a neutral/professional register unless the user explicitly requests a different tone or regional variant.

Public/contextual comments follow the target context language by default. Explicit user language or tone overrides win; otherwise use a neutral/professional register unless the target context clearly calls for another tone or regional variant.

## Activation Contract

Run this phase when the orchestrator/user asks to initialize SDD in a project. You are the phase executor: do the work yourself, do not delegate, and do not behave like the orchestrator.

## Hard Rules

- Detect the real stack, conventions, architecture, and testing tools; never guess.
- Persistence is engram-only. Do **not** create `openspec/`.
- Persist the project context to engram as `sdd-init/{project}` (the init-guard topic the lanes check).
- Always persist testing capabilities separately to engram as `sdd/{project}/testing-capabilities`.
- Always build `.atl/skill-registry.md`; also save `skill-registry` to Engram when available.
- Use `capture_prompt: false` for automated SDD/config saves when supported; omit it if the tool schema lacks it.

## Decision Gates

| Input | Action |
|---|---|
| (always) | Save project context and testing capabilities to Engram. |
| explicit `strict_tdd: false` marker | Preserve `strict_tdd: false`. |
| explicit `strict_tdd: true` marker and an explicit workspace-level test command covers every in-scope project | Use `strict_tdd: true`. |
| explicit `strict_tdd: true` marker without that workspace-level command | Fail closed to `strict_tdd: false` and explain that downstream execution requires a workspace-wide command. |
| no marker, non-empty discovered project set, and an explicit workspace-level test command covers every in-scope project | Default `strict_tdd: true`. |
| zero projects discovered or no explicit workspace-level test command covers every in-scope project | Set `strict_tdd: false`; preserve and report every project-local command. Explain the no-runner or workspace-wide-command fallback. |

## Execution Steps

1. Identify the authoritative workspace root. Before classifying a stack or applying any no-runner fallback, discover every in-scope project root from that root using the bounded rules in `references/init-details.md`.
2. Inspect each discovered project for `package.json`, `go.mod`, `pyproject.toml`, `Cargo.toml`, CI, and lint/test config; preserve its relative path and summarize its stack/conventions.
3. Detect each project's test runner and command, test layers, coverage, linter, type checker, and formatter. Aggregate those project-to-tool associations in the one workspace-level result; never select one project runner for the workspace.
4. Resolve Strict TDD from an agent marker only after every discovered project has been evaluated. Set it to true only for a non-empty discovered project set when one explicit workspace-level test command covers every in-scope project. Preserve and report every project-local command, including missing or independent commands; those local facts do not override a workspace-level command that covers every in-scope project. Use the false fallback only when zero projects are discovered or no explicit workspace-level test command covers every in-scope project.
5. Initialize engram persistence (project context + testing capabilities).
6. Build `.atl/skill-registry.md` using the skill-registry scan rules.
7. Persist testing capabilities and project context.
8. Return the structured initialization envelope.

## Output Contract

Return `status`, `executive_summary`, `artifacts`, `next_recommended`, and `risks`. Include project, stack, persistence mode, Strict TDD status, testing capability table, saved observation IDs/paths, registry path, and next `/sdd-explore` or `/sdd-new` step.

## References

- [references/init-details.md](references/init-details.md) — detection checklist, Engram payloads, and output templates.
