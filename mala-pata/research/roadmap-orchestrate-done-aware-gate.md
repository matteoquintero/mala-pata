---
idea_slug: roadmap-orchestrate-done-aware-gate
project: mala-pata-skills
domain: mala-pata-suite
roadmap: none
verdict: PROCEED
created_at: 2026-11-05T20:32:52-0500
next: /mala-pata-triage roadmap-orchestrate-done-aware-gate
size_signal: one-unit
kind: research
---
# Research: a per-phase, done-aware, route-accurate gate for roadmap-orchestrate

## Verdict: PROCEED
Replace the blanket "refuse the whole roadmap if any phase forecasts loop" gate with a per-phase planner: derive state live, drop done phases, resolve the ACTUAL route for the rest, orchestrate the organic/shot ones in waves, exclude genuine loops with a "needs a human" flag. Refuse only when every non-done phase is a genuine loop. The change is small (two SKILL.md files + one shared fragment) and aligns the planner with behavior `-orchestrate-start` already has at runtime.

Evidence tags: **[F]** verified in the files read this session. **[A]** assumption, not grounded in a file.

## Raw idea (what you asked)
`/mala-pata-roadmap-orchestrate` Hard rule #0 refuses the whole roadmap when ANY phase's Tentative route is `loop*`. Two defects seen in a real run: (1) it reads the forecast, not the re-triaged route; (2) it ignores done-ness, so already-delivered loop phases block the remaining organic work. The human had to fall back to `/mala-pata-organic-orchestrate` by hand.

## Discover

