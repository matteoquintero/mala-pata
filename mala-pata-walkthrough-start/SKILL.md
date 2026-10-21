---
name: mala-pata-walkthrough-start
description: RUNS a QA walkthrough that /mala-pata-walkthrough wrote — executes it phase by phase in a real browser via Playwright MCP, leaving EVIDENCE per phase (a screenshot + a Playwright trace) in the repo, with the verdict decided by assertions (not by interpreting the image) and a console/network error gate. Honors the walkthrough's delicacy level: low → the agent runs it and reports with evidence; medium → runs it and flags "review the evidence"; high/delicate → the agent does NOT run the sensitive steps, it seeds + opens the app + hands the step list to the human. Standalone, and also the executor the smoke-test gate delegates to (twin of mala-pata-seed). Trigger — "/mala-pata-walkthrough-start <path>", "corré el smoke de <feature>", "hacé el walkthrough por browser".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.1.0"
---

# /mala-pata-walkthrough-start — run a walkthrough in the browser, leave evidence

Input: **the one delivered by the CLI** — the path to a walkthrough QA (`mala-pata/walkthroughs/<slug>-qa.md`) or its slug.

Your job: **execute** the QA walkthrough that `/mala-pata-walkthrough` described — drive the real app in a browser, phase by phase, proving each `Then` with an assertion and leaving a human-readable evidence trail. You are the executor counterpart of `/mala-pata-walkthrough` (which describes, read-only), exactly as `/mala-pata-seed` is the executor of its `## Seed` recipe. You run the smoke; you do not decide what counts as critical (that is the delicacy level + the human).

> **Verdict by assertions, evidence by screenshots.** Pass/fail comes from **web-first / ARIA assertions** on each `Then` (visible text, role, URL, title) — NEVER from "looking at the screenshot and deciding it looks right" (that is the failure mode that returns plausible-but-wrong with no error). The screenshot + trace are the **human record**, not the judge.
> **Delicacy decides who runs it.** You read the walkthrough's `smoke_delicacy` and act on it (Phase 1). You are not the one who decides a flow is too risky to touch — the level is; and for anything delicate, the human runs it.
> **Evidence lives in the repo, never in /tmp.** Per-phase screenshots + the Playwright trace go to `mala-pata/walkthroughs/<slug>/evidence/` (write-only; the human commits). Leaving evidence in a scratchpad temp dir is forbidden — it is impossible to find later.

## Requirements (orchestrate, do not reinvent)

- **Mandatory for an agent-run** (no fallback that fakes it): **Playwright MCP** (`mcp__…playwright__*`) — the browser driver (accessibility tree = deterministic actions on stable refs). If it is NOT available, do NOT improvise nor fake a pass: treat the run like `delicacy: high` → seed, give the human the step list, and ask them to run it by hand. Also `git` (repo root).
- **Recommended** (warn, continue degraded): `mala-pata-seed` (seeds the `## Seed` recipe); `engram` (walkthrough pointer). Fallback: ask for the QA path; the file is the source.

## Hard rules

> **#1 — Playwright MCP, accessibility-first.** Act on roles/labels/refs, not pixel coordinates (layout shifts break coordinate clicks). Wait on real readiness (web-first assertions, `document.fonts.ready`), never fixed sleeps.
> **#2 — Deterministic + isolated environment.** Run against the **TEST env on this worktree's port** (never prod). Apply the determinism levers: disable animations, fixed viewport, seeded data (via seed), block third-party noise (analytics, chat widgets, cookie banners) so they do not flake the run.
> **#3 — Console + network gate.** Register `page.on('console')` and the response listener; **FAIL the run on any console error or any 4xx/5xx** during the flow (allowlist known-harmless noise, and keep warnings separate from errors). This catches the regressions the happy-path `Then` does not.
> **#4 — Absolute paths**; evidence folder created with `mkdir -p`; write-only (no commit).

## Phase 0 — Load the walkthrough

1. Resolve the QA (path, or slug → `mala-pata/walkthroughs/<slug>-qa.md`, or the `sdd/<change>/walkthrough` pointer). None resolves → STOP, ask for the path. If there is no QA → route to `/mala-pata-walkthrough` to create it first (you do not invent scenarios).
2. Read the frontmatter (`slug`, `domain`, `change`, `smoke_delicacy`, `qa_done`) + the **Access block** (test URL + how to bring the app up + the credential SOURCE) + the **Test table** (the phases: `# | Given | When | Then | Evidence`) + the **`## Seed`** recipe (if present).

## Phase 1 — Delicacy gate (who runs it)

Resolve `smoke_delicacy` (infer from the change if unset — money, prod-like data, irreversible writes, or judgment-heavy UX → round UP on doubt):

