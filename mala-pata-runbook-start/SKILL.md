---
name: mala-pata-runbook-start
description: RUNS a runbook created by /mala-pata-runbook — reads the runbook md and executes it step by step, deterministically: recomputes context-dependent values at run time, runs each step's exact Action, compares the real output to the Expected output, and on a mismatch follows the step's "If not as expected" (branch or STOP). Honors preconditions, safety rails, timing gates, rollback and stop/escalation; aborts after N failed attempts instead of looping. Authorization is governed by the runbook's standing_authorization + trigger; destructive/remote steps are gated when it is not standing. It executes ONLY what the runbook documents, against ONLY the targets it names. Trigger — "/mala-pata-runbook-start <slug>", "corré el runbook <slug>", or the runbook's own trigger phrase.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.2.0"
---

# /mala-pata-runbook-start — run a runbook deterministically

Input: **the one delivered by the CLI** — normally just the **slug** (e.g. `release-a-main`), which resolves to `mala-pata/runbooks/<slug>.md` from the repo root; an absolute path or the runbook's own trigger phrase also work. **Prefer the slug — the full path is a pain, you do not need it.**

Your job: **execute** the runbook exactly as written. You are the executor counterpart of `/mala-pata-runbook` (which describes, read-only): the runbook says WHAT to do and WHAT the expected output is; you DO it and verify each result. This is to a runbook what `/mala-pata-organic-start` is to an organic kickoff.

> **Deterministic, not creative.** You run EXACTLY the documented steps, against EXACTLY the targets the runbook names, with the tools/sessions it declares in `requires`. You never improvise a step, never touch a target the runbook did not name, and never fake an expected output. If the runbook is wrong, incomplete, or a step cannot be verified → **STOP** and send it back to `/mala-pata-runbook`; you do not patch it mid-run.

## Hard rules

> **#1 — Only what the runbook documents.** Execute only its steps, only its targets, only with the sessions/credentials its `requires` names. Do NOT discover or reuse ambient credentials, sessions, or sockets beyond that (remote-operation boundary). If a required session/tool is missing → STOP.
> **#2 — Authorization comes from the runbook.** If `standing_authorization: yes`, the human invoking this (or saying the trigger) authorizes ALL steps without per-step confirmation — proceed. If `standing_authorization: no`, **confirm before each destructive or remote step** (deploy, merge, send, delete, write to prod). Either way, honor every Safety rail and every timing gate — standing authorization is not permission to skip a rail or run before an agreed time.
> **#3 — Verify every step, abort instead of looping.** After each Action, capture the REAL output and compare it to the step's Expected output. Match → record evidence, continue. Mismatch → follow that step's "If not as expected" (branch or STOP + escalate). Never retry blindly: abort a step after the runbook's attempt limit (default: 3) and escalate. Never report a result you did not observe.
> **#4 — Absolute paths always**, and recompute context-dependent values (clock/timezone, counts, current branch, latest tag) at RUN time from the rule the runbook names — never trust a frozen value baked into the doc.

## Requirements (orchestrate, do not reinvent)

- **Mandatory** (no fallback — if missing, STOP): `git`; plus every CLI/tool/session the runbook's `requires` lists (e.g. `az`, `gh`). Check each with `command -v` / the tool's auth-status command; a missing or unauthenticated required session STOPS the run.
- **Recommended** (with fallback — warn in one line and continue degraded): `engram` — to read the runbook pointer and record a run note. Fallback: the runbook file is the source.

## Phase 0 — Load the runbook

1. Resolve the runbook, slug-first: a **slug** → `<repo-root>/mala-pata/runbooks/<slug>.md` (`git -C <cwd> rev-parse --show-toplevel`); an **absolute path** → use it directly; a **trigger phrase** → the `runbooks/<slug>` engram pointer. Prefer the slug. If none resolves → STOP and ask for the slug. Do not invent steps.
2. `Read` it in full: frontmatter (`slug`, `domain`, `kind`, `trigger`, `standing_authorization`, `risk`, `reversible`, `idempotent`, `requires`, `inputs`, `owner`, `last_reviewed`) and body (Purpose, When to run, Preconditions, Inputs/references, Safety rails, Steps, Verification, Rollback, Stop/escalation, Evidence).
3. If the file is not a runbook in this standard (missing Steps with Expected output) → STOP: it is not runnable; route to `/mala-pata-runbook` to normalize it first.

## Phase 1 — Preflight (STOP on any failure)