### What exists today [F]
- `mala-pata-roadmap-orchestrate/SKILL.md`: Hard rule #0 scans the `Tentative route` column BEFORE any state derivation and says "ANY phase - deferred or not, done or not". Refusal report is a BLUF plus a table (`#`, `Phase`, `slug`, `Tentative route`). Step 2 already derives per-phase state live (reusing radar Phase 2); Step 3 builds ready/wave/deferred/blocked; Step 4 has a frozen label set. Hard-rules and "What it does NOT do" both restate the refusal.
- `mala-pata-roadmap-orchestrate-start/SKILL.md`: has the SAME entry gate (Hard rule #0, "done or not"), plus a **Runtime guard**: if triage upgrades a phase to loop at Round step 3, the phase is PAUSED, reported as `✗ blocked: needs human - became loop at triage`, other non-loop phases still proceed, the loop phase's dependents stay blocked. Round step 1 derives state live (done phases are never READY); Round step 3 runs `/mala-pata-triage <slug>` once per READY code phase and tabulates `Forecast route` / `Resolved lane` / `Why it changed`; loop is "NOT dispatched". "Park-and-continue" already exists for parked phases.
- `mala-pata-roadmap/SKILL.md` Hard rule #3 and Step 4-bis: the route is a FORECAST; "a phase forecast as loop may become organic (or the other way around)"; triage rules. So the current gate contradicts its own roadmap contract.
- `mala-pata-roadmap-radar/SKILL.md` Phase 2 + `_shared/git-truth.md`: canonical done-derivation (code: any ONE git signal; ops: declared Status + Evidence `[attested]`; spike: finding + re-entry; `? unbound`, `blocked`). Phase 3 "Next step" already reads the kickoff file `mala-pata/kickoffs/<slug>.md` to pick the stage-aware command, and treats a roadmap-fixed Route as "triage done".
- Kickoff frontmatter: the organic kickoff carries `route: organic` (`mala-pata-organic` template); the loop kickoff carries `profile: <PERFIL>` and no `route:` line (`mala-pata-loop` template). Both are at `mala-pata/kickoffs/<slug>.md`, both carry `roadmap:`.
- `_shared/lane-gate.md`: the loop discriminator is "needs DESIGN"; borderline -> ask one question. Triage is "decision only, creates nothing" (orchestrate-start Round step 3).

### Root cause of the two bugs [F]
1. Gate placement: it runs BEFORE state derivation and reads only a forecast column. Both facts are explicit in the skill text.
2. "done or not" was a deliberate choice, but it conflicts with `-orchestrate-start`'s runtime behavior (pauses loops per phase) and with the forecast contract. It is a conservative shortcut, not a requirement.

## Design questions and recommended answers

### Q1. How to get the "actual" route cheaply in a read-only planner
**Recommendation: a 3-tier resolution, cheapest first, never running triage in the planner.**
1. **Kickoff exists** (`mala-pata/kickoffs/<slug>.md`, read in the repo or in the phase's worktree/branch if not on the integration branch [A: kickoffs may live only in a phase branch before merge]): read frontmatter. `route: organic` -> organic. `profile:` present (no `route:`) -> loop (genuine). This is the re-decided route (triage already ran to produce the kickoff). Tag `[kickoff]`.
2. **No kickoff**: use the forecast, tagged `forecast` and treat it as provisional. A forecast `organic`/`shot` is plannable. A forecast `loop*` is classified `loop?` (unconfirmed loop).
3. **Do not run `/mala-pata-triage` in the planner.** It is a decision skill and the planner is read-only and meant to be cheap; the executor already runs triage per READY phase at Round step 3 and is the right place for the final re-decision.

Why not re-triage per phase: heavy, may ask the human questions (lane-gate says "ask ONE question when borderline"), and a planner must stay non-interactive. Why not forecast only: that is bug 1.

**Fallback for `loop?` (forecast loop, no kickoff, not done).** Exclude it from the wave and flag it `needs a human - forecast loop, not yet triaged`, with the hint `/mala-pata-triage <slug>` first (it may re-decide to organic, in which case the next planner run picks it up via the kickoff) and then `/mala-pata-loop` + `/mala-pata-loop-start` if it stays loop. Rationale: conservative (never auto-orchestrate something forecast as needing design) yet not a batch refusal, and it gives the human the cheap, correct next action. [A: excluding rather than "optimistically treat as organic" is the safer default; open decision D2.]

### Q2. Dependency / wave impact
- **Done dependency (any kind, git or attested)**: satisfies dependents exactly as today (radar rule: "a dependent of a done phase is NOT blocked"). Done phases are dropped from the waves and shown as `✓ done` rows; no change needed.
- **Excluded still-loop dependency**: it is NOT done, so its dependents are `✗ blocked`, with Note `waits for phase <n> (needs a human - loop)`. They are NOT excluded from the batch's DAG; they simply cannot become READY until the human lands the loop phase. This matches the executor's Runtime guard ("the loop phase's dependents stay blocked until the human merges it").
- Consequence for round forecast: rounds stop at the first dependency chain that goes through an excluded loop; the forecast states `rounds beyond N require phase <n> (human)`.
- Independent branches of the DAG are unaffected and still orchestrate (this is the whole point; mirrors "Park-and-continue").
- Genuine-loop dependency whose dependents are `deferred`: deferral wins (not started anyway).

### Q3. The all-non-done-are-loop edge case: report shape
Only when the set {non-done, non-ops-attestable phases} contains zero orchestrable (organic/shot) phases AND at least one loop phase. A roadmap with ZERO non-done phases is NOT a refusal: it is the existing "all done" report. A roadmap whose only non-done phases are `ops` (human-attested) or blocked-on-ops is the normal plan with ops-attest rows, not a refusal.

Recommended fixed shape (English labels verbatim, per `_shared/structural-labels.md`; only values localized):
- BLUF: `Needs you: roadmap <slug> - <n> remaining phase(s), all need a human (loop). Nothing to orchestrate; ✓ <d> done · ✗ <n> need you`
- Table (real Markdown, one line per cell), column headers frozen: `#` | `Phase` | `slug` | `Route (actual)` | `Route source` | `Status` | `Note`. `Route source` enum: `kickoff` | `forecast`. `Note` carries `forecast loop, not yet triaged` or `kickoff profile: <PERFIL>`.
- Next step per phase (plain text, copy-paste, never run): kickoff present -> `/mala-pata-loop-start <abs kickoff path>`; no kickoff -> `/mala-pata-triage <slug>` then `/mala-pata-loop <slug>`. No `/mala-pata-roadmap-orchestrate-start` handoff line (nothing to orchestrate).
- This reuses the existing refusal-report vocabulary (BLUF + table) so it stays visually consistent; it is no longer called "Refused".

### Q4. Does `-orchestrate-start` need a change?
Yes, two edits, smaller than the planner's:
- **Entry gate (Hard rule #0)**: same defect (forecast-only, "done or not"). Replace with the same per-phase partition. The Runtime guard already covers "became loop at triage" and must be kept; extend it with the excluded `loop?` set so the Round 1 report lists them as `✗ blocked: needs human - loop` from the start instead of refusing.
- **Done-skip**: already covered. Round step 1 derives state live and READY requires `pending`/`in progress`, so done phases are never launched; "Every non-deferred phase done -> final report" exists. Only the gate and the two "refuses any roadmap containing a loop phase" sentences (frontmatter description, Hard rules, "What it does NOT do") need rewriting. The Final report `Status` column should gain the `✗ blocked: needs human - loop` value (already used by the guard) [F: guard text names it].

## Recommended gate behavior (replaces Hard rule #0)
1. Load roadmap (Step 1), derive every phase's live state (Step 2, unchanged), BEFORE any route decision.
2. Drop `✓ done` phases from planning (they still appear as rows and still satisfy dependents).
3. For each non-done code phase resolve the actual route per Q1 (kickoff `route:`/`profile:` -> else forecast). Partition: orchestrable = organic/shot (+ ops attest rows); needs-human = loop (genuine via kickoff `profile:`) or `loop?` (forecast, no kickoff).
4. Plan waves over orchestrable phases only; needs-human phases are excluded from waves and listed in a new Warnings type `needs human (loop)`; their dependents are `✗ blocked`. If orchestrable is empty and needs-human is non-empty -> the Q3 report. Never emit "Refused".
Hand-off line stays `/mala-pata-roadmap-orchestrate-start <slug>` whenever at least one orchestrable phase exists; the executor re-derives and re-triages, so the planner's route claim is advisory.

## Open decisions (owner)
- **D1. Kickoff location**: read kickoffs only from the integration branch checkout, or also from phase branches/worktrees? [A] Recommend integration + `git show <branch>:mala-pata/kickoffs/<slug>.md` for in-progress branches; cheap and read-only.
- **D2. Unconfirmed `loop?` default**: exclude-and-flag (recommended) vs include-and-let-executor-triage. Including is more automatic but plans a wave around a phase that may park at runtime.
- **D3. Column naming**: rename the table column `Route (forecast)` to `Route (actual)` + new `Route source`, or keep `Route (forecast)` and add `Route source`. Either changes frozen labels; pick one and update both skills in lockstep.
- **D4. Mixed routes in legacy roadmaps** (no `Kind` column): treat as `code` (existing default); no new decision needed.
- **D5. Version bump size**: minor (behavior change, label-set change) for both skills. [A]

## Files that would change (later implementation pass; NOT done here)
1. `mala-pata-roadmap-orchestrate/SKILL.md`: frontmatter `description`; replace "Hard rule #0 - ENTRY GATE" with the per-phase partition; Step 1 point 3 (extract kickoff `route:`/`profile:` per phase); Step 2 (add route resolution after state); Step 3 (exclude needs-human, blocked-by-loop dependents, round-forecast note); Step 4 (BLUF, `Route` column and `Route source`, Warnings `needs human (loop)` type, new all-loop report, frozen-label enumeration); "Hard rules" and "What it does NOT do" bullets that restate the refusal.
2. `mala-pata-roadmap-orchestrate-start/SKILL.md`: frontmatter `description`; replace Hard rule #0 with the same partition (keep and extend the Runtime guard); Step 0 extraction; Round step 1 (exclude needs-human from READY, report them); Round step 3 table; Final report Status values; "Hard rules" and "What it does NOT do" bullets.
3. Optional new `_shared/` fragment (e.g. `route-resolution.md`) holding the 3-tier route resolution + partition so both skills reference one source (house rule: single source of truth, as `git-truth.md` and `structural-labels.md` do). If skipped, duplicate the text in both and risk drift.
4. Sync/mirror, version bump and Conventional commit via `/mala-pata-skill` (not part of this research).
`mala-pata-roadmap-radar` and `mala-pata-roadmap` need NO change (radar is the done-derivation source; roadmap already states the forecast contract).

## Handoff
`/mala-pata-triage roadmap-orchestrate-done-aware-gate` (one unit; routes to organic or shot-sized skill edit via `/mala-pata-skill`).
