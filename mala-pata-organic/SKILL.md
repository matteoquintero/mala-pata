---
name: mala-pata-organic
description: Corre un cambio chico y ya entendido de punta a punta en UNA sola pasada — worktree → Organic Implementation Routing (direct inline / delegated direct) → apply (TDD) → verify liviano → PR → limpieza. Sin ciclo SDD completo (sin explore/propose/spec/design/preview, sin kickoff separado). Si en el camino se descubre que el alcance no era chico, escala a /mala-pata-loop. Trigger: pedido puntual ya entendido, pocos archivos, sin decisión de arquitectura pendiente.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.0.0"
---

# /mala-pata-organic — cambio directo, sin ciclo SDD completo

Pedido del usuario: **entrada entregada por el CLI**

Tu trabajo: interpretar el pedido YA (nada de kickoff separado, nada de explore/propose/spec/design/preview) y correrlo de punta a punta en UNA sola pasada: worktree → ruta orgánica → apply → verify → PR → limpieza. Es el camino rápido — si el pedido no entra en ese molde, este skill tiene que frenar y mandarte a `/mala-pata-loop`, no forzarlo.

> ⛔ **Regla dura #1 — esto es para cambios CHICOS y ya entendidos.** Si en cualquier punto descubrís que en realidad toca muchos archivos, hay una decisión de arquitectura sin resolver, o el alcance no está claro — **PARÁ** y decíselo al usuario: "esto no es un `/mala-pata-organic`, hace falta `/mala-pata-loop`". No fuerces un cambio grande por acá — es exactamente el error que este skill existe para evitar.
>
> ⛔ **Regla dura #2 — la base sale de DONDE VIVE el código que se toca, y SIEMPRE se confirma con el humano antes de crear/tocar nada.** A diferencia del ciclo SDD completo (que sí exige `main`/`development`), organic puede salir de **cualquier rama** — un fix sobre código que solo existe en una feature en curso se hace SOBRE esa feature (commits incrementales en su worktree existente, o worktree nuevo off esa rama), no off main. Lo no negociable acá no es la rama: es la **pregunta** — proponé la base con tu razón ("el código que toco vive en X") y esperá el OK. Nunca asumas la base en silencio, ni bloquees por no ser main.
>
> ⛔ **Regla dura #3 — únicas preguntas interactivas válidas: confirmación de la base (Regla #2), destino del PR/merge y consent de Revisión/RDD** (estas dos últimas con el mismo mecanismo que el ciclo completo, ver Paso 5). Nada de "ritmo" ni "artifact store" — igual que en `/mala-pata-loop-start`.

## Paso 0 — Gate de tamaño (antes de tocar nada)

Medí si el pedido entra en el molde:
- **(a)** ¿Ya sabés exactamente qué archivo(s) tocar y cómo, sin necesitar investigar el "por qué" del negocio?
- **(b)** ¿Son pocos archivos (orientativo: 1-5), sin componente UI nuevo genuino, sin endpoint/contrato nuevo?
- **(c)** ¿No hay ninguna decisión de arquitectura pendiente por resolver con el humano?

- Las 3 son sí → seguís al Paso 1.
- Falta claridad en 1-2 → hacé 1-2 preguntas concretas puntuales y esperá la respuesta. No inventes alcance.
- No entra en el molde (grande, ambiguo, con decisión de diseño real) → **PARÁ** y proponé `/mala-pata-loop` en su lugar. No sigas con este skill.

> **Organic ≠ perfil MINIMAL del ciclo** (decisión deliberada): organic NO hace SDD — cero artefactos de planeación, una sola pasada. Si el cambio es chico pero amerita rastro SDD (spec/design/trazabilidad en engram), eso es `/mala-pata-loop` con perfil MINIMAL, no este skill.

## Paso 1 — Worktree (mismo mecanismo que `/mala-pata-loop-start`, Paso 2)

