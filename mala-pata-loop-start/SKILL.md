---
name: mala-pata-loop-start
description: Starts and runs the SDD CYCLE from the path of the kickoff file that /mala-pata-loop left — explore → propose → spec → design → tasks → preview → apply → verify → archive, one phase at a time (sequential, spec and design NOT in parallel), interactive with a gate per phase. Preview is a MANDATORY human gate between tasks and apply (plain-language walkthrough + anti-duplication). The init is guaranteed by /mala-pata-loop (once per project). Planning goes BEFORE touching code. The brief is input to the cycle, NOT an order to implement directly. Trigger — "arrancá el SDD de este kickoff", "corré el ciclo de <kickoff.md>", "/mala-pata-loop-start <ruta>".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.10.0"
---

# /mala-pata-loop-start — Runs the SDD CYCLE from a kickoff file

Kickoff: **input delivered by the CLI**

Your job: read the *kickoff* that `/mala-pata-loop` left and **run the COMPLETE SDD CYCLE, phase by phase, ONE AT A TIME (sequential, never in parallel)**:

`explore → propose → spec → design → tasks → preview → apply → verify → archive`

(The *init* —once per project— was already guaranteed by `/mala-pata-loop`. The *explore* here **goes deeper into the real code of the worktree**; the kickoff was only the high-level reinterpretation.) Each phase closes with **summary + PAUSE** waiting for OK before the next one. All the planning (explore→propose→spec→design→tasks) goes **before** writing a single line of code.

> **Hard rule #1 — do NOT implement directly.** It is forbidden to write code, migrations or create implementation files **before the PREVIEW is approved** (the final gate before code: tasks first, then preview). The brief's "phase plan" is material for the Tasks phase, NOT the signal to start coding. If you catch yourself exploring in order to "go solving the task", stop: you are skipping the cycle.
> **Hard rule #2 — ALWAYS your own worktree + your own new branch, even if the brief says to reuse.** The cycle runs in a worktree DEDICATED to this change, on a NEW branch `<type>/<change-name>` created off the `branch_base`. **NEVER in-place on an integration/shared branch, NEVER reusing another feature's worktree — even if the brief's startup command points to an existing worktree or uses an integration branch as the working branch.** If the brief says that, it is WRONG: override — create a fresh worktree of your own off the base with a new branch `<type>/<change-name>`, and warn in one line that you corrected the brief. The `branch_base` does come from the brief as is (it may be `main`/`development` or a feature in progress — you branch off it and consolidate at merge in the closing). From the brief's startup command you reuse the base and the symlinks (`.env`/`node_modules`), not the worktree nor the working branch. **Only valid reuse**: THIS change's OWN worktree (same change-name) on a resume. The only lane that works WITHOUT a worktree is `/mala-pata-shot`. If the brief does not bring base/symlinks, STOP and ask the orchestrator for it.

> **Stack-agnostic.** The concrete examples in this command (`.env`, `node_modules`, `npm`, `TEST_DB_URL`, Storybook, `gh`) are from the Node/Postgres/GitHub stack. **Map them to the project's real stack** (test environment/DB, dependency manager, config/secrets files, component workshop, PR host according to what the project uses). The project's convention rules over any example.

> **Hard rule #3 — there is EXACTLY ONE mandatory preflight gate: gentle-ai SDD's canonical preflight (3 questions), asked ONLY ONCE in Step 2 (new sub-step, see Step 2.9), in the interactive root/parent session, BEFORE the first dispatch of an `sdd-*` Agent.** It is not optional nor discretionary for this skill: since gentle-ai 3.7, the `PreToolUse:Agent` hook (`gentle-ai sdd-preflight-hook`) **rejects every `sdd-*` dispatch** if it does not find, in the live transcript of the current session, a real, byte-exact `AskUserQuestion` already answered by the human — neither the kickoff, nor engram, nor any state on disk satisfies it. mala-pata's opinionated preferences (interactive pace, artifacts in engram, PR ask-on-risk) are still carried, but now as the **recommendation** inside the text of each question (taken from the kickoff's `sdd_preflight` block) — the human still chooses, because the hook demands a real answer and the labels/order of the options are fixed by gentle-ai (they cannot be annotated or reordered, see Step 2.9). The other human interactions of the cycle stay the same: base branch confirmation (Step 2.2) and PR/merge destination (Step 4). **RDD still does not run in the SDD cycle** — it belongs to the organic/ODD lane (see `mala-pata-organic`), so there is no receipt gate here. No additional PRE-CYCLE gates beyond these three (canonical preflight, base branch, PR/merge destination) — if you think of building an additional selection menu before starting the cycle, it is a sign that you are adding something outside this skill. The in-cycle gates (preview, smoke, cleanup, migration, conflict) are legitimate and unaffected.

