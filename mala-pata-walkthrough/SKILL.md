---
name: mala-pata-walkthrough
description: From a PR/change OR a roadmap (a PR = "a one-node roadmap"), generates a test walkthrough of the functionality in Given/When/Then + followable steps, and projects it into TWO lanes WITHOUT mixing them (Diátaxis) — (1) internal QA/UAT guide "what to test / how to test" and (2) how-to/tutorial documentation for the end customer. Living documentation (BDD): the same Given/When/Then verifies AND documents. It does NOT write code, does NOT run the SDD cycle, does NOT replace sdd-verify (which is machine verification). Trigger: "documentá cómo probar esto", "guía de prueba", "tutorial de la funcionalidad", "doc de funcionamiento para el cliente", starting from a PR, a change-name or a roadmap.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.6.0"
---

# /mala-pata-walkthrough — test walkthrough + customer doc base

User input: **delivered by the CLI** (a PR/change, or the path to a roadmap).

Your job: turn an already-defined or already-delivered functionality into a **walkthrough a human can follow by hand** to test it, written so that it **can be reused as functioning documentation for the end customer**. You do NOT write code, do NOT run the SDD cycle, do NOT replace `sdd-verify`.

## Requirements (orchestrate, don't reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory**: none.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded):
  - `gh` — reading PRs. Fallback: pass the PR/diff by hand. Install: `brew install gh`.

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP, e.g. serena). If a mandatory one is missing, do not continue.

## Principles (proven, not invented)

