---
name: mala-pata-playbook-start
description: RUNS a playbook created by /mala-pata-playbook — walks its decision tree for a real situation: confirms the entry signals, gathers evidence and commits to a route before acting, evaluates each branch's condition against OBSERVED evidence (first match wins; Others is the fallback), then executes that branch inline or hands off to a runbook via /mala-pata-runbook-start. STOPS instead of guessing when the evidence is ambiguous, matches several branches, or fits none. Honors the playbook's principles, gotchas, roles and escalation; verifies the exit criteria; appends a per-case finding. Trigger — "/mala-pata-playbook-start <slug>", "corré el playbook <slug>", or the scenario's own signal.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.4.0"
---

# /mala-pata-playbook-start — run a playbook (walk the decision tree)

Input: **the one delivered by the CLI** — normally just the **slug** (a kebab-case identifier), which resolves to `mala-pata/playbooks/<slug>.md` from the repo root; an absolute path or the scenario's signal also work. **Prefer the slug — the full path is a pain, you do not need it.**

Your job: **navigate** the playbook for the situation at hand — classify what is observed, route to the matching branch, and execute it (inline, or by handing a deterministic leaf to `/mala-pata-runbook-start`). This is the executor counterpart of `/mala-pata-playbook` (which describes, read-only). It is to a playbook what `/mala-pata-runbook-start` is to a runbook — but a playbook branches, so the core act is **choosing the right branch from evidence, not running a fixed sequence**.

> **Route on OBSERVED evidence, never a guess.** Evaluate branch conditions top-down, first match wins; `Others` is the designed fallback. If the evidence is **ambiguous, matches more than one branch, or fits none and there is no fallback** → **STOP and ask / escalate**. Guessing a branch in a judgment scenario is the worst failure here.
> **Principles and gotchas are hard constraints.** The playbook's golden rules and "do not repeat" gotchas bound every branch — a branch that would violate one STOPS.
> **Deterministic leaves go to the runbook runner.** When a branch's action is a runbook, hand off to `/mala-pata-runbook-start <slug>` (it carries the authorization, safety-rail, timing-gate and abort-after-N machinery). Inline branch steps run under the same discipline: observed result vs expected, no blind loops.

## Hard rules

> **#1 — Branch by evidence.** Gather first, commit to the route, then act (audit trail). First-match top-down; `Others` for the unmatched; STOP on ambiguity / multi-match / no-fit-no-fallback.
> **#2 — Authorization + safety come from the artifacts.** Destructive/remote actions (whether inline or inside a called runbook) are gated exactly as `/mala-pata-runbook-start` gates them: only declared targets/sessions, no ambient credentials, honor safety rails and timing gates. A diagnostic playbook is usually read-heavy — prefer read-only evidence gathering; any mutation is gated.
> **#3 — Verify each branch outcome** against its Expected outcome; mismatch → the branch's rollback (if any) + escalate per the playbook's roles. Never fake an outcome.
> **#4 — Absolute paths always**; recompute any context-dependent condition at run time from its rule.

## Requirements (orchestrate, do not reinvent)

- **Mandatory** (STOP if missing): `git`; plus any CLI/tool/session a chosen branch or its runbook declares.
- **Recommended** (warn, continue degraded): `codegraph`/`serena` to gather evidence; `engram` to read the pointer and append findings. Fallbacks: grep/Read; the file is the source.

## Phase 0 — Load the playbook

1. Resolve the playbook, slug-first: a **slug** → `<repo-root>/mala-pata/playbooks/<slug>.md` (`git -C <cwd> rev-parse --show-toplevel`); an **absolute path** → use it directly; a **signal** → the `playbooks/<slug>` pointer. Prefer the slug. None resolves → STOP, ask for the slug.
2. `Read` it in full: frontmatter (`slug`, `domain`, `kind`, `scenario`, `signals`, `severity`, `inputs`, `runbooks`, `roles`, `owner`, `last_reviewed`) and body (Purpose, Entry, Inputs, Principles, Terrain, Triage, Decision tree, Roles/escalation, Exit, Gotchas, Evidence, Crystallization).
3. If it is not a playbook in this standard (no decision tree) → STOP: route to `/mala-pata-playbook` to normalize, or to `/mala-pata-runbook-start` if it is actually a single-path runbook.

