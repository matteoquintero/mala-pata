---
name: mala-pata-roadmap-radar
description: Status READ-ONLY de un ROADMAP (no de SDD sueltos — eso es /mala-pata-radar). Toma el roadmap .md de un dominio (versionado en el repo, NO memoria), deriva el estado de CADA fase EN VIVO contra git (terminado / en proceso / pendiente / bloqueado), y muestra una tabla fija + qué está listo para arrancar ahora y cuáles pueden ir en paralelo. NO mira engram, NO orquesta, NO ejecuta, NO muta nada. Formato de salida fijo e inmutable. Trigger — "status del roadmap", "cómo va el roadmap de <dominio>", "avance del roadmap <slug>", o la ruta/slug de un roadmap.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.1.0"
---

# /mala-pata-roadmap-radar — avance de un roadmap contra git (formato fijo)

Entrada: **la provista por el CLI** — la ruta a un roadmap `.md` (`mala-pata/roadmap/<slug>.md`) o el slug/dominio del roadmap.

Tu trabajo: mostrar, en **un formato fijo y siempre igual**, cómo va un roadmap de un dominio — fase por fase — derivando cada estado **en vivo contra git**, y marcando **qué puede arrancar ahora y cuáles en paralelo**. Es a los roadmaps lo que `/mala-pata-radar` es a los SDD sueltos, con dos diferencias deliberadas: la **unidad es la fase de un roadmap** (no un change), y la **fuente es el roadmap `.md` + git, NUNCA engram**.

> **No es `/mala-pata-radar`.** radar descubre SDD/changes desde la memoria y los confirma con git. Este skill NO toca memoria: lee el roadmap `.md` (que vive en el repo) y mide git. Si lo que querés es el estado de SDD sueltos, ese es radar.

## Requisitos (orquestar, no reinventar)

mala-pata orquesta herramientas de comunidad — no las reimplementa. Chequeá al arrancar:

- **Obligatorias** (sin fallback — si falta, PARÁ y pedí instalarla, no arranques):
  - `git` — fuente de verdad del avance. Siempre presente; no requiere instalación.
- **Recomendadas** (con fallback — si falta, avisá en una línea y seguí degradado):
  - `gh` (o la CLI de PRs del proyecto, p.ej. `az repos`) — estado de PRs. Fallback: solo ramas y merges locales/remotos; marcá que no se consultaron PRs. Instalar: `brew install gh`.
- **Explícito — NO usa engram.** El roadmap `.md` (en el repo) + git son las dos únicas fuentes. No busques en memoria.

Chequeo: `command -v <tool>`. Si falta una obligatoria, no sigas.

## Principios duros (no negociables)

- **Git = verdad.** "terminado" se confirma SOLO contra la branch de integración recién fetcheada — nunca por un checkbox del `.md`, un archive-report, ni memoria. Un `.md` dice qué se planeó; git dice qué pasó.
- **Cero cache, cero memoria.** Cada corrida re-deriva todo desde el `.md` + git vivo. Prohibido reportar un estado sin re-medirlo en esta corrida. NO engram.
- **Read-only.** Nunca commit, push, merge, fetch destructivo ni escritura. Correr este radar siempre es seguro.
- **No tomás atribuciones.** Solo informás qué fase está en qué estado y qué puede arrancar. NUNCA ejecutás ni OFRECÉS ejecutar una fase (triage, apply, PR, merge). Tu salida TERMINA en el reporte — prohibido cerrar con "¿arranco X?".
- **Formato fijo SIEMPRE** — mismo orden, mismas columnas, mismo léxico, en cada corrida (memoria mecánica para el humano).

## Fase 0 — Cargar el roadmap (git, no memoria)

1. Resolvé el project root: `git -C <cwd> rev-parse --show-toplevel`.
2. Resolvé el roadmap `.md`:
   - Si la entrada es una ruta → `Read` directo.
   - Si es un slug/dominio → buscá `mala-pata/roadmap/<slug>.md` (o el default que el roadmap haya usado). Si hay varios candidatos y no se especificó → listá los `.md` disponibles y pedí cuál (una sola pregunta, parás y esperás).
   - Si no existe → decilo y PARÁ; no inventes fases.
3. Del `.md` extraé por fase: **#**, **nombre**, **slug** (el change-name estable), **ruta** (organic/loop:PERFIL/shot), **Depende de**, y del cierre del DAG el **orden topológico** y los **paralelizables** (`{..}`). Si el roadmap es viejo y una fase no tiene `slug`, marcá esa fase `sin-slug` (no se puede matchear determinísticamente — ver Fase 2).

## Fase 1 — Frescura (git vivo, cero cache)

