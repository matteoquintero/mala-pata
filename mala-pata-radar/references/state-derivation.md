# Derivación de fase + semáforo EN VIVO

Todo se re-deriva cada corrida. Dos fuentes, ninguna cacheada:
- **VCS (git)** = verdad de branch/merge/limpieza.
- **Memoria persistente disponible** = verdad de fase (qué artefactos existen).

## Paso A — Frescura (git)

```
git fetch --all --prune
```
- Detectá la branch de integración del repo (mirá a qué se mergean los feature
  branches; suele ser `development` o `main`). Confirmala, no la asumas.
- Guardá `git rev-parse --short origin/<integr>` para el banner. Por defecto
  operá sobre EL repo actual (el del cwd). Un proyecto abarca varios repos SOLO
  si el humano los nombra explícitamente (o la config del proyecto los declara);
  NUNCA asumas ni salgas a buscar repos hermanos por memoria de sesión ni
  adivinando rutas. Si son varios, repetí los pasos por cada repo nombrado.

## Paso B — Ciclo COMPLETO de cada SDD (memoria — comandos exactos)

Stack concreto: memoria = engram MCP (`mem_search`, `mem_get_observation`). Si
tu runtime usa otra memoria, mapeá a "búsqueda por título exacto" + "traer
contenido por id".

Por CADA change-name `C`, traé TODAS sus fases con UNA búsqueda por el
change-name EXACTO y desnudo (sin palabras extra — agregar
"archive/verify/shipped" hace fallar la búsqueda semántica y fue el bug
histórico de confiar en 1 hit):

```
mem_search(query="C")
```

Quedate con TODAS las observaciones cuyo título sea `sdd/C/<fase>`. Fases en
orden canónico:
```
kickoff · explore · proposal · spec · design · tasks · preview
· apply-progress · verify-report · archive-report · state
```
`fase_memoria` = la MÁS AVANZADA presente. Progreso parcial: si `apply-progress`
dice "X/Y tasks", reportá `apply X/Y`.

Anti-truncado (OBLIGATORIO): si `mem_search("C")` parece truncado o faltan fases
tardías, confirmá el cierre con búsquedas dirigidas y traé el contenido:
```
mem_search(query="sdd/C/archive-report")
mem_search(query="sdd/C/verify-report")
mem_search(query="sdd/C/state")
mem_get_observation(id=<fase más avanzada>)
mem_get_observation(id=<state/decisión de cierre, si existe>)
```
PROHIBIDO derivar la fase de un único hit de búsqueda. Enumerá el ciclo completo.

## Paso C — Realidad git de cada SDD

Convención de branch: `<tipo>/<change-name>` — el prefijo de tipo (`feature/`, `fix/`,
`hotfix/`, `refactor/`, `chore/`, `docs/`, `release/`) se elige por trabajo y se confirma
(ver `_base.md`); **nunca `sdd/`**. El sufijo `<change-name>` es único e igual pase lo que
pase con el prefijo — por eso **localizá la rama por el sufijo, no por prefijo fijo**:
1. Si tenés el kickoff, usá su `branch:` del frontmatter (nombre exacto ya confirmado).
2. Si no, buscá por sufijo: `git branch -r --list '*/<change-name>'` (matchea cualquier
   prefijo convencional). Si aparece bajo `sdd/...`, es una rama LEGACY fuera de convención —
   marcala con flag "rama legacy sdd/ — renombrar" en la evidencia (los skills nuevos ya no
   generan `sdd/`).
   Nota: `<change-name>` es único → el sufijo no colisiona entre SDDs.

Con `<branch>` resuelto (llamalo así abajo):
- ¿Branch existe en remoto? `git branch -r --list 'origin/<branch>'` (o el resultado del punto 2).
- ¿Mergeado a integración? Confirmá por CONTENIDO/commits, no por `--merged`
  solo (el squash no aparece como merged). Dos señales fuertes:
  - `git log origin/<integr> --oneline | grep -i '<change o PR#>'`
  - un archivo/símbolo distintivo del SDD presente en `origin/<integr>`
    (`git grep <símbolo> origin/<integr> -- <path>`).
