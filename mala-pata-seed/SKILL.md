---
name: mala-pata-seed
description: Deterministic fixture seeder for testing on a branch, OUTSIDE shot/organic/loop. Reads the `## Seed` section of the QA that mala-pata-walkthrough generated (which fixtures, derived from the Givens + the kickoff's smoke_test.data) and seeds them with the project's mechanism (seeders/factories that sdd-init detected), idempotently, against the test DB. It does NOT improvise — if the recipe or the mechanism is missing, it STOPS and warns. It does NOT touch prod, does NOT write app code, does NOT run tests. It is also the executor that the smoke test gate (4.1-ter) delegates to in-cycle. Trigger — "sembrá los fixtures", "seed para probar <feature>", or run it on a branch before testing by hand.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.4.0"
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

## Hard rule — the test DB, NEVER prod (and for a smoke run, its ephemeral fork)

You seed ONLY against the project's **test DB** (`TEST_DB_URL` or the equivalent that `sdd-init` states) — **NEVER prod**. Before seeding, confirm the target; if you cannot confirm it, **STOP**. **When the caller is the in-cycle smoke gate** (`mala-pata-loop-start` 4.1-ter / `mala-pata-organic-start` Step 7), the confirmed target is an **ephemeral FORK of the test DB** that the gate created — seed into **that fork**, never the shared base test DB. Seeding against prod or against an unconfirmed DB is forbidden. Absolute paths always.

## Flow

1. **Find the recipe.** Locate the `## Seed (fixtures)` section of the `mala-pata-walkthrough` QA for this feature (direct path, or through the engram pointer `sdd/<change>/walkthrough`). If the QA does not exist or has no `## Seed` → **STOP** and ask that `mala-pata-walkthrough` be run first (it is the one that builds the recipe). Do not invent fixtures.
2. **Resolve the project's mechanism.** `mem_search("sdd-init/<project>")` → what the project seeds with (seeders/factories/command). If `sdd-init` is not there or does not define a seed mechanism → **STOP** and warn; do not build ad-hoc INSERTs.
3. **Confirm the target DB** (hard rule above) — the test DB standalone, or the smoke gate's **ephemeral fork** when invoked in-cycle; never the shared base in a smoke run, never prod.
4. **Seed, idempotently.** Run the project's mechanism with the recipe's data. Idempotent: upsert / stable keys / namespaced by change, so that re-running does not clash on constraints nor duplicate rows.
5. **Report what you seeded.**

   **BLUF first** (plain line):
   - Happy path: `Seeded <n> fixtures into <test DB>`.
   - Stopped: `✗ stopped: <missing recipe | missing mechanism | unconfirmed test DB>`.

   Then **what you seeded** (a REAL Markdown table, NEVER fenced; emit EXACTLY this shape — never prose or vertical blocks; one line per cell — one row per fixture), so the human (or the gate) goes straight to testing with walkthrough's **table** (`# | Given | When | Then`) and its access block:

   | Fixture | Records/ids | Key | Mechanism | Target DB | Idempotent |
   |---|---|---|---|---|---|
   | <fixture> | <ids/records ready> | <stable idempotent key> | <project seeder/factory> | <test DB — never prod> | ✓ yes · ✗ no |

   **Emit every structural label verbatim in English** — section headers, field labels and table/column headers (`Fixture`, `Records/ids`, `Key`, `Mechanism`, `Target DB`, `Idempotent`) stay English even when the conversation is in the user's language; only the values are localized.

   `Structure: xUnit Test Patterns — fixture setup (Meszaros). Test-DB-never-prod safety rule = house method.`

6. **Leave a record (mandatory — forward-only, feeds `/mala-pata-domain-radar`).** Write a lightweight record `mala-pata/seeds/<change>.md` (`mkdir -p` the folder) that STARTS with YAML frontmatter: `domain: <X>` (**copy it from the walkthrough QA frontmatter you read in step 1**; if that QA has no `domain`, infer FEATURE → area → `main` and **ASK the human on ANY doubt** — never blank), `roadmap: <slug | none>` (from the same QA), `change: <change-name>`, `seeded_at: <ISO 8601>`. Body: one line naming the fixtures seeded and the target test DB (no secrets — reference the mechanism, not credentials). This is how domain-radar sees a change was seeded. **Write only — do NOT commit/push**; name the path to the human. This record is the ONE repo artifact seed leaves — it still writes no app code and still touches only the test DB.

## Teardown (optional, asked — default NO)

When finished, one line: **"¿Borro lo que sembré? (default: no)"**. Default is not to delete — a persistent test DB with data is useful. If asked to delete, delete **only what this run seeded** (by ids/namespace), NEVER a wipe of the DB.

## What it does NOT do

- Does NOT invent fixtures — it only seeds what walkthrough's `## Seed` recipe says.
- Does NOT touch prod or a DB not confirmed to be the test one.
- Does NOT write application code, does NOT run the SDD cycle, does NOT dispatch `sdd-*` agents.
- Does NOT generate the test script (that is `mala-pata-walkthrough`) — it only seeds.
