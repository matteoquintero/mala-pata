# Delivery-structure consistency plan (all mala-pata emitters)

Status: **approved to execute, one skill at a time.** Nothing applied yet in this doc's own commit.
Goal: every emitter skill's OUTPUT/DELIVERY block is consistent and grounded in a real framework,
with a `Structure:` footer citing it (or honestly labelled `house method`).

## Decisions (locked)

- **A — Unify the vocabulary** across all emitters.
- **B1 — Radar v2**: split `Light` into `State` + `Attention`; drop the colour words
  (RED/YELLOW/ORANGE/BLACK/GREEN); version `radar/references/table-format.md` to v2. The `Attention`
  values carry glyphs (see shared vocabulary).
- **B2 — All `DoD`**: one field name `DoD` everywhere (was `Done` / `Definition of Done` / `Done (when)`),
  content always in **Given/When/Then**. Coordinated rename (organic-start + walkthrough parse `## Done`).
- **B3 — N/A off `○`**: N/A uses a meaningful glyph, **`∅ n/a`** (empty set = none/not-applicable),
  not a bare dash.

## Shared vocabulary (the single source of glyph meanings)

- **Workflow state:** `✓ done` · `◐ in progress` · `○ pending` · `✗ blocked` · `∅ n/a`
- **Check / step outcome:** `✓ pass` · `✗ fail` · `◐ partial: <reason>`
- **Severity:** `▲ high` · `● medium` · `▼ low`
- **Attention (radar v2 — glyphs proposed, confirm/tune):**
  `→ needs you now` · `◆ awaiting gate` · `‖ parked` · `· cleanup pending` · `∅ none`
- **Provenance:** `[noted]` · `[inferred]` · `[asked]` · `[assumed]`
- **Footer (one line, last):** `Structure: <Framework> (<url>)` — or `Structure: house method`
- **Rules carried over:** structural labels emitted VERBATIM in English; tables never flat lists for
  findings/status/coverage; BLUF/Minto — verdict/decision line FIRST, evidence after.
- **Every emitter output carries at least ONE table** — even shot (a compact one-row table). This
  overrides the earlier "shot = no table" note.
- **Tables render as REAL Markdown tables, NEVER inside a ``` code fence** — a fenced table shows raw
  pipes and does not render as a bordered table. Only banner/BLUF/legend/footer lines are plain text.
- **Count / summary lines always carry the WORD, not just glyph + number** — `✓ 2 done · ○ 3 pending`,
  never `✓ 2 · ○ 3` (glyph + number alone is unreadable; the glyph needs its word next to it).

> Open glyph confirmations: `∅` for n/a and the Attention set above. All are typographic (not emoji):
> `∅` U+2205, `→` U+2192, `◆` U+25C6, `‖` U+2016, `·` U+00B7. Add them to the allowed whitelist.

## Frameworks + re-verify list

Re-verify these URLs before pinning them in footers (cited from memory): Cockburn information-radiator,
Harel statecharts (1987), DARPA Heilmeier page. `house method` (no external source): lane routing,
preview's 4 sections + risk-tier + audit + autotest gate, PROCEED/SHARPEN/RECONSIDER verdict, roadmap
core-vs-complete/Deferrable/Level-1-2/tentative-route, kickoff brief fields, gaps noted/inferred +
3-source model, wave planning, radar Attention set + urgency order.

## Per-skill plan (ungrouped — apply one by one)

### 1. research
- CHANGE: `Done (when)` → `DoD` (Given/When/Then).
- IMPROVE: "Problem vs proposed solution" and the 7 Heilmeier answers become **tables** with a provenance column.
- ADD: DoR-lite handoff using the lane field names (What / Why / DoD / Decisions / Risk); `Structure:` footer.
- Footer: `Heilmeier Catechism (DARPA) + Double Diamond (Design Council)`.
- House: verdict PROCEED/SHARPEN/RECONSIDER, `size_signal`, "Left OUT".

### 2. triage
- IMPROVE: decision as a 2-line BLUF (`Lane: <…> — Reason: <test applied>`); draft as a 5-row table (`Field | Value | Provenance`) with field names What / Why / DoD / Decisions / Risk.
- ADD: a `DoR:` line; `Structure:` footer.
- CHANGE: `Done` → `DoD` (coordinated rename).
- Footer: `Definition of Ready + INVEST` (routing = house method).
- House: the lane-routing tree, vague-work bounce.

### 3. shot
- IMPROVE: one-line fixed close `✓ <change> — Check: <cmd → result> — Commit: <sha> <type(scope): subject>` and `✗ stopped: <why> → /mala-pata-organic`.
- ADD: English-label guard; short `Structure:` footer. (A compact one-row table, no feature-doc — keep the lane fast.)
- Footer: `Definition of Done + Conventional Commits`.
- House: the shot lane itself.

### 4. organic
- CHANGE: `## Done` → `## DoD` (Given/When/Then).
- IMPROVE: close summary as a 2-column table (`Field | Value`).
- ADD: a `DoR:` line in the close; `Structure:` footer.
- Footer: `DoR-style brief (house) + BLUF close + Given/When/Then (Fowler)`.
- House: the What/Why/DoD/Decisions/Risk brief.

