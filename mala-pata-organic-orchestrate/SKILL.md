---
name: mala-pata-organic-orchestrate
description: READ-ONLY planner for a batch of ORGANIC (ODD) kickoffs — analyzes several kickoffs with `route: organic` and returns a wave plan (dependencies, parallelism, file/migration conflicts, recommended splits, deferrals) + the single copy-paste command that launches wave 1. It does NOT create worktrees, does NOT advance branches, does NOT launch sessions, does NOT merge — /mala-pata-organic-orchestrate-start does that. Organic kickoffs only: loops always need a human and are never batch-orchestrated. Trigger — "planificá estos kickoffs organic en olas", "qué cambios organic puedo correr en paralelo", "orquestá este lote de ODD", "armá el plan de olas de los organic".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.0.0"
---

# /mala-pata-organic-orchestrate — Plan a BATCH of organic kickoffs (READ-ONLY)

You are the batch **planner** for the ODD lane. You are handed **several organic kickoffs** and you return a **wave plan**: in which **waves** to run them, what to **parallelize** and what **NOT**, where there is a **file/migration conflict**, which kickoff **is worth splitting**, which to **defer**, and the command ready to paste.

> **This skill executes NOTHING**: it does not create worktrees, does not advance branches, does not write launch configs, does not open sessions, does not merge. It is ONLY analysis + plan. To **launch and drive** the batch use `/mala-pata-organic-orchestrate-start` (planner vs executor).

You do NOT run the ODD cycles here (each one is `/mala-pata-organic-start <kickoff>` in its own tab, launched by the sibling skill). This command **plans the batch**.

> **Organic, not loop.** Loops (SDD) always need a human at their gates and are never batch-orchestrated. This skill plans ONLY kickoffs whose frontmatter says `route: organic`. A kickoff with any other route (loop, or no route) is NOT yours: list it as excluded and tell the human to run it by hand with `/mala-pata-loop-start`.

## Requirements (orchestrate, do not reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP and ask to install it, do not start):
  - `git` — reading branches and detecting conflicts. Install: always present; requires no installation.
  - `gentle-ai` — ODD engine. Install: `brew install gentleman-programming/tap/gentle-ai`.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded):
  - `engram` — persistent memory and continuity pointer. Fallback: continue with the explicit list of kickoffs. Install: comes with gentle-ai (`brew install gentleman-programming/tap/gentle-ai`).

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP, e.g. serena). If a mandatory tool is missing, do not continue.

## Step 1 — Load the kickoffs

Resolve the project root: `git -C <cwd> rev-parse --show-toplevel`. Input (accepts any of these forms):
- **Explicit list**: absolute paths to organic kickoff `.md` files, or bare change-names (slug-first: a change-name resolves to `<repo-root>/mala-pata/kickoffs/<change-name>.md`).
- **Auto-discover** (no list passed): scan ONLY `<repo-root>/mala-pata/kickoffs/*.md` — where `/mala-pata-organic` writes the kickoff (in-repo, versioned) — and keep ONLY files whose YAML frontmatter has `route: organic`. Loop kickoffs live in the same folder — the `route: organic` filter is what separates them; never guess by filename. No other location is scanned.

For each one: `Read` in full. If it is not found → warn and continue with the rest (do not invent context). If `route` is not `organic` → exclude it and say so in the warnings table.

## Step 2 — Extract the metadata that governs orchestration

From each kickoff take:
- `change_name`, `project`, `base`, `branch`, `worktree`, `domain`, `roadmap`, `tdd_mode`.
- `depends_on` (the dependency list of change-names; blocking by default) and `parallelizable_with` — if the kickoff carries them. If it does not, say `none declared` and do NOT invent a dependency; flag it for the human in the warnings table when the body hints at one (a Decision or Risk that names another change).
- **Affected areas/files**: the `Where (optional hint)` plus the What/Done body — keyed to detect clashes. An empty Where is normal (organic discovers it in Explore): mark `where unknown` and treat it as a possible clash with anything in the same domain.
- **Migration?** = a provisional migration number is named (`migrations_reserved` or the body). Provisional, never a reservation.
- **Weight**: organic has no profile — infer small / substantial from What + Done (2+ meaningful steps = substantial, which will create a feature-doc).

## Step 3 — Analyze (plan rules)

