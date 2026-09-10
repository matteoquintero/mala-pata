---
name: sdd-preview
description: >
  Resumen ejecutivo pre-Apply — un walkthrough corto en cristiano de lo que sdd-apply va a
  hacer, con gate humano duro que FRENA hasta obtener aprobación. El propio preview lee
  tasks + design y decide su modo audit (0, 1 o 2 revisores ciegos) — no depende de que
  sdd-tasks lo pida. Trigger: when the orchestrator launches the preview phase between
  `sdd-tasks` and `sdd-apply`.
license: MIT
metadata:
  author: mala-pata
  version: "3.0"
---

## Purpose

Producir un **resumen ejecutivo corto** de qué va a hacer `sdd-apply`, en lenguaje llano ("en cristiano"), para que el humano lo lea en ≤30 segundos y decida si el plan sigue en pie o se salió del camino.

Esta fase sitúa entre `sdd-tasks` (plan aprobado) y `sdd-apply` (código). **NO** escribe código, migraciones, ni archivos del proyecto. Su output es un artefacto corto y un **gate humano DURO** que no se puede pasar con un "sí" ciego.

**Objetivo primario**: resumen para tomar una decisión rápida.
**Objetivo secundario (condicional, autodecidido)**: auditoría adversarial con 0, 1 o 2 revisores — el número lo decide el propio preview (ver Self-assessment), no `sdd-tasks`.

## What You Receive

Del orchestrator:
- Change name
- Artifact store mode (`engram | openspec | hybrid | none`)
- Absolute path del worktree a inspeccionar
- Perfil del kickoff (FULL/STANDARD/LITE/MINIMAL) — determina target de palabras del resumen

El **modo audit y el número de reviewers (0/1/2) NO llegan del orchestrator ni de `sdd-tasks`** — los fija el propio preview en el paso de Self-assessment, antes de escribir el resumen.

## Execution and Persistence Contract

> Follow **Section A** (skill loading), **Section B** (retrieval), and **Section C** (persistence) from `skills/_shared/sdd-phase-common.md`.

Lecturas requeridas (parallel + `mem_get_observation` — previews truncados):
- `sdd/{change-name}/tasks` (required)
- `sdd/{change-name}/design` (required)
- `sdd/{change-name}/kickoff` (required — para leer DoD)
- `sdd/{change-name}/spec`, `sdd/{change-name}/proposal`, `sdd/{change-name}/explore` (contexto)

También leer el **código real del worktree** (Grep/Glob/Read) — no revisar en abstracto.

## Self-assessment — cuántos reviewers (0, 1 o 2)

Antes de escribir el resumen, con `tasks` + `design` (+ código real) ya leídos, el propio preview decide el modo audit. Esto reemplaza la señal que antes venía de `sdd-tasks` — `sdd-tasks` ya no la manda.

**Regla base (tomada del modelo de riesgo nativo de gentle-ai, `internal/reviewtransaction/risk.go`): el volumen NUNCA decide el número.** Ni cantidad de tasks, ni de archivos, ni de líneas estimadas — "un cambio de 5 líneas en autenticación pesa más que un rename mecánico de 5000 líneas" (cita del propio comentario del código de gentle-ai). El "Review Workload Forecast" que `tasks` sigue calculando (budget de 400 líneas) es para OTRA cosa — decidir si conviene partir en PRs encadenados — y **no es señal de riesgo acá**. Solo escala evidencia concreta, igual que en gentle-ai: se arma con las categorías que tu propio audit YA produce (Blast-radius, Reuse-first, Smells de arquitectura), leyendo el plan de tasks/design contra el código real.

**0 reviewers (solo resumen, sin audit)** — TODAS estas condiciones:
- Blast-radius: ningún archivo tocado cae en las señales de alto riesgo de abajo.
- Reuse-first: todo es **REUSA** o **ADAPTA** de un precedente exacto ya existente — nada queda como **NUEVO** estructural.
- Smells de arquitectura: ninguno.
- No toca archivos de configuración (`.env`, `package.json`/lockfiles, `go.mod`, `Dockerfile`, `Makefile`, o extensión `.json`/`.yaml`/`.yml`/`.toml`/`.ini`).

**1 reviewer** — el caso por defecto cuando no aplica ni 0 ni 2: hay algo **NUEVO** en Reuse-first o superficie nueva moderada, pero sin ninguna de las señales de alto riesgo de abajo.

