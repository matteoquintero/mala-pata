---
name: mala-pata-loop
description: Reinterprets a request into technical terms, chooses an execution profile with the human, and generates the full context in a markdown file (inside the repo, `mala-pata/kickoffs/`, versioned) to start an interactive SDD — with only a one-line pointer in engram. It does NOT run the SDD — it only leaves the brief ready for another agent to run it.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.9.0"
---

# /mala-pata-loop — Context generator to start an SDD

User request: **input delivered by the CLI**

Your only job is to turn that request into a **COMPLETE TECHNICAL CONTEXT saved in a markdown file** inside the repo (`mala-pata/kickoffs/`, see Step 5) that another agent will consume to RUN an SDD.

> **You do NOT start the SDD. You do NOT write code. You do NOT create real specs/tasks/migrations. You do NOT run tests.**
> You only produce the *brief* (context) and persist it in a file (with a one-line pointer in engram so it can be searched). When you finish, the SDD is **ready to start**, not started.

> **When you are on the right lane (border with organic).** You arrive at `/mala-pata-loop` when you **cannot start coding yet because DESIGN is missing** — typically because the `/mala-pata-organic` gate diagnosed unresolved `Decisions already made` (an architecture fork, a contract/endpoint whose *shape* must be decided, disputed requirements). **Size alone NEVER sends you here**: a large but specifiable change (you can fill in What + Done + Decisions) goes to `/mala-pata-organic`; one bigger than a single cycle goes to `/mala-pata-roadmap`. If on reading the request you already know what to build and the architecture is decided, this is NOT loop — send it back to `/mala-pata-organic`.

---

## Requirements (orchestrate, don't reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Required** (no fallback — if missing, STOP and ask for it to be installed, do not start):
  - `gentle-ai` — SDD engine. Install: `brew install gentleman-programming/tap/gentle-ai`.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded):
  - `engram` — persistent memory and continuity pointer. Fallback: continue without the pointer; the brief in the file is the source. Install: ships with gentle-ai (`brew install gentleman-programming/tap/gentle-ai`).

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP, e.g. serena). If a required one is missing, do not continue.

## Base rules and profiles

This skill relies on two layers of rules — the generated kickoff **MUST** inject both so the executor has them at hand:

- **Base rules (universal)**: `references/profiles/_base.md` — method invariants (Phase 0, TDD, verify, engineering principles) + universal conventions for commits, branches, paths, authorship attribution.
- **Active profile rules**: one of `references/profiles/{full,standard,lite,minimal}.md` — adjusts TDD granularity, verify depth, spec+design merging, explore reuse, human gate of Phase 0.

**Stack tools, project-specific conventions and concrete contracts** do NOT live here — `sdd-init` detects them and they live in engram as project context (`sdd-init/<project>`) or in the change's kickoff.

---

## Step 0 — Vagueness gate + Definition of Ready (light DoR)