### 5. organic-start
- ADD: BLUF `Result:` line above the Step-8 table; `Evidence` column; `Structure:` footer.
- IMPROVE: shared state lexicon (`∅ n/a` not `○`); per-row DoD check in Given/When/Then.
- Footer: `Definition of Done + information radiator (Cockburn)`.
- House: the milestone row set.

### 6. loop
- IMPROVE: add a DoR result to the kickoff (same field names as organic); `Risks / open decisions` as a table (`Item | Type | Owner | Provenance`); close-table treatment like organic.
- ADD: `Structure:` footer.
- CHANGE: DoD field naming consistent.
- Footer: `DoR-style brief (house) + BLUF close`.
- House: profiles, sdd_preflight recommendations.

### 7. loop-start
- ADD: BLUF `Result:` line above the Step-5 table; `Evidence` column; `Structure:` footer.
- IMPROVE: align glyphs to the shared lexicon.
- Footer: `Definition of Done + information radiator (Cockburn)`.
- House: cycle phases, 4.x closing gates.

### 8. loop-orchestrate
- ADD: BLUF plan line (`Plan: <n> kickoffs → <w> waves; <k> conflicts; recommended: <…>`); **English-label guard** (missing); `Structure:` footer.
- CHANGE: explicit `Depends on` column / small DAG so waves derive from a visible dependency network.
- IMPROVE: warnings as a table (`Type | Kickoffs | Evidence | Recommendation`).
- Footer: `Precedence diagramming / PDM (PMBOK) + wave layering (house method)`.
- House: wave planning, boundary, file-conflict heuristics.

### 9. loop-orchestrate-start
- IMPROVE: Step-4 report as a table (`Kickoff | Branch | Worktree | At origin/<base> | Tab | Apply order`).
- ADD: BLUF `Launched <n>/<n> sessions`; English-label guard; `Structure: house method` footer.
- House: the whole report.

### 10. roadmap
- IMPROVE (BLUF): a `Bottom line` block at the TOP of both the gate and the `.md` (core vs complete, magnitude, cheapest workaround) — today it sits after the coverage table.
- ADD: a MECE/100%-rule check line under the coverage table (`Axes in Step 1: N · in table: N · overlaps: none`); a DoR pass per phase header; `Structure:` footer. Parallel order uses `//`.
- Footer: `Minto Pyramid / MECE + INVEST / vertical slices + WBS 100%-rule + dependency DAG`.
- House: Deferrable, extra-proposal, Level 1/2, tentative route, core-vs-complete block.

### 11. roadmap-radar
- CHANGE (BLUF): move "Ready to start now / In parallel / Blocked" ABOVE the table as a headline.
- ADD: a "count by state" line (`✓ 2 · ◐ 1 · ○ 3 · ✗ 1`); `Structure:` footer.
- IMPROVE: it is the reference implementation of the state lexicon — keep its glyph set as the standard.
- Footer: `Information radiator (Cockburn) + workflow-state lexicon`.
- House: live-git state derivation, "ready now" computation.

### 12. radar (+ references/table-format.md) — v2
- CHANGE: split `Light` into `State` (shared workflow lexicon) + `Attention` (glyph set:
  `→ needs you now · ◆ awaiting gate · ‖ parked · · cleanup pending · ∅ none`); drop RED/YELLOW/ORANGE/BLACK/GREEN.
  Version table-format.md contract to **v2**.
