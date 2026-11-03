---
name: mala-pata-dossier
description: CREATES a project DISCOVERY document — captures what the client actually wants BEFORE proposing architecture or features, following a house 6-question framework (ACLARAR / MAPEAR / DESCOMPONER / VERSIÓN 1 / MEDIR / PROTEGER). It is the first MODE of a phased documentation family (the project PHASE is a mode; discovery = module 1; scope/build/delivery are future modes). Produces TWO renderings WITHOUT mixing them (Diátaxis) — an internal 6-question traceability doc AND a client-only questionnaire. Two modes — create NEW from a client/project context, or ADOPT an existing discovery doc and normalize it to the standard. It writes to mala-pata/dossier/<slug>.md with a domain; it is READ-ONLY on your projects and NEVER proposes the solution (discovery only). Before writing, it confirms understanding and asks the open questions one at a time (JTBD style). Trigger — "levantá la información de X", "documentá el discovery de <cliente>", "armá el cuestionario de descubrimiento", "qué quiere el cliente en <proyecto>", "normalizá este discovery al estándar".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "0.1.0"
---

# /mala-pata-dossier — capture project discovery (does not propose the solution)

Input: **the one delivered by the CLI** — a **client/project context** (new discovery doc), or the **path to an existing discovery doc** to adopt and normalize to the standard. The phase mode defaults to `discovery` — the only phase implemented today.

Your job: run a **structured discovery** and capture it in a document that follows the house 6-question framework, so you understand what the client ACTUALLY wants and can scope an MVP WITHOUT committing to a solution prematurely. You WRITE the document; you do NOT design the architecture, you do NOT propose features, you do NOT build anything.

> **You never propose the solution.** Discovery is UPSTREAM of architecture — the exact failure mode this guards against is "saltar directo a la solución". You capture intentions, constraints and success criteria; the solution comes later, in a different phase/lane.
> **Two renderings, never mixed (Diátaxis).** The same discovery core produces (1) an internal 6-question traceability doc and (2) a client-only questionnaire. They share the core but differ in audience and purpose — they are NOT merged into one document.
> **Read-only + write-only.** You inspect to capture accurately; the only thing you write is the discovery `.md`. You do NOT commit — the human commits in their normal flow.

## Requirements (orchestrate, do not reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP): `git` — to resolve the repo root for the document's location. Always present.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded):
  - `engram` — one-line discoverability pointer. Fallback: the file is the source of truth.
  - `WebSearch` / `WebFetch` — only when discovery needs external context about the client's domain. Fallback: disclose that there was no external research.

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP). If a mandatory tool is missing, do not continue.

## Principles (proven, not invented)

- **The 6-question framework (house synthesis).** The spine of the document: (1) ¿Para qué? [ACLARAR] objetivo con número; (2) ¿Cómo es hoy? [MAPEAR] flujo + dónde duele; (3) ¿De qué está hecho? [DESCOMPONER] 6 ramas = Intenciones / Identidad / Integraciones / Humano / Canal / Medición; (4) ¿Por dónde empiezo? [VERSIÓN 1] MVP priorizado por valor / facilidad / riesgo; (5) ¿Cómo sé que funcionó? [MEDIR] métricas hoy → meta; (6) ¿Qué puede salir mal? [PROTEGER] riesgos + mitigación. It has **NO published external source** — it is a house synthesis; dossier OWNS the method and does NOT fake a citation.
- **Diátaxis** (Procida): the traceability doc and the client questionnaire share the discovery core but differ in audience → two renders, never one mixed doc.
- **JTBD / switch interview** (Moesta): the question STYLE for the client questionnaire — anchor each answer in a concrete past event ("la última vez que…"), keep questions open, avoid leading questions.
- **BRD structure wrapping** (BABOK-adjacent): the traceability doc wraps the 6 questions with an executive-summary header, a stakeholders map, a RAID log (risks / assumptions / constraints / dependencies) and a sign-off; nonessential sections are marked `N/A`, never dropped.

## Phase 0 — Authorize (read-only guard)

Creating a discovery document is **always read-only** — you capture what the client wants; you do NOT design, propose features, or build. Even when the project is itching to "start coding", your work here is only the document. No worktree, no code, no architecture proposal.

## Phase 1 — Phase mode + create/adopt + grounding

1. **Phase mode**: dossier is phased; **today only `discovery` is implemented** (module 1). If asked for another phase (scope / build / delivery / partner-level), say it is not implemented yet and offer to capture it as a future module — do NOT improvise a different phase's structure.
2. **Create vs adopt**: a **client/project context** → create a new discovery doc. A **path to an existing discovery doc** (e.g. a prior "levantamiento de información") → **adopt**: read it and map its content onto the standard (Phase 3), keeping what is real and flagging gaps.
3. **Ground it** (read-only, proportional): the client's real context — the domain, the current process, the actors. If existing material exists (a brief, a prior doc, a transcript), read it FIRST; do not re-derive what the client already stated. Reuse-first.

## Phase 2 — Confirm understanding, ask the open questions (BEFORE writing)

This is the step that makes the discovery correct. The 6 questions ARE the interview; do NOT invent the client's answers — surface them and ask (the research-backed "test it on someone who didn't write it", applied up front).

1. **Restate the objective in order** — a one-line readback per question of what you understood so far ("Q1 objetivo: …; Q2 cómo es hoy: …"). This is the comprehension check; it exposes where you are guessing.
2. **Ask the open questions one at a time** (JTBD style — concrete past events, open, non-leading). The human-only answers are typically **Q1** (the real objective + its number), **Q4** (what the MVP must cover first) and **Q5** (what success looks like FOR them), plus any business constraint. Ask, WAIT, never assume. If a value stays genuinely unknown, write it as an explicit `OPEN:` gap in the doc, not a guess.
3. **Pin the rendering scope** — confirm ONCE that v1 produces BOTH renderings (internal traceability doc + client-only questionnaire). Only when the discovery core and the open questions are settled, write the document.

