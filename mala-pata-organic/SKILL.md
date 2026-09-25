---
name: mala-pata-organic
description: Genera el kickoff de un cambio ODD (Organic Driven Development). Se invoca DESPUÉS de que el carril ya fue decidido — normalmente vía `/mala-pata-triage`, o directo cuando el humano ya sabe que es organic. Asume route=organic y captura/confirma el formato estricto (Qué, Why, Done, Decisiones, Riesgo) — si triage pasó un borrador, lo confirma/completa en vez de arrancar de cero. Si el formato queda completo, escribe el kickoff en una carpeta hermana del proyecto (fuera del repo) con un puntero de una línea en engram. NO ejecuta el ciclo ODD — el ejecutor es `/mala-pata-organic-start <ruta-al-kickoff>`. Red de seguridad: si al capturar los campos aparece que `Decisiones` está sin resolver, rebota a `/mala-pata-loop` — pero decidir el carril ya no es su trabajo primario.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "3.2.0"
---

# /mala-pata-organic — Generador de kickoff ODD (route ya decidido)

Pedido del usuario: **entrada entregada por el CLI** (o el borrador de campos que pasó `/mala-pata-triage` al decidir organic)

Tu único trabajo es convertir ese pedido en un **kickoff ODD** — un archivo markdown, guardado fuera del repo, que otro agente (`/mala-pata-organic-start`) va a consumir para CORRER el ciclo. Es a ODD lo que `/mala-pata-loop` es al SDD: generás el contexto, no lo ejecutás.

> **Asumís route=organic.** La decisión de carril (organic vs loop vs roadmap) la toma `/mala-pata-triage` ANTES de llegar acá. Si venís de triage, ya tenés un borrador de Qué/Why/Done/Decisiones/Riesgo — tu trabajo es **confirmarlo o completarlo**, no re-derivarlo desde cero. Si te invocaron directo (el humano ya sabía que era organic), hacé la misma captura desde el pedido crudo.
> **NO ejecutás nada.** NO creás el worktree, NO explorás el código, NO escribís código, NO abrís PRs. Solo capturás/confirmás el formato y, si queda completo, escribís el kickoff.
> El resultado es: (a) el kickoff listo para `/mala-pata-organic-start`, o (b) el rebote de red-de-seguridad a `/mala-pata-loop` si aparece que Decisiones no estaba resuelto, o (c) preguntas puntuales si falta un campo bloqueante.

> **El protocolo ODD es la fuente de verdad.** Sus 7 pasos, el feature-doc, los work-unit commits, RDD por commit y el delivery slicing viven en tu **CLAUDE.md global** (`## Implementation Routing → ### ODD protocol`). Este skill no los duplica — el kickoff que generás es el insumo que `/mala-pata-organic-start` usa para seguirlos. Si el CLAUDE.md y este skill difieren en la mecánica de ODD, **manda el CLAUDE.md**.

> **Organic usa workers de ODD (direct/delegated), NUNCA agentes `sdd-*`.** El preflight `PreToolUse:Agent` de gentle-ai (`gentle-ai sdd-preflight-hook`) solo intercepta dispatches `sdd-*` — no aplica ni a este skill ni a `/mala-pata-organic-start`. No inventes un gate de preflight acá: no existe para este carril.

## Reglas duras

> **#1 — Red de seguridad, no tu trabajo primario: si al capturar `Decisiones ya tomadas` te das cuenta de que está sin resolver** (arquitectura sin resolver, contrato/endpoint nuevo sin decidir, riesgo que amerita ciclo completo con preview), **no fuerces organic — rebotá a `/mala-pata-loop`**. Esto es un fallback: lo normal es que `/mala-pata-triage` ya haya filtrado esto antes de que llegues. El tamaño del cambio o el conteo de archivos NUNCA fuerza el loop — ODD maneja lo chico y lo **substancial**.
> **#2 — Base: proponé y confirmá, no crees nada.** La base sale de DONDE VIVE el código que se va a tocar (`main`/`development`, o una feature en curso). Proponé con tu razón en una línea ("el código vive en X") y esperá el OK antes de fijarla en el kickoff. Este skill NO crea el worktree — eso lo hace `/mala-pata-organic-start` con la base ya confirmada acá.
> **#3 — El gate es sobre el formato, no sobre el tamaño.** Un cambio de 5 líneas con Qué/Done/Decisiones concretos pasa en una interacción de 10 segundos — una línea por campo alcanza. El gate rechaza lo SUB-especificado, no lo corto. Si estás pidiendo más de una línea por campo para un cambio chico, estás rearmando SDD adentro de organic: pará.
> **#4 — Rutas absolutas SIEMPRE** en cualquier comando que muestres o dejes en el kickoff (`worktree:` es una ruta absoluta propuesta, nunca relativa).

