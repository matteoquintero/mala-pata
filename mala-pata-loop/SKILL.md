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

## Paso 0 — Gate de vaguedad

Medí qué tan accionable es la solicitud. Le falta lo mínimo si no podés inferir **(a)** qué se quiere lograr, **(b)** dónde/qué módulo/dominio toca, **(c)** cómo se sabe que está "listo".

- **Accionable** (falta a lo sumo 1 dato menor) → procedé directo.
- **Recuperable** (falta 1–2 datos) → hacé **1–2 preguntas concretas** y esperá; no inventes alcance.
- **Demasiado vaga** (falta el objeto mismo: "mejorá la app", "hacelo mejor", sin qué/dónde) → **NO generes contexto.** Respondé exactamente:

  > **trabaje vago 🛠️** — necesito al menos: *qué* querés lograr, *dónde* (módulo/feature) y *cuándo está listo*. Con eso te armo el contexto.

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
8. **Branch base — SIEMPRE se propone y confirma con el humano** (ver `references/profiles/_base.md`): proponé la base con tu razón — default `main`/`development` (integración), u otra rama si el trabajo construye sobre una feature en curso ("el código vive en X") — y **esperá el OK antes de fijarla en el kickoff**. Cualquier rama es válida con confirmación; lo prohibido es asumirla en silencio (ej. la branch actual del cwd por default) o bloquear solo por no ser main. Esta pregunta puede ir junto con la del perfil (Paso 1.5) en una sola interacción.

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

## Paso 2 — Clasificar dominio (skills condicionales adicionales)

Las reglas transversales del método (Clean Architecture, DDD, SOLID, etc.) YA están en `_base.md`. Este paso identifica **skills adicionales condicionales** según el dominio del change:

- Si toca **UI/frontend** → cargar `heuristic-evaluation` (Nielsen) además de lo base.
- Si toca **RAG / LLM / búsqueda / embeddings** → cargar `rag-architect`, `rag-retrieval`, `hybrid-search-implementation`, `llm-app-patterns`, `prompt-engineering-patterns`, `evolutionary-metric-ranking` según corresponda.

**Init guard**: `mem_search("sdd-init/<project>")`. Si NO existe → correr `sdd-init` para detectar stack, convenciones, testing, `strict_tdd`. Si ya existe → reusá.

---

## Paso 3 — Reservar migraciones en engram (si aplica)

Si el change necesita migraciones de DB:

1. `mem_search("migrations/registry")` scope proyecto → `mem_get_observation`.
2. Si NO existe registry → bootstrap (leé el último identificador de migración del proyecto y arrancá desde ahí).
3. **Reservá** el/los próximo(s) identificador(es) para este change con `mem_save` topic_key `migrations/registry` (upsert).
4. Registrá el/los identificador(es) reservado(s) en el kickoff.

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
branch: feature/<change-name>
branch_base: main|development
worktree: <ruta absoluta sugerida>
depends_on: <change-name(s)|ninguno>
paralelizable_con: <change-name(s)|ninguno>
migrations_reserved: <identificador(es)|no aplica>
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
# Convención ÚNICA (ver _base.md): branch feature/<change-name> · worktree <ABS-repo>/.claude/worktrees/<change-name>
git -C <ABS-repo> worktree add <ABS-repo>/.claude/worktrees/<change-name> -b feature/<change-name> <branch_base>
ln -s <ABS-repo>/.env <ABS-repo>/.claude/worktrees/<change-name>/.env && ln -s <ABS-repo>/node_modules <ABS-repo>/.claude/worktrees/<change-name>/node_modules
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