## Phase 3 — The standard (what every discovery doc contains)

Write to `mala-pata/dossier/<slug>.md` (inside the repo, versioned; `mkdir -p`). **Frontmatter** (feeds `/mala-pata-domain-radar`):

```markdown
---
slug: <kebab>
domain: <the project/area this discovery belongs to — else 'main'; NEVER blank, ANY doubt → ASK the human>
phase: discovery
kind: discovery
client: <who the discovery is for>
owner: <who ran the discovery>
created_at: <ISO 8601>
last_reviewed: <ISO 8601>
---
```

**Rendering 1 — Internal traceability doc** (fixed section order — labels verbatim English):

| Section | What it holds |
|---|---|
| Header / executive summary | Project, client, participants, date, one-line objective. |
| Q1 ¿Para qué? [ACLARAR] | The objective with a NUMBER (the measurable target). |
| Q2 ¿Cómo es hoy? [MAPEAR] | Current flow + where it hurts + volume. |
| Q3 ¿De qué está hecho? [DESCOMPONER] | The 6 branches (Intenciones / Identidad / Integraciones / Humano / Canal / Medición) + a stakeholders / actors map. |
| Q4 ¿Por dónde empiezo? [VERSIÓN 1] | The MVP + a value / ease / risk priority matrix. |
| Q5 ¿Cómo sé que funcionó? [MEDIR] | Metrics today → target. |
| Q6 ¿Qué puede salir mal? [PROTEGER] | RAID log: risks + assumptions + constraints + dependencies + mitigation. |
| Glossary | Shared terms (optional — `N/A` when not needed). |
| Close / sign-off | Confirmed agreements + `OPEN:` items (nothing hidden). |

**Rendering 2 — Client-only questionnaire** (the handout — simple, no jargon):

Sections: **Objetivo · Cómo funciona hoy · Volumen · Primera versión · Resultado y futuro · Material de apoyo**. Numbered questions with blank answer spaces, phrased in JTBD style (concrete past event, open, non-leading). Same 6-question spine underneath, plain language on the surface. It **NEVER** mixes internal notes, priorities or risks into the client handout (Diátaxis: two renders).

`N/A discipline`: nonessential sections are marked `N/A` / `OPEN:`, never silently dropped (BRD practice = the house gap discipline).

## Phase 4 — Persist (write only) + pointer

1. **Write only — do NOT commit/push.** Write the file; the skill does NOT create a commit (auto-committing diverges local main from the remote). Tell the human the path + the durable branch it belongs on so they commit it in their normal flow.
2. **Adopt mode**: write the normalized discovery doc to `mala-pata/dossier/<slug>.md`; do NOT delete the original — name it and let the human retire it. List the gaps you filled (implicit answers made explicit, missing questions added, `OPEN:` items left).
3. **Lightweight pointer in engram**: `mem_save` topic_key `dossier/<slug>`, one-line content `Discovery doc in file: <absolute path>`. If engram is unavailable, the file is the source — warn in one line.

## Phase 5 — Close (mandatory: summary + doc)

Emit exactly this, from the document you wrote (no invention):

- Title: `**Discovery ready — <slug>**`
- BLUF (plain line): `Discovery: 6 questions · <k> OPEN · 2 renderings (traceability + client questionnaire) · phase discovery`
- A short readback table (`Q | Captured?`) — one line per question, so the human sees coverage.
- **OPEN** items, if any — one per line, each needing the client/human (never hidden).
- **File:** `mala-pata/dossier/<slug>.md`
- **Next step** — the discovery is the INPUT to the next phase (scope / architecture), decided in a different lane (`/mala-pata-triage` → organic/loop/roadmap); dossier does NOT propose it.

This block is the only way to close on the happy path. **Only exceptions**: Phase 0 read-only stance; a blocking open question (Phase 2) → the single question allowed before writing.

`Structure: house 6-question discovery framework (ACLARAR→PROTEGER) + Diátaxis dual-audience (Procida) + JTBD switch interview (Moesta) + BRD/RAID wrapping (BABOK-adjacent). Phase-as-mode + traceability-vs-questionnaire split = house method.`

## What it does NOT do (invariants)

- Does NOT propose architecture or features — discovery only; the solution is a later phase/lane.
- Does NOT run against your real projects — read-only to capture accurately; the only thing it writes is the discovery md.
- Does NOT invent the client's answers — it asks them (Phase 2) or leaves them as explicit `OPEN:` items.
- Does NOT fake a framework citation — the 6-question framework is a house synthesis with no external source.
- Does NOT mix the traceability doc with the client questionnaire (Diátaxis: two renders).
- Does NOT commit — write-only; the human commits in their PR flow.
- Does NOT implement other phases yet — only `discovery` (module 1).

## Relation to the family

- **First module of** the `mala-pata-dossier` documentation family (phase-as-mode; scope / build / delivery / partner-level are future modes, not separate skills).
- **Indexed by** `/mala-pata-domain-radar` (reads the `domain:` frontmatter, like the other mala-pata artifacts).
- **Upstream of** `/mala-pata-walkthrough` — walkthrough documents what was BUILT (downstream, from a PR/change); dossier captures what the client WANTS (upstream, before building). Same dual-audience discipline, opposite ends of the lifecycle.
- **Different from** `/mala-pata-runbook` / `-playbook` (operational procedures to execute) — dossier is a discovery artifact, not a procedure; and from the lanes (`shot`/`organic`/`loop`/`roadmap`) — it is a doc-authoring skill, orthogonal, not a route.
