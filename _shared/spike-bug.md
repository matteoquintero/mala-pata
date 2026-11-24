# Bug-spike (diagnostic) — mala-pata single source of truth

The **bug** (diagnostic) profile of `/mala-pata-research --spike`: the read-only probe to run when a defect's ROOT CAUSE is UNKNOWN — you cannot yet size or route the fix because you do not know WHY it happens. It is a normal spike (read-only, scope-boxed, produces a `## Finding`, re-enters via triage); this file is its assessment checklist. Index: `_shared/mala-pata-spike-catalog.md`. Entry alias: `/mala-pata-bug`.

## When
A defect whose FIX APPROACH is unknown BECAUSE the ROOT CAUSE is unknown: "why does X happen?", "what state/input triggers it?", "which layer owns the defect?". A fix whose cause is ALREADY known is NOT a bug-spike — it is a normal change: route it through `/mala-pata-research` → `/mala-pata-triage` (and the lane applies `_shared/mala-pata-bug-entry-check.md`). The bug-spike is ONLY for the unknown-cause case. It is NOT a lane and it does NOT fix the code — it diagnoses, then the real fix routes by size × uncertainty.

## The probe (read-only — reproduce and isolate; NEVER push a fix or mutate prod/data)
1. **Reproduce.** Establish a deterministic reproduction, or at minimum a precise expected-vs-actual with the exact inputs/state. If it cannot be reproduced, the probe's job is to SAY SO and name the missing evidence (a case, logs, a repro env) — do NOT guess a fix. (Same reproduce-before-code bar as `bug-entry-check` step 1.)
2. **Isolate (bisect the surface).** Narrow WHERE the defect lives — which layer/module/commit. Use what git/logs/tests give: a regression → bisect to the introducing change; a data-shaped failure → the record that triggers it; a boundary → the input class. Anchor to the real code; never reason from the symptom alone.
3. **Root cause (not the symptom).** Name the ACTUAL cause — the line/condition/contract/state that produces the wrong behavior — with evidence (file:line, a failing assertion, the triggering input). A fix on the symptom that leaves the cause is a false fix.
4. **Blast radius + regression risk.** What else shares the buggy code/path (shared helpers, siblings) so the fix and its test cover the real surface, not only the reported case.
5. **Fix options sized by the cause.** Lay the candidate fixes side by side with their size: a one-line / one-condition fix (→ shot), a contained change (→ organic), or a fix that needs design because the cause is architectural (→ loop). Name the regression test that pins it (part of the DoD, per `bug-entry-check`).

## Finding (the deliverable)
`## Finding`: **root cause** (with evidence) · **reproduction** (the deterministic repro, or the missing evidence) · **rejected hypotheses** (what it was NOT, with evidence) · **residual unknowns** · **fix options + recommended lane** (shot / organic / loop, sized by the cause) · **regression test** that will pin it. **Exit criterion:** *"the root cause is named and the fix approach/lane follows from it"* OR *"cannot reproduce/diagnose read-only"* (→ name the missing evidence; do NOT guess a fix). Refuse a bug-spike with no exit criterion.

## Re-entry
`/mala-pata-triage` reads the finding: root cause known → the fix routes shot / organic / loop by the sized options (and the chosen lane applies `_shared/mala-pata-bug-entry-check.md`: reproduce, the regression test in the DoD, a `fix/` branch). Cannot-reproduce → RECONSIDER / gather the missing evidence before routing a fix.
