---
idea_slug: idd-as-mala-pata-method
project: mala-pata-skills
domain: mala-pata-suite
roadmap: none
icebox: mala-pata-lanes
verdict: SHARPEN
created_at: 2026-11-02T09:19:24-0500
next: none (SHARPEN — answer the open question, then re-run research)
size_signal: one-unit
---
# Research: IDD as a mala-pata methodology (icebox cube c3)

## Verdict: SHARPEN
"IDD" has no single authoritative meaning (at least three live, unrelated readings), and the acronym's source was not given; which IDD is a human-only decision. Under every reading, the shape of the answer is likely "orthogonal / mostly covered", not a new lane, but that is conditional on the meaning.

## Raw idea (what you asked)
Icebox cube c3: "IDD · decide whether and how it becomes a mala-pata methodology (which lane/skill, if any)". Sibling cubes c2-c6 name EDD, CDD, RDD, VSD in the same family as SDD/ODD; c1 proposes a "methodology manager" skill. The acronym expansion and its source were not defined.

## Discover

### How it's done today + limits (with sources)
"IDD" is ambiguous. Candidates found (none official; all are community/vendor sources, not standards):

| Candidate | How it is practiced | Source | Maturity |
|---|---|---|---|
| Intent-Driven Development | Build with AI coding agents by making intent explicit and structuring context around it; positioned as SDD plus durable intent, context engineering and verifying output matches intent. Separate projects use the same name: a Product→Intentions→Expectations→Specs framework replacing epics/stories; a NuGet tool + agent skills separating durable product intent from temporary tasks; a Manning book chapter ("intent articulation is the new bottleneck"). | https://intent-driven.dev/knowledge/intent-driven-development/ · https://awesome.ecosyste.ms/projects/github.com%2FGrillerGeek%2Fidd-framework · https://www.nuget.org/packages/DimonSmart.IntentDrivenDevelopment.Tool · https://livebook.manning.com/book/spec-driven-development/chapter-1 · https://elixirforum.com/t/ai-intent-driven-development-idd-guidelines-and-instructions-for-ai-coding-agents-ai-coding-assistants-and-llms/73187 | Recent, several competing definitions, no standard |
| Interface-Driven Development | Design by Contract / outside-in: define and agree interfaces first, then implement; inspired by Responsibility-Driven Design and DDD; related to interface-based programming (Wikipedia). | https://dzone.com/articles/introduction-to-interface-driven-development-idd · https://www.format-d.com/en/insights/t3n-interface-driven-development.html · https://www.wikipedia.org/wiki/Interface-based_programming | Older, design technique rather than a workflow |
| Issue-Driven Development | A GitHub/tracker issue is the single source of truth per task: issue exists before code, branch+worktree per issue (`gh issue develop`), PR closes the issue, cleanup after merge. Only community agent-skills describe it; no canonical definition. | https://skillselion.com/skills/hamsterider-m/issue-driven-skill/issue-driven · https://claudeskills.info/ja/skills/notedit/happy-skills/issue-flow/ · https://www.skills.lc/robinmordasiewicz/terraform-provider-f5xc/robinmordasiewicz-terraform-provider-f5xc-claude-skills-github-issue-workflow-skill-md | Folk practice, no authority |
| Integration-Driven Development | Only a single wiki-mirror listing; not corroborated. | https://wiki.riteme.site/wiki/IDD | Weak/unverified; treat as not established |
| (Non-methodology) Interface Design Description | MIL-STD-498 documentation artifact; unrelated to a workflow. Other IDD hits are healthcare ("intellectual and developmental disabilities"). | https://www.ppi-int.com/wp-content/uploads/2021/01/DID-Interface-Design-Description-IDD.pdf | Noise |

Limit of current practice: no single authoritative definition of "IDD" as a methodology exists. Intent-Driven is the only reading that is a whole-lifecycle method comparable to SDD/ODD; Interface-Driven is a design discipline inside implementation; Issue-Driven is a tracking/delivery convention. The sibling cubes (EDD, CDD, RDD, VSD) suggest the user's family is AI-era workflow names, which weakly favors Intent-Driven, but that is an inference [inferred], not a stated fact.