**Inputs gate (FIRST, hard).** Read the runbook's `inputs`. If any **required** parameter was not provided in the invocation (or resolvable from context) → **STOP and ask for the missing ones by name** (e.g. "this runbook needs `excel` and `case_ref`"); do NOT start. Optional inputs use their declared defaults. You cannot evaluate preconditions or run steps without the required inputs.

1. **Tools/sessions**: every `requires` entry is present and authenticated. Missing → STOP (name what to install/log in).
2. **Preconditions**: evaluate each gate; every one must be true. Any false → STOP and report which.
3. **Recompute context values**: resolve each context-dependent input from its rule NOW (e.g. Bogota clock → first time slot with margin). These are the values the run will use.
4. **Resolve authorization**: read `standing_authorization`. Note which steps are destructive/remote (they will be gated if `no`).
5. **`OPEN:` items**: if the runbook still has unresolved `OPEN:` gaps that a step depends on → STOP; send back to `/mala-pata-runbook`.

## Phase 2 — Plan readback (announce, do not interrogate)

Emit a one-line-per-step plan with the recomputed values and the hard gates, so the human sees exactly what is about to happen:

`Plan — <slug>: <n> steps · <recomputed values, e.g. deploy slot = 12:30> · timing gate: <step/when> · rollback: <available/none>`

- If `standing_authorization: yes` and the trigger was given → **proceed to Phase 3 without a per-step gate** (the readback is an announcement, not a question).
- If `standing_authorization: no` → proceed, but Phase 3 will confirm before each destructive/remote step.

## Phase 3 — Execute, step by step (sequential)

For each step, in order:

1. **Honor the gate**: if it is a timing gate (e.g. "merge only at the agreed time"), WAIT until then — never run early, never force. If authorization is `no` and the step is destructive/remote, confirm first.
2. **Run the Action** exactly as written, absolute paths, only the declared target/session.
3. **Capture the real output** and compare to the step's Expected output.
   - **Match** → record the evidence (ids, status, timestamp) and continue.
   - **Mismatch** → follow the step's "If not as expected": a branch runs that branch; a STOP stops the run and escalates per the runbook's Stop/escalation. Abort the step after the attempt limit (default 3) — never loop.
4. **Safety rails** are checked at every step; a rail violation STOPS the run immediately.

## Phase 4 — Verify + rollback

1. Run the runbook's **Verification** end-state check. If it passes → success. If it fails → do NOT claim success.
2. On failure (or a rollback condition met), execute **Rollback/recovery** if the runbook defines it and it is reversible; if not reversible → STOP, preserve state, escalate per Stop/escalation. Never leave a half-done destructive run silent.

## Phase 5 — Evidence + close (mandatory)

1. **Evidence**: record what the runbook's Evidence section asks (ids, timestamps, who ran it, final state). If it asks for persistence, write a run note `mala-pata/runbooks/runs/<slug>-<ISO>.md` (write-only — do NOT commit) and `mem_save` a one-line pointer `runbooks/<slug>/run`.
2. **Close** — BLUF then a real table (NEVER fenced; one line per cell; one row per step):

   `Run — <slug>: <done/stopped> · <k>/<n> steps · verification <pass/fail> · <recomputed key values>`

   | # | Step | Status | Evidence |
   |---|---|---|---|
   | 1 | <action> | ✓ done · ○ skipped · ✗ stopped | <id/status/timestamp> |

   If it stopped: the row where it stopped starts `✗` with the reason + the escalation taken. Labels (`#` / `Step` / `Status` / `Evidence`) verbatim English; values follow the conversation language.

`Structure: executable decision tree (action / expected / if-not) + sequential run with abort-after-N (no blind loops) + verify-then-rollback. Authorization-from-the-runbook + only-declared-targets = house method.`

## What it does NOT do (invariants)

- Does NOT improvise steps, touch undeclared targets, or discover ambient credentials beyond the runbook's `requires`.
- Does NOT fake or assume an Expected output — only observed results, or it stops.
- Does NOT loop on a failing step — it aborts after the attempt limit and escalates.
- Does NOT skip a Safety rail or a timing gate, even under standing authorization.
- Does NOT rewrite the runbook mid-run — if the runbook is wrong, it STOPS and routes to `/mala-pata-runbook`.
- Does NOT commit — a run note is write-only; the human commits.

## Relation to the family

- **Runner of** `/mala-pata-runbook` (creator / runner split, like `mala-pata-organic` / `mala-pata-organic-start`).
- The runbook's `domain:` is what `/mala-pata-domain-radar` indexes; this skill reads it but does not change it.