## Fase 0 — Autorizar (ODD paso 1, read-only guard)

¿El pedido autoriza un **cambio**? Investigación, explicación, review, auditoría, comparación, o propuesta/planeación = **read-only** salvo que el humano pida implementar u otra mutación explícita.
- Read-only → inspeccioná/explicá/recomendá, pero **NO** generes kickoff, NO propongas worktree, NO avances de fase.
- Intención ambigua o condicional → 1 pregunta y quedate read-only hasta la respuesta.

Si el pedido autoriza cambio, seguí al gate.

## Fase 1 — Capturar/confirmar el formato estricto (insumo del kickoff, no el ruteo)

El carril ya está decidido (route=organic) — esto no es más el gate que elige entre organic/loop/roadmap, eso ya lo hizo `/mala-pata-triage`. Acá **recolectás/confirmás** los campos que van a quedar en el kickoff. Si `/mala-pata-triage` te pasó un borrador, arrancás de ahí y confirmás con el humano en vez de inferir desde cero:

| Campo | Bloquea | Qué prueba |
|---|---|---|
| **Qué** | SÍ | Objetivo = comportamiento/resultado observable y concreto. "Mejorar X" sin blanco concreto → FALLA. |
| **Why** | NO | Motivación en 1 línea. Siempre se pide, nunca bloquea — pero FLUYE al feature-doc y al body del PR. |
| **Done** | SÍ | Definición testeable = el CUÁNDO: "cuando X, pasa Y" o el check que lo prueba. |
| **Decisiones ya tomadas** | SÍ | El approach/arquitectura está DECIDIDO o es obvio. |
| **Riesgo** | NO (opcional) | Blast radius en una línea. |
| **Dónde** | NUNCA bloquea | Es un OUTPUT de la fase Explore de `/mala-pata-organic-start`, no una precondición — en ODD explorás primero. El humano puede dejar una pista opcional, pero jamás bloquea. |

### Qué hacer con el resultado

- **Qué + Done + Decisiones concretos (confirmados)** → generá el kickoff organic (Fase 2).
- **Cualquiera de los tres sigue en "no sé" al confirmar** → NO generes kickoff:
  - **Decisiones falla** (recién se descubre acá que la arquitectura no estaba resuelta) → red de seguridad, Regla dura #1 → rebotá a **`/mala-pata-loop`** (SDD, con preview y design formal).
  - **Qué/Done están claros pero el alcance es enorme o cruza varios loops** → recomendá **`/mala-pata-roadmap`** (descomponer primero).
  - **Solo Dónde es "no sé" y el resto está claro** → NO es motivo de rebote — es organic normal, vas a explorar en `/mala-pata-organic-start`.

### Proporcionalidad (no negociable, Regla dura #3)

Un cambio chico = una línea por campo, ~10 segundos de llenar. El gate no pide un párrafo por campo — pide que cada campo bloqueante tenga un **contenido concreto**, sea largo o corto. No infles el kickoff de un fix de 5 líneas con secciones que no aportan: eso reconstruye SDD adentro de organic y le mata el carril rápido.

## Fase 2 — Generar el kickoff de organic (si la captura quedó completa)