### What exists in the code (real anchoring)
Verified by reading `/Users/matteoquintero/.agent-skills/mala-pata-research/SKILL.md`, `mala-pata-triage/SKILL.md` and `~/.claude/skills/_shared/mala-pata-lane-gate.md`; the repo icebox `mala-pata/icebox/mala-pata-lanes.md`. (codegraph MCP was unavailable this session; fallback was Read/grep.)

- Intent reading: triage's form gate (What / DoD / Decisions, blocking) plus research's Heilmeier Catechism and "restate the OBJECTIVE, the outcome, not the idea's wording" already capture, sharpen and verify intent BEFORE any code. The kickoff (organic/loop) persists What/Why/DoD/Decisions/Risk as a durable, versioned artifact, and the loop adds spec/design/preview gates. This overlaps heavily with what Intent-Driven writers call "durable intent + spec" [verified: the gate and kickoff fields exist; equivalence with external IDD definitions is a judgment].
- Issue reading: no mala-pata skill is issue-centric. Grep of the non-SDD mala-pata skills finds no issue-first lane; the tracking artifacts are research doc / kickoff / roadmap / icebox `.md` in the repo plus an engram pointer. Issue handling exists only in non-mala-pata gentle skills (`issue-creation`, `branch-pr`, `work-unit-commits`, `chained-pr`) that the lanes may use at delivery. A GitHub issue is not a mala-pata unit of work.
- Interface reading: no mala-pata skill covers it as a method. It lives as external design skills (`clean-architecture`, `clean-ddd-hexagonal`, `solid`, `design-patterns`) and could be consumed inside loop `design` or organic Explore, i.e. a technique, not a lane. `mala-pata-art` is the closest suite precedent for an orthogonal "judgment" skill that is NOT a router.
- Already-owned analog for the family: RDD exists as the orthogonal review switch (not a lane); lanes are shot / organic(ODD) / loop(SDD) / roadmap. The lane-gate says lane = f(form gate fields, decision needs design). A new methodology only earns a lane if it changes that function.

### Jobs-to-be-done
As the suite's owner, I need a clear answer on whether "IDD" deserves a place in mala-pata so that the suite stays coherent (one routing function) and I do not collect named methodologies that overlap. The real struggle behind the request is probably (a) "name collection": each *-DD seen in the wild gets a cube, and (b) deciding where each sits relative to lane-vs-orthogonal. That is a classification problem, shared by c1-c6; the answer for IDD should be consistent with theirs. [inferred]

### Problem dimension (scope / frequency / severity)
- Scope: one cube (c3) of a seven-cube icebox; shares one decision pattern with c2, c4-c6 and the proposed c1 manager skill.
- Frequency: a one-time classification decision, no recurring operational pain observed. [inferred; not asked]
- Severity: low. No current failure; risk is suite bloat or a redundant lane. [inferred]
- Not measurable from evidence: urgency/priority. Marked as asked in Open decisions.

### Problem vs proposed solution
| Piece | Class | Evidence | Provenance |
|---|---|---|---|
| A new IDD lane (alongside shot/organic/loop/roadmap) | extra (unproven; likely already-exists for intent reading) | lane-gate routes by form gate + "needs design"; no IDD input changes that function | [inferred] |
| Intent capture/refinement before coding | already-exists | triage form gate, research Heilmeier, kickoff What/Why/DoD/Decisions | [verified, SKILL.md files] |
| Issue as unit of work / issue-first rule | necessary ONLY if "Issue-Driven" is chosen | no mala-pata skill covers it; non-mala-pata gentle skills cover issue creation/PR | [verified absence in non-SDD mala-pata skills] |
| Interface-first design discipline | derivable (technique inside loop design / organic Explore, via existing architecture skills) | external skills listed above | [inferred] |
| Orthogonal skill/flag (like RDD or mala-pata-art) instead of a lane | necessary to decide, shape unresolved | RDD and art precedents | [noted] |
| Methodology-manager catalog (c1) | out of scope here (separate cube) | icebox c1 | [noted] |

