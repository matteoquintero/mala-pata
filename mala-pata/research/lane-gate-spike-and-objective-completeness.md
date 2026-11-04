---
idea_slug: lane-gate-spike-and-objective-completeness
project: mala-pata-skills
domain: mala-pata-suite
roadmap: none
verdict: PROCEED
created_at: 2026-11-03T13:09:36-0500
next: triage
size_signal: multi-unit
---
# Research: lane-gate loop-vs-spike discriminator, spike phase type, and research objective-completeness gate

## Verdict: PROCEED
All three gaps are real in the live skills (cited below), each has a proven methodology behind it, and most of the machinery already exists in `roadmap` and can be lifted rather than invented. Four open owner decisions remain (end of doc), none blocking.

## Raw idea (what you asked)
Fix three structural gaps, domain-neutrally: (1) `research` has no explicit completeness gate; (2) `lane-gate` conflates a scoped design decision with a broad "I don't know how" unknown under `loop`; (3) there is no spike/research-phase type to route an approach-unknown phase to.

Evidence tags: **[S]** verified by fetch/search this session. **[M]** from memory, not re-fetched. **[U]** unsourced / house judgment.

## Problem (generalized)

1. **Completeness is implicit in `research`, and the lanes differ.** `research` Phase 1(f) already says "list what the objective REQUIRES, mark MISSING", but it is explicitly bounded ("single-unit discipline ... a broad domain checklist belongs to roadmap"), has no dimension list, and no test of whether the missing items change the *shape* of the work. An incomplete objective can pass as PROCEED with the missing piece (a screen, a permission model, a migration, an NFR, an integration) undiscovered. The gap is "what is missing", not "what architecture".
2. **`loop` discriminator conflates two unknowns.** `_shared/lane-gate.md` line: "loop - a decision that NEEDS DESIGN: several viable architectures with tradeoffs to investigate, *or options unknowable without exploring*". The second clause is the leak: "unknowable without exploring" covers both (a) a scoped design choice inside one known unit and (b) a broad "I do not know HOW" that reshapes the decomposition. `triage` repeats it ("do I need to investigate/explore to even know the options" -> loop) and `roadmap` Step 4 repeats it ("options that cannot be known without exploring -> loop:PROFILE").
3. **No spike type.** When a roadmap phase or a triage call hits an unknown approach, the only exits are `loop` (full SDD + design + preview, used as a catch-all for "hard") or guessing organic. `research` is read-only and runs *before* triage; nothing routes a phase *back* to it, and `roadmap` has no phase Kind for investigation (Kind today distinguishes code vs ops phases).

## Grounding

### Gap 1 - completeness across ALL dimensions
| Method | Use here | Tag |
|---|---|---|
| Gap analysis (desired vs current state) | The core move: enumerate what the objective requires, subtract what exists, the remainder is the gap | [M] generic; house version already in `roadmap` Step 4-ter |
| User Story Mapping (Patton) | Walk the user's journey end to end and slice horizontally; surfaces missing steps/screens nobody named | [M] Patton, *User Story Mapping* (2014) |
| MECE + WBS 100% rule | Dimension set must be non-overlapping and cover the whole objective; "if not exhaustive, keep looking" | [M] Minto / PMBOK WBS; house version in `roadmap` Step 1 |
| ISO/IEC 25010 quality model | Closed-ish vocabulary for non-functional completeness (performance efficiency, security, reliability, maintainability, compatibility, usability, portability, functional suitability) | [M] standard not re-fetched |
| Jobs-to-be-done | Surfaces user-facing pieces the feature list omits; already in `research` 1(c) and `roadmap` Step 1 | [M]; in-repo |
| Definition of Ready | The handoff gate; `research` already ends with a DoR line | [M]; in-repo |

**Reuse-first (verified by reading the live files):** `roadmap` already has (i) desired-state = human literal + domain canonical feature-set + repo intent docs (Step 1), (ii) MECE + 100% rule (Step 1), (iii) per-dimension inventory against the code (Step 2.2), (iv) gap analysis desired-vs-current with "verify against code before it counts" (Step 4-ter), (v) Level 1 (adjacent-implied) vs Level 2 (broad domain) split, (vi) a coverage table with an "axes in = axes out" check (Step 5). Nothing here needs inventing; research needs a *lightweight* subset with different stopping rule (see Proposal A).

