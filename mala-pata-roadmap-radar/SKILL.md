---
name: mala-pata-roadmap-radar
description: READ-ONLY status of a ROADMAP (not of loose SDDs — that is /mala-pata-radar). Takes a domain's roadmap .md (versioned in the repo, NOT memory), derives the state of EACH phase LIVE against git (done / in progress / pending / blocked), and shows a fixed table + what is ready to start now and which can go in parallel. It does NOT look at engram, does NOT orchestrate, does NOT execute, does NOT mutate anything. Fixed, immutable output format. Trigger — "status del roadmap", "cómo va el roadmap de <dominio>", "avance del roadmap <slug>", or the path/slug of a roadmap.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.4.0"
---

# /mala-pata-roadmap-radar — progress of a roadmap against git (fixed format)

Input: **the one provided by the CLI** — the path to a roadmap `.md` (`mala-pata/roadmap/<slug>.md`) or the roadmap's slug/domain.

Your job: show, in a **fixed format that is always the same**, how a domain's roadmap is going — phase by phase — deriving each state **live against git**, and marking **what can start now and which in parallel**. It is to roadmaps what `/mala-pata-radar` is to loose SDDs, with two deliberate differences: the **unit is a roadmap phase** (not a change), and the **source is the roadmap `.md` + git, NEVER engram**.

> **This is not `/mala-pata-radar`.** radar discovers SDDs/changes from memory and confirms them with git. This skill does NOT touch memory: it reads the roadmap `.md` (which lives in the repo) and measures git. If what you want is the state of loose SDDs, that is radar.

