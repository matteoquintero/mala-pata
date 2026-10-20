---
name: mala-pata-playbook
description: CREATES a playbook — a markdown for a SCENARIO that has branches (not a single path), built around a decision tree so an agent (or human) navigates "if observed A → branch X; if B → branch Y", where each leaf either runs inline steps or hands off to a runbook. It is the scenario-level counterpart of mala-pata-runbook (one procedure): the playbook narrows an ambiguous situation to a known condition, then routes. Two modes — create NEW from a scenario description, or ADOPT an existing doc and normalize it. Writes mala-pata/playbooks/<slug>.md + a companion findings file; READ-ONLY on your projects, NEVER executes (the runner is mala-pata-playbook-start). Before writing it confirms understanding and asks the open decisions one at a time. Trigger — "creá un playbook para X", "armá el playbook de diagnóstico/incidente/reconciliación de X", "normalizá este playbook al estándar".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.0.0"
---

# /mala-pata-playbook — create a scenario playbook (decision tree; does not run it)

Input: **the one delivered by the CLI** — a **scenario description** (new playbook), or the **path to an existing doc** to adopt and normalize.

Your job: turn a SCENARIO into a playbook an agent can navigate — a decision tree that classifies what is observed and routes to the right branch, where each leaf runs inline steps or hands off to a runbook. A runbook is ONE known procedure; a playbook is the scenario-level guide that decides WHICH procedure, under branches and roles. You WRITE the playbook; you do NOT execute it — running it is `/mala-pata-playbook-start`.

> **Playbook ≠ runbook. If it is a single deterministic path, it is a runbook** — route to `/mala-pata-runbook` instead. A playbook EARNS its name only when there are real branches (several observed conditions leading to different actions) or genuine judgment/roles. Do not dress a one-path procedure as a playbook.
> **Branches route on OBSERVED, measurable conditions** — never on a guess. Every decision node has conditions the runner can evaluate from evidence, plus a fallback (`Others`) branch for the unmatched. If a branch would need the runner to guess, it is not a branch — it is an open product decision to resolve now (Phase 2).
> **Playbooks orchestrate runbooks.** A leaf whose procedure is deterministic links to a runbook (`/mala-pata-runbook-start <slug>`). As a branch stabilizes (same action sequence every run), it should **crystallize** into a runbook and the playbook just routes to it — the playbook is where judgment lives, the runbook is the crystallized leaf.

## Requirements (orchestrate, do not reinvent)

- **Mandatory** (no fallback — if missing, STOP): `git` — to resolve the repo root.
- **Recommended** (warn in one line and continue degraded): `codegraph`/`serena` — ground the terrain (systems, data sources, levers) and find the runbooks the branches can call. `WebSearch/WebFetch` — external best-practice for the scenario type. `engram` — a one-line pointer. Fallbacks: grep/Read; the file is the source.

Check with `command -v` / `claude mcp list`. If a mandatory tool is missing, do not continue.

## Phase 0 — Authorize (read-only guard)

Creating a playbook is **always read-only**: you write the markdown; you never run the scenario. No execution, no mutation, no code.

## Phase 1 — Mode + is-this-really-a-playbook

