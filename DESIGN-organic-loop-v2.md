# mala-pata v2 — Frontera organic/loop, kickoff universal y desacople del motor

> Design doc / roadmap. Estado: **PROPUESTO** (2026-09-24). Se ejecuta por fases (ver §9).
> Fuente de la discusión: sesión de diseño con el usuario tras el anuncio de gentle-ai
> (transmisión del 2026-09-23) de que **ODD pasa a ser el default y SDD sería eliminado**.

## 1. Contexto y motivación

- gentle-ai 3.7 hizo **ODD el workflow default obligatorio**; SDD quedó como rama on-demand
  dentro de ODD. En una transmisión (2026-09-23) el creador anunció que **piensan eliminar SDD**.
- `mala-pata-loop` / `mala-pata-loop-start` **dependen de los agentes `sdd-*` de gentle-ai**.
  Si los borran, el carril loop se rompe. `mala-pata-organic` (envuelve ODD) sobrevive.
- El SDD original es invención del usuario (previo a gentle-ai). No debe morir con un release ajeno.

**Objetivo de este rediseño:**
1. Definir con precisión **qué va a organic y qué va a loop** (hoy el criterio es difuso).
2. Hacer que **el motor sea enchufable** para que el borrado de SDD por gentle-ai no rompa mala-pata.
3. Reposicionar a mala-pata como **capa de decisión + orquestador de herramientas**, no "la herramienta de SDD".

## 2. Decisión de diseño — la frontera

La frontera **NO es tamaño** (chico vs grande). Es **certeza de forma**:

> **¿Ya sé QUÉ construir y puedo empezar a codear task-by-task, o primero tengo que DISEÑARLO?**

- **Sé qué** → **organic**. Aunque sea grande, aunque toque muchos archivos, aunque sea un
  endpoint nuevo — si puedo pasar una **buena especificación**, va a organic.
- **No sé qué / hay que decidir la forma antes de tocar código** → **loop**.

Criterios que **NO** disparan loop (van a organic): tamaño o cantidad de archivos por sí solos;
endpoint/contrato nuevo con **forma conocida**; feature multi-paso ya entendida; refactor con
target conocido; bugfix, aunque sea arquitectónico, si el fix ya se entiende.

Disparan loop (varias inclinadas a "sí", no una sola): elegir entre **alternativas de arquitectura
reales** sin resolver; **requisitos ambiguos/en disputa** que hay que fijar con el humano antes de
código; cambio tan grande/cross-cutting que **hacerlo mal = retrabajo caro**.

## 3. Insight central — el formato estricto ES el router

El "formato estricto para el prompt de organic" y el "cómo decidimos organic vs loop" **son lo mismo**.
El formato pregunta campos concretos; el acto de llenarlos ES el test de la frontera:

- **Se pueden llenar todos los campos concretos** → sé qué hacer → **se crea el kickoff de organic**.
- **Un campo sale "no sé / hay que decidir"** → NO sé qué hacer → el gate **no solo rechaza: diagnostica
  que es loop** (o que hace falta un spike previo).

No hace falta un decisor aparte: **el formato decide por construcción**. Determinístico, sin modelo.

## 4. El corazón — formato estricto del kickoff de organic

Campos del gate. Los que **bloquean** (Qué, Done, Decisiones) deben ser **concretamente llenables**;
si alguno sale "no sé", el gate frena y **diagnostica** (loop, roadmap o afinar objetivo), nombrando
el campo que falló.

| Campo | Rol / qué exige | Si sale "no sé" → |
|---|---|---|
| **Qué** | Objetivo = comportamiento/resultado observable concreto. No vale "mejorar X" sin target. | loop / afiná el objetivo |
| **Why** (1 línea) | Motivación. **NO bloquea**; se pide siempre y **fluye** a feature-doc + cuerpo del PR. | — |
| **Done** | Definición testeable = el **WHEN**: "cuando X, pasa Y" o el check que lo prueba. | loop (si no sabés cómo se prueba, no lo entendés) |
| **Decisiones ya tomadas** | El approach/arquitectura está **decidido** (o es obvio). **Discriminador de loop.** | **loop** (fork de arquitectura sin resolver) |
| **Riesgo** (opcional) | Qué puede romper / blast radius, una línea. | — |

**"Dónde" NO es campo del gate** (corrección de diseño): los archivos son un **output de la fase Explore**
de `organic-start`, no una precondición. En ODD explorás primero — no podés saber los archivos antes de
mirar el código. El humano puede dejar un *hint* si lo tiene, pero nunca bloquea.

**Regla del gate:** **Qué + Done + Decisiones** concretos → se crea el kickoff de organic. Alguno falla →
no se crea; se reporta cuál faltó y se rutea.

**Ruteo por resultado del gate:**
- *Decisiones* falla → **loop** (arquitectura sin resolver).
- *Qué/Done* claros pero scope enorme/disperso (varios loops) → **roadmap**.
- *Dónde* desconocido pero lo demás claro → **organic normal** (explorás y listo).

**Proporcionalidad (no negociable):** cambio chico = una línea por campo (10 segundos). **El gate rechaza
lo *sub-especificado*, no lo *corto*.** Si un fix de 5 líneas necesita un kickoff pesado, reinventamos SDD
y matamos la razón de existir de organic.

## 5. Simetría kickoff + start, y desacople del motor

Hoy `mala-pata-organic` inicia "de una". Se parte en dos, igual que loop:

