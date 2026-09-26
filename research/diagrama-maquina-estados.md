---
idea_slug: diagrama-maquina-estados
project: mala-pata
verdict: PROCEDER
created_at: 2026-09-26
next: triage
size_signal: una-unidad
---

# Research: comando mala-pata para diagramar la máquina de estados de un feature (con archify)

## Veredicto: PROCEDER
La idea es sólida y el foco quedó claro: no es "dibujar" (archify ya lo hace) sino **extraer con fidelidad** la máquina de estados real del código y renderizarla tan limpia que el humano detecte transiciones rotas de un vistazo. Buildable, con un principio de diseño duro que baja el riesgo. Una sola unidad.

## Idea cruda (lo que pediste)
> "Agregar un comando a mala-pata que, usando archify, cree la máquina de estados del feature que se le pida (ej: 'pedido' → dibuje abierto / en_revision / aprobado / entregado / etc con sus transiciones). Antes de crearlo, analicemos bien el objetivo."

## Discover

### Cómo se hace hoy + límites (con fuentes)
- La extracción **general** de máquinas de estado (FSM) desde código es grado-investigación: static analysis sobre LLVM ([FSMExtractor](https://songlh.github.io/paper/feast02.pdf)), o enfoques recientes con LLM + prompt-chaining ([Agentic FSM extraction](https://arxiv.org/html/2507.11222v1)). El patrón que estos trabajos explotan: los FSM viven en loops con transición dependiente del estado actual.
- **Límite clave**: la extracción general es difícil e imperfecta. Pero el **caso común** —estados en un enum explícito + transiciones en guards/servicios de dominio— un LLM + codegraph lo extrae bien.
- Hoy en este ecosistema se hace **a mano**: el `lifecycle` de bodega se generó leyendo el código y el `CLAUDE.md`. Límite: manual, no reproducible, se desactualiza y nadie lo nota.

### Qué existe en el código (anclaje real)
- **archify ya tiene `diagram_type: "lifecycle"`** y hay esquema probado (bodega `docs/diagrams/lifecycle.json`): `states` (id/type/label/sublabel/lane/col/step/tag/width), `transitions` (from/to/label/variant/guard/sides/route), `cards`, `lanes`. **La parte de dibujar está resuelta — no se reinventa nada.**
- archify corre `validate` / `deliver --quality showcase` / `visual-check` — ya hay pipeline de calidad determinista.
- El caso real (pedido) tiene los estados en un enum (`PedidoEstado`) y las transiciones en la lógica de dominio + guards (compare-and-swap sobre `estado`), con un estado combinado (`enviado_a_caja_parcialmente`, bisagra) que en bodega se decidió NO modelar como nodo sino describir en cards.

### Jobs-to-be-done
- "Como dev/dueño del sistema, necesito ver la máquina de estados REAL de un feature sin leer el código a mano, para **onboarding** y para **detectar transiciones rotas/faltantes** — pero quiero detectarlas YO, visualmente, no que el skill me las reporte."

## Heilmeier Catechism (7)
1. **Qué (investigación):** un comando mala-pata que, dado un feature por nombre, extrae del código su(s) máquina(s) de estado y las dibuja con archify como HTML fiel.
2. **Cómo se hace hoy + límites (investigación):** a mano (leyendo código); la extracción general es grado-investigación; el caso enum-explícito es tratable.
3. **Novedad (investigación):** reusar archify (lifecycle ya existe) + codegraph para extraer estados/transiciones del enum + guards; principio ortogonal+mínimo para que el diagrama sea legible y no un god-machine.
4. **A quién le importa (RESPONDIDO por el humano):** a vos, para **onboarding** y **detectar transiciones rotas** — uso interno, no cliente.
5. **Riesgos (investigación):** el diagrama MIENTE si la extracción es incompleta (transición implícita o estado combinado que el LLM no ve) → detectás un falso problema o se te pasa uno real.
6. **Costo (investigación):** un skill nuevo de orquestación; archify ya está; orden de magnitud = una unidad.
7. **Exámenes de éxito (RESPONDIDO por el humano):** el diagrama es **tan fiel y limpio que VOS detectás visualmente** una transición rota; el skill NO te dice qué está roto — solo produce el visual. Fidelidad + legibilidad, no análisis.

## Define — idea afinada (borrador para triage)
- **Qué** — comando mala-pata que, dado un feature por nombre, extrae del código su(s) máquina(s) de estado (enum + transiciones/guards), aplica el principio ortogonal+mínimo, y las renderiza con archify (`lifecycle`) como HTML fiel para inspección visual humana.
- **Why** — hoy hay que leer el código a mano para ver la máquina real; un diagrama fiel y limpio deja ver de un vistazo una transición rota o un estado sin salida.
- **Done (when)** — dado un feature con estados explícitos: el comando produce un HTML archify que (a) refleja los estados y transiciones REALES del código (si falta una transición en el código, falta en el diagrama — no se inventa), (b) es **ortogonal** (una máquina por concern, no god-machine) y **mínimo** (un estado existe solo si cambia qué acciones se permiten; el resto es metadata), (c) pasa `archify visual-check`; y el humano puede señalar en el diagrama una transición rota que efectivamente está rota en el código.
- **Decisiones ya tomadas (por research + el humano):**
  - Renderer = archify `lifecycle`. No se reinventa el dibujo.
  - Extracción anclada al código (enum de estados + guards/transiciones) vía codegraph/read. Se dibuja lo REAL, no lo ideal.
  - El skill **NO juzga ni reporta** ("no me digas qué está roto") — solo produce el visual fiel; el humano detecta.
  - **Principio duro: ortogonal + mínimo.** Dimensión combinada → se parte en su propia máquina/columna, o se degrada a metadata (no se inventa un god-state).
- **Decisiones abiertas (para triage/ejecución):**
  - Nombre del comando (`mala-pata-diagram-estados` / `mala-pata-fsm` / otro).
  - ¿v1 soporta solo features con **enum explícito**, o también estado implícito/scattered? (cambia el alcance y el riesgo).
  - Cómo dispone **varias máquinas ortogonales** en archify (múltiples lifecycle vs lanes/columnas).
  - Dónde se guarda el HTML por default (¿`docs/diagrams/` como bodega?).
  - Qué hace ante extracción ambigua: ¿marca el nodo/edge como "incierto" en el diagrama en vez de inventar?
- **Riesgo** — el diagrama miente por extracción incompleta. Mitigación: anclaje estricto al código + ortogonal/mínimo (legibilidad) + `visual-check` + dibujar lo real (incluidos los huecos).
- **Señal de tamaño** — una-unidad. Es un skill de orquestación (archify ya está, skill-authoring ya lo dominamos). Va a triage; tentativamente organic.

## Handoff

```
/mala-pata-triage diagrama-maquina-estados
```
