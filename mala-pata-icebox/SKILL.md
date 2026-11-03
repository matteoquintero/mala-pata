---
name: mala-pata-icebox
description: FREEZE a desired outcome for LATER — captures a DoD (a "cube") into a deferred backlog (an "icebox") WITHOUT solving it now. An icebox is a flat, append-only list of INDEPENDENT cubes you accumulate over time (cheap, no research, no routing); you DEFROST it later (`/mala-pata-icebox-defrost`) to run research + triage over the whole thing and route each cube into shot/organic/loop/roadmap. Different from a roadmap (ONE objective decomposed into a dependent DAG right now) — the icebox is a bottom-up POOL of independent asks for later. It does NOT research, does NOT route, does NOT size authoritatively, does NOT read code, does NOT execute; it only appends one or many cubes to `mala-pata/icebox/<slug>.md` (write-only, no commit). Supports bulk — freeze a whole findings list in one pass. Trigger — "agregá un cube al icebox <slug>", "congelá esto para después", "metelo al icebox", "guardá esta idea para después", "congelá estos hallazgos", "freeze this".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "0.2.2"
---

# /mala-pata-icebox — freeze a cube into a deferred backlog

Input: **the one delivered by the CLI** — a **DoD / desired outcome** to capture, plus **which icebox** (a slug). If the icebox does not exist yet, this also creates it.

Your job: **freeze** the outcome — append a one-line **cube** to the icebox file — and nothing else. You do NOT solve it, research it, route it, size it for real, read the code, or run anything. The whole point is **capture now, route later**: the investment (research + triage) is deferred to `/mala-pata-icebox-defrost`.

> **An icebox is a POOL, not a plan.** It is a flat list of INDEPENDENT cubes accumulated over time (bottom-up). It is NOT a roadmap — a roadmap is ONE objective decomposed into a dependent DAG, right now, top-down. If what you have is a single objective that needs decomposition with dependencies, that is `/mala-pata-roadmap`, not an icebox.
> **Freeze is cheap — a cube is one line.** If capturing a cube costs more than a line, the gracia breaks. No research, no code reading, no interview: just the concrete outcome. The size-hint is OPTIONAL and is only a hint — `defrost` + `triage` decide the real route.
> **Deferred by design.** A cube is NOT solved here. Leaving it unsolved is the feature, not an omission.

## Requirements (orchestrate, do not reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP): `git` — to resolve the repo root where the icebox file lives. Always present.
- **Recommended** (with fallback — warn in one line and continue degraded):
  - `engram` — discoverability pointer (`icebox/<slug>`). Fallback: the file is the source of truth.

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP). If a mandatory tool is missing, do not continue.

## Phase 0 — Authorize (read-only on your real projects)

Freezing a cube writes ONLY the icebox file (`mala-pata/icebox/<slug>.md`). It writes no application code, runs nothing, touches no DB, executes no lane. It is always safe. If the request is actually "do X now" (not "save X for later"), this is the WRONG skill — bounce to `/mala-pata-triage` (to route it now) and do not freeze it.

## Phase 1 — Resolve the icebox (create or append)

1. Resolve the repo root: `git -C <cwd> rev-parse --show-toplevel`.
2. Resolve the icebox file `mala-pata/icebox/<slug>.md`:
   - **Slug given and the file exists** → **append mode**.
   - **Slug given, file absent** → **create mode** (a new icebox).
   - **No slug** → ask which icebox (one question: an existing slug, or a name to create). Stop and wait. Do not guess.
