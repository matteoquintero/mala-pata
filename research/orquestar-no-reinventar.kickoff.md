---
change_name: orquestar-no-reinventar
project: mala-pata
route: organic
base: "repo espejo mala-pata-skills @ main; authoring live en ~/.agent-skills/mala-pata-*"
branch: "N/A — sin worktree; commit directo a main del repo espejo (patrón del suite, igual que mala-pata-states)"
worktree: "N/A — los skills viven en ~/.agent-skills (runtime, no git); el repo es el espejo"
tdd_mode: "N/A — SKILL.md son instrucciones; verificación por test-run"
created_at: 2026-09-30
---

# Kickoff ODD: orquestar-no-reinventar

## Qué
Agregar a cada skill de mala-pata un bloque **"Requisitos / preflight"** que: (a) declara la(s) herramienta(s) de comunidad que ese skill orquesta, (b) la chequea al arrancar, y (c) guía a instalarla si falta. Rigidez **por-herramienta**: obligar las que no tienen fallback, recomendar las que sí.

## Why
Formalizar "orquestar, no reinventar la rueda" como contrato verificable: que el fallo por herramienta faltante aparezca temprano y claro, no a mitad de ciclo. (Fluye al feature-doc y al PR.)

## Done
- Los 13 skills (`research, triage, organic, organic-start, loop, loop-start, loop-orchestrate, loop-orchestrate-start, roadmap, radar, walkthrough, states, sdd-preview`) tienen el bloque "Requisitos", con el mismo patrón.
- Correr un skill sin su herramienta **OBLIGATORIA** frena al arranque con un mensaje claro + cómo instalar. Test-run: `states` sin `archify` frena con hint.
- Correr un skill cuya herramienta tiene **fallback** avisa y degrada (no frena). Test-run: `research` sin `codegraph` avisa y usa grep/Read.
- `triage` no declara herramienta dura (solo decide) — su bloque dice "ninguna herramienta obligatoria".

## Decisiones ya tomadas
- **Rigidez por-herramienta** (confirmada por el humano):
  - **Obligar** (sin fallback): `gentle-ai` → organic, organic-start, loop, loop-start, loop-orchestrate(+start), sdd-preview · `archify` → states · `git` → radar.
  - **Recomendar / declarar** (con fallback): `codegraph` → research, roadmap, states · `Serena` (MCP LSP, navegación/edición símbolo-nivel) → research, roadmap, states, organic-start, loop-start (recomendado, fallback a codegraph/grep) · `engram` → radar y donde aplique · `gh` → walkthrough.
- El preflight vive como **primer paso del SKILL.md** (markdown que el agente sigue), apoyado en el patrón doctor/preflight de la comunidad.
- Delivery = authoring live en `~/.agent-skills/` → symlinks ya existentes → **sync al repo `mala-pata-skills` + commit a main** (sin worktree, patrón mala-pata-states).
- **Sin emojis** (preferencia del usuario). Español con tildes.
- Fijar PRIMERO el bloque-plantilla y aplicarlo IGUAL a los 13 (consistencia), no improvisar por skill.

## Riesgo
Inconsistencia entre skills si cada uno redacta su bloque distinto; mitigado definiendo la plantilla una vez y copiándola. Obligar de más donde hay fallback — ya resuelto por la rigidez por-herramienta.

## Dónde (hint opcional — a descubrir en Explore)
- Los 13 `SKILL.md` en `~/.agent-skills/mala-pata-*` (+ `sdd-preview`), espejados en `mala-pata-skills/`.
- A confirmar en Explore: cuáles ya mencionan su herramienta en prosa (states→archify, research→codegraph) para no duplicar, y la forma exacta del comando de instalación por herramienta (gentle-ai: brew tap; archify: `npx skills add tt-a1i/archify -g`; codegraph: su CLI/MCP).
- Decisión abierta a confirmar: ¿el chequeo vive solo en cada SKILL.md, o también en el `install.sh` (cuando exista)?