> **Hard rule #4 — the objective is defined BEFORE preview, never IN preview. Debate alarm.** Preview exists to review **whether what is going to be done is right**, NOT to discuss **whether the objective is right** — the WHAT already had to be closed in explore/propose/spec. During the planning phases (explore→spec), if you notice that the WHAT is **being debated a lot** — questions about the objective keep coming back, the scope moves, "and this too?" questions appear that do not close, or the same decision is re-discussed more than once — that is the signal that **the objective was not well defined** (red cards that slipped through `/mala-pata-loop`'s gate, see its Step 0). Do NOT keep pushing forward: **send the cycle back to explore or propose** to fix the WHAT again, and only when it is closed do you continue. An objective with the WHAT still under discussion **CANNOT reach preview**. This is not re-running phases for fun — planning on a moving objective guarantees throwing the plan away later.

## Requirements (orchestrate, don't reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Required** (no fallback — if missing, STOP and ask for it to be installed, do not start):
  - `gentle-ai` — `sdd-*` agents. Install: `brew install gentleman-programming/tap/gentle-ai`.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded):
  - `codegraph` — code graph (anchoring and structure). Fallback: grep/Read. Install: global npm CLI; per-project init with `gentle-ai codegraph init --cwd <repo>`.
  - `serena` — symbol-level navigation and editing. Fallback: codegraph/grep. Install: `uv tool install -p 3.13 serena-agent && serena setup claude-code`.
  - `engram` — persistent memory and continuity pointer. Fallback: continue without the pointer; the brief in the file is the source. Install: ships with gentle-ai (`brew install gentleman-programming/tap/gentle-ai`).

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP, e.g. serena). If a required one is missing, do not continue.

## Step 1 — Load the brief

**Current format (default)**: `input delivered by the CLI` is an **absolute path to a `.md` file** (the one `/mala-pata-loop` writes to `mala-pata/kickoffs/<change-name>.md`, inside the repo).

1. If the input is an absolute path (starts with `/`) → `Read` directly on that file. If the file does not exist → **STOP** and ask for the correct path. Do not invent the context.
1.5. **Method-rules paths**: the kickoff's "Method rules" section lists `references/profiles/_base.md` and `references/profiles/<perfil>.md`, relative to the `mala-pata-loop` skill directory. Resolve them against the installed skill dir (e.g. `~/.agent-skills/mala-pata-loop/references/profiles/` or `~/.claude/skills/mala-pata-loop/references/profiles/`), not against the cwd/worktree, and `Read` them.
2. Read the frontmatter (change_name, profile, project, branch, branch_base, worktree, depends_on, parallelizable_with, migrations_reserved) and the WHOLE body: method rules, project context, contract, technical reinterpretation, architecture, conditional skills, **open decisions**, phase plan, Definition of Done.

**Legacy format (kickoffs created before this change — only for compatibility, do not use it for new kickoffs)**: if the input is NOT an absolute path, it may come as **(a)** an engram id (`#1234` or `1234`), **(b)** a topic_key (`sdd/<change-name>/kickoff`), or **(c)** the old combined format `sdd/<change-name>/kickoff · engram #<id>`.
3. With `#<number>` (cases a/c) → `mem_get_observation(id: <number>)` DIRECTLY, never `mem_search`.
4. With a pure topic_key (case b) → `mem_search` by the topic_key → `mem_get_observation`. If what it returns is the **new light pointer** (`Kickoff in file: <path>`) instead of the full content → follow that path and go to point 1.
5. **One-shot auto-migration**: if through the legacy route you obtained the FULL content from engram (pre-migration kickoff), write it to the new format (`mala-pata/kickoffs/<change-name>.md`) and update the engram observation to the one-line pointer — that way that kickoff is migrated and next time it enters through the normal route. Then continue with that file.
6. If nothing is found → **STOP** and ask for the correct identifier.

