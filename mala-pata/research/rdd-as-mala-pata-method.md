---
idea_slug: rdd-as-mala-pata-method
project: mala-pata-skills
domain: mala-pata-suite
roadmap: none
icebox: mala-pata-lanes
verdict: RECONSIDER
created_at: 2026-11-02T09:19:59-0500
next: none
size_signal: shot
---

# Research: rdd-as-mala-pata-method

## Verdict
**RECONSIDER** — if "RDD" means Receipt-Driven Development, it already exists and is already wired into the suite as a per-commit check inside the ODD lanes. There is no lane or skill left to create. The only residual gap is documentation, which belongs to cube c1 (`methodology-manager-skill`). Not ready for triage as its own item; close c5 as "already covered" unless the owner meant a different RDD.

## Discover

### Code anchoring (reuse-first)
Read live under `~/.agent-skills/mala-pata-*` (grep for `RDD|receipt-driven|gentle-ai review`, 12 skills hit):

| Where | What it does with RDD |
|---|---|
| `mala-pata-organic-start/SKILL.md` | Hard rule #2: "RDD lives here, per work-unit commit." After each commit, if RDD is on: `gentle-ai review assess --cwd <worktree> --agent claude-code --base-ref <last reviewed boundary> --committed-only --json`, read `review_due`, run `next_transition.command` verbatim. Close table has an "RDD per commit" row. Defers all detail to the global CLAUDE.md ODD protocol. |
| `mala-pata-shot/SKILL.md` | Work-unit commit step: if RDD is on, run `gentle-ai review assess --cwd <repo> --json` and follow the native plan (usually passive for trivial changes). Close table has an RDD row. |
| `mala-pata-loop-start/SKILL.md` | Explicit boundary: "RDD still does not run in the SDD cycle — it belongs to the organic/ODD lane"; section 4.3 is "no RDD Gate in the SDD cycle". |
| `mala-pata-organic`, `-orchestrate`, `-orchestrate-start`, `mala-pata-roadmap-orchestrate(-start)` | Reference per-commit RDD and surface its outcome in merge-gate tables. |
| Global CLAUDE.md: `## Receipt-driven development is user-owned`, ODD protocol step 6, "Delegated Verification Gate", "Review Execution Contract" | Defines the switch `gentle-ai review mode enable|disable|status` (on by default, opt-out), per-commit assess, candidate consent, lifecycle. This is the source of truth; the skills say CLAUDE.md wins on conflict. |

Mapping that already holds: SDD -> `loop`, ODD -> `organic`/`shot`, RDD -> the review switch evaluated per work-unit commit inside ODD lanes (and deliberately absent from SDD). Related cube c1 already records that RDD "exists as a switch, not as a documented methodology entry", and c5 is flagged there as partially stale.

### External research
- Receipt-Driven Development is a gentle-ai concept. Its README describes it as on by default and opt-out via `gentle-ai review mode disable` ([README](https://raw.githubusercontent.com/Gentleman-Programming/gentle-ai/main/README.md)). The v3.0.0 notes say RDD was removed from the SDD lifecycle and became a separate user-owned review switch ([release v3.0.0](https://newreleases.io/project/github/Gentleman-Programming/gentle-ai/release/v3.0.0)). Earlier it was marketed as "Organic RDD" (v2.2.0). A receipt is described as an authorization tied to the exact fingerprint of a set of changes ([article](https://ai.plainenglish.io/we-keep-asking-ai-if-the-code-works-were-asking-the-wrong-question-612760c31669)). Sources are project materials and author posts, not independent evaluations.
- Acronym collision: **README-Driven Development** (Tom Preston-Werner, 2010: write the README before the code) is also "RDD" ([ponyfoo summary](https://ponyfoo.com/articles/readme-driven-development), [Simon Willison](https://simonwillison.net/2010/Aug/23/readme)). A third candidate, Responsibility-Driven Design (Wirfs-Brock), is a design method, not "development"; I did not verify it by search, so it is listed from background knowledge only.
- Related, not equivalent: README-Driven Development overlaps with what the suite already does through kickoff docs (What/Why/DoD written before code) and `mala-pata-research`.

### JTBD
"When I write 'RDD' in the idea pool, I want to know whether it needs work or is already handled." Evidence level: the cube text is one line with no definition, so the intent is inferred. Problem size: tiny, episodic; no incident evidence.

## Heilmeier

| Question | Answer | Source |
|---|---|---|
| What are you trying to do? | Decide whether RDD becomes a mala-pata methodology/lane. | Cube c5. |
| How is it done today? | Receipt-Driven: switch + per-commit assess in organic/shot, excluded from loop; defined in global CLAUDE.md. | Code (verified). |
| What is new? | Nothing new if Receipt-Driven. A lane or skill would duplicate the switch and the lane gate. | Reasoned. |
| Risks? | Creating a second, competing definition of RDD; wrong-acronym work (README-Driven). | Reasoned. |
| Cost? | Zero for existence; at most a catalog entry via c1. | Estimate. |
| HUMAN-ONLY decision | Which RDD did you mean? | OPEN below. |

## Define (draft)
- **What:** Resolve cube c5: either confirm RDD = Receipt-Driven (already built, close the cube) or identify a different intended method and re-scope.
- **Why:** The suite already evaluates RDD per commit; leaving c5 open invites duplicate work and a second definition.
- **DoD:**
  - Given the owner confirms Receipt-Driven, When c5 is reviewed, Then it is closed as covered, with the mapping SDD->loop, ODD->organic/shot, RDD->review switch recorded in c1's catalog entry (no new lane or skill).
  - Given the owner meant another RDD, When re-researched, Then a new research doc exists for that meaning.
- **Decisions made:** No new lane/skill for Receipt-Driven; RDD stays out of the SDD cycle (as loop-start already states); routing stays with triage + lane-gate.
- **Open decisions:** (1) Which RDD did you mean: Receipt-Driven (already built), README-Driven, Responsibility-Driven, or something else? Everything else depends on this.
- **Risk:** Low. Main risk is manufacturing work that already exists.
- **size_signal:** shot (at most a one-line catalog/doc entry, carried by c1).

## Assumption challenge
**Premise: "RDD needs to become a methodology."** Evidence against, if Receipt-Driven: it is a user-owned switch with no lane of its own by design (CLAUDE.md "Receipt-driven development is user-owned"), it is already invoked in `organic-start`, `shot` and the orchestrators, and the loop lane intentionally excludes it. Promoting it to a lane would contradict that design. Evidence for work: only documentation (c1). Evidence gap: I could not confirm the owner's intent; the cube is a single line.

## DoR
What ✓ · DoD ✓ · Decisions ✗ (which RDD).

## Handoff
`next: none`. Ask the owner the single open question. If Receipt-Driven: close c5 as covered and let c1 absorb the catalog line. If another meaning: re-run `/mala-pata-research` for it.

Structure: Double Diamond (Discover/Define) + Heilmeier Catechism + Definition of Ready.
