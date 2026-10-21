---
name: mala-pata-runbook
description: CREATES a runbook/playbook — a markdown that tells an agent (or human) how to execute an operational task step by step, with the EXPECTED OUTPUT of each step, so the execution is deterministic and self-verifiable (runbooks-as-agent-instructions). Two modes — create a NEW runbook from a task description, or ADOPT an existing doc and normalize it to the standard. It writes the runbook to mala-pata/runbooks/<slug>.md with a domain; it is READ-ONLY on your projects and NEVER executes the runbook (the runner is a separate skill). Before writing, it confirms understanding and asks the open decisions one at a time. Trigger — "creá un runbook para X", "armá el playbook de X", "normalizá este runbook al estándar", "runbook de <tarea operativa>".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.3.0"
---

# /mala-pata-runbook — create a deterministic runbook (does not run it)

Input: **the one delivered by the CLI** — a **task description** (new runbook), or the **path to an existing doc** to adopt and normalize to the standard.

Your job: turn an operational task into a **runbook an agent can execute end to end deterministically** — every implicit action becomes an explicit command/tool call, every vague condition a measurable threshold, every assumed context a declared reference (the "runbooks-as-agent-instructions" pattern). You WRITE the runbook; you do NOT execute it — running it is a separate skill (`/mala-pata-runbook-start`).

> **You never execute the task.** You are read-only on the project: you inspect to write the steps accurately, but you do NOT send the email, create the PR, run the migration, deploy, or touch anything the runbook describes. The runbook is your only deliverable.
> **Determinism is the whole point.** A good step has an exact action, an exact expected output, and what to do if the output is NOT what was expected. If a step cannot be made verifiable, say so — do not paper over it.

## Requirements (orchestrate, do not reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP): `git` — to resolve the repo root for the runbook's location. Always present.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded):
  - `codegraph` / `serena` — ground the steps in the real code (exact commands, file paths, symbols). Fallback: grep/Read.
  - `engram` — one-line discoverability pointer. Fallback: the file is the source of truth.

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP). If a mandatory tool is missing, do not continue.

## Phase 0 — Authorize (read-only guard)

Creating a runbook is **always read-only** — you write a markdown describing HOW to do a task; you never do the task. Even if the task is a change (deploy, migration, cleanup), your work here is only the document. No worktree, no code, no execution.

## Phase 1 — Mode + grounding