1. Derivá un `change-name` corto en kebab-case a partir del pedido.
2. **Base — proponé y confirmá (Regla dura #2)**: determiná DÓNDE vive el código que vas a tocar:
   - Vive en `main`/`development` → proponé esa como base (worktree nuevo, convención única).
   - Vive solo en una **feature en curso** (un SDD in-flight u otra rama de trabajo) → proponé ESA rama: commits incrementales en su worktree existente si está vivo, o worktree nuevo off esa rama si hace falta aislamiento.
   Presentale la propuesta al humano con tu razón en una línea ("el código que toco vive en X") y **esperá el OK antes de crear/tocar nada**. Nunca bloquees por "no es main" — esa regla es del ciclo SDD completo, no de organic.
3. Creá el worktree (`git worktree add`) off esa base — **convención ÚNICA, sin excepciones**: branch `feature/<change-name>`, ruta `<ABS-repo>/.claude/worktrees/<change-name>` (el radar localiza ramas y worktrees por esta convención; desviarse los vuelve invisibles al diagnóstico). Symlinkeá `.env`/`node_modules` o el equivalente untracked del stack del proyecto.
4. Confirmá que el init del proyecto ya existe (`mem_search("sdd-init/{project}")`, quedate solo con el ítem EXACTO). Si no existe → corré `sdd-init` primero, no lo saltees.
5. Trabajá el worktree con rutas ABSOLUTAS siempre — la cwd se resetea entre comandos.

## Paso 2 — Ruta orgánica (Organic Implementation Routing del CLAUDE.md global)

Con el worktree listo, aplicá el routing orgánico tal cual está definido en las reglas globales — no reinventes un mecanismo propio acá:

- **Entender 1-3 archivos, o un cambio mecánico ya entendido** → directo inline: escribilo vos mismo, sin lista de tasks separada ni sub-agente.
- **Entender necesita 4+ archivos, o escribir 2+ archivos no triviales** → delegated direct: UN agente de exploración O UN agente escritor (lo que haga falta, no ambos si no corresponde), con instrucciones puntuales derivadas del pedido — nunca dispares un `sdd-tasks`/`sdd-apply` completo, eso es del ciclo SDD, no de este skill.

Si en este paso el alcance real resulta más grande de lo que parecía al entrar → volvé a la Regla dura #1 y escalá a `/mala-pata-loop`. No es un fallo, es el diseño funcionando.

## Paso 3 — Apply (según el modo del proyecto)

Leé `strict_tdd` de `sdd-init/{project}` (Paso 1) y seguí el modo real, igual que `/sdd-apply`:

- **`strict_tdd: true` → Strict TDD Mode, NO NEGOCIABLE**: Red → Green → Refactor para el cambio, aunque sea chico. Escribí el test que falla primero, hacelo pasar con lo mínimo, después refactorizá.
- **`strict_tdd: false` → Standard Workflow**: implementá directo, matcheando el estilo/patrones existentes del proyecto. Esto NO es un atajo degradado — es el modo oficial para proyectos que deliberadamente no fuerzan esa disciplina, tengan o no test runner. No inventes tests que el proyecto no pide.

En ambos modos: corré la suite existente antes de dar por hecho. Nunca dejes tests rotos ni los borres/skippees para que pasen.

## Paso 4 — Verify liviano

No hay spec formal en este camino — verificá contra lo que el usuario pidió explícitamente, no inventes criterios nuevos:
- Build limpio + suite de tests en verde.
- Smoke live si el cambio toca algo visible/ejecutable (UI, endpoint, comando).
- Si algo no pasa → arreglalo antes de seguir. No marques "listo" con algo en rojo.

## Paso 5 — Cierre: PR, Gate RDD, CI y limpieza

Reusá **exactamente** el Paso 4 de `/mala-pata-loop-start` (sub-fases 4.1 a 4.5: reporte de cierre → destino del PR/merge con GATE → Gate RDD con GATE, se dispara solo → revisión de CI proactiva → limpieza con GATE proactivo, nunca esperes a que te lo pidan). Mismo mecanismo, mismas reglas — no lo reinventes acá, es exactamente el mismo skill al que le arreglamos la limpieza pasiva.

**Excepción de limpieza (4.5) cuando la base fue una feature en curso**: si trabajaste con commits incrementales DENTRO del worktree existente de esa feature, la limpieza **NO aplica** — ese worktree y esa rama pertenecen al ciclo de la feature, los cierra SU propio SDD, no organic. Solo limpiás lo que organic mismo creó.

## Paso 6 — Resumen final en tabla (OBLIGATORIO)

Mismo formato que el Paso 5 de `/mala-pata-loop-start`: tabla Markdown, un hito por fila, emoji + evidencia concreta. Filas típicas de este camino (incluí solo las que apliquen):

| Hito | Estado |
|---|---|
| Apply (TDD si aplica) | ✅ Red-Green-Refactor, `<n>` tests |
| Verify | ✅ build + suite en verde |
| Gate RDD (pre-pr) | ✅ receipt `<target_identity corto>` · lentes: `<0\|1\|4>` |
| PR `#<n>` → `<branch>` | ✅ MERGEADO (merge commit `<sha>`) |
| CI post-merge | ✅ VERDE |
| Cleanup (worktree + rama) | ✅ Hecho |

## Persistencia (liviana, no fase-por-fase)

A diferencia del ciclo completo, acá **no** se persiste un artefacto por fase. Al cerrar (después del Paso 6), un solo `mem_save` con `topic_key: "sdd/<change-name>/organic"`, `type: "architecture"`, resumiendo: qué se pidió, qué se tocó (archivos), cómo se verificó, y el resultado del cierre (PR/merge + gate RDD). Esto le da continuidad futura sin la ceremonia de 9 artefactos separados.