## Heilmeier Catechism
| # | Question | Answer | Provenance |
|---|---|---|---|
| 1 | What are you trying to do? Explain it with no jargon. | Decide whether a methodology called "IDD" gets a place in the suite and where. Cannot be stated precisely until "IDD" is defined. | [noted] |
| 2 | How is it done today, and what are the limits of current practice? | Three unrelated live meanings (intent / interface / issue); no authoritative definition. Suite covers intent capture via triage+kickoff; nothing issue-first; interface is a design technique. | [verified] |
| 3 | What is new in your approach, and why do you think it will work? | Nothing new yet. If Intent-Driven: likely adds only a naming/positioning layer on existing gates; if Issue-Driven: adds an issue-as-unit adapter at the delivery edge. | [inferred] |
| 4 | Who cares? If you succeed, what difference does it make? | Not established. Owner-only decision. | [assumed: suite owner; priority to confirm] |
| 5 | What are the risks? | Suite bloat, a second routing function competing with the lane-gate, naming collisions with RDD/ODD/SDD vocabulary, adopting a term with no stable definition. | [inferred] |
| 6 | How much will it cost / how long will it take? | Decision: minutes once meaning is fixed. Implementation: none to one skill/doc edit if orthogonal; one-unit even for a new adapter. | [inferred] |
| 7 | What are the intermediate and final exams of success? | Not established. Human-only. | [open] |

Assumption challenge (single): premise "mala-pata needs IDD as a methodology". Evidence against: (1) the term has no single meaning, (2) the intent reading is already covered by triage/research/kickoff, (3) interface and issue readings are a technique and a delivery convention respectively, not workflows that change lane selection. Evidence for: Issue-Driven has no mala-pata coverage today, so if that is the meaning the gap is real but small. Net: the premise is unproven; the likely outcome is "covered or orthogonal", never "a fifth lane", but the user must say which IDD.

## Define — sharpened idea (draft for triage)
- What: Decide, per the chosen meaning of IDD, one of: (a) already covered, no change; (b) documented as a mapping onto existing lanes/gates; (c) a small orthogonal skill or convention (precedent: RDD switch, mala-pata-art); (d) a new lane. Output is a recorded decision, not code.
- Why: Keep the suite coherent: one routing function, no overlapping named methodologies.
- DoD: Given the icebox cube c3, When the human has defined which IDD is meant, Then a decision (a/b/c/d) is recorded with its reason, and the cube is closed or turned into one concrete change.
- Decisions already made: IDD must not be assumed to be one specific method; any outcome must be consistent with the c1-c6 classification approach; skills stay domain-neutral; a lane is only added if it changes the lane-gate's routing function.
- Open decisions (human-only, NOT invented here):
  1. Which IDD is meant (Intent / Interface / Issue / other), and where did the term come from? Blocking.
  2. Lane or orthogonal (like RDD / art)? Depends on 1.
  3. Whether the answer should be decided together with c2/c4/c5/c6 for consistency (and c1's manager skill).
  4. Priority / who cares (Heilmeier 4) and what "done" means (Heilmeier 7).
- Risk: Low blast radius (docs/skill-level decision); risk is suite bloat or a duplicate router.
- Size signal: one-unit [hypothesis for triage]. The classification may merge with c2-c6 into one pass, which triage/defrost can decide.

## DoR (hand-off gate): What ✓ · Why ✓ · DoD ✓ · Decisions ✗ (meaning of IDD unresolved)

## Handoff
Not ready for triage. Answer open decision 1 (which IDD, and its source), then re-run `/mala-pata-research idd-as-mala-pata-method`, extending this doc. If the answer is "Intent-Driven", expect a quick PROCEED toward a mapping/doc outcome; if "Issue-Driven", the gap is the issue-as-unit adapter; if "Interface-Driven", expect RECONSIDER as a lane (technique only).

Left OUT / pending:
- New IDD lane — stays out until meaning is fixed and it is shown to change the lane-gate routing — [judgment]
- Methodology-manager skill — belongs to cube c1 — [skill rule]
- Integration-Driven reading — single uncorroborated source — [judgment]

Structure: Heilmeier Catechism (DARPA) + Double Diamond (Design Council). Verdict / size-signal / Left-OUT = house method.
