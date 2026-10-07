---
name: mala-pata-walkthrough
description: A partir de un PR/change O un roadmap (un PR = "un roadmap de un solo nodo"), genera un recorrido de prueba de la funcionalidad en Given/When/Then + pasos seguibles, y lo proyecta en DOS carriles SIN mezclarlos (Diátaxis) — (1) guía QA/UAT interna "qué probar / cómo probar" y (2) documentación how-to/tutorial para el cliente final. Living documentation (BDD): el mismo Given/When/Then verifica Y documenta. NO escribe código, NO corre el ciclo SDD, NO reemplaza a sdd-verify (que es verificación de máquina). Trigger: "documentá cómo probar esto", "guía de prueba", "tutorial de la funcionalidad", "doc de funcionamiento para el cliente", a partir de un PR, un change-name o un roadmap.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.1.0"
---

# /mala-pata-walkthrough — recorrido de prueba + base de doc de cliente

Entrada del usuario: **entregada por el CLI** (un PR/change, o la ruta de un roadmap).

Tu trabajo: convertir una funcionalidad ya definida o ya entregada en un **recorrido que un humano puede seguir a mano** para probarla, escrito de forma que **se reuse como documentación de funcionamiento para el cliente final**. NO escribís código, NO corrés el ciclo SDD, NO reemplazás a `sdd-verify`.

## Requisitos (orquestar, no reinventar)

mala-pata orquesta herramientas de comunidad — no las reimplementa. Chequeá al arrancar:

- **Obligatorias**: ninguna.
- **Recomendadas** (con fallback — si falta, avisá en una línea y seguí degradado):
  - `gh` — lectura de PRs. Fallback: pasar el PR/diff a mano. Instalar: `brew install gh`.

Chequeo: `command -v <tool>` (CLI) o `claude mcp list` (MCP, p.ej. serena). Si falta una obligatoria, no sigas.

## Principios (probados, no inventados)

- **Diátaxis** (framework de doc de Canonical/Ubuntu): tutorial (aprender) ≠ how-to (resolver una tarea) ≠ reference ≠ explanation. El guion de QA y la doc de cliente **comparten los pasos pero difieren en audiencia y propósito** → NO se mezclan en un solo doc; salen **dos renders del mismo core**.
- **BDD / living documentation**: el mismo **Given/When/Then** verifica Y documenta. Es el puente entre "prueba" y "doc". El DoD de los kickoffs de esta familia YA está en Given/When/Then — es materia prima directa.
- **Frontera con verify (no duplicar)**: `sdd-verify` es verificación **técnica/de máquina** contra el DoD (build, tests, checklist). Esto es un **recorrido humano** + la base de doc para el cliente. Propósitos distintos.

## Modelo unificado de entrada — todo es 1..N "unidades shippables"

Dos entradas, **PARES** (ninguna es secundaria):

- **PR / change** → **1 unidad** (un PR es "un roadmap de un solo nodo").
- **Roadmap** → **N unidades** (una por fase shippable).

**Normalizá SIEMPRE la entrada a una lista ordenada de unidades.** De ahí en adelante el flujo por unidad es idéntico, venga de un PR o de una fase de roadmap.

## Paso 0 — Gate de entrada

Detectá el tipo de entrada y armá la lista de unidades:
- **Ruta a un `.md` de roadmap** → cada fase = una unidad (leé su IN/OUT, DoD y bordes).
- **PR# / branch / change-name** → una unidad (vas a traer el diff + los artefactos SDD).

