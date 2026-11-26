---
name: mala-pata-roadmap-radar
cognitive_tier: light
description: READ-ONLY status of a ROADMAP (not of loose SDDs — that is /mala-pata-radar). Takes a domain's roadmap .md (versioned in the repo, NOT memory), derives the state of EACH phase LIVE against git (done / in progress / pending / blocked), and shows a fixed table + what is ready to start now, which can go in parallel, and the stage-aware next command per ready phase (pipeline triage → lane → -start, as copy-paste text). It does NOT look at engram, does NOT orchestrate, does NOT execute, does NOT mutate anything. Fixed, immutable output format. Trigger — "status del roadmap", "cómo va el roadmap de <dominio>", "avance del roadmap <slug>", or the path/slug of a roadmap.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.15.3"
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

- **Git = truth, for `code` phases.** A `code` phase's "done" is confirmed ONLY against the freshly fetched integration branch (by ANY git evidence — a merge, a PR, a slug commit, a delivering artifact, or the OPTIONAL `Mala-Pata-Phase` trailer) — never by a checkbox in the `.md`, an archive-report, nor memory. A `.md` says what was planned; git says what happened. **`ops` phases are the one exception**: deploy/infra/manual steps leave NO git artifact, so their `done` is **attested** in the `.md` with mandatory evidence (URL/id/health/date) and tagged `[attested]` — never confused with a git-proven `done`.
- **Zero cache, zero memory.** Every run re-derives everything from the `.md` + live git. Reporting a state without re-measuring it in this run is forbidden. NO engram.
- **Read-only.** Never commit, push, merge, destructive fetch nor write. Running this radar is always safe.
- **You take no attributions.** You only report which phase is in which state and what can start. You NEVER execute nor OFFER to execute a phase (triage, apply, PR, merge). **Emitting the next command as copy-paste TEXT (the stage-aware `triage` → lane → `-start` suggestion of Phase 3) is allowed and is NOT "offering to execute"** — you print it, you never run it and you never ask "¿arranco?". The human copies it if they want. Your output ENDS at the report + that text; closing with "¿arranco X?" is still forbidden.
- **Fixed format ALWAYS** — same order, same columns, same lexicon, on every run (mechanical memory for the human).

## Phase 0 — Load the roadmap (git, not memory)

1. Resolve the project root: `git -C <cwd> rev-parse --show-toplevel`.
2. Resolve the roadmap `.md`:
   - If the input is a path → `Read` directly.
   - If it is a **slug** → look for `mala-pata/roadmap/<slug>.md`.
   - If it is a **domain** (e.g. `<domain>`) → list `mala-pata/roadmap/*.md` and keep ONLY those whose frontmatter `domain:` matches (the owner field — do NOT guess by filename). Roadmaps of OTHER domains are excluded: **never mix domains in one run.** An old roadmap with no `domain:` → fall back to matching its slug/name and note it was matched heuristically.
   - If several roadmaps of the SAME domain match (a domain, a list, or none specified) → do NOT ask: run the radar on EACH and emit one compact block per roadmap (see Output, multi-roadmap). If the candidates span SEVERAL domains → ask which domain (one question, stop and wait); never render roadmaps of different domains in one run — mixing domains loses the objective.
   - If NO roadmap matches → do NOT dead-end: if the domain was built via SDD loops/changes (no roadmap), point to `/mala-pata-radar` (needs no roadmap `.md`); if the roadmap was archived, ask for its path. Do not invent phases.
3. Read the roadmap's frontmatter `domain:` (the owner — used for scoping above). Then from the `.md` extract per phase: **#**, **name**, **slug** (the stable change-name), **kind** (`code`/`ops`/`spike`; default `code` if the column is absent in an old roadmap), **route**, **Depends on**, and — for `ops` phases — the declared **Status** / **Evidence** / **Verify**; for `spike` phases the **question** and the finding doc slug (`mala-pata/research/<slug>.md`). From the DAG closing take the **topological order** and the **parallelizable** ones (`{..}`). If the roadmap is old and a phase has no `slug`, mark that phase `no-slug` (it cannot be matched deterministically — see Phase 2).