**2 reviewers (doble ciego + síntesis)** — CUALQUIERA de estas señales concretas en el Blast-radius o en el código real que va a tocarse (mismas categorías que gentle-ai usa para su tier "high"):
- Ruta/símbolo con `auth`, `security`, `payments`, `webhook`, o manejo de tokens/credenciales/secrets.
- Cambio de bit ejecutable (un archivo pasa a/desde ejecutable), scripts de shell (`.sh`/`.bash`/`.zsh`), o workflows de CI (`.github/workflows/*.yml`).
- Migración de datos/DDL, o cualquier dato personal/sensible.
- Reuse-first marca **NUEVO** un patrón/arquitectura sin precedente 1:1 en el repo (no un componente más del mismo tipo — un patrón genuinamente nuevo).
- Smells de arquitectura con severidad **alta**.
- `design` dejó decisiones abiertas sin resolver del todo con el humano.

Dejá explícito en el artefacto (línea corta, no una sección aparte) el número elegido y **la señal concreta** que lo motivó — nunca "audit activo" sin decir cuál evidencia lo disparó.

Persistencia:
- **engram**: `sdd/{change-name}/preview` (type: `architecture`).
- **openspec / hybrid**: `preview.md` en la carpeta del change.
- **none**: return inline; no escribir archivos.

## Output — Resumen ejecutivo (SIEMPRE)

Un artefacto markdown con exactamente **4 secciones obligatorias**, ninguna vacía:

```markdown
# Preview: <change-name>

**Perfil**: <FULL/STANDARD/LITE/MINIMAL> · **Modo audit**: <activo/inactivo>

## Voy a hacer
- <acción concreta 1 — verbo + qué>
- <acción 2>
- <acción 3>
(3-5 bullets, cada uno accionable)

## Afecta
- <archivos/módulos/servicios impactados, 1-3 líneas>
- <lo que NO se toca, si el scope tiene bordes importantes>

## DoD (del kickoff)
<copia textual del "Definition of Done" del kickoff — NO reinventar criterios>

## Riesgos
- <cosas que pueden salir mal, cosas que mirar de cerca — 1-3 líneas>
```

### Target de palabras por perfil

| Perfil | Target del resumen |
|---|---|
| MINIMAL | ≤100 palabras |
| LITE | ≤150 palabras |
| STANDARD | ≤250 palabras |
| FULL | ≤400 palabras |

Target orientativo, no cap duro. Si necesitás más para ser honesto, decilo.

### Reglas del resumen

- **Cero jargon innecesario**: un humano no-autor debe entender qué va a pasar.
- **No hay resumen vacío**: si "Voy a hacer" tiene solo 1 bullet, algo está mal — o el change es demasiado chico para pasar por preview, o el plan no está listo.
- **DoD es copia textual del kickoff**, no reinvención — el preview NUNCA reescribe ni "mejora" criterios por su cuenta, y por default **no audita el DoD**. Solo levantás un criterio como hallazgo si es un **bloqueante duro de comprobabilidad** (un criterio que literalmente NO se puede verificar tal como está escrito — no "podría estar mejor", no "quedó un poco viejo"). Ese umbral alto es a propósito: cazar criterios mejorables en cada pasada es lo que generaba el loop de volver a design/tasks sin fin. Si de verdad hay un bloqueante y el humano elige "Ajustar", es la ruta barata (editar el DoD del kickoff + volver al gate, ver la opción Ajustar), NO regeneración de plan.
- **"Afecta" es concreto**: nombres de archivos/módulos, no genéricos ("varios archivos" prohibido).

## Output — Modo audit (cuando el self-assessment decide ≥1 reviewer)

Cuando el self-assessment de arriba decide ≥1 reviewer, después del resumen se agrega este bloque:

```markdown
## Auditoría adversarial

### Blast-radius
| Archivo | Acción | ~LOC | Símbolo público |
|---|---|---|---|
| <path> | NUEVO/MODIFICADO/BORRADO | <n> | <symbol> |

### Reuse-first (REUSA / ADAPTA / NUEVO)
- <pieza nueva 1>: **REUSA** `<file:line>` — <helper existente que aplica>
- <pieza 2>: **ADAPTA** `<file:line>` — <mínima diferencia>
- <pieza 3>: **NUEVO** — <por qué no existe equivalente>

### Smells de arquitectura
- **alta/media/baja**: <descripción> — `<file:line>` o `<task ref>`

### Supuestos silenciosos
- <default que Apply hornearía si nadie mira>
```

**Reglas del audit**:
- El número de reviewers (1 o 2) ya quedó fijado en el Self-assessment. El orchestrator solo hace el fan-out según ese número.
- Reviewers son **adversariales**: default a suspechar duplicación/over-engineering; el plan tiene que probar novedad.
- **Empty audit prohibido**: si no hay hallazgos, explicitar QUÉ se buscó y por qué cada cosa se descartó.
- Reviewers NO ven el output del otro. Se hace synthesis (merge + dedup) después.

## UNA SOLA PASADA es el objetivo (ANTI-LOOP)

Preview está diseñado para correr **UNA vez** y ser lo bastante completo como para que el humano decida en esa única pasada. Hacé la auditoría a fondo la primera vez — no dejes nada "para mirar en una segunda vuelta", porque no hay segunda vuelta como norma. El resumen + audit + gate salen completos de una.

