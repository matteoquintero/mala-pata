---
name: mala-pata-icebox-radar
description: READ-ONLY status of an ICEBOX — how many of its cubes are still frozen, thawed (defrosted + routed, not started), in progress, or done, deriving `done` LIVE against git (the twin of /mala-pata-roadmap-radar, for cubes instead of roadmap phases). Source is the icebox `.md` (in the repo) + git — NEVER engram, zero cache, re-derived every run. Cubes are an independent pool (no DAG, no blocked/parallel). It does NOT orchestrate, does NOT execute, does NOT mutate anything. Fixed, immutable output format. Trigger — "status del icebox <slug>", "cómo va el icebox", "cuántos cubes quedan", "icebox radar <slug>".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "0.1.1"
---

# /mala-pata-icebox-radar — status of an icebox against git (fixed format)

Input: **the one delivered by the CLI** — an **icebox slug** (resolves to `mala-pata/icebox/<slug>.md`) or the path to the file.

Your job: show, in a **fixed format that is always the same**, how an icebox is going — cube by cube — deriving each `done` **live against git**. It is to the icebox what `/mala-pata-roadmap-radar` is to a roadmap, with one simplification: cubes are an **independent pool** (no dependencies), so there is no `blocked` state and no parallel-wave DAG.

> **This is not `/mala-pata-roadmap-radar`.** That one reads a roadmap's phases; this one reads an icebox's cubes. Both derive `done` from git, never from a checkbox.

