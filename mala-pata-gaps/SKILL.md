---
name: mala-pata-gaps
description: Auditor READ-ONLY de completitud de un DOMINIO — dado uno o varios roadmaps del mismo dominio + el CÓDIGO real, encuentra qué falta para cubrir el objetivo total (follow-ups). Aunque todas las fases estén terminadas, puede faltar algo. Cruza 3 fuentes — el objetivo total (roadmaps), los follow-ups ya ANOTADOS (Nivel-2 / diferidas / propuestas-extra no hechas / TODO-FIXME en código) y los gaps INFERIDOS del código (codegraph/serena, anclados a evidencia). Cada gap sale tag [anotado] o [inferido] con evidencia (file:line o la anotación). NO mira solo el .md — analiza el código. NO ejecuta fases ni toca código — deja su reporte en mala-pata/gaps/<dominio>.md (versionado) + puntero engram, y sugiere rutear. Distinto de mala-pata-roadmap-radar (ese es status de fases vs git; este es completitud del objetivo). Trigger — "tenemos follow ups", "gaps de <dominio>", "qué falta del dominio <X>", "qué falta para cubrir <objetivo>".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.1.0"
---

# /mala-pata-gaps — qué falta para cubrir el objetivo de un dominio (contra el código)

Entrada: **la del CLI** — un **dominio** (keyword, ej. `facturacion`) o una **lista de slugs de roadmap** del mismo dominio.

Tu trabajo: decir **qué falta para cubrir el objetivo TOTAL** de un dominio — los follow-ups. No es el status de las fases (eso es `mala-pata-roadmap-radar`); es la **completitud**: aunque todas las fases estén en "terminado", ¿queda algo sin cubrir del objetivo? Lo respondés cruzando los roadmaps del dominio con el **código real**.

> **No es `mala-pata-roadmap-radar`.** radar te dice dónde están las fases declaradas (git). Este te dice **qué NO está declarado/hecho y hace falta** para el objetivo del dominio. Se complementan.

## Requisitos (orquestar, no reinventar)

mala-pata orquesta herramientas de comunidad — no las reimplementa. Chequeá al arrancar:

- **Obligatorias** (sin fallback — si falta, PARÁ):
  - `git` — ubicar el repo y el estado real. Siempre presente.
- **Recomendadas** (con fallback — si falta, avisá en una línea y seguí degradado):
  - `codegraph` / `serena` — medir el estado real del código (qué del objetivo ya existe, qué no) a nivel símbolo. Fallback: grep/Read (más grueso, decilo).
  - `engram` — puntero a los roadmaps del dominio. Fallback: listar `mala-pata/roadmap/*.md`.

Chequeo: `command -v <tool>` (CLI) o `claude mcp list` (MCP, p.ej. serena). Si falta una obligatoria, no sigas.

## Principios duros

- **Anclado a evidencia, NUNCA inventado.** Cada gap sale de una anotación real o de una lectura del código con `file:line`. Si no lo podés anclar, no es un gap — es una pregunta, marcala aparte.
- **`[anotado]` vs `[inferido]`** por cada gap: anotado = ya estaba escrito (Nivel-2, diferida, TODO); inferido = lo detectó el modelo cruzando objetivo + código. El humano confía distinto en cada uno — como el `[regla/juicio]` de los otros skills.
- **Read-only sobre el código/proyecto.** NO ejecuta fases, NO toca código, NO crea kickoff/roadmap. Pero SÍ deja su **propio reporte** en `mala-pata/gaps/<dominio>.md` + puntero engram (como research/roadmap) — para trazabilidad. Sugiere rutear y termina.
- **Sobre-descubrir, el humano recorta.** Mejor proponer un gap de más (marcado `[inferido]`) que callarlo. Pero nunca inventado.

## Fase 0 — Resolver el dominio y sus roadmaps

1. Project root: `git -C <cwd> rev-parse --show-toplevel`.
2. Resolvé los roadmaps del dominio:
   - Si la entrada es una **lista de slugs** → esos `.md` en `mala-pata/roadmap/`.
   - Si es un **dominio/keyword** → listá `mala-pata/roadmap/*.md` y quedate con los que pertenecen a ese dominio (por slug/objetivo). Si hay ambigüedad sobre cuáles entran, listalos y pedí confirmación (una pregunta).
3. Si no hay roadmaps que matcheen → decilo y PARÁ; no inventes el objetivo.

## Fase 1 — Objetivo TOTAL del dominio

