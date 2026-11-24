---
roadmap_slug: suite-hardening
project: mala-pata-skills
domain: suite
created_at: 2026-11-24T10:31:46-0500
status: executed (P0-P4 landed on feature/suite-hardening-p1, merged to local main; not pushed)
source: 9-class read-only design pass (9 agents) + 4 resolved architecture forks (F1-F4)
---

# Roadmap: Suite hardening — move honor-system contracts onto verifiable media

## Objective

The mala-pata suite enforces almost nothing mechanically; it relies on the agent
faithfully following prose loaded into context. The ONLY three real enforcement
primitives that exist today are:

1. **git commit trailers** (`Mala-Pata-Phase/Domain/Roadmap/Lane`) — radars derive state from git.
2. **sdd-init declared fields** (stack, testing-capabilities) — read at runtime.
3. **the Stop-hook output-lint** (`~/.mala-pata/bin/mala-pata-output-lint.py`).

Everything else is honor-system: prose the agent can skip, name-without-reading, or
improvise around. This roadmap moves the highest-leverage honor-system contracts onto a
**verifiable medium** (git / a declared field / a lockfile / a hook) and, where that is
genuinely impossible, writes the explicit recovery/PARK rule.

## Resolved architecture forks (the decisions this roadmap is built on)

| Fork | Decision |
|---|---|
| **F1 — symlink-live** | `_shared` stays **live** (edit canonical = instantly live). NO build-time inlining. Mechanical enforcement via hooks ONLY where there is an output signature (extend output-lint to `structural-labels` + new `enum-lint`). Process-only canonicals get an explicit "re-read from disk on apply" rule. |
| **F2 — mechanism vs prose** | **Mechanize**: atomic `mkdir` per-worktree lock in `platform.md` (+ sub-agent dedup backed by it); consumer RE-DERIVES `lane-gate` and **BLOCKS** on mismatch; restrict the orchestrator's edit-surface so it cannot write source code. |
| **F3 — where policy lives** | One **versioned repo file** `mala-pata/project-policy.md` (sdd-init writes, lanes read). Delivery is a 2-entry rule: passive/docs-only (computed from the diff, reusing the existing `passive` verification tier) -> direct push; code/CI/migration -> declared `code_delivery: pr\|direct`. `direct-merge` becomes a legal value. |
| **F4 — declare run-context** | Orchestrator injects `RUN-MODE: unattended` -> lane PARKs product decisions (reuse `phase-status` `parked` marker + mirror file `mala-pata/parked-decisions/<change>.md`) instead of ask-and-wait; docs declare `branch:` in frontmatter and readers trust it (fallback: scan worktrees). |

## DAG of phases

| # | Phase (racimo) | Classes | Route | Depends on | Parallel with |
|---|---|---|---|---|---|
| P0 | Mirror re-sync (quick win) | — | shot (owned flow) | — | — |
| P1 | `_shared` infra | 2, 3, 6 | mala-pata-skill (owned flow) | — | — |
| P2 | Receipts + resolution | 1, 8 | mala-pata-skill (owned flow) | P1 | P3, P4 |
| P3 | Orchestrators + unattended + lock | 4, 5, 9 | mala-pata-skill (owned flow) | P1 | P2, P4 |
| P4 | Declared policy | 7 | mala-pata-skill (owned flow) | — | P2, P3 |

**Suggested order:** P0 -> P1 -> {P2, P3, P4 in parallel}.
**Parallelizable:** {P2, P3, P4} after P1.
**Each phase runs via the owned `/mala-pata-skill` flow in its OWN isolated worktree** (phase
edit-surfaces overlap across phases), branch-first, Conventional Commit, zero AI attribution,
**no push/PR/merge without the human**.

---

## P0 — Mirror re-sync (quick win)

- **IN:** re-sync the stale repo mirror `_shared/spike-catalog.md` — the live source has the
  `bug` profile row (line 14) that the versioned mirror lacks (VERIFIED: `diff` confirms).
