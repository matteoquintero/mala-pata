---
name: mala-pata-organic
description: Generates the kickoff of an ODD (Organic Driven Development) change. It is invoked AFTER the lane has already been decided — normally via `/mala-pata-triage`, or directly when the human already knows it is organic. It assumes route=organic and captures/confirms the strict format (What, Why, Done, Decisions, Risk) — if triage passed a draft, it confirms/completes it instead of starting from scratch. If the format ends up complete, it writes the kickoff inside the repo (`mala-pata/kickoffs/`, versioned) with a one-line pointer in engram. It does NOT run the ODD cycle — the executor is `/mala-pata-organic-start <path-to-kickoff>`. Safety net: if while capturing the fields it turns out that `Decisions` is unresolved, it bounces to `/mala-pata-loop` — but deciding the lane is no longer its primary job. Trigger — "armá el kickoff organic de <cambio>", "generá el kickoff ODD", "ya sé que es organic, prepará el brief".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "3.10.0"
---

# /mala-pata-organic — ODD kickoff generator (route already decided)

User request: **input delivered by the CLI** (or the draft of fields that `/mala-pata-triage` passed when it decided organic)

Your only job is to turn that request into an **ODD kickoff** — a markdown file, saved inside the repo (`mala-pata/kickoffs/`, versioned), that another agent (`/mala-pata-organic-start`) will consume to RUN the cycle. It is to ODD what `/mala-pata-loop` is to SDD: you generate the context, you do not execute it.

> **You assume route=organic.** The lane decision (organic vs loop vs roadmap) is made by `/mala-pata-triage` BEFORE getting here. If you come from triage, you already have a draft of What/Why/Done/Decisions/Risk — your job is to **confirm or complete it**, not re-derive it from scratch. If you were invoked directly (the human already knew it was organic), do the same capture from the raw request.
> **You do NOT execute anything.** You do NOT create the worktree, do NOT explore the code, do NOT write code, do NOT open PRs. You only capture/confirm the format and, if it ends up complete, write the kickoff.
> The result is: (a) the kickoff ready for `/mala-pata-organic-start`, or (b) the safety-net bounce to `/mala-pata-loop` if it turns out Decisions was not resolved, or (c) specific questions if a blocking field is missing.

> **The ODD protocol is the source of truth.** Its 7 steps, the feature-doc, the work-unit commits, RDD per commit and the delivery slicing live in your **global CLAUDE.md** (`## Implementation Routing → ### ODD protocol`). This skill does not duplicate them — the kickoff you generate is the input that `/mala-pata-organic-start` uses to follow them. If CLAUDE.md and this skill differ on ODD mechanics, **CLAUDE.md rules**.

> **Organic uses ODD workers (direct/delegated), NEVER `sdd-*` agents.** gentle-ai's `PreToolUse:Agent` preflight (`gentle-ai sdd-preflight-hook`) only intercepts `sdd-*` dispatches — it applies neither to this skill nor to `/mala-pata-organic-start`. Do not invent a preflight gate here: it does not exist for this lane.

## Requirements (orchestrate, don't reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP and ask to install it, do not start):
  - `gentle-ai` — ODD engine. Install: `brew install gentleman-programming/tap/gentle-ai`.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded):
  - `engram` — persistent memory and continuity pointer. Fallback: continue without the pointer; the kickoff file is the source. Install: ships with gentle-ai (`brew install gentleman-programming/tap/gentle-ai`).

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP, e.g. serena). If a mandatory one is missing, do not continue.

## Hard rules

> **#1 — Safety net, not your primary job: if while capturing `Decisions already made` you realize it is unresolved** (unresolved architecture, a new contract/endpoint left undecided, risk that deserves a full cycle with preview), **do not force organic — bounce to `/mala-pata-loop`**. This is a fallback: normally `/mala-pata-triage` has already filtered this out before you arrive. The size of the change or the file count NEVER forces the loop — ODD handles the small and the **substantial**. **But first distinguish**: if that decision is **decidable with one question** (known options, the human chooses), ask that question and, once resolved, **stay in organic — do NOT bounce**. Bounce to `/mala-pata-loop` ONLY if the decision **needs design** (viable architectures with tradeoffs to research, or options that cannot be known without exploring). The loop discriminator is not "there is a decision", it is "the decision needs design".
> **#2 — Base: propose and confirm, create nothing.** The base comes from WHERE THE CODE TO BE TOUCHED LIVES (`main`/`development`, or an in-progress feature). Propose it with your reason in one line ("the code lives in X") and wait for the OK before fixing it in the kickoff. This skill does NOT create the worktree — `/mala-pata-organic-start` does that with the base already confirmed here. **The working branch is ALWAYS a new `<type>/<change-name>` (never an existing integration branch) and the `worktree` is ALWAYS a new dir per change (`<ABS-repo>-worktrees/<change-name>`) — never put `branch: <integration>` nor `worktree: <reuse/existing>` in the kickoff. The base may be an in-progress feature; the working branch does not replace it (organic-start branches off the base in its own worktree and consolidates on merge).**
> **#3 — The gate is about format, not size.** A 5-line change with concrete What/Done/Decisions passes in a 10-second interaction — one line per field is enough. The gate rejects the UNDER-specified, not the short. If you are asking for more than one line per field for a small change, you are rebuilding SDD inside organic: stop.
> **#4 — Absolute paths ALWAYS** in any command you show or leave in the kickoff (`worktree:` is a proposed absolute path, never relative).