```
organic:  prompt → [gate formato] → kickoff → organic-start → motor ODD (gentle-ai)
loop:     prompt → [gate + diseño] → kickoff → loop-start   → motor SDD (gentle-ai)
```

Consecuencia clave: **el kickoff pasa a ser el artefacto universal de mala-pata**, y el "motor"
detrás de cada `start` queda **enchufable**. Si gentle-ai borra SDD, la estructura kickoff+start
sobrevive intacta; solo se cambia el motor. **El desacople sale como consecuencia natural, no como
trabajo extra.**

**Fricción a cuidar:** dos pasos (kickoff → start) por TODO puede molestar en cambios chicos.
Regla: organic chico puede correr kickoff+start de una; el split explícito se usa cuando querés
revisar el kickoff o pasárselo a otra sesión (igual que loop).

## 6. Identidad de mala-pata

mala-pata deja de ser "la herramienta de SDD" y pasa a ser **la capa que (a) decide la ruta y
(b) orquesta los motores/herramientas que existan**. Así, el borrado de SDD por gentle-ai no la
toca: apunta a otro motor. Es la estrategia de desacople vista desde la identidad del producto.

## 7. `laya` — parkeado (no es cimiento)

[laya](https://github.com/NandhaKishorM/laya): motor de decisión System 1 — clasificación tipada
(choice/score/yes-no) en un forward pass (~33ms), calibrado, 100+ idiomas. Librería Python
(PyTorch/BERT). **Es una primitiva de decisión, no un orquestador.**

Decisión: **NO adoptarlo ahora.**
1. El **formato estricto ya hace el routing determinísticamente** (por estructura, sin modelo).
2. Es **infra pesada** (Python, PyTorch, modelos, serve) para una suite con humano en el loop,
   donde cada decisión pasa una vez y el humano confirma. Sus ventajas rinden a escala de miles
   de clasificaciones, no en este flujo.

Nicho futuro (opcional): darle un **score calibrado de readiness** al prompt de organic (0–1)
en vez de un sí/no. Upgrade, no base.

## 8. Riesgos

- **Matar el carril rápido de organic** con ceremonia → mitigado por proporcionalidad (§4).
- **Fricción de dos pasos** en cambios chicos → mitigado por kickoff+start en una para lo chico (§5).
- **Nota importante:** `mala-pata-organic` usa ODD (workers direct/delegated), **NO despacha agentes
  `sdd-*`**, así que el hook `PreToolUse:Agent` de preflight de gentle-ai **no afecta a organic** —
  ese gate es solo del carril loop.

## 9. Plan por fases

- [x] **Fase 1 — Design doc** (este archivo). Versionable en el repo.
- [x] **Fase 2 — Formato estricto + kickoff en `mala-pata-organic`** (v3.0.0): gate del formato,
  genera kickoff en carpeta hermana + puntero engram, auto-diagnóstico organic/loop/roadmap, NO ejecuta.
- [x] **Fase 3 — `mala-pata-organic-start`** (v1.0.0, skill nuevo): lee el kickoff y corre el ciclo ODD
  por fases (worktree → explorar → clasificar → feature-doc → task-by-task + RDD → cerrar → tabla).
  Symlinkeado en `~/.claude/skills` y `~/.codex/skills`.
- [x] **Fase 4 — Alinear `mala-pata-loop`**: brújula de frontera al inicio — loop solo si `Decisiones`
  sin resolver; el tamaño nunca manda a loop; grande-especificable → organic; multi-loop → roadmap.
- [x] **Fase 5 — sync + push** (skills + este doc).

## 10. Estado de decisiones

| Decisión | Estado |
|---|---|
| Frontera = certeza de forma, no tamaño | ✅ acordado |
| Formato estricto = router (fill→organic, no→loop) | ✅ acordado |
| organic gana kickoff + `organic-start` (simetría con loop) | ✅ acordado |
| kickoff = artefacto universal, motor enchufable | ✅ acordado |
| mala-pata = capa de decisión + orquestador | ✅ acordado |
| laya parkeado | ✅ acordado |
| Contrato/endpoint NO es criterio de loop | ✅ acordado (corrección del usuario) |
| Front door `mala-pata-triage` decide el carril; organic solo genera | ✅ acordado + implementado |

## 11. Adición — front door `mala-pata-triage`

El router quedó fuera de `mala-pata-organic` (antes v3.0.0 hacía de gate + ruteo). Se creó un skill fino
**`mala-pata-triage`** (v1.0.0) como **puerta única de entrada**:

- Trigger: cualquier pedido de cambio, ANTES de tocar código. Es la entrada recomendada cuando no sabés
  por dónde va (los 3 carriles siguen invocables directo si ya lo sabés).
- Lee el pedido, aplica el gate de forma (Qué + Done + Decisiones), y **RESPONDE** el carril:
  `→ /mala-pata-organic` (con borrador de campos), `→ /mala-pata-loop`, `→ /mala-pata-roadmap`, o
  `trabajo vago 🛠️` si ni una pregunta alcanza.
- **NO genera archivos, NO crea worktrees, NO ejecuta.** Es un skill de decisión pura; no despacha
  `sdd-*`, así que el preflight hook no aplica.
- `mala-pata-organic` bajó a **v3.1.0**: asume `route=organic`, la tabla de campos pasa a ser
  *insumo del kickoff* (no el ruteo), y la vieja Regla #1 quedó como **red de seguridad** (si al capturar
  aparece que `Decisiones` no estaba resuelto, rebota a loop).

Flujo final: `pedido → /mala-pata-triage → (organic-start | loop | roadmap)`.