- **Diátaxis** (documentation framework from Canonical/Ubuntu): tutorial (learning) ≠ how-to (solving a task) ≠ reference ≠ explanation. The QA script and the customer doc **share the steps but differ in audience and purpose** → they are NOT mixed into a single doc; **two renders of the same core** come out.
- **BDD / living documentation**: the same **Given/When/Then** verifies AND documents. It is the bridge between "test" and "doc". The DoD of this family's kickoffs is ALREADY in Given/When/Then — it is direct raw material.
- **Boundary with verify (don't duplicate)**: `sdd-verify` is **technical/machine** verification against the DoD (build, tests, checklist). This is a **human walkthrough** + the doc base for the customer. Different purposes.

## Unified input model — everything is 1..N "shippable units"

Two inputs, **PEERS** (neither is secondary):

- **PR / change** → **1 unit** (a PR is "a one-node roadmap").
- **Roadmap** → **N units** (one per shippable phase).

**ALWAYS normalize the input to an ordered list of units.** From there on the per-unit flow is identical, whether it comes from a PR or from a roadmap phase.

## Step 0 — Entry gate

Detect the input type and build the list of units:
- **Path to a roadmap `.md`** → each phase = one unit (read its IN/OUT, DoD and edges).
- **PR# / branch / change-name** → one unit (you will fetch the diff + the SDD artifacts).

If you cannot identify the functionality or where to get it from → **STOP** and ask for the concrete input (PR#, change-name or roadmap path). Do not invent functionality.

## Step 1 — Gather sources per unit (read-only)

For each unit, collect what ALREADY exists (do not re-derive from scratch):
- **SDD in engram**: `sdd/<change>/spec` (Given/When/Then scenarios), `design`, `tasks`, and the **kickoff DoD** (already in Given/When/Then).
- **Organic change (ODD)**: there is no spec. Read the feature-doc `mala-pata/odd/<change>.md` (if it exists) + the organic kickoff's `## DoD` (now Given/When/Then) and use it directly. Do not invent behavior the DoD does not state.
- **The real change**: the diff (`gh pr diff <n>` / `git -C <repo> diff <base>...<branch>`), and the **endpoints / screens / commands** that were touched.
- **Roadmap**: IN/OUT and success criteria of each phase.
- Keep ONLY the **user-observable behavior**, not the internals. If something is only visible by reading code, it is not walkthrough material.

## Step 2 — Extract the "scenario core" (single source of truth)

For each observable behavior, one scenario in this format — it is the **core** from which both lanes derive:

```
### <behavior in user language>
- **Context (Given)**: <concrete initial state>
- **Action (When)**:
  1. <concrete, followable step — EXACT click / command / input>
  2. ...
- **Expected result (Then)**: <observable, verifiable by eye>
- **Test data**: <concrete inputs, not "any value">
- **Edge cases**: <variations that must also be checked>
```

Hard rule: **if a step cannot be followed by someone who did not write the code, it is badly written.** Zero internal jargon in the core.

## Step 3 — QA/UAT lane (internal use: "what to test / how to test")

**Access block (MANDATORY, goes first — without this the lane is not delivered).** So the human can test without breaking anything, the script ALWAYS starts with how to access:
- **URL**: that of the TEST environment (localhost:<port> or the test env). **NEVER production.**
- **Test credentials**: the test user/login to use — **reference the credential SOURCE (the seeder/factory that creates the QA user, `.env.test`, or the secret manager), NEVER the literal value**. The QA file is committed to the repo (`mala-pata/walkthroughs/`, Step 6), so a pasted password / token / API-key would leak into git history. Test environment only.
- **Server running**: how to bring up the app against the **test DB** and confirm it is up before starting.

**Test table (MANDATORY, fixed format).** From the core, ONE row per scenario — this is the exact format, do not change it:

| # | Given (path) | When | Then (what you must see) | Pass/Fail | Failure signal |
|---|---|---|---|---|---|
| 1 | <concrete initial state + where/route> | <exact action> | <result observable by eye> | ✓ pass · ✗ fail | <what is seen if it did NOT work, not just the happy path> |

Below the table, per scenario (`Pass/Fail` and `Failure signal` now live IN the table columns):
- **Test data and edge cases** explicit.
- **Regression note**: what should NOT have changed and should be confirmed along the way.

This lane is an **actionable checklist**, not prose. The **access block** and the **table** are ALWAYS mandatory.

`Structure: Diátaxis how-to (internal verification) + BDD Given/When/Then (North). QA access block = house method.`

## Step 3.5 — `## Seed` section (fixtures recipe, for `mala-pata-seed`)

walkthrough does NOT seed (it stays read-only) — it leaves the **recipe** for `mala-pata-seed` (standalone, on a branch) or the smoke-test gate (in-cycle, 4.1-ter / Step 7) to execute. If the change touches data, add a `## Seed (fixtures)` section to the QA:
One row per fixture (a REAL Markdown table, NEVER fenced), **derived from the core's `Given` + `Test data`** (+ the kickoff's `smoke_test.data` if it exists):

| Fixture | Derived from (Given) | Mechanism | Key | Status |
|---|---|---|---|---|
| <minimal fixture> | <the core `Given` + `Test data` it comes from> | <project seeder/factory from `sdd-init`> | <stable idempotent key> | ✓ ready · ◐ to confirm |

- **Do NOT invent data** — if a `Given` is not enough to fix a value, its `Status` is `◐ to confirm`, never a guessed value.
- **Where** — the **test DB** (never prod). **Idempotent** — stable keys so re-seeding does not collide.
- Name the `Mechanism` (the project's seeders/factories detected by `sdd-init`); do not reimplement it.

This section is the contract that `mala-pata-seed` reads. If the change does NOT touch data (e.g. purely visual), omit it and say so explicitly.

## Step 4 — End-customer lane (how-to / tutorial)

From the **SAME** core, rewrite for the end user:
- **No jargon, no pass/fail, no internal test data.**
- Oriented to **outcome and "what for / when to use it"**, not to "verifying".
- Title in task form ("How to <do X>") or as a guided tutorial, depending on what Diátaxis calls for.
- **Screenshot placeholders** for each visual step (`![description](placeholder)`); capturing them is optional (Step 5).
- Lean on the **`cognitive-doc-design`** skill for writing quality (load it lightly, do not run it as a phase).

This lane **NEVER** mentions tests, branches, migrations or anything internal.

`Structure: Diátaxis how-to / tutorial + Living Documentation (Adzic/Martraire).`

## Step 5 — Screenshots (optional, if the app can be run)

If the stack allows bringing up the app **and the human OKs it**: capture the visual steps with the project's tool (Playwright if available) and replace the placeholders. If it is not possible or not wanted, leave the placeholders marked for the human to complete. **It is not mandatory** to close.

## Step 6 — Location and persistence (advise + confirm)

Diátaxis says **do NOT mix** → **two files**, not one:
- **End customer** (versionable, goes to the repo): advise `docs/guides/<slug>.md` (or the docs convention the project uses). Confirm the folder with the human.
- **QA/UAT** (internal): advise `mala-pata/walkthroughs/<slug>-qa.md` (inside the repo, versioned, like the rest of mala-pata). Confirm.
- **Lightweight pointer in engram**: `mem_save` topic_key `sdd/<change>/walkthrough`, one-line content with the paths of the two files (so the radar and future sessions can find it). If the input was a roadmap without a unique change-name, use the roadmap slug.

## Step 7 — Human gate

**BLUF first** (plain line): `Walkthrough: <n> scenarios · 2 files · <k> to confirm`.

Then present the two lanes (short summary + file paths) and **wait for OK or adjustments** before considering it closed. Like everything in the family: do not mark "done" with something unreviewed.

**Emit every structural label verbatim in English** — in BOTH lanes and the `## Seed` block: section headers, field labels (`Access block`, `Test credentials`, `URL`, `Server running`), table/column headers (`Given (path)`, `When`, `Then`, `Pass/Fail`, `Failure signal`, `Fixture`, `Derived from (Given)`, `Mechanism`, `Key`, `Status`), and enum/option tokens stay English even when the conversation is in the user's language; only the values and content are localized.

`Structure: Diátaxis (Procida) + BDD Given/When/Then (North) + Living Documentation (Adzic/Martraire). QA access block + two-lane split = house method.`

## Relation to the family

- **Consumes** a roadmap from `/mala-pata-roadmap`, or a change/PR closed by `/mala-pata-loop-start` or `/mala-pata-organic`.
- **Typical moment**: after `verify` (real functionality → richer doc), or over a roadmap **going forward** (generates a provisional skeleton that gets filled in as each phase is implemented).
- It does **not** orchestrate, does **not** execute phases, does **not** mutate code.

## What it does NOT do (invariants)

- Does NOT write code nor run the SDD cycle.
- Does NOT replace `sdd-verify` (machine verification against the DoD).
- Does NOT mix the QA lane with the customer lane (Diátaxis: two renders, two files).
- Does NOT invent behavior that is not in the PR / roadmap / SDD artifacts.