## Phase 0 — Authorize (ODD step 1, read-only guard)

Does the request authorize a **change**? Investigation, explanation, review, audit, comparison, or proposal/planning = **read-only** unless the human asks to implement or another explicit mutation.
- Read-only → inspect/explain/recommend, but do **NOT** generate a kickoff, do NOT propose a worktree, do NOT advance phases.
- Ambiguous or conditional intent → 1 question and stay read-only until the answer.

If the request authorizes a change, proceed to the gate.

## Phase 1 — Capture/confirm the strict format (kickoff input, not the routing)

The lane is already decided (route=organic) — this is no longer the gate that chooses between organic/loop/roadmap, `/mala-pata-triage` already did that. Here you **collect/confirm** the fields that will go in the kickoff. If `/mala-pata-triage` passed you a draft, you start from there and confirm with the human instead of inferring from scratch:

| Field | Blocks | What it tests |
|---|---|---|
| **What** | YES | Objective = concrete, observable behavior/result. "Improve X" with no concrete target → FAILS. |
| **Why** | NO | Motivation in 1 line. Always asked, never blocks — but it FLOWS into the feature-doc and the PR body. |
| **Done** | YES | Testable definition = the WHEN: "when X, Y happens" or the check that proves it. |
| **Decisions already made** | YES | The approach/architecture is DECIDED or obvious. |
| **Risk** | NO (optional) | Blast radius in one line. |
| **Where** | NEVER blocks | It is an OUTPUT of the Explore phase of `/mala-pata-organic-start`, not a precondition — in ODD you explore first. The human may leave an optional hint, but it never blocks. |

### What to do with the result

- **What + Done + Decisions concrete (confirmed)** → generate the organic kickoff (Phase 2).
- **Any of the three still "don't know" on confirming** → do NOT generate a kickoff:
  - **Decisions fails** (it is only discovered here that the architecture was not resolved) → safety net, Hard rule #1 → bounce to **`/mala-pata-loop`** (SDD, with preview and formal design) (unless that decision is **decidable with one question**: ask the question and, once resolved, stay in organic — loop only if it needs design).
  - **What/Done are clear but the scope is huge or crosses several loops** → recommend **`/mala-pata-roadmap`** (decompose first).
  - **Only Where is "don't know" and the rest is clear** → it is NOT a reason to bounce — it is normal organic, you will explore in `/mala-pata-organic-start`.

### Proportionality (non-negotiable, Hard rule #3)

A small change = one line per field, ~10 seconds to fill. The gate does not ask for a paragraph per field — it asks that each blocking field have **concrete content**, whether long or short. Do not inflate the kickoff of a 5-line fix with sections that add nothing: that rebuilds SDD inside organic and kills its fast lane.

## Phase 2 — Generate the organic kickoff (if the capture ended up complete)

