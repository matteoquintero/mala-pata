---
name: mala-pata-radar
description: >
  Radar READ-ONLY de SDD — descubre Y diagnostica en una sola corrida (absorbe a
  la ex torre de control). Fase A: descubre los SDD activos en la memoria
  (engram, best-effort ≤20/búsqueda) o toma la lista explícita que le pases.
  Fase B: confirma cada uno contra git EN VIVO (cero cache) — fase del ciclo,
  merge real contra integración, dependencias, branch stale, gate humano,
  parqueado, falta limpieza. Alcance: por default SOLO el proyecto del cwd;
  acepta una ruta de proyecto o `global` (todos los proyectos, agrupado).
  NO orquesta, NO ejecuta fases, NO muta nada.
  Trigger: "radar de SDD", "SDD activos", "torre de control", "cómo van estos
  SDD", "estado de estos SDD", o una lista de change-names para revisar.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "4.0.0"
---

## Propósito

Visibilidad global y **100% confiable** del avance de los SDD, en UNA corrida:
descubre qué hay activo (memoria) y lo confirma contra la realidad (git). Antes
eran dos skills ("radar propone, torre confirma") — ahora es un solo pipeline:
la Fase A propone, la Fase B confirma, y la salida es una sola tabla diagnosticada.

La confianza viene de **no confiar en ningún estado cacheado**: cada corrida
re-deriva todo desde las fuentes vivas (memoria + VCS). Es puramente informativa:
te dice **qué falta y dónde**, y ahí termina — NO ejecuta ni ofrece ejecutar nada
(cada fase se trabaja en su propia sesión).

**Agnóstica**: solo VCS (git) + la memoria persistente disponible. No conoce ni
consulta gestores de tickets ni servicios externos.

## Entrada

Dos dimensiones independientes en la entrada del CLI: **alcance** (qué proyecto/s) y
**lista** (qué SDDs).

**Alcance — de qué proyecto se miran los SDD:**
- **Default (sin parámetro de alcance)**: SOLO el proyecto en el que estás parado
  (el del cwd). Fase A filtra los hits de memoria por el `project` de ese cwd;
  Fase B opera sobre ese repo. NUNCA mezcles SDDs de otros proyectos en el default.
- **`<ruta absoluta>`**: opera sobre ESE proyecto — Fase A filtra los hits por el
  proyecto de esa ruta (los resultados de la memoria traen su `project`; descartá
  los que no coincidan), Fase B corre git en ese repo.
- **`global`**: todos los proyectos — Fase A busca sin filtro de proyecto y agrupa
  la tabla por proyecto; Fase B corre git por cada proyecto cuyo repo sea
  resolvible (del `project_path` que devuelve la memoria, o de la ruta del archivo
  de kickoff). Si un repo no se puede resolver, sus celdas git van con `?` y se
  explica en la evidencia.

**Lista — qué SDDs (opcional, combinable con el alcance):**
- **Lista explícita**: change-names (`sentencias-mora`), identificadores de
  memoria (`#7280`, `sdd/<change>/tasks`), `all <prefijo>-*`, o una mezcla →
  **saltá la Fase A** y andá directo a la Fase B con esa lista.
- **Vacía o solo un prefijo/dominio** → corré la Fase A para armar la lista,
  dentro del alcance elegido.

## Proceso

### Fase A — Descubrir candidatos activos (memoria, solo si no hay lista explícita)

Seguí [references/discovery.md](references/discovery.md) (engram-only, comandos
exactos con `limit=20` y `match_mode="any"`): búsquedas-ancla por fases de
actividad + loop-until-dry; ciclo completo por candidato (**PROHIBIDO**
clasificar con un solo hit); filtrá cancelados y archivados (contalos aparte).
**Respetá el alcance de la Entrada**: salvo `global`, descartá todo hit cuyo
`project` no sea el del proyecto objetivo — los resultados de la memoria traen
su proyecto; un SDD de otro proyecto en la tabla es un error de alcance.
La lista filtrada de activos pasa a la Fase B. **Best-effort declarado**: engram
topa en 20 resultados por búsqueda, no existe inventario 100% — el disclaimer va
SIEMPRE en el banner.

