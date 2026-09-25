---
name: mala-pata-triage
description: Front-door único de mala-pata. Trigger — cualquier pedido de cambio, ANTES de tocar código. Lee el pedido, aplica el gate de forma (Qué + Done + Decisiones), y RESPONDE qué carril/skill correr — `/mala-pata-organic`, `/mala-pata-loop` o `/mala-pata-roadmap` — pasándole al carril elegido el borrador de campos ya inferidos. NO genera archivos, NO crea worktrees, NO ejecuta nada: es un skill de decisión, no de ejecución.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.0.0"
---

# /mala-pata-triage — Router de entrada (decide, no ejecuta)

Pedido del usuario: **entrada entregada por el CLI**

Tu único trabajo es **leer el pedido y decidir el carril**, después **responder cuál skill correr**. No generás kickoffs, no escribís archivos, no tocás código. Sos el gate — el mismo gate que documenta el diseño de mala-pata (`DESIGN-organic-loop-v2.md` §3: "el formato estricto ES el router") — separado de los tres carriles que lo consumen.

> **NO ejecutás nada.** NO creás worktree, NO escribís kickoff, NO corrés fases de ningún ciclo.
> El resultado es SIEMPRE una de estas cuatro cosas: (a) respuesta read-only directa, (b) "→ corré `/mala-pata-organic`" con el borrador de campos, (c) "→ corré `/mala-pata-loop`", (d) "→ corré `/mala-pata-roadmap`", o (e) `trabaje vago ` pidiendo lo mínimo.

> **Triage no despacha agentes `sdd-*`.** Es un skill de decisión puro — el preflight `PreToolUse:Agent` de gentle-ai no aplica acá, igual que no aplica a `/mala-pata-organic`.
> **Los tres carriles siguen invocables directo** si el humano ya sabe cuál es (`/mala-pata-organic`, `/mala-pata-loop`, `/mala-pata-roadmap`). Triage es la entrada recomendada cuando NO sabés por dónde va — no un paso obligatorio.

## Fase 0 — Autorizar (read-only guard)

¿El pedido es un **CAMBIO**? Investigación, explicación, review, auditoría o comparación son **read-only** — no hay carril que decidir, respondé directo desde tu propio conocimiento/exploración y listo (no es un carril de mala-pata).

Solo si hay intención real de cambiar código, seguís al gate.

Ambigüedad sobre si es cambio → 1 pregunta puntual, parás y esperás.

## Fase 1 — Gate de forma (diagnóstico rápido, no entrevista)

Evaluá el pedido contra estos tres campos, tal como los definió el diseño original (misma tabla que usa `/mala-pata-organic` y que `/mala-pata-loop` referencia como brújula):

| Campo | Bloquea | Qué prueba |
|---|---|---|
| **Qué** | SÍ | Objetivo = comportamiento/resultado observable y concreto. "Mejorar X" sin blanco concreto → FALLA. |
| **Done** | SÍ | Definición testeable = el CUÁNDO: "cuando X, pasa Y". |
| **Decisiones ya tomadas** | SÍ | El approach/arquitectura está DECIDIDO o es obvio. Es EL discriminador de loop. |
| **Why** | NO | Motivación en 1 línea — se pide, no bloquea. |
| **Riesgo** | NO (opcional) | Blast radius en una línea. |
| **Dónde** | NUNCA es gate | Se descubre en la fase Explore de organic/loop-start, no acá. |

Esto es un **diagnóstico desde el texto del pedido**, proporcional al pedido — no un formulario completo. Podés hacer **1 sola pregunta aclaratoria** SOLO si sin ella no podés decidir el carril (ambigüedad bloqueante real). Hacela, parás y esperás la respuesta.

## Fase 2 — Decidí y respondé el carril

- **Qué + Done enunciables y Decisiones resueltas/obvias** → **organic**.
  Respondé: `→ corré /mala-pata-organic`, y pasale como borrador los campos que ya inferiste (Qué / Why / Done / Decisiones / Riesgo) para que organic confirme en vez de arrancar de cero.

- **Decisiones sin resolver** (fork de arquitectura real, forma de contrato/endpoint sin decidir, requisitos en disputa) → **loop**.
  Respondé: `→ corré /mala-pata-loop`.

- **Qué/Done claros pero el alcance abarca varios ciclos** (multi-loop) → **roadmap**.
  Respondé: `→ corré /mala-pata-roadmap`.

- **Demasiado vago para siquiera enunciar Qué/Done** (y 1 pregunta no alcanza para arreglarlo) → **NO rutees.** Respondé estilo "trabajo vago", igual que el Paso 0 de `/mala-pata-loop`:

  > **trabajo vago ** — necesito al menos: *qué* querés lograr, *dónde* (módulo/feature, si lo sabés) y *cuándo está listo* (criterio verificable, no "que quede bien"). Con eso te digo el carril.

  Y parás ahí.

## Fase 3 — No hace nada más

No creás worktree, no escribís kickoff, no corrés fases de ningún ciclo. Tu respuesta termina en el punto anterior: o el carril + borrador, o el rebote a trabajo vago, o la única pregunta aclaratoria permitida.

**Únicas excepciones** (cuando la respuesta no es solo el ruteo):
- Fase 0 read-only → quedate en modo lectura, sin decidir carril.
- Ambigüedad bloqueante real → la única pregunta permitida antes de decidir.
- Gate demasiado vago → `trabajo vago `.
