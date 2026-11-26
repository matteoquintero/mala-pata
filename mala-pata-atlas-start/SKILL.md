---
name: mala-pata-atlas-start
cognitive_tier: standard
description: >
  RUNS the atlas that `/mala-pata-atlas` wrote — walks its roadmap of
  walkthrough-units phase by phase, in risk order, honoring dependencies, and
  for EACH unit drives the full existing pipeline (`/mala-pata-walkthrough`
  authors the scenarios if the unit has none → `/mala-pata-seed` seeds the test
  DB → `/mala-pata-walkthrough-start` runs the browser smoke and leaves
  evidence). It honors each unit's `delicacy` (high → the human runs it) and
  keeps a LIVE coverage+run ledger so nothing is skipped and no unit is marked
  done without its verdict observed. It is the executor twin of `/mala-pata-atlas`
  (which plans, read-only). LIGHT by design: NO worktrees, NO new branches, NO
  merges, NO parallel tabs — a QA smoke is read-only against the test env. It
  does NOT touch app code, does NOT run against prod, does NOT flip `qa_done`
  (the human's flag). Sequential and resumable.
  Trigger — "ejecutá el atlas de <feature>", "corré el roadmap de walkthroughs de
  <feature>", "/mala-pata-atlas-start <slug>", "probá todo el atlas de <feature>
  por fases".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "0.1.3"
---

# /mala-pata-atlas-start — run a feature's whole QA atlas, unit by unit, phase by phase

Input: **the one delivered by the CLI** — normally just the **slug** (resolves to `mala-pata/atlas/<slug>.md` from the repo root); an absolute path also works. **Prefer the slug — the full path is a pain.**

Your job: **execute** the coverage plan that `/mala-pata-atlas` drew — walk its roadmap of walkthrough-units in order, and for each unit drive the existing pipeline end to end so the big feature's whole surface actually gets tested, with evidence, **without forgetting a single unit**. You are the executor counterpart of `/mala-pata-atlas` (which plans, read-only), exactly as `/mala-pata-walkthrough-start` is the executor of one walkthrough. You run the plan; you do not decide what the coverage is (the atlas did) nor what counts as critical (the per-unit `delicacy` + the human do).

> **Determinism over speed.** You run the units in the atlas's order, one at a time, and a unit is `done` ONLY after its run verdict is observed — never marked done by assumption. This is the whole point: an agent that forgets half a big feature's QA is the failure this skill exists to prevent.
> **LIGHT executor — nothing like the build orchestrators.** A QA smoke is read-only against the test env and leaves evidence; it merges nothing. So you create **NO worktrees, NO new branches, NO merges, NO parallel Warp tabs**. You run in place. (That is what separates this from `/mala-pata-roadmap-orchestrate-start`, which delivers *construction*.)
> **Sequential, not parallel.** Playwright MCP is a single browser session; running several browser smokes at once in one session flakes. You run units one after another. Independent units still run — just in sequence, not in parallel.

## Requirements (orchestrate, do not reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP): `git` — resolve the repo root (`git rev-parse --show-toplevel`) and the atlas/walkthrough paths.
- **Recommended** (with fallback — warn in one line and continue degraded):
  - **Playwright MCP** (`mcp__…playwright__*`) — the browser driver for the run half. Delegated to `/mala-pata-walkthrough-start`, which already handles its absence (treats the unit as `delicacy: high` → hands it to the human). Do NOT fake a run.
  - `codegraph` / `serena` — for the authoring half (`/mala-pata-walkthrough`). Fallback: grep/Read.
  - `engram` — the atlas / walkthrough pointers. Fallback: the atlas `.md` is the source.

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP). If the mandatory tool is missing, do not continue.

## Hard rules