### Fase B — Confirmar y diagnosticar con git (SIEMPRE, cero cache)

Ejecutá en orden, sin saltarte pasos (detalle en
[references/state-derivation.md](references/state-derivation.md)):

1. **Frescura primero.** El/los repo(s) los define el **alcance de la Entrada**
   (default = el del cwd; `<ruta>` = ese; `global` = uno por proyecto resolvible).
   `git fetch --all --prune` en cada uno. Detectá la branch de integración
   (confirmala, no la asumas). Anotá los SHA para el banner.
2. **Resolvé cada SDD contra la memoria por identificador EXACTO** (change-name
   o topic_key), nunca por semántica difusa. Recogé qué artefactos existen y su
   última revisión. (El kickoff es un archivo: la observación de engram es un
   puntero `Kickoff en archivo: <ruta>` — seguilo con `Read`.)
3. **Derivá fase + semáforo EN VIVO** con la máquina de estados de
   `state-derivation.md`. Regla dura: **el merge NUNCA se cree por un
   archive-report o apply-progress** — se confirma contra la branch de
   integración recién traída.
4. **Detectá**: dependencias entre los SDD de la lista, branch stale,
   parqueado/bloqueado, sin instrucción, gate humano pendiente, y falta limpieza
   (mergeado pero worktree/branch vivos — incluidos los `paused-at-preview`, que
   registran la ruta de su worktree vivo en el `state`).

## Salida

Exactamente el formato de [references/table-format.md](references/table-format.md):
banner de frescura (+ el disclaimer best-effort si corrió la Fase A) + tabla de
7 columnas + leyenda del semáforo + bloque de evidencia (por cada SDD, el
identificador de memoria + SHA/branch que respaldan el estado). Mismo formato,
mismo orden, mismo léxico, **siempre** — memoria mecánica para el humano. Si la
Fase A vio archivados/cancelados, cerrá con UNA línea de conteo "otros vistos",
marcada **no exhaustivo**.

## Reglas

- **CERO cache.** Prohibido reportar un estado sin re-derivarlo en esta corrida
  desde memoria + VCS.
- **READ-ONLY.** Nunca commit, push, merge, fetch destructivo, ni escritura en
  memoria. Correr el radar siempre es seguro.
- **NO TOMÁS ATRIBUCIONES.** Solo informás **qué falta y dónde**. NUNCA ejecutás
  ni OFRECÉS ejecutar una fase (apply, verify, archive, PR, merge, limpieza) —
  cada una se trabaja en su **propia sesión aparte**. Tu salida TERMINA en el
  reporte. Prohibido cerrar con "¿arranco X?", "¿lo corro?", "¿mergeo?" o similar.
- **Merge = solo git.** Un archive-report dice "el ciclo cerró", NO "está
  mergeado".
- **No un solo hit**: por cada SDD traé TODO su ciclo; para el universo,
  loop-until-dry con `limit=20`, `match_mode="any"`.
- **Identificador exacto** al agrupar/resolver; nunca frases ni semántica difusa.
- **Best-effort declarado** cuando corre la Fase A: el banner SIEMPRE dice que el
  descubrimiento no es 100% (límite de engram). La lista explícita no tiene ese
  límite.
- **Agnóstica de runtime**: "la memoria disponible", "la herramienta de preguntas
  disponible"; rutas relativas al skill; sin `$ARGUMENTS`; sin tools propietarias.
- **Sin datos**: si no hay memoria disponible, pedí la lista o los artefactos al
  humano; nunca adivines la fase ni inventes SDD.

## Recursos

- [references/discovery.md](references/discovery.md) — Fase A: descubrimiento engram-only.
- [references/state-derivation.md](references/state-derivation.md) — Fase B: derivación de fase/estado en vivo + detecciones.
- [references/table-format.md](references/table-format.md) — el formato fijo de salida (contrato inmutable).
