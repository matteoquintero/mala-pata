---
name: mala-pata-loop-orchestrate
description: READ-ONLY planner for a batch of SDD kickoffs — analyzes several kickoffs and returns a start plan (waves, parallelism, file/migration conflicts, recommended splits, deferrals) + copy-paste commands. It does NOT create worktrees, does NOT advance branches, does NOT launch sessions — /mala-pata-loop-orchestrate-start does that. Trigger — "planificá estos kickoffs en olas", "qué kickoffs puedo correr en paralelo", "orquestá este lote de SDD".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "2.5.0"
---

# /mala-pata-loop-orchestrate — Plan a BATCH of kickoffs (READ-ONLY)

You are the batch **planner**. You are handed **several kickoffs** and you return a **start plan**: in
which **waves** to run them, what to **parallelize** and what **NOT**, where there is a **file/migration
conflict**, which kickoff **is worth splitting in two**, which to **defer** for low value, and the commands ready to
paste.

> **This skill executes NOTHING**: it does not create worktrees, does not advance branches, does not write launch configs,
> does not open sessions. It is ONLY analysis + plan. To **launch** the batch use `/mala-pata-loop-orchestrate-start`
> (separation of responsibilities, same as `loop` vs `loop-start`).

You do NOT run the SDD cycles here (that is done by `/mala-pata-loop-start` per kickoff). This command
**plans the batch**; the launch lives in the sibling skill.

## Requirements (orchestrate, do not reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP and ask to install it, do not start):
  - `git` — reading branches and detecting conflicts. Install: always present; requires no installation.
  - `gentle-ai` — SDD engine. Install: `brew install gentleman-programming/tap/gentle-ai`.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded):
  - `engram` — persistent memory and continuity pointer. Fallback: continue with the explicit list of kickoffs. Install: comes with gentle-ai (`brew install gentleman-programming/tap/gentle-ai`).

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP, e.g. serena). If a mandatory tool is missing, do not continue.

## Step 1 — Load the kickoffs
Input (accepts any of these forms):
- **Explicit list of paths** (current format): absolute paths to the kickoff `.md` files that `/mala-pata-loop` left in `mala-pata/kickoffs/` (inside the repo).
- **Auto-discover**: if no list is passed, list `mala-pata/kickoffs/*.md` (or by a prefix/module if they indicate one, e.g. "todos los de sentencias").
- **Legacy** (old kickoffs, compatibility only): engram ids (`#6717 #6712 …`) or topic_keys (`sdd/<name>/kickoff`).

For each one: if it is a path → `Read` directly. If it is legacy → `mem_search` → `mem_get_observation`; if what it returns is the lightweight pointer (`Kickoff in file: <path>`) instead of the full content, follow that path and read the file.
If any is not found → warn and continue with the rest (do not invent context).

## Step 2 — Extract the metadata that governs orchestration
From each kickoff take:
- `change_name`, `profile` (FULL / STANDARD / LITE / MINIMAL — infer the weight/size from it), `depends_on` (the dependency list; blocking by default), `parallelizable_with` (what the kickoff declares as safe to run alongside).
- **Affected areas/files** (the "Architecture and affected layers" section — BCs/layers + ARCHITECTURE.md refs; cross-check "Technical reinterpretation" Scope IN) → key for detecting clashes.
- **Migration?** = `migrations_reserved` is not `N/A` (provisional number present).
- **base branch** declared in the kickoff.
- **Phases**: almost all are SDD (`explore→propose→spec→design→tasks→apply→verify→archive`).
  The **only NON-SDD phases** are the **final tail** of `/mala-pata-loop-start` (Step 4): **PR →
  pipeline/CI review → cleanup**. Use this phase awareness to place the
  parallel/serial boundary (see Step 3).

## Step 3 — Analyze (plan rules)
1. **Dependency graph** (`depends_on`) → topological order. Every listed dependency is blocking by default = the
   dependent does not enter **Apply** until the provider closes **design** (the convention/contract).