## Requirements (orchestrate, do not reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP): `git` — source of truth for `done`. Always present.
- **Recommended** (with fallback — warn in one line and continue degraded):
  - `gh` (or the project's PR CLI) — PR status. Fallback: local/remote branches and merges only; flag that PRs were not queried.
- **Explicit — does NOT use engram for state.** The icebox `.md` (in the repo) + git are the only two sources.

Check: `command -v <tool>`. If a mandatory tool is missing, do not continue.

## Hard principles (non-negotiable)

- **Git = truth for `done`.** A cube is `done` ONLY when its change-slug landed in the freshly fetched integration branch (merge / PR / slug commit / delivering artifact / optional `Mala-Pata-Phase` trailer) — never by the icebox's own status line. The `.md` says what was routed; git says what shipped.
- **Zero cache, zero engram.** Re-derive everything from the `.md` + live git on every run. Reporting a state without re-measuring it is forbidden.
- **Read-only.** Never commit, push, merge, destructive fetch, nor write. Never execute nor OFFER to execute a cube. Emitting the next command as copy-paste TEXT is allowed and is NOT "offering to execute".
- **Fixed format ALWAYS** — same order, same columns, same lexicon, every run.

## Phase 0 — Load the icebox (git, not memory)

1. Resolve the repo root: `git -C <cwd> rev-parse --show-toplevel`.
2. Resolve the icebox `.md`: a path → `Read` it; a slug → `mala-pata/icebox/<slug>.md`. If none resolves → **STOP** and ask for the slug (do not invent cubes).
3. Read the frontmatter `domain`/`project`, and from `## Cubes` every cube: `c<N>`, DoD, size-hint, and `status` (`frozen` / `thawed(route:…, research:…)` / `reconsider:…` / `done`). The `thawed` line carries the **change-slug** (`research:<cube-slug>`) — that is what you match against git.

## Phase 1 — Freshness (live git, zero cache)

1. `git -C <repo> fetch --all --prune`.
2. Detect and **confirm** the integration branch (`main`/`development`/whichever the repo uses); note its SHA for the banner.
3. If there is a `gh`/PR CLI, fetch the repo's open/merged PRs.

## Phase 2 — State per cube, live

> **Canonical done-derivation — single source of truth.** Apply `_shared/mala-pata-git-truth.md` verbatim; it supersedes any restatement in this skill. Do not paraphrase or re-derive it.

Branch by the cube's icebox status:

- **`frozen`** — never defrosted, so it has no change-slug and no git footprint → report `frozen` (pending defrost). Do not look in git for it.
- **`thawed`** (defrosted + routed) — match its change-slug against git reality, any ONE signal confirming (all equal weight, the trailer OPTIONAL): a `Mala-Pata-Phase: <slug>` trailer in integration, a merged PR for the slug, a merged branch `<type>/<slug>` or a slug commit ancestor of integration, a delivering artifact, or a recorded sha ancestor. Derive:
  - **done** — any signal confirms the change landed in integration. Evidence: the SHA / PR# / artifact, `[git]`.
  - **in progress** — not in integration yet, but a live branch or OPEN PR for the slug has its own commits.
  - **thawed** — routed by defrost but no branch/PR/commit exists yet (not started).
  - **`? unbound (confirm)`** — implementing commits clearly exist but cannot be tied to the slug → show them and ask; NEVER a confident `thawed` when work demonstrably exists.
- **`reconsider`** — research proposed killing/parking it → report `reconsider` with the one-line reason; it is not pending work.

Rules:
- **`done` is NEVER the icebox status line** — it is git reality. The `.md` says routed; git says shipped.
- Cubes are independent: **no `blocked`, no dependency wave.** Do not invent ordering between cubes.

## Phase 3 — What is actionable now

- **To melt** — `frozen` cubes: they need a defrost before they can be routed.
- **To run** — `thawed` cubes not yet started: ready to execute via triage.
- **In progress** — cubes with a live branch/PR (so as not to relaunch).
- **Icebox completion (derived from git, NOT stored)** — when ALL non-`reconsider` cubes are `done`, the icebox is complete; its finish is the **latest git date among the done cubes**. If not complete, say "in progress, <d>/<N>". Never invent it.

## Output — fixed format (ALWAYS identical)

**Render the table as a REAL Markdown table — NEVER inside a code fence. Reason first, render the table last; one line per cell.** The banner, BLUF, legend and Structure footer are plain text; the middle is a real Markdown table. In order:

Banner (3 lines):
`Icebox: <name/slug>  ·  domain: <domain>  ·  repo: <name>  ·  integration: <branch>@<short-sha>`
`Source: icebox.md + live git · NO engram · <date-time>`
`Timeline: created <icebox created_at> · <when 100% done: completed <latest git date among done cubes> (derived from git) — else: in progress, <d>/<N> cubes done>`

For the run time `<date-time>`: fill it from the machine's local clock — run `date '+%Y-%m-%dT%H:%M:%S%z'` and use its exact output (local time with UTC offset, e.g. `2026-11-01T17:25:40-0500`); never invent the time and never default to UTC. (The Timeline's `created_at` is the icebox's stored value — read it, never regenerate it.)

BLUF (2 lines):
`Bottom line: ✓ <d> done · ◐ <p> in progress · ○ <t> thawed · ❄ <f> frozen · ✗ <k> reconsider  (of <N> cubes)`
`To run now: thawed <list>  ·  To melt: frozen <list>  ·  In progress: <list, or none>`

Then the real table:

| # | Cube (DoD) | Change-slug | Route | Status | Evidence |
|---|---|---|---|---|---|
| c1 | <one line> | <cube-slug> | organic | ✓ done | merge <sha> / PR #<n> [git] |
| c2 | <one line> | <cube-slug> | loop | ◐ in progress | branch <type>/<slug> +<k> commits [git] |
| c3 | <one line> | <cube-slug> | shot | ○ thawed | routed by defrost, not started |
| c4 | <one line> | — | — | ❄ frozen | pending defrost |
| c5 | <one line> | — | — | ✗ reconsider | <research's one-line reason> |

Then, for the actionable cubes, the **Next step** block (plain text, copy-paste — the radar does NOT run it):
`Next step per cube:`
`  · frozen cubes <list>: /mala-pata-icebox-defrost <slug> (melt them)`
`  · thawed cube <c> (<cube-slug>, route <lane>): /mala-pata-triage <cube-slug>`
(one line per actionable cube; triage re-decides the lane on arrival.)

Then the closing lines (plain text):
`Legend: ✓ done = change-slug landed in integration (git) · ◐ in progress = live branch/PR not merged · ○ thawed = defrosted + routed, not started · ❄ frozen = not defrosted yet · ✗ reconsider = research proposed kill/park · ? unbound = work exists but not tied to the slug (confirm) · [git] = proven in git`
`Structure: information radiator (Cockburn) + workflow-state lexicon. Live-git done-derivation for an independent cube pool = house method.`

- One row per cube, in `.md` order. No cube omitted.
- State with a leading curated glyph + the text token; concrete evidence + `[git]` provenance per `done`/`in progress` row — never a bare "ok".
- If `gh`/the PR CLI was missing, the banner says so.
- **Emit this block's structural labels verbatim in English** — headers, field labels, table/column headers, and enum tokens stay English even when the conversation is in the user's language; only values and content are localized.

## Rules

- **ZERO cache, ZERO engram for state.** Re-derive from `.md` + git every run.
- **READ-ONLY.** Never mutate; never execute nor offer to execute a cube.
- **`done` = git only.** The icebox status line does NOT prove a merge.
- **Cubes are independent** — no `blocked`, no dependency wave; `frozen` cubes have no git footprint.
- **Fixed format** — same columns, order, lexicon, always.
- **No data**: no icebox `.md` → ask for it; no git → do not run. Never invent a cube's state.

## Relation to the family

- **The status end** of the icebox family: `mala-pata-icebox` (freeze) → `mala-pata-icebox-defrost` (melt → route) → **`mala-pata-icebox-radar`** (this: how many cubes shipped, against git).
- **Twin of** `/mala-pata-roadmap-radar` (same live-git `done` derivation) — but for an independent cube pool, so simpler (no DAG). **Different from** `/mala-pata-domain-radar` (a whole domain's index); the icebox-radar is one icebox's cube status.
