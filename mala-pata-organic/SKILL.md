---
name: mala-pata-organic
description: Envuelve el ODD nativo de gentle-ai (Organic Driven Development) y lo organiza en el flujo mala-pata — autorizar → worktree aislado → explorar → clasificar → (feature-doc si es substancial) → implementar task-by-task (work-unit commit + RDD por commit) → cerrar (PR/CI/limpieza) → tabla. RDD vive ACÁ (por commit), NO en el loop/SDD. Si el trabajo necesita spec/design formal, escala a /mala-pata-loop. Trigger: cambio directo ya entendido, o trabajo substancial sin decisión de arquitectura pendiente.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "2.0.0"
---

# /mala-pata-organic — el carril ODD, organizado en tu flujo

Pedido del usuario: **entrada entregada por el CLI**

Tu trabajo: correr el cambio por el **carril ODD** (Organic Driven Development) de gentle-ai, pero **organizado en el flujo mala-pata** (worktree aislado, gates humanos, tabla final). Es a ODD lo que `/mala-pata-loop` es al SDD: **no reimplementás ODD — lo orquestás.**

> 📖 **El protocolo ODD es la fuente de verdad.** Sus 7 pasos (Authorize → Explore → Resolve → Classify → Track → Implement → Close), el modelo de feature-doc (`odd/tasks/<feature>.md` + mirror en engram `odd/<feature>/tasks`), los work-unit commits, la evaluación RDD por commit y el delivery slicing viven en tu **CLAUDE.md global** (`## Implementation Routing → ### ODD protocol`). Este skill NO los duplica: los sigue y les suma la capa mala-pata. Si el CLAUDE.md y este skill difieren en la mecánica de ODD, **manda el CLAUDE.md**.

## Reglas duras

> ⛔ **#1 — Escalá a `/mala-pata-loop` (SDD) SOLO si el trabajo necesita spec/design FORMAL**: decisión de arquitectura sin resolver, contrato/endpoint nuevo, o riesgo que amerite el ciclo completo con preview. ODD maneja tanto lo chico como lo **substancial** (con feature-doc); "substancial" NO significa "hace falta SDD". No fuerces SDD por tamaño ni por conteo de archivos.
> ⛔ **#2 — Worktree + base: proponé y confirmá.** La base sale de DONDE VIVE el código que tocás (`main`/`development`, o una feature en curso). Proponé con tu razón en una línea ("el código vive en X") y esperá el OK antes de crear/tocar nada. Nunca asumas la base en silencio ni bloquees por no ser main.
> ⛔ **#3 — RDD vive acá, por work-unit commit.** Tras cada commit, si RDD está on, corré `gentle-ai review assess` y seguí el plan nativo (ver ODD protocol). NO es un gate al final — es **per-commit**. RDD ya NO corre en el loop/SDD.
> ⛔ **#4 — Rutas absolutas SIEMPRE** (la cwd se resetea entre comandos a tu dir base, que suele ser el repo principal): `git -C <ABS-worktree> …`, nunca comandos pelados; antes de CUALQUIER escritura/commit, `git -C <ABS-worktree> rev-parse --show-toplevel` debe devolver el worktree, no el main.

## Fase 0 — Autorizar (ODD paso 1)

¿El pedido autoriza un **cambio**? Investigación, explicación, review, auditoría, comparación, o propuesta/planeación = **read-only** salvo que el humano pida implementar u otra mutación explícita.
- Read-only → inspeccioná/explicá/recomendá, pero **NO** escribas, NO delegues un writer, NO invoques apply, NO crees artefactos de implementación.
- Intención ambigua o condicional → 1 pregunta y quedate read-only hasta la respuesta.

## Fase 1 — Worktree + base (capa mala-pata — lo que ODD nativo no hace)

