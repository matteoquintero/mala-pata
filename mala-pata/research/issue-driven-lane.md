---
idea_slug: issue-driven-lane
project: mala-pata-skills
domain: mala-pata-suite
roadmap: none
verdict: SHARPEN
created_at: 2026-11-04T17:33:44-0500
next: triage
size_signal: small (an optional work-type tag + one triage check; NOT a lane, NOT a roadmap)
---

# Issue-Driven: a new lane, or an entry criterion?

Evidence tags: [L] read live in the suite this session; [M] model memory, NOT fetched or verified this session; [U] no source found.
No web fetch was done for this doc. All external claims are [M] and flagged as such.

## Verdict: SHARPEN
Do NOT add an "Issue-Driven" lane. It is a different axis (work-type / origin), not size x uncertainty. The real value is a `kind: bug` tag plus a bug-specific entry check (reproduce first, regression test as the DoD), routed through the existing lanes. The owner must still decide whether the tag lives in triage output only or also in the kickoff frontmatter (open decision 1).

## Raw question
"When we are sure it is an issue, not an improvement, not new functionality" - does that merit a new lane?

## 1. What Issue-Driven Development is (standalone)
- **Core idea** [M]: the tracker issue is the unit of work. The issue exists before the code, one branch / one PR per issue, and the PR closes the issue (closing keywords, e.g. "Fixes #N"). Traceability runs requirement -> issue -> branch -> PR -> release note.
- **Related, better-documented practices** [M]: Ticket-Driven Development (same idea with a ticket tool), GitHub Flow (branch per unit, PR, merge), trunk-based "small PR per ticket", and the classic ITIL / defect-tracking split between *incident/defect* and *change/enhancement* [M].
- **Source quality: weak.** "Issue-Driven Development" is an informal community label, not a standard or a published method. No authoritative definition was found [U]. It is mostly a description of how GitHub/GitLab-centered teams work. Treat it as a workflow convention, not a methodology with evidence of outcomes.
- **Key property**: it is a statement about *where the unit of work is recorded and how it is closed*. It says nothing about how big or how uncertain the work is. That matters for section 4.

## 2. What already covers bug work in the suite [L]
- `_shared/lane-gate.md`: lanes are chosen by form gate (What / DoD / Decisions) then SIZE x UNCERTAINTY: shot, organic, loop, spike, roadmap. Nothing in the gate reads work-type. A bug is not mentioned.
- `mala-pata-shot`: explicitly lists "a one-line fix" as its example. Bug fixes of the smallest size are already a shot.
- `mala-pata-organic`: branch-type step already advises `feature/ | fix/ | hotfix/ | refactor/ | chore/ | docs/`, so work-type already exists as a *branch naming attribute*, orthogonal to the lane. The kickoff already has What / Why / Done (Given/When/Then) / Decisions / Risk; for a bug, "Done" is naturally "the failing behavior no longer occurs".
- `mala-pata-triage`: no bug/kind handling found (grep for bug, fix, issue, kind, hotfix returns only unrelated hits). Triage does not capture work-type today.
- `issue-creation` skill (Gentle AI, not mala-pata) [L]: handles bug reports vs feature requests and approval labels. It owns the *tracker-side* artifact.
- `branch-pr` skill (Gentle AI) [L]: enforces issue-first PRs, `fix/<description>` branches and exactly one `type:bug` label. It owns the *PR-side* artifact and already encodes "issue exists before code, PR closes it".
- Conclusion of the reuse check: the issue-first / one-PR-per-issue / PR-closes-issue mechanics are already implemented by `issue-creation` + `branch-pr`. What is missing is only (a) a `kind` signal at triage and (b) bug-specific discipline inside the lanes (reproduce first).

## 3. Overlap with existing skills (honest)
- Issue-Driven's whole mechanical content (issue before code, one PR per issue, close on merge) overlaps ~fully with `issue-creation` + `branch-pr`. A new lane would duplicate them.
- Its "sure it is a defect, not an improvement" classification is the only new element, and it is a *classification question*, not an execution path.

## 4. The core tension

### Argument FOR a new lane
- Bugs do have a distinct process: reproduce, find root cause, regression test, often a hotfix path. A named entry could make that discipline visible and consistent.
- Owners already think in "this is an issue" terms; a front-door label would match how work arrives (from a tracker).
- A lane gives a place to hang bug-specific steps (reproduction capture, regression-test DoD) so they are not forgotten.