Si no podés identificar la funcionalidad ni de dónde sacarla → **PARÁ** y pedí el insumo concreto (PR#, change-name o ruta del roadmap). No inventes funcionalidad.

## Paso 1 — Reunir fuentes por unidad (read-only)

Por cada unidad, juntá lo que YA existe (no re-derives desde cero):
- **SDD en engram**: `sdd/<change>/spec` (escenarios Given/When/Then), `design`, `tasks`, y el **DoD del kickoff** (ya en Given/When/Then).
- **El cambio real**: el diff (`gh pr diff <n>` / `git -C <repo> diff <base>...<branch>`), y los **endpoints / pantallas / comandos** que se tocaron.
- **Roadmap**: IN/OUT y criterios de éxito de cada fase.
- Quedate SOLO con el **comportamiento observable por el usuario**, no el interno. Si algo únicamente se ve leyendo código, no es material de walkthrough.

## Paso 2 — Extraer el "scenario core" (única fuente de verdad)

Por cada comportamiento observable, un escenario en este formato — es el **core** del que salen los dos carriles:

```
### <comportamiento en lenguaje de usuario>
- **Contexto (Given)**: <estado inicial concreto>
- **Acción (When)**:
  1. <paso concreto y seguible — clic / comando / input EXACTO>
  2. ...
- **Resultado esperado (Then)**: <observable, verificable a ojo>
- **Datos de prueba**: <inputs concretos, no "un valor cualquiera">
- **Casos borde**: <variaciones que también hay que mirar>
```

Regla dura: **si un paso no lo puede seguir alguien que no escribió el código, está mal escrito.** Cero jerga interna en el core.

## Paso 3 — Carril QA/UAT (uso interno: "qué probar / cómo probar")

**Bloque de acceso (OBLIGATORIO, va primero — sin esto no se entrega el carril).** Para que el humano pruebe sin romper nada, el guion SIEMPRE arranca con cómo acceder:
- **URL**: la del entorno de PRUEBA (localhost:<puerto> o la test env). **NUNCA producción.**
- **Credenciales de prueba**: el usuario/login de prueba a usar (indicá de dónde salen; NO pegues secretos reales — el QA vive fuera del repo, Paso 6).
- **Servidor corriendo**: cómo levantar la app contra la **test DB** y confirmar que está arriba antes de empezar.

**Tabla de prueba (OBLIGATORIA, formato fijo).** Del core, UNA fila por escenario — este es el formato exacto, no lo cambies:

| # | Given (ruta) | When | Then (lo que tenés que ver) |
|---|--------------|------|-----------------------------|
| 1 | <estado inicial concreto + dónde/ruta> | <acción exacta> | <resultado observable a ojo> |

Debajo de la tabla, por escenario:
- **casilla pass/fail**.
- **Señal de que falló**: qué se ve si NO anduvo (no solo el happy path).
- **Datos de prueba y casos borde** explícitos.
- **Nota de regresión**: qué NO debería haber cambiado y hay que confirmar de paso.

Este carril es un **checklist accionable**, no prosa. El **bloque de acceso** y la **tabla** son obligatorios SIEMPRE.

## Paso 3.5 — Apartado `## Seed` (receta de fixtures, para `mala-pata-seed`)

walkthrough NO siembra (sigue read-only) — deja la **receta** para que la ejecuten `mala-pata-seed` (standalone, en una rama) o el gate de smoke test (in-cycle, 4.1-ter / Paso 7). Si el change toca datos, agregá al QA un apartado `## Seed (fixtures)`:
- **Qué fixtures** — el estado inicial mínimo para correr la tabla, **derivado de los `Given` + `Datos de prueba` del core** (+ el `smoke_test.data` del kickoff si existe). NO inventes datos: si un `Given` no alcanza para fijar un valor, marcalo "a confirmar".
- **Mecanismo** — con qué sembrar (seeders/factories del proyecto que detectó `sdd-init`). Nombralo, no lo reimplementes.
- **Dónde** — la **test DB** (nunca prod).
- **Idempotente** — claves estables para que re-sembrar no choque.

Este apartado es el contrato que `mala-pata-seed` lee. Si el change NO toca datos (ej. visual puro), omitilo y decilo explícito.

## Paso 4 — Carril cliente final (how-to / tutorial)

Del **MISMO** core, reescribí para el usuario final:
- **Sin jerga, sin pass/fail, sin datos de test internos.**
- Orientado a **resultado y "para qué / cuándo usarlo"**, no a "verificar".
- Título en forma de tarea ("Cómo <hacer X>") o de tutorial guiado, según lo que pida Diátaxis.
- **Placeholders de screenshot** por paso visual (`![descripción](placeholder)`); capturarlos es opcional (Paso 5).
- Apoyate en la skill **`cognitive-doc-design`** para la calidad de redacción (cargala liviana, no la ejecutes como fase).

Este carril **NUNCA** menciona tests, ramas, migraciones ni nada interno.

## Paso 5 — Screenshots (opcional, si la app se puede correr)

Si el stack permite levantar la app **y el humano lo OK**: capturá los pasos visuales con la herramienta del proyecto (Playwright si está disponible) y reemplazá los placeholders. Si no se puede o no se quiere, dejá los placeholders marcados para que el humano los complete. **No es obligatorio** para cerrar.

## Paso 6 — Ubicación y persistencia (aconsejar + confirmar)

Diátaxis manda **NO mezclar** → **dos archivos**, no uno:
- **Cliente final** (versionable, va al repo): aconsejá `docs/guias/<slug>.md` (o la convención de docs que use el proyecto). Confirmá la carpeta con el humano.
- **QA/UAT** (interno): aconsejá el sibling `<carpeta-del-proyecto>-mala-pata/walkthroughs/<slug>-qa.md` (fuera del repo, como los kickoffs), o `docs/qa/` si el proyecto versiona QA. Confirmá.
- **Puntero liviano en engram**: `mem_save` topic_key `sdd/<change>/walkthrough`, contenido de una línea con las rutas de los dos archivos (para que el radar y futuras sesiones lo encuentren). Si la entrada fue un roadmap sin change-name único, usá el slug del roadmap.

## Paso 7 — Gate humano

Presentá los dos carriles (resumen corto + rutas de archivo) y **esperá OK o ajustes** antes de dar por cerrado. Como todo en la familia: no marques "listo" con algo sin revisar.

## Relación con la familia

- **Consume** un roadmap de `/mala-pata-roadmap`, o un change/PR cerrado por `/mala-pata-loop-start` o `/mala-pata-organic`.
- **Momento típico**: después de `verify` (funcionalidad real → doc más rica), o sobre un roadmap **hacia adelante** (genera un esqueleto provisional que se rellena cuando cada fase se implementa).
- **No** orquesta, **no** ejecuta fases, **no** muta código.

## Qué NO hace (invariantes)

- NO escribe código ni corre el ciclo SDD.
- NO reemplaza `sdd-verify` (verificación de máquina contra el DoD).
- NO mezcla el carril QA con el de cliente (Diátaxis: dos renders, dos archivos).
- NO inventa comportamiento que no esté en el PR / roadmap / artefactos SDD.