2. **Conflict by shared file**: intersect the affected areas. Two kickoffs that edit
   the SAME file **cannot Apply in parallel** (merge conflict) → serialize their Apply
   or stagger them. Use each kickoff's `parallelizable_with` as the starting parallel grouping (a declared pair still gets serialized if the file/migration check finds a clash). **Planning** (explore→design) CAN go in parallel (it does not write code).
3. **Migration collision**: if ≥2 seed a migration and run in parallel → the number is **provisional,
   not a reservation**: the first to merge keeps it and the others renumber on integration (see
   `/mala-pata-loop-start`, Step 4.1-bis). The truth about taken numbers is **git** (measure the branches),
   NOT a registry in engram; the kickoffs carry their provisional number in the frontmatter
   `migrations_reserved`. Never trust the file number nor a registry.
4. **Triage by weight**: a MINIMAL/LITE kickoff the kickoff itself flags as optional ("evaluar si amerita") → **defer it** out of the
   first batch (or close them at propose without code). Do not put them in wave 1.
5. **Split (ONLY recommend)**: if a kickoff mixes 2 independent concerns or is profile FULL with two
   separable deliverables → **recommend** splitting it into A/B with the reason. Do NOT create the
   split kickoffs (that is the user's decision).
6. **Shared final tail**: if several changes go to the same destination, decide whether **one consolidated
   PR** or **separate PRs** is better; remember that the final tail (PR/CI/clean) of each cycle is NOT
   blindly parallelized (do not merge with red CI; a single active PR per piece of work).
7. **Base branch freshness (only DETECT and WARN — do not fix here)**: for each distinct base branch
   in the batch, `git fetch origin <base>` and compare `git rev-parse <base>` vs
   `origin/<base>`. If the local is BEHIND, flag it in the plan: "`<base>` local behind origin —
   `/mala-pata-loop-orchestrate-start` will advance the worktrees before launching". The real fix
   (ff/rebase of the worktrees) is done by the start skill; here it is only reported so the user
   knows before launching.

## Step 4 — Output: PLAN as a wave table + commands + handoff to start
ALWAYS return:
1. **Wave table**: `Wave | kickoff (#id) | start phase | parallelizes with | boundary (up to what
   phase in parallel) | conflict/note`.
2. **Copy-paste commands** per wave, to run each cycle by hand if the user does NOT want to launch in Warp:
   ```
   /mala-pata-loop-start <absolute-path-of-kickoff>.md
   ```
   (All enter through **Explore**; make that clear. The difference is the wave and up to which phase it can advance
   in parallel.)
3. **Handoff to start**: the line to launch the batch (or a wave) in Warp with the sibling skill:
   ```
   /mala-pata-loop-orchestrate-start <kickoffs-of-the-wave-to-launch>
   ```
   Make clear to the user: `orchestrate` only plans; to create worktrees + open sessions use
   `orchestrate-start`.
4. **Warnings**: file clashes, migration collision, dependencies, recommended splits,
   deferrals, final tail coordination, and **base freshness** (Step 3.7).

## Hard rules
- **DO NOT** execute anything mutating: no worktrees, no ff/rebase, no launch config, no opening sessions.
  If the user asks "lanzá / orquestá de verdad", redirect to `/mala-pata-loop-orchestrate-start`.
- **DO NOT** create the kickoffs of a split (you only recommend).
- The `git fetch`/comparison of Step 3.7 is the ONLY thing that touches network/git, and it is READ-ONLY (fetch + rev-parse).
- ABSOLUTE paths in the commands; relative only when talking to the user.

## Runtime compatibility
The analysis, the waves and the commands are portable to any CLI. The handoff to Warp/Claude only
applies when the runtime is Claude with Warp; in another CLI, return the plan and the commands and omit the
`orchestrate-start` handoff.