### Gap 2/3 - loop vs spike
| Method | Use here | Tag |
|---|---|---|
| Cynefin (Snowden): Complicated = cause and effect knowable by analysis/expertise, approach sense-analyze-respond, "good practice"; Complex = cause/effect visible only in hindsight, approach probe-sense-respond via small safe-to-fail experiments, "emergent practice" | Direct basis for the discriminator: *can an expert design it now (loop) or must we probe first (spike)?* | **[S]** web search this session (secondary summaries; primary HBR article page fetched but paywalled to the summary) |
| XP Spike (Kent Beck): time-boxed investigation (typically 1-3 days) to reduce uncertainty so a story can be estimated/committed; output is knowledge, the spike code is usually thrown away | The phase type itself; time-box = exit point, then document findings and decide | **[S]** vendor/blog summaries only; primary XP page unreachable (TLS error). Cohn's wording unverified |
| Tracer bullet / walking skeleton (Hunt & Thomas; Cockburn) | Adjacent and different: a thin *production-grade* end-to-end slice that is kept. Use when the approach is *chosen* but integration is unproven; a spike is throwaway knowledge | [M] |
| Risk-Driven Architecture (Fairbanks) | Proportionality: invest design effort only until technical risk falls below other risks; avoids both big-design-up-front and none | **[S]** fetched fairbanks page confirms the principle |
| Architecturally significant requirements | A decision "forks the decomposition" when it is architecturally significant: it changes boundaries/slices | [M] |

Honesty note: Cynefin is a sense-making heuristic, and sources themselves say domain assignment is debatable [S]. The proposal uses it as a *question to ask*, not a classifier that decides.

## Proposal A - research completeness gate (extend `mala-pata-research`, do not replace)

**Where:** a new sub-step `Phase 1(g) - Completeness gate`, immediately after 1(f) (gap to objective). 1(f) stays as the mechanism; (g) adds the dimension sweep and the fork test.

**A.1 Dimension sweep (open list, prompts not a fixed schema).** For the restated objective, ask of each lens "what is MISSING for the objective to be fully reachable?" and record only items that are `MISSING` or `unknown`, each with provenance (`verified` against code/authoritative source vs `inferred`):

- User-facing: screens/states/empty-error-loading, copy, journey steps nobody named (Story-Map walk, JTBD).
- Data: model changes, migrations/backfill, retention, ownership.
- Access: roles, permissions, tenancy, audit.
- Integrations: external systems, contracts, failure/retry behavior.
- Edge cases: concurrency, partial failure, legacy data, limits.
- Non-functional (ISO 25010 as the prompt vocabulary): performance, security, reliability, compatibility, maintainability, usability.
- Operations: observability, config/flags, rollout, rollback, support runbooks.
- Infrastructure: only if the objective demands it.
- `<other>` - the list is explicitly open; add any lens the domain implies. A lens judged irrelevant is recorded `n/a - <reason>`, never silently skipped (this is the MECE "no silent drop" rule).

**A.2 Proportionality (so research does not become a roadmap).** Reuse the existing Level 1 / Level 2 split: only *adjacent-implied* gaps go into the sharpened idea; broad-domain items go to a compact "not covered" checklist. Depth scales with problem size (1d) and stops when remaining unknowns are below the cost of more research (Fairbanks risk-driven stopping rule [S]).

**A.3 The fork test (new, the key addition).** For every MISSING/unknown item ask: *"Does the answer to this change the decomposition (the slices, their order, or their boundaries)?"*
- No -> it is a detail; record in Define as a normal open decision or DoD line.
- Yes -> it is an **approach-fork**. Count it and flag it. One scoped fork inside a single unit -> normal Open decision (candidate loop). A broad fork ("I do not know how to approach this part at all") -> **spike candidate** (see B and C).

**A.4 Verdict wiring.**
- Unverified MISSING items that only the human can answer -> SHARPEN (existing behavior).
- Objective cannot be reached without a broad approach-fork -> PROCEED is still allowed, but `size_signal: multi-unit`, `next: triage`, and Define carries `Spike candidates: <list>`; triage/roadmap decide (research must not route).
- Add one DoR line: `Completeness: lenses swept N - missing M - forks F (spike candidates S)`.

