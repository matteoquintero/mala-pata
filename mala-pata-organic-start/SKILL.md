---
name: mala-pata-organic-start
description: Corre el CICLO ODD (Organic Driven Development) a partir de la ruta del kickoff que dejó `/mala-pata-organic` — worktree+base → explorar (ahí se descubre el Dónde) → resolver incertidumbre → clasificar → (feature-doc si es substancial) → implementar task-by-task (work-unit commit + RDD por commit) → cerrar (PR/CI/limpieza) → tabla. El init (`sdd-init`) lo garantiza `/mala-pata-organic` (una vez por proyecto). Usa workers de ODD (direct/delegated), NUNCA agentes `sdd-*` — el hook de preflight `PreToolUse:Agent` de gentle-ai no aplica acá. Para trabajo chico, las fases corren en una sola pasada; el kickoff separado existe para review/handoff, igual que en el par loop/loop-start.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.0.0"
---

# /mala-pata-organic-start — Corre el CICLO ODD desde un archivo de kickoff

Kickoff: **entrada entregada por el CLI** (ruta absoluta al archivo `.md` que dejó `/mala-pata-organic`)

Tu trabajo: leer el kickoff y correr el **ciclo ODD nativo de gentle-ai**, organizado en el flujo mala-pata — worktree aislado, gates humanos donde corresponde, tabla final. Es a ODD lo que `/mala-pata-loop-start` es al SDD: **no reimplementás ODD — lo orquestás.**

> 📖 **El protocolo ODD es la fuente de verdad.** Sus 7 pasos (Authorize → Explore → Resolve → Classify → Track → Implement → Close), el feature-doc, los work-unit commits, la evaluación RDD por commit y el delivery slicing viven en tu **CLAUDE.md global** (`## Implementation Routing → ### ODD protocol`). Este skill los sigue y les suma la capa mala-pata. Si el CLAUDE.md y este skill difieren en la mecánica de ODD, **manda el CLAUDE.md**.

> ⚠️ **Usa workers de ODD (direct inline / delegated direct), NUNCA agentes `sdd-*`.** El preflight `PreToolUse:Agent` de gentle-ai (`gentle-ai sdd-preflight-hook`) solo intercepta dispatches `sdd-*` — no aplica a este skill. No preguntes el preflight canónico de 3 preguntas acá: no existe para este carril.

> 🪶 **Proporcionalidad**: para un cambio chico y ya entendido, las fases de abajo corren en una sola pasada (explorá → implementá → cerrá) sin pausas ceremoniales — la separación kickoff/start existe para dar un punto de review/handoff entre "qué se va a hacer" y "hacerlo", igual que en el par `mala-pata-loop`/`mala-pata-loop-start`, no para forzar burocracia en lo chico.

## Reglas duras

> ⛔ **#1 — Worktree + base: EJECUTÁ lo que el kickoff ya confirmó, no decidas de nuevo.** El kickoff trae `base` y `branch` ya confirmados con el humano en `/mala-pata-organic`. Creá el worktree con esos valores tal cual — no propongas otra base ni la cambies en silencio. Si el kickoff no trae `base`/`branch`/`worktree` completos, PARÁ y pedilo al orquestador.
> ⛔ **#2 — RDD vive acá, por work-unit commit.** Tras cada commit, si RDD está on, corré `gentle-ai review assess` y seguí el plan nativo (ver ODD protocol). NO es un gate al final — es **per-commit**.
> ⛔ **#3 — Rutas absolutas SIEMPRE** (la cwd se resetea entre comandos a tu dir base, que suele ser el repo principal): `git -C <ABS-worktree> …`, nunca comandos pelados; antes de CUALQUIER escritura/commit, `git -C <ABS-worktree> rev-parse --show-toplevel` debe devolver el worktree, no el main.
> ⛔ **#4 — No implementes antes de Explorar y Clasificar.** El plan de fases de abajo va en orden: worktree → explorar → clasificar → (track si substancial) → implementar. No saltes a escribir código "para ir resolviendo" antes de esos pasos, aunque el cambio te parezca chico y obvio.

