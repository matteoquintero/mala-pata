---
name: mala-pata-shot
description: MINIMUM lane of ODD — the "direct inline" of ODD with no worktree and no ceremony, for the smallest, already-understood change (a color, a copy, a flag, a one-line fix). Runs in a single pass — authorize → enter the safe branch → understand (1-3 files) → edit with the project's TDD mode → work-unit commit (+ RDD per commit if on). Does NOT create a worktree, does NOT write a feature-doc, does NOT do preview or smoke test, does NOT dispatch sdd-*. If midway a decision appears, the blast radius grows or design is needed → STOP and bounce to /mala-pata-organic. Trigger — trivial change + understood + minimal blast radius, or when /mala-pata-triage routes here.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.4.0"
---

# /mala-pata-shot — ODD in a single pass, no worktree

User request: **input delivered by the CLI** (or the draft of fields that `/mala-pata-triage` passed when deciding shot)

This is mala-pata's smallest lane: **bare ODD**. Same method as `/mala-pata-organic-start` (authorize → explore → implement → close, with work-unit commit and RDD per commit), but **no worktree, no feature-doc, no kickoff/start split, no preview or smoke test**. One shot and done (*one-shot*) for a change so small and so well understood that all that ceremony is pure overhead.

> **The ODD protocol is the source of truth.** Its steps, the work-unit commits and the RDD evaluation per commit live in your **global CLAUDE.md** (`## Implementation Routing → ### ODD protocol`). This skill runs the minimum subset of that protocol — the **direct inline** route. If the CLAUDE.md and this skill differ, **the CLAUDE.md wins**.

> **Uses ODD workers (direct inline), NEVER `sdd-*` agents.** The gentle-ai `PreToolUse:Agent` preflight does not apply here, same as in `/mala-pata-organic`.

## Requirements (orchestrate, do not reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP and ask to install it, do not start):
  - `git` — version control; the work-unit commit is part of the lane. Always present.
  - `gentle-ai` — RDD-per-commit engine (ODD lane). Install: `brew install gentleman-programming/tap/gentle-ai`.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded):
  - `codegraph` — locate the symbol/file to touch without over-reading. Fallback: grep/Read. Install: global npm CLI; per-project init with `gentle-ai codegraph init --cwd <repo>`.
  - `serena` — symbol-level navigation/editing. Fallback: codegraph/grep. Install: `uv tool install -p 3.13 serena-agent && serena setup claude-code`.
  - `engram` — optional continuity. Fallback: none — shot leaves no durable artifact by design. Install: comes with gentle-ai (`brew install gentleman-programming/tap/gentle-ai`).

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP, e.g. serena). If a mandatory tool is missing, do not continue.

## Hard rules

> **#1 — Entry gate: shot is for the TRIVIAL and UNDERSTOOD, not for the small-but-uncertain.** Shot applies only if: the What/Done are obvious, there are no decisions that **need design**, the blast radius is minimal (1-3 files), no migration, no new contract/endpoint, no new UI. A decision that is **decidable with one question** (known options, the human chooses) does NOT take you out of shot: ask that question and continue. Only a decision that **needs design** (architectures with tradeoffs to investigate) escalates to organic/loop. The criterion is NOT line count — it is the **absence of uncertainty and of necessary ceremony**. If any of that is missing → it is NOT shot: bounce to `/mala-pata-organic` (or `/mala-pata-loop` if there are design decisions, `/mala-pata-roadmap` if it is multi-unit).

> **#2 — NEVER a worktree. This is what makes shot fast — it is the only lane that works in-place.** Do NOT create or use a worktree under any circumstance; creating a worktree is exactly what shot avoids (if you think one is needed, it was not shot → bounce to organic/loop). You work in-place, but **NEVER touch `main` directly**. If you are standing on a protected branch (`main`/`development`), **branch-first**: create a short branch `<type>/<slug>` (`fix`/`chore`/`refactor`/`docs`) and commit there. If you are already on a feature branch, commit on that one. The worktree is skipped; the safe branch is NOT.

> **#3 — Absolute paths ALWAYS** in every git/read/write command (`git -C <ABS-repo> …`). Before editing or committing: `git -C <ABS-repo> rev-parse --abbrev-ref HEAD` must return a branch that is NOT `main`/`development`. If it returns a protected one, apply #2 before writing.

> **#4 — A single pass.** There is no kickoff, no start phase, no ceremonial gates. If you find yourself wanting to open a feature-doc, a preview or a smoke test, it is a sign the change was NOT shot (see #1) — bounce to organic.

## Flow (ODD direct-inline, in one pass)

1. **Authorize (ODD step 1).** Does the request authorize a change? Investigation/explanation/review/comparison = read-only → answer directly, touching nothing. Only if it authorizes a change, you continue.
2. **Safe branch (no worktree) — Rule #2/#3.** `git -C <ABS-repo> rev-parse --abbrev-ref HEAD`. If it is `main`/`development` → `git -C <ABS-repo> switch -c <type>/<slug>` (branch-first) and confirm the type in one line. If you are already on a feature → stay there. No worktree is created.
3. **Understand (1-3 files).** Locate what must be touched (codegraph/serena, or grep/Read as fallback). **If you need 4+ files, or a design decision appears, or the blast radius grows → STOP** (Rule #1): it is not shot, bounce to `/mala-pata-organic`.
4. **Edit + checks.** Apply the change with the **project's TDD mode**: if strict TDD is on, Red → Green → Refactor; otherwise, targeted functional checks. Run the **check that proves this change** (not the whole suite, unless it is cheap). Never consider it done without seeing the check green.
5. **Work-unit commit.** `git -C <ABS-repo>` with explicit pathspec and a Conventional Commit. If **RDD is on**, after the commit run `gentle-ai review assess --cwd <ABS-repo> --json` and follow the native plan (for a trivial change it almost always yields passive). The full RDD detail lives in the CLAUDE.md ODD protocol — do not reimplement it.
6. **Close (one line, fixed format).** Emit exactly one line:
   - success → `✓ <change> — Check: <cmd → result> · Commit: <sha> <type(scope): subject> · Next: push/PR is yours`
   - stopped → `✗ stopped: <why> → /mala-pata-organic`

   **Push, PR and merge are left to the human** (shot does not open a PR on its own unless you ask). No feature-doc, no table — keeping it to one line is what makes the lane fast. Emit the labels `Check` / `Commit` / `Next` **verbatim in English**; the values follow the conversation language.
   **Structure:** Definition of Done + Conventional Commits. The shot lane itself = house method.

## Escape guard (Rule #1, but midway)

If you started as shot and midway you discover the change was NOT trivial (a decision appeared, the blast radius grew, design or migration is needed) → **STOP, do not force shot**. Do not commit something half-done or broken; leave the work on the branch and recommend escalating to `/mala-pata-organic` (or `/mala-pata-loop` if there are design decisions). Forcing shot on something that grew is exactly what this lane avoids.

## What shot does NOT do

- Does NOT create a worktree.
- Does NOT write a feature-doc or kickoff.
- Does NOT do preview or smoke test (if the change needs them, it was not shot).
- Does NOT dispatch `sdd-*` agents.
- Does NOT push, open a PR or merge on its own — that is left to the human.