1. Derivá un `change-name` corto en kebab-case.
2. **Base — proponé y confirmá (Regla #2)**: dónde vive el código (`main`/`development` o una feature en curso). Esperá el OK.
3. **Tipo de rama — aconsejá y confirmá**: `feature/`/`fix/`/`hotfix/`/`refactor/`/`chore/`/`docs/` — nunca `sdd/`. Creá el worktree: `git worktree add <ABS-repo>-worktrees/<change-name> -b <tipo>/<change-name> <base>`; symlinkeá `.env`/`node_modules` o el equivalente del stack.
4. Init guard: `mem_search("sdd-init/{project}")` (solo el ítem EXACTO). Si no existe → `sdd-init` primero.
5. Rutas absolutas siempre (Regla #4). (Si trabajás sobre el worktree existente de una feature en curso, no creás rama nueva.)

## Fase 2 — Explorar + resolver incertidumbre (ODD 2-3)

Explorá el código y los requisitos **proporcional al pedido** antes de escribir. Research opcional solo para una **incertidumbre nombrada**; 1 pregunta al humano solo para una **decisión de producto real** (después pará y esperá); a lo sumo **un** assumption-challenge read-only para una premisa de alto impacto. No inventes alcance.

## Fase 3 — Clasificar (ODD 4)

**Substancial** = 2+ pasos de implementación con sentido, o progreso que valga recuperar tras una interrupción. **Chico y entendido** = queda chico, sin artefactos durables.

## Fase 4 — Track (ODD 5 — solo si substancial)

Antes del primer write: creá `odd/tasks/<feature>.md` + su mirror en engram `odd/<feature>/tasks` (automático, sin pedir permiso de tasks/storage). Avisá en **1 línea** qué feature-doc creaste y cuántas tasks tiene. (Contenido y contrato del doc: ODD protocol del CLAUDE.md.)

## Fase 5 — Implementar task-by-task (ODD 6)

Por cada task: la **topología más chica** — direct inline (1-3 archivos ya entendidos) / delegated direct (entender 4+ o escribir 2+ no triviales) — con el **modo TDD del proyecto** (`strict_tdd` de sdd-init) y los checks aplicables. Marcá la task solo tras **observar** su resultado + checks; actualizá el feature-doc y el mirror.
- **Cada task cierra con ≥1 work-unit commit en la feature branch** (branch first si estás en la default), con tests+docs junto al comportamiento, Conventional Commit; registrá el commit en el feature-doc como evidencia.
- **RDD por commit**: tras cada work-unit commit, si RDD on → `gentle-ai review assess --cwd <ABS-worktree> --agent claude-code --base-ref <último boundary revisado> --committed-only --json`; leé `review_due`; si es true, ejecutá **verbatim** el `next_transition.command` que devuelve; el boundary avanza al acknowledgear. `false` → registrá `review_due_reason` y seguí. **El detalle completo (tiers, consent medio/alto, continuaciones) vive en el ODD protocol del CLAUDE.md — no lo reimplementes.**
- **Delivery slicing**: forecast ~400 líneas autoradas; estrategia `ask-on-risk` (default) / `auto-chain` / `single-pr`; resolvé los skills `work-unit-commits` y `chained-pr` por nombre de registro antes de armar PRs.

## Fase 6 — Cerrar (ODD 7 + cierre mala-pata)

Reportá el **resultado verificado** + todo check fallado/skippeado/pendiente + próximo paso. Después, el cierre mala-pata: reusá de `/mala-pata-loop-start` las sub-fases **4.1 (reporte), 4.1-bis (re-verificar/renumerar migración si tocaste una), 4.2 (destino PR/merge con GATE), 4.4 (CI proactivo), 4.5 (limpieza con GATE)** — **NO la 4.3** (esa ya no existe; RDD corrió por commit en la Fase 5).
**Excepción de limpieza** si trabajaste con commits incrementales DENTRO del worktree de una feature en curso: esa rama/worktree la cierra su propio ciclo, no organic — solo limpiás lo que organic creó.

## Fase 7 — Tabla final (OBLIGATORIO)

Mismo formato que `/mala-pata-loop-start` Paso 5: tabla Markdown, un hito por fila, emoji + evidencia concreta. Filas típicas (solo las que apliquen):

| Hito | Estado |
|---|---|
| Autorización | ✅ cambio autorizado / read-only |
| Feature-doc (si substancial) | ✅ `odd/tasks/<feature>.md` · `<n>` tasks |
| Apply (TDD si aplica) | ✅ Red-Green-Refactor, `<n>` tests |
| Work-unit commits | ✅ `<n>` commits · RDD assess: `<granted/passive/…>` |
| PR `#<n>` → `<branch>` | ✅ MERGEADO (merge commit `<sha>`) |
| CI post-merge | ✅ VERDE |
| Cleanup (worktree + rama) | ✅ Hecho |

## Persistencia

Para trabajo **substancial**, el **feature-doc** (`odd/tasks/<feature>.md` + mirror engram `odd/<feature>/tasks`) ES la persistencia de ODD — reemplaza el viejo "un solo mem_save al cierre". Para trabajo **chico** sin feature-doc, un cierre liviano opcional (`mem_save` topic `sdd/<change>/organic`) si querés continuidad futura.
