# SDD base rules — universal invariants (stack- and project-agnostic)

They apply to **all profiles** (FULL / STANDARD / LITE / MINIMAL) and to **all projects**.

## Method (non-negotiable)

- **Interactive phase-by-phase execution**: each phase closes with a summary and a **pause** waiting for the human's OK before the next one. **Pace default = interactive.** `/mala-pata-loop-start` Step 2.9 asks pace + artifacts in the hook's canonical question; this rule gives the RECOMMENDED DEFAULT the runner feeds into that question (interactive; automatic only in LITE/MINIMAL and only if the human picks it). The active profile (FULL/STANDARD/LITE/MINIMAL) already defines how explicit each specific human gate is (see profiles).
  - **Automatic ceiling by objective size (non-negotiable)**: even if the human asks for it, automatic mode is only allowed in **LITE / MINIMAL**. In **FULL / STANDARD** the pace is interactive phase-by-phase ALWAYS — "auto until X" is not accepted. Reason: a large objective run in auto **dams up all the confirmations at the preview** — the human arrives at a gate with 5-6 phases of accumulated decisions they can no longer genuinely review, and the preview stops being a checkpoint and becomes a rubber stamp. If the FULL/STANDARD human asks for auto, answer in one line that because of the objective's size the cycle goes interactive (and why), and you continue phase-by-phase. In any profile, additionally, the **preview** phase is NEVER automatic (it always stops, see `sdd-preview`).
- **Artifact store: recommended default `engram`**. This is the default the runner feeds into the canonical pace + artifacts question in `/mala-pata-loop-start` Step 2.9 — the human may pick another store there.
- **Return envelope per phase**: each phase returns `{ status, executive_summary, artifacts, risks, next_recommended, skill_resolution }` (the gentle-ai result contract).
- **Init guard**: before starting, `mem_search("sdd-init/<project>")`. If it does not exist, run `sdd-init` to detect the project's stack, testing, conventions and tools. Those remain in engram as project context — **NOT in the SDD rules**.
- **Phase 0 (if the change touches UI)**: audit REUSA/ADAPTA/NUEVO + Atomic Design + component workshop (Storybook or whichever the project uses). The human gate level is defined by the profile.
- **TDD**: always present. Granularity (per task vs per feature) is defined by the profile.
- **Verify**: always present. Depth (light/normal/heavy): the profile gives the **default**, but the EVIDENCE can raise it — the profile was chosen by size/cost BEFORE explore, so it cannot be the last word on risk. If the `sdd-preview` self-assessment detected real risk signals (auth/payments/permissions/shell/CI/data migration, or a pattern without precedent), verify rises to at least **normal** even if the profile says light. A 3-file auth fix is MINIMAL by size but does NOT deserve the lightest verify — volume never decides risk (same principle as the reviewer count).
- **Kickoff idempotency**: `mem_search("sdd/<change-name>/kickoff")` before creating.
- **Conflict in flight**: `git worktree list` + review active branches. If there is overlap → confirm with the human before generating.
- **Migrations (if they apply)**: the number is **provisional for the author, final at merge**. The source of truth for numbers ALREADY taken is **git** (measure the base branch + the sibling branches in flight), NOT a reservation registry in engram (it is a lock that long branches do not respect and that drifts). You take the next free one as provisional to write/test, and renumber on integration if a sibling merged first ("the first to merge keeps it"). HOW to renumber depends on the stack's migrator (`sdd-init` knows it) — with chained-state migrators (journal/snapshots) it is **regenerate, not rename**. **Never** infer the next number by counting files on disk.

## Engineering principles (apply to every change)

- `clean-architecture` — dependency inward; domain without framework/ORM/web; screaming architecture.
- `clean-ddd-hexagonal` — `Infrastructure → Application → Domain`; one aggregate per transaction; repository per aggregate; ports & adapters (never controller→repo directly).
- `solid` — SOLID + object calisthenics; Value Objects for domain concepts (never raw primitives); YAGNI / KISS / DRY-after-Rule-of-Three.
- `design-patterns` — patterns **emerge from refactoring**, they are not forced; use pattern vocabulary when naming.
- `heuristics-and-checklists` — use **forcing functions** ("does not advance until X"), not soft reminders.
- **SSOT** — every domain literal lives in ONE single place; zero duplication of truth.

## Universal conventions (apply to all projects)

### Names