> **#1 — LIGHT, in place.** NO worktrees, NO new branches, NO merges, NO parallel tabs. You run the pipeline against the test env on the current checkout. Anything that looks like it needs a worktree/branch/merge is NOT this skill's job.
> **#2 — Test DB / env ONLY, never prod.** Apply `_shared/mala-pata-test-db-guard.md` verbatim (it supersedes any restatement here): seeding and running happen against the project's **test DB / test env** only; if you cannot confirm the target is the test one, **STOP**. The seed and the run sub-skills enforce this too — do not weaken it.
> **#3 — Delicacy decides who runs each unit.** Each unit carries a `delicacy` (from the atlas / the walkthrough frontmatter). `low`/`medium` → the agent runs the smoke; **`high` → PAUSE the unit, hand the human the step list + access block, mark it `⚑ needs human`, and continue with the rest.** On any doubt, round UP.
> **#4 — Never mark a unit done without its verdict (validate everything).** A unit is `✓ pass` only after `/mala-pata-walkthrough-start` returns a pass (assertions + console/network gate). No assumed passes, no faked runs. A `✗` on a unit that others depend on stops THAT chain; independent units continue.
> **#5 — Absolute paths for evidence.** Evidence is written by `/mala-pata-walkthrough-start` to `<ABS>/mala-pata/walkthroughs/<unit>/evidence/`; report it absolute, with the resolved `<opener>` line (`_shared/mala-pata-platform.md`), never a repo-relative path.

## Phase 0 — Load the atlas

1. Resolve the atlas, slug-first: a **slug** → `<repo-root>/mala-pata/atlas/<slug>.md`; an **absolute path** → use it; or the `atlas/<slug>` engram pointer. None resolves → **STOP**, ask for the slug. If there is no atlas → route to `/mala-pata-atlas` to plan it first (you do not invent the coverage).
2. Read the **coverage matrix** and the **walkthrough roadmap** (units with their Scope, Case classes, Risk, Depends on, Delicacy, Phase) + the frontmatter (`feature`, `domain`, `roadmap`).

## Phase 1 — Derive the run order (live, done-aware)

1. Order the units by **Phase**, then by **Risk** (high first) within a phase; respect **Depends on** (a unit never runs before its prerequisites).
2. **Done-aware (live, not cached):** a unit is already `done` when its walkthrough's `qa_done: done` (the human's flag) — skip it, report it as carried. Everything else is pending. Do not re-run what the human already signed off.
3. Announce the plan: `<n>` pending units across `<p>` phases, in order, with which are `delicacy: high` (will be handed to the human).

## Phase 2 — Per-unit drive (the loop — author → seed → run)

For each pending unit, in order, drive the existing pipeline end to end:

