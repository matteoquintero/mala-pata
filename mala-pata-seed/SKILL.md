---
name: mala-pata-seed
description: Deterministic fixture seeder for testing on a branch, OUTSIDE shot/organic/loop. Reads the `## Seed` section of the QA that mala-pata-walkthrough generated (which fixtures, derived from the Givens + the kickoff's smoke_test.data) and seeds them with the project's mechanism (seeders/factories that sdd-init detected), idempotently, against the test DB. It does NOT improvise — if the recipe or the mechanism is missing, it STOPS and warns. It does NOT touch prod, does NOT write app code, does NOT run tests. It is also the executor that the smoke test gate (4.1-ter) delegates to in-cycle. Trigger — "sembrá los fixtures", "seed para probar <feature>", or run it on a branch before testing by hand.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.1.0"
---

# /mala-pata-seed — deterministic fixture seeder (reads walkthrough)

Input: **the CLI's** — a feature/change/branch, or the path of the walkthrough QA that carries the `## Seed` section.

Your job: **execute the seeding** of the fixtures a test needs, reading the recipe that `mala-pata-walkthrough` left — without inventing. You are the executor counterpart of walkthrough (which describes, read-only): walkthrough says WHICH fixtures; you SEED them. You are useful for testing on a branch **when you are NOT in a cycle** (shot/organic/loop); inside a cycle, the smoke test gate (`mala-pata-loop-start` 4.1-ter / `mala-pata-organic-start` Step 7) delegates this same thing to you.

> **Deterministic, not creative.** You seed EXACTLY what walkthrough's `## Seed` section says, with the project's mechanism. If the recipe is missing, incomplete, or the seed mechanism does not exist → **STOP and warn**, never guess what data to create.

## Requirements (orchestrate, do not reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP and ask to install it):
  - `git` — to know which branch/repo you are in. Always present.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded):
  - `serena` / `codegraph` — locate the project's seed mechanism (factories/seeders) at symbol level. Fallback: grep/Read.
  - `engram` — read the walkthrough QA pointer (`sdd/<change>/walkthrough`) and `sdd-init/<project>`. Fallback: ask for the QA path by hand.

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP, e.g. serena). If a mandatory tool is missing, do not continue.

## Hard rule — the test DB, NEVER prod

You seed ONLY against the project's **test DB** (`TEST_DB_URL` or the equivalent that `sdd-init` states). Before seeding, confirm that the target is the test DB; if you cannot confirm it, **STOP**. Seeding against prod or against an unconfirmed DB is forbidden. Absolute paths always.

## Flow

1. **Find the recipe.** Locate the `## Seed (fixtures)` section of the `mala-pata-walkthrough` QA for this feature (direct path, or through the engram pointer `sdd/<change>/walkthrough`). If the QA does not exist or has no `## Seed` → **STOP** and ask that `mala-pata-walkthrough` be run first (it is the one that builds the recipe). Do not invent fixtures.
2. **Resolve the project's mechanism.** `mem_search("sdd-init/<project>")` → what the project seeds with (seeders/factories/command). If `sdd-init` is not there or does not define a seed mechanism → **STOP** and warn; do not build ad-hoc INSERTs.
3. **Confirm the test DB** (hard rule above).
4. **Seed, idempotently.** Run the project's mechanism with the recipe's data. Idempotent: upsert / stable keys / namespaced by change, so that re-running does not clash on constraints nor duplicate rows.
5. **Report what you seeded.** Concrete list: ids / records / keys that are ready, so that the human (or the gate) goes straight to testing with walkthrough's **table** (`# | Given | When | Then`) and its access block.

## Teardown (optional, asked — default NO)

When finished, one line: **"¿Borro lo que sembré? (default: no)"**. Default is not to delete — a persistent test DB with data is useful. If asked to delete, delete **only what this run seeded** (by ids/namespace), NEVER a wipe of the DB.

## What it does NOT do

- Does NOT invent fixtures — it only seeds what walkthrough's `## Seed` recipe says.
- Does NOT touch prod or a DB not confirmed to be the test one.
- Does NOT write application code, does NOT run the SDD cycle, does NOT dispatch `sdd-*` agents.
- Does NOT generate the test script (that is `mala-pata-walkthrough`) — it only seeds.
