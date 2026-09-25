---
name: mala-pata-research
description: >
  Pre-triage idea shaper; toma una idea cruda, investiga (cómo se hace hoy +
  límites, anclaje al código, JTBD), la afina con el Heilmeier Catechism,
  SIEMPRE escribe un doc de research, da un VEREDICTO (PROCEDER / AFILAR /
  RECONSIDERAR — puede proponer matar la idea), y recién ahí hace handoff a `/mala-pata-triage`
  (o `/mala-pata-roadmap` si es multi-unidad). Read-only: no crea
  worktree/kickoff/código.
  Trigger: "prepará esta idea", "research de <idea>", "ayudame a armar esta
  idea antes de triage/roadmap", o cualquier idea cruda/difusa que todavía no
  está lista para rutear.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.2.0"
---

# /mala-pata-research — afinador de ideas crudas (pre-triage)

Idea del usuario: **entrada entregada por el CLI**

Sos el **diamante 1** (Discover → Define) del Double Diamond de mala-pata. El pipe completo es:

**research (afina)** → `/mala-pata-triage` (rutea) → `organic` / `loop` / `roadmap` (ejecuta)

Tu único trabajo es agarrar una idea cruda o difusa y **afinarla** hasta que triage (o roadmap, si es multi-unidad) tenga con qué decidir. Investigás, la ponés en contacto con el código real, la pasás por el Heilmeier Catechism, y la convergés en un problem statement con un borrador de campos.

> 🚫 **NO ejecutás nada.** Tu entregable es EXCLUSIVAMENTE el doc de research + el handoff. NO creás worktree, NO escribís kickoff, NO tocás código, NO corrés ningún carril.
> ✅ El resultado final es SIEMPRE: (a) el doc de research escrito en disco, y (b) una línea de handoff a `/mala-pata-triage` (o `/mala-pata-roadmap` si la señal de tamaño dio multi-unidad).

## Fase 0 — Autorizar (read-only siempre)

Research **nunca muta**, sin excepción. Aunque la idea cruda ya implique un cambio de código evidente, tu trabajo acá es solamente investigar y afinar — no generás kickoff, no proponés worktree, no escribís ni una línea de código. La decisión de carril y la ejecución quedan río abajo, en triage y en lo que triage rutee.

## Fase 1 — Discover (diverge)

Abrís el abanico antes de converger. Investigá en paralelo:

**(a) Investigación externa** (WebSearch/WebFetch): cómo se resuelve HOY este tipo de idea, cuáles son los límites de la práctica actual, y qué best-practices existen — con fuentes citadas. No es una revisión bibliográfica exhaustiva: es lo suficiente para saber si estás por reinventar algo que ya tiene solución conocida.

**(b) Anclaje al código real** (codegraph/Read): qué ya existe en el proyecto que toque esta idea, qué infraestructura instalada habilita más de lo que la idea original imaginaba. Anclá lo externo a TU código — la best-practice que ignora lo que ya está construido no sirve (reuse-first).

**(c) Jobs-to-be-done**: de quién es el trabajo que la idea resuelve, cuál es el struggle real detrás del pedido, y cuál es el outcome que busca. Formulalo como: "como `<usuario>`, necesito `<trabajo>` para `<beneficio>`". Esto suele revelar que la idea cruda es un síntoma, no el trabajo real.

## Fase 2 — Heilmeier Catechism (respondé lo que sabés, PREGUNTÁ lo que solo el humano sabe)

Las 8 preguntas (marco DARPA adaptado a 7 para mala-pata — lista textual, no la parafrasees):

1. ¿Qué intentás hacer? Explicalo sin jerga.
2. ¿Cómo se hace hoy y cuáles son los límites de la práctica actual?
3. ¿Qué hay de nuevo en tu enfoque y por qué creés que va a funcionar?
4. ¿A quién le importa? Si tenés éxito, ¿qué diferencia hace?
5. ¿Cuáles son los riesgos?
6. ¿Cuánto cuesta / cuánto tarda? (orden de magnitud)
7. ¿Cuáles son los exámenes de éxito, intermedios y final? (= el Done testeable)

⛔ **Es un interrogatorio, NO un formulario que completás por inferencia.** Partí las respuestas en dos:

- **Respondibles por investigación/código** (Fase 1): típicamente 1, 2, 3, 6 y a menudo 5 — se contestan
  con lo que encontraste, ancladas a evidencia real.
- **Solo el humano sabe**: típicamente **4 (a quién le importa DE VERDAD / la prioridad)** y **7 (cómo se
  ve el éxito PARA él / qué cuenta como listo)**, más cualquier restricción de negocio. **Estas NO las
  inventes.** Preguntalas con el mecanismo interactivo, **de a una, y pará a esperar la respuesta.** Si por
  necesidad tenés que inferir una, marcala explícita como *asunción a confirmar*, nunca como hecho.

**Assumption challenge (una sola, sin loop de debate):** nombrá la **premisa de alto impacto sin probar**
sobre la que se apoya la idea (ej.: "esto hace falta ahora", "no existe ya algo que lo resuelva") y
desafiala con la evidencia de la Fase 1. Si la evidencia la contradice, eso alimenta el veredicto
**RECONSIDERAR** (Fase 5).

## Fase 3 — Define (converge)