1. Derivá un `change-name` corto en kebab-case.
2. **Base — proponé y confirmá (Regla dura #2)**: de dónde vive el código (`main`/`development` o una feature en curso). Esperá el OK.
3. **Tipo de rama — aconsejá y confirmá**: `feature/`/`fix/`/`hotfix/`/`refactor/`/`chore/`/`docs/` — nunca `sdd/`. El nombre completo va como `worktree` propuesto (ruta absoluta, `<ABS-repo>-worktrees/<change-name>`) — **no lo creás acá**, eso lo ejecuta `/mala-pata-organic-start`.
4. **Init guard**: `mem_search("sdd-init/{project}")` (solo el ítem EXACTO). Si no existe → corré `sdd-init` primero para detectar stack y `strict_tdd`. Tomá `tdd_mode` de ahí para el frontmatter.
5. **Idempotencia**: `mem_search("odd/<change-name>/kickoff")`. Si ya existe uno igual/parecido → ofrecé actualizar o cambiar nombre.
6. Armá el kickoff con esta estructura (mismo mecanismo de persistencia que `/mala-pata-loop` — ver Fase 3):

```markdown
---
change_name: <change-name>
project: <project>
route: organic
base: main|development|<feature-en-curso>   # confirmado con el humano — Regla dura #2
branch: <tipo>/<change-name>                # tipo confirmado — nunca sdd/
worktree: <ruta absoluta propuesta>          # <ABS-repo>-worktrees/<change-name> — organic-start lo crea, no este skill
tdd_mode: <strict|standard>                  # de sdd-init/<project>
created_at: <ISO 8601>
---

# Kickoff ODD: <change-name>

## Qué
<objetivo concreto y observable — una línea si el cambio es chico>

## Why
<motivación en 1 línea — fluye al feature-doc y al PR>

## Done
<definición testeable — "cuando X, pasa Y" o el check que lo prueba>

## Decisiones ya tomadas
<approach/arquitectura decidido u obvio — confirmalo, no lo redecidas>

## Riesgo
<blast radius en 1 línea — opcional, "N/A" si no aplica>

## Dónde (hint opcional — a descubrir en Explore)
<archivo(s)/módulo si el humano ya lo sabe, o "a determinar en Explore">
```

## Fase 3 — Puntero de una línea en engram

Igual que `/mala-pata-loop` (Paso 5): el kickoff vive en un **archivo**, no en engram — así nunca se sube al repo por accidente.

1. **Ubicación — carpeta hermana del proyecto, NUNCA dentro del repo**: `<carpeta-del-proyecto>-mala-pata/`, al mismo nivel que la carpeta del proyecto. Ejemplo: proyecto en `/ruta/a/mi-proyecto` → kickoff en `/ruta/a/mi-proyecto-mala-pata/<change-name>.md`. Creá la carpeta (`mkdir -p`) si no existe.
2. Escribí el kickoff completo de la Fase 2 en `<carpeta-hermana>/<change-name>.md`.
3. **Puntero liviano en engram**: `mem_save` con `topic_key: "odd/<change-name>/kickoff"`, `type: "architecture"`, contenido de **una sola línea**: `Kickoff ODD en archivo: <ruta absoluta>`. No dupliques el contenido acá — el archivo es la única fuente de verdad.
4. Si engram no está disponible, el archivo sigue siendo la fuente de verdad — avisá en una línea que el puntero no quedó guardado (afecta la idempotencia futura, no el kickoff en sí).

## Fase 4 — NO ejecuta · cierre obligatorio (resumen + kickoff)

Tu respuesta al humano es un cierre **OBLIGATORIO y estándar (resumen + kickoff)** — no es opcional ni "solo la ruta". Todo el resumen sale del kickoff que acabás de escribir, sin inventar nada. Emití exactamente esta estructura (mismo formato que `/mala-pata-loop` Paso 5):

- Título: `**Kickoff listo — <change-name>**`
- Resumen (una línea por ítem):
  - **Qué:** <una línea>
  - **Carril:** organic
  - **Base → rama:** <base> → <tipo>/<change-name>
  - **Worktree:** <ruta absoluta>
  - **DoD:** <criterio testeable, una línea>
- **Kickoff:** `<ruta absoluta del .md>`
- **Siguiente paso** (en bloque de código, copy-paste):

  ```
  /mala-pata-organic-start <ruta absoluta del .md>
  ```

Este bloque es la ÚNICA forma de cerrar en el happy path.

**Únicas excepciones** (cuando la respuesta no es solo eso):
- Fase 0 read-only → quedate en modo lectura, sin kickoff.
- Campo bloqueante sigue sin resolver al confirmar → una línea con el campo que falló + la recomendación (`/mala-pata-loop` o `/mala-pata-roadmap`), sin crear kickoff.
- Confirmación de base/tipo de rama (Fase 2, puntos 2-3) → única pregunta permitida antes de escribir el kickoff.
