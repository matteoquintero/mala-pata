---
name: mala-pata-loop-orchestrate
description: Planificador READ-ONLY de un lote de kickoffs SDD — analiza varios kickoffs y devuelve un plan de arranque (olas, paralelismo, conflictos de archivo/migración, splits recomendados, diferidos) + comandos copy-paste. NO crea worktrees, NO adelanta branches, NO lanza sesiones — eso lo hace /mala-pata-loop-orchestrate-start.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "2.0.0"
---

# /mala-pata-loop-orchestrate — Planificar un LOTE de kickoffs (READ-ONLY)

Sos el **planificador** del lote. Te pasan **varios kickoffs** y devolvés un **plan de arranque**: en
qué **olas** correrlos, qué **paralelizar** y qué **NO**, dónde hay **conflicto de archivo/migración**,
qué kickoff **conviene partir en dos**, cuáles **diferir** por bajo valor, y los comandos listos para
pegar.

> **Este skill NO ejecuta nada**: no crea worktrees, no adelanta branches, no escribe launch configs,
> no abre sesiones. Es SOLO análisis + plan. Para **lanzar** el lote usá `/mala-pata-loop-orchestrate-start`
> (separación de responsabilidades, igual que `loop` vs `loop-start`).

NO corrés los ciclos SDD acá (eso lo hace `/mala-pata-loop-start` por kickoff). Este comando
**planifica el lote**; el lanzamiento vive en el skill hermano.

## Paso 1 — Cargar los kickoffs
Input (acepta cualquiera de estas formas):
- **Lista explícita de rutas** (formato actual): rutas absolutas a los `.md` de kickoff que dejó `/mala-pata-loop` en `<carpeta-proyecto>-mala-pata/`.
- **Auto-descubrir**: si no se pasa lista, listá `<carpeta-proyecto>-mala-pata/*.md` (o por un prefijo/módulo si lo indican, ej. "todos los de sentencias").
- **Legacy** (kickoffs viejos, solo compatibilidad): ids de engram (`#6717 #6712 …`) o topic_keys (`sdd/<name>/kickoff`).

Para cada uno: si es ruta → `Read` directo. Si es legacy → `mem_search` → `mem_get_observation`; si lo que devuelve es el puntero liviano (`Kickoff en archivo: <ruta>`) en vez del contenido completo, seguí esa ruta y leé el archivo.
Si alguno no se encuentra → avisá y seguí con el resto (no inventes contexto).

## Paso 2 — Extraer los metadatos que gobiernan la orquestación
De cada kickoff sacá:
- `change-name`, `size`, `depends_on` (duro/blando).
- **Áreas/archivos afectados** (sección "Referencias"/"Áreas afectadas") → clave para detectar choques.
- **¿Migración?** (seed/DDL sí/no).
- **Severidad/valor** (alta / baja / "evaluar si amerita").
- **branch base** declarada en el kickoff.
- **Fases**: casi todos son SDD (`explore→propose→spec→design→tasks→apply→verify→archive`).
  Las **únicas fases NO-SDD** son la **cola final** de `/mala-pata-loop-start` (Paso 4): **PR →
  revisión de pipeline/CI → cleanup**. Usá esta conciencia de fases para ubicar la frontera
  paralelo/serie (ver Paso 3).

## Paso 3 — Analizar (reglas del plan)
1. **Grafo de dependencias** (`depends_on`) → orden topológico. Una dependencia dura = el
   dependiente no entra a **Apply** hasta que el proveedor cierre **design** (la convención/contrato).
2. **Conflicto por archivo compartido**: intersectá las áreas afectadas. Dos kickoffs que editan
   el MISMO archivo **no pueden hacer Apply en paralelo** (conflicto de merge) → serializá su Apply
   o escaloná. La **planeación** (explore→design) SÍ puede ir en paralelo (no escribe código).
3. **Colisión de migraciones**: si ≥2 seedean migración y van en paralelo → el número es **provisional,
   no una reserva**: el primero que mergea se lo queda y los demás renumeran al integrar (ver
   `/mala-pata-loop-start`, Paso 4.1-bis). La verdad de los números tomados es **git** (medí las ramas),
   NO un registry en engram; los kickoffs traen su número provisional en el frontmatter
   `migrations_reserved`. Nunca confiar en el número de archivo ni en un registry.
4. **Triage por valor**: los marcados "evaluar si amerita"/baja severidad → **diferilos** fuera del
   primer lote (o cerralos en propose sin código). No los metas en la ola 1.
5. **Split (SOLO recomendar)**: si un kickoff mezcla 2 concerns independientes o es size L con dos
   entregables separables → **recomendá** partirlo en A/B con el motivo. NO crees los kickoffs
   partidos (eso lo decide el usuario).
6. **Cola final compartida**: si varios cambios van al mismo destino, decidí si conviene **un PR
   consolidado** o **PRs separados**; recordá que la cola final (PR/CI/clean) de cada ciclo NO se
   paraleliza a ciegas (no mergear con CI en rojo; un solo PR activo por trabajo).
7. **Frescura de la branch base (solo DETECTAR y AVISAR — no arreglar acá)**: por cada branch base
   distinta del lote, `git fetch origin <base>` y comparar `git rev-parse <base>` vs
   `origin/<base>`. Si el local está ATRÁS, marcalo en el plan: "`<base>` local atrás de origin —
   `/mala-pata-loop-orchestrate-start` va a adelantar los worktrees antes de lanzar". El arreglo real
   (ff/rebase de los worktrees) lo hace el skill de start; acá solo se reporta para que el usuario lo
   sepa antes de lanzar.

## Paso 4 — Salida: PLAN en tabla de olas + comandos + handoff a start
Devolvé SIEMPRE:
1. **Tabla de olas**: `Ola | kickoff (#id) | fase de arranque | paraleliza con | frontera (hasta qué
   fase en paralelo) | conflicto/nota`.
2. **Comandos copy-paste** por ola, para correr cada ciclo a mano si el usuario NO quiere lanzar en Warp:
   ```
   /mala-pata-loop-start sdd/<change-name>/kickoff
   ```
   (Todos entran por **Explore**; aclaralo. La diferencia es la ola y hasta qué fase puede avanzar
   en paralelo.)
3. **Handoff a start**: la línea para lanzar el lote (o una ola) en Warp con el skill hermano:
   ```
   /mala-pata-loop-orchestrate-start <kickoffs-de-la-ola-a-lanzar>
   ```
   Aclarale al usuario: `orchestrate` solo planifica; para crear worktrees + abrir sesiones use
   `orchestrate-start`.
4. **Advertencias**: choques de archivo, colisión de migración, dependencias, splits recomendados,
   diferidos, coordinación de la cola final, y **frescura de base** (Paso 3.7).

## Reglas duras
- **NO** ejecutes nada mutante: sin worktrees, sin ff/rebase, sin launch config, sin abrir sesiones.
  Si el usuario pide "lanzá / orquestá de verdad", derivá a `/mala-pata-loop-orchestrate-start`.
- **NO** crees los kickoffs de un split (solo recomendás).
- El `git fetch`/comparación del Paso 3.7 es lo ÚNICO que toca red/git, y es READ-ONLY (fetch + rev-parse).
- Rutas ABSOLUTAS en los comandos; relativas solo al hablarle al usuario.

## Compatibilidad de runtime
El análisis, las olas y los comandos son portables a cualquier CLII. El handoff a Warp/Claude solo
aplica cuando el runtime es Claude con Warp; en otro CLI, devolvé el plan y los comandos y omití el
handoff de `orchestrate-start`.
