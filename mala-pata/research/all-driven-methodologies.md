---
created_at: 2026-11-02T09:48:12-0500
type: research
topic: catalog of "*-Driven" software methodologies
status: draft (read-only research, not committed)
---

# Catalog of `*-Driven` software development / design methodologies

Evidence tags used in the Source column:
- **[S]** = source surfaced by a web search in this session (URL given). Secondary pages are noted as such.
- **[M]** = from model memory (author/year/book/URL), NOT re-verified this session. Treat as a lead to confirm.
- **[U]** = unsourced / folk term; no citation found. Not fabricated.

Search results were mostly secondary (blogs, vendor pages, Wikipedia mirrors). Where the primary text was not retrieved it is flagged.

## 1. Verification-driven

| Acronym | Full name | What it's for | Category | Primary source | Collision notes |
|---|---|---|---|---|---|
| TDD | Test-Driven Development | Write a failing test, make it pass, refactor (red-green-refactor) to drive code and design | verification | Kent Beck, *Test-Driven Development: By Example*, Addison-Wesley 2002 [M]. Overview: https://dzone.com/articles/tdd-bdd-and-atdd [S, secondary] | Same acronym: Type-Driven Development (Idris), Test-Driven Design (same acronym, design emphasis). Variants: London/outside-in (Freeman & Pryce, *Growing Object-Oriented Software, Guided by Tests*, 2009 [M]) |
| TDD | Type-Driven Development | Use types (dependent types) as the tool to construct programs and rule out errors | verification | Edwin Brady, *Type-Driven Development with Idris*, Manning 2017 https://www.manning.com/authors/edwin-brady [S] | Collides with Test-Driven Development |
| BDD | Behavior-Driven Development | Shift TDD vocabulary from tests to behaviour; Given-When-Then scenarios as shared language | verification | Dan North, "Introducing BDD", Better Software 2006, http://dannorth.net/introducing-bdd [S: existence confirmed via secondary pages; primary text not fetched] | Spelling "Behaviour". Related to ATDD / Specification by Example |
| ATDD | Acceptance Test-Driven Development | Stakeholders, devs, testers agree acceptance tests before coding | verification | Koskela, *Test Driven: Practical TDD and Acceptance TDD for Java Developers*, Manning 2007 [M]; overview https://dzone.com/articles/tdd-bdd-and-atdd [S] | Also called Customer-TDD / Story-TDD [M]; sometimes conflated with BDD |
| SbE | Specification by Example | Living, example-based specifications from collaboration with business | verification | Gojko Adzic, *Specification by Example*, Manning 2011 [M] | Often used as a synonym of BDD/ATDD flavours |
| EDD (example) | Example-Driven Development | Informal label: drive work from concrete examples | verification | Giorgio Sironi, "what drives development nowadays" https://www.giorgiosironi.com/2009/08/what-drives-development-nowadays.html [S, informal survey]; search note: usually a local label for BDD/ATDD flavours | EDD also = Eval-, Event-, Experiment-Driven |
| EDD (eval) | Eval-Driven Development | Define LLM evals first (working spec for LLM apps), iterate against them, gate releases | verification | O'Reilly Radar https://www.oreilly.com/radar/escaping-poc-purgatory-evaluation-driven-development-for-ai-systems [S]; DeepEval https://deepeval.com/blog/eval-driven-development [S]; Braintrust https://www.braintrust.dev/articles/eval-driven-development [S] (vendor/practitioner; no standard definition) | Also "Evaluation-Driven Development". Collides with other EDDs |
| PBT / (property-driven) | Property-Based Testing (a.k.a. "Property-Driven Development") | State universally quantified properties; tool generates random cases and shrinks failures | verification | Claessen & Hughes, "QuickCheck", ICFP 2000, pp.268-279 https://www.cs.tufts.edu/comp/150FP/archive/john-hughes/quick.pdf [S]. "Property-driven development" as a named method: [U] (no source found) | "PDD" also = Prompt-/Plan-/Process-Driven |
| HDD | Hypothesis-Driven Development | Treat each feature as a hypothesis with expected outcome and measure; experiment-led delivery | verification (experiment) / process | Humble, O'Reilly, Molesky, *Lean Enterprise*, O'Reilly 2014 (Barry O'Reilly credited with coining; single secondary source, unverified) https://www.oreilly.com/library/view/lean-enterprise/9781491946527/part02ch02.html [S] | HDD also = Hype-Driven Development (joke) |
| EDD (experiment) | Experiment-Driven Development | Run experiments (A/B, canaries) to decide what to build | verification (experiment) | [U] as a named method; adjacent: Eric Ries, *The Lean Startup*, 2011 [M] | Collides with other EDDs |
| ODD (observability) | Observability-Driven Development | Instrument first; use production telemetry before/during/after development | verification (ops feedback) | Charity Majors; InfoQ https://www.infoq.com/articles/observability-driven-development/ [S]; Majors, Fong-Jones, Miranda, *Observability Engineering*, O'Reilly 2022 [S: book listing]; Honeycomb post "A next step beyond test-driven development" https://www.honeycomb.io/blog/a-next-step-beyond-test-driven-development2 [S] | ODD also = Organic Driven Development (gentle-ai), Outcome-Driven (see below) |
| MDD (monitoring) | Monitoring-Driven Development | Write monitors/alerts first, like tests | verification (ops feedback) | [U] | Collides with Model-Driven Development |
| CDD (chaos) | Chaos-Driven Development | Design chaos experiments early, TDD-style, for distributed systems | verification | Amaranath & Vento (Bloomberg), SREcon23 Americas https://usenix.org/conference/srecon23americas/presentation/amaranath [S, talk abstract] | CDD has many meanings (see section 6). Underlying discipline: Principles of Chaos Engineering, https://principlesofchaos.org [M] |
| FDD (failure) | Failure-Driven Development | Drive design from failure modes | verification | [U] (searched; no matches) | Collides with Feature-Driven Development |
| DDT / KDT | Data-Driven Testing / Keyword-Driven Testing | Separate test logic from data or action keywords | verification | Hans Buwalda, Action Based Testing [M] | "Data-Driven" also design sense |
| MBT-ish | (Test-Driven Design) | Use test-writing pressure to shape design | verification/design | Beck 2002 [M] | Same acronym as Test-Driven Development |

## 2. Design / architecture-driven

| Acronym | Full name | What it's for | Category | Primary source | Collision notes |
|---|---|---|---|---|---|
| DDD | Domain-Driven Design | Model software around the business domain: ubiquitous language, bounded contexts, aggregates | design/architecture | Eric Evans, *Domain-Driven Design*, Addison-Wesley 2003 [M]; overload noted at https://learn.microsoft.com/en-us/archive/blogs/cellfish/dd [S] | DDD also = Data-Driven Development, Documentation-Driven Development, Delete-Driven (joke) |
| DDD (data) | Data-Driven Development / Design | Organize behaviour/objects around data (or decisions from data) | design/architecture | Contrast with RDD in https://home.cs.colorado.edu/~kena/classes/5448/f12/presentation-materials/wood.pdf [S]; data-oriented design: Mike Acton, CppCon 2014 [M] | Collides with Domain-Driven Design |
| RDD (responsibility) | Responsibility-Driven Design | Design objects by roles, responsibilities, collaborations (CRC cards) | design/architecture | Wirfs-Brock & Wilkerson, "Object-Oriented Design: A Responsibility-Driven Approach", OOPSLA 1989 https://bibtex.github.io/OOPSLA-1989-Wirfs-BrockW.html [S]; Wirfs-Brock & McKean, *Object Design*, 2003 [S] | RDD also = README-, Receipt-, REPL-, Risk-, Resume-Driven |
| MDD | Model-Driven Development | Build software primarily from models, generating code | design/architecture | https://modeling-languages.com/clarifying-concepts-mbe-vs-mde-vs-mdd-vs-mda/ [S] | MDD also = Monitoring-/Metadata-Driven |
| MDE | Model-Driven Engineering | Broader than MDD: models across process, analysis, evolution | design/architecture | same modeling-languages.com article [S]; arXiv roadmap https://arxiv.org/pdf/1409.6620 [S] | Nesting of MBE/MDE/MDD/MDA disputed across sources |
| MDA | Model-Driven Architecture | OMG framework: CIM/PIM/PSM, UML/MOF/XMI (launched 2001) | design/architecture | OMG; https://en.wikipedia.org/wiki/Model-driven_architecture [S, secondary] | Not "Mobile Device Architecture" etc. |
| ADD | Attribute-Driven Design | Architecture design driven by quality-attribute requirements | design/architecture | SEI (Bass, Clements, Kazman), *Software Architecture in Practice* [M] | Not surfaced by search; verify |
| CDC | Consumer-Driven Contracts | Providers evolve services against the union of consumers' expectations | design/architecture | Ian Robinson, 2006 https://www.martinfowler.com/articles/consumerDrivenContracts.html [S] | CDC also "Contract-Driven..."; tooling: Pact [M] |
| CDD (contract) | Contract-Driven Development / Design by Contract | Write explicit contracts (pre/post/invariants or API) first | design/architecture | Bertrand Meyer, *Object-Oriented Software Construction*, 1988/1997 [M]; API contract-first: https://www.apiopscycles.com/resources/contract-first-design [S, vendor] | CDD = Component-/Context-/Chaos-Driven |
| IDD (interface) | Interface-Driven Development | Define interfaces before implementations | design/architecture | [U] as a named method; principle: GoF "program to an interface", 1994 [M] | IDD = Intent-/Issue-Driven |
| CDD (component) | Component-Driven Development | Build UIs bottom-up: components in isolation, then screens | design/architecture | Tom Coleman, https://www.componentdriven.org (via Chromatic blog) https://www.chromatic.com/blog/component-driven-development/ [S: copies of the article surfaced] | CDD collisions above |
| EDA / EDD | Event-Driven Architecture / Development | Systems built on event production/consumption | design/architecture | Martin Fowler, "What do you mean by Event-Driven?" https://martinfowler.com/articles/201701-event-driven.html [M]; Event Storming: Alberto Brandolini [M] | EDD = Eval-/Example-/Experiment-Driven |
| SDD (schema) | Schema-Driven Development (schema-first) | Define data/API schema (OpenAPI, Protobuf, GraphQL) first, generate code | design/architecture | OpenAPI spec https://spec.openapis.org [M]; practitioner overview https://academy.threedots.tech/knowledge/api-first-design/ [S, secondary] | SDD also = Spec-Driven (below), Software Design Description (IEEE 1016 [M]) |
| API-first | API-Driven / API-First Design | Treat the API as the product and design it first | design/architecture | same sources as Schema-Driven [S] | "API-Driven" sometimes means automation via APIs |
| CoC | Convention-/Configuration-Driven Development | Convention over configuration; behaviour driven by declarative config | design/architecture | DHH, Ruby on Rails, ~2004 [M]; "configuration-driven" as method: [U] | CDD collisions |
| MDD (metadata) | Metadata-Driven Development | Behaviour/UI generated from metadata | design/architecture | [U] | Collides with Model-Driven |
| VSD | Value Sensitive Design | Account for human values throughout technology design (conceptual/empirical/technical investigations) | design/architecture | Batya Friedman, 1996; Friedman & Hendry, *Value Sensitive Design*, MIT Press 2019 https://en.wikipedia.org/wiki/Batya_Friedman [S] | VSD also = Vertical Slice Development/Design |
| (risk) | Risk-Driven Development / Spiral Model | Choose next activity by highest risk | design/process | Barry Boehm, spiral model, 1986-88 [M] | RDD collision |
| (threat) | Threat-Driven Design/Modeling | Design from threat model | design/architecture | [U] | |
| ODI / ODD | Outcome-Driven Innovation | Requirements from customer jobs and desired outcomes | design/process | Anthony Ulwick, *What Customers Want*, 2005 [M] | ODD collision |

## 3. Process / workflow-driven

| Acronym | Full name | What it's for | Category | Primary source | Collision notes |
|---|---|---|---|---|---|
| FDD | Feature-Driven Development | Iterative delivery of small client-valued features, domain model first | process/workflow | De Luca & Coad; Coad, Lefebvre, De Luca, *Java Modeling in Color with UML*, 1999; Palmer & Felsing, *A Practical Guide to FDD*, 2002 https://en.wikipedia.org/wiki/Feature-driven_development [S] | FDD also Failure-Driven (see above; folk) |
| (issue) | Issue-Driven Development | Work starts from, is tracked by, an issue | process/workflow | [U] | IDD collision |
| (ticket) | Ticket-Driven Development | Same, with tickets | process/workflow | [U] (often pejorative) | |
| SDD | Spec-Driven Development | Written spec precedes AI-generated code; specify, plan, tasks, implement | process/workflow | Martin Fowler site https://www.martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html [S]; GitHub Spec Kit, Kiro [S via comparisons]. Definition "still in flux" | SDD also = Schema-Driven, Software Design Description. In gentle-ai, SDD is the optional branch of ODD |
| IDD | Intent-Driven Development | Make intent explicit so AI agents build what was meant | process/workflow | https://intent-driven.dev/knowledge/intent-driven-development/ [S, community]; Manning *Spec-Driven Development* (early access) https://manning.com/books/spec-driven-development [S] | Terminology unsettled; IDD = Interface-/Issue-Driven |
| VSA | Vertical Slice (Architecture/Development) | Organize and deliver by feature slices not layers | process/design | Jimmy Bogard, ~2018 https://www.jimmybogard.com/tag/vertical-slice-architecture/ [S]; user-story slicing Bill Wake (INVEST) [M] | VSD collision |
| (value-stream) | Value-Stream-Driven / Flow Framework | Optimise end-to-end flow of value | process/workflow | Mik Kersten, *Project to Product*, 2018 [M]; Lean value-stream mapping [M] | |
| (trunk) | Trunk-Based Development | Short-lived branches, integrate to trunk continuously | process/workflow | https://trunkbaseddevelopment.com [M]; name is "-Based", flagged for completeness | |
| (flow) | Flow-Driven Development | Drive work by flow metrics | process/workflow | [U] | |
| (plan) | Plan-Driven Development | Upfront plan, then execute (traditional) | process/workflow | Boehm & Turner, *Balancing Agility and Discipline*, 2003 [M] | PDD collision |
| (story) | Story-Driven Development | Drive from user stories | process/workflow | informal; see Sironi link above [S] | |
| (REPL) | REPL-Driven Development | Develop interactively at a live REPL | process/workflow | Clojure guide https://clojure.org/guides/repl/introduction [M] | RDD collision |
| (GitOps) | Git-Driven / GitOps | Git as source of truth for ops state | process/workflow | Weaveworks, 2017 [M] | |
| ODD | Organic Driven Development | gentle-ai default workflow: authorize, explore, classify, track, implement, close | process/workflow | In-session orchestrator config (this environment); no public canonical source [U] | ODD also Observability-/Outcome-Driven |
| RDD | Receipt-Driven Development | gentle-ai user-owned switch: native review produces a receipt authorizing a candidate | process/workflow | gentle-ai configuration/instructions in this environment [U] (not public canonical) | FLAGGED collision with README-Driven Development; also Responsibility-/REPL-/Risk-/Resume-Driven |

## 4. Documentation / context-driven

| Acronym | Full name | What it's for | Category | Primary source | Collision notes |
|---|---|---|---|---|---|
| RDD | README-Driven Development | Write the README first to define what the software does | documentation/context | Tom Preston-Werner, Aug 2010, http://tom.preston-werner.com/2010/08/23/readme-driven-development.html [M URL]; summaries https://ponyfoo.com/articles/readme-driven-development [S, secondary]; Zach Holman, "A Documentation Talk", 2011 https://zachholman.com/posts/documentation/ [S] | Collides with Receipt-/Responsibility-/REPL-Driven. A guide calls RDD a subset of Documentation-Driven (secondary) |
| DDD / DocDD | Documentation-Driven Development | Docs before code; docs as spec | documentation/context | Daniele Procida, EuroPython 2016 slides https://ep2016.europython.eu/media/conference/slides/documentation-driven-development.pdf [S]; Isaac Schlueter https://blog.izs.me/2017/06/documentation-driven-development/ [S] | DDD collision |
| CDD | Context-Driven Development (AI agents) | Engineer context/constraints/feedback around agents; versioned context files | documentation/context | Luca Sepe, Leanpub https://leanpub.com/context-driven-development [S]; https://engleadai.substack.com/p/context-driven-development [S] | No standard definition. Different from Context-Driven Testing (Kaner/Bach/Pettichord, *Lessons Learned in Software Testing*, 2001 [M]) |
| PDD | Prompt-Driven Development | Prompt as source of truth; fix prompt, not output | documentation/context | https://hexaware.com/blogs/prompt-driven-development-coding-in-conversation/ [S]; https://dev.to/blame76/prompt-driven-development-pdda-manifesto-against-comfortable-guessing-4m4a [S] | No canonical definition; PDD = Plan-/Process-/Property-Driven |

## 5. Humorous / anti-pattern "-Driven" terms (for disambiguation only)

| Acronym | Full name | Source | Note |
|---|---|---|---|
| DDD | Delete-Driven Development | https://learn.microsoft.com/en-us/archive/blogs/cellfish/dd [S, blog] | Joke |
| CDD | Consultant-Driven Development | same [S] | Joke |
| PDD | Process-Driven Development | same [S] | Joke/informal |
| RDD | Resume-Driven Development | [U] | Folk anti-pattern |
| HDD | Hype-Driven Development | [U] | Folk anti-pattern |
| SODD | Stack-Overflow-Driven Development | [U] | Folk |

## Coverage limits

- Searches were broad, not exhaustive; many entries rely on [M] memory citations that were not re-verified.
- No primary text fetched for BDD (dannorth.net), README-Driven (tom.preston-werner.com), Evans DDD, Beck TDD.
- Terms with no source found: Property-Driven (as method), Monitoring-Driven, Failure-Driven, Experiment-Driven, Interface-Driven, Issue/Ticket/Flow-Driven, Metadata-/Configuration-Driven, Threat-Driven, humorous terms, RDD (Receipt) and ODD (Organic) public sources.
- Not covered: Data-/Domain-specific variants (Test-Driven Infrastructure, Test-Driven Documentation), regulated-domain methods, and non-English usage.
