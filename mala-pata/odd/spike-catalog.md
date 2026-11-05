# Feature: spike-catalog

**Objective:** ship the spike-profile catalog — index + data and integration profiles — wired into research `--spike` and objective-completeness.
**Why:** a completeness fork should name a profile, and the spike should apply that profile's read-only checklist (infra already works this way).
**Source plan:** `mala-pata/research/spike-catalog.md` (verdict SHARPEN; owner decisions resolved 2026-11-05).
**Scope:** `_shared/spike-catalog.md`, `_shared/spike-data.md`, `_shared/spike-integration.md` (+ `mala-pata-` symlinks), `_shared/objective-completeness.md`, `mala-pata-research/SKILL.md`. `spike-infra.md` is NOT touched. Performance profile is out of scope (not read-only).
**Constraints:** domain-neutral, English, mala-pata-skill flow (edit live → mirror → branch commit), zero attribution, no push.
**Decisions:** (1) ship index + data + integration; (2) add optional `profile:` frontmatter on spikes; (3) promotion rule = 2 real cases + owner gate; (4) naming = live `_shared/<x>.md` + symlink `~/.claude/skills/_shared/mala-pata-<x>.md` (verified on disk).
**TDD:** not applicable (markdown skill content; no test runner). Checks = structural readback + context-leak gate + symlink resolution.

## Tasks
- [x] T1 — Write catalog index + spike-data + spike-integration, symlinks, wire research SKILL.md (`profile:` field, selection) + objective-completeness (Data/Integrations lenses fork to profiles; no-match → generic), version bump, mirror, commit. Route: delegated (5 non-trivial files).

## Progress / evidence
- T1 done (delegated writer). Files: _shared/spike-catalog.md, spike-data.md, spike-integration.md (new, + mala-pata- symlinks); _shared/objective-completeness.md (Data/Integrations fork to profiles, no-match -> generic); mala-pata-research/SKILL.md 1.19.0 -> 1.20.0 (optional `profile:` field, catalog selection).
- Checks: symlinks resolve (4); context-leak grep clean on new/edited content; spike-infra.md untouched. Commit: see git log (feat(research): spike-profile catalog).