1. `change-name`: if the incoming draft carries a `change_name` (a roadmap phase slug), HONOR it as-is — do NOT derive a new one (the branch `<type>/<slug>` must match what `mala-pata-roadmap-radar` searches for). Only when `change_name` is absent, derive a short one in kebab-case.
2. **Base — propose and confirm (Hard rule #2)**: where the code lives (`main`/`development` or an in-progress feature). Wait for the OK.
3. **Branch type — advise and confirm**: `feature/`/`fix/`/`hotfix/`/`refactor/`/`chore/`/`docs/` — never `sdd/`. The full name goes as the proposed `worktree` (absolute path, `<ABS-repo>-worktrees/<change-name>`) — you do **not create it here**, `/mala-pata-organic-start` executes that.
4. **Init guard**: `mem_search("sdd-init/{project}")` (only the EXACT item). If it does not exist → run `sdd-init` first to detect the stack and `strict_tdd`. Take `tdd_mode` from there for the frontmatter.
5. **Idempotency**: `mem_search("odd/<change-name>/kickoff")`. If one equal/similar already exists → offer to update or rename.
6. Build the kickoff with this structure (same persistence mechanism as `/mala-pata-loop` — see Phase 3):

```markdown
---
change_name: <change-name>
project: <project>
route: organic
base: main|development|<feature-en-curso>   # confirmed with the human — Hard rule #2
branch: <type>/<change-name>                # type confirmed — never sdd/
worktree: <proposed absolute path>          # <ABS-repo>-worktrees/<change-name> — organic-start creates it, not this skill
tdd_mode: <strict|standard>                  # from sdd-init/<project>
smoke_test:                                  # does it need manual testing with seeded data after apply? (organic-start confirms)
  needed: auto                               # auto|yes|no — auto = organic-start proposes and the human confirms
  data: <scenario/data to seed, or "a definir">
created_at: <ISO 8601>
---

# Kickoff ODD: <change-name>

## What
<concrete, observable objective — one line if the change is small>

## Why
<motivation in 1 line — flows into the feature-doc and the PR>

## Done
<testable definition — "when X, Y happens" or the check that proves it>

## Decisions already made
<approach/architecture decided or obvious — confirm it, do not re-decide it>

## Risk
<blast radius in 1 line — optional, "N/A" if it does not apply>

## Where (optional hint — to be discovered in Explore)
<file(s)/module if the human already knows, or "a determinar en Explore">
```

(The section headings and frontmatter keys in the template are fixed identifiers read by `/mala-pata-organic-start` and stay as written; only the `<...>` placeholders and comments are prose.)

**`smoke_test` field**: capture early whether the change is likely to need a manual test with seeded data after apply (gate of `organic-start`, Step 7 / 4.1-ter). Default `needed: auto` — `organic-start` proposes yes/no based on the shape of the change and the human confirms; set `yes`/`no` only if you already know. In `data`, one line with the scenario to seed, or "a definir". The seed uses the project's mechanism and runs against the test DB.

## Phase 3 — One-line pointer in engram

Same as `/mala-pata-loop` (Step 5): the kickoff lives in a **file**, not in engram — so it is never pushed to the repo by accident.

1. **Location — inside the repo, versioned (traceability)**: `mala-pata/kickoffs/<change-name>.md` (relative to the repo root, `git rev-parse --show-toplevel`; `mkdir -p` if it does not exist).
2. Write the full kickoff from Phase 2 to `mala-pata/kickoffs/<change-name>.md`.
3. **Lightweight pointer in engram**: `mem_save` with `topic_key: "odd/<change-name>/kickoff"`, `type: "architecture"`, **single-line** content: `Kickoff ODD in file: <absolute path>`. Do not duplicate the content here — the file is the sole source of truth.
4. If engram is unavailable, the file is still the source of truth — warn in one line that the pointer was not saved (it affects future idempotency, not the kickoff itself).

## Phase 4 — Does NOT execute · mandatory close (summary + kickoff)

Your reply to the human is a **MANDATORY and standard close (summary + kickoff)** — it is not optional nor "just the path". The whole summary comes from the kickoff you just wrote, without inventing anything. Emit exactly this structure (same format as `/mala-pata-loop` Step 5):

- Title: `**Kickoff ready — <change-name>**`
- Summary (one line per item):
  - **What:** <one line>
  - **Lane:** organic
  - **Base → branch:** <base> → <type>/<change-name>
  - **Worktree:** <absolute path>
  - **DoD:** <testable criterion, one line>
- **Kickoff:** `<absolute path of the .md>`
- **Next step** (in a code block, copy-paste):

  ```
  /mala-pata-organic-start <absolute path of the .md>
  ```

Emit the field labels above (Kickoff ready, What, Lane, Base → branch, Worktree, DoD, Kickoff, Next step) **verbatim in English** — they are structural; only the values and any surrounding prose follow the conversation language.

This block is the ONLY way to close on the happy path.

**Only exceptions** (when the reply is not just that):
- Phase 0 read-only → stay in read mode, no kickoff.
- A blocking field is still unresolved on confirming → one line with the field that failed + the recommendation (`/mala-pata-loop` or `/mala-pata-roadmap`), without creating a kickoff.
- Confirmation of base/branch type (Phase 2, points 2-3) → the only question allowed before writing the kickoff.
