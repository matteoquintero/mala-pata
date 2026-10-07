---
name: mala-pata-seed
description: Sembrador determinista de fixtures para probar en una rama, FUERA de shot/organic/loop. Lee el apartado `## Seed` del QA que generó mala-pata-walkthrough (qué fixtures, derivados de los Given + el smoke_test.data del kickoff) y los siembra con el mecanismo del proyecto (seeders/factories que detectó sdd-init), idempotente, contra la test DB. NO improvisa — si falta la receta o el mecanismo, PARA y avisa. NO toca prod, NO escribe código de app, NO corre tests. Es también el ejecutor que el gate de smoke test (4.1-ter) delega in-cycle. Trigger — "sembrá los fixtures", "seed para probar <feature>", o correrlo sobre una rama antes de probar a mano.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.0.0"
---

# /mala-pata-seed — sembrador determinista de fixtures (lee walkthrough)

Entrada: **la del CLI** — un feature/change/rama, o la ruta del QA de walkthrough que trae el apartado `## Seed`.

Tu trabajo: **ejecutar el sembrado** de los fixtures que una prueba necesita, leyendo la receta que dejó `mala-pata-walkthrough` — sin inventar. Sos el complemento ejecutor de walkthrough (que describe, read-only): walkthrough dice QUÉ fixtures; vos los SEMBRÁS. Servís para probar en una rama **cuando NO estás en un ciclo** (shot/organic/loop); dentro de un ciclo, el gate de smoke test (`mala-pata-loop-start` 4.1-ter / `mala-pata-organic-start` Paso 7) te delega esto mismo.

> **Determinista, no creativo.** Sembrás EXACTAMENTE lo que dice el apartado `## Seed` de walkthrough, con el mecanismo del proyecto. Si la receta falta, está incompleta, o el mecanismo de seed no existe → **PARÁ y avisá**, nunca adivines qué datos crear.

## Requisitos (orquestar, no reinventar)

mala-pata orquesta herramientas de comunidad — no las reimplementa. Chequeá al arrancar:

- **Obligatorias** (sin fallback — si falta, PARÁ y pedí instalarla):
  - `git` — para saber en qué rama/repo estás. Siempre presente.
- **Recomendadas** (con fallback — si falta, avisá en una línea y seguí degradado):
  - `serena` / `codegraph` — ubicar el mecanismo de seed del proyecto (factories/seeders) a nivel símbolo. Fallback: grep/Read.
  - `engram` — leer el puntero del QA de walkthrough (`sdd/<change>/walkthrough`) y `sdd-init/<project>`. Fallback: pedí la ruta del QA a mano.

Chequeo: `command -v <tool>` (CLI) o `claude mcp list` (MCP, p.ej. serena). Si falta una obligatoria, no sigas.

## Regla dura — la test DB, NUNCA prod

Sembrás SOLO contra la **test DB** del proyecto (`TEST_DB_URL` o el equivalente que diga `sdd-init`). Antes de sembrar, confirmá que el target es la test DB; si no lo podés confirmar, **PARÁ**. Prohibido sembrar contra prod o contra una DB sin confirmar. Rutas absolutas siempre.

## Flujo

1. **Encontrá la receta.** Localizá el apartado `## Seed (fixtures)` del QA de `mala-pata-walkthrough` para este feature (ruta directa, o por el puntero engram `sdd/<change>/walkthrough`). Si no existe el QA o no tiene `## Seed` → **PARÁ** y pedí que se corra `mala-pata-walkthrough` primero (es quien arma la receta). No inventes fixtures.
2. **Resolvé el mecanismo del proyecto.** `mem_search("sdd-init/<project>")` → con qué siembra el proyecto (seeders/factories/comando). Si `sdd-init` no está o no define mecanismo de seed → **PARÁ** y avisá; no armes INSERTs ad-hoc.
3. **Confirmá la test DB** (regla dura de arriba).
4. **Sembrá, idempotente.** Ejecutá el mecanismo del proyecto con los datos de la receta. Idempotente: upsert / claves estables / namespaced por change, para que re-correr no choque por constraints ni duplique filas.
5. **Reportá qué sembraste.** Lista concreta: ids / registros / claves que quedaron listos, para que el humano (o el gate) vaya directo a probar con la **tabla** de walkthrough (`# | Given | When | Then`) y su bloque de acceso.

## Teardown (opcional, se pregunta — default NO)

Al terminar, una línea: **"¿Borro lo que sembré? (default: no)"**. Default no borrar — la test DB persistente con datos es útil. Si piden borrar, borrá **solo lo que esta corrida sembró** (por ids/namespace), NUNCA un wipe de la DB.

## Qué NO hace

- NO inventa fixtures — solo siembra lo que dice la receta `## Seed` de walkthrough.
- NO toca prod ni una DB sin confirmar que es la de test.
- NO escribe código de aplicación, NO corre el ciclo SDD, NO despacha agentes `sdd-*`.
- NO genera el guion de prueba (eso es `mala-pata-walkthrough`) — solo siembra.
