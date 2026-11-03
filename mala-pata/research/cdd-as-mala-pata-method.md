---
idea_slug: cdd-as-mala-pata-method
project: mala-pata-skills
domain: mala-pata-suite
roadmap: none
icebox: mala-pata-lanes
verdict: SHARPEN
created_at: 2026-11-02T09:19:50-0500
next: none (SHARPEN)
size_signal: one-unit
---
# Research: CDD as a mala-pata methodology (icebox cube c4)
## Verdict: SHARPEN
"CDD" has no single established meaning (at least three live, unrelated expansions) and the human never said which one; the three candidates also relate to mala-pata very differently, so the lane/skill question cannot be answered until "which CDD?" is answered.

## Raw idea (what you asked)
"CDD · decide whether and how it becomes a mala-pata methodology (which lane/skill, if any)". The acronym and its source were not defined.

## Discover
### How it's done today + limits (with sources)
"CDD" is ambiguous. Candidates found (no canonical standard found for any of them):

| Candidate | What it is | Practice | Sources |
|---|---|---|---|
| Component-Driven Development | Bottom-up UI method: build components in isolation, write a "story" per variation, compose into larger components, then pages. Described as "Visual TDD". Tooling-bound (isolated workshop, a11y/interaction/visual tests). | UI-only; strongest and most mature use of the exact acronym in the frontend world. | https://storybook.js.org/docs/why-storybook ; https://storybook.js.org/docs/react/why-storybook ; https://lindanthillanayagam.substack.com/p/adopting-component-driven-development |
| Contract-Driven Development | API structure defined BEFORE implementation; both sides agree on the contract; mocks generated; enforced by schema validation + contract tests (consumer-driven e.g. Pact, or provider-driven e.g. OpenAPI). Related but not identical to "consumer-driven contracts" (a testing pattern). | Cross-boundary systems; the acronym "CDD" is used loosely here, CDC (consumer-driven contracts) is the better-established term. | https://microsoft.github.io/code-with-engineering-playbook/automated-testing/cdc-testing/ ; https://www.speakeasy.com/blog/pact-vs-openapi (vendor view, discount) ; https://dev.to/therizwansaleem/how-to-build-a-practical-api-contract-testing-strategy-42h2 |
| Context-Driven Development | AI-agent era: make intent, requirements, architecture decisions, constraints, task boundaries and verification evidence explicit as versioned context; loop intent -> requirements -> architecture -> bounded tasks -> verification -> context evolution. Self-described as overlapping TDD/BDD/ADR/DDD, not replacing them. | Several independent, informal uses (a book, a Claude Code plugin with /cdd:* commands, blog posts); no authoritative standard. | https://leanpub.com/context-driven-development ; https://themobileagent.substack.com/p/context-driven-development-meets ; https://engleadai.substack.com/p/context-driven-development |

Other expansions (Config-/Convention-Driven, Chaos-, Cloud-, Compliance-Driven) were not researched in depth; they exist as phrases but surfaced no practice relevant to an agent-assisted dev workflow. [not searched]

Limits: no expansion is a recognized standard like TDD/BDD; Context-Driven is the newest and least settled; Contract-Driven is better known as CDC/contract testing.

### What exists in the code (real anchoring)
Verified by grep/Read over `/Users/matteoquintero/.agent-skills/mala-pata-*` (codegraph MCP failed to connect; fell back to grep/Read):
- Component-Driven: no lane or skill is named after it. Partial neighbors only: `mala-pata-standards` harvests "Component patterns" (anatomy, variants, states) as approved rules; `mala-pata-art` is the visual design director (orthogonal to lanes, "to ODD what clean-architecture is to code"). Neither builds bottom-up in isolation or prescribes a story-per-variation workflow. Atomic-design / container-presentational guidance lives in the user's global config, not in mala-pata.
- Contract-Driven: nothing. `sdd-design` has an "Interfaces / Contracts" section, and triage's form gate mentions "migration/contract/new UI" as a blast-radius signal; there is no contract-first practice or contract-test gate.
- Context-Driven: largely already covered. The kickoff (What/Why/DoD/Decisions/Risk), research docs, the SDD artifact chain, `mala-pata/` versioned docs + engram pointers, `sdd-init` context, and per-phase verification are exactly "explicit, versioned context + bounded tasks + verification". The suite IS a context-driven workflow without using the name.
- Related sibling research: `mala-pata/research/methodology-manager-skill.md` (c1) covers the catalog-of-methodologies idea; the CDD verdict should be reconciled with it.
- Lane taxonomy today: loop (SDD) / organic (ODD) / shot / roadmap; RDD is a review switch, not a lane. Precedent: not every "-DD" becomes a lane.

### Jobs-to-be-done
As the suite owner, I need to know whether "CDD" is a distinct way of working that mala-pata lacks, so that the suite neither misses a real practice nor grows a redundant lane/skill. The real struggle is acronym-completeness of a methodology catalog (c1..c6), not a felt delivery problem. [inferred from the icebox framing]