- ADD: BLUF line above the table (`<n> need you now · <n> awaiting gate · <n> parked`); `Structure:` footer.
- IMPROVE: keep the best-effort disclaimer + evidence block.
- Footer: `Information radiator (Cockburn) + workflow-state lexicon`.
- House: Attention set, urgency order, phase pipeline.
- NOTE: loop-orchestrate-start references radar — check nothing parses the old colour words.

### 13. gaps
- ADD (BLUF): a count line (`<n> gaps (<a> noted, <b> inferred) across <m>/<M> axes`); a MECE coverage table (`Axis | Verified | Gaps found | Status`); `Structure:` footer.
- IMPROVE: `Severity` column (`▲ ● ▼`) so triage can order the backlog; shared provenance tags.
- Footer: `Gap analysis + MECE` (noted/inferred provenance = house).
- House: noted/inferred tags, 3-source model.

### 14. walkthrough
- ADD: **English-label guard** (missing — QA table headers, access block, `## Seed`); Step-7 BLUF summary (`Walkthrough: <n> scenarios, 2 files, <k> to confirm`); `Structure:` footer per lane naming the Diátaxis quadrant.
- IMPROVE: QA table gets `Pass/Fail` + `Failure signal` columns; `## Seed` becomes a table (`Fixture | Derived from (Given) | Mechanism | Key | Status`).
- Footer: `Diátaxis (Procida) + BDD Given/When/Then (North) + Living Documentation (Adzic/Martraire)`.
- House: the QA access block.

### 15. states
- IMPROVE: "what was drawn" as a table (`Machine | States | Transitions | Degraded (reason)`).
- ADD: BLUF line (`Drew <n> machine(s): <path>` / `✗ not supported: no explicit state enum`); English-label guard; `Structure:` footer.
- Footer: `Harel statecharts / UML state machine (HTML via archify)`.
- House: orthogonal+minimal filter, degrade-to-card rule.

### 16. seed
- IMPROVE: report as a table (`Fixture | Records/ids | Key | Mechanism | Target DB | Idempotent`).
- ADD: BLUF line (`Seeded <n> fixtures into <test DB>` / `✗ stopped: <missing recipe|mechanism|DB>`); English-label guard; `Structure:` footer.
- Footer: `xUnit Test Patterns — fixture setup (Meszaros)`.
- House: the test-DB-never-prod safety rule.

### 17. sdd-preview
- ADD (BLUF): a `Bottom line:` first line (`<ready to apply | needs adjustment | not ready> — Risk: ▲/●/▼ — Audit: <n> findings`); `Structure:` footer.
- IMPROVE: Reuse-first and Silent assumptions become tables; `▲ ● ▼` in Architecture smells; tag assumptions `[inferred]`/`[assumed]`.
- Footer: `BLUF (AR 25-50) + Minto for ordering` (4 sections + audit + self-assessment = house).
- House: the 4 sections, 0/1/2 reviewer self-assessment, anti-loop, autotest gate.

### 18. art
- ADD: a fixed advice-MD shape, BLUF first (`Bottom line: <n> issues (▲ a · ● b · ▼ c) — top fix: <…>`), then a findings table (`# | Finding (observable) | Principle violated (cited) | Severity | Change`); English-label guard; `Structure:` footer.
- IMPROVE: keep the human-eye gate line last.
- Footer: `Gestalt / Swiss / Bauhaus / Rams / Norman / Laws of UX / Refactoring UI` (house ordering).
- House: the 3-level judgment ordering, invariants-first rule.

## Apply checklist (one by one)

- [x] 1 research   - [x] 2 triage   - [x] 3 shot   - [x] 4 organic   - [x] 5 organic-start
- [x] 6 loop   - [x] 7 loop-start   - [ ] 8 loop-orchestrate (paused)   - [ ] 9 loop-orchestrate-start (paused)
- [x] 10 roadmap   - [x] 11 roadmap-radar   - [ ] 12 radar (v2)   - [ ] 13 gaps
- [ ] 14 walkthrough   - [ ] 15 states   - [ ] 16 seed   - [ ] 17 sdd-preview   - [ ] 18 art

Each applied skill: bump its MINOR version, keep emoji-free (whitelist glyphs only), sync + commit.
