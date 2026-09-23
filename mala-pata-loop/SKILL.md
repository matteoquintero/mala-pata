---
name: mala-pata-loop
description: Reinterpreta una solicitud a términos técnicos, elige perfil de ejecución con el humano, y genera el contexto completo en un archivo markdown (carpeta hermana del proyecto, fuera del repo) para arrancar un SDD interactivo — con solo un puntero de una línea en engram. NO ejecuta el SDD — solo deja el brief listo para que otro agente lo corra.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.0.0"
---

# /mala-pata-loop — Generador de contexto para iniciar un SDD

Solicitud del usuario: **entrada entregada por el CLI**

Tu único trabajo es convertir esa solicitud en un **CONTEXTO TÉCNICO COMPLETO guardado en un archivo markdown** (fuera del repo, ver Paso 5) que otro agente consumirá para EJECUTAR un SDD.

> 🚫 **NO inicias el SDD. NO escribís código. NO creás specs/tasks/migraciones reales. NO corrés tests.**
> ✅ Solo producís el *brief* (contexto) y lo persistís en un archivo (con un puntero de una línea en engram para que se pueda buscar). Al terminar, el SDD queda **listo para arrancar**, no arrancado.

---

## Reglas base y perfiles

Este skill se apoya en dos capas de reglas — el kickoff generado **DEBE** inyectar ambas para que el ejecutor las tenga a mano:

- **Reglas base (universales)**: `references/profiles/_base.md` — invariantes del método (Fase 0, TDD, verify, principios de ingeniería) + convenciones universales de commits, branches, rutas, atribución de autoría.
- **Reglas del perfil activo**: uno de `references/profiles/{full,standard,lite,minimal}.md` — ajusta granularidad de TDD, profundidad de verify, fusión spec+design, reutilización de explores, gate humano de Fase 0.

**Herramientas del stack, convenciones específicas del proyecto y contratos concretos** NO viven aquí — los detecta `sdd-init` y viven en engram como contexto del proyecto (`sdd-init/<project>`) o en el kickoff del change.

---

## Paso 0 — Gate de vaguedad + Definition of Ready (DoR liviano)

Antes de reinterpretar nada, medí si la solicitud está **lista para entrar al ciclo** (Definition of Ready). No es una fase nueva ni un artefacto aparte — es este mismo gate, afilado. La idea, tomada de prácticas probadas (Example Mapping / "Three Amigos" y el criterio *Testable* de INVEST), es simple: **un objetivo mal definido NUNCA debe arrancar el ciclo** — es infinitamente más barato pararlo acá que descubrirlo en preview.

### Dos chequeos de readiness

**1. Tarjetas rojas (preguntas del QUÉ sin responder).** Una tarjeta roja es cualquier pregunta abierta sobre *qué se quiere* — NO sobre *cómo se implementa* (eso se resuelve en Design, no acá). Ejemplos de rojas: "¿esto incluye también X?", "¿el objetivo es A o B?", "¿qué pasa con el caso Y?". Regla:
- **0 rojas** → el QUÉ está claro, seguí.
- **1–2 rojas** → hacé esas preguntas concretas y esperá (nivel "Recuperable" de abajo). No inventes la respuesta.
- **3+ rojas, o una sola roja que cambia el objetivo entero** → el objetivo NO está definido. NO generes contexto: devolvé el pedido a definición (respondé como "Demasiado vaga", listando las rojas). Meter esto al ciclo con las rojas abiertas es exactamente lo que después hace que el humano y el preview terminen debatiendo el objetivo en la fase equivocada.

**2. DoD testeable (criterio *Testable* de INVEST).** El "cuándo está listo" tiene que poder escribirse como algo **verificable**, no como un deseo. Test rápido de cada criterio: *¿alguien que no seas vos podría decir objetivamente si se cumplió o no?*
- "que funcione bien", "que quede prolijo", "que sea rápido" → NO testeable → es una tarjeta roja (falta el criterio real).
- "que el endpoint responda <200ms en p95", "que el usuario pueda filtrar por fecha y vea el resultado sin recargar" → testeable → OK.
- Si el "listo" no se puede volver testeable ni preguntando 1–2 cosas → tratalo como objetivo no definido (Demasiado vaga).

### Resolución (los tres niveles de siempre, ahora con los dos chequeos adentro)

