---
idea_slug: discovery-doc-skill
project: mala-pata-skills
domain: project-docs
roadmap: none
verdict: PROCEED
created_at: 2026-10-29T00:00:00Z
next: triage
size_signal: one-unit
---
# Research: discovery-doc-skill (first module of mala-pata-dossier)

## Verdict: PROCEED
Solid idea filling a real gap (no mala-pata skill generates a project-DISCOVERY document today), and all
open decisions are now settled with the user: the family is **`mala-pata-dossier`** — ONE authoring skill
with the project PHASE as a mode, **discovery = module 1**; v1 generates two renderings (full 6-question
traceability doc + client-only questionnaire); output is `.md` only. Finding accepted: the 6-question
framework has NO published name/source — it is a house synthesis from the FDE interview prep, so dossier
owns the method, it does not cite an external one. Ready for `/mala-pata-triage`.

## Raw idea (what you asked)
Create a NEW mala-pata skill (start of a future SET of skills) to GENERATE project documentation across
phases (discovery → build → …) and audience levels (técnico / cliente / socio). Start ONLY with the first
stage: discovery — understand what the client wants BEFORE proposing architecture or features. The generated
doc must follow a 6-question discovery framework: (1) ¿Para qué?, (2) ¿Cómo funciona hoy?, (3) ¿De qué está
hecho? (Intenciones/Identidad/Integraciones/Humano/Canal/Medición), (4) ¿Por dónde empiezo? (MVP), (5) ¿Cómo
sé que funcionó? (métricas), (6) ¿Qué puede salir mal? (riesgos). Search the internet for the framework's
NAME and SOURCE; do not invent a citation. Give proposals and help land the idea. This is a doc-authoring
skill like runbook/playbook — NOT a lane (not organic/loop/shot).

## Discover

