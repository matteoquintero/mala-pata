---
change_name: mala-pata-dossier
project: mala-pata-skills
domain: project-docs
roadmap: none
research: discovery-doc-skill
route: organic
base: main
branch: feature/mala-pata-dossier
worktree: none   # META-WORK: no worktree — the live skill is the symlink at ~/.agent-skills/mala-pata-dossier (into ~/.claude/skills); author there, rsync-mirror to the repo, commit on the branch (same as runbook/playbook/walkthrough/states/art)
tdd_mode: standard   # authoring a SKILL.md .md has no test runner; "check" = conforms to the mala-pata authoring standard + loads. strict-TDD does not apply to prose authoring
smoke_test:
  needed: no   # doc-authoring artifact; no seeded-data manual test. Verification = structural (standard conformance + the skill loads)
  data: N/A
created_at: 2026-10-30T00:00:00Z
---

# Kickoff ODD: mala-pata-dossier

## What
Build `mala-pata-dossier` — a doc-authoring skill (like runbook/playbook/walkthrough, NOT a lane) with the
project PHASE as a mode; ship **discovery = module 1**. It generates a project-discovery document following
the house 6-question framework, create-vs-adopt, read-only on projects + write-only, `.md` only. It writes to
`mala-pata/dossier/<slug>.md` and never executes anything it documents.

## Why
Capture each project phase consistently and reusably before/while building; stop re-deriving the discovery
doc by hand (3 PDFs so far, each re-derived, one drifted off-framework); one growing dossier per project for
traceability. Flows into the feature-doc and the PR body.

## DoD
Given a client/project context in `discovery` mode, When `mala-pata-dossier` runs, Then it writes
`mala-pata/dossier/<slug>.md` with the LOCKED structure and nothing executed:
- **Rendering 1 — internal traceability doc**: header/executive-summary → Q1 ¿Para qué? [ACLARAR] → Q2 ¿Cómo
  es hoy? [MAPEAR] → Q3 ¿De qué está hecho? [DESCOMPONER] (6 ramas Intenciones/Identidad/Integraciones/
  Humano/Canal/Medición + stakeholders) → Q4 ¿Por dónde empiezo? [VERSIÓN 1] (MVP + matriz valor/facilidad/
  riesgo) → Q5 ¿Cómo sé que funcionó? [MEDIR] (hoy→meta) → Q6 ¿Qué puede salir mal? [PROTEGER] (RAID:
  riesgos+supuestos+restricciones+dependencias+mitigación) → glosario (opcional, `N/A` si no aplica) →
  cierre/sign-off (acuerdos + `OPEN:` items).
- **Rendering 2 — client-only questionnaire** (not mixed, Diátaxis): simple sections (Objetivo / Cómo
  funciona hoy / Volumen / Primera versión / Resultado y futuro / Material de apoyo), numbered questions in
  JTBD style (concrete past event, open-ended, non-leading), blank answer spaces.
- Read-only + write-only (no commit by the skill), engram one-line pointer, fixed BLUF close block, `.md`
  only, `domain:` frontmatter for domain-radar, create-vs-adopt modes.

## Decisions already made
- Authoring skill, NOT a lane (orthogonal, like runbook/playbook).
- Reuse the `mala-pata-runbook`/`-walkthrough` skeleton VERBATIM — no new machinery.
- ONE skill, phase-as-mode: discovery = module 1; later phases (scope/build/delivery…) are future modes, not
  new skills, not this change.
- Anchor to the house 6-question framework; NO external citation (web search negative) — dossier owns the
  method.
- Dual rendering (traceability doc + client questionnaire), never mixed.
- `.md` only (no PDF render in scope).
- **Document structure LOCKED** and reference-backed (sharpen 2026-10-30: BRD → header/stakeholders/RAID/
  glossary/sign-off; discovery-call templates → 6-question coverage; JTBD → client-question style; Diátaxis →
  audience split). See `mala-pata/research/discovery-doc-skill.md`.

## Risk
Low — new, additive, no lane, no global files touched; only risk is over-scoping v1 into the whole doc set
(explicitly deferred: later phase-modes + "nivel socio" are a future roadmap, not this change).

## Where (optional hint — to be discovered in Explore)
New skill authored at `~/.agent-skills/mala-pata-dossier/SKILL.md` (symlinked into `~/.claude/skills`), then
rsync-mirrored to `mala-pata-skills/mala-pata-dossier/`. Template to mirror: `mala-pata-runbook/SKILL.md`
(frontmatter + body section order + Phase 0 read-only guard + Phase 2 confirm/ask + Phase 4 write-only +
engram pointer + Phase 5 fixed close). Closest sibling for the dual-audience split: `mala-pata-walkthrough`.

## Meta-work flow (replaces the worktree model for this change)
1. Author `~/.agent-skills/mala-pata-dossier/SKILL.md` (live via the `~/.claude/skills` symlink).
2. Mirror: `rsync -a --delete ~/.agent-skills/mala-pata-dossier/ <repo>/mala-pata-dossier/`.
3. Commit on `feature/mala-pata-dossier` (Conventional Commits, ZERO AI attribution). Push is the user's call.
4. Include `mala-pata/research/discovery-doc-skill.md` in the same branch/PR (the `research:` link).