1. `git -C <repo> fetch --all --prune`.
2. Detectá y **confirmá** la branch de integración (no la asumas: `main`/`development`/la que el repo use). Anotá su SHA para el banner.
3. Si hay `gh`/CLI de PRs, traé la lista de PRs abiertos/mergeados del repo.

## Fase 2 — Estado por fase, en vivo (match por slug)

Por cada fase, matcheá contra git por su **slug**: una rama o PR cuyo nombre sea `<slug>` o termine en `/<slug>` (la convención del roadmap: change-name = slug, rama `<tipo>/<slug>`). Derivá el estado — **solo desde git**:

- **terminado** — la rama de la fase está **mergeada en la branch de integración** recién fetcheada (confirmado por `git branch --merged <integración>`, un merge commit, o un PR con estado merged). Evidencia: merge SHA o PR#.
- **en proceso** — existe la rama o un PR ABIERTO para el slug, con commits propios, pero NO mergeado. Evidencia: rama + nº de commits ahead, o PR# abierto.
- **pendiente** — no hay rama ni PR para el slug.
- **bloqueado** — es `pendiente` PERO al menos una de sus `Depende de` NO está `terminado`. (Es un `pendiente` que explica por qué todavía no puede arrancar.)

Reglas de la derivación:
- **terminado NUNCA se infiere del `.md`** ni de un checkbox de DoD — solo del merge real en git.
- Fase `sin-slug` (roadmap viejo): no la claves por semántica difusa. Marcala `? (sin slug)` en Estado, con nota "el roadmap no registró slug; re-generá el roadmap o pasá el branch a mano". No adivines.
- Una rama mergeada cuyo worktree/branch sigue viva es `terminado` igual (el merge manda); podés anotarlo en evidencia como "mergeado, falta limpieza".

## Fase 3 — Qué puede arrancar ahora + paralelo

- **Listo para arrancar ahora** — fases en estado `pendiente` (no `bloqueado`) cuyas dependencias están TODAS `terminado`.
- **En paralelo** — dentro de las "listo ahora", agrupá las que el DAG marca paralelizables entre sí (del bloque `Paralelizables: {..}` del roadmap) y que no declaran conflicto — esa es la ola que se puede lanzar junta.
- **En proceso ahora** — las que ya están corriendo (para no re-lanzarlas).

## Salida — formato fijo (SIEMPRE idéntico)

```
Roadmap: <nombre/slug>  ·  repo: <nombre>  ·  integración: <branch>@<sha-corto>
Fuente: roadmap.md + git en vivo · SIN engram · <fecha-hora>

| # | Fase | slug | Ruta | Depende de | Estado | Evidencia |
|---|------|------|------|-----------|--------|-----------|
| 1 | <nombre> | <slug> | loop:STD | — | terminado | merge <sha> / PR #<n> |
| 2 | <nombre> | <slug> | organic | 1 | en proceso | rama <tipo>/<slug> +<k> commits / PR #<n> |
| 3 | <nombre> | <slug> | shot | 1 | pendiente | sin rama |
| 4 | <nombre> | <slug> | loop:LITE | 2 | bloqueado | espera fase 2 |

Listo para arrancar ahora: <fases cuyas deps están todas terminadas>
  En paralelo (se pueden lanzar juntas): { <fase>, <fase> }
En proceso ahora: <fases con rama/PR vivos>
Bloqueado por dependencias: <fase> → espera <fase(s)>

Leyenda: terminado = mergeado a integración (git) · en proceso = rama/PR vivo sin mergear · pendiente = sin rama · bloqueado = pendiente con deps sin terminar
```

- La tabla lleva **una fila por fase del roadmap**, en el orden del `.md`. Ninguna fase se omite.
- **Estado con tokens de texto** (`terminado` / `en proceso` / `pendiente` / `bloqueado`) — sin emojis, sin colores inventados.
- **Evidencia concreta** por fila (SHA de merge, PR#, nº de commits ahead, o "sin rama") — nunca "ok" a secas.
- Si faltó `gh`/CLI de PRs, el banner lo dice ("PRs no consultados; estado por ramas/merges").

## Reglas

- **CERO cache, CERO engram.** Re-derivá todo desde `.md` + git en cada corrida.
- **READ-ONLY.** Nunca mutar nada; nunca ejecutar ni ofrecer ejecutar una fase.
- **Merge = solo git.** Un DoD tildado o un archive-report NO prueban merge.
- **Match por slug exacto**, nunca semántica difusa. Sin slug → `? (sin slug)`, no adivines.
- **Formato fijo** — mismas columnas, mismo orden, mismo léxico, siempre.
- **Sin datos**: si no hay roadmap `.md`, pedilo; si no hay git, no corras. Nunca inventes el estado de una fase.
