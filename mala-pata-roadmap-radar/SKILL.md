---
name: mala-pata-roadmap-radar
description: READ-ONLY status of a ROADMAP (not of loose SDDs — that is /mala-pata-radar). Takes a domain's roadmap .md (versioned in the repo, NOT memory), derives the state of EACH phase LIVE against git (done / in progress / pending / blocked), and shows a fixed table + what is ready to start now, which can go in parallel, and the stage-aware next command per ready phase (pipeline triage → lane → -start, as copy-paste text). It does NOT look at engram, does NOT orchestrate, does NOT execute, does NOT mutate anything. Fixed, immutable output format. Trigger — "status del roadmap", "cómo va el roadmap de <dominio>", "avance del roadmap <slug>", or the path/slug of a roadmap.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.11.0"
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

- **Git = truth, for `code` phases.** A `code` phase's "done" is confirmed ONLY against the freshly fetched integration branch (by ANY git evidence — a merge, a PR, a slug commit, a delivering artifact, or the OPTIONAL `Mala-Pata-Phase` trailer) — never by a checkbox in the `.md`, an archive-report, nor memory. A `.md` says what was planned; git says what happened. **`ops` phases are the one exception**: Railway/Neon/GitHub/manual leave NO git artifact, so their `done` is **attested** in the `.md` with mandatory evidence (URL/id/health/date) and tagged `[attested]` — never confused with a git-proven `done`.
- **Zero cache, zero memory.** Every run re-derives everything from the `.md` + live git. Reporting a state without re-measuring it in this run is forbidden. NO engram.
- **Read-only.** Never commit, push, merge, destructive fetch nor write. Running this radar is always safe.
- **You take no attributions.** You only report which phase is in which state and what can start. You NEVER execute nor OFFER to execute a phase (triage, apply, PR, merge). **Emitting the next command as copy-paste TEXT (the stage-aware `triage` → lane → `-start` suggestion of Phase 3) is allowed and is NOT "offering to execute"** — you print it, you never run it and you never ask "¿arranco?". The human copies it if they want. Your output ENDS at the report + that text; closing with "¿arranco X?" is still forbidden.
- **Fixed format ALWAYS** — same order, same columns, same lexicon, on every run (mechanical memory for the human).

## Phase 0 — Load the roadmap (git, not memory)

1. Resolve the project root: `git -C <cwd> rev-parse --show-toplevel`.
2. Resolve the roadmap `.md`:
   - If the input is a path → `Read` directly.
   - If it is a **slug** → look for `mala-pata/roadmap/<slug>.md`.
   - If it is a **domain** (e.g. `caja`) → list `mala-pata/roadmap/*.md` and keep ONLY those whose frontmatter `domain:` matches (the owner field — do NOT guess by filename). Roadmaps of OTHER domains are excluded: **never mix domains in one run.** An old roadmap with no `domain:` → fall back to matching its slug/name and note it was matched heuristically.
   - If several candidates and none specified → list them and ask which one (one question, stop and wait).
   - If NO roadmap matches → do NOT dead-end: if the domain was built via SDD loops/changes (no roadmap), point to `/mala-pata-radar` (needs no roadmap `.md`); if the roadmap was archived, ask for its path. Do not invent phases.
3. Read the roadmap's frontmatter `domain:` (the owner — used for scoping above). Then from the `.md` extract per phase: **#**, **name**, **slug** (the stable change-name), **kind** (`code`/`ops`; default `code` if the column is absent in an old roadmap), **route**, **Depends on**, and — for `ops` phases — the declared **Status** / **Evidence** / **Verify**. From the DAG closing take the **topological order** and the **parallelizable** ones (`{..}`). If the roadmap is old and a phase has no `slug`, mark that phase `no-slug` (it cannot be matched deterministically — see Phase 2).

## Phase 1 — Freshness (live git, zero cache)

1. `git -C <repo> fetch --all --prune`.
2. Detect and **confirm** the integration branch (do not assume it: `main`/`development`/whichever the repo uses). Note its SHA for the banner.
3. If there is a `gh`/PR CLI, fetch the repo's list of open/merged PRs.

## Phase 2 — State per phase, live (code: from git reality · ops: by declared status)

Branch the derivation by the phase's **kind**:

**`code` phases — match from git reality (flexible, several signals; the trailer is OPTIONAL).** Branches get deleted in cleanup, so use whatever evidence git has. **Any ONE of these confirms, all equal weight** — do NOT treat the trailer as primary nor its absence as "weak":
- the `Mala-Pata-Phase: <slug>` trailer in an integration commit (`git -C <repo> log <integration> --grep '^Mala-Pata-Phase: <slug>$' -E` — cleanest when present, NOT required);
- a merged PR for the slug (`gh`);
- a branch `<type>/<slug>` merged into integration, or a commit whose subject/body mentions the slug that is an ancestor (`git log <integration> --grep <slug>` + `git merge-base --is-ancestor`);
- a migration / file the phase delivers, present in integration;
- a recorded `Evidence` sha/PR# that is an ancestor of integration.