- **OUT:** everything else.
- **Fix shape:** `rsync`/copy the live `~/.agent-skills/_shared/spike-catalog.md` row into the
  mirror (or re-run `deploy-shared.sh`'s mirror step). Trivial, SDD-independent.

## P1 — `_shared` infra (classes 2, 3, 6) — THE BASE, do first

- **IN:**
  - New canonicals: `_shared/phase-kind.md` (`code|ops|spike`), `_shared/delicacy.md`
    (`low|medium|high`), `_shared/verdict-glyphs.md` (set + meaning, done != pass declared).
  - New `bin/mala-pata-enum-lint.py` (sibling of output-lint): fails if a consumer uses an
    enum token without referencing its canonical.
  - Extend `mala-pata-output-lint.py` to cover `structural-labels`.
  - `deploy-shared.sh`: deploy the new canonicals (prefixed symlinks, no inlining); keep the
    "every rule resolves" check; add the enum-lint wiring.
  - Explicit **"re-read `_shared` from disk on apply"** rule for process-only canonicals
    (`lane-gate`, `domain-rule`, `objective-completeness`, `bug-entry-check`).
  - Re-point enum consumers to the single-source canonicals (roadmap, roadmap-orchestrate(-start),
    walkthrough(-start), atlas, radars).
- **OUT:** no build-time inlining; `_shared` stays symlink-live (F1). No `version:` field unless
  a cross-session staleness actually bites.
- **Open decisions (closed by forks):** enum-lint runs at deploy or as Stop-hook — default
  Stop-hook (runtime), consistent with output-lint. Confirm during build.

## P2 — Receipts + resolution (classes 1, 8)

- **IN:**
  - `_shared/lane-gate.md`: consumer RE-DERIVATION rule — organic/loop/shot re-apply the gate on
    the received draft and **REFUSE** if it yields a different lane (F2: blocks, not warns).
  - New trailer `Mala-Pata-Triage: <gate|direct>` in `_shared/git-truth.md` so radars see a
    skipped/direct triage from git. (Note: changes a contract radars consume — high-risk, its own commit.)
  - `triage`: entry gate requiring `mala-pata/research/<slug>.md` with a verdict for `kind: bug`.
  - New `_shared/doc-resolve.md` (worktree-aware resolver: cwd -> `git worktree list` -> declared
    `branch:` via `git show`); the 17 readers reference it; roadmap/kickoff declare `branch:`/`worktree:`.
- **OUT:** loop-specific triage->loop handoff hardening (deferred — see loop-lane flag below).
- **Depends:** P1 (uses the `_shared` single-source conventions).

## P3 — Orchestrators + unattended + lock (classes 4, 5, 9)

- **IN:**
  - New `_shared/platform.md` primitive: atomic `mkdir` per-worktree lock (`<lock-acquire>/<lock-release>`),
    stale-reclaim by pid-liveness/TTL. Replace the sentinel+lsof late-start heuristic with it.
  - New `_shared/unattended-policy.md` (single source: RUN-MODE detection + PARK rule + queue shape).
  - `phase-status.md`: `parked_decisions[]` array; mirror file `mala-pata/parked-decisions/<change>.md`
    for non-orchestrated runs.
  - Both `*-orchestrate-start`: inject `RUN-MODE: unattended`; use the lock; **restrict their
    edit-surface** so they cannot write source code (makes "never live inside a phase cycle"
    verifiable); recovery clause (a merged phase is immutable -> a defect re-enters via triage/bug,
    never fixed in-line); declare the central single-suite-run owner (post-merge).
  - `organic-start`/`triage`/`shot`: PARK under unattended instead of ask-and-wait.
  - `~/.claude/CLAUDE.md`: back the sub-agent dedup rule with the lock.
  - `loop-start`/`organic-start`: ephemeral test-DB fork name with a unique run token.
- **OUT:** loop-specific orchestration (loop lane is out of scope — see flag).
- **Depends:** P1.

## P4 — Declared policy (class 7)

- **IN:**
  - New `mala-pata/project-policy.md` (versioned repo file, single source of project policy).
  - `mala-pata-sdd-init` (SKILL + init-details + agent): detect and WRITE the file; fields
    `integration_base`, `ci:{present,gate}`, `code_delivery:{pr|direct}`, `delivery_strategy`.
  - Kickoffs inherit; `organic-start`/`loop-start` 4.2/4.4 read the policy; orchestrators read it
    for the per-tab prompt and the post-merge CI check.
  - The passive-vs-code classification reuses the existing `passive` verification tier (computed
    from the diff) -> docs-only changes deliver by direct push; code path follows `code_delivery`.
- **OUT (SDD retirement adjustment):** do **NOT** migrate `strict_tdd` — it is a no-op in
  gentle-ai v4 (test-first is the default there). Drop it from the policy file.
- **Depends:** none. Parallelizable.

---

## Coverage (9 classes -> phases)

| Class | What | Phase |
|---|---|---|
| 1 | Handoff without proof token | P2 (lane-gate re-derivation + triage trailer) |
| 2 | `_shared` verbatim not force-read | P1 (hooks where signature + re-read rule) |
| 3 | Stale context between invocations | P1 (re-read rule) + P3 (per-round doc hash recheck) |
| 4 | Unattended mode without policy (PARK) | P3 |
| 5 | Invariant without recovery path | P3 (recovery clause + edit-surface) |
| 6 | Producer/consumer vocabulary drift | P1 (enum canonicals + enum-lint) |
| 7 | Project policy in memory, not a field | P4 |
| 8 | Worktree path assumptions | P2 (doc-resolve) |
| 9 | Advisory guards race / shared-action owner | P3 (atomic lock + central owner) |

## Out of scope (flagged, separate project)

- **loop / SDD lane rework.** gentle-ai v4 removed SDD entirely; the loop lane IS the SDD engine
  (`loop-start` dispatches now-removed `sdd-*` agents). Hardening a lane headed for rework/retirement
  is wasted effort. The loop-lane decision (retire / re-found on ODD / keep) is a SEPARATE project,
  best done alongside the v4 upgrade. This roadmap's mechanisms are lane-agnostic and do NOT depend
  on it; only loop-SPECIFIC hardening (part of class 1 on the triage->loop path) is deferred.

## Notes

- **Branch placement:** this doc was written write-only while on `feature/os-agnostic-launch`.
  It belongs on a durable branch (main/development); commit it there in the normal flow.
- **Risk:** every phase touches shared contracts (`_shared`, trailers, sdd-init, orchestrators,
  CLAUDE.md) = high-risk by ODD definition. None is a "small understood change". Run each phase as
  its own tracked unit via `/mala-pata-skill`, one isolated worktree per phase.

Structure: WBS 100%-rule + dependency DAG + vertical slices. Honor-system -> verifiable-medium +
collision-driven clustering = house method.

## Execution log

- P0: merged feature/mala-pata-bug + feature/os-agnostic-launch to main (unblock).
- P1: enum canonicals (verdict-glyphs/delicacy/phase-kind) + enum-lint (fail-open, --strict) + class-6 wiring + output-lint translated-label check + re-read guard.
- P2: lane-gate consumer re-derivation + doc-resolve canonical + triage bug-cause gate. (git-truth triage trailer deferred.)
- P3: platform atomic mkdir lock + unattended-policy (RUN-MODE/PARK) + phase-status parked_decisions + orchestrate-start edit-surface/recovery. (CLAUDE.md dedup-lock deferred.)
- P4: project-policy declared file (F3 2-entry delivery) + sdd-init writes it.
- enum-lint --strict GREEN; all 28 _shared canonicals deploy-verify clean.
