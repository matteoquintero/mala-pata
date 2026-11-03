---
idea_slug: vsd-as-mala-pata-method
project: mala-pata-skills
domain: mala-pata-suite
roadmap: none
icebox: mala-pata-lanes
verdict: SHARPEN
created_at: 2026-11-02T09:20:00-0500
next: none
size_signal: one-unit
---

# Research: vsd-as-mala-pata-method

## Verdict
**SHARPEN** — "VSD" has no single official meaning and the user did not define it. Under the only reading that matches the suite's grain (vertical slicing), it is **already covered** (RECONSIDER as a *new* methodology); under the other readings it is a different idea entirely. The acronym is a human decision, so the idea cannot be routed yet.

## Discover

### External research: "VSD" candidates (no official name asserted)

| Candidate | What it is | Source | Fit with mala-pata |
|---|---|---|---|
| Vertical Slice Development / Architecture (VSA) | Organize code by feature, as a cross-section through all layers; low coupling between slices, high coupling within one. Coined by Jimmy Bogard in 2018 (blog + NDC Sydney talk). Secondary-source confirmation only; primary blog post not opened. | [jimmybogard.com tag](https://www.jimmybogard.com/tag/vertical-slice-architecture/), [Semantic Anchors summary](https://llm-coding.github.io/Semantic-Anchors/anchor/vertical-slice-architecture), [Packt chapter](https://subscription.packtpub.com/book/web-development/9781803249841/19/ch19lvl1sec04/vertical-slice-architecture) | High, but it is a CODE-STRUCTURE pattern, not a process lane. |
| Value Stream Driven Development (VSDD) | A 2022 PNSQC talk (Kaushal Dalvi, UKG) framing quality attributes as contributors to the value stream. Niche; no broad adoption found. | [PNSQC 2022 paper](https://www.pnsqc.org/docs/Dalvi-Kaushal2022.pdf), [related blog](https://www.mkltesthead.com/2022/) | Low. Adjacent: value stream management (flow metrics, bottlenecks) is tooling-oriented ([GitLab](https://about.gitlab.com/blog/three-steps-to-optimize-software-value-streams/), [Splunk](https://splunk.com/en_us/blog/learn/value-stream-management.html)). |
| Vision and Scope Document | Wiegers' business-requirements deliverable: vision, scope, limits, business risks. | [Wiegers template](https://people.eecs.ku.edu/~saiedian/812/Project/Wiegers-Resources/Chapter%205/Vision%20and%20Scope%20Template.docx), [Jama](https://www.jamasoftware.com/?p=12833) | Overlaps `mala-pata-dossier` (discovery) and research's Heilmeier; a document, not a driven method. |
| Value Sensitive Design (Friedman) | Design methodology integrating human values. | NOT verified: my search returned nothing on it. Listed only as a candidate from the brief. | Unknown / low. |
| Verifiable / other "...-Driven" variants | Not searched; the family is open (TDD, BDD, DDD, ODD, SDD, RDD). | n/a | n/a |

No single authoritative "VSD methodology" exists. The suite's own "drivens" are named with a `-Driven Development` pattern, so a literal VSDD would be "Value Stream Driven" or "Vertical Slice Driven" — still unresolved.

### Code anchoring (reuse-first)
Read live under `/Users/matteoquintero/.agent-skills`:

- `mala-pata-roadmap/SKILL.md` L145-147: "Each phase is a shippable VERTICAL slice — an end-to-end slice that leaves the system working, not a horizontal layer... If the phase cannot be merged and stay green on its own, it is not a valid phase."
- Same file L184-190: the vertical slice is the **fragmentation floor** — each phase must be independently shippable, testable and fit ONE unit; a cut that cannot ship alone is rejected. L273/L374: method = "INVEST / vertical slices + WBS 100%-rule + dependency DAG". L315-317: phase table has a `Vertical slice` column.
- `mala-pata-triage/SKILL.md` L81: a roadmap is warranted only when the objective needs decomposition into several INDEPENDENT vertical slices.
- `mala-pata-research/SKILL.md` L117: size_signal is multi-unit only for genuine independent vertical slices.
- The lanes `organic`/`shot`/`loop` each deliver one unit, and the roadmap's phase = one unit = one lane run. So vertical slicing is the suite's unit-of-work invariant.
- Sibling research `methodology-manager-skill.md` (same icebox) already concluded the evidenced gap is a reference catalog, not a new router/lane; any VSD entry would belong there.

Conclusion: if VSD = Vertical Slice (the dominant reading), the **principle is already embodied** at the planning layer (roadmap/triage/research) and inherited by every lane. Not embodied: a standalone *code-level* convention (organize code by feature, not layers) — that is a project standards matter (`mala-pata-standards` structural layer, named as a future layer), not a lane.

### JTBD and problem size
- JTBD (inferred, unconfirmed): "When I add a method name to my vocabulary, I want to know whether it is a new lane, an existing practice, or just a label, so the suite stays coherent."
- Problem size: small. One naming/placement decision; no code. Single unit (a catalog entry or a standards note at most), no roadmap.

## Heilmeier split
- Answerable from evidence: vertical slicing is already a core concept of roadmap/triage/research (above); no lane would be created by it.
- OPEN (human-only, not invented): which VSD is meant; whether a method label is wanted at all; where it would live.

## Assumption challenge
Premise: "VSD merits becoming its own mala-pata methodology/lane." Evidence against: lanes are defined by work shape (shot/organic/loop/roadmap) and the form gate, not by methodology names; vertical slicing already governs phase validity and the size signal. Consequence if wrong: a redundant lane duplicating triage's routing and the roadmap's slice rule. Verdict on the premise under the Vertical Slice reading: RECONSIDER (already covered). Under other readings: not enough information.

## Define

**What:** Resolve what "VSD" means for mala-pata and, once known, record it in the right place (not a new lane by default).

**Why:** Avoid a redundant methodology while capturing any genuine gap (e.g. a code-structure convention for feature-sliced code).

**DoD:** (a) the acronym is defined by the human with a source; (b) a recorded disposition: already-covered / catalog entry (in the methodology reference decided by `methodology-manager-skill`) / standards-layer note / new lane; (c) no new skill created if disposition is already-covered.

**Decisions made:**
- Vertical slicing is already embodied (roadmap L145-190, triage L81, research L117).
- A new lane is not justified by the Vertical Slice reading.

**Open decisions (human-only):**
1. Which "VSD" is meant (Vertical Slice Development/Architecture, Value Stream Driven, Vision-Scope Document, Value Sensitive Design, other)?
2. If Vertical Slice: is the interest a *code-structure convention* (feed `mala-pata-standards` structural layer) or a *method label* (catalog entry)? Or simply "already covered, close the cube"?
3. Is a literal "-Driven" lane wanted, or is a documented practice enough?

**Risk:** Low. Main risk is inventing a lane that duplicates triage/roadmap, or silently picking a meaning for the acronym.

**size_signal:** one-unit (hypothesis for triage to validate against code; not a verdict).

## Next
Not ready for triage: answer open decision 1 first. If the answer is Vertical Slice and no code-structure interest, close the cube as already-covered; otherwise re-run research with the defined meaning.
