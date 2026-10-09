# LIVE phase + status-light derivation

Everything is re-derived every run. Two sources, neither cached:
- **VCS (git)** = truth about branch/merge/cleanup.
- **Available persistent memory** = truth about phase (which artifacts exist).

## Step A — Freshness (git)

```
git fetch --all --prune
```
- Detect the repo's integration branch (look at what the feature
  branches are merged into; usually `development` or `main`). Confirm it, do not assume it.
- Save `git rev-parse --short origin/<integr>` for the banner. By default
  operate on THE current repo (the cwd's). A project spans several repos ONLY
  if the human names them explicitly (or the project config declares them);
  NEVER assume nor go looking for sibling repos from session memory nor
  by guessing paths. If there are several, repeat the steps for each named repo.

## Step B — COMPLETE cycle of each SDD (memory — exact commands)

Concrete stack: memory = engram MCP (`mem_search`, `mem_get_observation`). If
your runtime uses another memory, map to "search by exact title" + "fetch
content by id".

For EACH change-name `C`, fetch ALL its phases with ONE search by the
EXACT and bare change-name (no extra words — adding
"archive/verify/shipped" makes the semantic search fail and was the
historical bug of trusting 1 hit):

```
mem_search(query="C")
```

Keep ALL the observations whose title is `sdd/C/<phase>`. Phases in
canonical order:
```
kickoff · explore · proposal · spec · design · tasks · preview
· apply-progress · verify-report · archive-report · state
```
`memory_phase` = the MOST ADVANCED one present. Partial progress: if `apply-progress`
says "X/Y tasks", report `apply X/Y`.

Anti-truncation (MANDATORY): if `mem_search("C")` looks truncated or late phases
are missing, confirm closure with targeted searches and fetch the content:
```
mem_search(query="sdd/C/archive-report")
mem_search(query="sdd/C/verify-report")
mem_search(query="sdd/C/state")
mem_get_observation(id=<most advanced phase>)
mem_get_observation(id=<state/closing decision, if it exists>)
```
FORBIDDEN to derive the phase from a single search hit. Enumerate the full cycle.

## Step C — Git reality of each SDD

Branch convention: `<type>/<change-name>` — the type prefix (`feature/`, `fix/`,
`hotfix/`, `refactor/`, `chore/`, `docs/`, `release/`) is chosen per job and confirmed
(see `_base.md`); **never `sdd/`**. The `<change-name>` suffix is unique and the same no matter
what happens with the prefix — that is why **locate the branch by the suffix, not by a fixed prefix**:
1. If you have the kickoff, use its frontmatter `branch:` (exact name already confirmed).
2. If not, search by suffix: `git branch -r --list '*/<change-name>'` (matches any
   conventional prefix). If it shows up under `sdd/...`, it is a LEGACY branch outside the convention —
   flag it with "legacy branch sdd/ — rename" in the evidence (the new skills no longer
   generate `sdd/`).
   Note: `<change-name>` is unique → the suffix does not collide between SDDs.

With `<branch>` resolved (call it that below):
- Does the branch exist on the remote? `git branch -r --list 'origin/<branch>'` (or the result of point 2).
- Merged into integration? Confirm by CONTENT/commits, not by `--merged`
  alone (a squash does not show up as merged). Two strong signals:
  - `git log origin/<integr> --oneline | grep -i '<change or PR#>'`
  - a distinctive file/symbol of the SDD present in `origin/<integr>`
    (`git grep <symbol> origin/<integr> -- <path>`).
- Stale: `git rev-list --left-right --count origin/<integr>...origin/<branch>`
  → `A` (integr ahead) `B` (branch ahead). Large `A` = old branch.
- Local worktree/branch alive? `git worktree list`, `git branch --list` (the worktree dir
  is still `<change-name>` without prefix).

## Step D — State machine (first match wins, top to bottom)

1. **CANCELLED** — there is a `state` artifact/decision that says ABANDONED/
   cancelled. Next action: none.
2. **CLOSED** — merged into integration AND no remote branch AND no local worktree/
   branch. Next action: none.
3. **MERGED (cleanup pending)** — merged into integration BUT worktree or
   branch (local/remote) are still alive. Next action: clean up.
4. **RED: READY FOR PR** — apply complete + verify PASS (and/or archive) BUT NOT
   merged (code on branch, absent from integration). Next action: open
   PR / merge. If `stale` (B small, A large): add "WARNING: update branch +
   re-verify before the PR".
5. **RED: APPLY/VERIFY NOT CLOSED** — apply-progress complete without verify, or verify
   PASS without archive. Next action: run the missing phase (verify / archive).
6. **YELLOW: HUMAN GATE** — the last artifact is a `preview` with no later approval
   decision, OR `verify-report` with unresolved CRITICAL/WARNING, OR
   a decision that asks for explicit human input. Next action: review/approve.
7. **ORANGE: PARKED/BLOCKED** — depends on another SDD in the list not yet merged
   (BLOCKED), OR there is a pause note (adjacency/sibling worktree without merge), OR
   a stale branch that blocks. Next action: unblock (name the blocker).
8. **BLACK: NO INSTRUCTION** — cycle stuck with no clear next step: partial apply-progress
   (X/Y) without continuation nor pending gate, or planning stopped midway
   with no gate and no recent activity. Next action: the human defines what is next.
9. **GREEN: IN PROGRESS** — advances normally; a phase closed and the next one is auto-runnable
   without a gate. Next action: run the next phase (name it: e.g. "run
   spec", "run tasks").

## Step E — Dependencies (among the SDDs in the list)

Dependency signals (read from kickoff/proposal/design):
- "off <branch> after merge of sibling PR #X" / "depends_on" / "base branch".
- Same file/service touched by two SDDs (adjacency → blocking risk).

**Kickoff = file, not engram**: the engram observation `sdd/C/kickoff` is just a
one-line pointer (`Kickoff en archivo: <path>`). To read `depends_on`/base branch
from the kickoff, follow that path with `Read` — the file's YAML frontmatter carries
`depends_on`, `parallelizable_with` and `branch_base` directly. Only old kickoffs
(pre-migration) have the full content in engram.

If A depends on B and B is not merged → A goes ORANGE with `Depends = #idxB BLOCKED`.
If B is already merged → show `Depends = #idxB` without BLOCKED (informational).

## Derivation rules (non-negotiable)

- **Never** derive "merged" from memory. Only from git against integration.
- **Never** trust a state from a previous run. Always re-derive.
- On a memory↔git conflict, **git rules** for branch/merge/cleanup; memory
  rules for phase/gate/cancellation.
- If a datum cannot be verified live, mark the cell with `?` and explain in
  the evidence — never fill with an assumption.