Derive:
- **done** — ANY of the above confirms the phase landed in the freshly fetched integration branch. Evidence: the SHA / PR# / artifact, tagged `[git]`. A confirmed merge/ancestor is plain `[git]` — **never `[weak]`**; only a loose subject-only guess gets `[git, by subject]`.
- **in progress** — not in integration yet, but a live branch or an OPEN PR for the slug exists with its own commits.
- **pending** — **ONLY when there is NO evidence at all** (no trailer, no PR, no slug commit, no delivering artifact, no recorded sha).
- **`? unbound (confirm)`** — implementing commits CLEARLY exist but cannot be tied to the slug (work landed under another slug/PR): show those commits and ask the human — **NEVER a confident `pending` when work demonstrably exists.**
- **blocked** — `pending` with at least one `Depends on` not `done`.

**`ops` phases — NO git artifact; read the declared status.** Railway/Neon/GitHub/manual leave nothing in git, so **NEVER mark an `ops` phase `pending`/`blocked` for lacking a branch/trailer.** Read the `.md`'s declared fields:
- **done** — `Status: done` AND `Evidence` present (URL/id/health/date). Evidence: that string `[attested]`.
- **pending** — `Status: pending`, OR `done` WITHOUT evidence (attested-without-evidence is NOT done — same honesty rule as gaps). Show the phase's `Verify` so the human can confirm it.
- **blocked** — pending with at least one `Depends on` not `done`.

Derivation rules:
- **`code` done is NEVER a DoD checkbox** — it is confirmed by git reality (any signal above). The `.md` says what was planned; git says what landed. **`ops` done requires declared `Status: done` + evidence** (git cannot prove it); tag it `[attested]`, never `[git]`.
- **A dependent of a `done` phase is NOT blocked whether the parent is `[git]` or `[attested]`** — an ops `done` satisfies deps like a code `done` (kills the false `blocked` cascade).
- `no-slug` phase (old roadmap, no slug): try the other signals (branch/PR/artifact) first; if still unmatchable, mark `? (no slug)` and ask for the evidence by hand. Do not guess.
- A code phase whose branch is still alive AND already in integration is `done` anyway; note "merged, cleanup pending".

## Phase 3 — What can start now + parallel

- **Ready to start now** — phases in state `pending` (not `blocked`) whose dependencies are ALL `done`.
- **In parallel** — within the "ready now", group those the DAG marks as parallelizable with each other (from the roadmap's `Parallelizable: {..}` block) and that declare no conflict — that is the wave that can be launched together.
- **In process now** — those already running (so as not to relaunch them).
- **Next step per ready phase (stage-aware chain — emitted as TEXT in the Output).** The entry is NOT `-start`; follow the real pipeline `triage → lane (loop/organic/shot) → -start`, detecting the stage from the phase's Route + whether a kickoff file exists (read-only; triage leaves no artifact, so "triage done" is inferred from the roadmap having fixed the Route):
  - **Route undecided / `?`** (no lane fixed → triage not done) → `/mala-pata-triage <slug>` (decide the lane first).
  - **Route = shot** → `/mala-pata-shot <slug>` (direct, no kickoff).
  - **Route = organic | loop** → look for the kickoff `mala-pata/kickoffs/<slug>.md`:
    - kickoff MISSING → the lane creator `/mala-pata-organic <slug>` or `/mala-pata-loop <slug>` (writes the kickoff).
    - kickoff PRESENT → the runner `/mala-pata-organic-start <abs kickoff path>` or `/mala-pata-loop-start <abs kickoff path>`.
  - **Route = ops** → no command; verify manually per the phase's `Verify` (attested).

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

Then, for the "ready to start now" phases, the **Next step** block (plain text, copy-paste — the radar does NOT run it and does NOT offer to; it only shows the command the human may copy):
`Next step per ready phase (pipeline triage → lane → start):`
`  · phase <x> (<slug>, route <lane>): <stage-aware command — see Phase 3>`
`  · phase <y> (<slug>, route shot): /mala-pata-shot <slug>`
(one line per ready-now phase; `ops` phases show "verify manually per Verify", no command. In-progress phases with a live kickoff show the `-start` runner to resume.)

Then the closing lines (plain text):
`Legend: ✓ done = landed in integration — confirmed by git reality (merge / PR / slug commit / artifact / optional trailer) for code, or declared with evidence for ops · ◐ in progress = live branch/PR not merged · ○ pending = NO evidence at all (code) or Status pending (ops) · ? unbound = work exists but not tied to the slug (confirm) · ✗ blocked = pending with unfinished deps · [git] = proven in git · [attested] = ops, human-declared`
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
- **Match `code` phases from git reality** — any of: merged PR/branch, slug commit ancestor, delivering artifact, recorded sha, or the OPTIONAL `Mala-Pata-Phase` trailer; the trailer is NOT required and its absence never downgrades a confirmed match. **`ops` phases by declared `Status`/`Evidence`.** **Scope by the roadmap's `domain:`** — never mix domains in one run. `pending` only with zero evidence; work-exists-but-unbound → `? unbound`, never a false pending.
- **Fixed format** — same columns, same order, same lexicon, always.
- **No data**: if there is no roadmap `.md`, ask for it; if there is no git, do not run. Never invent the state of a phase.
