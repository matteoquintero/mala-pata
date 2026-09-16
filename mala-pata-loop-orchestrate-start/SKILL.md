---
name: mala-pata-loop-orchestrate-start
description: Ejecuta un lote de kickoffs SDD EN PARALELO — crea un worktree por kickoff, los adelanta a origin/<base> (anti-stale), arma UN launch config de Warp (una sesión de Claude por tab) y lo abre. El propósito ES lanzar muchos SDD en paralelo de una sola ola; el conflicto de archivos se maneja serializando el APPLY (cada sesión frena en su gate), NO reteniendo el lanzamiento.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.0.0"
---

# /mala-pata-loop-orchestrate-start — Lanzar un LOTE de SDD en paralelo

Sos el **ejecutor del lote**. Te pasan los kickoffs de una **ola** y los **lanzás TODOS en paralelo**:
un worktree por kickoff + una sesión de Claude por kickoff (una tab de Warp cada una). El plan
(olas/conflictos/orden de Apply) lo produce `/mala-pata-loop-orchestrate` — este skill EJECUTA.

> ✅ **El propósito es el paralelismo.** Lanzá TODOS los kickoffs de la ola que te den, aunque
> compartan archivos. Los worktrees aíslan el trabajo (dirs/índices distintos) → las sesiones
> **planean en paralelo** sin pisarse. El conflicto por archivo compartido se resuelve **serializando
> el APPLY** (cada `/mala-pata-loop-start` frena en su gate previo a Apply; el humano/kickoff decide el
> orden de merge), **NO** reteniendo el lanzamiento. NUNCA limites el lanzamiento a "solo la ola sin
> conflicto": eso mata el sentido de orquestar.

NO corrés los ciclos SDD acá — cada tab es una **sesión de Claude independiente** con su propio
contexto y sus propios gates. Este skill solo **prepara y abre** esas sesiones.

## Paso 0 — Input y confirmación
- Input: la lista de kickoffs de la ola a lanzar (rutas absolutas a los `.md` de `/mala-pata-loop`;
  legacy: ids de engram o topic_keys `sdd/<name>/kickoff`) + la **branch base** (default `development`).
- Para cada kickoff: si es ruta → `Read` directo y sacá `change_name`/`branch_base` del frontmatter YAML. Si es legacy → `mem_search` → `mem_get_observation`; si devuelve el puntero liviano (`Kickoff en archivo: <ruta>`), seguí esa ruta.
- **Confirmación de branch base — SIEMPRE, una sola vez para toda la ola**: manda el `branch_base` del
  frontmatter de cada kickoff (ya confirmado con el humano al crearlo); el default de la ola solo aplica a
  kickoffs legacy sin frontmatter. En la confirmación del lote, mostrá **la base de cada kickoff** en la
  lista ("`<change>` off `<base>`") y esperá UN solo OK para toda la ola. Cualquier rama es válida con ese
  OK — no bloquees ningún kickoff por no salir de `main`/`development`; si el humano corrige una base,
  actualizá el frontmatter de ese kickoff antes de lanzar.
- Si el usuario no aclaró qué lanzar, lanzá **todos** los kickoffs que te pasó (el default es la ola
  completa en paralelo). Solo escaloná si el usuario lo pide explícito.

## Paso 1 — Un worktree por kickoff (§18, aislamiento real)
Por cada `change-name`, secuencial (para no lockear el índice de git):
```
git -C /ABS worktree add /ABS-worktrees/<change-name> -b feature/<change-name> <branch-base>
```
Después symlinkeá los untracked que el stack necesite (`.env`/`node_modules` o equivalente), igual que
hace el comando de arranque de un kickoff individual. ⚠️ Para verificar el symlink de `.env` NUNCA lo
nombres como argumento directo (`ls -la <wt> | grep '\.env'` — ver la regla en loop-start).