- **Accionable** — 0 rojas y DoD testeable (o falta a lo sumo 1 dato menor) → procedé directo al Paso 1.
- **Recuperable** — 1–2 rojas, o el DoD se vuelve testeable con 1–2 preguntas → hacé **esas preguntas concretas** y esperá. No inventes alcance.
- **Demasiado vaga** — falta el objeto mismo ("mejorá la app", "hacelo mejor"), o 3+ rojas, o el "listo" no se puede volver testeable → **NO generes contexto.** Respondé exactamente:

  > **trabaje vago 🛠️** — necesito al menos: *qué* querés lograr, *dónde* (módulo/feature) y *cuándo está listo* (en criterios verificables, no "que quede bien"). [Si hay tarjetas rojas concretas, listalas acá como bullets.] Con eso te armo el contexto.

  Y parás ahí. No reinterpretes ni adivines.

---

## Paso 1 — Reinterpretar a términos técnicos

1. Detectá el **proyecto activo** (la herramienta de memoria disponible o el cwd) y leé su arquitectura (`CLAUDE.md`, `ARCHITECTURE.md` o equivalentes).
2. `mem_search` con keywords de la solicitud (y `mem_get_observation` para lo relevante). Reusá decisiones/convenciones existentes.
3. Explorá lo mínimo del código para aterrizar la reinterpretación (grep/lectura). No edites nada.
4. Reescribí la solicitud como **objetivo técnico**: Objetivo, Problema/causa raíz, Alcance IN, Alcance OUT, Criterios de éxito medibles, `change-name` en kebab-case.
5. **Idempotencia**: `mem_search("sdd/<change-name>/kickoff")`. Si ya existe uno igual/parecido → ofrecé actualizar o cambiar nombre.
6. **Guard de tamaño / troceo**: un SDD = un objetivo coherente. Si abarca varios, recomendá trocear en N SDDs (con grafo de dependencias) y generá solo el primero.
7. **Conflicto en vuelo**: `git worktree list` + branches activos. Si hay solape → avisá y confirmá antes de seguir.
8. **Branch base + tipo de rama — SIEMPRE se proponen y confirman con el humano** (ver `references/profiles/_base.md`):
   - **Base**: proponé con tu razón — default `main`/`development` (integración), u otra rama si el trabajo construye sobre una feature en curso ("el código vive en X"). Cualquier rama es válida con confirmación; lo prohibido es asumirla en silencio o bloquear solo por no ser main.
   - **Tipo de rama**: aconsejá el prefijo convencional según QUÉ es el cambio (`feature/` funcionalidad nueva, `fix/`/`bugfix/` corrección, `hotfix/` urgencia prod, `refactor/`, `chore/`, `docs/`, `release/`) y proponé el nombre completo `<tipo>/<change-name>`. **Nunca `sdd/...`**. Ej.: un fix de bug → propuesta `fix/<change-name>`; una feature nueva → `feature/<change-name>`.
   - **Esperá el OK** antes de fijar `branch:` y `branch_base` en el kickoff. Estas dos confirmaciones pueden ir junto con la del perfil (Paso 1.5) en una sola interacción.

---

## Paso 1.5 — Elegir perfil de ejecución (gate humano)

Estimá el **tamaño** del change y **proponé un perfil** basado en:

- Cuántos containers, services, tipos, tests toca.
- Si el módulo ya se exploró recientemente (existe `sdd/<...>/explore` en engram del mismo módulo).
- Si hay componentes UI nuevos genuinos (no solo adaptaciones).
- Si hay contrato BE nuevo (endpoints, migraciones, cambio de shape).
- Riesgo de regresión en flujos críticos.

Los 4 perfiles disponibles:

| Perfil | Cuándo | Costo aprox |
|---|---|---|
| **FULL** | Change L, primer paso en el módulo, contrato BE nuevo, riesgo alto | ~500K tokens |
| **STANDARD** | Change M típico, módulo conocido, aditivo sobre contrato existente | ~250K tokens |
| **LITE** | Change S/M en módulo caliente, adapta atoms/molecules | ~120K tokens |
| **MINIMAL** | Fix chico, refactor mecánico, migración de tipo | ~70K tokens |

Presentá la propuesta al humano con **la función de preguntas interactiva disponible en el CLI**:

- **Pregunta**: "¿Qué perfil usamos para este SDD?"
- **Opciones**: los 4 perfiles con descripción corta (una línea cada uno).
- **Recomendación** (etiquetá con "(Recomendado)" y ponelo como primera opción): la que corresponde a tu estimación.
- En el reasoning, escribí una línea corta explicando **por qué recomendás ese perfil** (ej: "módulo `X` ya explorado esta semana, sin componentes nuevos, cambio aditivo → LITE").