**Lift from `roadmap` (do not rewrite):** the three-source desired state, MECE/100% rule, "verify each against code before it counts", Level 1/2 split, silent-drop rule. Because both skills need it, the cleanest reuse is to move the dimension list + fork test into a shared file `_shared/objective-completeness.md` (pattern already used by `lane-gate.md` and `mala-pata-domain-rule.md`) and have `research` and `roadmap` Step 1 both point at it verbatim. [U: house-pattern judgment]

## Proposal B - lane-gate loop-vs-spike discriminator

Replace the `loop` bullet and the discriminator's "Needs design" clause in `_shared/lane-gate.md`. Proposed wording:

> - **loop** - a SCOPED design decision: the unit's boundaries are known, and the open question is *which* of several viable designs fits (tradeoffs to weigh). An expert could lay out the options now. May be standalone or a phase inside a roadmap.
> - **spike (research)** - a BROAD approach-unknown: you do not know HOW to do it, the answer would change what the units even are, and the options cannot be listed without probing (prototype, measurement, reading an unfamiliar system, vendor/feasibility check). Not a lane that ships; it produces knowledge, then re-enters the pipeline.

Discriminator test (Cynefin-derived), asked in order:
1. *Can I state the options and does one answer close them?* -> yes: NOT loop (organic/shot). (Unchanged.)
2. *Can an expert design it NOW from known practice, with the unit's boundaries already fixed?* -> yes: **loop** (complicated: analyze, then decide). Standalone is fine.
3. *Must we PROBE before the options or the boundaries are even known, or would the answer reshape the decomposition?* -> yes: **spike/research**, not loop (complex: probe, sense, respond).
4. Breadth, not roadmap-membership, is the axis: a loop is still valid standalone for a scoped design-heavy single unit. "Hard" or "big" alone is neither loop nor spike.

Rule of thumb to add: *"I do not know how" never routes to loop. "I know the shape, I must choose among designs" does.* Replace the clause "or options unknowable without exploring" (it is the leak) with "or the design space is known but the choice has tradeoffs". Keep "loop is the heaviest lane" language.

Propagation (same sentence, single source of truth): `triage` Phase 2 open-decision bullet, `roadmap` Step 4 tentative-route bullet, and `research` Phase 3 already say "apply lane-gate verbatim", so the main edit is one file plus removal of the duplicated "options not known without exploring" phrasing in triage and roadmap so they stop contradicting it.

Caveat to state in the rule: when the test is borderline, default to asking ONE question (existing triage behavior) rather than guessing the Cynefin domain [S: domain assignment is debatable].

## Proposal C - the spike / research-phase type

**Definition.** A *spike* is a time-boxed, read-mostly investigation whose deliverable is **a decision-grade finding**, not shipped code. Exit = a resolved approach (or a "not feasible / reconsider" finding) that the originating phase can then route to organic/loop/roadmap. Spike code is disposable unless the finding says "promote this as a tracer bullet", in which case a normal lane implements it properly.

**Reuse, do not add a skill if avoidable.** The investigative machinery is `/mala-pata-research` (read-only, always writes a doc, has a verdict). Minimal new surface:
- `research` gains a **spike mode**: input is a *question* (not a raw idea), with a **time-box** (e.g. 1-3 working sessions [S as typical range]) and an **exit criterion** ("we can name the approach and the slices", or "proved infeasible"). Output is the same research doc with `kind: spike` in frontmatter and a fixed `## Finding` section: chosen approach / rejected options with evidence / residual unknowns / effect on decomposition.
- Allowed to include throwaway code only if the owner approves it (research is read-only today; whether spike may write a scratch branch is Open Decision 2).

**Routing in (three entry points, all produce the same handoff):**
1. **triage:** after the Phase 2 open-decision test, a new outcome `-> run /mala-pata-research --spike "<question>"`, with the draft of fields and the specific unknown named. Reason line: `Reason: approach unknown, a probe is required before options can be listed`.
2. **roadmap Step 4:** a phase may have `Kind: spike` (alongside the current code/ops Kinds) and tentative route `spike`, blocking its dependents. Rule: a phase whose approach is unknown is **split** into `spike -> implementation phase(s)` instead of being forced to loop. The loop-count minimization rule keeps working. If the broad unknown affects the whole objective (not one phase), roadmap bounces to research instead of writing a DAG (mirrors the existing "collapsed to one unit, bounce to triage" rule).
3. **research (self):** the A.3 fork test emits `Spike candidates` in Define.