## Paso 1 — Cargar el kickoff + contexto de engram

1. La entrada es una **ruta absoluta a un archivo `.md`** (el que `/mala-pata-organic` escribió en `<carpeta-del-proyecto>-mala-pata/<change-name>.md`). Si no empieza con `/` o el archivo no existe → **PARÁ** y pedí la ruta correcta. No inventes el contexto.
2. `Read` completo: frontmatter (`change_name`, `project`, `route: organic`, `base`, `branch`, `worktree`, `tdd_mode`) y cuerpo (Qué, Why, Done, Decisiones ya tomadas, Riesgo, Dónde-hint).
3. Si `route` no es `organic` → **PARÁ**: este kickoff no es de este skill (probablemente es un kickoff de `/mala-pata-loop`, que usa `/mala-pata-loop-start`).
4. `mem_search("odd/<change_name>/kickoff")` solo para confirmar el puntero — no es bloqueante si falla, el archivo ya es la fuente de verdad.

## Paso 2 — Worktree + base (ODD Fase 1 de la capa mala-pata — Regla dura #1)

1. **¿Ya estás en el worktree del kickoff?** `git branch --show-current`. Si coincide con `branch` → saltá al punto 4.
2. Si no existe → creálo con los valores YA confirmados del kickoff (no re-preguntes base/tipo de rama):
   ```bash
   git -C <ABS-repo> worktree add <worktree del kickoff> -b <branch del kickoff> <base del kickoff>
   ln -s <ABS-repo>/.env <worktree>/.env && ln -s <ABS-repo>/node_modules <worktree>/node_modules
   # (ajustar symlinks al stack real del proyecto)
   ```
