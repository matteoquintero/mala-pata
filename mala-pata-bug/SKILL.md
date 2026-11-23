---
name: mala-pata-bug
description: ENTRY for a defect whose ROOT CAUSE is UNKNOWN — you cannot size or route the fix because you do not know WHY it happens. It runs a read-only BUG-SPIKE (the `bug` profile of `/mala-pata-research --spike`): reproduce → isolate → root cause → fix options sized by the cause; it writes a finding and hands to `/mala-pata-triage` (which routes the fix shot/organic/loop, and the chosen lane applies `_shared/mala-pata-bug-entry-check.md`). It does NOT fix the code and does NOT decide the lane. If the cause is ALREADY known, this is the WRONG skill → use `/mala-pata-research` (sharpen the fix) → `/mala-pata-triage`. Trigger — "no sé por qué pasa este bug", "investigá por qué falla X", "diagnosticá este error", "bug de causa desconocida", "/mala-pata-bug <defecto>".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "0.1.0"
---

# /mala-pata-bug — diagnose a defect of unknown root cause (bug-spike entry)

Input: **the one delivered by the CLI** — a defect description (the symptom + any reproduction / evidence you have).

Your job: find the ROOT CAUSE of a defect you cannot yet explain, READ-ONLY, and propose the sized fix — then hand to triage. You are a THIN entry: the mechanics ARE the spike mode of `/mala-pata-research` with the `bug` profile; you do not reimplement them, you apply them.

> **You investigate, you do NOT fix.** Like research/spike: read-only. You reproduce, isolate and NAME the root cause; you do NOT write the fix, create a worktree, or decide the final lane (triage rules it).
> **Only for an UNKNOWN cause.** If the cause is ALREADY known (you know WHY and the fix is understood), this is the wrong skill — bounce to `/mala-pata-research` → `/mala-pata-triage`. The bug-spike exists only for "I don't know why it happens".

## Phase 0 — Authorize (always read-only)
Diagnosing never mutates: no fix, no worktree, no prod/data change. If the request is actually "fix X now" with the cause already known, bounce (wrong skill); do not run a spike.

## Phase 1 — Known or unknown cause? (the gate)
Decide whether the ROOT CAUSE is known. If it is genuinely ambiguous, ask ONE question and wait.
- **Known** → bounce: `/mala-pata-research` (sharpen the fix) then `/mala-pata-triage`. The fix only needs sizing/routing + the in-lane `_shared/mala-pata-bug-entry-check.md`. Do NOT run a spike.
- **Unknown** → continue: this is a bug-spike.

## Phase 2 — Run the bug-spike (apply the profile + the spike contract; do not reinvent)
Run it as the spike mode of `/mala-pata-research` with `profile: bug`:
1. **Apply `_shared/mala-pata-spike-bug.md` verbatim** — the probe: reproduce → isolate (bisect) → root cause (not the symptom) → blast radius → fix options sized by the cause.
2. **Honor the spike contract** (canonical in `/mala-pata-research`'s Spike mode — do not restate it, apply it): read-only; a MANDATORY exit criterion (*"root cause named and the fix approach/lane follows"* OR *"cannot reproduce/diagnose read-only"*); a one-line cost/scope forecast before probing; refuse with no exit criterion; the anti-ceremony guard (one spike per question).
3. **Write the research doc** as a spike: frontmatter `kind: spike`, `profile: bug`, the fixed `## Finding` section (root cause · reproduction · rejected hypotheses · residual unknowns · fix options + recommended lane · regression test). Write-only, no commit, on a durable branch — same as `/mala-pata-research`.

## Phase 3 — Hand off (no routing, no fix)
Hand the finding to `/mala-pata-triage <slug>`: root cause known → triage routes the fix shot/organic/loop by the finding's sized options, and the chosen lane applies `_shared/mala-pata-bug-entry-check.md` (reproduce, the regression test in the DoD, a `fix/` branch). Cannot-reproduce → RECONSIDER: name the missing evidence; do NOT route a guessed fix.

## Close (mandatory)
Close with the spike's close (BLUF + the `## Finding` summary) exactly as `/mala-pata-research` spike mode does. Apply `_shared/mala-pata-output-contract.md` (tables + fixed blocks, no narrative).

## What it does NOT do (invariants)
- Does NOT fix the code, create a worktree, or run any lane — it diagnoses, read-only.
- Does NOT decide the final lane — it proposes; `/mala-pata-triage` rules.
- Does NOT reimplement the spike — it applies `/mala-pata-research` spike mode + the `bug` profile.
- Does NOT run for a KNOWN cause — that bounces to research/triage.
- Does NOT guess a fix when it cannot reproduce — it names the missing evidence (RECONSIDER).

## Relation to the family
- The DISCOVERABLE entry for "a defect I cannot explain yet". It is a thin wrapper over `/mala-pata-research --spike` with `profile: bug` (`_shared/mala-pata-spike-bug.md`).
- **Different from** `/mala-pata-research` (known-cause fix / idea sharpening) — research is for when you already know WHAT/WHY; this is for the unknown root cause.
- Re-enters the pipeline at `/mala-pata-triage`, like every spike.

Structure: Cynefin / XP spike + diagnostic (reproduce → isolate → root cause) + Double Diamond. Bug-spike profile + known-vs-unknown gate = house method.
