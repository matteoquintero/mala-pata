---
idea_slug: methodology-manager-skill
project: mala-pata-skills
domain: mala-pata-suite
roadmap: none
icebox: mala-pata-lanes
verdict: SHARPEN
created_at: 2026-11-02T09:18:59-0500
next: none
size_signal: one-unit
---

# Research: methodology-manager-skill

## Verdict
**SHARPEN** — the need (one place that knows the drivens) is real, but a *router/manager skill* would duplicate `mala-pata-triage` + `_shared/lane-gate.md`; the evidenced gap is a **reference catalog**, and the form (shared doc vs. skill) is a human decision. Not ready for triage until the open decisions below are answered.

## Discover

### Code anchoring (reuse-first)
Inventory of what already overlaps (read live, 44 `mala-pata-*` skills under `~/.agent-skills`):

| Existing mechanism | What it covers | Covers "catalog of drivens"? |
|---|---|---|
| `mala-pata-triage` + `_shared/lane-gate.md` | Routes a CHANGE to a lane (shot/organic/loop/roadmap) by the form gate (What/DoD/Decisions). The discriminator is "does the decision need DESIGN", not "which methodology". | No. It routes by *work shape*, never by methodology name. |
| `mala-pata-loop` / `-start` | The SDD lane (gentle-ai SDD). | Implements one methodology; does not describe others. |
| `mala-pata-organic` / `-start` | The ODD lane. | Same. |
| RDD (`gentle-ai review mode enable\|disable\|status`, referenced in 59 places across the skills) | Receipt-Driven Development as a user-owned switch. | Exists as a *switch*, not as a documented methodology entry. |
| `mala-pata-skill` | Authoring path for skills (domain-neutral, context-leak gate). | Would be the path to author any new skill/doc. |

Evidence of the gap: `grep -ri methodolog` over all mala-pata skills and `_shared/` returns **zero** hits. No artifact states "mala-pata supports SDD, ODD, RDD; EDD/IDD/CDD/VSD are not adopted, because X". The mapping methodology -> lane/skill lives only in the author's head and the global CLAUDE.md.

Related icebox cubes (same pool `mala-pata-lanes`): c2-c6 each ask "does EDD / IDD / CDD / RDD / VSD become a mala-pata methodology?" and c7 asks to rename `loop`. c1 (this idea) is the index those would populate; c5 is partially stale, since RDD already exists as a switch (the open question there is documentation, not existence).

### Does triage already "manage" methodologies?
Partially, by accident: lanes = methodologies (loop=SDD, organic=ODD), and triage picks between them. But triage is a *per-request decision skill* with a fixed output shape; it does not enumerate, define, or compare methodologies, and it knows nothing of RDD/EDD/IDD/CDD/VSD. A separate "manager that routes" would create a second router competing with the lane gate (lane-gate.md states it is the single source of truth and must never be re-derived). So: **redundant as a router, absent as a catalog.**