## Paso 2 — Anti-stale: adelantar los worktrees a origin/<base> (OBLIGATORIO)
`git worktree add` basa el worktree en tu `<base>` LOCAL tal cual esté — y el local suele estar
**atrás** de origin (ver memoria `worktree-nace-viejo-development-stale`). Si lanzás así, los explore
de las sesiones concluyen sobre código stale. Por eso, ANTES de abrir las tabs:
```
git -C /ABS fetch origin <base>
# por cada worktree recién creado (branches sin commits → ff limpio, sin tocar historia):
git -C /ABS-worktrees/<change-name> merge --ff-only origin/<base>
```
Verificá que cada worktree quede en `origin/<base>` (`git -C <wt> rev-parse --short HEAD`). Si un
worktree ya tuviera commits y el ff fallara, PARÁ y avisá (no forces): ese worktree no nace limpio.
(`ff-only` no pierde historia — por eso es la única forma de avance permitida acá.)

## Paso 3 — Un launch config de Warp con N tabs (una sesión de Claude por kickoff)
- Verificá `claude` en PATH (`which claude` → típicamente `/Users/<user>/.local/bin/claude`).
- Escribí UN launch configuration:
  - Archivo: `~/.warp/launch_configurations/mpl-orchestrate-<slug-lote>.yaml` (creá el dir si falta).
  - Schema (verificado con docs Warp):
    ```yaml
    ---
    name: mpl-orchestrate-<slug-lote>
    windows:
      - tabs:
          - title: <change-name>
            color: blue
            layout:
              cwd: /ABS-worktrees/<change-name>
              commands:
                - exec: claude "/mala-pata-loop-start <ruta-absoluta-del-kickoff-1.md>"
          - title: <change-name-2>
            color: green
            layout:
              cwd: /ABS-worktrees/<change-name-2>
              commands:
                - exec: claude "/mala-pata-loop-start <ruta-absoluta-del-kickoff-2.md>"
          # ... una tab por kickoff de la ola
    ```
- Abrir: `open "warp://launch/mpl-orchestrate-<slug-lote>"`.
  Si el URI no dispara en esta versión de Warp → decile al usuario que la abra desde el
  **Command Palette → "Launch Configuration" → mpl-orchestrate-<slug-lote>** (el YAML ya quedó escrito).
  No inventes otro mecanismo.

## Paso 4 — Reportar
Devolvé: worktrees creados (+ que quedaron en `origin/<base>`), path del launch config, y qué tabs
quedaron (una por kickoff). Recordá el **orden de Apply** que dio el plan (qué mergea primero) y que
las demás sesiones **esperan en su gate previo a Apply** y rebasan sobre `origin/<base>` al integrar.
⚠️ El orquestador (esta sesión) NO sigue esos ciclos; el seguimiento/gates ocurren en cada tab. Ofrecé
`mala-pata-radar` para ver el avance del lote (descubre y confirma con git en una sola corrida).

## Reglas duras
- **LANZÁ LA OLA COMPLETA en paralelo** — no la recortes a "solo lo sin conflicto". El paralelismo ES
  el objetivo; el conflicto se maneja serializando el Apply, no el lanzamiento.
- **Anti-stale SIEMPRE** (Paso 2): ningún worktree se lanza sin estar en `origin/<base>`.
- **Colisión de migraciones**: si ≥2 kickoffs de la ola seedean migración, recordales (en el reporte)
  que el número es **provisional, no una reserva**: el primero que mergea se lo queda y los demás
  renumeran al integrar (ver `/mala-pata-loop-start`, Paso 4.1-bis). La verdad de los números tomados
  es **git** (medí las ramas), NO un registry en engram; los kickoffs traen su número provisional en el
  frontmatter (`migrations_reserved`). Nunca por el número de archivo.
- NO auto-lances kickoffs con **dependencia dura sin resolver** (el proveedor no cerró design): esos
  quedan para una ola posterior; el resto de la ola sí va.
- `ff-only` y `fetch` son las únicas mutaciones de git; nunca `reset --hard`/`rebase` forzado acá.
- Rutas ABSOLUTAS en comandos/YAML; relativas solo al hablarle al usuario.

## Compatibilidad de runtime
El bloque de Warp/Claude solo corre cuando el runtime es Claude con Warp. En otro CLI: creá los
worktrees + anti-stale y devolvé los comandos `/mala-pata-loop-start` por worktree; no invoques
`claude`, Warp ni rutas `.claude/` que no apliquen.