### Argument AGAINST (stronger)
- **Wrong axis.** Lanes classify SIZE x UNCERTAINTY. A bug is spread across the whole space: a one-line fix is a `shot`; a bug with a stated repro and obvious fix is `organic`; a bug whose fix needs a design choice (e.g. concurrency, data-model flaw) is `loop`; a bug whose cause is unknown is a `spike`; a systemic defect cluster may be a `roadmap`. A single "Issue-Driven" lane would have to either duplicate all five lanes or collapse them, breaking the discriminators in `lane-gate.md` ("size alone never forces a heavier route").
- **It would add a second, orthogonal axis (work-origin/type) into a gate whose single job is routing by size x uncertainty.** Every lane-touching skill applies the gate "verbatim"; adding a type axis means changing a single source of truth and its eight consumers.
- **The unique risk is epistemic, and it is already handled.** "Sure it's a bug, not an improvement" is the Form gate's What/DoD test restated: a bug has an expected-vs-actual that can be written as Given/When/Then. If it cannot be stated, it fails the gate or is a spike.
- **Overlap.** Issue-first, branch-per-issue and PR-closes-issue are already enforced by `branch-pr` / `issue-creation`.
- **Risk of mis-trust.** "We are sure it is a bug" is a human certainty claim; a lane that skips questions because of it invites the wrong fix (symptom patched, root cause missed).

### Conclusion of the tension
Issue-Driven is a **work-type / origin attribute**, not a point on the size x uncertainty plane. It belongs as a tag plus an entry check that still routes through the existing lanes. A new lane would break the axis.

## 5. Options compared
| Option | What it is | Verdict |
|---|---|---|
| A. New lane `issue` | Separate path for bugs | No: orthogonal axis, duplicates five lanes, changes the single-source gate, overlaps `branch-pr`/`issue-creation`. |
| B. Entry criterion on shot/organic only | "If a bug is trivial, shot; if stated, organic" | Partly right but already true today; adds nothing by itself and ignores loop/spike bugs. |
| C. `kind: bug` tag (recommended) | Triage records work-type; lane still chosen by gate; bug-specific entry check applies in whichever lane | Yes: adds the missing signal without touching the gate. |
| D. Do nothing | Rely on `fix/` branch type | Acceptable fallback; loses the reproduce-first and regression-DoD prompt. |

## 6. Recommendation: C, a `kind` tag + bug entry check (not a lane)
- **Triage** records an optional `kind: bug | feature | chore | ...` as a non-routing field, same status as the `size-hint` (never routes).
- **Bug entry check** (applied in whichever lane the gate picks):
  1. A reproduction (or a stated expected-vs-actual) exists before code. Cannot reproduce -> spike, not organic.
  2. The DoD includes a regression test that fails before the fix and passes after (fits the Strict TDD RED step).
  3. The tracker issue is linked in the kickoff and the PR; `branch-pr` / `issue-creation` own the issue/PR mechanics (reuse, do not reimplement).
  4. Branch type = `fix/` (or `hotfix/` for production urgency); that already exists in `mala-pata-organic`.
- **"Sure it's an issue, not improvement"**: treat as a triage question with evidence (repro or documented intended behavior), not as a bypass of the form gate.
- Escalation stays lane-gate-driven: a "bug" that needs design is a loop; one with unknown cause is a spike.

## 7. Open decisions for the owner
1. Where does `kind` live: triage output only, or also in kickoff frontmatter (so `domain-radar` could group bugs)? Affects `mala-pata-triage`, `mala-pata-organic`, `mala-pata-domain-radar`.
2. Does the bug entry check live in `_shared/` as a small shared note (consumed by shot + organic) or inline in each skill? Preference: shared, to avoid drift.
3. Is a `hotfix` (production-urgent) a separate concern worth its own note, or out of scope? It is urgency, a third axis, and should not be folded into this decision.
4. Should the issue link be mandatory in the kickoff, or only when a tracker exists? (`issue-creation` assumes GitHub; the suite is tracker-neutral.)

## 8. Sources and quality
- [L] `_shared/lane-gate.md`, `mala-pata-shot`, `mala-pata-organic`, `mala-pata-triage`, `issue-creation`, `branch-pr` (read this session).
- [M] Issue-/Ticket-Driven Development as an informal community practice; GitHub Flow; ITIL defect-vs-change split. Not fetched; low-to-medium reliability, community-level, no outcome evidence.
- [U] No authoritative or empirical source defining "Issue-Driven Development" as a methodology.
