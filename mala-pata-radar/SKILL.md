---
name: mala-pata-radar
description: >
  READ-ONLY SDD radar — discovers AND diagnoses in a single run (absorbs the
  former control tower). Phase A: discovers the active SDDs in memory
  (engram, best-effort ≤20/search) or takes the explicit list you pass it.
  Phase B: confirms each one against LIVE git (zero cache) — cycle phase,
  actual merge against integration, dependencies, stale branch, human gate,
  parked, cleanup pending. Scope: by default ONLY the cwd's project;
  accepts a project path or `global` (all projects, grouped).
  It does NOT orchestrate, does NOT execute phases, does NOT mutate anything.
  Trigger: "radar de SDD", "SDD activos", "torre de control", "cómo van estos
  SDD", "estado de estos SDD", or a list of change-names to review.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "4.6.0"
---

# /mala-pata-radar — SDD radar (discover + diagnose, read-only)

> Scope: radar tracks `sdd/…` changes only. ODD changes (`odd/…`) are tracked via the feature-doc (`mala-pata/odd/<change>.md`), not radar.

## Requirements (orchestrate, don't reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP and ask to install it, do not start):
  - `git` — source of truth for the diagnosis. Install: always present; no installation required.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded):
  - `engram` — persistent memory and continuity pointer. Fallback: explicit list of change-names. Install: ships with gentle-ai (`brew install gentleman-programming/tap/gentle-ai`).

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP, e.g. serena). If a mandatory one is missing, do not continue.

## Purpose

Global and **100% reliable** visibility of SDD progress, in ONE run:
discovers what is active (memory) and confirms it against reality (git). Before
there were two skills ("radar proposes, tower confirms") — now it is a single pipeline:
Phase A proposes, Phase B confirms, and the output is a single diagnosed table.

Trust comes from **not trusting any cached state**: each run
re-derives everything from the live sources (memory + VCS). It is purely informative:
it tells you **what is missing and where**, and that is where it ends — it does NOT execute nor offer to execute anything
(each phase is worked in its own session).

**Agnostic**: only VCS (git) + the available persistent memory. It does not know about
nor query ticket managers or external services.

## Input

Two independent dimensions in the CLI input: **scope** (which project/s) and
**list** (which SDDs).

**Scope — which project the SDDs are looked at from:**
- **Default (no scope parameter)**: ONLY the project you are standing in
  (the cwd's). Phase A filters the memory hits by that cwd's `project`;
  Phase B operates on that repo. NEVER mix SDDs from other projects in the default.
- **`<absolute path>`**: operates on THAT project — Phase A filters the hits by the
  project of that path (memory results carry their `project`; discard
  those that do not match), Phase B runs git in that repo.
- **`global`**: all projects — Phase A searches with no project filter and groups
  the table by project; Phase B runs git for each project whose repo is
  resolvable (from the `project_path` the memory returns, or from the path of the kickoff
  file). If a repo cannot be resolved, its git cells go with `?` and it is
  explained in the evidence.

**List — which SDDs (optional, combinable with the scope):**
- **Explicit list**: change-names (`sentencias-mora`), memory identifiers
  (`#7280`, `sdd/<change>/tasks`), `all <prefix>-*`, or a mix →
  **skip Phase A** and go straight to Phase B with that list.
- **Empty or only a prefix/domain** → run Phase A to build the list,
  within the chosen scope.

## Process

### Phase A — Discover active candidates (memory, only if there is no explicit list)

Follow [references/discovery.md](references/discovery.md) (engram-only, exact commands
with `limit=20` and `match_mode="any"`): anchor searches by phases of
activity + loop-until-dry; full cycle per candidate (**FORBIDDEN** to
classify with a single hit); filter out cancelled and archived (count them separately).
**Respect the scope from Input**: unless `global`, discard every hit whose
`project` is not the target project's — memory results carry
their project; an SDD from another project in the table is a scope error.
The filtered list of active ones goes to Phase B. **Declared best-effort**: engram
caps at 20 results per search, a 100% inventory does not exist — the disclaimer ALWAYS goes
in the banner.

### Phase B — Confirm and diagnose with git (ALWAYS, zero cache)

Execute in order, without skipping steps (detail in
[references/state-derivation.md](references/state-derivation.md)):

1. **Freshness first.** The repo(s) are defined by the **scope from Input**
   (default = the cwd's; `<path>` = that one; `global` = one per resolvable project).
   `git fetch --all --prune` in each. Detect the integration branch
   (confirm it, do not assume it). Note the SHAs for the banner.
2. **Resolve each SDD against memory by EXACT identifier** (change-name
   or topic_key), never by fuzzy semantics. Collect which artifacts exist and their
   latest revision. (The kickoff is a file: the engram observation is a
   pointer `Kickoff in file: <path>` — follow it with `Read`.)
3. **Derive phase + status light LIVE** with the state machine of
   `state-derivation.md`. Hard rule: **merge is NEVER believed from an
   archive-report or apply-progress** — it is confirmed against the freshly fetched
   integration branch.
4. **Detect**: dependencies among the SDDs in the list, stale branch,
   parked/blocked, no instruction, pending human gate, and cleanup pending
   (merged but worktree/branch alive — including the `paused-at-preview` ones, which
   record the path of their live worktree in the `state`).
   **Out-of-sync worktree name**: run `git worktree list` and flag any worktree whose path does not resolve on disk, or whose registered id != the folder (happens via `mv` without `git worktree move`) — suggest `git worktree repair <path>` (renamed) or `git worktree prune` (deleted). Without that, git errors name phantom folders you cannot find on disk.

## Output

Exactly the format of [references/table-format.md](references/table-format.md):
freshness banner (+ the best-effort disclaimer if Phase A ran) + 7-column
table + status-light legend + evidence block (for each SDD, the
memory identifier + SHA/branch that back the state). Same format,
same order, same lexicon, **always** — mechanical memory for the human. If
Phase A saw archived/cancelled ones, close with ONE count line "others seen",
marked **non-exhaustive**.

## Rules

- **ZERO cache.** Reporting a state without re-deriving it in this run
  from memory + VCS is forbidden.
- **READ-ONLY.** Never commit, push, merge, destructive fetch, nor memory writes.
  Running the radar is always safe.
- **YOU DO NOT TAKE OWNERSHIP.** You only report **what is missing and where**. NEVER execute
  nor OFFER to execute a phase (apply, verify, archive, PR, merge, cleanup) —
  each one is worked in its **own separate session**. Your output ENDS at the
  report. Closing with "shall I start X?", "shall I run it?", "shall I merge?" or similar is forbidden.
- **Merge = git only.** An archive-report says "the cycle closed", NOT "it is
  merged".
- **Not a single hit**: for each SDD fetch its ENTIRE cycle; for the universe,
  loop-until-dry with `limit=20`, `match_mode="any"`.
- **Exact identifier** when grouping/resolving; never phrases nor fuzzy semantics.
- **Declared best-effort** when Phase A runs: the banner ALWAYS says that
  discovery is not 100% (engram limit). The explicit list does not have that
  limit.
- **Runtime-agnostic**: "the available memory", "the available question
  tool"; paths relative to the skill; no `$ARGUMENTS`; no proprietary tools.
- **No data**: if no memory is available, ask the human for the list or the artifacts;
  never guess the phase nor invent SDDs.

## Resources

- [references/discovery.md](references/discovery.md) — Phase A: engram-only discovery.
- [references/state-derivation.md](references/state-derivation.md) — Phase B: live phase/state derivation + detections.
- [references/table-format.md](references/table-format.md) — the fixed output format (immutable contract).