3. **`domain` (create mode only) — MANDATORY, never blank.** An icebox belongs to a domain like every other mala-pata artifact (so `mala-pata-domain-radar` can group it). Infer it from what the icebox is FOR, per the canonical rule below. (Append mode reuses the file's existing `domain`.)

   > **Canonical `domain` rule — single source of truth.** Apply `_shared/mala-pata-domain-rule.md` verbatim; it supersedes any restatement in this skill. Do not paraphrase or re-derive it.

## Phase 2 — Capture the cube(s) (one line each, cheap)

0. **One or many (bulk).** The input may be a single outcome OR a LIST (e.g. an audit / findings dump where each item has its own tag). Freeze each item as its own cube in a single pass — same one-line rule per cube, sequential ids, same idempotency check. Bulk stays cheap: still NO research and NO per-cube analysis (classifying research-vs-triage is `/mala-pata-icebox-defrost`'s job, not freeze's). When the source items carry their own tags (e.g. `<tag><n>`), keep the tag as a prefix in the cube's DoD so the full detail stays traceable.
1. **The cube is a concrete, observable outcome in ONE line** — the WHAT, not the how. "Mejorar X" with no concrete target is NOT a cube: if the input is that vague, ask for the concrete outcome in one line (same spirit as the triage `What` gate) — but do NOT over-interview; freezing is meant to take seconds.
2. **size-hint — OPTIONAL, a hint only.** If the human offers a rough size, record it (`shot` | `organic` | `loop` | `roadmap`); otherwise `?`. **Do NOT compute it authoritatively and do NOT research to decide it** — `defrost` runs triage for the real routing. A wrong hint costs nothing; it is overwritten at defrost.
3. **Assign the next cube id** (`c<N>`, continuing the file's existing ids). Status is always `frozen` when you write it — only `defrost`/`radar` later move a cube to `routed`/`done`.
4. **Idempotency.** If a near-identical cube already exists in this icebox, warn in one line and **do not duplicate it**. The icebox is a pool, not a log.

## Phase 3 — Write (write-only — do NOT commit/push)

1. **Create mode**: `mkdir -p <repo>/mala-pata/icebox`, then write the file:

```markdown
---
icebox_slug: <slug>
project: <project>
domain: <per _shared/mala-pata-domain-rule.md — NEVER blank; ANY doubt → ASK the human>
created_at: <ISO 8601>
---
# Icebox: <name>

> Deferred backlog — freeze cubes here; defrost later to route them. Flat list of INDEPENDENT cubes (not a roadmap).

## Cubes
- [ ] c1 · <DoD: concrete observable outcome, one line> · size-hint: <?|shot|organic|loop|roadmap> · status: frozen
```

   (The frontmatter keys and the `## Cubes` heading are fixed identifiers read by `/mala-pata-icebox-defrost` and `/mala-pata-icebox-radar`; keep them verbatim. Only the `<...>` values are filled.)

2. **Append mode**: add the new cube as one line under `## Cubes`, with the next `c<N>` id.
3. **Timestamps.** Fill every generated timestamp from the machine's local clock — run `date '+%Y-%m-%dT%H:%M:%S%z'` and use its exact output (local time with UTC offset, e.g. `2026-11-01T17:25:40-0500`); never invent the time and never default to UTC.
4. **Write only — do NOT commit/push.** Write the file; the skill does NOT create a git commit (auto-committing diverged local `main` from the remote in sibling skills). Tell the human the path + that the icebox belongs on a durable branch (`main`/`development` or the feature it serves), so they commit it in their normal flow.
5. **Lightweight pointer in engram**: `mem_save` with `topic_key: "icebox/<slug>"`, single-line content: `Icebox in file: <absolute path>`. Do not duplicate the cubes into engram — the file is the source. If engram is unavailable, the file is still the source; warn in one line.

## Phase 4 — Close (MANDATORY: summary)

Emit exactly this, from what you actually did (no invention):

- Title: `**Cube frozen — <icebox-slug>**` (or `**Icebox created — <icebox-slug>**` on create mode).
- BLUF: `Icebox <slug> · domain <domain> · <N> cubes · <created | appended>`.
- **The cube(s) you added.** One cube → its `c<N>` line. **Two or more (bulk) → a REAL Markdown table** (never fenced, one line per cell):

  | # | Cube (DoD) | size-hint | Status |
  |---|---|---|---|
  | c1 | <one line> | organic | frozen |
  | c2 | <one line> | ? | frozen |
- **Icebox:** `mala-pata/icebox/<slug>.md` (repo-relative) — write-only, commit it on `<durable branch>`.
- **Next step** — keep freezing, or defrost when ready:

  ```
  /mala-pata-icebox-defrost <slug>
  ```

- **Structure:** deferred backlog (capture-now / route-later) + BLUF close. Icebox / cube / freeze / defrost = house method.

Emit the structural labels above (Cube frozen, Icebox created, BLUF, Icebox, Next step, Structure) **verbatim in English**; only the values and surrounding prose follow the conversation language.

This block is the only way to close on the happy path. **Only exceptions**: Phase 0 wrong-skill bounce; the single resolve question (Phase 1) or the single concrete-outcome question (Phase 2) when the input is missing/vague.

## What it does NOT do (invariants)

- Does NOT research, route, size authoritatively, read code, or execute — all of that is deferred to `/mala-pata-icebox-defrost`.
- Does NOT solve the cube now — deferral is the point.
- Does NOT decompose like a roadmap — the icebox is a flat pool of independent cubes, not a dependent DAG.
- Does NOT commit/push — write-only; the human commits it in their flow.
- Does NOT invent `domain` or a size — it asks on doubt, and the size stays a hint.

## Relation to the family

- **The capture end** of the icebox family: `mala-pata-icebox` (freeze, this) → `mala-pata-icebox-defrost` (research + triage in parallel over the whole icebox → batch routing recommendation) → `/mala-pata-triage` → `shot`/`organic`/`loop`/`roadmap`. `mala-pata-icebox-radar` reports how many cubes are done against git.
- **Different from** `/mala-pata-research` (sharpens ONE idea now) and `/mala-pata-roadmap` (decomposes ONE objective into a dependent DAG now). The icebox is a bottom-up pool of independent asks for later.
- It is a backlog-authoring skill, orthogonal to the lanes — it is NOT a route and decides no lane (that is triage, at defrost time).