"Ajustar" es un **escape raro**, no un round-trip esperado. Si el humano lo elige:
- El orchestrator hace SOLO el cambio puntual pedido (editar el DoD del kickoff, o el arreglo de plan específico si era defecto real de plan).
- **Al volver, preview NO se re-ejecuta**: nada de nuevo resumen, nada de nueva auditoría, nada de buscar hallazgos frescos. Se muestra un **delta corto** ("pediste X → se hizo Y") y se va **DIRECTO al gate**. Esta es la regla que hace imposible el loop: volver de un ajuste nunca genera hallazgos nuevos, porque no se re-audita.
- Ese re-gate ofrece solo: **Aprobar** (con el delta a la vista) o **Detener**. NO vuelve a ofrecer "Ajustar" — si el delta no alcanzó, es Detener y repensar fuera del ciclo, no otra vuelta de regeneración.

Backstop duro: **nunca hay una tercera interacción de preview** para el mismo change. Pasada 1 (completa) → a lo sumo un re-gate de delta → apply o stop. Un change no puede quedar rebotando entre preview y design/tasks.

## Hallazgo de nivel-objetivo vs nivel-plan (clasificá antes de disponer)

Preview revisa **el plan**, no **el objetivo** — el QUÉ ya tuvo que quedar cerrado en explore/propose/spec (ver `mala-pata-loop-start`, Regla dura #4). Por eso, antes de meter cualquier hallazgo en la tabla de disposición, clasificá su **nivel**:

- **Nivel-plan** (duplicación, over-engineering, flujo hardcodeado, mala capa, reuse ignorado, task mal pensada) → es lo que preview SÍ dispone: REUSAR / REFACTOR / IGNORAR, o va por "Ajustar" si necesita un arreglo de plan puntual. Camino normal.
- **Nivel-objetivo** (el hallazgo no es "el plan está mal" sino "el plan resuelve el objetivo equivocado / el objetivo no está definido / falta la mitad del alcance / el DoD no es testeable y no es un simple reword") → **NO lo dispongas** (no es REUSAR/REFACTOR/IGNORAR) y **NO lo mandes por "Ajustar"** (Ajustar es para plan o para reword de DoD, nunca para redefinir el QUÉ). Un defecto de objetivo que llega hasta acá significa que se coló por el gate de origen. La disposición correcta es **frenar y devolverlo atrás**:
  - El gate ofrece **🛑 Detener** con motivo explícito `objetivo-no-listo → explore/propose`.
  - El orchestrator marca `sdd/<change>/state = "objective-not-ready-at-preview"` (con la ruta absoluta del worktree vivo, igual que el pause normal) y el ciclo vuelve a **explore o propose** a redefinir el QUÉ.
  - NO se re-audita el plan, NO se re-gatea el preview. Es un **escape hacia atrás**, no un round-trip: no viola "una sola pasada" (el preview termina acá; lo que sigue es planeación desde más atrás, no otra vuelta de preview).

Regla de oro: **si te encontrás debatiendo con el humano si el objetivo está bien, ese debate NO va en preview.** Cortalo y devolvé a explore/propose. Preview asume objetivo definido; su trabajo empieza donde el objetivo termina.

## The GATE — DURO, siempre corre, siempre frena

El gate corre **SIEMPRE**, tenga o no audit activo. Es **inmune a cualquier modo "auto"** del resto del SDD — esta fase FRENA independientemente. El artefacto DEBE incluir el gate payload listo para la función de preguntas interactiva disponible en el CLI.

### Opciones del gate (3 en la pasada única; si hubo "Ajustar", el re-gate del delta trae solo 2: Aprobar / Detener — ver ANTI-LOOP)

**✅ Aprobar (requiere autotest de comprensión)**
- El humano escribe en 1 línea qué entendió que se va a hacer.
- Sin esa línea, no se aprueba. **Micro-forcing-function** contra rubber-stamp.
- Si la respuesta no coincide razonablemente con "Voy a hacer" del resumen, el orchestrator pide re-lectura y reformulación.
- Al aprobar → `next_recommended: sdd-apply`.

**⚠️ Ajustar antes (textarea libre)** — *escape raro; al volver es un re-gate de delta (Aprobar/Detener), NO otra pasada de preview (ver ANTI-LOOP).*
- El humano escribe feedback: qué cambiar, qué falta, qué está mal.
- **Ruta según el TIPO de ajuste — NO todo ajuste regenera el plan** (esto es lo que evita el loop):
  - **DoD stale / criterio incomprobable u obsoleto** → el orchestrator edita SOLO la sección Definition of Done del archivo de kickoff y **vuelve DIRECTO al gate de preview**. NO reejecuta design/tasks — un ajuste de criterio no es un defecto de plan.
  - **Defecto real de plan** (duplicación, mala arquitectura, flujo hardcodeado, task mal pensada) → ahí sí vuelve a `sdd-tasks` o `sdd-design` según el feedback.
  - **Defecto de objetivo** (el QUÉ está mal/incompleto, no el plan ni el wording del DoD) → NO es "Ajustar": es **Detener con motivo `objetivo-no-listo`** y volver a explore/propose (ver "Hallazgo de nivel-objetivo vs nivel-plan"). Ajustar nunca redefine el objetivo.
  - Ante la duda entre DoD y plan, es DoD/gate (camino barato), no regeneración.
- Estado en engram: `sdd/<change>/state = "adjustment-requested-at-preview"` con feedback + el tipo de ruta tomada.

**🛑 Detener (pausa retomable, Opción A)**
- Marca `sdd/<change>/state = "paused-at-preview"` en engram, con motivo opcional del humano, **y la ruta absoluta del worktree que queda VIVO** — un SDD pausado es el candidato #1 a filtrar worktrees huérfanos; registrarlo es lo que permite que el radar lo liste para limpieza futura.
- **NO borra** artefactos previos (explore/proposal/spec/design/tasks quedan en engram).
- **Retomable con `/mala-pata-loop-start <ruta-del-kickoff>`** — al retomar, loop-start detecta el `paused-at-preview` y salta directo a este mismo gate (NO uses `/sdd-continue`: es de gentle-ai y no conoce la fase preview — rutea por encima del gate).
- Estado registrado para memoria futura (si vuelve en 2 semanas sabe por qué frenó).
- **Variante objetivo-no-listo**: si el motivo de detener es un defecto de **nivel-objetivo** (ver la sección de clasificación), el estado es `sdd/<change>/state = "objective-not-ready-at-preview"` en vez de `paused-at-preview`, y el retome NO es en el gate de preview sino en **explore/propose** (hay que redefinir el QUÉ primero). El resto es igual: worktree vivo registrado, artefactos previos intactos.

### Reglas del gate

- El orchestrator es quien corre la función de preguntas interactiva disponible en el CLI — el reviewer sub-agent NO.
- No hay "OK global" que barra sin lectura. La única forma de decir sí es escribir la línea del autotest.
- El gate está incluido en el artefacto como `gate_payload` — el orchestrator lo lee y lo dispara.

## Doble reviewer (solo cuando el self-assessment decidió 2)

Cuando el Self-assessment decidió 2 reviewers:
- Reviewers corren **en paralelo, ciegos** entre sí.
- Cada uno produce su set de findings adversarial (audit).
- Un run separado en modo `synthesis` merge/dedup los findings y produce el artefacto único.
- El orchestrator hace el fan-out — el reviewer sub-agent NO llama a otros agentes.

## What to Do — Role: `reviewer`

1. Leer artefactos y código real del worktree.
2. Correr el **Self-assessment** y fijar el número de reviewers (0/1/2).
3. Producir el **resumen** (4 secciones obligatorias, respetando target del perfil).
4. Si el self-assessment decidió ≥1: producir el bloque audit.
5. Preparar el `gate_payload` con las 3 opciones fijas.
6. Devolver al orchestrator — NO persistir a menos que seas `synthesis`.

## What to Do — Role: `synthesis` (solo cuando hay 2 reviewers)

1. Recibir los 2 reviews.
2. Merge + dedup del audit (mantener severidad más alta si overlappean; señalar hallazgos que solo uno vio).
3. Ensamblar el artefacto único (resumen + audit + gate).
4. Persistir a `sdd/{change-name}/preview` (Section C).

## Rules

- **NUNCA** escribir código, migraciones, o archivos del proyecto.
- **NUNCA** lanzar sub-agents desde el reviewer.
- **Empty resumen prohibido**: las 4 secciones tienen contenido concreto o no hay preview.
- **Empty audit prohibido** (cuando activo): explicitar qué se buscó y descartó.
- **Gate no se puede pasar sin autotest** (1 línea escrita).
- **Gate frena aunque el resto del SDD esté en modo auto** — esta fase es interactiva por diseño.
- Size budget del **resumen** por perfil (ver tabla). Audit no tiene cap.
- Return envelope per **Section D** from `skills/_shared/sdd-phase-common.md`; `next_recommended: sdd-apply` **solo** después de aprobación del gate.
- **Registrá las disposiciones en el artefacto persistido** (`sdd/<change>/preview`): por cada hallazgo, su disposición final (REUSAR / REFACTOR / IGNORAR / aceptado-como-gap). El objetivo es UNA pasada: si hubo un "Ajustar", registrá también el delta pedido y que el cierre fue por re-gate de delta, no por otra pasada de auditoría (sección ANTI-LOOP).