**No continúes** hasta que el humano confirme. Si elige "Other", tomá su respuesta como el perfil (validá que sea uno de los 4).

---

## Paso 2 — Elegir skills SEGÚN EL OBJETIVO (enfocado, no una lista fija)

El ejecutor va a cargar exactamente los skills que este kickoff liste — así que elegilos **por el Alcance IN del objetivo**, no "por si acaso". Menos y precisos > muchos y genéricos (un set inflado hace al agente más lento y gasta tokens sin mejorar el resultado).

### Base del método (motor de ingeniería)

- **Siempre** (aplican a cualquier código): `clean-architecture`, `solid`.
- **Si el objetivo toca lógica de backend/dominio** (no para un cambio puramente visual/estático): + `clean-ddd-hexagonal`, `design-patterns`.

### Condicionales por dominio — elegí SOLO las señaladas por el objetivo

| Señal en el objetivo (Alcance IN) | Skills a cargar |
|---|---|
| **DB**: schema, migración, query, modelo de datos, índices | `database-design` |
| **UI/frontend**: pantalla, componente, formulario, flujo de usuario | `ui-ux-pro-max`, `heuristic-evaluation` |
| **Diseño visual** nuevo / rediseño / branding / "que no parezca IA" | `frontend-design`, `impeccable` |
| **Color / tokens / paletas** | `color-expert` |
| **Animación / micro-interacción / transición / scroll** | `motion-design` (+ `gsap-*` / `threejs-*` **solo si el stack los usa**) |
| **Diagramas** de arquitectura/flujo/estados | `archify` o `diagram-design` |
| **Charts / dashboards / data viz** | `dataviz` |
| **Docs** para humanos (runbook, guía) / doc de prueba o de cliente | `cognitive-doc-design` / `mala-pata-walkthrough` |
| **RAG / búsqueda / embeddings** | `rag-architect`, `rag-retrieval`, `hybrid-search-implementation` |
| **App LLM / agentes / prompts / tools** | `llm-app-patterns`, `prompt-engineering-patterns`, `ai-engineer`, `multi-agent-patterns`, `tool-design` |
| **Evaluación de modelos / LLM-judge / métricas** | `advanced-evaluation`, `evaluation`, `evolutionary-metric-ranking` |
| **Memoria de agentes / persistencia cross-sesión** | `memory-systems` |
| **Diseño de sistema grande / build-vs-buy / descomposición** | `software-architect` |
| **Seguridad / revisión de vulnerabilidades** | `security-review` |
| **Librería/framework/API** (setup, versión, sintaxis) | `context7` (ya es regla global — nombralo en el kickoff si es central al objetivo) |

### Reglas de selección (no negociables)

1. **Por objetivo, no por reflejo**: si el Alcance IN no lo menciona, no lo cargues. Ej.: un fix de query NO carga `ui-ux-pro-max`; un rediseño de pantalla NO carga `rag-*`.
2. **Techo ~3-4 condicionales.** Si te salen más, probablemente el objetivo es demasiado grande → trocealo (Paso 1.6), no cargues de todo.
3. **Cada skill elegido va en el kickoff** (sección "Skills condicionales") **con UNA línea de por qué** (qué parte del objetivo lo justifica). El ejecutor carga esa lista literal.
4. **Solo skills que EXISTAN** en la sesión (mirá `<available_skills>`); nunca inventes un nombre. Algunos son de plugin → usá el nombre `plugin:skill` tal como aparece en el listado. Los stack-specific (`gsap-*`, `threejs-*`, `go-testing`, `neon-postgres`) solo si `sdd-init` confirma que el stack los usa.

**Init guard**: `mem_search("sdd-init/<project>")`. Si NO existe → correr `sdd-init` para detectar stack, convenciones, testing, `strict_tdd`. Si ya existe → reusá (es lo que te dice qué stack-specific aplican).

---

## Paso 3 — Número de migración: provisional al autor, final al merge (si aplica)

Si el change necesita migraciones de DB, **NO reserves un número como lock**. La fuente de verdad de los números YA tomados es **git, no engram** — un registry de reserva es un lock que las ramas largas no respetan y que además driftea (se lo vio decir "próximo libre 0071" cuando el real era 0003). En cambio:

1. **Medí git, no un registry**: mirá qué números ocupan la rama base Y las ramas hermanas en vuelo — con el comando del proyecto para listar migraciones (ej. `git ls-tree -r --name-only <rama> -- <carpeta-de-migraciones>`; la carpeta y el esquema exactos los sabe `sdd-init`). **Nunca infieras el próximo contando archivos en disco** (la numeración puede no ser contigua).
2. **Tomá el próximo libre como PROVISIONAL**: es el número con el que vas a escribir el archivo y correr el round-trip, pero **no es final** — si otra rama hermana mergea antes, este change renumera al integrar (ver `/mala-pata-loop-start`, Paso 4.1-bis). Regla del proyecto: "el primero que mergea se lo queda".
3. **Registralo en el kickoff como provisional-en-disputa, no como reserva**: en `migrations_reserved` del frontmatter poné el número provisional + la nota "final al merge; 1° que mergea se lo queda; re-verificar contra hermanas justo antes del merge". Si hay varias ramas peleando el mismo número, listalas.
4. **El CÓMO renumerar es del stack, no de acá**: si el proyecto usa un migrador con estado encadenado (journal/snapshots, ej. drizzle-kit), renumerar **NO es renombrar archivos — es regenerar**. Ese detalle vive en `sdd-init/<project>` / el `CLAUDE.md` del repo, no en estas reglas.

Si no necesita migraciones, dejalo explícito ("no aplica") en el kickoff.

---

## Paso 4 — Construir el kickoff

El kickoff es un **archivo markdown**, no una entrada de engram — sin límite práctico de longitud, así que sé tan detallado como el change lo pida. El orden de las secciones está pensado a propósito, no es solo estético: **el contexto/background va primero, el pedido/instrucción va al final**. Es la práctica documentada por Anthropic para prompts largos que mezclan referencia + instrucción — "queries at the end can improve response quality by up to 30%, especially with complex, multidocument inputs" ([Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)). No reordenes las secciones aunque te parezca más prolijo de otra forma.

Armá el brief con esta estructura, **INYECTANDO** los MDs de reglas:

```markdown
---
change_name: <change-name>
profile: <PERFIL>
project: <project>
branch: <tipo>/<change-name>   # tipo confirmado (feature|fix|hotfix|refactor|chore|docs|release) — nunca sdd/
branch_base: main|development
worktree: <ruta absoluta sugerida>
depends_on: <change-name(s)|ninguno>
paralelizable_con: <change-name(s)|ninguno>
migrations_reserved: <número(s) provisional(es) + "final al merge; 1° que mergea se lo queda"|no aplica>
sdd_preflight:              # recomendaciones que el runner (loop-start) usa como default de la pregunta canónica del hook
  pace: interactive        # interactive|automatic — FULL/STANDARD => interactive; LITE/MINIMAL pueden ser automatic
  artifacts: engram        # engram|openspec|both — default engram para este usuario
  pr_strategy: ask-on-risk # ask-on-risk|single-pr|auto-chain — default ask-on-risk
created_at: <ISO 8601>
---

# Kickoff: <change-name>

<!-- ===== CONTEXTO — leer esto antes que el pedido. Es material de referencia. ===== -->

## Reglas del método
- Base (universales): `references/profiles/_base.md`
- Perfil activo (**<PERFIL>**): `references/profiles/<perfil>.md` — razón: <una línea corta explicando por qué este perfil>. Costo orden de magnitud: ~<N>K tokens.

## Contexto del proyecto
`sdd-init/<project>` — engram #<id> (stack, testing, convenciones ya detectadas; no las repitas acá).

## Comando de arranque
El comando COMPLETO y ejecutable que crea el entorno (worktree off la branch base + symlinks de config/deps del stack). `loop-start` lo ejecuta TAL CUAL, sin decidir nada — si falta, el ejecutor PARA (Regla dura #2 de loop-start).

```bash
# Branch = el <tipo>/<change-name> confirmado (frontmatter `branch:`) · worktree dir = <change-name> (sin prefijo) · nunca sdd/
git -C <ABS-repo> worktree add <ABS-repo>-worktrees/<change-name> -b <branch> <branch_base>
ln -s <ABS-repo>/.env <ABS-repo>-worktrees/<change-name>/.env && ln -s <ABS-repo>/node_modules <ABS-repo>-worktrees/<change-name>/node_modules
# (ajustar symlinks al stack real del proyecto)
```

## Contrato del change
- Endpoints, shapes, tipos, migraciones (si BE tiene entrega asociada).
- Refs a artefactos previos (kickoffs BE, decisiones en engram).

## Reinterpretación técnica
- Objetivo:
- Problema / causa raíz:
- Alcance IN:
- Alcance OUT:

## Arquitectura y capas afectadas
- BCs/capas del proyecto + refs a ARCHITECTURE.md.

## Skills condicionales adicionales (Paso 2)
- Lista de skills cargados según dominio (UI, RAG, LLM, etc.).

## Riesgos / decisiones abiertas
- Lista para resolver dentro del SDD (Design es donde se resuelven con el humano, no acá).

<!-- ===== EL PEDIDO — va al final a propósito. Es la instrucción que el ejecutor ejecuta. ===== -->

## Plan de fases alto nivel
- Fase 0 (si toca UI): audit REUSA/ADAPTA/NUEVO + Storybook + gate humano según perfil.
- Fase 1..N: objetivos coherentes, NO tasks (esas las produce `sdd-tasks`).

## Definition of Done
Criterios verificables, no bullets vagos — usá Given/When/Then para el comportamiento observable, agregá lo procedural del método debajo:

- [ ] Given <estado inicial>, When <acción del usuario/sistema>, Then <resultado observable y verificable>.
- [ ] (repetí un ítem por criterio de éxito real del pedido — el que definiste en "Reinterpretación técnica")
- [ ] Todas las tasks con TDD verde según granularidad del perfil.
- [ ] Verify pasa según profundidad del perfil.
- [ ] PR abierto contra la branch base, sin push directo a integración.
- [ ] Kickoff referenciado en el PR body (ruta del archivo — ver Paso 5).
```

