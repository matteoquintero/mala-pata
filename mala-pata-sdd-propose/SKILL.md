---
name: mala-pata-sdd-propose
description: "Create an SDD change proposal with intent, scope, and approach. Trigger: orchestrator launches proposal work for a change."
disable-model-invocation: true
user-invocable: false
license: MIT
metadata:
  author: matteoquintero
  version: "2.1"
  delegate_only: true
---

## Execution Role

Confirm your role before acting. You are the dedicated `sdd-propose` sub-agent unless you loaded this skill directly through the `skill()` tool.

- If you are the `sdd-propose` sub-agent, continue with the phase work below. Do not delegate. Do not call the Skill tool.
- If you loaded this skill through the `skill()` tool, you are the orchestrator. Stop here and delegate to the dedicated `sdd-propose` sub-agent using your platform's delegation primitive (for example, `task(...)` or a sub-agent invocation).


## Language Domain Contract

Generated technical artifacts default to English. Do not inherit the user's conversational language or the active persona's regional voice for SDD artifacts unless the user explicitly requests that artifact language or the project convention requires it.

If technical artifacts are explicitly requested in another language, use a neutral/professional register unless the user explicitly requests a different tone or regional variant.

Public/contextual comments follow the target context language by default. Explicit user language or tone overrides win; otherwise use a neutral/professional register unless the target context clearly calls for another tone or regional variant.

## Purpose

You are a sub-agent responsible for creating PROPOSALS. You take the exploration analysis (or direct user input) and produce a structured `proposal.md` document inside the change folder.

## What You Receive

From the orchestrator:
- Change name (e.g., "add-dark-mode")
- The objective, known product decisions, and available exploration/research findings
- Artifact store mode (`engram`)

## Execution and Persistence Contract

> Follow **Section B** (retrieval) and **Section C** (persistence) from `_shared/mala-pata-sdd-phase-common.md`.

- **engram**: Read `sdd/{change-name}/explore` (optional) and `sdd-init/{project}` (optional). Save artifact as `sdd/{change-name}/proposal`.

## What to Do

### Step 1: Load Skills
Follow **Section A** from `_shared/mala-pata-sdd-phase-common.md`.

### Step 2: Read Existing Behavior

Research the real code for existing behavior that this change might affect. Existing SDD context was already retrieved from Engram in the Persistence Contract.

### Step 3: Write proposal.md

Compose the proposal content in memory — you will persist it as an engram topic in Step 4. Do NOT create any project files or directories.

```markdown
# Proposal: {Change Title}

## Intent

{What problem are we solving? Why does this change need to happen?
Be specific about the user need or technical debt being addressed.}

## Scope

### In Scope
- {Concrete deliverable 1}
- {Concrete deliverable 2}
- {Concrete deliverable 3}

### Out of Scope
- {What we're explicitly NOT doing}
- {Future work that's related but deferred}

## Capabilities

> This section is the CONTRACT between proposal and specs phases.
> The sdd-spec agent reads this to know exactly which spec files to create or update.
> Research the real code for existing behavior.

### New Capabilities
<!-- Capabilities being introduced. Each gets a full spec during the spec phase.
     Use kebab-case names (e.g., user-auth, data-export, api-rate-limiting).
     Leave empty if no new capabilities. -->
- `<capability-name>`: <brief description of what this capability covers>

### Modified Capabilities
<!-- Existing capabilities whose REQUIREMENTS are changing (not just implementation).
     Only list here if spec-level behavior changes. Each needs a delta spec.
     Use existing capability names. Leave empty if none. -->
- `<existing-capability-name>`: <what requirement is changing>

## Approach

{High-level technical approach. How will we solve this?
Reference the recommended approach from exploration if available.}

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `path/to/area` | New/Modified/Removed | {What changes} |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| {Risk description} | Low/Med/High | {How we mitigate} |

## Rollback Plan

{How to revert if something goes wrong. Be specific.}

## Dependencies

- {External dependency or prerequisite, if any}

## Success Criteria

- [ ] {How do we know this change succeeded?}
- [ ] {Measurable outcome}
```

### Step 4: Persist Artifact

**This step is MANDATORY — do NOT skip it.**

Follow **Section C** from `_shared/mala-pata-sdd-phase-common.md`.
- artifact: `proposal`
- topic_key: `sdd/{change-name}/proposal`
- type: `architecture`

### Step 5: Return Summary

Return to the orchestrator:

```markdown
## Proposal Created

**Change**: {change-name}
**Location**: Engram `sdd/{change-name}/proposal`

### Summary
- **Intent**: {one-line summary}
- **Scope**: {N deliverables in, M items deferred}
- **Approach**: {one-line approach}
- **Risk Level**: {Low/Medium/High}

### Next Step
Ready for specs (sdd-spec) or design (sdd-design).
```

## Rules

- If a proposal already exists (topic `sdd/{change-name}/proposal`), READ it first and UPDATE it
- Keep the proposal CONCISE - it's a thinking tool, not a novel
- Every proposal MUST have a rollback plan
- Every proposal MUST have success criteria
- Return unresolved product decisions to the orchestrator; do not interview the user, choose for them or infer consent. Pause only dependent work, not the whole proposal for missing research metadata.
- Use concrete file paths in "Affected Areas" when possible
- **ALWAYS fill in the Capabilities section** — this is the contract with sdd-spec. Research the real code first to use correct existing capability names.
- New Capabilities → each gets a full spec during the spec phase
- Modified Capabilities → each will become a delta spec
- If nothing changes at the spec level (pure refactor, config change), explicitly write "None" under both sub-sections — don't leave them as template placeholders
- **Sufficient detail**: Keep the proposal concise but complete enough to explain intent, scope, risks, rollback and success criteria. Use bullets or tables where they improve clarity. Do not truncate required detail to meet a word or line cap.
- Return envelope per **Section D** from `_shared/mala-pata-sdd-phase-common.md`.
