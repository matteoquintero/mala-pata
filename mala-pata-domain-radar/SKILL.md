---
name: mala-pata-domain-radar
description: READ-ONLY high-level overview of a whole DOMAIN — one level ABOVE mala-pata-roadmap-radar. Given a domain (e.g. `caja`), it gathers EVERY mala-pata artifact that belongs to it — research, kickoffs (organics/loops), shots and roadmaps — by the `domain:` frontmatter field + the `Mala-Pata-Domain` commit trailer (so shots, which leave no .md, are found by their commit). It groups them: roadmaps (with a one-line rollup → run roadmap-radar for the phase detail) vs standalone items not under any roadmap. Coarse status (done / in progress / pending) from live git reality. It ALSO shows a completeness view per change — whether its QA walkthrough was run by hand (the `qa_done` human flag), whether it was seeded, whether its state diagram was drawn — plus the domain-level gaps rollup (Release GO/NO-GO) read from the gaps report. It does NOT replace roadmap-radar (phase detail) nor gaps (the full missing-work audit); it is the INDEX + completeness dashboard of a domain. It does NOT orchestrate, execute, or mutate anything. Trigger — "qué se hizo en el dominio <X>", "overview de <dominio>", "todo lo de caja", "domain radar <dominio>".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "2.2.0"
---

# /mala-pata-domain-radar — everything in a domain, from a high level

Input: **the one provided by the CLI** — a **domain** (e.g. `caja`, `clientes`, `facturacion`).

Your job: show, in a **fixed format**, EVERYTHING mala-pata did in that domain — research, kickoffs (organics/loops), shots and roadmaps — **grouped** by whether each belongs to a roadmap or is standalone, with a coarse live status. It is the **index/overview** of a domain; the detail of each roadmap is `mala-pata-roadmap-radar`'s job.

> **Three sibling radars, three altitudes.** `mala-pata-radar` = loose SDDs from memory. `mala-pata-roadmap-radar` = the phases of ONE roadmap, in detail. **This one = a whole DOMAIN, from above** — all its artifacts and roadmaps at a glance. For a roadmap's phase-by-phase detail, it points you to roadmap-radar; it does NOT duplicate it.
> **NOT gaps.** `mala-pata-gaps` says what is MISSING to cover the objective. This says what EXISTS and how it is going. They complement each other.

## Requirements (orchestrate, do not reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP): `git` — the live source for status + the `Mala-Pata-Domain` commit trailer. Always present.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded): `gh` (or the project's PR CLI) — PR status. Fallback: branches/merges only.
- **Explicit — does NOT use engram.** The artifacts (`mala-pata/{research,kickoffs,roadmap,walkthroughs,diagrams,seeds,gaps,runbooks,playbooks}/*.md`, in the repo) + git are the only sources.

Check: `command -v <tool>`. If a mandatory tool is missing, do not continue.

## Hard principles (non-negotiable)

- **Git = truth for status.** Coarse `done`/`in progress`/`pending` is derived from live git (same OPEN matching as roadmap-radar — several equal-weight signals; the `Mala-Pata-Phase` trailer is optional, not required). Never from a `.md` checkbox.
- **Scope strictly by `domain`.** Only artifacts whose `domain:` (or `Mala-Pata-Domain` trailer) matches the requested domain. **Never mix domains in one run.** (`domain` = the FEATURE it belongs to, else the functional AREA it touches, else `main` — the catch-all bucket for area-less direct-to-main chores.)
- **Read-only.** Never commit, push, merge, nor execute/offer to execute a lane or another radar. Your output ENDS at the overview.
- **This is the overview, not the detail.** For a roadmap's phases you emit a one-line rollup + "run roadmap-radar"; you do NOT expand the phase table here.

## Phase 0 — Resolve the domain + project

1. Project root: `git -C <cwd> rev-parse --show-toplevel`.
2. The input is a **domain** keyword. If it is missing or ambiguous → ask once (which domain), stop and wait. Do not guess.

## Phase 1 — Gather every artifact of the domain (two sources)

**(a) Artifacts with a `.md`** (`domain:` frontmatter field). Two groups:

*Delivery artifacts* (what was planned/built — these are the inventory rows):
- `mala-pata/roadmap/*.md` → roadmaps where `domain: <X>`.
- `mala-pata/kickoffs/*.md` → organic/loop kickoffs where `domain: <X>` (each carries `roadmap: <slug | none>`).
- `mala-pata/research/*.md` → research docs where `domain: <X>` (with its `verdict:`).

*Completeness artifacts* (did the surrounding work get done — these fill the completeness view, Phase 4):
- `mala-pata/walkthroughs/*-qa.md` → QA walkthroughs where `domain: <X>` (each carries `change:`, `roadmap:`, and the **`qa_done: pending | done`** human flag).
- `mala-pata/diagrams/*-states.md` → state-diagram pointers where `domain: <X>` (each carries `change:`/`feature:`).
- `mala-pata/seeds/*.md` → seed records where `domain: <X>` (each carries `change:`).
- `mala-pata/gaps/<X>.md` → the domain's gaps report (ONE per domain), reading its frontmatter rollup `release:` / `open:` / `deferred:` / `closed:`.

