---
idea_slug: orquestar-no-reinventar
project: mala-pata
verdict: PROCEDER
created_at: 2026-09-30
next: triage
size_signal: una-unidad
---

# Research: formalizar en cada skill "orquestar, no reinventar" (preflight de herramientas)

## Veredicto: PROCEDER (con un refinamiento a la premisa)
La idea es sólida y buildable: cada skill declara y chequea la(s) herramienta(s) de comunidad de la que depende, y guía a instalarla si falta. **Refinamiento:** no todas se "obligan" igual — la rigidez es POR HERRAMIENTA según haya o no fallback. Obligar donde no hay fallback (gentle-ai, archify); declarar + recomendar donde sí lo hay (codegraph).

## Idea cruda (lo que pediste)
> "Formalizar en cada skill el principio de orquestar y no inventar la rueda: que research obligue a tener codegraph instalado, organic/loop obliguen gentle-ai, y así con todas."

## Discover

### Cómo se hace hoy + límites
- Hoy el acoplamiento es **implícito**: los skills mencionan sus herramientas en prosa (states nombra archify, research nombra codegraph) pero **ninguno chequea** que estén instaladas. El fallo aparece a mitad de camino, no al arrancar.
- Patrón probado de la comunidad: **doctor / preflight de dependencias** (gentle-ai ya tiene `gentle-ai doctor` que valida herramientas en PATH). La práctica estándar es fail-fast con un hint de instalación.

### Qué existe en el código (anclaje real) — qué orquesta cada skill
| skill | herramienta que orquesta | ¿tiene fallback? | rigidez propuesta |
|---|---|---|---|
| research | codegraph (+ web para investigar) | sí (grep/Read; web opcional) | **declarar + recomendar** |
| triage | — (solo decide) | — | ninguna |
| organic / organic-start | gentle-ai (motor ODD + RDD) + engram | no | **obligar** |
| loop / loop-start / orchestrate(+start) | gentle-ai (agentes sdd-*) + engram | no | **obligar** |
| roadmap | codegraph (+ web) | sí (grep) | **declarar + recomendar** |
| radar | git (fuente de verdad) + engram | git siempre; engram parcial | git **obligar**, engram recomendar |
| walkthrough | gh (PRs) | sí | **declarar** |
| states | archify (renderer) + codegraph | archify no; codegraph sí | **obligar archify**, recomendar codegraph |
| sdd-preview | gentle-ai (parte del SDD) | no | **obligar** (vía loop) |

- Dato clave: **codegraph tiene fallback documentado** (la regla global dice "si no hay `.codegraph/`, usá Read/Grep"). Obligarlo contradice su propio diseño de degradación. gentle-ai y archify NO tienen fallback — son el motor / el renderer.

### Jobs-to-be-done
> "Como dueño de mala-pata (y como alguien que la comparte), necesito que cada skill **falle temprano y claro** si falta la herramienta que orquesta, para no descubrirlo a mitad del ciclo — y que quede explícito que mala-pata no reinventa, orquesta."

## Heilmeier Catechism (7)
1. **Qué (investigación):** agregar a cada skill un bloque "Requisitos" que declare sus herramientas, haga un preflight (chequeo) y dé el comando de instalación si falta.
2. **Cómo se hace hoy + límites (investigación):** implícito en prosa, sin chequeo; el fallo llega tarde.
3. **Novedad (investigación):** formaliza "orquestar no reinventar" en un contrato verificable; rigidez por-herramienta (no blanket) respetando los fallbacks existentes.
4. **A quién le importa (asunción a confirmar):** a vos y a quien instale mala-pata; falla temprana > falla a mitad de ciclo.
5. **Riesgos (investigación):** obligar de más donde hay fallback (codegraph) rompe el carril sin necesidad; obligar de menos donde NO hay fallback (gentle-ai) deja pasar el fallo tardío. Por eso: rigidez por-herramienta.
6. **Costo (investigación):** un bloque "Requisitos" por skill (13 archivos) — repetitivo pero mecánico una vez fijado el patrón. Una unidad grande.
7. **Exámenes de éxito (investigación):** correr un skill sin su herramienta obligatoria falla al arranque con un mensaje claro + cómo instalar; con herramienta con-fallback, avisa y sigue degradado.

## Define — idea afinada (borrador para triage)
- **Qué** — agregar a cada skill de mala-pata un bloque **"Requisitos / preflight"**: declara la(s) herramienta(s) que orquesta, chequea su presencia al arrancar, y guía a instalarla si falta. Rigidez por-herramienta (obligar sin-fallback; declarar+recomendar con-fallback).
- **Why** — formalizar "orquestar, no reinventar la rueda" como contrato verificable; fallar temprano y claro.
- **Done (when)** — cada skill tiene su bloque Requisitos; correr un skill sin su herramienta OBLIGATORIA frena al arranque con hint de instalación; con herramienta con-fallback, avisa y degrada; el patrón es consistente en los 13.
- **Decisiones ya tomadas (por research):** rigidez POR-HERRAMIENTA, no blanket; el preflight vive como primer paso del skill (markdown que el agente sigue); se apoya en el patrón doctor/preflight de la comunidad; se puede conectar al instalador de mala-pata (que discutimos) para chequear todo de una.
- **Decisiones abiertas (confirma el humano):**
  - La rigidez por-herramienta propuesta: ¿la aceptás (obligar gentle-ai/archify, recomendar codegraph), o querés obligar TODO duro como dijiste literal?
  - ¿Se hace solo como bloque en cada SKILL.md, o también lo chequea el `install.sh`/instalador?
- **Riesgo** — obligar de más rompe carriles con fallback; mitigado por la rigidez por-herramienta.
- **Señal de tamaño** — una-unidad (patrón + aplicarlo a 13 archivos; mecánico una vez fijado). Va a triage; probablemente organic.

## Handoff

```
/mala-pata-triage orquestar-no-reinventar
```