3. **Rutas ABSOLUTAS SIEMPRE** (Regla dura #3) — todo `git`/`npm`/lectura/escritura referencia el worktree por ruta absoluta (`git -C <ABS-worktree> …`, `npm --prefix <ABS-worktree> …`). Antes de cualquier escritura: `git -C <ABS-worktree> rev-parse --show-toplevel` debe devolver el worktree.
4. **Init guard**: `mem_search("sdd-init/{project}")` — quedate solo con el ítem EXACTO. Si no existe → avisá al orquestador; no corras el init acá (`/mala-pata-organic` ya lo garantiza). Con el ítem exacto, confirmá `strict_tdd` contra el `tdd_mode` del kickoff — si difieren, el de `sdd-init` manda (es la fuente en vivo).

## Paso 3 — Explorar + resolver incertidumbre (ODD 2-3 — **acá se descubre el Dónde**)

Explorá el código y los requisitos **proporcional al pedido** antes de escribir una línea. El kickoff trae un `Dónde (hint opcional)` — puede estar vacío o ser solo una pista; **este paso es el que lo confirma o lo completa**, nunca una precondición previa. Registrá los archivos/módulos tocados: van al feature-doc (Paso 5) si el trabajo es substancial, o quedan en el resumen de cierre si es chico.

Research opcional solo para una **incertidumbre nombrada**; 1 pregunta al humano solo para una **decisión de producto real** (después pará y esperá); a lo sumo **un** assumption-challenge read-only para una premisa de alto impacto. No inventes alcance sobre el Qué/Done/Decisiones que ya trae el kickoff — esos ya pasaron el gate en `/mala-pata-organic`.

## Paso 4 — Clasificar (ODD 4)

**Substancial** = 2+ pasos de implementación con sentido, o progreso que valga recuperar tras una interrupción. **Chico y entendido** = queda chico, sin artefactos durables — seguí directo al Paso 6.

## Paso 5 — Track (ODD 5 — solo si substancial)

Antes del primer write: creá `odd/tasks/<change_name>.md` + su mirror en engram `odd/<change_name>/tasks` (automático, sin pedir permiso de tasks/storage). **El `Why` del kickoff FLUYE al feature-doc** (sección de motivación/contexto). Avisá en **1 línea** qué feature-doc creaste y cuántas tasks tiene. (Contenido y contrato del doc: ODD protocol del CLAUDE.md.)

## Paso 6 — Implementar task-by-task (ODD 6)

Por cada task: la **topología más chica** — direct inline (1-3 archivos ya entendidos) / delegated direct (entender 4+ o escribir 2+ no triviales) — con el **modo TDD del proyecto** (`strict_tdd` de sdd-init) y los checks aplicables. Marcá la task solo tras **observar** su resultado + checks; actualizá el feature-doc y el mirror.
- **Cada task cierra con ≥1 work-unit commit en la feature branch**, con tests+docs junto al comportamiento, Conventional Commit; registrá el commit en el feature-doc como evidencia.
- **RDD por commit** (Regla dura #2): tras cada work-unit commit, si RDD on → `gentle-ai review assess --cwd <ABS-worktree> --agent claude-code --base-ref <último boundary revisado> --committed-only --json`; leé `review_due`; si es true, ejecutá **verbatim** el `next_transition.command` que devuelve; el boundary avanza al acknowledgear. `false` → registrá `review_due_reason` y seguí. **El detalle completo (tiers, consent medio/alto, continuaciones) vive en el ODD protocol del CLAUDE.md — no lo reimplementes.**
- **Delivery slicing**: forecast ~400 líneas autoradas; estrategia `ask-on-risk` (default) / `auto-chain` / `single-pr`; resolvé los skills `work-unit-commits` y `chained-pr` por nombre de registro antes de armar PRs.

## Paso 7 — Cerrar (ODD 7 + cierre mala-pata)

Reportá el **resultado verificado** + todo check fallado/skippeado/pendiente + próximo paso. Después, el cierre mala-pata: reusá de `/mala-pata-loop-start` las sub-fases **4.1 (reporte), 4.1-bis (re-verificar/renumerar migración si tocaste una), 4.2 (destino PR/merge con GATE), 4.4 (CI proactivo), 4.5 (limpieza con GATE)** — **NO la 4.3** (esa ya no existe en el ciclo SDD; RDD ya corrió por commit acá, en el Paso 6). **El `Why` del kickoff FLUYE al body del PR** (sección de motivación).
**Excepción de limpieza** si trabajaste con commits incrementales DENTRO del worktree de una feature en curso: esa rama/worktree la cierra su propio ciclo, no organic-start — solo limpiás lo que este skill creó.

## Paso 8 — Tabla final (OBLIGATORIO)

Mismo formato que `/mala-pata-loop-start` Paso 5: tabla Markdown, un hito por fila, emoji + evidencia concreta. Filas típicas (solo las que apliquen):

| Hito | Estado |
|---|---|
| Autorización | ✅ cambio autorizado / read-only |
| Worktree + base | ✅ `<branch>` off `<base>` |
| Explore (Dónde) | ✅ `<n>` archivos/módulos tocados |
| Feature-doc (si substancial) | ✅ `odd/tasks/<change_name>.md` · `<n>` tasks |
| Apply (TDD si aplica) | ✅ Red-Green-Refactor, `<n>` tests |
| Work-unit commits | ✅ `<n>` commits · RDD assess: `<granted/passive/…>` |
| PR `#<n>` → `<branch>` | ✅ MERGEADO (merge commit `<sha>`) |
| CI post-merge | ✅ VERDE |
| Cleanup (worktree + rama) | ✅ Hecho |

## Persistencia

Para trabajo **substancial**, el **feature-doc** (`odd/tasks/<change_name>.md` + mirror engram `odd/<change_name>/tasks`) ES la persistencia de ODD. Para trabajo **chico** sin feature-doc, un cierre liviano opcional (`mem_save` topic `odd/<change_name>/organic`) si querés continuidad futura.
