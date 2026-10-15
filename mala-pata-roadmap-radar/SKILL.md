---
name: mala-pata-roadmap-radar
description: READ-ONLY status of a ROADMAP (not of loose SDDs — that is /mala-pata-radar). Takes a domain's roadmap .md (versioned in the repo, NOT memory), derives the state of EACH phase LIVE against git (done / in progress / pending / blocked), and shows a fixed table + what is ready to start now and which can go in parallel. It does NOT look at engram, does NOT orchestrate, does NOT execute, does NOT mutate anything. Fixed, immutable output format. Trigger — "status del roadmap", "cómo va el roadmap de <dominio>", "avance del roadmap <slug>", or the path/slug of a roadmap.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.9.0"
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

- **Git = truth, for `code` phases.** A `code` phase's "done" is confirmed ONLY against the freshly fetched integration branch (by the `Mala-Pata-Phase` commit trailer) — never by a checkbox in the `.md`, an archive-report, nor memory. A `.md` says what was planned; git says what happened. **`ops` phases are the one exception**: Railway/Neon/GitHub/manual leave NO git artifact, so their `done` is **attested** in the `.md` with mandatory evidence (URL/id/health/date) and tagged `[attested]` — never confused with a git-proven `done`.
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
3. From the `.md` extract per phase: **#**, **name**, **slug** (the stable change-name), **kind** (`code`/`ops`; default `code` if the column is absent in an old roadmap), **route**, **Depends on**, and — for `ops` phases — the declared **Status** / **Evidence** / **Verify**. From the DAG closing take the **topological order** and the **parallelizable** ones (`{..}`). If the roadmap is old and a phase has no `slug`, mark that phase `no-slug` (it cannot be matched deterministically — see Phase 2).

## Phase 1 — Freshness (live git, zero cache)

1. `git -C <repo> fetch --all --prune`.
2. Detect and **confirm** the integration branch (do not assume it: `main`/`development`/whichever the repo uses). Note its SHA for the banner.
3. If there is a `gh`/PR CLI, fetch the repo's list of open/merged PRs.

## Phase 2 — State per phase, live (code: by commit trailer · ops: by declared status)

Branch the derivation by the phase's **kind**:

**`code` phases — match by the commit trailer, NOT by branch.** Branches are ALWAYS deleted in cleanup, so the durable anchor is the trailer `Mala-Pata-Phase: <slug>` on the landing commit. Derive state from git only:
- **done** — a commit carrying `Mala-Pata-Phase: <slug>` is reachable from the freshly fetched integration branch: `git -C <repo> log <integration> --grep '^Mala-Pata-Phase: <slug>$' -E --format=%H` returns a SHA (optionally confirm `git merge-base --is-ancestor <sha> <integration>`). Evidence: that commit/merge SHA (+ PR# if `gh` has it) `[git]`.
- **in progress** — no trailer in integration yet, BUT a live branch or an OPEN PR for the slug exists with its own commits. Evidence: branch +<k> commits, or open PR# `[git]`.
- **pending** — no trailer in integration and no live branch/PR.
- **blocked** — `pending` with at least one `Depends on` not `done`.
- **Fallback (weaker — flag it):** if the slug's landing commit lost the trailer (e.g. a squash that dropped it), fall back to the roadmap's recorded `Evidence` sha/PR# (confirm the sha is an ancestor of integration) or a subject grep `git log <integration> --grep <slug>`; tag the evidence `[git, weak: no trailer]` so the human knows it is a looser match.

**`ops` phases — NO git artifact; read the declared status.** Railway/Neon/GitHub/manual leave nothing in git, so **NEVER mark an `ops` phase `pending`/`blocked` for lacking a branch/trailer.** Read the `.md`'s declared fields:
- **done** — `Status: done` AND `Evidence` present (URL/id/health/date). Evidence: that string `[attested]`.
- **pending** — `Status: pending`, OR `done` WITHOUT evidence (attested-without-evidence is NOT done — same honesty rule as gaps). Show the phase's `Verify` so the human can confirm it.
- **blocked** — pending with at least one `Depends on` not `done`.

Derivation rules:
- **`code` done is NEVER inferred from the `.md`** nor a DoD checkbox — only from the trailer reachable in git. **`ops` done requires declared `Status: done` + evidence** (git cannot prove it); tag it `[attested]`, never `[git]`.
- **A dependent of a `done` phase is NOT blocked whether the parent is `[git]` or `[attested]`** — an ops `done` satisfies deps exactly like a code `done` (this is what kills the false `blocked` cascade on infra phases).
- `no-slug` phase (old roadmap with neither slug nor trailer): mark `? (no slug)`, note "regenerate the roadmap or pass the evidence by hand". Do not guess.
- A code phase whose branch is still alive AND whose trailer is already in integration is `done` anyway; note "merged, cleanup pending" in the evidence.

## Phase 3 — What can start now + parallel

- **Ready to start now** — phases in state `pending` (not `blocked`) whose dependencies are ALL `done`.
- **In parallel** — within the "ready now", group those the DAG marks as parallelizable with each other (from the roadmap's `Parallelizable: {..}` block) and that declare no conflict — that is the wave that can be launched together.
- **In process now** — those already running (so as not to relaunch them).

## Output — fixed format (ALWAYS identical)

**Render the table as a REAL Markdown table — NEVER inside a ``` code fence. Emit EXACTLY this shape (reason first, render the table last) — never vertical `Field:/Value:` blocks, never prose; one line per cell** (a fenced table shows raw pipes and does not render). The banner, the BLUF lines, the legend and the Structure footer are plain text lines; the table in the middle is a real Markdown table. The format, in order:

Banner (2 lines):
`Roadmap: <name/slug>  ·  repo: <name>  ·  integration: <branch>@<short-sha>`
`Source: roadmap.md + live git · NO engram · <date-time>`

BLUF (3 lines):
`Bottom line: ✓ <d> done · ◐ <p> in progress · ○ <q> pending · ✗ <b> blocked  (of <N> phases)`
`Ready to start now: phases <list> (deps all done)  ·  launch in parallel: { <phase>, <phase> }`
`In progress now: <phases, or none>  ·  Blocked: phase <x> (waits for <y>)`

Then the real table:

| # | Phase | slug | Route | Depends on | Status | Evidence |
|---|---|---|---|---|---|---|
| 1 | <name> | <slug> | loop:STANDARD | — | ✓ done | merge <sha> / PR #<n> [git] |
| 2 | <name> | <slug> | organic | 1 | ◐ in progress | branch <type>/<slug> +<k> commits [git] |
| 3 | <name> | <slug> | shot | 1 | ○ pending | no trailer/branch |
| 4 | <name> | <slug> | ops | — | ✓ done | <env URL / health 200 / date> [attested] |
| 5 | <name> | <slug> | loop:LITE | 2 | ✗ blocked | waits for phase 2 |

Then the closing lines (plain text):
`Legend: ✓ done = in integration — matched by the Mala-Pata-Phase trailer (code) or declared with evidence (ops) · ◐ in progress = live branch/PR not merged · ○ pending = no trailer/branch (code) or Status pending (ops) · ✗ blocked = pending with unfinished deps · [git] = proven in git · [attested] = ops, human-declared with evidence`
`Structure: information radiator (Cockburn) + workflow-state lexicon. Live-git state derivation + ready-now computation = house method.`

- The table carries **one row per roadmap phase**, in the `.md` order. No phase is omitted.
- State with a leading curated glyph + the text token (`✓ done` / `◐ in progress` / `○ pending` / `✗ blocked`); no emoji, no invented colors.
- **Concrete evidence + provenance** per row: `[git]` (trailer/merge SHA, PR#, commits ahead) or `[attested]` (ops — the declared URL/id/health/date) — never a bare "ok". The provenance tag is MANDATORY so a git-proven state is never confused with an attested one.
- If `gh`/the PR CLI was missing, the banner says so ("PRs not queried; status by branches/merges").
- **Emit this block's structural labels verbatim in English** — section headers, field labels, table/column headers, and enum/option tokens stay English even when the conversation is in the user's language; only the values and content are localized.

## Rules

- **ZERO cache, ZERO engram.** Re-derive everything from `.md` + git on every run.
- **READ-ONLY.** Never mutate anything; never execute nor offer to execute a phase.
- **Merge = git only.** A ticked DoD or an archive-report does NOT prove a merge.
- **Match `code` phases by the commit trailer `Mala-Pata-Phase: <slug>`** (durable; branches are deleted on cleanup), never fuzzy subject semantics; **`ops` phases by their declared `Status`/`Evidence`** (git cannot see them). No slug and no trailer → `? (no slug)`, do not guess.
- **Fixed format** — same columns, same order, same lexicon, always.
- **No data**: if there is no roadmap `.md`, ask for it; if there is no git, do not run. Never invent the state of a phase.