**Resuming an SDD paused in Preview**: as soon as the brief is loaded, check `mem_search("sdd/<change-name>/state")`. If the EXACT item says `paused-at-preview` (left by `sdd-preview`'s "Stop" gate) → do NOT re-run the planning phases: do the Step 2 preflight and jump DIRECTLY to the Preview gate (Step 3, phase 6) re-presenting the already-persisted `sdd/<change-name>/preview` artifact. `/sdd-continue` (a gentle-ai command) does NOT know the preview phase — the resume goes through here. If instead the EXACT item says `objective-not-ready-at-preview` (objective bounce from the preview, see Hard rule #4 and `sdd-preview`) → the WHAT was left open: **do NOT jump to preview**; do the preflight and **re-enter through explore/propose** to redefine the objective before advancing again.

## Step 2 — Preflight + environment preparation (following the brief, without deciding)
1. **Are you already in the brief's worktree?** `git branch --show-current`. If it matches the brief's branch → jump to point 5.
2. **Base branch confirmation — ALWAYS ask before creating the worktree**: the brief carries the base in its frontmatter (`branch_base`), already proposed in the kickoff. Before running the startup command, **confirm it with the human in one line** ("worktree off `<base>` — go ahead?"). Any branch is valid with the OK — `main`/`development` (integration default) or a feature in progress if the work builds on it. **Do not block because of the branch** (that rigidity already broke real startups, e.g. base `feature/caja`); what is forbidden is creating the worktree WITHOUT confirming. With the OK you continue to point 3; if the human corrects the base, update the kickoff's frontmatter before continuing.
3. **If the worktree does not exist or you are on another branch** → **prepare it by running the brief's startup command AS IS** (it creates the worktree off the already-validated base branch + symlinks `.env` and `node_modules`). This is NOT "deciding the environment": it is running what the brief already defined. You only STOP if the brief does not bring a complete startup (no base branch) or if the base did not pass the guard of point 2.
4. **ABSOLUTE paths ALWAYS — never "bare" commands.** The shell's cwd **resets between commands** to your base directory, which is usually the **MAIN REPO, not the worktree** (even if you did `cd`). That is why a `cd <worktree> && …` is valid ONLY for that command, and any `git`/`npm`/write **without an explicit path runs on the main repo** — it mixes your work with that of other branches or sweeps up foreign files that are loose in main's working tree (it really happened: an agent pushed to its feature files from main that another session had left there).
   - Hard rule: **EVERY** command references the worktree by absolute path — `git -C <ABS-worktree> …` (including `add`, `status`, `commit`, `push`, `worktree`, `rev-parse`), `npm --prefix <ABS-worktree> …`, and absolute paths in every read/write.
   - **FORBIDDEN** a bare `git add`/`commit`/`status`/`push`, and forbidden to use `cd <worktree> && git …` as a substitute for `-C`.
   - Before ANY write or commit, confirm which repo you are standing on: `git -C <ABS-worktree> rev-parse --show-toplevel` must return the worktree, not main. If it returns main, STOP: you are about to write in the wrong place.
4.5. **Drifted worktree check (one line, before operating)**: confirm that the worktree is at its canonical path `<ABS-repo>-worktrees/<change-name>` and that `git worktree list` shows it there, resolving on disk. If the registered id != the folder, or the path does not resolve (someone renamed it with `mv`), warn and offer `git worktree repair <path>` (or `git worktree prune` if it was deleted) before continuing. **NEVER use `mv` to rename a worktree** — use `git worktree move`.
5. **Executable environment**: verify that the untracked files the stack needs are resolved in the worktree (config/secrets + dependencies — e.g. `.env` and `node_modules`, or the project's equivalent). If a symlink is missing → recreate it with the same startup command (point 3). Do not run tests/migrations without this.
6. **Init already done** (guaranteed by `/mala-pata-loop`, once per project) — EXACT EXISTENCE check, not exploration: `mem_search(query: "sdd-init/{project}")` returns several results by fuzzy ranking (other kickoffs/artifacts of the project). **Keep ONLY the item whose title/topic_key is EXACTLY `sdd-init/{project}`; the rest are false positives of the ranking — do NOT read them nor consider them context for this task.** With that exact item: `mem_get_observation` and read `strict_tdd` (if `true`, NON-NEGOTIABLE). If the exact item does NOT appear → warn the orchestrator; do not run the init.
7. **Load EXACTLY the skills the kickoff chose by objective (Step 2 of `/mala-pata-loop`), no more and no less.** Base: `clean-architecture` and `solid` always; `clean-ddd-hexagonal` + `design-patterns` only if the objective touches backend/domain. Conditionals: those in the kickoff's "Additional conditional skills" section (e.g. `database-design`, `ui-ux-pro-max`, `heuristic-evaluation`, `rag-*`, etc. — according to what the kickoff listed for THIS objective). Via the **Skill** tool, one per name (not all in one call); plugin ones use the `plugin:skill` name from the listing. **Do not add skills the kickoff did not choose** — the focused selection was already done when generating the brief; loading extra only adds noise.
8. **Do not explore the code to "go solving"** — only the minimum that the Spec/Design phase needs.

### Step 2.9 — gentle-ai canonical preflight gate (MANDATORY, only once)

Before the **first** dispatch of an `sdd-*` Agent (that is, before the Explore phase of Step 3), make **ONE single call** to `AskUserQuestion` with exactly 3 single-select questions, in the root/parent session (never from a subagent — a subagent can never carry this authority, the hook reads the transcript of the session that fires the Agent). Without this, `gentle-ai sdd-preflight-hook` will reject the `sdd-explore` dispatch.

**Exact shape, byte-exact — do not alter it:**

- The question texts literally start with `Gentle AI SDD preflight 1/3:`, `Gentle AI SDD preflight 2/3:` and `Gentle AI SDD preflight 3/3:` (the validator uses the regex `/^Gentle AI SDD preflight \d\/3:\s*/`). What comes AFTER the marker is free — that is where you put the kickoff's recommendation.
- The `header` of each group is EXACTLY: `Pace`, `Artifacts`, `PR strategy`.
- The option labels are EXACT and go IN THIS ORDER — the validator compares by index, so do NOT reorder nor add suffixes like "(Recommended)":
  - Q1 Pace: `Interactive`, then `Automatic`.
  - Q2 Artifacts: `OpenSpec`, then `Engram`, then `Both`.
  - Q3 PR strategy: `Ask me`, then `Single PR`, then `Auto`.
- Canonical descriptions (use them as is):
  - Interactive: `Confirm before each SDD phase advances.`
  - Automatic: `Advance through SDD phases without per-phase confirmation.`
  - OpenSpec: `Track this change with OpenSpec proposal, spec, design, and task files.`
  - Engram: `Track this change with Engram memory topics.`
  - Both: `Track this change with OpenSpec files and Engram memory together.`
  - Ask me: `Ask before opening a pull request when review risk is high.`
  - Single PR: `Deliver the change as a single pull request.`
  - Auto: `Chain pull requests automatically as work completes.`

**Literal payload template** (copy it as is, only filling in the recommendation between `<>` in each question text):

```
AskUserQuestion({
  questions: [
    {
      question: "Gentle AI SDD preflight 1/3: Cycle pace — the kickoff recommends: <Interactive|Automatic>",
      header: "Pace",
      multiSelect: false,
      options: [
        { label: "Interactive", description: "Confirm before each SDD phase advances." },
        { label: "Automatic", description: "Advance through SDD phases without per-phase confirmation." }
      ]
    },
    {
      question: "Gentle AI SDD preflight 2/3: Tracking artifacts — the kickoff recommends: <OpenSpec|Engram|Both>",
      header: "Artifacts",
      multiSelect: false,
      options: [
        { label: "OpenSpec", description: "Track this change with OpenSpec proposal, spec, design, and task files." },
        { label: "Engram", description: "Track this change with Engram memory topics." },
        { label: "Both", description: "Track this change with OpenSpec files and Engram memory together." }
      ]
    },
    {
      question: "Gentle AI SDD preflight 3/3: PR strategy — the kickoff recommends: <Ask me|Single PR|Auto>",
      header: "PR strategy",
      multiSelect: false,
      options: [
        { label: "Ask me", description: "Ask before opening a pull request when review risk is high." },
        { label: "Single PR", description: "Deliver the change as a single pull request." },
        { label: "Auto", description: "Chain pull requests automatically as work completes." }
      ]
    }
  ]
})
```

**Where the recommendation comes from**: read the kickoff's frontmatter, `sdd_preflight:` block (`pace` / `artifacts` / `pr_strategy` — see `/mala-pata-loop`, Step 4). Token-to-label mapping: Pace → `interactive`→`Interactive`, `automatic`→`Automatic`; Artifacts → `openspec`→`OpenSpec`, `engram`→`Engram`, `hybrid`→`Both`; PR strategy → `ask-on-risk`→`Ask me`, `single-pr`→`Single PR`, `auto-chain`→`Auto`. Inject that label as the recommendation in the text of the corresponding question (e.g.: `... — the kickoff recommends: Engram`). **If the kickoff does NOT bring a `sdd_preflight` block** (legacy kickoff), recommend mala-pata's defaults: `Interactive` / `Engram` / `Ask me`.

**Hard rules of this gate:**
- Exactly 3 questions, in ONE single call — never 3 separate calls nor more/fewer questions.
- Byte-exact labels in the canonical order above — never reorder, never add suffixes ("(Recommended)" or any other) to a label. The recommendation goes ONLY in the question text, after the marker.
- It has to run in the root/parent session — a subagent can never satisfy this gate.
- **NEVER manually write or duplicate the `## SDD Session Preflight` block** — the runtime automatically prepends it to the child's prompt when the preflight resolves successfully.

**Automatic ceiling (enforced rule)**: right after the pace answer, check the profile. FULL / STANDARD may NOT end up Automatic — if the human answered Automatic, clamp the cycle to Interactive and say so in one line (a large objective in auto dams up confirmations at the preview). LITE / MINIMAL may stay Automatic. The preview phase is never automatic in any profile.

With the human's answer (after the ceiling check), the hook already has what it needs: continue straight to Step 3 (dispatch of `sdd-explore`).

## Step 3 — SDD CYCLE, one phase at a time (each phase: summary + PAUSE + OK)
Run the phases IN ORDER, **one by one** (never two together, never spec and design in parallel), reusing the project's `sdd-*` skills and persisting each artifact in engram (`sdd/<change-name>/<artifact>`). Do not advance a phase without the user's OK.

**Execution mechanism (do NOT deduce from elsewhere)**: each phase is executed with the **Agent** tool, `subagent_type` = the name in parentheses of that phase (`sdd-explore`, `sdd-propose`, `sdd-spec`, `sdd-design`, `sdd-tasks`, `sdd-preview`, `sdd-apply`, `sdd-verify`, `sdd-archive`) — NEVER by loading that phase's SKILL.md into the current context with the Skill tool (that would run the phase inline, without the context isolation that the apply/verify phases need). `model` = the one mapped for that phase in the Model Assignments table of `~/.claude/skills/_shared/sdd-orchestrator-workflow.md` (the lazy-loaded surface that CLAUDE.md references — the table does NOT live in CLAUDE.md itself). **mala-pata exception (that table is gentle-ai's and does not know `sdd-preview`)**: for `sdd-preview` use **`opus`** — it is the most judgment-heavy adversarial phase of the cycle, it goes in the same tier as propose/design, not in the default. If the table is not available for the other phases, use `sonnet`.

1. **Explore** (`sdd-explore`) — investigate the **real code and context of the worktree** to ground the proposal: current state, approaches, risks, what to reuse. Reads the kickoff as input. Does not write code. Persist `sdd/<change-name>/explore`. → **GATE**.
2. **Propose** (`sdd-propose`) — the change's proposal (intent, scope, approach), backed by the explore + kickoff. Persist `sdd/<change-name>/proposal`. → **GATE**.
3. **Spec** (`sdd-spec`) — requirements + scenarios (delta specs). Reads the proposal. Persist `sdd/<change-name>/spec`. → **GATE**.
4. **Design** (`sdd-design`) — technical approach and architecture decisions. **This is where the brief's open decisions are RESOLVED, with the user.** Reads proposal + spec (runs AFTER spec, not in parallel). Persist `sdd/<change-name>/design`. → **GATE**.
5. **Tasks** (`sdd-tasks`) — ordered, atomic checklist (include **Phase 0 of components** if there is UI). Reads spec + design. Persist `sdd/<change-name>/tasks`. → **Plan approval GATE**. Once approved, it moves to **Preview** (NOT directly to Apply). **Up to here and during Preview: ZERO code, ZERO migrations, ZERO setup.**
6. **Preview** (`sdd-preview`) — MANDATORY human walkthrough between tasks and apply (via Agent, same mechanism as above): translates the plan into human language and detects duplication / badly thought-out architecture / hardcoded flows. **Precondition (Hard rule #4)**: before launching preview, confirm that the WHAT is closed — no open objective red cards nor scope decisions still under debate. If the objective is still under discussion, do NOT launch preview: go back to explore/propose. Preview assumes a defined objective; it reviews the plan, not the objective. `sdd-preview` itself reads tasks + design (+ spec + proposal + **the real code of the worktree**) and decides in a self-assessment **how many blind reviewers to run (0, 1 or 2)** — it NO longer depends on `sdd-tasks` recommending it. It does NOT write code. Persist `sdd/<change-name>/preview`. → **MANDATORY anti-rubber-stamp GATE**: ALWAYS interactive, **immune to automatic mode** (even if they asked for "auto up to X", this phase STOPS anyway) — whether or not there is an audit. The orchestrator presents the gate that the artifact brings (directed questions + disposition per finding REUSE/REFACTOR/IGNORE when there was an audit — never a "global OK"). **Apply stays TIED to the approved dispositions.** Only with the preview approved do you move on to Apply. **Kickoff handoff to preview (and to any SDD phase that needs the DoD verbatim)**: the engram topic `sdd/<change-name>/kickoff` holds only the pointer `Kickoff in file: <path>`, not the content — so pass the kickoff's **ABSOLUTE PATH** in the phase prompt (e.g. `Kickoff: <ABS-path>`) so the phase can `Read` the file and copy the DoD verbatim.
6.5. **Worktree freshness gate** (between approved preview and apply, BEFORE writing a single line) — **auto-update-and-notify, it is NOT a human pause unless there is a real conflict**. Between when the worktree was created (Step 2) and this point all the planning went by (sometimes hours or days of gates), so the base may have advanced. Since phases 1-6 **do not write code**, the worktree's branch has no commits of its own and updating it is a **risk-free fast-forward**. ALWAYS check:
   1. `git -C <ABS-worktree> fetch origin <base>` (the `<base>` is the kickoff's `branch_base`).
   2. `git -C <ABS-worktree> rev-list --left-right --count origin/<base>...HEAD` → `A` (base ahead) `B` (worktree ahead).
   3. **A=0** → worktree up to date. Continue to apply (an optional line: "worktree up to date with `<base>`").
   4. **A>0 and B=0** (normal case — planning wrote nothing) → **automatic fast-forward**: `git -C <ABS-worktree> merge --ff-only origin/<base>`. **Warn in ONE line** ("base `<base>` advanced `A` commits; worktree updated by fast-forward") and continue to apply. You update on your own, you do not ask for OK.
   5. **A>0 and B>0** (the worktree ALREADY has commits of its own — typical when RESUMING mid-apply) → **the only situation that STOPS**: it is no longer ff, it is rebase/merge with possible conflict. Report and offer `git -C <ABS-worktree> rebase origin/<base>`; if there are conflicts, leave the worktree as is and wait for a human decision. **Never force** (`--force`, `reset --hard`, `--no-verify`).
   6. **Cross-check with migrations**: if `A>0` and this change has a migration, a sibling branch may have merged its migration in that advance → fire early the number re-verification of Step 4.1-bis (measure git). If your provisional number was taken by another branch, renumber (regenerate) **BEFORE apply**, not at merge — it is cheaper to discover it here.
   7. After the fast-forward, reconfirm the executable environment (the `.env`/`node_modules` symlinks survive an ff, but verify they are still resolved) before starting apply.
7. **Apply** (`sdd-apply`) — only now is code written. For each task: **STRICT TDD** (Red → Green → Refactor) + **100% verify** (0 warnings/critical). Migration with the kickoff's **provisional** number (it is NOT yet final — it is confirmed or renumbered at merge, see Step 4.1-bis), validated **according to the project's testing convention** (round-trip if applicable). Persist `apply-progress` (MERGE, not overwrite). On closing each batch/phase → summary + PAUSE.
   - Phase 0 (if there is UI) — **MANDATORY Storybook-first + Atomic Design + reuse-first** (recurring error: things get created without this):
     - **BEFORE building, audit the project's library/workshop and list REUSES / ADAPTS / NEW per component** — reuse or compose on top of what exists, only create what does not exist.
     - Build with **Atomic Design**: **atom → molecule → organism**, in that order; no monolithic organisms. One story per component with its states/variants.
     - **HARD RULE — NEVER write PRESENTATION specs before visual approval.** Apply's **STRICT TDD does NOT apply** to the visual Phase 0. (Real error committed in `paso-4-cycle-detail-modal-rediseno`: 49 green specs were written on a layout that the human later rejected — work thrown in the trash and, worse, the "green" TDD gave a false sense of progress.) Split the specs into two categories:
       - **BEHAVIOR** (which service/channel is called and with what arguments, validations, transaction sequence, permissions, model state) → **yes**, it goes with TDD before the visual approval; it **survives** any redesign.
       - **PRESENTATION** (structural `data-testid`, number/order of sections, CSS classes, viewport measurements, presence/absence of blocks in the DOM) → **FORBIDDEN to write them before the visual OK**; they die with the layout. They are written **after**, against the already-approved design.
       - Category test, when in doubt: *is this assertion still true if the human picks another layout?* If the answer is no → it is presentation → it goes after.
     - The visual Phase 0 is built with **stories + fixtures ONLY** (zero layout specs) — as cheap as possible to throw in the trash, because that is what the gate is for.
     - Corollary for **Spec/Design**: presentational success criteria (measurements, `data-testid`, section count) stay marked as **provisional** until the visual gate passes; do not turn them into TDD invariants before that OK.
     - **Do not offer layout variants that are the same box with the content reordered.** If the alternatives share the same inner component without redesigning, they are not design alternatives: they are the same screen. Commit to ONE direction and show it.
     - Wait for **APPROVAL** before continuing; once approved, the rest advances without further component approvals.
8. **Verify** (`sdd-verify`) — final verification vs spec/tasks + **Definition of Done** checklist. It must pass at **100%**. Persist `sdd/<change-name>/verify-report`. → **GATE**.
9. **Archive** (`sdd-archive`) — only with verify green: sync delta specs → main specs, close the change. Persist `sdd/<change-name>/archive-report`.

> If at any point an unresolved decision appears, **raise it to the Design phase and consult** — do not resolve it by coding.

## Step 4 — Closing: PR, pipeline/CI review and cleanup (post-cycle, one sub-phase at a time, same GATE rigor as Step 3 — never sit passively waiting for the human to ask you, you check and announce)

### 4.1 — Closing report
After Verify (100%) + Archive, report status — **Done** (evidence: TDD green, verify 100%) or **partial** (what is missing and why). `verify-report` is already in engram. It is only a summary — you go straight on to 4.2, without waiting for OK here.

### 4.1-bis — Migrations: re-verify and renumber before integrating (only if the change touched migrations)
If this change created a migration, its number was **provisional** (see Step 3 phase 7 and the kickoff). **Right before integrating** — not when opening the PR, but as close as possible to the real merge (the project rule "the first to merge keeps it") — re-measure git:
1. List the numbers occupied in the base branch AND in the sibling in-flight branches (with the project's command — e.g. `git ls-tree -r --name-only <branch> -- <migrations-folder>`). **Do NOT count files on disk.**
2. **If your provisional number is still free** → confirm it and continue to 4.2.
3. **If a sibling already took it (merged first)** → **renumber to the next free one**. The HOW belongs to the stack (`sdd-init` knows it): with a chained-state migrator (journal/snapshots, e.g. drizzle-kit) it is **NOT renaming files — it is regenerating** (delete the migration + its snapshot, revert the journal entry, `git pull` of the base with the winner, regenerate against the schema, re-write the paired rollback) and **re-run the round-trip**. Only with the final number and the round-trip green do you continue to 4.2.
4. If the PR stays open waiting for human merge and in the meantime a sibling merges → **repeat this check before the final merge**. Leave it noted in the PR body.
Do not continue to 4.2 without the migration number confirmed (or renumbered + round-trip green).

### 4.1-ter — Smoke test with seeded data → MANDATORY GATE (only if applicable)
A quick manual test that the REAL functionality is met, with data already seeded — so the human does not have to build the fixture by hand. It is the HUMAN acceptance gate that is missing between the machine test (verify) and the PR. It runs between 4.1-bis and 4.2.

1. **Applicability gate — you propose, the human confirms (one line).** Derive the proposal from the shape of the change and from the kickoff's `smoke_test` field:
   - **It is SKIPPED** (propose "no"): pure refactor, config, docs, chore, internal util with no surface that a human exercises, **purely visual/presentational changes** (layout, colors, hover, spacing — the visual approval already covers them), or when verify already covers the end-to-end case with data. A MIXED change (visual + behavior) is not skipped because of the visual part: the behavior part weighs.
   - **It runs** (propose "yes"): the change adds/alters behavior that a human would exercise by running the app and that verify does not test end-to-end with real data.
   - If the kickoff brings `smoke_test.needed: yes|no`, respect it; with `auto`, propose and wait for the OK in one line. If "no" → record it and continue to 4.2.

2. **Script + seed recipe — orchestrate `mala-pata-walkthrough` (QA/UAT lane).** Do not write your own script: ask `mala-pata-walkthrough` for this change's walkthrough. It ALWAYS returns the **access block** (test URL + credentials + server running against the test DB), the fixed **table** `# | Given (path) | When | Then`, and —if it touches DB— the **`## Seed`** section (fixture recipe derived from the `Given`s + the kickoff's `smoke_test.data`). It runs BEFORE the seeding, because the seed reads that recipe.

3. **Seed (only if it touches DB) — delegate to `mala-pata-seed`.** The seeding is executed by `mala-pata-seed`, which reads the `## Seed` section of the walkthrough's QA and seeds with the project's mechanism (`sdd-init`), **idempotently**, against the **test DB** (never prod). A single executor for in-cycle (here) and standalone. Present to the human what was seeded (ids/records) together with the script. If the change does not touch DB (UI-only with no data), skip the seed.

4. **Confirmation → hard GATE.** Ask explicitly: **"Was the functionality met? (yes / no)"**.
   - **Yes** → record it and continue to 4.2.
   - **No** → do NOT open the PR: **reopen tasks** with what failed (it goes back to the cycle: apply, or design if it is a deep issue), just like any finding that reopens TODOs.

5. **Teardown — optional, it is asked (default NO).** On closing the gate, one line: **"Do I delete the data I seeded? (default: no)"**. The default is not to delete — a persistent test DB with data is useful. If the human asks to delete, delete **only what this run seeded** (by the seed's ids/namespace), NEVER a wipe of the entire DB.

Do not continue to 4.2 without: (a) the "not applicable" confirmed by the human, or (b) the human's confirmation that the functionality was met.

### 4.2 — Destination of the work → **MANDATORY GATE**
As soon as Verify is green, **STOP and ask yourself, without the human having to ask you** — **NEVER assume a PR** nor carry on past it:
> How do I close this: **(a) open a PR** (towards which branch — `main` or another?), or **(b) merge into a feature branch** (which one, e.g. `feature/caja`)?
- **(a) PR**: check whether there is **already an active PR** for this work (`gh pr list` / `gh pr view`). If it exists → **consolidate there**, do not open a second one (a single active PR). If not → propose and **open the PR only with OK** (title, summary, link to SDD artifacts in engram). **Do not merge/close the PR without an explicit request** — you stop at **green CI**. (The branch is NOT touched at this point: it is only deleted in the cleanup and ONLY once merged — see 4.5.)
- **(b) Merge into a feature branch**: integrate the SDD's branch into the indicated feature branch **only with the user's OK**. Commits with **explicit pathspec**. (Once the merge is done, the SDD's branch is integrated → it is deleted in the cleanup, 4.5.)
- In both cases: if there are conflicts or red CI → **STOP and report**, do not force.
Do not continue to the closing without the human's explicit answer to this question.

### 4.3 — (no RDD Gate in the SDD cycle)
**RDD does NOT run in the loop/SDD.** Since gentle-ai v3, RDD is native to the **ODD** lane — it evaluates per *work-unit commit* (`gentle-ai review assess`), not at the closing of an SDD cycle. The one that orchestrates it is **`mala-pata-organic`** (see there). The SDD cycle closes without a receipt gate: from **4.2** (destination + human's OK) you go straight to **4.4** (CI). If someday you want a review on a specific SDD PR, you run it by hand outside — it is not a gate of the cycle.

### 4.4 — Pipeline/CI review → your PROACTIVE check, not passive
After opening the PR (or merging), **you yourself actively review the run's status** — do not wait for the human to ask you "and the CI?" nor assume it turned out green. Use the project's tool (GitHub Actions → `gh run list`/`gh run view`; Azure DevOps → `az pipelines runs list`/`az pipelines runs show`; GitLab → its CLI/API; Jenkins/others → whatever applies). Confirm that **ALL stages** of the relevant run are green before announcing anything.
- If something is **red** → **STOP**, bring the log of the step that failed and report the **exact error**. Do not mark "Done" with the pipeline red.
- If the change includes **migrations/DDL**: explicitly verify that the deploy's `migrate`-equivalent step passed (it is usually the one that breaks the most). If it fails, report the specific reason (graph conflict, data-migration, etc.).
- Distinguish an **infra** failure (transient/retryable) from a failure **of the change** (it has to be fixed before closing).
- If the project does NOT have CI/pipeline → leave it explicit and continue (do not invent one).
Do not continue to 4.5 without confirming yourself that the relevant pipeline is green (or that there is no pipeline).

### 4.5 — Cleanup → **MANDATORY GATE, your PROACTIVE check — never wait for them to ask**
As soon as 4.4 closes green, **check the status yourself** (`gh pr view` of the PR, or `git log` of the feature branch) — the trigger is that 4.4 came out green, **NOT** that the user tells you or reminds you. As soon as you confirm PR closed/merged (or merge into the feature done) **announce explicitly**:
> "PR/merge closed and CI green. Ready to do the cleanup (kill processes, delete worktree, delete local+remote branch). Shall I proceed?"

Only with the human's OK (or if the profile is running in explicit automatic mode requested by the human — never by default), **from outside the worktree** (main repo/orchestrator — you cannot remove the worktree where you are standing):
- **Kill background processes/servers** that you left for this SDD (dev server, test/vitest watch, etc.).
- `git worktree remove <ABS-worktree>` + `git worktree prune` (the `.env`/`node_modules` symlinks go away with the folder — it **does not touch** the main repo's target).
- Delete temporary files / build artifacts that were left over.
- **Delete the merged branch — local AND remote — as a STANDARD part of the cleanup** (an already-integrated branch is dead code; it needs no separate request beyond the OK above). Local: `git branch -d <branch>` (use `-d`, not `-D`: `-d` fails if it is NOT merged, protecting you). Remote: `git push origin --delete <branch>` (or `az repos ref delete` / the project's equivalent). **Exception — do NOT delete the branch if the integration did NOT happen**: PR just opened without merge, abandoned PR, or a merge that did not reach green. In those cases the branch has unintegrated work → ask for explicit separate OK before deleting. (If when merging the PR you already used `--delete-source-branch`, the remote no longer exists — you only clean the local one.)
- **Seeded data (4.1-ter):** do NOT wipe the test DB here — its deletion was already decided at the smoke test gate (default: do not delete). If at 4.1-ter deletion was requested and deferred, delete here only what that run seeded.
- Confirm that nothing was left running or hanging.

## Step 5 — Final summary as a TABLE (MANDATORY)

When EVERYTHING is finished (verify + archive + PR/merge + CI + cleanup), **ALWAYS close with a status table** — not with loose prose. It is the last thing the user sees and must be readable at a glance. Markdown format, one row per milestone, left column = milestone, right column = status with a **curated typographic glyph + word, no emoji** (`✓` ok · `◐` partial/with note · `✗` failed · `○` N/A or pending) + **concrete evidence** (numbers, ids, commits — never a bare "ok").

Canonical rows (include ONLY those that apply; do NOT invent a row that did not happen):

| Milestone | Status |
|---|---|
| SDD cycle (explore→archive) | Complete |
| Verify | PASS `<n>/<n>`, `0 CRITICAL` |
| Smoke test (fixtures + human confirmation) | ✓ functionality OK · or `○ N/A (did not apply)` |
| e2e real case `<id>` | `<obtained>` vs `<expected>` (delta `<%>`), `<detail>` |
| No-regression | `<Nf>/<Ne>` identical to baseline |
| PR `#<n>` → `<branch>` | ✓ MERGED (merge commit `<sha>`) |
| CI post-merge (deploy + migrate `<N>`) | ✓ GREEN (`<build detail>`) |
| Cleanup (worktree + local/remote branch) | ✓ Done |

Table rules:
- **Adapt the rows to the real change**: no migration → remove the `migrate <N>` from the CI row; no real e2e case → remove that row; PR vs merge-to-feature → adjust the destination row; project without CI → `CI` row with `○ N/A (project without pipeline)`.
- **No false green**: if something was left partial/red/pending, the row carries the specific reason, prefixed `◐ partial: <reason>` or `✗ red: <reason>` — the table must reflect the truth of the closing (consistent with the rule of not marking "Done" with a red pipeline).
- Below the table you can add 1-3 lines of non-blocking follow-ups if there are any; the rest of the detail already lives in the engram artifacts.