> **Canonical phase kind — single source of truth.** Apply `_shared/mala-pata-phase-kind.md` verbatim: a `code` phase is proven by git, an `ops` phase by the human-maintained Verify/Status/Evidence (`[attested]`), a `spike` by its finding (`[finding]`). Never read an `ops`/`spike` phase as "no git → pending".

## Phase 1 — Freshness (live git, zero cache)

1. `git -C <repo> fetch --all --prune`.
2. Detect and **confirm** the integration branch (do not assume it: `main`/`development`/whichever the repo uses). Note its SHA (internal; not printed).
3. If there is a `gh`/PR CLI, fetch the repo's list of open/merged PRs.

## Phase 2 — State per phase, live (code: from git reality · ops: by declared status)

> **Canonical done-derivation — single source of truth.** Apply `_shared/mala-pata-git-truth.md` verbatim; it supersedes any restatement in this skill. Do not paraphrase or re-derive it.

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

**`spike` phases — state comes from the FINDING, NOT from a merged code slice.** A spike ships knowledge, not code, so NEVER derive it from a merged PR/branch/trailer. Read the finding doc (`mala-pata/research/<slug>.md`, frontmatter `kind: spike`, fixed `## Finding` section) in the repo:
- **done** — the finding doc exists with a filled `## Finding` (chosen approach · rejected options · residual unknowns · effect on decomposition) AND the spike has **re-entered the pipeline** (its finding was handed to `/mala-pata-triage`: evidenced by a dependent phase now having a fixed Route/kickoff, or the finding/roadmap recording the triage hand-off). Evidence: the finding path `[finding]`. A finding written but not yet re-entered is `◐ in progress` with note "finding written, awaiting triage re-entry" — dependents stay blocked.
- **in progress** — the spike was started (a research doc with `kind: spike` exists or a live research branch for the slug) but has no filled `## Finding` yet (or the finding is not yet re-entered, see above).
- **pending** — not started: no finding doc and no live research branch for the slug.
- **blocked** — pending with at least one `Depends on` not `done`.
- **A spike BLOCKS its dependents until it is `done`** (its finding may reshape the decomposition): any phase listing the spike in `Depends on` is `blocked` while the spike is `pending` or `in progress` — never `ready to start now`.

**`ops` phases — NO git artifact; read the declared status.** deploy/infra/manual steps leave nothing in git, so **NEVER mark an `ops` phase `pending`/`blocked` for lacking a branch/trailer.** Read the `.md`'s declared fields:
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
- **Roadmap completion (derived from git, NOT stored)** — the roadmap carries `created_at` (when it was planned); its FINISH time is **derived**: when ALL phases are `done`, it is the **latest git date among the done phases** (the last merge/commit that landed a phase). Roadmaps have no "close" step that writes it back; it is NOT printed (compact output) — derive it only if the human asks, never invent it.
- **Next step per ready phase (stage-aware chain — emitted as TEXT in the Output).** The entry is NOT `-start`; follow the real pipeline `triage → lane (loop/organic/shot) → -start`, detecting the stage from the phase's Route + whether a kickoff file exists (read-only; triage leaves no artifact, so "triage done" is inferred from the roadmap having fixed the Route):
  - **Route undecided / `?`** (no lane fixed → triage not done) → `/mala-pata-triage <slug>` (decide the lane first).
  - **Route = shot** → `/mala-pata-shot <slug>` (direct, no kickoff).
  - **Route = organic | loop** → look for the kickoff `mala-pata/kickoffs/<slug>.md`:
    - kickoff MISSING → the lane creator `/mala-pata-organic <slug>` or `/mala-pata-loop <slug>` (writes the kickoff).
    - kickoff PRESENT → the runner `/mala-pata-organic-start <abs kickoff path>` or `/mala-pata-loop-start <abs kickoff path>`.
  - **Route = spike** → `/mala-pata-research --spike "<question>"` (pending); in progress with a written finding → `/mala-pata-triage <finding path>` to re-enter the pipeline.
  - **Route = ops** → no command; verify manually per the phase's `Verify` (attested).