1. **Author if missing.** If `<repo-root>/mala-pata/walkthroughs/<unit>-qa.md` does NOT exist → run **`/mala-pata-walkthrough <unit>`** to author its scenarios (it keeps its own human gate and writes the two lanes + the `## Seed` recipe). If it already exists (authored in a prior pass) → reuse it; do not re-author.
2. **Seed.** Run **`/mala-pata-seed <unit>`** — seeds the walkthrough's `## Seed` recipe into the test DB, idempotently. If the unit touches no data, seed skips itself.
3. **Run.** Run **`/mala-pata-walkthrough-start <unit>`** — it honors `delicacy` (Hard rule #3): `low`/`medium` → the agent runs the browser smoke and leaves evidence; `high` → it does not run the sensitive steps, it seeds + opens the app + hands the human the step list. It returns a verdict (assertions + console/network gate) and the absolute evidence path.
4. **Record the verdict** in the live ledger: `✓ pass` · `✗ fail` · `⚑ needs human` (delicacy high, awaiting the human) · `○ pending` (blocked by a failed prerequisite). A `✗` on a unit others depend on → stop that dependency chain, keep running the independent units, collect all outcomes (never bail on the whole atlas because one unit failed).

Do not skip a unit silently. If a unit cannot run for a real reason (missing prerequisite, unconfirmed test DB), mark it with that reason — never drop it from the ledger.

## Phase 3 — Phase boundary (keep a long run legible)

After each phase's units complete, emit a one-line phase rollup (`Phase <k>: <pass>/<units> · <h> handed to human · <f> fail`) before starting the next phase, so a long QA is readable as it goes. Then continue to the next phase.

## Phase 4 — Close (MANDATORY: BLUF + run ledger)

**BLUF first** — one `Result:` line: `Result: ✓ atlas run · <pass>/<total> units · <p> phases · <h> handed to human` (or `◐ partial: <reason>` / `✗ blocked: <reason>`).

Then the **run ledger** — one unit per row, in run order:

| Walkthrough | Phase | Delicacy | Result | Evidence |
|---|---|---|---|---|
| `WT-1 <name>` | 1 | medium | ✓ pass | `<ABS>/…/WT-1/evidence/` |
| `WT-2 <name>` | 2 | high | ⚑ needs human | seeded · step list handed |
| `WT-3 <name>` | 2 | low | ✗ fail | `<ABS>/…/WT-3/evidence/` (console error) |

- **Coverage rollup:** `run ✓ <pass>` · `failed <f>` · `handed to human <h>` · `pending <o>` · `carried (qa_done) <c>`. This is the execution face of the atlas's coverage ledger.
- **Next step** — fix the `✗` units; run the `⚑ needs human` units by hand from their step list; the human flips `qa_done: done` per walkthrough once it genuinely passes by hand (never flipped here). Re-running this skill is resumable — it skips the already-`done` units.
- **Structure:** `Risk-ordered sequential execution of a coverage plan + per-unit pipeline drive (author → seed → run) + delicacy-driven who-runs-it + done-aware resume. Light in-place executor (no worktrees/branches/merges) = house method.`

**Frozen structural label set** (this block applies `_shared/mala-pata-structural-labels.md` verbatim — emit these EXACTLY, in English, even when the conversation is in another language; only Value/Evidence content and surrounding prose are localized):
`Result:` · ledger headers `Walkthrough | Phase | Delicacy | Result | Evidence` · delicacy tokens `low` `medium` `high` · result tokens `✓ pass` `✗ fail` `⚑ needs human` `○ pending` · `Coverage rollup:` · `Next step` · `Structure:`. Rows are one-per-unit, in run order. No label is translated, renamed or added.

This block is the only way to close on the happy path. **Only exceptions:** Phase 0 STOP (no atlas resolves); a Hard rule #2 STOP (unconfirmed test DB); a `delicacy: high` hand-off that pauses for the human.

## Persistence

The per-unit evidence (written by `/mala-pata-walkthrough-start`) and the per-unit `qa_done` flag ARE the durable record; this skill's close is the rollup over them. Optionally leave a one-line engram pointer `atlas/<slug>/run` for discoverability. **Never flip `qa_done`** — that is the human's flag, set only after a human actually runs/accepts the walkthrough.

## What it does NOT do (invariants)

- Does NOT create worktrees, new branches, merges, or parallel tabs — light, in place.
- Does NOT run against prod, nor the sensitive steps of a `delicacy: high` unit.
- Does NOT invent coverage — it runs the atlas's units; a missing atlas routes to `/mala-pata-atlas`.
- Does NOT author scenarios itself — it delegates authoring to `/mala-pata-walkthrough` (which keeps its gate).
- Does NOT fake a run, does NOT mark a unit done without its verdict, does NOT flip `qa_done`, does NOT write app code, does NOT commit.

## Relation to the family

- **Executor twin of** `/mala-pata-atlas` (planner / executor split, like `mala-pata-roadmap` + `mala-pata-roadmap-orchestrate-start`, but LIGHT — QA, not construction).
- **Drives** the existing per-unit pipeline: `/mala-pata-walkthrough` → `/mala-pata-seed` → `/mala-pata-walkthrough-start`, each keeping its own gates and guards.
- **Done-aware** like `/mala-pata-roadmap-radar` / `/mala-pata-roadmap-orchestrate-start` — it skips units the human already signed off (`qa_done: done`) and is resumable.
- **Different from** the build orchestrators (`roadmap`/`organic`-orchestrate-start): those deliver code through worktrees and merges; this one only runs read-only QA smokes and leaves evidence.