1. **Dependency graph** (`depends_on`) → topological order. A dependent is READY only when each dependency is MERGED into the integration branch (not merely PR-ready) — that is the rule the executor applies live in git.
2. **Conflict by shared file**: intersect the affected areas. Two kickoffs that edit the SAME file or share a `where unknown` domain are NOT parallel-safe → **serialize them across waves**, core / highest fan-in first. A declared `parallelizable_with` pair is only the starting grouping; it still gets serialized if the file/migration check finds a clash.
3. **Migration collision**: if two kickoffs in the same wave seed a migration → serialize them across waves (organic merges centrally, so the second renumbers on integration). The truth about taken numbers is **git** (measure the branches), not a registry; the executor re-verifies at the merge gate (sibling of `/mala-pata-loop-start` 4.1-bis).
4. **Triage by weight**: a kickoff that itself flags as optional ("evaluar si amerita") or that is tiny enough to be a `/mala-pata-shot` → **defer** it out of the first wave (or recommend downgrading it to shot). Do not put it in wave 1.
5. **Split (ONLY recommend)**: if a kickoff mixes 2 independent concerns → **recommend** splitting into A/B with the reason. Do NOT create the split kickoffs (the user's decision).
6. **Merge order inside a wave**: since the executor merges centrally between waves, state the intended merge order of each wave (dependency, then fan-in, then smallest first). Per-commit RDD and the smoke gate stay INSIDE each tab (`organic-start` runs them) — the plan only notes which kickoffs will need a smoke gate (UI/behavior change) so the human knows what the merge table will show.
7. **Base branch freshness (only DETECT and WARN — do not fix here)**: for each distinct `base` in the batch, `git -C <repo> fetch origin <base>` and compare `git rev-parse <base>` vs `origin/<base>`. If local is BEHIND, flag it: "`<base>` local behind origin — `/mala-pata-organic-orchestrate-start` advances the worktrees before launching". Fetch + rev-parse are READ-ONLY.
8. **Mixed bases**: if kickoffs declare different `base` branches, say so — a wave only mixes kickoffs of the SAME base (the executor derives readiness per base).

## Step 4 — Output: PLAN (BLUF) + wave table + warnings table + handoff

ALWAYS return, in this order:

1. **BLUF line (first):** `Plan: <n> kickoffs → <w> waves · <k> conflicts · recommended: <launch wave 1 | split X | defer Y>`.

2. **Wave table** — one row per kickoff; waves derive from the dependency network:

   | Wave | Kickoff | Depends on | Parallelizes with | Conflict / note |
   |---|---|---|---|---|
   | 1 | <change-name> | — | {<change-name>, <change-name>} | <file clash / migration / where unknown / none> |
   | 2 | <change-name> | <change-name> | — | <serialized after X: shared file> |

3. **Split / defer table** (only when relevant — omit the whole block otherwise):

   | Type | Kickoffs | Evidence | Recommendation |
   |---|---|---|---|
   | split / defer / downgrade-to-shot | <change-names> | <two independent concerns / optional flag / 1-3 files> | <split into A/B / defer past wave N / run as shot> |

4. **Warnings table** — one row per issue, never a flat list (omit rows that do not apply, but ALWAYS emit the table with at least a `none` row):

   | Type | Kickoffs | Evidence | Recommendation |
   |---|---|---|---|
   | file clash / migration collision / undeclared dependency / excluded (not organic) / base-freshness / mixed bases | <change-names> | <file:line / number / branch behind / route value> | <serialize / renumber / confirm / ff first> |

5. **Handoff to start** (the single copy-paste command; absolute paths):
   ```
   /mala-pata-organic-orchestrate-start <absolute-path-of-kickoff-1>.md <absolute-path-of-kickoff-2>.md …
   ```
   Pass the kickoffs of **wave 1** to launch one round; pass the **whole batch** instead to let the executor run every round (it derives each wave live in git and owns the merges between waves). `organic-orchestrate` only plans.

**Emit this block's structural labels verbatim in English** — the BLUF line, every table header (`Wave`, `Kickoff`, `Depends on`, `Parallelizes with`, `Conflict / note`, `Type`, `Kickoffs`, `Evidence`, `Recommendation`) and the command line stay English; only the values follow the conversation language.

**Structure:** Precedence diagramming / PDM (PMBOK) + wave layering (house method).

## Hard rules
- **DO NOT** execute anything mutating: no worktrees, no ff/rebase, no launch config, no opening sessions, no merge. If the user asks "lanzá / orquestá de verdad", redirect to `/mala-pata-organic-orchestrate-start`.
- **DO NOT** create the kickoffs of a split (you only recommend), and **DO NOT** edit any kickoff.
- **DO NOT** plan non-organic kickoffs: exclude them and tell the human to run loops by hand with `/mala-pata-loop-start`.
- **Never invent a dependency** a kickoff did not declare; flag a suspected one and let the human confirm.
- The `git fetch`/comparison of Step 3.7 is the ONLY thing that touches network/git, and it is READ-ONLY (fetch + rev-parse).
- ABSOLUTE paths in the commands; relative only when talking to the user.

## What it does NOT do
- It does not create worktrees, branches, launch configs or Warp tabs.
- It does not run `/mala-pata-organic-start`, RDD, smoke, PR, merge or cleanup — those belong to the executor and to each lane tab.
- It does not decide smoke or RDD: it only notes which kickoffs will likely need a smoke gate.
- It does not write to engram or to the repo; it is a read-only report.
- It does not plan SDD (loop) kickoffs nor roadmaps (roadmaps: see `/mala-pata-roadmap-orchestrate`).

## Runtime compatibility
The analysis, the waves and the command are portable to any CLI. The handoff to Warp/Claude only applies when the runtime is Claude with Warp; in another CLI, return the plan and the per-kickoff `/mala-pata-organic-start <absolute-path>` commands and omit the `orchestrate-start` handoff.

**Structure:** precedence diagramming + wave layering = house method.