## Requirements (orchestrate, do not reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP and ask to install it, do not start):
  - `git` — source of truth for progress. Always present; requires no installation.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded):
  - `gh` (or the project's PR CLI, e.g. `az repos`) — PR status. Fallback: only local/remote branches and merges; flag that PRs were not queried. Install: `brew install gh`.
- **Explicit — does NOT use engram.** The roadmap `.md` (in the repo) + git are the only two sources. Do not search memory.

Check: `command -v <tool>`. If a mandatory tool is missing, do not continue.

## Hard principles (non-negotiable)

- **Git = truth.** "done" is confirmed ONLY against the freshly fetched integration branch — never by a checkbox in the `.md`, an archive-report, nor memory. A `.md` says what was planned; git says what happened.
- **Zero cache, zero memory.** Every run re-derives everything from the `.md` + live git. Reporting a state without re-measuring it in this run is forbidden. NO engram.
- **Read-only.** Never commit, push, merge, destructive fetch nor write. Running this radar is always safe.
- **You take no attributions.** You only report which phase is in which state and what can start. You NEVER execute nor OFFER to execute a phase (triage, apply, PR, merge). Your output ENDS at the report — closing with "¿arranco X?" is forbidden.
- **Fixed format ALWAYS** — same order, same columns, same lexicon, on every run (mechanical memory for the human).

## Phase 0 — Load the roadmap (git, not memory)

1. Resolve the project root: `git -C <cwd> rev-parse --show-toplevel`.
2. Resolve the roadmap `.md`:
   - If the input is a path → `Read` directly.
   - If it is a slug/domain → look for `mala-pata/roadmap/<slug>.md` (or the default the roadmap used). If there are several candidates and none was specified → list the available `.md` files and ask which one (a single question, you stop and wait).
   - If it does not exist → say so and STOP; do not invent phases.
3. From the `.md` extract per phase: **#**, **name**, **slug** (the stable change-name), **route** (organic/loop:PROFILE/shot), **Depends on**, and from the DAG closing the **topological order** and the **parallelizable** ones (`{..}`). If the roadmap is old and a phase has no `slug`, mark that phase `no-slug` (it cannot be matched deterministically — see Phase 2).

## Phase 1 — Freshness (live git, zero cache)

1. `git -C <repo> fetch --all --prune`.
2. Detect and **confirm** the integration branch (do not assume it: `main`/`development`/whichever the repo uses). Note its SHA for the banner.
3. If there is a `gh`/PR CLI, fetch the repo's list of open/merged PRs.

## Phase 2 — State per phase, live (match by slug)

For each phase, match against git by its **slug**: a branch or PR whose name is `<slug>` or ends in `/<slug>` (the roadmap's convention: change-name = slug, branch `<type>/<slug>`). Derive the state — **only from git**:

- **done** — the phase is **merged into the freshly fetched integration branch**. Confirm by ANY of: (1) `git branch --merged <integration>` shows the phase's branch; (2) fallback for when the branch was already deleted by loop-start cleanup (and for squash merges): `git log <integration> --grep <slug>` finds a merge/squash commit mentioning the slug; (3) when `gh` is available, a merged PR for the slug. Evidence: merge/squash commit SHA or PR#, noting "branch deleted after merge" when applicable.
- **in progress** — the branch or an OPEN PR exists for the slug, with its own commits, but NOT merged. Evidence: branch + number of commits ahead, or open PR#.
- **pending** — there is no branch nor PR for the slug.
- **blocked** — it is `pending` BUT at least one of its `Depends on` is NOT `done`. (It is a `pending` that explains why it cannot start yet.)

Derivation rules:
- **done is NEVER inferred from the `.md`** nor from a DoD checkbox — only from the real merge in git.
- `no-slug` phase (old roadmap): do not key it by fuzzy semantics. Mark it `? (no slug)` in Status, with the note "the roadmap did not record a slug; regenerate the roadmap or pass the branch by hand". Do not guess.
- A merged branch whose worktree/branch is still alive is `done` anyway (the merge rules); you may note it in the evidence as "merged, cleanup pending".

## Phase 3 — What can start now + parallel

- **Ready to start now** — phases in state `pending` (not `blocked`) whose dependencies are ALL `done`.
- **In parallel** — within the "ready now", group those the DAG marks as parallelizable with each other (from the roadmap's `Parallelizable: {..}` block) and that declare no conflict — that is the wave that can be launched together.
- **In process now** — those already running (so as not to relaunch them).

## Output — fixed format (ALWAYS identical)

```
Roadmap: <name/slug>  ·  repo: <name>  ·  integration: <branch>@<short-sha>
Source: roadmap.md + live git · NO engram · <date-time>

| # | Phase | slug | Route | Depends on | Status | Evidence |
|---|------|------|------|-----------|--------|-----------|
| 1 | <name> | <slug> | loop:STD | — | ✓ done | merge <sha> / PR #<n> |
| 2 | <name> | <slug> | organic | 1 | ◐ in progress | branch <type>/<slug> +<k> commits / PR #<n> |
| 3 | <name> | <slug> | shot | 1 | ○ pending | no branch |
| 4 | <name> | <slug> | loop:LITE | 2 | ✗ blocked | waits for phase 2 |

Ready to start now: <phases whose deps are all done>
  In parallel (can be launched together): { <phase>, <phase> }
In progress now: <phases with live branch/PR>
Blocked by dependencies: <phase> → waits for <phase(s)>

Legend: ✓ done = merged to integration (git) · ◐ in progress = live branch/PR not merged · ○ pending = no branch · ✗ blocked = pending with unfinished deps
```

- The table carries **one row per roadmap phase**, in the `.md` order. No phase is omitted.
- State with a leading curated glyph + the text token (`✓ done` / `◐ in progress` / `○ pending` / `✗ blocked`); no emoji, no invented colors.
- **Concrete evidence** per row (merge SHA, PR#, number of commits ahead, or "no branch") — never a bare "ok".
- If `gh`/the PR CLI was missing, the banner says so ("PRs not queried; status by branches/merges").
- **Emit this block's structural labels verbatim in English** — section headers, field labels, table/column headers, and enum/option tokens stay English even when the conversation is in the user's language; only the values and content are localized.

## Rules

- **ZERO cache, ZERO engram.** Re-derive everything from `.md` + git on every run.
- **READ-ONLY.** Never mutate anything; never execute nor offer to execute a phase.
- **Merge = git only.** A ticked DoD or an archive-report does NOT prove a merge.
- **Match by exact slug**, never fuzzy semantics. No slug → `? (no slug)`, do not guess.
- **Fixed format** — same columns, same order, same lexicon, always.
- **No data**: if there is no roadmap `.md`, ask for it; if there is no git, do not run. Never invent the state of a phase.
