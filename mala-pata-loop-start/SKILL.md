---
name: mala-pata-loop-start
description: Inicia y corre el CICLO SDD a partir de la ruta del archivo de kickoff que dejó /mala-pata-loop — explore → propose → spec → design → tasks → preview → apply → verify → archive, una fase por vez (secuencial, spec y design NO en paralelo), interactivo con gate por fase. Preview es un gate humano OBLIGATORIO entre tasks y apply (recorrido en cristiano + anti-duplicación). El init lo garantiza /mala-pata-loop (una vez por proyecto). La planeación va ANTES de tocar código. El brief es insumo del ciclo, NO una orden de implementar directo.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.0.0"
---

# /mala-pata-loop-start — Corre el CICLO SDD desde un archivo de kickoff

Kickoff: **entrada entregada por el CLI**

Tu trabajo: leer el *kickoff* que dejó `/mala-pata-loop` y **correr el CICLO SDD completo, fase por fase, UNA POR UNA (secuencial, nunca en paralelo)**:

`explore → propose → spec → design → tasks → preview → apply → verify → archive`

(El *init* —una vez por proyecto— ya lo garantizó `/mala-pata-loop`. El *explore* de acá **profundiza en el código real del worktree**; el kickoff fue solo la reinterpretación a alto nivel.) Cada fase cierra con **resumen + PAUSA** esperando OK antes de la siguiente. Toda la planeación (explore→propose→spec→design→tasks) va **antes** de escribir una línea de código.

> ⛔ **Regla dura #1 — NO implementes directo.** Está prohibido escribir código, migraciones o crear archivos de implementación **antes de que el PREVIEW esté aprobado** (el gate final antes de código: tasks primero, luego preview). El "plan de fases" del brief es material para la fase de Tasks, NO la señal para empezar a codear. Si te encontrás explorando para "ir resolviendo la tarea", frená: estás saltando el ciclo.
> ⛔ **Regla dura #2 — preparás el entorno EJECUTANDO el comando de arranque del brief, sin decidir nada.** Si el worktree no existe, creálo corriendo **exactamente** el comando de arranque del brief (ya trae el base branch + los symlinks de `.env`/`node_modules`). No elijas base, no inventes paths, no adivines `main`: solo ejecutás lo que el brief ya especificó. **Solo PARÁS si el brief NO trae comando de arranque completo** (le falta base branch o symlinks) — ahí sí pedilo al orquestador.

> 🌐 **Agnóstico de stack.** Los ejemplos concretos de este comando (`.env`, `node_modules`, `npm`, `TEST_DB_URL`, Storybook, `gh`) son del stack Node/Postgres/GitHub. **Mapealos al stack real del proyecto** (entorno/DB de pruebas, gestor de deps, archivos de config/secrets, workshop de componentes, host de PRs según lo que el proyecto use). La convención del proyecto manda sobre cualquier ejemplo.

> ⛔ **Regla dura #3 — únicas preguntas interactivas válidas de todo el ciclo: confirmación de branch base (Paso 2.2), destino del PR/merge (Paso 4) y consent de Revisión/RDD (Gate RDD, Paso 4.3).** Nada más se pregunta como gate/menú. En particular: **NUNCA preguntes "ritmo"** (interactivo/automático) — el ritmo siempre es interactivo fase-por-fase, ya definido por el perfil del kickoff (ver `_base.md`); un modo automático solo existe si el humano lo pide él mismo, explícito, sin que se lo ofrezcas como opción, **y aun pedido tiene techo por tamaño: solo LITE/MINIMAL; en FULL/STANDARD el ciclo va interactivo sí o sí** (ver `_base.md`, "techo de automático por tamaño de objetivo"). **NUNCA preguntes "artifact store"** — siempre es `engram` para este usuario, no se ofrece como elección. Si en algún punto se te ocurre armar un gate de selección (tabs, menú de "Ritmo/Artefactos/PRs/Revisión" o similar) antes de arrancar el ciclo, es una señal de que estás inventando fuera de este skill — no lo hagas: andá directo del preflight (Paso 2) a la fase Explore (Paso 3).