**Re-entry.** Spike finding -> `triage` (always triage decides the lane, house rule). Triage reads the finding as research (Phase 0.5 already reads and synthesizes research docs; a spike doc is one more). Effects:
- Approach now known and scoped -> organic or loop on the original phase.
- Decomposition changed -> roadmap re-decomposes (the spike's `effect on decomposition` field is its input); the roadmap re-runs the 4-ter gap check against the new picture.
- Infeasible/too costly -> RECONSIDER, kill or pivot (existing verdict semantic).
Guard against loops of spikes: a phase may be spiked at most once without an explicit human decision (anti-ceremony), and a spike with no exit criterion is refused.

**Adjacent, kept distinct.** Tracer bullet / walking skeleton is *not* a spike: it is a kept, thin production slice for integration risk once an approach is chosen; it maps to an ordinary organic/loop phase placed first in the DAG. Mention in roadmap Step 4 as a slicing tactic. [M]

## Structure line
Gap analysis (desired vs current) + MECE/100% rule + ISO/IEC 25010 prompts + Story-Map walk (completeness); Cynefin complicated-vs-complex test + XP Spike (loop vs spike); Risk-Driven Architecture proportionality; house reuse of `roadmap` Step 1 / 4-ter and the shared-rule pattern (`_shared/`).

## Reuse summary (what is lifted, what is new)
| Item | Source | Status |
|---|---|---|
| Three-source desired state, MECE/100%, silent-drop rule | `roadmap` Step 1, Step 5 | Lift (via shared file) |
| Desired-vs-current gap, verify-against-code | `roadmap` Step 4-ter | Lift (light subset) |
| Level 1 / Level 2 proportionality | `roadmap` Step 4-ter | Lift |
| JTBD, Heilmeier, DoR, problem size | `research` | Already present; reference |
| "Bounce when it collapses to one unit" | `roadmap` hard rule #2 | Mirror for spike bounce |
| Dimension sweep list | new, open list | New (small) |
| Fork test | new | New (small, the key idea) |
| Cynefin question in lane-gate | new wording | New (edit) |
| Spike mode + `Kind: spike` + triage outcome | new | New (smallest viable) |

## Open decisions for the owner
1. **Home of the completeness rule:** new `_shared/objective-completeness.md` referenced by research and roadmap (recommended, matches `lane-gate.md` pattern), or inline in research only?
2. **Spike write authority:** read-only investigation (docs, measurement, reading) only, or may a spike write throwaway code on a scratch branch? Recommendation: read-only default, throwaway code only with explicit owner approval.
3. **Spike as new skill vs `research --spike` mode:** recommended mode (reuse); a dedicated `/mala-pata-spike` only if the doc template diverges enough to hurt.
4. **Default time-box:** suggest 1-3 sessions with a mandatory exit criterion; confirm or set your own.

Delivery note: this is multi-unit (lane-gate edit, research edit, roadmap edit, triage edit, optional shared file) but each is small and doc-only. Triage owns the roadmap-or-not call; a likely single `organic` per skill or one organic across the four SKILL.md files, since decisions are resolved once 1-4 above are answered.

## Sources
- Cynefin summaries (complicated: sense-analyze-respond / good practice; complex: probe-sense-respond / emergent practice; caveat that domain assignment is debatable): ModelThinkers, Consortium for Service Innovation, Wikipedia (search results [S]; direct fetches of Wikipedia/HBR failed or were paywalled).
- Agile spike definition, 1-3 day time-box, XP origin: aggregated vendor/blog results [S]; primary XP site unreachable (certificate error), Cohn wording unverified.
- Fairbanks risk-driven model: georgefairbanks.com [S].
- Patton, ISO/IEC 25010, Minto/WBS, Hunt & Thomas, Cockburn: [M], not fetched.
- Live skills read: `_shared/lane-gate.md`, `mala-pata-research/SKILL.md` (v1.17.2), `mala-pata-roadmap/SKILL.md`, `mala-pata-triage/SKILL.md`.
- Search results contained no embedded instructions.

## Handoff
-> `/mala-pata-triage lane-gate-spike-and-objective-completeness` after the owner answers open decisions 1-4.