### External research (light, one search)
- "A catalog of `*-driven development` styles" is a known pattern: Wikipedia's [List of software development philosophies](https://Www.Wikipedia.org/wiki/List_of_software_development_philosophies) and several blog catalogs (e.g. [“Driven Development” styles](https://guilde-llimes.github.io/posts/x-driven-development-styles), [Driven by Acronyms](https://www.ozimmer.ch/index/2020/10/30/DrivenByTLAs.html)) exist. They are descriptive lists, not executable handlers.
- **Acronym collisions are the main hazard**: Wikipedia lists *Readme*-Driven Development as RDD (mala-pata's RDD is *Receipt*-Driven); CDD appears as *Configuration*-Driven Development (and Contract-driven in other sources); DDD is Domain/Data. SDD is explicitly "not standardized" across sources. Source quality is low (blogs, informal lists); no primary-source standard exists. EDD, IDD and VSD were not found as established terms in this single search, so their meanings here are **unverified** (see Open decisions).
- Implication: a catalog's value is not listing names (the web already does) but pinning *mala-pata's own definition* of each acronym and its mapping to a lane, so the collisions cannot be misread.

### JTBD
"When I (or an agent) meet or invent a `*DD` term, I want one authoritative place saying what it means in mala-pata and which lane/skill/switch (if any) embodies it, so I stop re-deciding or mis-routing it." Who: the single owner/maintainer (personal suite) and agents loading context (a cheap lookup instead of reconstructing from CLAUDE.md). Secondary: onboarding/documentation. Evidence level: inferred from the icebox cubes c2-c6, not from observed incidents.

### Problem size
- Scope: suite-wide but read-only knowledge; touches no lane behavior.
- Frequency: low, episodic (when a new methodology is considered; seven cubes are frozen on exactly this question today).
- Severity: low-medium. No data loss or wrong code; the cost is repeated re-decision and acronym confusion (RDD already means two things across the web). No incident evidence found in the repo; severity is an estimate.

## Heilmeier

| Question | Answer | Source |
|---|---|---|
| What are you trying to do? | Give mala-pata one authoritative index of the `*DD` methodologies: mala-pata's definition, status (adopted / considered / rejected) and lane/skill/switch mapping. | Derived from the ask. |
| How is it done today and what are the limits? | Implicitly: lanes encode SDD/ODD, RDD is a switch, the rest are undocumented; triage routes by work shape. No catalog exists (zero `methodolog` hits). | Code (verified). |
| What is new and why will it work? | A single catalog gives c2-c6 a place to land and fixes acronym meanings. | Reasoned. |
| Who cares / what difference? | The owner and loading agents; fewer re-decisions. | Inferred. |
| Risks? | Duplicating triage (second router); definitions drifting from the lanes; scope creep into adopting every acronym; skill bloat (44 already). | Code + reasoning. |
| Cost / time? | One unit if it is a reference doc; larger only if it grows routing behavior. | Estimate. |
| Midterm / final exams? | Midterm: every in-scope acronym has a definition + lane mapping. Final: triage/loop/organic consumers can cite it with no contradiction. | Draft. |
| HUMAN-ONLY decisions | See Open decisions. | — |

## Define (draft)

- **What:** Produce one authoritative catalog of the `*DD` methodologies for mala-pata: for each, mala-pata's own definition, status (adopted / considered / rejected), and the lane, skill or switch that embodies it (SDD -> loop, ODD -> organic, RDD -> review switch; others per human decision).
- **Why:** Seven frozen cubes ask about individual methodologies with no place to record the answer; acronyms collide (RDD, CDD, DDD) and today the mapping lives only in the author's head and global instructions.
- **DoD:**
  - Given the catalog exists, When an agent or the owner looks up SDD, ODD or RDD, Then each shows definition, status and its lane/skill/switch, matching the live lanes.
  - Given an acronym that collides with an external meaning (RDD, CDD), When looked up, Then the entry states mala-pata's meaning and names the colliding meaning.
  - Given triage is invoked, When it routes a change, Then its behavior is unchanged (the catalog adds no routing step).
- **Decisions made:**
  - It must NOT become a second router; routing stays with triage + `_shared/lane-gate.md`.
  - Content must stay domain-neutral (suite-authoring invariant).
  - Authoring, if a skill is created, goes through `/mala-pata-skill`.
- **Open decisions:** see below.
- **Risk:** Low blast radius (read-only knowledge). Main risk: drift from the lanes and silent re-introduction of routing logic.
- **size_signal:** one-unit (as a reference artifact). Would become multi-unit only if the human chooses a handler with behavior.

### Open decisions (human-only, NOT invented)
1. **Form:** (a) a shared reference doc `_shared/methodologies.md` consumed by triage/research (no new skill), (b) a read-only lookup skill, or (c) a decision-helper that recommends a methodology? Evidence favors (a): zero routing need was found, and a skill adds to a 44-skill surface. Needs the owner's call.
2. **v1 scope:** which acronyms are in? SDD, ODD, RDD are verifiable in the suite today. EDD, IDD, CDD, VSD have **no definition in the repo and no confirmed meaning from this research**; the owner must state what each means (and whether CDD is Configuration-, Contract- or something else) before anything is written.
3. **Status vocabulary:** adopted / considered / rejected, or something else?
4. **Relationship to c2-c7:** does the catalog subsume the per-methodology cubes (decide inside the catalog) or stay a pure index while each cube still gets its own decision? And does `loop` renaming (c7) happen first, since the catalog would cite lane names?

## Assumption challenge
**Premise: "a NEW skill is warranted."** Evidence against: (1) triage + lane-gate already own routing and declare themselves the single source; (2) skills here are verbs/executors or auditors, while a catalog is a noun/reference, which in this suite lives in `_shared/` (lane-gate, domain-rule, git-truth); (3) the web already lists generic `*DD` names, so the unique value is only mala-pata's own mapping, which is small (3 verified entries). Evidence for a skill: discoverability via description triggers, which `_shared/` docs lack unless a skill points to them. Net: a new *manager/handler* skill is **not justified by current evidence**; a shared reference (optionally with a one-line pointer from triage/research) covers the gap. This is why the verdict is SHARPEN, not PROCEED. Gap in evidence: no observed incident of mis-routing or lost context; the JTBD is inferred from the icebox, not measured.

## DoR
What ✓ · DoD ✓ · Decisions ✗ (form and v1 scope unresolved; EDD/IDD/CDD/VSD meanings unknown)

## Handoff
`next: none` — answer Open decisions 1 and 2 first (the owner, one at a time), then re-run `/mala-pata-research` or go to `/mala-pata-triage` with the resolved draft. Likely lane once resolved as a reference doc: organic (or shot if tiny), authored via `/mala-pata-skill` if a skill form is chosen.

Structure: Double Diamond (Discover/Define) + Heilmeier Catechism + Definition of Ready.