1. **Mode**: a **scenario description** → new; a **path to a doc** → adopt (map onto the standard, keep what is real).
2. **Playbook vs runbook gate**: are there genuine branches / judgment / roles? **No branches, single path** → STOP and route to `/mala-pata-runbook`. Yes → continue.
3. **Ground the terrain** (read-only): the systems, data sources, models, and the **levers/knobs** the branches turn; and which existing **runbooks** the leaves can call. Reuse-first: a leaf that is already a runbook links to it, it is not rewritten here.
4. **Scope to ONE scenario** — do not combine unrelated scenarios in one playbook (that is the #1 way branching rots into duplicate/missed paths).

## Phase 2 — Confirm understanding, ask the open decisions (BEFORE writing)

Do NOT invent the branches or thresholds — surface and ask (the `/mala-pata-research` Phase 2 split: what the code answers vs what only the human knows).

1. **Restate the scenario + the branches** you understood — a short readback: the entry signals and each branch "if <condition> → <action>".
2. **Ask the open decisions one at a time**, waiting each time: the exact **conditions/thresholds** that distinguish branches (and the sustained period, to avoid flapping), which leaves are deterministic enough to be **runbooks**, **owners/roles** per branch, escalation path + max time, rollback thresholds (who decides/executes), and the **exit criteria** (what declares the scenario resolved). Never assume a branch.
3. Only with those settled, write it. Anything still unknown is an explicit `OPEN:` gap, not a guess.

## Phase 3 — The standard (what every playbook contains)

Write to `mala-pata/playbooks/<slug>.md` (inside the repo, versioned; `mkdir -p`). **Frontmatter**:

```markdown
---
slug: <kebab>
domain: <the operational area/system it covers — else 'main'; NEVER blank, ANY doubt → ASK the human>
kind: incident | diagnostic | reconciliation | decision | recovery
scenario: <one line: the situation this handles>
signals: [<observable entry triggers>]
severity: <levels + indicators, or N/A>
runbooks: [<slugs of runbooks the branches orchestrate>]
roles: <who decides / executes / escalates (RACI-lite)>
owner: <who owns this playbook>
last_reviewed: <ISO 8601>
---
```

**Body** (fixed section order — labels verbatim English):

| Section | What it holds |
|---|---|
| Purpose / Scenario | ONE scenario this handles (scope to one). |
| Entry — signals & when | Observable triggers + thresholds (sustained, not instantaneous) + severity classification. |
| Principles / golden rules | The non-negotiables that govern EVERY branch (e.g. verify in isolation; read the source before assuming; preserve evidence before acting). |
| Terrain / references | Declared context: systems, data sources, models, the levers/knobs, tools, the runbooks leaves can call. |
| Triage / classify | Gather evidence and **commit to a route before acting** (audit trail); the diagnosis order. |
| Decision tree | The core — the branch table below. |
| Roles / escalation | RACI-lite + escalation channel + max time per step + severity → escalation triggers. |
| Exit / verification | The criteria that declare the scenario resolved (the "clean bill of health"). |
| Gotchas / anti-patterns | Learned "do not repeat" — the living knowledge of this scenario. |
| Evidence / findings | What to record; per-case concrete instances go to the **companion findings file**, not here (see Phase 4). |
| Crystallization | Which branches are stabilizing toward a runbook, and the note to promote them. |

Render the decision tree as a real Markdown table (NEVER fenced; one line per cell; long detail as a sub-bullet):

| Condition (observed, measurable) | Branch | Action (inline steps or runbook) | Expected outcome | Owner | Rollback |
|---|---|---|---|---|---|
| <evidence X crosses threshold> | <name> | `/mala-pata-runbook-start <slug>` or inline | <verifiable result> | <role> | <undo + condition> |
| none of the above | Others (fallback) | <diagnose further / escalate> | — | <role> | — |

- Conditions are evaluated top-down, **first match wins**; `Others` catches the unmatched. If two could match or none fits a real situation → the runner STOPS (never guesses) — note that intent here.

## Phase 4 — Persist (write only) + method/findings split + pointer

1. **Write only — do NOT commit/push.** Write the file; tell the human the path + durable branch so they commit it in their flow.
2. **Method vs findings (mandatory split)**: the playbook is **reusable method only**. Per-case concrete instances (numbers, "what we tried and ruled out") go to a companion `mala-pata/playbooks/<slug>-findings.md`. The playbook is **self-feeding**: each run appends a finding there (always) and, if a reusable rule emerged, a Gotcha in the playbook.
3. **Adopt mode**: write the normalized playbook; do NOT delete the original — name it, list the gaps you filled (branches made measurable, fallback added, leaves linked to runbooks, `OPEN:` items).
4. **Pointer in engram**: `mem_save` topic_key `playbooks/<slug>`, one-line `Playbook in file: <absolute path>`. If engram is down, the file is the source — warn in one line.

## Phase 5 — Close (mandatory: summary + playbook)

- Title: `**Playbook ready — <slug>**`
- BLUF: `Playbook: <scenario> · <b> branches (+ fallback) · orchestrates <r> runbooks · severity <…/N/A>`
- A short readback table (`Condition | Branch | Action`) — the first branches, so the human sees the tree shape.
- **OPEN** items, if any — one per line.
- **File:** `<absolute path>` (+ the companion findings file)
- **Next step** — run it:

  ```
  /mala-pata-playbook-start <absolute path>
  ```

`Structure: decision-tree playbook (first-match branches + Others fallback) + diagnostic triage (commit-to-route, symptom→cause→action) + playbook-orchestrates-runbooks + crystallization (stable branch → runbook). Method-vs-findings split + golden-rules/gotchas living doc = house method.`

## What it does NOT do (invariants)

- Does NOT execute the playbook — that is `/mala-pata-playbook-start`.
- Does NOT dress a single-path procedure as a playbook — that is a runbook (`/mala-pata-runbook`).
- Does NOT invent branches or thresholds — it asks them (Phase 2) or leaves `OPEN:`.
- Does NOT run against your real projects (read-only to write the tree), paste secrets, or commit.

## Relation to the family

- **Pairs with** `/mala-pata-playbook-start` (creator / runner split).
- **Orchestrates** `/mala-pata-runbook` leaves (a branch can run a runbook); stable branches crystallize INTO runbooks.
- **Indexed by** `/mala-pata-domain-radar` (reads the `domain:` frontmatter).
- **Different from** `/mala-pata-runbook` (one deterministic procedure): a playbook owns the DECISION of which procedure, under branches and roles.