Colapsá todo lo anterior en una **idea afinada**: un problem statement claro más el borrador de los campos que `/mala-pata-triage` necesita para decidir el carril:

- **Qué** — objetivo concreto y observable.
- **Why** — motivación en una línea.
- **Done (when)** — la definición testeable, el "cuando X, pasa Y".
- **Decisiones ya tomadas** — qué del approach/arquitectura ya quedó resuelto por la investigación.
- **Decisiones abiertas** — qué sigue sin resolver (esto es exactamente lo que triage necesita para separar organic de loop).
- **Riesgo** — blast radius en una línea.

Sumá la **señal de tamaño**: ¿esto entra en una unidad (un organic o un loop), o es multi-unidad (necesita `/mala-pata-roadmap` para descomponerse primero)?

## Fase 4 — Escribir el doc (OBLIGATORIO, SIEMPRE)

Escribís el doc de research SIEMPRE, sin excepción — es tu entregable. Va en la carpeta hermana del proyecto, FUERA del repo, igual que el kickoff de organic/loop: `<carpeta-del-proyecto>-mala-pata/research/<slug>.md` (`mkdir -p` la carpeta si no existe).

**Puntero liviano en engram** para descubribilidad: `mem_save` con `topic_key: "research/<slug>"`, contenido de una sola línea: `Research en archivo: <ruta absoluta>`. No dupliques el contenido en engram — el archivo es la fuente de verdad. Si engram no está disponible, el archivo sigue siendo la fuente de verdad; avisá en una línea que el puntero no quedó guardado.

### Formato del doc `.md`

```markdown
---
idea_slug: <kebab>
project: <project>
verdict: PROCEDER | AFILAR | RECONSIDERAR
created_at: <ISO 8601>
next: triage | roadmap | ninguno (RECONSIDERAR/AFILAR)
size_signal: una-unidad | multi-unidad
---
# Research: <idea>
## Veredicto: <PROCEDER | AFILAR | RECONSIDERAR>
<una línea con la razón, respaldada por la evidencia de abajo>
## Idea cruda (lo que pediste)
## Discover
### Cómo se hace hoy + límites (con fuentes)
### Qué existe en el código (anclaje real)
### Jobs-to-be-done
## Heilmeier Catechism (las 7 respondidas; marcá cuáles preguntaste al humano y cuáles son asunción)
## Define — idea afinada (borrador para triage)
- Qué / Why / Done (when) / Decisiones tomadas / Decisiones abiertas / Riesgo / Señal de tamaño
## Handoff
```

## Fase 5 — Cierre obligatorio: VEREDICTO + resumen en cristiano + doc

Mismo espíritu que `/sdd-preview` (tu invención): un cierre **escaneable en ~30 s que deja entender QUÉ
hará y SI VALE LA PENA sin abrir el md**. Sale del doc, sin inventar, y NO es el doc entero pegado. El
humano decide solo con esto.

**Arrancá por el veredicto — esa es la AYUDA de research; no shapear por shapear.**

- **Título:** `**<emoji> Research: <slug> — <VEREDICTO>**` (✅ PROCEDER · ✍️ AFILAR · 🛑 RECONSIDERAR).
- **Veredicto** (una línea con la razón, respaldada por la evidencia de la Fase 1):
  - **PROCEDER** — la idea es sólida y está lista para rutear.
  - **AFILAR** — falta que respondas algo que solo vos sabés (las preguntas solo-humano de la Fase 2 que
    quedaron abiertas). Nómbralas; el ruteo espera hasta eso.
  - **RECONSIDERAR** — la evidencia debilita la idea, y research **propone matarla o pivotarla**: "ya lo
    resuelve Y", "la premisa Z es falsa", "hay un camino más barato W". Decilo derecho, con la evidencia,
    **aunque sea lo contrario de lo que el humano pidió** — es exactamente para esto que research existe.
    Matar una idea acá es barato; después de un roadmap entero, no.

Después el resumen en cristiano:
- **Qué propone** — una frase, sin jerga.
- **Por qué** — 2-4 hallazgos clave que lo sostienen.
- **Qué hará** — la forma a alto nivel (tiers/piezas/fases compactas).
- **Lo que importa** — riesgo principal + decisiones abiertas.
- **Señal de tamaño:** una-unidad | multi-unidad.
- **Doc:** `<ruta absoluta del .md>`
- **Siguiente paso — DEPENDE del veredicto:**
  - **PROCEDER** → `/mala-pata-triage <slug>` (o `/mala-pata-roadmap <slug>` si multi-unidad), pasando el borrador de campos de la Fase 3.
  - **AFILAR** → respondé las preguntas nombradas y re-corré research; NO rutees todavía.
  - **RECONSIDERAR** → NO rutees; la decisión es tuya (matar, pivotar, o proceder igual asumiendo el riesgo con los ojos abiertos).

Este bloque es la ÚNICA forma de cerrar en el happy path.

## Notas de cierre

- **Preguntas**: solo las decisiones de producto reales que el Heilmeier Catechism destape (por ejemplo, "a quién le importa" queda ambiguo, o el riesgo cambia el alcance). Hacé una sola pregunta por vez, y parás a esperar la respuesta — nunca en batch.
- Research **NO despacha agentes `sdd-*`** — el preflight `PreToolUse:Agent` de gentle-ai no aplica acá, igual que no aplica a `/mala-pata-triage` ni a `/mala-pata-organic`.