*Operational assets* (the domain's runbooks and playbooks — standing procedures/scenarios, not tied to one change):
- `mala-pata/runbooks/*.md` → runbooks where `domain: <X>` (each carries `kind:`, `trigger:`, `risk:`, `reversible:`, `last_reviewed:`). Deterministic single-task procedures (`/mala-pata-runbook`).
- `mala-pata/playbooks/*.md` → playbooks where `domain: <X>` (each carries `kind:`, `scenario:`, `signals:`, `severity:`, `runbooks:`, `last_reviewed:`). Scenario-level decision trees (`/mala-pata-playbook`) that orchestrate runbooks.
- Both are surfaced in their own tables (Output), not as inventory or completeness rows.

**(b) Work with NO `.md`** (shots, and anything older) — from git:
- `git -C <repo> log <integration> --grep '^Mala-Pata-Domain: <X>$' -E` → commits tagged with this domain. These catch **shots** (the minimum lane leaves no kickoff — only a commit) and any change whose artifact is gone. Read their trailers: **`Mala-Pata-Lane`** → the TYPE (`shot`/`organic`/`loop`) — THIS is how a shot, which has no `.md`, is identified as a shot; `Mala-Pata-Phase` → the slug; `Mala-Pata-Roadmap` → whether it belongs to a roadmap.

Deduplicate: a change with both a kickoff `.md` and tagged commits is ONE item (the `.md` is the primary record).

## Phase 2 — Relate (roadmap vs standalone)

For each item, resolve its link to a roadmap:
- A kickoff/research with `roadmap: <slug>` (or a commit with `Mala-Pata-Roadmap: <slug>`) → belongs to that roadmap.
- `roadmap: none` (or no link) → **standalone** (a loop/organic/shot/research done on its own, not under any roadmap).

Group: one bucket per roadmap of the domain (+ its linked items as a rollup), and one bucket for standalone items.

## Phase 3 — Coarse status (live git, OPEN matching)

Same OPEN logic as `mala-pata-roadmap-radar` Phase 2 (reuse it; do NOT reinvent): a thing is `done` when ANY git signal confirms it landed in the freshly fetched integration branch (merged PR/branch, slug commit ancestor, delivering artifact, recorded sha, or the optional trailer). `in progress` = live branch/PR not merged. `pending` = no evidence.
- **Per roadmap**: a ONE-LINE rollup — `<done>/<total>` phases — plus the pointer to roadmap-radar for the detail. Do NOT expand phases here.
- **Per standalone item**: its own coarse status (research shows its `verdict` instead).

## Phase 4 — Completeness of the domain (did the surrounding work get done)

Beyond "was it built", show whether each change got its QA, diagram and seed — and the domain-level gaps rollup. This is the "¿se completó todo?" view the inventory alone does not give.

- **Per change** (key by `change:` across the completeness artifacts of Phase 1a, grouped with their delivery item when one exists): resolve three signals from the artifacts, NEVER invented —
  - **Walkthrough / QA done**: `✓ done` if a `*-qa.md` with `qa_done: done` exists; `○ pending` if the QA exists but `qa_done: pending` (the walkthrough was written but **the human has not tested it by hand yet** — this is the "aviso"); `— none` if no QA for that change.
  - **Seed**: `✓ seeded` if a seed record exists for the change; `— none` otherwise.
  - **States diagram**: `✓ drawn` if a diagram pointer exists; `— none` otherwise.
- **Domain-level gaps** (ONE line, from `mala-pata/gaps/<X>.md` frontmatter): `Release: <GO | NO-GO | GO-with-conditions> · <open> open · <deferred> deferred`. If there is no gaps report → `Gaps: not audited — run /mala-pata-gaps <X>`.
- Forward-only: a change whose artifacts predate these fields simply shows `— none` in its cells; never infer "done" from the absence of a record.

## Output — fixed format (ALWAYS identical)

Reason first; the LAST thing you emit is EXACTLY this shape — a BLUF line then ONE real Markdown table (NEVER fenced, never prose, one line per cell).

Banner (plain text):
`Domain: <domain>  ·  repo: <name>  ·  integration: <branch>@<short-sha>  ·  <date-time>`

BLUF (plain text, immediately below):
`Bottom line: <r> roadmaps · <s> standalone · ✓ <d> done · ◐ <p> in progress · ○ <q> pending · QA ✓ <w>/<W> done · <rb> runbooks · <pb> playbooks · Release: <GO | NO-GO | n/a>`

Then the **inventory** table (one row per item — roadmaps and standalone — never expand roadmap phases here):

| Type | Name / slug | Under roadmap | Status | Detail |
|---|---|---|---|---|
| roadmap | <slug> | — | ✓ complete (3/3) | run `/mala-pata-roadmap-radar <slug>` |
| roadmap | <slug> | — | ◐ 2/6 | run `/mala-pata-roadmap-radar <slug>` |
| loop | <slug> | none (standalone) | ✓ done | merge <sha> [git] |
| organic | <slug> | <roadmap-slug> | ◐ in progress | branch +<k> |
| shot | <slug> | none | ✓ done | commit <sha> [git] |
| research | <slug> | none | PROCEED | `mala-pata/research/<slug>.md` |

Then a second BLUF line + the **completeness** table (one row per change — did its QA, seed and diagram get done; `qa_done` is the human "did you actually test it" aviso):

`Completeness: <c> changes · QA ✓ <w> done · ○ <wp> pending · seed ✓ <se> · diagram ✓ <di>`

| Change | Walkthrough / QA done | Seed | States diagram |
|---|---|---|---|
| <change> | ✓ done | ✓ seeded | ✓ drawn |
| <change> | ○ pending (not tested by hand) | — none | ✓ drawn |
| <change> | — none | — none | — none |

Then the domain-level gaps line (plain text, from `mala-pata/gaps/<X>.md` frontmatter):
`Gaps: Release <GO | NO-GO | GO-with-conditions> · <open> open · <deferred> deferred → mala-pata/gaps/<X>.md`  — or, if absent: `Gaps: not audited — run /mala-pata-gaps <X>`.

Then the **Runbooks** table (one row per runbook of the domain; omit the whole table if there are none):

| Runbook | Kind | Trigger | Risk | Reversible | Last reviewed |
|---|---|---|---|---|---|
| <slug> | deploy | "release a main" | high | no | 2026-10-20 |
| <slug> | recovery | <trigger> | medium | yes | <date> |

- Run one with `/mala-pata-runbook-start <path>` (as text — you do NOT run it). A runbook with a stale `last_reviewed` (older than the domain's recent activity) is worth flagging in one line, not hiding.

Then the **Playbooks** table (one row per playbook of the domain; omit the whole table if there are none):

| Playbook | Kind | Scenario | Branches | Orchestrates | Last reviewed |
|---|---|---|---|---|---|
| <slug> | diagnostic | <one-line scenario> | <n> (+fallback) | <runbook slugs> | <date> |
| <slug> | incident | <one-line scenario> | <n> | <runbook slugs> | <date> |

- Run one with `/mala-pata-playbook-start <path>` (as text — you do NOT run it). Same stale-`last_reviewed` flag applies.

Then the closing lines (plain text):
`Not tracked here: shots with no Mala-Pata-Domain trailer and no commit match (if any) — say so, do not invent.`
`Structure: information radiator (Cockburn) + workflow-state lexicon. Domain-wide roll-up (roadmap vs standalone) + delegate-detail-to-roadmap-radar = house method.`

- **One row per item**, grouped roadmaps first then standalone; each ordered the same way every run.
- **Status glyph + word** (`✓ done · ◐ in progress · ○ pending`); for a roadmap use `✓ complete (n/N)` or `◐ <n>/<N>`. Research shows its verdict (`PROCEED`/`SHARPEN`/`RECONSIDER`), not a done/pending.
- **Concrete evidence** in Detail (merge SHA / commit / the roadmap-radar command / the research path) — never a bare "ok".
- **Emit every structural label verbatim in English** — headers, field labels, table/column headers and enum tokens stay English even when the conversation is in the user's language; only the values are localized.

## Rules

- **ZERO engram.** Re-derive from the artifacts (`.md`) + git on every run.
- **READ-ONLY.** Never mutate; never execute nor offer to execute a lane or another radar. The only command you suggest is `/mala-pata-roadmap-radar <slug>` for a roadmap's detail — as text, you do not run it.
- **Scope strictly by `domain`** — never mix domains.
- **Overview, not detail** — a roadmap is ONE row with a rollup; never expand its phases (that is roadmap-radar).
- **No data**: if there are no artifacts and no tagged commits for the domain, say so and stop. Never invent items.

## Relation to the family

- **Above** `/mala-pata-roadmap-radar` (which details ONE roadmap) and `/mala-pata-radar` (loose SDDs).
- **Complements** `/mala-pata-gaps` (what is missing) — this shows what exists AND reads gaps' domain-level rollup for the Release line.
- Reads the `domain:`/`roadmap:` frontmatter that `/mala-pata-roadmap`, `/mala-pata-research`, `/mala-pata-organic` and `/mala-pata-loop` write; the completeness frontmatter that `/mala-pata-walkthrough` (`qa_done`), `/mala-pata-states` and `/mala-pata-seed` write; the rollup frontmatter `/mala-pata-gaps` writes; the runbook frontmatter `/mala-pata-runbook` writes (run with `/mala-pata-runbook-start`); the playbook frontmatter `/mala-pata-playbook` writes (run with `/mala-pata-playbook-start`); and the `Mala-Pata-Domain` commit trailer the lanes stamp.
- **Forward-only** (except the shared OPEN git matching, which it reuses from roadmap-radar): artifacts predating the completeness fields show `— none`; only `/mala-pata-roadmap-radar` is required to keep working on legacy.