- **`change-name`**: kebab-case, concise, domain/BC prefix when it helps. **No** version suffixes (`-v2`, `-nuevo` → they leave orphaned dead code). Max ~40 chars.
- **Branch**: `<type>/<change-name>` — the **type is advised according to the work and the human confirms it** (same as the base branch). Conventional types (Conventional Branch / git-flow): `feature/` (new functionality), `fix/` or `bugfix/` (correction), `hotfix/` (prod urgency), `refactor/` (refactor without behavior change), `chore/` (tooling/build/deps), `docs/` (documentation), `release/` (prepare a release). lowercase + hyphens, short and descriptive. **`sdd/...` is FORBIDDEN** as a branch or worktree prefix — it is the engram topic_keys convention, NOT git's. The `<change-name>` (suffix) is unique and the same whatever happens with the prefix — that is why radar can locate the branch by the `branch:` registered in the kickoff or by the suffix `*/<change-name>`, without depending on the prefix.
- **Worktree**: one worktree **per SDD** for isolation. **SINGLE path**: `<ABS-repo>-worktrees/<change-name>` — sibling to the repo, **never inside**. The dir is just `<change-name>` (no type prefix, no `sdd/`), stable so that radar and cleanup find it.
  - **Why outside, and not in `.claude/worktrees/`**: a worktree inside the repo is a complete source tree that the project's collectors find on their own. Measured on 2026-09-16 in bodega-ferreteria-colombia: with a single worktree inside, `vitest` went from 747 test files to **1496** and from 24s to **50s** — every test running twice — and **3 false failures** appeared (Playwright specs run by vitest, because the exclusion pattern was relative to the root and did not reach the copy). CI does not reproduce it: its checkout is clean. So the symptom is "fails locally, passes in CI", and whoever sees it will look for the cause in their change.
  - **Different from mala-pata artifacts**: mala-pata docs (kickoffs, research, roadmap, walkthroughs) DO live **inside the repo** under `mala-pata/`, versioned for traceability — they are markdown, not source trees. The worktree goes outside for the technical reason above (it is a complete source tree that the project's collectors run), not because of a "nothing inside" rule.
  - **Stable name (avoid ghost worktrees)**: the worktree's basename must be `<change-name>` and match the id git registers (`git worktree add` derives the id from the path's basename, so creating at `<ABS-repo>-worktrees/<change-name>` already leaves them equal). **NEVER rename the worktree with `mv`** — git keeps pointing at the old path and its errors start naming folders that do not exist on disk (e.g.: folder `caja` registered as `feature-caja`). To move it: `git worktree move <viejo> <nuevo>`. If it is already out of sync (a `git worktree list` path that does not resolve, or registered id != folder): `git worktree repair <path>` (if it was renamed) or `git worktree prune` (if it was deleted).
- **Engram topic keys**: `sdd/<change-name>/{kickoff,explore,proposal,spec,design,tasks,apply-progress,verify-report,archive-report}`.

### Commits

- **Conventional Commits**: `<type>(<scope>): <description>` — standard types (`feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `build`, `ci`, `style`). The scope is defined by the project (detected by sdd-init).
- **NO AI-assistant attribution** in commits (`Co-Authored-By: Claude`, `Generated with Claude Code`, any similar trailer). The commit is signed by the human.
- **NO `git stash`** during the SDD flow — it moves work out of history and complicates recovery in case of rollback. Use real commits (even WIP) or leave it in the working tree.
- **NO `--no-verify`** nor `--no-gpg-sign` — respect the project's hooks unless the human explicitly asks otherwise.
- **NO amend to published commits** — each correction goes in a new commit.

### Branches and PRs

- **NEVER `git push` directly to `main` / `master` / integration branch**. Always through a PR (or the repo's review mechanism).
- **PR title**: Conventional Commits format, same style as the commits.
- **PR body**: include (a) summary of what changes, (b) verifiable test plan, (c) link/reference to the kickoff FILE (`mala-pata/kickoffs/<change-name>.md`; kickoffs are files now, engram holds only a pointer).
- **Base branch**: default/recommended `main` or `development`, but **any branch is valid if the human confirms it** (e.g.: work that builds on a feature in progress comes off THAT feature). What is NON-NEGOTIABLE is the **confirmation**: the base is ALWAYS proposed with its reason ("the code lives in X" / "integration default") and the human's OK is awaited before fixing it — it is never assumed silently, never blocked just for not being main. It is recorded explicitly in the kickoff (frontmatter `branch_base`), and that confirmation holds for the whole cycle.

### Paths

- **In code**: paths relative to the workspace (according to the stack's resolver — `tsconfig`, `pyproject.toml`, etc.).
- **In communication with the human**: paths relative to the repo when addressing the human in prose (not absolute to the filesystem); in commands and artifacts (e.g. the copy-paste start command that the Step-5 closes show) the path stays ABSOLUTE.
- **In shell commands**: absolute paths (`git -C <abs>`, `--prefix`, absolute paths), no `cd` to operate in another directory.

## Kickoff structure (SSOT)

Every kickoff **MUST** have:

1. **Active profile** — FULL/STANDARD/LITE/MINIMAL, confirmed by the human in Step 1.5. With the proposal's reasoning and estimated cost (order of magnitude).
2. **Orchestration metadata** — change-name, branch, worktree, profile, depends_on, parallelizable_with, base branch, start command.
3. **Change contract** — endpoints, shapes, types, BE migrations if applicable. Specific to the change, NOT to the method.
4. **Technical reinterpretation** — objective, problem, IN/OUT, measurable success criteria.
5. **Architecture and affected layers** — with refs to the project's ARCHITECTURE.md (detected by sdd-init).
6. **High-level phase plan** — by objective, NOT by task. The tasks are produced by `sdd-tasks` in the corresponding phase.
7. **Definition of Done** — verifiable closing criteria.
8. **Risks / open decisions** — to resolve within the SDD.

## What does NOT go in the base rules

- Stack-specific tools (type regen, build/test commands, UI/testing libraries, file format) → detected by sdd-init and live in the project context in engram.
- Concrete contracts of endpoints, types, or payloads → live in the specific change's kickoff.
- Rules of concrete projects (commit scope format, branch pattern with custom prefixes, worktree location) → live in the project's CLAUDE.md or in sdd-init.
- Number of `sdd-preview` reviewers → decided by `sdd-preview` itself in its self-assessment (blast-radius / reuse-first / architecture smells), `sdd-tasks` no longer recommends it. The profile does not force a number.
