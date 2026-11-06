# Feature: orchestrate-gate-and-launch

**Objective:** (1) make the roadmap orchestrator gate per-phase, done-aware and route-accurate; (2) make the Warp wave launch robust (valid YAML, validated before open, launch verified, prefer a tab in the active window).
**Problem:** Hard rule #0 refuses a whole roadmap when any FORECAST route is loop, even if those phases are done or re-triaged to organic. The Warp launch template writes an unquoted `exec:` containing `: ` → invalid YAML → Warp silently drops it while `open` exits 0.
**Sources:** `mala-pata/research/roadmap-orchestrate-done-aware-gate.md` (verdict PROCEED; doc recommendations accepted by the owner 2026-11-06); real-run evidence of the YAML bug; Warp capability research (tabs in the active window, listing tabs).
**Scope:** `mala-pata-roadmap-orchestrate`, `mala-pata-roadmap-orchestrate-start`, `mala-pata-organic-orchestrate-start` (launch step), optional `_shared/` fragments (route resolution, wave launch).
**Constraints:** domain-neutral, English, mala-pata-skill flow (edit live → mirror → minor bump → branch commit), zero attribution, no push.
**TDD:** not applicable (markdown skill content). Checks = structural readback, `tomllib` parse of the tab-config template + a `sh` round-trip of a prompt containing `: `, `"` and `'`, context-leak grep, mirror sync.

## Tasks
- [x] T1 — Done-aware, route-accurate gate in roadmap-orchestrate + roadmap-orchestrate-start (Hard rule #0, steps, report shapes). Route: delegated. Evidence: orchestrate 1.0.1→1.1.0, orchestrate-start 1.1.0→1.2.0, new _shared/route-resolution.md (+ symlink mala-pata-route-resolution.md); Route (actual)+Route source (kickoff|forecast); commit recorded in git log.
- [x] T2 — Robust Warp launch (quoted exec / block scalar, YAML validation before open, launch verification + fallback, active-window tab if supported) in both -start skills, ideally one shared fragment. Route: delegated. Done: shared _shared/wave-launch.md (Warp tab configs, prompt-in-file, tomllib validation, sentinel verify, fallback chain), both -start skills point to it (roadmap 1.2.0→1.3.0, organic 1.1.0→1.2.0). Evidence: tomllib parses rendered template; prompt with ": ", quotes and apostrophe round-trips via sh; legacy YAML removed.

- [x] T3 — Review-advisory follow-ups (6 findings). Route: delegated (single writer). Done: wave-launch 60s timeout + late-start guard (sentinel + `claude` cwd re-check before every fallback); run-scoped `mpl-<run-id>-<slug>` tab configs and run-only cleanup; Terminal.app fallback with quoted paths passed via AppleScript argv; kickoff precedence (phase branch wins, no route/profile = no kickoff); unified `⚑ needs a human` label; this doc. Versions: roadmap-orchestrate 1.1.0→1.1.1, roadmap-orchestrate-start 1.3.0→1.3.1, organic-orchestrate-start 1.2.0→1.2.1. Evidence: tomllib parse OK with a spaced worktree path; tab command round-trips `: `, `"`, `'` and creates the sentinel; Terminal fallback command round-trips via argv.

## Progress / evidence
- T1 commit 86047c1 (research doc + feature doc) and 3b2c70f (done-aware, route-accurate gate); T2 commit 80948fb (Warp tab configs, validated and verified).
- Native review: lineage review-01162303b7639c3c approved and acknowledged (6 non-blocking advisories).
- T3: follow-up commit on this branch (see `git log`) addresses all 6 advisories.
- Next step: human decides push / PR.