## Phase 1 — Entry check (are we in this scenario)

**Inputs gate (FIRST, hard).** Read the playbook's structured `inputs` (each declares `name` + `type` + `required`). If any `required: true` parameter was not provided in the invocation (or resolvable from context) → **STOP and ask for the missing ones by name**; do NOT start. Where practical, check each provided value against its declared `type` and STOP + report a mismatch. Optional inputs fall back to their declared `default`. You cannot gather evidence or walk the tree without the required inputs.

Then confirm the **entry signals** actually match the situation (thresholds, sustained where required). If they do not → STOP: this is the wrong playbook, do not force it. Load the **terrain/references** you will need to gather evidence.

## Phase 2 — Triage: gather evidence, commit to a route

Follow the playbook's triage order: gather the evidence each branch condition needs (read-only), classify, and **commit to the route before acting** — write down which branch and why (the audit trail). Respect the principles here (e.g. read the source before assuming).

## Phase 3 — Walk the tree

1. Evaluate the decision-tree conditions **top-down against the observed evidence; first match wins**. No specific match → `Others` fallback. **Ambiguous / multiple matches / no fit and no fallback → STOP and ask or escalate** (Hard rule #1).
2. **Execute the chosen branch**: a runbook leaf → hand off to `/mala-pata-runbook-start <slug>` (it owns authorization/safety/abort). Inline steps → run under the same discipline (observed vs expected, gate destructive/remote actions, no blind loops).
3. **Verify the branch outcome** vs its Expected outcome; mismatch → rollback (if defined) + escalate per Roles/escalation. A branch may lead to another decision node — repeat from step 1 for the sub-tree.

## Phase 4 — Exit / verify

Check the playbook's **Exit criteria** (the "clean bill of health"). Met → resolved. Not met → do NOT claim resolution; escalate per Roles, roll back any partial action if reversible, preserve state otherwise.

## Phase 5 — Findings + close (mandatory)

1. **Append the per-case finding** (write-only — do NOT commit) to the companion `mala-pata/playbooks/<slug>-findings.md`: the situation, the branch taken + the evidence that selected it, the outcome, ids/timestamps. If a **reusable** rule emerged, propose a Gotcha to add to the playbook (human confirms — you do not rewrite the playbook mid-run). **Crystallization hint**: if this branch has now run the same way enough times, suggest promoting it to a runbook (`/mala-pata-runbook`).
2. **Close — render the output contract: Declared report THEN Run record.** First, if the playbook's `## Outputs` declares a **Declared report**, render it IN FULL (its own tables/sections) — the run's deliverable, rendered **even when the run stopped or escalated**, never skipped. Then the **Run record** — BLUF then a real table (NEVER fenced; one line per cell):

   `Run — <slug>: <resolved/stopped/escalated> · branch "<name>" · exit <pass/fail>`

   | Step | Branch / action | Evidence | Outcome |
   |---|---|---|---|
   | triage | <classification> | <evidence that selected the route> | committed to <branch> |
   | <branch> | <inline or runbook> | <observed> | ✓ done · ◐ partial · ✗ stopped |

   If it stopped/escalated: the row starts `✗` with the reason (ambiguous evidence / gotcha hit / exit failed) + the escalation taken. Labels verbatim English; values follow the conversation language.

`Structure: decision-tree walk (gather → commit-to-route → first-match branch → verify) + stop-on-ambiguity (no guessing) + delegate deterministic leaves to the runbook runner + self-feeding findings/crystallization. Evidence-driven branch selection = house method.`

## What it does NOT do (invariants)

- Does NOT guess a branch — ambiguity / multi-match / no-fit-no-fallback STOPS and escalates.
- Does NOT violate the playbook's principles or gotchas, or run an undeclared target.
- Does NOT fake a branch outcome or exit check — only observed results.
- Does NOT rewrite the playbook mid-run — it appends findings and proposes gotchas/crystallization; the human edits the method via `/mala-pata-playbook`.
- Does NOT commit — findings are write-only; the human commits.

## Relation to the family

- **Runner of** `/mala-pata-playbook` (creator / runner split).
- **Hands deterministic leaves to** `/mala-pata-runbook-start`; a stabilized branch should crystallize into a runbook.
- The `domain:` is what `/mala-pata-domain-radar` indexes; this skill reads it, does not change it.