> ⛔ **Regla dura #4 — el objetivo se define ANTES de preview, nunca EN preview. Alarma de debate.** El preview existe para revisar **si lo que se va a hacer está bien**, NO para discutir **si el objetivo está bien** — el QUÉ ya tuvo que quedar cerrado en explore/propose/spec. Durante las fases de planeación (explore→spec), si notás que se está **debatiendo mucho el QUÉ** — vuelven preguntas sobre el objetivo, el alcance se mueve, aparecen "¿y esto también?" que no cierran, o la misma decisión se re-discute más de una vez — eso es la señal de que **el objetivo no quedó bien definido** (tarjetas rojas que se colaron por el gate de `/mala-pata-loop`, ver su Paso 0). NO sigas empujando hacia adelante: **devolvé el ciclo a explore o propose** para volver a fijar el QUÉ, y recién cuando esté cerrado seguís. Un objetivo con el QUÉ todavía en discusión **NO puede llegar a preview**. Esto no es re-correr fases por gusto — planear sobre un objetivo movedizo garantiza tirar el plan después.

## Paso 1 — Cargar el brief

**Formato actual (default)**: `entrada entregada por el CLI` es una **ruta absoluta a un archivo `.md`** (el que `/mala-pata-loop` escribe en `<carpeta-del-proyecto>-mala-pata/<change-name>.md`, fuera del repo).

1. Si la entrada es una ruta absoluta (empieza con `/`) → `Read` directo sobre ese archivo. Si el archivo no existe → **PARÁ** y pedí la ruta correcta. No inventes el contexto.
2. Leé el frontmatter (change_name, profile, project, branch, branch_base, worktree, depends_on, paralelizable_con, migrations_reserved) y TODO el cuerpo: reglas del método, contexto del proyecto, contrato, reinterpretación técnica, arquitectura, skills condicionales, **decisiones abiertas**, plan de fases, Definition of Done.

**Formato legacy (kickoffs creados antes de este cambio — solo por compatibilidad, no lo uses para kickoffs nuevos)**: si la entrada NO es una ruta absoluta, puede venir como **(a)** un id de engram (`#1234` o `1234`), **(b)** un topic_key (`sdd/<change-name>/kickoff`), o **(c)** el formato combinado viejo `sdd/<change-name>/kickoff · engram #<id>`.
3. Con `#<número>` (casos a/c) → `mem_get_observation(id: <número>)` DIRECTO, nunca `mem_search`.
4. Con topic_key puro (caso b) → `mem_search` por el topic_key → `mem_get_observation`. Si lo que devuelve es el **puntero liviano nuevo** (`Kickoff en archivo: <ruta>`) en vez del contenido completo → seguí esa ruta y andá al punto 1.
5. **Auto-migración one-shot**: si por la vía legacy obtuviste el contenido COMPLETO desde engram (kickoff pre-migración), escribilo al formato nuevo (`<carpeta-del-proyecto>-mala-pata/<change-name>.md`) y actualizá la observación de engram al puntero de una línea — así ese kickoff queda migrado y la próxima vez entra por la vía normal. Después seguí con ese archivo.
6. Si no se encuentra nada → **PARÁ** y pedí el identificador correcto.