1. **Mode**: a **task description** → create a new runbook. A **path to an existing doc** (e.g. one of the project's `docs/runbooks/*.md`) → **adopt**: read it and map its content onto the standard (Phase 3), keeping what is real.
2. **Ground it in the real system** (read-only): the exact commands, CLIs, file paths, repo/org/project identifiers, env vars, and tools the task uses. A step that says "deploy" is not a step; `az repos pr set-vote --vote approve ...` with the exact target is. Reuse-first: if the project already has a script/command that does part of this, the step calls IT, not a reinvention.
3. **Context-dependent values** (clock/timezone, counts, current branch, latest tag): name the **rule** that computes them, not a frozen value — e.g. "read the system clock in the relevant timezone; pick the first slot from <list> with enough margin". The runner recomputes at run time.

## Phase 2 — Confirm understanding, ask the open decisions (BEFORE writing)

This is the step that makes the runbook correct. Do NOT invent the operational decisions — surface them and ask (the research-backed "test it on someone who didn't write it", applied up front).

1. **Restate the flow in order** — a numbered one-line-per-step readback of what you understood ("Step 1 <action>; Step 2 <action> if <condition>; Step 3 <action> at <agreed time>"). This is the comprehension check.
2. **Ask the open decisions one at a time** (the `/mala-pata-research` Phase 2 split): what only the human can settle — ambiguous timing/ordering, who is authorized, which recipients, exact thresholds, what counts as done, rollback boundaries, and whether the **trigger is standing authorization** (does one trigger phrase authorize ALL steps without per-step confirmation, or is each destructive/remote step gated?). Ask, WAIT, never assume. **Also pin the minimum run parameters** — for EACH one define its `name`, its `type` (value / file / link / id / number / boolean / date / enum / ...), and whether it is `required` or optional (with a `default`). These become the structured frontmatter `inputs`, and the runner refuses to start without the required ones.
3. Only when the flow and the open decisions are settled, write the runbook. If something stays genuinely unknown, write it as an explicit `OPEN:` gap in the runbook, not a guess.

## Phase 3 — The standard (what every runbook contains)

Write to `mala-pata/runbooks/<slug>.md` (inside the repo, versioned; `mkdir -p`). **Frontmatter** (feeds `/mala-pata-domain-radar` and the runner):

```markdown
---
slug: <kebab>
domain: <the operational area/system it touches (deploy, release, database, <system>, <feature>, ...) — else 'main'; NEVER blank, ANY doubt → ASK the human>
kind: operational | deploy | database | recovery | diagnostic
trigger: <the phrase/condition that starts it>
standing_authorization: yes | no   # yes = the trigger authorizes ALL steps without per-step confirmation
risk: low | medium | high
reversible: yes | no
idempotent: yes | no               # safe to re-run from the top?
requires: [<exact CLIs/tools/sessions needed, e.g. az, gh>]
inputs:            # minimum RUN parameters (distinct from requires = tools). EACH parameter is defined HERE, at creation, with its name + type + whether it is required. The runner STOPS if a required one is missing.
  - name: <param-name>
    type: <value | file | link | id | number | boolean | date | enum(a|b|c) | ...>   # its kind, DEFINED here per parameter — never presumed
    required: true            # true | false
    description: <what this parameter is>
  - name: <param-name>
    type: <...>
    required: false
    default: <value>          # only when required: false
    description: <what this parameter is>
owner: <who owns this procedure>
created_at: <ISO 8601>
last_reviewed: <ISO 8601>
---
```

**Body** (fixed section order — labels verbatim English):

| Section | What it holds (where the determinism comes from) |
|---|---|
| Purpose | One line: the task this executes. |
| When to run | The trigger + whether it is standing authorization. |
| Preconditions | Measurable gates that MUST be true before Step 1 (else STOP). |
| Inputs / references | **The run parameters (the `inputs` contract): each parameter declares `name` + `type` + `required` (+ `description`, and `default` when optional)**, all defined at creation; the `type` (value / file / link / id / number / boolean / date / enum / ...) is pinned per parameter, never presumed. The runner STOPS if a required one is missing. Plus the declared context: exact files, env, identifiers, recipients. **Secrets by reference** (the seeder/`.env`/secret manager), NEVER literal values. Context-dependent values named as a rule, not frozen (Phase 1.3). |
| Safety rails | What it must NEVER do (prod guard, read-only scope, "do not merge before the agreed time", destructive/remote steps need the authorization). |
| Steps | Numbered, sequential. **Each step = Action (exact command/tool) · Expected output (exact, verifiable) · If not as expected (branch or STOP+escalate)**. This is the core. |
| Verification | The end-state check that proves the whole task succeeded (the DoD). |
| Rollback / recovery | How to undo + the conditions that trigger a rollback. `N/A` only if truly irreversible (then say so loudly in Safety rails). |
| Stop / escalation | Abort conditions (e.g. after N failed attempts on a step) + who/where to escalate. |
| Evidence | What to record on each run (ids, timestamps, who ran it) for audit. |

Render the Steps as a real Markdown table (NEVER fenced, one line per cell; long detail as a sub-bullet under the table, not inside a cell):

| # | Action | Expected output | If not as expected |
|---|---|---|---|
| 1 | <exact command / external action> | <exact verifiable result> | <branch, or STOP + escalate> |

## Phase 4 — Persist (write only) + pointer

1. **Write only — do NOT commit/push.** Write the file; the skill does NOT create a commit (auto-committing diverged local main from the remote). Tell the human the path + the durable branch it belongs on so they commit it in their normal flow.
2. **Adopt mode**: write the normalized runbook to `mala-pata/runbooks/<slug>.md`; do NOT delete the original — name it and let the human retire it. List the gaps you filled (implicit actions made explicit, missing expected-outputs/rollback added, `OPEN:` items left).
3. **Lightweight pointer in engram**: `mem_save` topic_key `runbooks/<slug>`, one-line content `Runbook in file: <absolute path>`. If engram is unavailable, the file is the source — warn in one line.

## Phase 5 — Close (mandatory: summary + runbook)

Emit exactly this, from the runbook you wrote (no invention):

- Title: `**Runbook ready — <slug>**`
- BLUF (plain line): `Runbook: <n> steps · trigger "<trigger>" · standing-auth <yes/no> · risk <r> · reversible <y/n>`
- A short readback table (`# | Action | Expected output`) — the first lines only, so the human sees the shape.
- **OPEN** items, if any — one per line, each needing the human (never hidden).
- **File:** `<absolute path>`
- **Next step** — run it with the runner:

  ```
  /mala-pata-runbook-start <absolute path>
  ```

This block is the only way to close on the happy path. **Only exceptions**: Phase 0 read-only stance; a blocking open decision (Phase 2) → the single question allowed before writing.

`Structure: runbooks-as-agent-instructions (explicit action + measurable threshold + declared reference) + executable decision tree (action / expected / if-not) + SRE runbook metadata (owner, last_reviewed, rollback). Trigger-as-standing-authorization + secrets-by-reference = house method.`

## What it does NOT do (invariants)

- Does NOT execute the runbook — that is `/mala-pata-runbook-start`. It never sends the email, opens the PR, runs the migration, or deploys.
- Does NOT run against your real projects — read-only to write the steps accurately; the only thing it writes is the runbook md.
- Does NOT invent operational decisions — it asks them (Phase 2) or leaves them as explicit `OPEN:` items.
- Does NOT paste literal secrets — references the credential source.
- Does NOT commit — write-only; the human commits in their PR flow.

## Relation to the family

- **Pairs with** `/mala-pata-runbook-start` (creator / runner split, like `mala-pata-organic` / `mala-pata-organic-start`).
- **Indexed by** `/mala-pata-domain-radar` (reads the `domain:` frontmatter, like the other mala-pata artifacts).
- **Different from** `/mala-pata-walkthrough` (QA/customer test guide for a feature) and `/mala-pata-states` (state diagram): a runbook is an OPERATIONAL procedure to EXECUTE a task deterministically, not a test or a diagram.
