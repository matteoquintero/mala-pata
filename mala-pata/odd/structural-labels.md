# Feature: structural-labels

**Objective:** freeze verbatim-English Field labels in close/summary tables across the mala-pata suite.
**Problem:** close tables render left-column labels in the user's language and reinvent them per case; the generic clause alone failed (research had it).
**Source:** `mala-pata/research/structural-labels-audit.md` (per-skill frozen label sets + proposed shared clause).
**Scope:** new `_shared/structural-labels.md` (+ `mala-pata-` symlink); 10 NEEDS-FIX skills: research, loop-start, organic-start, shot, walkthrough-start, runbook, playbook, standards, dossier, roadmap. Optional (only if cheap): icebox, icebox-defrost, icebox-defrost-start, playbook-start.
**Constraints:** domain-neutral, English, mala-pata-skill flow (edit live → mirror → minor bump → branch commit), zero attribution, no push. Dossier exception: client questionnaire stays Spanish; only internal traceability doc labels go verbatim English.
**TDD:** not applicable (markdown skill content). Checks = structural readback, context-leak grep, symlink resolution, per-skill frozen set present + pointer present.

## Tasks
- [x] T1 — Shared clause ref + symlink + 10 skills (enumerated frozen set + pointer) + dossier split + optional soft ones; minor bumps; mirror; commit. Route: delegated (11+ non-trivial files).

## Progress / evidence
- T1 done (delegated writer). Added `_shared/structural-labels.md` (+ symlink `~/.claude/skills/_shared/mala-pata-structural-labels.md`).
- 10 NEEDS-FIX skills (frozen set enumerated next to table + pointer; minor bump): research 1.20.0->1.21.0, loop-start 1.25.0->1.26.0, organic-start 1.24.0->1.25.0, shot 1.12.0->1.13.0, walkthrough-start 1.4.0->1.5.0, runbook 1.4.1->1.5.0, playbook 1.4.1->1.5.0, standards 0.1.1->0.2.0, dossier 0.1.2->0.2.0, roadmap 2.20.0->2.21.0.
- Soft skills hardened (cheap enumerate+pointer): icebox 0.2.2->0.3.0, icebox-defrost 0.2.1->0.3.0, icebox-defrost-start 0.1.1->0.2.0, playbook-start 1.4.0->1.5.0.
- dossier split: client questionnaire stays Spanish; internal traceability Q1..Q6 labels + close block verbatim English.
- roadmap: coverage table unified to `Axis (desired state) | Status | Phases / reason` in gate and file.
- Overlap note: research SKILL.md carries spike wiring (profile field, spike-catalog pointer) from the spike branch; spike-catalog.md is NOT on this branch.
- Checks: pointer grep >=1 in all 14; context-leak grep clean; symlink resolves.
- Commit: see git log (feat(skills): freeze verbatim-English structural labels in close tables).