- **low** — objective, reversible, no money/prod data → **the agent runs it** (Phases 2-4), reports with evidence, **no question**.
- **medium** — the agent runs it, and the report **flags "review the evidence"** before the human confirms.
- **high / delicate** — the agent does **NOT** execute the sensitive steps. It seeds, brings the app up, and hands the human the **step list + access block** with one line: "this smoke is delicate — better you run it." Then it stops at the human gate.

Only **medium/high (or unset)** prompt the human about who runs it; **low proceeds silently** (this is the "agent does the smoke on its own" the user liked).

## Phase 2 — Prepare (deterministic + isolated)

1. Confirm the target is the **test env + this worktree's port** (never prod); if you cannot confirm → STOP.
2. **Seed** the `## Seed` recipe via `/mala-pata-seed` (idempotent, test DB). If the change touches no data, skip.
3. Bring the app up per the Access block; apply the determinism levers (#2). Confirm it is up (a web-first assertion on the landing page) before Phase 3.
4. **Tag what the run itself creates (so cleanup can remove it).** Any record the smoke creates while exercising the app (byproducts — e.g. an order created during the flow) is an **ephemeral cycle-only fixture, NOT a seed**: create it under a **cycle/run-scoped namespace** (distinct from the persistent seed namespace) or inside a transaction that rolls back, so the cycle cleanup (`/mala-pata-loop-start` 4.5 / `/mala-pata-organic-start` Step 7) removes exactly those and keeps the seeds. Never write smoke byproducts under the seed's persistent namespace.

## Phase 3 — Run phase by phase (Playwright MCP)

Create `mala-pata/walkthroughs/<slug>/evidence/` and **start the trace**. For each row of the Test table, in order:

1. **Perform the `When`** — the exact action(s) on accessibility refs.
2. **Assert the `Then`** — a web-first/ARIA assertion on the observable result (text/role/URL/title). Match → phase `✓`. Mismatch → phase `✗`, capture the failure state.
3. **Screenshot** → `evidence/<NN>-<step-slug>.png` (one per phase — the per-phase evidence the human scans).
4. The console/network gate (#3) runs throughout; a console error or 4xx/5xx marks the run failed even if the `Then` passed.

A `✗` on a phase stops the flow if later phases depend on it; otherwise continue and collect all failures. Never retry blindly; never fake a `Then`.

## Phase 4 — Evidence + verdict

1. **Stop the trace** → save `evidence/trace.zip` (open with `npx playwright show-trace <path>` — DOM before/after each action + console + network + timeline).
2. **Verdict** = all phases `✓` AND no console errors / no 4xx-5xx (minus allowlist). Report — BLUF then a real table (NEVER fenced; one line per cell):

   `Smoke — <slug>: <pass/fail> · <k>/<n> phases · console/network <clean/ N errors> · delicacy <low/medium/high> · evidence → mala-pata/walkthroughs/<slug>/evidence/`

   | # | Phase | Assert (Then) | Evidence | Result |
   |---|---|---|---|---|
   | 1 | <when → then> | <what was asserted> | `<NN>-<step>.png` | ✓ pass · ✗ fail |

3. The **trace path** + the evidence folder (also in the BLUF).

## Phase 5 — Human gate (do not self-approve)

The agent's run is the evidence, not the acceptance. Present the verdict + evidence and leave the acceptance to the smoke-test gate's question ("was the functionality met? yes/no"):
- **low** → report pass/fail + evidence; the human confirms at the gate.
- **medium** → same, with an explicit "**review the evidence**" line.
- **high** → you did not run it; the human runs it from the step list and reports.
- **Never flip `qa_done`** — that is the human's flag (set only after a human actually runs the walkthrough).

`Structure: Playwright-MCP accessibility-first execution + assertion-as-verdict / screenshot+trace-as-evidence + console/network gate + determinism levers + delicacy-driven who-runs-it. Evidence-in-repo (never /tmp) = house method.`

## What it does NOT do (invariants)

- Does NOT decide a pass from a screenshot — only from assertions + the console/network gate.
- Does NOT run against prod, nor the sensitive steps of a `delicacy: high` walkthrough.
- Does NOT leave evidence in a temp/scratchpad dir — always `mala-pata/walkthroughs/<slug>/evidence/`.
- Does NOT fake a run when Playwright MCP is missing — it hands the walkthrough to the human.
- Does NOT flip `qa_done`, does NOT commit, does NOT write app code.

## Relation to the family

- **Runner of** `/mala-pata-walkthrough` (describer / runner split, like `mala-pata-organic` / `mala-pata-organic-start`).
- **Twin of** `/mala-pata-seed`: both are executors that run standalone AND are delegated to by the smoke-test gate (`mala-pata-loop-start` 4.1-ter / `mala-pata-organic-start` Step 7) — seed prepares the data, this runs the browser walkthrough.
- The walkthrough's `domain:` is what `/mala-pata-domain-radar` indexes; this skill reads it, does not change it.
