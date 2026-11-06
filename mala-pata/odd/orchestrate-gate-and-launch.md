# Feature: orchestrate-gate-and-launch

**Objective:** (1) make the roadmap orchestrator gate per-phase, done-aware and route-accurate; (2) make the Warp wave launch robust (valid YAML, validated before open, launch verified, prefer a tab in the active window).
**Problem:** Hard rule #0 refuses a whole roadmap when any FORECAST route is loop, even if those phases are done or re-triaged to organic. The Warp launch template writes an unquoted `exec:` containing `: ` → invalid YAML → Warp silently drops it while `open` exits 0.
**Sources:** `mala-pata/research/roadmap-orchestrate-done-aware-gate.md` (verdict PROCEED; doc recommendations accepted by the owner 2026-11-06); real-run evidence of the YAML bug; Warp capability research (tabs in the active window, listing tabs).
**Scope:** `mala-pata-roadmap-orchestrate`, `mala-pata-roadmap-orchestrate-start`, `mala-pata-organic-orchestrate-start` (launch step), optional `_shared/` fragments (route resolution, wave launch).
**Constraints:** domain-neutral, English, mala-pata-skill flow (edit live → mirror → minor bump → branch commit), zero attribution, no push.
**TDD:** not applicable (markdown skill content). Checks = structural readback, YAML template parses with `yaml.safe_load`, context-leak grep, mirror sync.

## Tasks
- [x] T1 — Done-aware, route-accurate gate in roadmap-orchestrate + roadmap-orchestrate-start (Hard rule #0, steps, report shapes). Route: delegated. Evidence: orchestrate 1.0.1→1.1.0, orchestrate-start 1.1.0→1.2.0, new _shared/route-resolution.md (+ symlink mala-pata-route-resolution.md); Route (actual)+Route source (kickoff|forecast); commit recorded in git log.
- [x] T2 — Robust Warp launch (quoted exec / block scalar, YAML validation before open, launch verification + fallback, active-window tab if supported) in both -start skills, ideally one shared fragment. Route: delegated. Done: shared _shared/wave-launch.md (Warp tab configs, prompt-in-file, tomllib validation, sentinel verify, fallback chain), both -start skills point to it (roadmap 1.2.0→1.3.0, organic 1.1.0→1.2.0). Evidence: tomllib parses rendered template; prompt with ": ", quotes and apostrophe round-trips via sh; legacy YAML removed.

## Progress / evidence
- (pending)