## Output — fixed format (ALWAYS identical, compact)

> **Canonical output contract — single source of truth.** Apply `_shared/mala-pata-output-contract.md` verbatim. **Reason INTERNALLY; emit ONLY the block below — NOTHING before it and NOTHING after it.** No generalities, ever: no banner (repo / source / integration / timeline), no legend, no Structure footer, no preamble, no recap. **No progress narration between tool calls either** ("Let me read…", "Now let me fetch…", "All N slugs are present…") — run the reads silently. Run the contract's pre-emit self-check before emitting.

The block, in order (nothing else):

1. **Heading** (one line): `**<roadmap-slug>**` — with several roadmaps, `#<i> — <roadmap-slug>` and the full block (heading + Bottom line + table + Next) repeats per roadmap, in file order, with nothing between blocks.
2. **Bottom line** (one line): `Bottom line: <non-zero counts only, in this order: ✓ <d> done · ◐ <p> in progress · ○ <q> pending · ✗ <b> blocked> (of <N>) · Ready now: <phase <x> (<slug or short name>), … | none>`
   - A zero count is omitted (`✓ 16 done (of 16)`, not `✓ 16 done · ◐ 0 in progress · …`). Pending `ops` phases carry `(ops)` after their count.
3. **The table** — a REAL pipe table, never inside a ``` fence, never as stacked per-phase blocks; one row per roadmap phase, in the `.md` order, none omitted:

| # | Phase | slug | Status | Evidence |
|---|---|---|---|---|
| 1 | <short name> | <slug> | ✓ done | <short-sha> |
| 2 | <short name> | <slug> | ◐ in progress | branch <type>/<slug> +<k> |
| 3 | <short name> | <slug> | ○ pending | — |
| 4 | <short name> | <slug> | ✓ done | <env / health / date> (attested) |
| 5 | <short name> | <slug> | ✗ blocked | waits for 2 |
| 6 | <short name> | <slug> | ✓ done | finding written |

4. **Next** (ONLY when `Ready now` is not `none`; one line per ready phase, copy-paste, the radar never runs it): `Next: phase <x> → <stage-aware command from Phase 3>` (`ops` → `Next: phase <x> → verify manually per Verify`).

Cell rules:
- **Phase** = a short name (2–4 words), never the full sentence from the roadmap.
- **Status** = curated glyph + English token: `✓ done` / `◐ in progress` / `○ pending` / `? unbound` / `✗ blocked`. No emoji, no colors.
- **Evidence** = the shortest concrete proof, never a bare "ok": `code` done → the landing commit/merge short SHA (9 chars) only — no "merge", no PR number, no `[git]` tag; in progress → `branch <type>/<slug> +<k>`; blocked → `waits for <#>`; `ops` → the declared evidence + `(attested)`; `spike` → `finding written` (or `finding written, awaiting triage`); pending → `—`.
- Route, Depends on, integration SHA, timeline and data sources are NOT shown — they are internal inputs to the state derivation, not output.
- Labels (`Bottom line`, `Ready now`, `Next`, column headers, status tokens) stay verbatim in English; only names and values follow the conversation language.

## Rules

- **ZERO cache, ZERO engram.** Re-derive everything from `.md` + git on every run.
- **READ-ONLY.** Never mutate anything; never execute nor offer to execute a phase.
- **Merge = git only.** A ticked DoD or an archive-report does NOT prove a merge.
- **Match `code` phases from git reality** — any of: merged PR/branch, slug commit ancestor, delivering artifact, recorded sha, or the OPTIONAL `Mala-Pata-Phase` trailer; the trailer is NOT required and its absence never downgrades a confirmed match. **`ops` phases by declared `Status`/`Evidence`.** **Scope by the roadmap's `domain:`** — never mix domains in one run. `pending` only with zero evidence; work-exists-but-unbound → `? unbound`, never a false pending.
- **Fixed compact format** — heading, Bottom line, 5-column table, optional Next lines; same columns, same order, same lexicon, always. Never generalities.
- **No data**: if there is no roadmap `.md`, ask for it; if there is no git, do not run. Never invent the state of a phase.