Before reinterpreting anything, measure whether the request is **ready to enter the cycle** (Definition of Ready). It is not a new phase or a separate artifact — it is this same gate, sharpened. The idea, taken from proven practices (Example Mapping / "Three Amigos" and INVEST's *Testable* criterion), is simple: **a poorly defined objective must NEVER start the cycle** — it is infinitely cheaper to stop it here than to discover it in preview.

### Two readiness checks

**1. Red cards (unanswered questions about the WHAT).** A red card is any open question about *what is wanted* — NOT about *how it is implemented* (that gets resolved in Design, not here). Examples of reds: "does this also include X?", "is the objective A or B?", "what about case Y?". Rule:
- **0 reds** → the WHAT is clear, continue.
- **1–2 reds** → ask those concrete questions and wait ("Recoverable" level below). Do not invent the answer.
- **3+ reds, or a single red that changes the whole objective** → the objective is NOT defined. Do NOT generate context: send the request back to definition (answer as "Too vague", listing the reds). Putting this into the cycle with the reds open is exactly what later makes the human and the preview end up debating the objective in the wrong phase.

**2. Testable DoD (INVEST's *Testable* criterion).** The "when is it done" has to be writable as something **verifiable**, not a wish. Quick test for each criterion: *could someone other than you objectively say whether it was met or not?*
- "make it work well", "keep it tidy", "make it fast" → NOT testable → it is a red card (the real criterion is missing).
- "the endpoint responds in <200ms at p95", "the user can filter by date and see the result without reloading" → testable → OK.
- If the "done" cannot be made testable even by asking 1–2 things → treat it as an undefined objective (Too vague).

### Resolution (the usual three levels, now with the two checks inside)

- **Actionable** — 0 reds and testable DoD (or at most 1 minor piece of data missing) → proceed straight to Step 1.
- **Recoverable** — 1–2 reds, or the DoD becomes testable with 1–2 questions → ask **those concrete questions** and wait. Do not invent scope.
- **Too vague** — the object itself is missing ("improve the app", "make it better"), or 3+ reds, or the "done" cannot be made testable → **do NOT generate context.** Answer exactly:

  > **vague work ** — I need at least: *what* you want to achieve, *where* (module/feature) and *when it is done* (in verifiable criteria, not "make it look good"). [If there are concrete red cards, list them here as bullets.] With that I'll build the context.

  And stop there. Do not reinterpret or guess.

---

## Step 1 — Reinterpret into technical terms

1. Detect the **active project** (the available memory tool or the cwd) and read its architecture (`CLAUDE.md`, `ARCHITECTURE.md` or equivalents).
2. `mem_search` with keywords from the request (and `mem_get_observation` for what is relevant). Reuse existing decisions/conventions.
3. Explore the minimum of the code to ground the reinterpretation (grep/reading). Do not edit anything.
4. Rewrite the request as a **technical objective**: Objective, Problem/root cause, Scope IN, Scope OUT, measurable Success criteria, `change-name` in kebab-case. If the incoming draft carries a `change_name` (a roadmap phase slug), HONOR it as the change-name — do NOT derive a new one (the branch `<type>/<slug>` must match what `mala-pata-roadmap-radar` searches for); derive only when it is absent.
5. **Idempotency**: `mem_search("sdd/<change-name>/kickoff")`. If one that is equal/similar already exists → offer to update it or rename.
6. **Size / splitting guard**: one SDD = one coherent objective. If it spans several, recommend splitting into N SDDs (with a dependency graph) and generate only the first.
7. **In-flight conflict**: `git worktree list` + active branches. If there is overlap → warn and confirm before continuing.
8. **Base branch + branch type — ALWAYS proposed and confirmed with the human** (see `references/profiles/_base.md`):
   - **Base**: propose it with your reason — default `main`/`development` (integration), or another branch if the work builds on a feature in progress ("the code lives in X"). Any branch is valid with confirmation; what is forbidden is assuming it silently or blocking just because it is not main.
   - **Branch type**: advise the conventional prefix according to WHAT the change is (`feature/` new functionality, `fix/`/`bugfix/` correction, `hotfix/` prod urgency, `refactor/`, `chore/`, `docs/`, `release/`) and propose the full name `<type>/<change-name>`. **Never `sdd/...`**. E.g.: a bug fix → proposal `fix/<change-name>`; a new feature → `feature/<change-name>`.
   - **Wait for the OK** before setting `branch:` and `branch_base` in the kickoff. These two confirmations can go together with the profile one (Step 1.5) in a single interaction. The working branch is ALWAYS the new `<type>/<change-name>` and the `worktree` is ALWAYS a new dir per change — never put an integration branch as `branch:` nor a worktree to reuse; the executor (loop-start) works isolated in its own worktree and consolidates at merge.

---

## Step 1.5 — Choose execution profile (human gate)

Estimate the **size** of the change and **propose a profile** based on:

- How many containers, services, types, tests it touches.
- Whether the module was explored recently (an `sdd/<...>/explore` of the same module exists in engram).
- Whether there are genuinely new UI components (not just adaptations).
- Whether there is a new BE contract (endpoints, migrations, shape change).
- Regression risk in critical flows.

The 4 available profiles:

| Profile | When | Approx cost |
|---|---|---|
| **FULL** | L change, first step in the module, new BE contract, high risk | ~500K tokens |
| **STANDARD** | Typical M change, known module, additive on an existing contract | ~250K tokens |
| **LITE** | S/M change in a hot module, adapts atoms/molecules | ~120K tokens |
| **MINIMAL** | Small fix, mechanical refactor, type migration | ~70K tokens |

Present the proposal to the human with **the interactive question function available in the CLI**:

- **Question**: "Which profile do we use for this SDD?"
- **Options**: the 4 profiles with a short description (one line each).
- **Recommendation** (label it "(Recommended)" and put it as the first option): the one matching your estimate.
- In the reasoning, write a short line explaining **why you recommend that profile** (e.g.: "module `X` already explored this week, no new components, additive change → LITE").

**Do not continue** until the human confirms. If they choose "Other", take their answer as the profile (validate that it is one of the 4).

---

## Step 2 — Choose skills ACCORDING TO THE OBJECTIVE (focused, not a fixed list)

The executor will load exactly the skills this kickoff lists — so choose them **by the objective's Scope IN**, not "just in case". Few and precise > many and generic (an inflated set makes the agent slower and burns tokens without improving the result).

### Method base (engineering engine)

- **Always** (apply to any code): `clean-architecture`, `solid`.
- **If the objective touches backend/domain logic** (not for a purely visual/static change): + `clean-ddd-hexagonal`, `design-patterns`.

### Conditionals by domain — choose ONLY those signaled by the objective

| Signal in the objective (Scope IN) | Skills to load |
|---|---|
| **DB**: schema, migration, query, data model, indexes | `database-design` |
| **UI/frontend**: screen, component, form, user flow | `ui-ux-pro-max`, `heuristic-evaluation` |
| New **visual design** / redesign / branding / "so it doesn't look like AI" | `frontend-design`, `impeccable` |
| **Color / tokens / palettes** | `color-expert` |
| **Animation / micro-interaction / transition / scroll** | `motion-design` (+ `gsap-*` / `threejs-*` **only if the stack uses them**) |
| **Diagrams** of architecture/flow/states | `archify` or `diagram-design` |
| **Charts / dashboards / data viz** | `dataviz` |
| **Docs** for humans (runbook, guide) / test doc or customer doc | `cognitive-doc-design` / `mala-pata-walkthrough` |
| **RAG / search / embeddings** | `rag-architect`, `rag-retrieval`, `hybrid-search-implementation` |
| **LLM app / agents / prompts / tools** | `llm-app-patterns`, `prompt-engineering-patterns`, `ai-engineer`, `multi-agent-patterns`, `tool-design` |
| **Model evaluation / LLM-judge / metrics** | `advanced-evaluation`, `evaluation`, `evolutionary-metric-ranking` |
| **Agent memory / cross-session persistence** | `memory-systems` |
| **Large system design / build-vs-buy / decomposition** | `software-architect` |
| **Security / vulnerability review** | `security-review` |
| **Library/framework/API** (setup, version, syntax) | `context7` (it is already a global rule — name it in the kickoff if it is central to the objective) |

### Selection rules (non-negotiable)

1. **By objective, not by reflex**: if the Scope IN does not mention it, do not load it. E.g.: a query fix does NOT load `ui-ux-pro-max`; a screen redesign does NOT load `rag-*`.
2. **Ceiling ~3-4 conditionals.** If you end up with more, the objective is probably too big → split it (Step 1.6), do not load everything.
3. **Every chosen skill goes in the kickoff** (section "Additional conditional skills") **with ONE line of why** (which part of the objective justifies it). The executor loads that list literally.
4. **Only skills that EXIST** in the session (look at `<available_skills>`); never invent a name. Some are plugin skills → use the `plugin:skill` name exactly as it appears in the listing. The stack-specific ones (`gsap-*`, `threejs-*`, `go-testing`, `neon-postgres`) only if `sdd-init` confirms the stack uses them.

**Init guard**: `mem_search("sdd-init/<project>")`. If it does NOT exist → run `sdd-init` to detect stack, conventions, testing, `strict_tdd`. If it already exists → reuse it (it is what tells you which stack-specific ones apply).

---

## Step 3 — Migration number: provisional for the author, final at merge (if applicable)

If the change needs DB migrations, **do NOT reserve a number as a lock**. The source of truth for numbers ALREADY taken is **git, not engram** — a reservation registry is a lock that long-lived branches do not respect and that also drifts (it was seen saying "next free 0071" when the real one was 0003). Instead:

1. **Measure git, not a registry**: look at which numbers the base branch AND the sibling in-flight branches occupy — with the project's command to list migrations (e.g. `git ls-tree -r --name-only <branch> -- <migrations-folder>`; the exact folder and scheme are known by `sdd-init`). **Never infer the next one by counting files on disk** (numbering may not be contiguous).
2. **Take the next free one as PROVISIONAL**: it is the number you will write the file with and run the round-trip, but it is **not final** — if another sibling branch merges first, this change renumbers when integrating (see `/mala-pata-loop-start`, Step 4.1-bis). Project rule: "the first to merge keeps it".
3. **Record it in the kickoff as provisional-in-dispute, not as a reservation**: in `migrations_reserved` in the frontmatter put the provisional number + the note "final at merge; 1st to merge keeps it; re-verify against siblings right before the merge". If several branches are fighting for the same number, list them.
4. **HOW to renumber belongs to the stack, not here**: if the project uses a migrator with chained state (journal/snapshots, e.g. drizzle-kit), renumbering is **NOT renaming files — it is regenerating**. That detail lives in `sdd-init/<project>` / the repo's `CLAUDE.md`, not in these rules.

If it does not need migrations, leave it explicit ("N/A") in the kickoff.

---

## Step 4 — Build the kickoff

The kickoff is a **markdown file**, not an engram entry — no practical length limit, so be as detailed as the change requires. The section order is deliberate, not just aesthetic: **context/background goes first, the request/instruction goes last**. This is the practice documented by Anthropic for long prompts mixing reference + instruction — "queries at the end can improve response quality by up to 30%, especially with complex, multidocument inputs" ([Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)). Do not reorder the sections even if another order seems tidier to you.

Assemble the brief with this structure, **INJECTING** the rules MDs:

```markdown
---
change_name: <change-name>
profile: <PERFIL>
project: <project>
branch: <type>/<change-name>   # confirmed type (feature|fix|hotfix|refactor|chore|docs|release) — never sdd/
branch_base: main|development
worktree: <suggested absolute path>
depends_on: <change-name(s)|none>
parallelizable_with: <change-name(s)|none>
migrations_reserved: <provisional number(s) + "final at merge; first to merge keeps it"|N/A>
smoke_test:                 # does it need manual testing with seeded data after apply? (confirmed by loop-start, Step 4.1-ter)
  needed: auto             # auto|yes|no — auto = loop-start proposes and the human confirms
  data: <scenario/data to seed, or "a definir">
sdd_preflight:              # recommendations the runner (loop-start) uses as the default of the hook's canonical question
  pace: interactive        # interactive|automatic — FULL/STANDARD => interactive; LITE/MINIMAL may be automatic
  artifacts: engram        # engram|openspec|hybrid — default engram for this user
  pr_strategy: ask-on-risk # ask-on-risk|single-pr|auto-chain — default ask-on-risk
created_at: <ISO 8601>
---

# Kickoff: <change-name>

<!-- ===== CONTEXT — read this before the request. It is reference material. ===== -->

## Method rules
- Base (universal): `references/profiles/_base.md`
- Active profile (**<PERFIL>**): `references/profiles/<perfil>.md` — reason: <one short line explaining why this profile>. Order-of-magnitude cost: ~<N>K tokens.

## Project context
`sdd-init/<project>` — engram #<id> (stack, testing, conventions already detected; do not repeat them here).

## Startup command
The COMPLETE and executable command that creates the environment (worktree off the base branch + config/deps symlinks of the stack). `loop-start` runs it AS IS, without deciding anything — if missing, the executor STOPS (Hard rule #2 of loop-start).

```bash
# Branch = the confirmed <type>/<change-name> (frontmatter `branch:`) · worktree dir = <change-name> (no prefix) · never sdd/
git -C <ABS-repo> worktree add <ABS-repo>-worktrees/<change-name> -b <branch> <branch_base>
ln -s <ABS-repo>/.env <ABS-repo>-worktrees/<change-name>/.env && ln -s <ABS-repo>/node_modules <ABS-repo>-worktrees/<change-name>/node_modules
# (adjust symlinks to the project's real stack)
```

## Change contract
- Endpoints, shapes, types, migrations (if BE has an associated delivery).
- Refs to previous artifacts (BE kickoffs, decisions in engram).

## Technical reinterpretation
- Objective:
- Problem / root cause:
- Scope IN:
- Scope OUT:

## Architecture and affected layers
- Project BCs/layers + refs to ARCHITECTURE.md.

## Additional conditional skills (Step 2)
- List of skills loaded according to domain (UI, RAG, LLM, etc.).

## Risks / open decisions
- List to resolve within the SDD (Design is where they are resolved with the human, not here).

<!-- ===== THE REQUEST — goes last on purpose. It is the instruction the executor carries out. ===== -->

## High-level phase plan
- Phase 0 (if it touches UI): REUSES/ADAPTS/NEW audit + Storybook + human gate according to profile.
- Phase 1..N: coherent objectives, NOT tasks (those are produced by `sdd-tasks`).

## Definition of Done
Verifiable criteria, not vague bullets — use Given/When/Then for observable behavior, add the procedural part of the method below:

- [ ] Given <initial state>, When <user/system action>, Then <observable and verifiable result>.
- [ ] (repeat one item per real success criterion of the request — the one you defined in "Technical reinterpretation")
- [ ] All tasks with TDD green according to the profile's granularity.
- [ ] Verify passes according to the profile's depth.
- [ ] PR opened against the base branch, no direct push to integration.
- [ ] Kickoff referenced in the PR body (file path — see Step 5).
```

The kickoff MUST include the full frontmatter and the "Method rules" block with the paths to the MDs — the executor reads them at startup. Those `references/profiles/...` paths are relative to the `mala-pata-loop` skill directory (not the repo); `/mala-pata-loop-start` resolves them against the installed skill dir. Do not compress the Definition of Done so that it "fits": there is no longer a character budget, use the space the change needs.

`sdd_preflight` are only RECOMMENDATIONS — they do NOT satisfy gentle-ai's preflight hook (which requires a real, live `AskUserQuestion` in the runner's session); `mala-pata-loop-start` reads them to pre-fill the recommendation text of the hook's mandatory canonical question. Derive `pace` from the profile: FULL/STANDARD → `interactive`; LITE/MINIMAL may go `automatic`.

**`smoke_test`** captures early whether the change will probably need manual testing with seeded data after apply (`loop-start` gate, Step 4.1-ter). Default `needed: auto` — `loop-start` proposes yes/no according to the shape of the change and the human confirms; put `yes`/`no` here only if you already know. In `data`, one line with the scenario to seed (e.g. "an order in DRAFT state with 2 items"), or "a definir". The seed always uses the project's mechanism and runs against the test DB.

---

## Step 5 — Persist and respond (mandatory closing: summary + kickoff)

The kickoff lives in a **file, not in engram** — so it is never pushed to the project repo by accident, and it does not have the practical length limit of an engram observation. This is specific to the kickoff: the rest of the cycle (explore, propose, spec, design, tasks, preview, apply-progress, verify-report, archive-report) keeps persisting in engram exactly as always — do not touch it.

1. **Location — inside the repo, versioned (traceability)**: `mala-pata/kickoffs/<change-name>.md` (relative to the repo root, `git rev-parse --show-toplevel`; `mkdir -p` if it does not exist).
2. Write the complete kickoff from Step 4 to `mala-pata/kickoffs/<change-name>.md`.
3. **Light pointer in engram** (only so `mem_search`/radar keep finding it — the idempotency of Step 1 point 5 depends on this): `mem_save` with `topic_key: "sdd/<change-name>/kickoff"`, `type: "architecture"`, **single-line** content: `Kickoff in file: <absolute path>`. Do not duplicate the kickoff's content here — the file is the only source of truth.
4. If you reserved migrations, confirm that the registry was updated.
5. **Your response to the human is a MANDATORY, standard closing (summary + kickoff)** — it is not optional nor "just the path". The whole summary comes from the kickoff you just wrote, inventing nothing. Emit exactly this structure:

   - Title: `**Kickoff listo — <change-name>**`
   - Summary (one line per item):
     - **What:** <one line>
     - **Profile:** <FULL/STANDARD/LITE/MINIMAL>
     - **Base → branch:** <base> → <type>/<change-name>
     - **Worktree:** <absolute path>
     - **DoD:** <testable criterion, one line>
     - **Migration / Phases:** <reserved migration if applicable> · <n> phases
   - **Kickoff:** `<absolute path of the .md>`
   - **Next step** (in a code block, copy-paste):

     ```
     /mala-pata-loop-start <absolute path of the .md>
     ```

   This block is the ONLY way to close on the happy path.

**Only exceptions** (when the response is NOT the closing block):
- Vagueness gate → answer `vague work ` (Step 0).
- Idempotency / in-flight conflict → a one-line warning + the question, before creating.
- Step 1.5 and Step 1.8 → the interactive question function available in the CLI to choose the profile and confirm the base branch (ideally in a SINGLE interaction; they are the only questions allowed before the kickoff).
- Engram not available for the pointer → the file is already the source of truth, continue anyway; warn in one line that the pointer was not saved (it affects future idempotency, not the kickoff itself).