El kickoff DEBE incluir el frontmatter completo y el bloque "Reglas del método" con las rutas a los MDs — el ejecutor los lee al arrancar. No comprimas la Definition of Done para que "quepa": ya no hay presupuesto de caracteres, usá el espacio que el change necesite.

`sdd_preflight` son solo RECOMENDACIONES — NO satisfacen el hook de preflight de gentle-ai (que exige un `AskUserQuestion` real y en vivo en la sesión del runner); `mala-pata-loop-start` las lee para pre-llenar el texto de recomendación de la pregunta canónica obligatoria del hook. Derivá `pace` del perfil: FULL/STANDARD → `interactive`; LITE/MINIMAL pueden ir `automatic`.

---

## Paso 5 — Persistir y responder (SOLO la ruta del archivo)

El kickoff vive en un **archivo, no en engram** — así nunca se sube al repo del proyecto por accidente, y no tiene el límite práctico de longitud de una observación de engram. Esto es específico del kickoff: el resto del ciclo (explore, propose, spec, design, tasks, preview, apply-progress, verify-report, archive-report) sigue persistiendo en engram exactamente como siempre — no lo toques.

1. **Ubicación — carpeta hermana del proyecto, NUNCA dentro del repo**: `<carpeta-del-proyecto>-mala-pata/`, al mismo nivel que la carpeta del proyecto. Ejemplo: proyecto en `/ruta/a/mi-proyecto` → kickoffs en `/ruta/a/mi-proyecto-mala-pata/<change-name>.md`. Creá la carpeta (`mkdir -p`) si no existe.
2. Escribí el kickoff completo del Paso 4 en `<carpeta-hermana>/<change-name>.md`.
3. **Puntero liviano en engram** (solo para que `mem_search`/radar lo sigan encontrando — la idempotencia del Paso 1 punto 5 depende de esto): `mem_save` con `topic_key: "sdd/<change-name>/kickoff"`, `type: "architecture"`, contenido de **una sola línea**: `Kickoff en archivo: <ruta absoluta>`. No dupliques el contenido del kickoff acá — el archivo es la única fuente de verdad.
4. Si reservaste migraciones, confirmá que el registry quedó actualizado.
5. **Tu respuesta al humano es ÚNICAMENTE la ruta absoluta del archivo** — sin resumen, sin prosa, sin checklist. Formato exacto:

   ```
   <ruta absoluta del archivo .md>
   ```

   Una sola línea. Punto.

**Únicas excepciones** (cuando la respuesta NO es solo la ruta):
- Gate de vaguedad → responder `trabaje vago 🛠️` (Paso 0).
- Idempotencia / conflicto en vuelo → una línea de aviso + la pregunta, antes de crear.
- Paso 1.5 y Paso 1.8 → la función de preguntas interactiva disponible en el CLI para elegir perfil y confirmar la branch base (idealmente en UNA sola interacción; son las únicas preguntas permitidas antes del kickoff).
- Engram no disponible para el puntero → el archivo ya es la fuente de verdad, seguí igual; avisá en una línea que el puntero no quedó guardado (afecta la idempotencia futura, no el kickoff en sí).