### Problem dimension (scope / frequency / severity)
- Scope: depends on which CDD. Component: UI work only. Contract: cross-boundary/API work only. Context: whole suite (already substantially covered).
- Frequency: not measurable; no evidence of a failing real change caused by the absence of CDD. [asked: open]
- Severity: low; no incident or blocked change cited. [inferred]

### Problem vs proposed solution
| Piece | Class | Evidence | Provenance |
|---|---|---|---|
| Add a "CDD" methodology (lane/skill) | extra until meaning chosen | no defined meaning | [inferred] |
| Context-Driven as a new lane | already-exists | kickoffs, research docs, SDD artifacts, versioned context | [verified in skills] |
| Component-Driven as a new lane | derivable / partial | UI work already routes organic/loop; `standards` + `art` supply the component conventions and judgment | [verified in skills] |
| Component-Driven as an orthogonal practice skill (build-in-isolation + variation stories, a sibling of `art`/`standards`) | necessary only if the human wants it | not covered anywhere in mala-pata | [verified absence in skills; need unproven] |
| Contract-Driven as an orthogonal practice (contract-first gate for cross-boundary changes) | necessary only if the human wants it | not covered; closest is SDD design "Interfaces/Contracts" | [verified absence; need unproven] |
| Catalog entry in c1 (methodology manager) for CDD | derivable | c1 would list it regardless of lane | [noted] |

## Heilmeier Catechism
| # | Question | Answer | Provenance |
|---|---|---|---|
| 1 | What are you trying to do? Explain it with no jargon. | Decide whether a methodology called "CDD" should exist in mala-pata and in what form. | [noted] |
| 2 | How is it done today, and what are the limits of current practice? | No CDD in mala-pata; "CDD" itself has three unrelated meanings and no standard. | [verified] |
| 3 | What is new in your approach, and why do you think it will work? | Nothing proposed yet; best hypothesis: treat each meaning as ORTHOGONAL to the lanes (like `art`/RDD), not a lane, since lanes classify change size/uncertainty while CDD variants classify how to build. | [inferred] |
| 4 | Who cares? If you succeed, what difference does it make? | Unknown: which CDD, for which project/work, and whether a real change is blocked. | [open - human only] |
| 5 | What are the risks? | Inventing a meaning; redundant lane diluting triage; a skill nobody uses (Context-Driven duplicates existing flow). | [inferred] |
| 6 | How much will it cost / how long will it take? | Decide-only: minutes once the meaning is chosen. Component or Contract orthogonal skill: one-unit authoring each. | [inferred] |
| 7 | What are the intermediate and final exams of success? | Unknown: what counts as "CDD is handled" for the human. | [open - human only] |

Assumption challenge (one): premise "mala-pata needs a CDD methodology". Evidence: Context-Driven is already the suite's backbone; Component-Driven is covered in judgment/standards form; only Contract-Driven is a genuine absence. Result: the premise holds at most for ONE of three meanings, and "lane" is the wrong shape for all three (they do not decide change size or uncertainty). Leans toward "covered or orthogonal", feeding a possible RECONSIDER for the lane form once the human picks the meaning.

## Define — sharpened idea (draft for triage)
- What: Resolve which expansion of "CDD" the user means, then decide its form: not a methodology (catalog-only entry), an orthogonal practice skill, or (least likely) a lane.
- Why: Keep the methodology catalog (c1..c6) honest without fabricating a definition or adding a redundant lane.
- DoD: Given the icebox cube c4, When the human states which CDD (Component / Contract / Context / other) and its source, Then a decision of form (catalog-only / orthogonal skill / lane) is recorded with the reason, and the cube is closed or re-routed.
- Decisions already made: do not create a CDD lane by default; lanes classify size/uncertainty, so a "how to build" methodology is not a lane by precedent (RDD, art). [inferred, from existing suite structure]
- Open decisions (human-only): (1) Which CDD, and the source? (2) Is it a lane, an orthogonal practice skill, or just a catalog entry in c1? (3) Does a real recent change motivate it (problem evidence)? (4) Reconcile with c1 (methodology manager) so the answer is not made twice.
- Risk: low blast radius (docs/skills only, no project code); real risk is inventing a meaning.
- Size signal: one-unit (hypothesis for triage; becomes trivial if the answer is "catalog-only").

## DoR (hand-off gate): What ✓ · Why ✓ · DoD ✓ · Decisions ✗ (meaning unresolved)

## Handoff
Do NOT route to triage yet. Answer the open question below and re-run `/mala-pata-research cdd-as-mala-pata-method`:
**Which "CDD" do you mean (Component-Driven, Contract-Driven, Context-Driven, or another), and where did you see it?**
Write-only: no commit made. Add this file in your normal PR flow on the durable branch (main).