**Retome de un SDD pausado en Preview**: apenas cargado el brief, chequeá `mem_search("sdd/<change-name>/state")`. Si el ítem EXACTO dice `paused-at-preview` (lo deja el gate "🛑 Detener" de `sdd-preview`) → NO re-corras las fases de planeación: hacé el preflight del Paso 2 y saltá DIRECTO al gate de Preview (Paso 3, fase 6) re-presentando el artefacto `sdd/<change-name>/preview` ya persistido. `/sdd-continue` (comando de gentle-ai) NO conoce la fase preview — el retome es por acá. Si en cambio el ítem EXACTO dice `objective-not-ready-at-preview` (bounce de objetivo desde el preview, ver Regla dura #4 y `sdd-preview`) → el QUÉ quedó abierto: **NO saltes a preview**; hacé el preflight y **re-entrá por explore/propose** para redefinir el objetivo antes de volver a avanzar.

## Paso 2 — Preflight + preparación del entorno (siguiendo el brief, sin decidir)
1. **¿Ya estás en el worktree del brief?** `git branch --show-current`. Si coincide con el branch del brief → saltá al punto 5.
2. **Confirmación de branch base — SIEMPRE preguntá antes de crear el worktree**: el brief trae la base en su frontmatter (`branch_base`), ya propuesta en el kickoff. Antes de correr el comando de arranque, **confirmala con el humano en una línea** ("worktree off `<base>` — ¿dale?"). Cualquier rama es válida con el OK — `main`/`development` (default de integración) o una feature en curso si el trabajo construye sobre ella. **No bloquees por la rama** (esa rigidez ya rompió arranques reales, ej. base `feature/caja`); lo prohibido es crear el worktree SIN confirmar. Con el OK seguís al punto 3; si el humano corrige la base, actualizá el frontmatter del kickoff antes de seguir.
3. **Si el worktree no existe o estás en otra branch** → **preparalo ejecutando el comando de arranque del brief TAL CUAL** (crea el worktree off el base branch ya validado + symlinkea `.env` y `node_modules`). Esto NO es "decidir el entorno": es ejecutar lo que el brief ya definió. Solo PARÁS si el brief no trae arranque completo (sin base branch) o si la base no pasó el guard del punto 2.
4. **Trabajá el worktree con rutas ABSOLUTAS** — `git -C <ABS-worktree> …`, paths absolutos, `npm --prefix <ABS-worktree> …`. **La cwd se resetea entre comandos**, así que NO confíes en `cd`; referenciá siempre el worktree por su ruta absoluta.
5. **Entorno ejecutable**: verificá que los untracked que el stack necesita estén resueltos en el worktree (config/secrets + dependencias — p.ej. `.env` y `node_modules`, o el equivalente del proyecto). Si falta un symlink → recreálo con el mismo comando del arranque (punto 3). No corras tests/migraciones sin esto.
6. **Init ya hecho** (lo garantiza `/mala-pata-loop`, una vez por proyecto) — chequeo de EXISTENCIA EXACTA, no exploración: `mem_search(query: "sdd-init/{project}")` devuelve varios resultados por ranking difuso (otros kickoffs/artefactos del proyecto). **Quedate ÚNICAMENTE con el ítem cuyo título/topic_key sea EXACTAMENTE `sdd-init/{project}`; el resto son falsos positivos del ranking — NO los leas ni los consideres contexto de esta tarea.** Con ese ítem exacto: `mem_get_observation` y leé `strict_tdd` (si `true`, NO NEGOCIABLE). Si el ítem exacto NO aparece → avisá al orquestador; no corras el init.
7. Cargá los skills referenciados en el brief (clean-architecture, clean-ddd-hexagonal, solid, design-patterns + condicionales) — vía el tool **Skill** (`skill: "clean-architecture"`, etc.; uno por nombre, no todos en una llamada).
8. **No explores el código para "ir resolviendo"** — solo lo mínimo que necesite la fase de Spec/Design.

## Paso 3 — CICLO SDD, una fase por vez (cada fase: resumen + PAUSA + OK)
Corré las fases EN ORDEN, **una por una** (nunca dos juntas, nunca spec y design en paralelo), reusando los skills `sdd-*` del proyecto y persistiendo cada artefacto en engram (`sdd/<change-name>/<artefacto>`). No avances de fase sin el OK del usuario.

**Mecanismo de ejecución (NO deducir de otro lado)**: cada fase se ejecuta con el tool **Agent**, `subagent_type` = el nombre entre paréntesis de esa fase (`sdd-explore`, `sdd-propose`, `sdd-spec`, `sdd-design`, `sdd-tasks`, `sdd-preview`, `sdd-apply`, `sdd-verify`, `sdd-archive`) — NUNCA cargando el SKILL.md de esa fase en el contexto actual con el tool Skill (eso ejecutaría la fase inline, sin el aislamiento de contexto que las fases de apply/verify necesitan). `model` = el mapeado para esa fase en la tabla Model Assignments de `~/.claude/skills/_shared/sdd-orchestrator-workflow.md` (la superficie lazy-loaded que CLAUDE.md referencia — la tabla NO vive en CLAUDE.md mismo). **Excepción mala-pata (esa tabla es de gentle-ai y no conoce a `sdd-preview`)**: para `sdd-preview` usá **`opus`** — es la fase adversarial de más criterio del ciclo, va en el mismo tier que propose/design, no en el default. Si la tabla no está disponible para las demás fases, usar `sonnet`.

1. **Explore** (`sdd-explore`) — investigá el **código y contexto real del worktree** para fundamentar la proposal: estado actual, approaches, riesgos, qué reutilizar. Lee el kickoff como insumo. No escribe código. Persistí `sdd/<change-name>/explore`. → **GATE**.
2. **Propose** (`sdd-propose`) — proposal de la change (intent, scope, enfoque), apoyada en el explore + kickoff. Persistí `sdd/<change-name>/proposal`. → **GATE**.
3. **Spec** (`sdd-spec`) — requisitos + escenarios (delta specs). Lee la proposal. Persistí `sdd/<change-name>/spec`. → **GATE**.
4. **Design** (`sdd-design`) — enfoque técnico y decisiones de arquitectura. **Acá se RESUELVEN, con el usuario, las decisiones abiertas del brief.** Lee proposal + spec (corre DESPUÉS de spec, no en paralelo). Persistí `sdd/<change-name>/design`. → **GATE**.
5. **Tasks** (`sdd-tasks`) — checklist ordenado y atómico (incluí **Fase 0 de componentes** si hay UI). Lee spec + design. Persistí `sdd/<change-name>/tasks`. → **GATE de aprobación del plan**. Aprobado, pasa a **Preview** (NO directo a Apply). **Hasta acá y durante Preview: CERO código, CERO migraciones, CERO setup.**
6. **Preview** (`sdd-preview`) — recorrido humano OBLIGATORIO entre tasks y apply (vía Agent, mismo mecanismo de arriba): traduce el plan a lenguaje humano y detecta duplicación / arquitectura mal pensada / flujos hardcodeados. **Precondición (Regla dura #4)**: antes de lanzar preview, confirmá que el QUÉ está cerrado — sin tarjetas rojas de objetivo abiertas ni decisiones de alcance todavía en debate. Si el objetivo sigue en discusión, NO lances preview: volvé a explore/propose. Preview asume objetivo definido; revisa el plan, no el objetivo. El propio `sdd-preview` lee tasks + design (+ spec + proposal + **el código real del worktree**) y decide en un self-assessment **cuántos revisores ciegos correr (0, 1 o 2)** — ya NO depende de que `sdd-tasks` lo recomiende. NO escribe código. Persistí `sdd/<change-name>/preview`. → **GATE OBLIGATORIO anti-sello**: SIEMPRE interactivo, **inmune al modo automático** (aunque hayan pedido "auto hasta X", esta fase FRENA igual) — corra o no audit. El orquestador presenta el gate que trae el artefacto (preguntas dirigidas + disposición por hallazgo REUSAR/REFACTOR/IGNORAR cuando hubo audit — nunca un "OK global"). **Apply queda ATADO a las dispositions aprobadas.** Recién con el preview aprobado se pasa a Apply.
6.5. **Gate de frescura del worktree** (entre preview aprobado y apply, ANTES de escribir una sola línea) — **auto-actualizar-y-avisar, NO es una pausa humana salvo conflicto real**. Entre que se creó el worktree (Paso 2) y este punto pasó toda la planeación (a veces horas o días de gates), así que la base pudo avanzar. Como las fases 1-6 **no escriben código**, el branch del worktree no tiene commits propios y actualizarlo es un **fast-forward sin riesgo**. Chequeá SIEMPRE:
   1. `git -C <ABS-worktree> fetch origin <base>` (el `<base>` es el `branch_base` del kickoff).
   2. `git -C <ABS-worktree> rev-list --left-right --count origin/<base>...HEAD` → `A` (base adelante) `B` (worktree adelante).
   3. **A=0** → worktree al día. Seguí a apply (una línea opcional: "worktree al día con `<base>`").
   4. **A>0 y B=0** (caso normal — la planeación no escribió nada) → **fast-forward automático**: `git -C <ABS-worktree> merge --ff-only origin/<base>`. **Avisá en UNA línea** ("la base `<base>` avanzó `A` commits; worktree actualizado por fast-forward") y seguí a apply. Actualizás solo, no pedís OK.
   5. **A>0 y B>0** (el worktree YA tiene commits propios — típico al RETOMAR a mitad de apply) → **única situación que FRENA**: ya no es ff, es rebase/merge con posible conflicto. Reportá y ofrecé `git -C <ABS-worktree> rebase origin/<base>`; si hay conflictos, dejá el worktree como está y esperá decisión humana. **Nunca fuerces** (`--force`, `reset --hard`, `--no-verify`).
   6. **Cruce con migraciones**: si `A>0` y este change tiene migración, una rama hermana pudo haber mergeado su migración en ese avance → dispará temprano la re-verificación de número del Paso 4.1-bis (medí git). Si tu número provisional se lo llevó otra rama, renumerá (regenerá) **ANTES de apply**, no al merge — es más barato descubrirlo acá.
   7. Tras el fast-forward, reconfirmá el entorno ejecutable (los symlinks `.env`/`node_modules` sobreviven a un ff, pero verificá que sigan resueltos) antes de arrancar apply.
7. **Apply** (`sdd-apply`) — recién ahora se escribe código. Por cada task: **STRICT TDD** (Red → Green → Refactor) + **verify 100%** (0 warnings/critical). Migración con el número **provisional** del kickoff (aún NO es final — se confirma o renumera al merge, ver Paso 4.1-bis), validada **según la convención de pruebas del proyecto** (round-trip si aplica). Persistí `apply-progress` (MERGE, no overwrite). Al cerrar cada lote/fase → resumen + PAUSA.
   - Fase 0 (si hay UI) — **OBLIGATORIO Storybook-first + Atomic Design + reuse-first** (error recurrente: se crea sin esto):
     - **ANTES de construir, auditá la librería/workshop del proyecto y listá REUSA / ADAPTA / NUEVO por componente** — reusá o componé sobre lo existente, solo creá lo que no existe.
     - Construí con **Atomic Design**: **átomo → molécula → organismo**, en ese orden; nada de organismos monolíticos. Una story por componente con sus estados/variantes.
     - ⛔ **REGLA DURA — NUNCA escribas specs de PRESENTACIÓN antes de la aprobación visual.** El **STRICT TDD de Apply NO aplica** a la Fase 0 visual. (Error real cometido en `paso-4-cycle-detail-modal-rediseno`: se escribieron 49 specs verdes sobre un layout que el humano después rechazó — trabajo a la basura y, peor, el TDD "verde" dio falsa sensación de avance.) Separá las specs en dos categorías:
       - **COMPORTAMIENTO** (qué servicio/canal se llama y con qué argumentos, validaciones, secuencia de la transacción, permisos, estado del modelo) → **sí** va con TDD antes de la aprobación visual; **sobrevive** cualquier rediseño.
       - **PRESENTACIÓN** (`data-testid` estructurales, cantidad/orden de secciones, clases CSS, medidas de viewport, presencia/ausencia de bloques en el DOM) → **PROHIBIDO escribirlas antes del OK visual**; mueren con el layout. Se escriben **después**, contra el diseño ya aprobado.
       - Test de categoría, ante la duda: *¿esta aserción sigue siendo verdad si el humano elige otro layout?* Si la respuesta es no → es presentación → va después.
     - La Fase 0 visual se construye con **stories + fixtures SOLAMENTE** (cero specs de layout) — lo más barata posible de tirar a la basura, porque para eso está el gate.
     - Corolario para **Spec/Design**: los criterios de éxito presentacionales (medidas, `data-testid`, conteo de secciones) quedan marcados como **provisionales** hasta que pase el gate visual; no los conviertas en invariantes de TDD antes de ese OK.
     - ⛔ **No ofrezcas variantes de layout que sean la misma caja con el contenido reordenado.** Si las alternativas comparten el mismo componente interno sin rediseñar, no son alternativas de diseño: son la misma pantalla. Comprometete con UNA dirección y mostrala.
     - Esperá **APROBACIÓN** antes de seguir; aprobados, el resto avanza sin más aprobaciones de componentes.
8. **Verify** (`sdd-verify`) — verificación final vs spec/tasks + checklist de **Definition of Done**. Debe pasar al **100%**. Persistí `sdd/<change-name>/verify-report`. → **GATE**.
9. **Archive** (`sdd-archive`) — solo con verify en verde: sincronizá delta specs → specs principales, cerrá la change. Persistí `sdd/<change-name>/archive-report`.

> Si en cualquier punto aparece una decisión no resuelta, **subila a la fase de Design y consultá** — no la resuelvas codeando.

## Paso 4 — Cierre: PR, revisión de pipeline/CI y limpieza (post-ciclo, una sub-fase por vez, mismo rigor de GATE que Paso 3 — nunca te quedes esperando pasivo a que el humano te lo pida, vos chequeás y anunciás)

### 4.1 — Reporte de cierre
Tras Verify (100%) + Archive, reportá estado — **Done** (evidencia: TDD verde, verify 100%) o **parcial** (qué falta y por qué). `verify-report` ya quedó en engram. Es solo resumen — seguís directo a 4.2, sin esperar OK acá.

### 4.1-bis — Migraciones: re-verificar y renumerar antes de integrar (solo si el change tocó migraciones)
Si este change creó una migración, su número era **provisional** (ver Paso 3 fase 7 y el kickoff). **Justo antes de integrar** — no al abrir el PR, sino lo más cerca posible del merge real (regla del proyecto "el primero que mergea se lo queda") — re-medí git:
1. Listá los números ocupados en la rama base Y en las ramas hermanas en vuelo (con el comando del proyecto — ej. `git ls-tree -r --name-only <rama> -- <carpeta-migraciones>`). **NO cuentes archivos en disco.**
2. **Si tu número provisional sigue libre** → confirmalo y seguí a 4.2.
3. **Si una hermana ya lo tomó (mergeó primero)** → **renumerá al próximo libre**. El CÓMO es del stack (lo sabe `sdd-init`): con un migrador de estado encadenado (journal/snapshots, ej. drizzle-kit) **NO es renombrar archivos — es regenerar** (borrar la migración + su snapshot, revertir la entrada del journal, `git pull` de la base con el ganador, regenerar contra el esquema, re-escribir el rollback pareado) y **re-correr el round-trip**. Recién con el número final y el round-trip verde seguís a 4.2.
4. Si el PR queda abierto esperando merge humano y mientras tanto mergea una hermana → **repetí este chequeo antes del merge final**. Dejalo anotado en el PR body.
No sigas a 4.2 sin el número de migración confirmado (o renumerado + round-trip verde).

### 4.2 — Destino del trabajo → **GATE OBLIGATORIO**
Apenas Verify está en verde, **PARÁ y preguntá vos mismo, sin que el humano te lo tenga que pedir** — **NUNCA asumas PR** ni sigas de largo:
> ¿Cómo cierro esto: **(a) abrir un PR** (¿hacia qué branch — `main` u otra?), o **(b) merge a una rama feature** (¿cuál, ej. `feature/caja`)?
- **(a) PR**: chequeá si **ya hay un PR activo** para este trabajo (`gh pr list` / `gh pr view`). Si existe → **consolidá ahí**, no abras un segundo (un solo PR activo). Si no → proponé y **abrí el PR solo con OK** (título, resumen, link a artefactos SDD en engram). 🚫 **No mergear/cerrar el PR sin pedido explícito** — parás en **CI verde**. (La rama NO se toca en este punto: recién se borra en el cleanup y SOLO una vez mergeada — ver 4.5.)
- **(b) Merge a rama feature**: integrá el branch del SDD en la rama feature indicada **solo con OK** del usuario. Commits con **pathspec explícito**. (Una vez hecho el merge, la rama del SDD queda integrada → se borra en el cleanup, 4.5.)
- En ambos casos: si hay conflictos o CI rojo → **PARÁ y reportá**, no fuerces.
No sigas a 4.3 sin la respuesta explícita del humano a esta pregunta.

### 4.3 — Gate RDD (pre-pr / pre-merge) → **GATE OBLIGATORIO, se dispara solo, no se espera**
Justo antes de ejecutar el `gh pr create` (u equivalente) o el merge de 4.2 — vos disparás esto proactivamente, no es algo que el humano te tenga que recordar:
1. Chequeá el kill switch: `gentle-ai review mode status --cwd <ABS-worktree>`. Si dice `disabled` (global o clone) → **saltá este paso sin preguntar nada**, seguí directo a abrir PR/merge, y anotalo como `N/A (RDD deshabilitado)` para la tabla final (Paso 5).
2. Si está `enabled` → corré `gentle-ai review status --cwd <ABS-worktree> --contract gentle-ai.review-integration/v2 --agent claude-code --next-transition` y seguí el protocolo ya definido en el CLAUDE.md global ("Native Bounded Review Orchestration": ejecutá `execute`, satisfacé `collect`, pará en `stop`) hasta llegar a un receipt terminal. **No reimplementes el protocolo acá** — este paso solo dispara el checkpoint en el momento correcto; el detalle (selección de lentes 0/1/4, consent, captura de resultados) ya vive en el CLAUDE.md.
3. Consent en riesgo medio/alto → `AskUserQuestion`, tal como especifica el contrato de "Lossless Blocking Prompts" del CLAUDE.md.
4. Si el resultado es `stop` con motivo de bloqueo (declined, findings severos sin corrección disponible) → tratalo igual que "CI rojo": **PARÁ, reportá el motivo puntual, NO abras el PR / NO mergees**.
5. Con receipt válido (o `N/A`) → seguí normalmente a abrir el PR / mergear.
No sigas a 4.4 sin un receipt terminal (o `N/A` explícito).

### 4.4 — Revisión de pipeline/CI → chequeo PROACTIVO tuyo, no pasivo
Tras abrir el PR (o mergear), **vos mismo revisás el estado del run activamente** — no esperés a que el humano te pregunte "¿y el CI?" ni asumas que quedó verde. Usá la herramienta del proyecto (GitHub Actions → `gh run list`/`gh run view`; Azure DevOps → `az pipelines runs list`/`az pipelines runs show`; GitLab → su CLI/API; Jenkins/otros → lo que corresponda). Confirmá que **TODAS las etapas** del run relevante quedan en verde antes de anunciar nada.
- Si algo está **rojo** → **PARÁ**, traé el log del paso que falló y reportá el **error exacto**. No marques "Done" con el pipeline en rojo.
- Si la change incluye **migraciones/DDL**: verificá explícitamente que el paso equivalente a `migrate` del deploy pasó (suele ser el que más se rompe). Si falla, reportá el motivo puntual (conflicto de grafo, data-migration, etc.).
- Distinguí fallo de **infra** (transitorio/reintentable) de fallo de **la change** (hay que arreglar antes de cerrar).
- Si el proyecto NO tiene CI/pipeline → dejalo explícito y seguí (no inventes uno).
No sigas a 4.5 sin confirmar vos mismo que el pipeline relevante está en verde (o que no hay pipeline).

### 4.5 — Limpieza → **GATE OBLIGATORIO, chequeo PROACTIVO tuyo — nunca esperes a que te lo pidan**
En cuanto 4.4 cierra en verde, **chequeá vos mismo el estado** (`gh pr view` del PR, o `git log` de la rama feature) — el disparador es que 4.4 dio verde, **NO** que el usuario te lo diga o te lo recuerde. Apenas confirmes PR cerrado/mergeado (o merge a la feature hecho) **anunciá explícitamente**:
> "PR/merge cerrado y CI en verde. Listo para hacer la limpieza (matar procesos, borrar worktree, borrar rama local+remota). ¿Procedo?"

Recién con el OK del humano (o si el perfil está corriendo en modo automático explícito pedido por el humano — nunca por default), **desde fuera del worktree** (repo principal/orquestador — no podés remover el worktree donde estás parado):
- **Matá procesos/servidores** en background que dejaste para este SDD (dev server, test/vitest watch, etc.).
- `git worktree remove <ABS-worktree>` + `git worktree prune` (los symlinks `.env`/`node_modules` se van con la carpeta — **no toca** el target del repo principal).
- Borrá temporales / artefactos de build que hayan quedado.
- **Borrá la rama mergeada — local Y remota — como parte ESTÁNDAR del cleanup** (una rama ya integrada es código muerto; no requiere pedido aparte más allá del OK de arriba). Local: `git branch -d <branch>` (usa `-d`, no `-D`: `-d` falla si NO está mergeada, protegiéndote). Remota: `git push origin --delete <branch>` (o `az repos ref delete` / equivalente del proyecto). ⚠️ **Excepción — NO borres la rama si la integración NO ocurrió**: PR apenas abierto sin merge, PR abandonado, o merge que no llegó a verde. En esos casos la rama tiene trabajo no integrado → pedí OK explícito por separado antes de borrar. (Si al mergear el PR ya usaste `--delete-source-branch`, la remota ya no existe — solo limpiás la local.)
- Confirmá que no quedó nada corriendo ni colgado.

## Paso 5 — Resumen final en TABLA (OBLIGATORIO)

Al terminar TODO (verify + archive + PR/merge + CI + limpieza), **cerrá SIEMPRE con una tabla de estado** — no con prosa suelta. Es lo último que ve el usuario y debe leerse de un vistazo. Formato Markdown, una fila por hito, columna izquierda = hito, columna derecha = estado con **emoji** (✅ ok · ⚠️ parcial/con nota · ❌ falló/pendiente) + **evidencia concreta** (números, ids, commits — nunca "ok" a secas).

Filas canónicas (incluí SOLO las que apliquen; NO inventes una fila que no ocurrió):

| Hito | Estado |
|---|---|
| Ciclo SDD (explore→archive) | ✅ Completo |
| Verify | ✅ PASS `<n>/<n>`, `0 CRITICAL` |
| e2e caso real `<id>` | ✅ `<obtenido>` vs `<esperado>` (delta `<%>`), `<detalle>` |
| No-regresión | ✅ `<Nf>/<Ne>` idéntico al baseline |
| Gate RDD (pre-pr) | ✅ receipt `<target_identity corto>` · lentes: `<0\|1\|4>` |
| PR `#<n>` → `<branch>` | ✅ MERGEADO (merge commit `<sha>`) |
| CI post-merge (deploy + migrate `<N>`) | ✅ VERDE (`<detalle build>`) |
| Cleanup (worktree + rama local/remota) | ✅ Hecho |

Reglas de la tabla:
- **Adaptá las filas al change real**: sin migración → quitá el `migrate <N>` de la fila de CI; sin caso e2e real → quitá esa fila; PR vs merge-a-feature → ajustá la fila de destino; proyecto sin CI → fila `CI` con `⚠️ N/A (proyecto sin pipeline)`; RDD deshabilitado (`gentle-ai review mode status` = disabled) → fila `Gate RDD (pre-pr)` con `⚠️ N/A (RDD deshabilitado)`.
- **Nada de verde falso**: si algo quedó parcial/rojo/pendiente, la fila va con ⚠️/❌ y el motivo puntual — la tabla debe reflejar la verdad del cierre (coherente con la regla de no marcar "Done" con pipeline en rojo).
- Debajo de la tabla podés agregar 1-3 líneas de follow-ups no bloqueantes si los hay; el resto del detalle ya vive en los artefactos de engram.