Uní el **estado deseado** de todos los roadmaps del dominio: sus "## Objetivo grande" + los ejes de la **tabla de cobertura** (estado deseado MECE). Ese conjunto de ejes es el **contrato de completitud** contra el que vas a medir. Si dos roadmaps solapan un eje, es uno solo (MECE).

## Fase 2 — Las 3 fuentes de gaps

**(a) Follow-ups ya ANOTADOS** (recogelos, no los inventes):
- Checklist **Nivel 2** de cada roadmap (dominio amplio no cubierto).
- Ejes marcados **diferida** o **propuesta-extra** que NO se hicieron.
- `TODO` / `FIXME` / notas en el **código** del dominio (grep/codegraph).

**(b) Estado actual del CÓDIGO** (medí, no asumas): por cada eje del objetivo (Fase 1), qué ya está implementado y qué no — con `codegraph_explore` / serena / grep. Anclá a `file:line`.

**(c) Gaps INFERIDOS**: donde el objetivo implica algo que el código NO hace. Ej.: "el objetivo dice que TODO tipo de error de factura debe ser accionable, pero en código estos 2 tipos no tienen handler de acción (`file:line`)". Razonado desde objetivo + código, nunca de la nada.

## Fase 3 — Gap analysis (estado deseado vs estado actual)

Mismo marco que el Gap Analysis de `/mala-pata-roadmap` (Paso 4-ter), pero **post-hoc y contra el código vivo**: **estado deseado** (objetivo total, Fase 1) **menos** **estado actual** (código, Fase 2b) = **los gaps**. Sumá los anotados (2a) y los inferidos (2c). Deduplicá.

## Fase 4 — Salida (formato fijo, read-only)

```
Gaps del dominio: <dominio>  ·  roadmaps: <slug, slug, …>  ·  repo: <nombre>  ·  <fecha-hora>
Fuente: roadmaps mala-pata/ + código en vivo

| # | Falta (qué) | Eje del objetivo | Evidencia | Tag |
|---|-------------|------------------|-----------|-----|
| 1 | <qué falta, concreto> | <eje> | <file:line o anotación/roadmap> | [anotado] / [inferido] |

Preguntas (no son gaps, faltó evidencia para confirmarlas): <o "ninguna">
Sugerencia de ruteo (NO ejecuto): <gap> → /mala-pata-research o /mala-pata-triage
```

- **Una fila por gap**, concreto, con evidencia real. Sin evidencia → no va a la tabla (va a "Preguntas").
- **Tag obligatorio** `[anotado]` o `[inferido]` por fila.
- Si no hay gaps: decilo explícito + **qué ejes verificaste** y por qué están cubiertos (igual que el empty-audit de preview — no un "todo bien" a secas).

## Fase 5 — Persistir el reporte (trazabilidad)

Escribí el reporte de la Fase 4 en **`mala-pata/gaps/<dominio>.md`** (dentro del repo, versionado; `mkdir -p` si no existe; `<dominio>` = el keyword, o un slug compuesto de los roadmaps analizados). Si ya existe, **actualizá** ese archivo — el gaps es un **backlog vivo** del dominio, no un append infinito ni un archivo nuevo por corrida. Puntero liviano en engram: `mem_save` topic_key `gaps/<dominio>`, contenido de una línea `Gaps en archivo: <ruta absoluta>` (no dupliques el contenido — el archivo es la fuente). Si engram no está, el archivo es la fuente; avisá en una línea.

Después de persistir, cerrás: sugerís rutear, **no ejecutás fases ni tocás código**.

## Reglas

- **Read-only sobre el código/proyecto.** No ejecuta fases, no toca código, no crea kickoff/roadmap. SÍ escribe su propio reporte en `mala-pata/gaps/<dominio>.md` + puntero engram (su artefacto, como research/roadmap).
- **Nunca inventar.** Todo gap anclado a anotación o `file:line`. Lo no anclable va como "Pregunta", no como gap.
- **No pisa a `mala-pata-roadmap-radar`** (status de fases) — este es completitud del objetivo.
- **Formato fijo** siempre.
- **Sin datos**: si no hay roadmaps del dominio o no hay código accesible, pedilo; no adivines el objetivo ni los gaps.

## Qué NO hace

- NO ejecuta ni ofrece ejecutar una fase/carril.
- NO crea kickoff, roadmap, research ni código.
- NO inventa gaps — solo anotados o inferidos-con-evidencia.
- NO despacha agentes `sdd-*`.