- Stale: `git rev-list --left-right --count origin/<integr>...origin/<branch>`
  → `A` (integr adelante) `B` (branch adelante). `A` grande = branch vieja.
- ¿Worktree/branch local vivos? `git worktree list`, `git branch --list` (el worktree dir
  sigue siendo `<change-name>` sin prefijo).

## Paso D — Máquina de estados (primer match gana, de arriba a abajo)

1. **❌ CANCELADO** — hay artefacto `state`/decisión que dice ABANDONADO/
   cancelado. Próxima acción: ninguna.
2. **✔️ CERRADO** — mergeado a integración Y sin branch remota Y sin worktree/
   branch local. Próxima acción: ninguna.
3. **✅ MERGEADO (🧹 falta limpieza)** — mergeado a integración PERO worktree o
   branch (local/remota) siguen vivos. Próxima acción: limpiar.
4. **🔴 LISTO P/PR** — apply completo + verify PASS (y/o archive) PERO NO
   mergeado (código en branch, ausente en integración). Próxima acción: abrir
   PR / mergear. Si `stale` (B chico, A grande): añadí "⚠️ actualizar branch +
   re-verificar antes del PR".
5. **🔴 APPLY/VERIFY SIN CERRAR** — apply-progress completo sin verify, o verify
   PASS sin archive. Próxima acción: correr la fase que falta (verify / archive).
6. **🟡 GATE HUMANO** — el último artefacto es un `preview` sin decisión de
   aprobación posterior, O `verify-report` con CRITICAL/WARNING sin resolver, O
   una decisión que pide input humano explícito. Próxima acción: revisar/aprobar.
7. **🟠 PARQUEADO/BLOQUEADO** — depende de otro SDD de la lista aún NO mergeado
   (⛔), O hay nota de pausa (adyacencia/worktree hermano sin merge), O branch
   stale que bloquea. Próxima acción: desbloquear (nombrá el bloqueador).
8. **⚫ SIN INSTRUCCIÓN** — ciclo trabado sin próximo paso claro: apply-progress
   parcial (X/Y) sin continuación ni gate pendiente, o planning detenido a mitad
   sin gate y sin actividad reciente. Próxima acción: el humano define qué sigue.
9. **🟢 EN CURSO** — avanza normal; una fase cerró y la próxima es auto-corrible
   sin gate. Próxima acción: correr la próxima fase (nombrala: p.ej. "correr
   spec", "correr tasks").

## Paso E — Dependencias (entre los SDD de la lista)

Señales de dependencia (leer de kickoff/proposal/design):
- "off <branch> tras merge del sibling PR #X" / "depends_on" / "base branch".
- Mismo archivo/servicio tocado por dos SDD (adyacencia → riesgo de bloqueo).

**Kickoff = archivo, no engram**: la observación `sdd/C/kickoff` de engram es solo un
puntero de una línea (`Kickoff en archivo: <ruta>`). Para leer `depends_on`/branch base
del kickoff, seguí esa ruta con `Read` — el frontmatter YAML del archivo trae
`depends_on`, `paralelizable_con` y `branch_base` directo. Solo los kickoffs viejos
(pre-migración) tienen el contenido completo en engram.

Si A depende de B y B no está mergeado → A va 🟠 con `Depende = #idxB ⛔`.
Si B ya está mergeado → mostrar `Depende = #idxB` sin ⛔ (informativo).

## Reglas de derivación (no negociables)

- **Nunca** derivar "mergeado" de la memoria. Solo de git contra integración.
- **Nunca** confiar en un estado de una corrida anterior. Re-derivar siempre.
- Ante conflicto memoria↔git, **git manda** para branch/merge/limpieza; la
  memoria manda para fase/gate/cancelación.
- Si un dato no se puede verificar en vivo, marcá la celda con `?` y explicá en
  la evidencia — nunca rellenar con una suposición.