### How it's done today + limits (with sources)
- The 6-question framework has **no published name or external source**. Web search over FDE discovery
  methodologies returned only interview-prep guides and secondary commentary on the Palantir-origin FDE role;
  none uses these 6 questions or the `3 I + H, C, M` decomposition
  ([fde.academy](https://fde.academy/blog/forward-deployed-engineer-interview-questions),
  [a16z "Trading Margin for Moat"](https://a16z.com), [techinterview.org Palantir guide](https://www.techinterview.org/companies/palantir/)).
  Adjacent public frameworks exist (consulting case structure: "structure first, hypothesis, deep-dive" —
  McKinsey/Bain, cited inside the decomposition PDF itself), but not this exact set.
- **Real origin (primary source on disk):** `career-ops/output/wonderful-fde-interview-prep-v2.pdf` §5.2
  "El framework de trabajo: las 6 preguntas del FDE" + the decomposition diagram (p.11): ACLARAR / MAPEAR /
  DESCOMPONER / VERSIÓN 1 / MEDIR / PROTEGER, each with a "qué produces" + "terminaste cuando…". The
  `wonderful-decomposition-case-prep.pdf` adds the "5 herramientas de negocio" (árbol de valor, mapa de
  actores, plan por fases, árbol de hipótesis, causa raíz). It is a **house synthesis**, built during the
  FDE interview prep — not a methodology we can attribute to an author.
- Limit of current practice (yours): the discovery doc is produced by hand each time (3 PDFs so far, each
  re-derived; one even drifted off-framework and had to be corrected). No reusable generator enforces the
  framework and the two audience renderings.
- **Reference document-structures (external, pulled in the 2026-10-30 sharpen):** how mature teams
  structure a discovery/requirements deliverable, to validate and enrich the house structure (not to replace
  it). Findings: (1) the **BRD** has no single standard — a 7–9 section core (executive summary, objectives,
  scope, requirements, stakeholders, constraints, assumptions/cost-benefit) plus optional glossary, sign-off
  and a RAID log; simpler projects mark nonessential sections `N/A`
  ([Slite — 7 sections](https://slite.com/en/learn/business-requirements-document-brd),
  [Business Analyst Mentor](https://businessanalystmentor.com/business-requirements-document/)). (2)
  **Client discovery-call templates** map almost 1:1 onto the 6 questions — goals, current workflow,
  volume/users, integrations, data migration, security, measurable success criteria, scope, stakeholders —
  and advise closing by confirming commitments
  ([SmartDev](https://smartdev.com/glossary-client-discovery-call/),
  [discovery session walkthrough](https://medium.com/swlh/discovery-session-for-the-new-project-step-by-step-4e137d01bdb1)).
  (3) **JTBD / switch interview** (Moesta) is a question-STYLE, not a structure: anchor each answer in a
  concrete past event ("the last time you…"), keep questions open, avoid leading
  ([Salesforce Trailhead — JTBD](https://trailhead.salesforce.com/content/learn/modules/jobs-to-be-done-framework-for-designers/discover-customers-jobs-to-be-done)).
  Net: the house 6-question framework already covers the substance; the references only add structural
  wrapping (header, stakeholders, RAID, glossary, sign-off) and the client-question style.

### What exists in the code (real anchoring)
- **Authoring-skill pattern already established** — `mala-pata-runbook` / `-playbook` / `-walkthrough` /
  `-states` all: write a versioned `.md` under `mala-pata/<kind>/<slug>.md`, carry a `domain:` frontmatter for
  domain-radar, run create-vs-adopt modes, are READ-ONLY + WRITE-ONLY (no commit), drop a one-line engram
  pointer, and close with a fixed BLUF block. The new skill reuses this skeleton verbatim — no new machinery.
- **Closest sibling = `mala-pata-walkthrough`** — it already produces CLIENT-facing docs via Diátaxis (how-to /
  tutorial) AND an internal QA guide, WITHOUT mixing them. That is exactly the dual-audience split this idea
  needs — but walkthrough runs DOWNSTREAM (from a PR/change, to document what was built). Discovery runs
  UPSTREAM (before anything is built). So: same dual-audience technique, opposite end of the lifecycle → a new
  skill, not an extension of walkthrough.
- **PDF generation precedent** — `career-ops/generate-pdf.mjs` (Playwright HTML→PDF) already renders
  client-ready PDFs in a sibling repo. If the skill must output PDF (open decision b), that mechanism is the
  reuse target, not a reinvention.
- **No existing discovery/requirements skill** — confirmed against the full skill inventory; no reuse collision.

### Jobs-to-be-done
As an FDE / consultant / dev starting a client engagement, I need to run a STRUCTURED discovery conversation
and capture it in a document that follows the 6-question framework, so that I understand what the client
actually wants and can scope an MVP WITHOUT committing to a solution prematurely (the exact failure mode the
PDFs warn against: "saltar directo a la solución").

### Problem dimension (scope / frequency / severity — with evidence; mark what you asked)
- **Scope**: 1 new skill now (discovery), first of a set (build-docs, partner-docs, … = future). Covers the
  first project phase × up to 2 audience renderings. [noted]
- **Frequency**: once per new client/project engagement — recurring across every future project. [inferred]
- **Severity**: medium. Getting discovery wrong propagates into building the wrong thing (highest-leverage
  phase). But it is a NEW capability, not a broken one — no regression risk. [inferred]

### Problem vs proposed solution
| Piece | Class | Evidence | Provenance |
|---|---|---|---|
| Discovery-doc authoring skill (6-question framework) | necessary | no skill generates a discovery doc today | [noted] |
| Create-vs-adopt modes, write-only, engram pointer, fixed close | already-exists (reuse) | `mala-pata-runbook/SKILL.md` pattern | [noted] |
| Dual audience rendering (cliente / técnico) | necessary (but scope of v1 = open) | both renderings exist in the source PDFs | [noted] |
| "Nivel socio" rendering | extra (future) | user named it as ambition, not for v1 | [noted] |
| Later-phase doc skills (build / delivery / …) | extra (future set) | user: "set de skills… inicemos solo con la primera" | [noted] |
| Find the framework's official NAME/source | already-exists answer = NONE | web search negative; origin is the house PDF | [noted] |
| Output as PDF (client-ready) | derivable-or-necessary (open decision b) | `career-ops/generate-pdf.mjs` precedent | [inferred] |

## Heilmeier Catechism
| # | Question | Answer | Provenance |
|---|---|---|---|
| 1 | What are you trying to do? | A skill that generates a client-discovery document following a 6-question framework, so discovery is captured consistently before building. First of a documentation skill set. | [noted] |
| 2 | How is it done today + limits? | By hand, PDF by PDF (3 so far); re-derived each time, drifted once. No generator enforces the framework or the audience renderings. | [noted] |
| 3 | What is new + why will it work? | Reuses the proven mala-pata authoring-skill skeleton (runbook/walkthrough) + the dual-audience Diátaxis split walkthrough already uses, applied UPSTREAM to discovery. Works because the pattern and the framework both already exist and are validated. | [noted] |
| 4 | Who cares? | The user, as FDE/consultant/dev, to run real client discovery and not build the wrong thing. | [asked] |
| 5 | Risks? | Low-blast (new, additive, no lane). Main risk: over-scoping v1 into the whole doc set. Naming the framework without a source. | [noted] |
| 6 | Cost / time? | One skill ≈ one authoring skill (runbook-sized). The SET is a future roadmap, not now. | [inferred] |
| 7 | Exams of success? | Given a client/project context, the skill produces a discovery doc that follows the 6 questions at the chosen audience level, capture-ready. (Exact DoD depends on open decisions a/b.) | [assumed] |

**Assumption challenge (one):** premise = "there is an official framework to cite." Evidence contradicts it —
the web search is negative and the only source is the house PDF. This does NOT weaken the skill (the framework
is sound and validated in use); it only means the skill must **own a descriptive name**. That is why the
verdict is SHARPEN (accept a house name), not RECONSIDER.

## Define — sharpened idea (draft for triage)
- **What**: `mala-pata-dossier` — ONE doc-authoring skill with the project phase as a mode (discovery first),
  that generates project documentation following the house 6-question framework, create-vs-adopt, write-only,
  like the other authoring skills.
- **Why**: capture each project phase consistently and reusably before/while building; stop re-deriving the
  discovery PDF by hand; one growing dossier per project (traceability).
- **DoD**: Given a client/project context in `discovery` mode, When `mala-pata-dossier` runs, Then it writes
  `mala-pata/dossier/<slug>.md` covering the 6 questions (ACLARAR→MAPEAR→DESCOMPONER→VERSIÓN 1→MEDIR→PROTEGER)
  as the internal traceability doc PLUS a client-only questionnaire rendering, read-only + write-only, engram
  pointer, fixed close block, `.md` only.
- **Decisions already made**: authoring skill, NOT a lane; reuse the runbook/walkthrough skeleton; one skill,
  phase-as-mode (discovery = module 1); anchor to the house 6-question framework (no external citation, dossier
  owns it); dual rendering (traceability doc + client questionnaire); `.md` only.
- **Decision RESOLVED (a) v1 scope** [asked 2026-10-29]: v1 generates **two renderings, not mixed** — (1) the
  FULL 6-question doc (ACLARAR→MAPEAR→DESCOMPONER→VERSIÓN 1→MEDIR→PROTEGER, with the 6-branch decomposition) as
  the **internal traceability artifact**, and (2) a **client-only questionnaire** (simple sections + blank
  spaces, like `levantamiento_de_informacion.pdf`) as the handout. Same dual-audience discipline as walkthrough.
- **Decision RESOLVED (b) output format** [asked 2026-10-29]: **`.md` only**, consistent with the whole
  authoring family (runbook/playbook/walkthrough). No PDF render in scope; no Playwright/HTML-template
  dependency. The user converts to PDF separately when needed.
- **Decision RESOLVED (c) family name + architecture** [asked 2026-10-29]: family = **`mala-pata-dossier`**
  (a dossier = the project's growing document collection across its lifecycle). Architecture = **ONE authoring
  skill with the project PHASE as a mode** (discovery now; scope/build/delivery/… added later as modes, like
  career-ops), NOT one skill per phase. **Discovery is module 1.** This keeps the first build future-proof for
  the whole set without a separate skill per phase.
- **No open decisions remain** — all three (a/b/c) resolved with the user.
- **Risk**: low — new, additive, no lane, no global files touched; only risk is over-scoping v1.
- **Size signal**: **one-unit** for THIS first skill (runbook-sized authoring skill). The broader
  documentation SET (later phases + "nivel socio") is a future multi-unit roadmap — named, not built now.

### Document structure (reference-backed — sharpen 2026-10-30, discovery mode)
The concrete structure the `discovery` mode emits, now LOCKED (house 6-question spine + reference wrapping).
Two renderings, same dossier run, never mixed (Diátaxis).

**Rendering 1 — Internal traceability doc** (`mala-pata/dossier/<slug>.md`, the full artifact):
1. **Header / executive summary** — project, client, participants, date, one-line objective (BRD).
2. **Q1 ¿Para qué?** [ACLARAR] — objetivo + número (metric target).
3. **Q2 ¿Cómo es hoy?** [MAPEAR] — flujo actual + dónde duele + volumen.
4. **Q3 ¿De qué está hecho?** [DESCOMPONER] — 6 ramas (Intenciones / Identidad / Integraciones / Humano /
   Canal / Medición) + **mapa de actores / stakeholders** (BRD + the house "5 herramientas").
5. **Q4 ¿Por dónde empiezo?** [VERSIÓN 1] — MVP + matriz valor / facilidad / riesgo.
6. **Q5 ¿Cómo sé que funcionó?** [MEDIR] — métricas hoy → meta.
7. **Q6 ¿Qué puede salir mal?** [PROTEGER] — **RAID log**: riesgos + supuestos + restricciones +
   dependencias + mitigación (BRD RAID folded into Q6).
8. **Glosario** (optional, `N/A` when not needed).
9. **Cierre / sign-off** — confirmación de acuerdos + `OPEN:` items (BRD sign-off + discovery "close by
   confirming commitments" + the house OPEN-gap discipline).

**Rendering 2 — Client-only questionnaire** (the handout, like `levantamiento_de_informacion.pdf`):
simple sections — Objetivo / Cómo funciona hoy / Volumen / Primera versión / Resultado y futuro / Material
de apoyo — with numbered questions and blank answer spaces, phrased in **JTBD style** (anchor in a concrete
past event, open-ended, non-leading). Same 6-question spine underneath, plain-language on the surface.

**N/A discipline**: nonessential sections are marked `N/A`/`OPEN:` rather than dropped (BRD practice =
the house gap discipline). Reuses the runbook/walkthrough skeleton verbatim — no new machinery.

### Name proposals (house-named, no false citation)
- **Discovery Canvas (6Q)** — "the 6 discovery questions" as the method label.
- **Client Discovery Brief** — emphasizes the deliverable.
- **Project Intake (6Q discovery)** — emphasizes the lifecycle stage.
- Skill id proposal: `mala-pata-discovery` (phase name), leaving room for `mala-pata-<phase>-doc` siblings.

## DoR (hand-off gate): What ✓ · Why ✓ · DoD ✓ · Decisions ✓

## Handoff
PROCEED. Triage (2026-10-30) ruled **organic** — authoring skill with a resolved spec (reuses the
runbook/walkthrough skeleton); the only open item was the document structure, which this 2026-10-30 sharpen
closed with reference-backed evidence (BRD / discovery-call / JTBD / Diátaxis). No open design remains → not
loop. Size signal is one-unit (discovery module of `mala-pata-dossier`); later phase-modes are future
additions, not this route.

Next → `/mala-pata-organic discovery-doc-skill` (route already decided; it confirms the Define draft and the
locked structure above, then writes the kickoff).

Structure: Heilmeier Catechism (DARPA) + Double Diamond (Design Council). Verdict / size-signal / Left-OUT = house method.
