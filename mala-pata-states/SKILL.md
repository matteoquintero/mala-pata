---
name: mala-pata-states
description: Dado un feature por nombre, extrae del código su(s) máquina(s) de estado (enum + guards) y las dibuja con archify (lifecycle) como HTML fiel para inspección visual humana — onboarding y detección de transiciones rotas. Read-only sobre el código del proyecto (no lo modifica); NO despacha sdd-*.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.1.0"
---

# mala-pata-states — Diagrama fiel de máquina de estados

Trigger: "máquina de estados de \<feature\>", "diagramá los estados de X", "mala-pata-states \<feature\>".

Este skill produce un diagrama, no un análisis. Es read-only sobre el código del proyecto objetivo: lee el enum de estados y las transiciones reales, y las dibuja — no modifica ni una línea del código que inspecciona. Usa workers de ODD (direct/delegated) para su propia ejecución; NO despacha agentes `sdd-*` — el preflight hook de gentle-ai no aplica acá. Rutas absolutas siempre, tanto para leer el proyecto objetivo como para invocar archify.

## Requisitos (orquestar, no reinventar)

mala-pata orquesta herramientas de comunidad — no las reimplementa. Chequeá al arrancar:

- **Obligatorias** (sin fallback — si falta, PARÁ y pedí instalarla, no arranques):
  - `archify` — renderer del diagrama (es una skill, no un binario), sin fallback. Instalar: `npx skills add tt-a1i/archify -g`.
- **Recomendadas** (con fallback — si falta, avisá en una línea y seguí degradado):
  - `codegraph` — grafo del código (anclaje y estructura). Fallback: grep/Read. Instalar: CLI npm global; init por proyecto con `gentle-ai codegraph init --cwd <repo>`.
  - `serena` — extraer enum y transiciones. Fallback: grep/Read. Instalar: `uv tool install -p 3.13 serena-agent && serena setup claude-code`.

Chequeo: `command -v <tool>` (CLI) o `claude mcp list` (MCP, p.ej. serena). Si falta una obligatoria, no sigas.

## Principios duros (no negociables)

- **FIDELIDAD sobre prolijidad**: se dibuja lo que el código HACE, no lo que debería hacer. Si una transición falta en el código, falta en el diagrama — nunca se inventan estados ni transiciones para que se vea completo. Un diagrama que miente es peor que no tener diagrama.
- **ORTOGONAL**: una máquina chica por concern, nunca una god-machine. Si un feature mezcla dimensiones (ej: estado de fulfillment + estado de pago), se separan en máquinas o columnas distintas.
- **MÍNIMO**: un estado existe SOLO si cambia qué acciones están permitidas. Todo lo demás es metadata, no estado. Los pseudo-estados (flags, timestamps, etiquetas combinadas) se degradan a metadata/cards, no se dibujan como nodos.
- **El skill NO juzga ni reporta** ("no me digas qué está roto") — produce el visual fiel; el HUMANO detecta el problema mirando. Nunca una salida tipo "la transición X está rota".
- **Alcance v1 = máquinas de estado con enum explícito** (estados viven en un enum/union y las transiciones en guards/servicios de dominio). Estado implícito o disperso queda FUERA de v1 — se documenta como extensión futura, y si un feature no tiene un enum explícito, el skill lo dice y para, en vez de adivinar.

## Fase 0 — Input + guard

La entrada es un nombre de feature (ej: `pedido`). Read-only sobre el código del proyecto objetivo — este skill no escribe ni edita nada del proyecto que inspecciona.

1. Resolvé el project root del proyecto objetivo: `git rev-parse --show-toplevel`.
2. Si CodeGraph está disponible para ese proyecto (`<project-root>/.codegraph/`), usalo para ubicar el enum de estados y sus referencias (regla global de CodeGraph: preferir `codegraph_explore` / la CLI de solo lectura antes de Grep/Read amplio). Si no está disponible, usar Grep/Read directo.
3. Si el feature no existe o no hay ningún candidato a enum de estados, decilo y parar — no hay diagrama que producir.

## Fase 1 — Extraer del código (anclado, v1 = enum explícito)

Localizá el/los enum(s) de estados del feature (ej: `PedidoEstado`) y las transiciones reales: guards, servicios de dominio, compare-and-swap sobre el campo de estado (`WHERE estado = <esperado>`), o cualquier otro mecanismo de guarda que el código use.

Para cada transición registrá: `from`, `to`, y la condición/guard/acción que la dispara (incluida cualquier nota relevante, ej. el error que lanza un guard).

Si el feature NO tiene un enum explícito de estados — decilo y PARÁ. v1 no soporta estado implícito ni disperso; queda como extensión futura, no como best-effort.

Se dibuja lo REAL: una transición que no existe en el código no se dibuja, aunque "tendría sentido" que existiera.

## Fase 2 — Ortogonal + mínimo (el filtro de calidad)

Aplicá los principios duros antes de tocar el JSON:

- ¿Hay dimensiones combinadas? (ej: estado de fulfillment + estado de pago del mismo feature) → se separan en máquinas o columnas/lanes distintas, nunca una sola máquina que las mezcle.
- ¿Algún "estado" candidato no cambia qué acciones se permiten? → es metadata: va a `cards`, no a `states`.
- ¿Hay un estado combinado/bisagra (ej: `enviado_a_caja_parcialmente`)? → se evalúa igual que en bodega: si no habilita/deshabilita acciones distintas de sus vecinos, se describe en una `card`, no se dibuja como nodo propio.

El resultado son 1..N máquinas chicas y legibles, nunca una god-machine.

## Fase 3 — Construir el JSON archify `lifecycle`

Mapeá el resultado de las fases 1-2 al esquema `lifecycle` de archify (`schema_version: 1`, `diagram_type: "lifecycle"`):

- `states[]`: cada estado real → `id`, `type` (`start` / `active` / `decision` / `waiting` / `success` / `failure`, según corresponda), `label`, `sublabel` (el valor real del enum), `lane`, `col`, y opcionalmente `step`, `tag`, `width`.
- `transitions[]`: cada transición real → `id`, `from`, `to`, `label`, `variant` (ej. `security` para rechazos, `dashed` para ramas condicionales, `emphasis` para transiciones con guard relevante), `guard`/`note` cuando aplique, `fromSide`/`toSide`, y `route` solo si hace falta.
- `lanes[]`: una lane por dimensión ortogonal o por agrupación lógica (flujo principal, ramas, terminales), según lo que salió de la Fase 2.
- `cards[]`: la metadata degradada (estados combinados, invariantes, notas de guard) y cualquier nota aclaratoria — nunca conclusiones tipo "esto está roto".
- `meta`: `title` descriptivo, `quality_profile: "showcase"`, y `viewBox` acorde al tamaño real del diagrama.

Respetá los gotchas documentados por archify para `lifecycle`: las columnas de fase `0..4` ocupan el riel principal; una columna de evento/terminal `N` en `0..2` se alinea exactamente debajo de la columna principal `N + 2`; un estado recuperable usa `type: "failure"` más una transición real de vuelta al estado activo (no un estado terminal fantasma).

### Sobre conocido-bueno de archify (construí ADENTRO, no thrashees)

El viewport que aprieta es **1440x900** (los demás — 1600/1920/2048 — entran solos). Construí dentro de este sobre para que `visual-check` pase en la PRIMERA render, en vez de iterar a ciegas:

- **`viewBox` alto = 566 fijo.** Es el piso duro de archify (rechaza cualquier valor menor con `viewBox/1 must be >= 566`). No es una palanca — no intentes bajarlo.
- **`viewBox` ancho ~1040-1100 (default 1080).** archify escala la fuente con `930 / viewBoxWidth`; anchos en esa banda mantienen la fuente proyectada `>= 6px`. Ensanchar de más baja la fuente por debajo de 6px y falla readability.
- **Máximo 3 cards.** La 4a card envuelve a una segunda fila (~+62px) y overflowea 1440x900 (`scrollHeight` 962 > 900). Si tenés más de 3 hallazgos, **fusionálos en 3 cards** (varios items por card), no agregues una 4a.
- **Presupuesto de altura:** a 1440 de ancho, `alto_SVG = 1440 x 566 / viewBoxW` (~754px con 1080) + chrome (título/toolbar/cards, ~146px) tiene que quedar `<= 900`.
- **Overflow = señal de SPLIT (principio ORTOGONAL).** Si una sola máquina no entra ni en el sobre, es evidencia de god-machine → partila en varias máquinas/diagramas (Fase 2), no la encajes a la fuerza. El fix del overflow ES el principio del skill, no una excepción.

## Fase 4 — Validar y entregar con archify

Corré estos comandos con rutas absolutas, desde el directorio de la skill archify (`/Users/matteoquintero/.agents/skills/archify`):

```bash
node bin/archify.mjs validate lifecycle <ruta-absoluta-json> --quality showcase --json
```

Debe dar `ok: true` (showcase completo: 9 checks de artefacto, 0 errores de composición, 0 warnings — un receipt con solo 4 checks es validación básica, no aceptación showcase).

```bash
node bin/archify.mjs deliver lifecycle <ruta-absoluta-json> <ruta-absoluta-html> --quality showcase --json
```

Es el comando de aceptación final: congela el JSON exacto, renderiza y chequea ese snapshot, y commitea el HTML de forma atómica.

```bash
node bin/archify.mjs visual-check <ruta-absoluta-html>
```

Debe pasar — es evidencia de navegador real sobre el HTML entregado, sin volver a renderizar.

### Playbook de remediación (si `visual-check` da `containment fail` — ordenado, sin loops ciegos)

archify solo detecta el overflow de altura en este paso lento (Chrome), no en `validate`. Si falla containment, seguí este orden exacto (no tunees al azar):

1. **Primero achicá el chrome:** fusioná a `<= 3` cards y acortá los items. Es la causa más común (la card que envuelve a una 2a fila) y no toca ni fuente ni geometría. Re-entregá y re-chequeá.
2. Si sigue y el que no entra es el SVG: **ensanchá `viewBoxW`** (baja el alto proyectado a 1440). NUNCA bajes el alto de 566 (piso duro) ni la fuente de 6px.
3. Si aún no entra en el sobre: es god-machine → **partí la máquina** (Fase 2, principio ortogonal), no sigas tuneando geometría.
4. **Una sola corrida de `visual-check` por cambio** — nunca loops a ciegas. Leé `scrollHeight` vs `innerHeight` en el `.visual-check.json` para saber cuántos px sobran antes de tocar nada.

Default de salida (si el usuario no pide otra ruta): `<project-root>/docs/diagrams/<feature>-states.{json,html}` (mismo patrón que `bodega-ferreteria-colombia/docs/diagrams/lifecycle.json`). El `.json` es versionable y editable; el `.html` es el entregable.

## Fase 5 — Cierre (sin juzgar)

Presentá:

- La ruta absoluta del HTML entregado.
- Un resumen de QUÉ se dibujó: cuántas máquinas, cuántos estados y transiciones por máquina, y qué se degradó a metadata/cards y por qué (ej: "`enviado_a_caja_parcialmente` se degradó a card porque no habilita ninguna acción distinta de `cerrado`").

Nunca un veredicto de "esto está roto" ni una lista de hallazgos — eso lo hace el humano abriendo el HTML.

Único caso de "no puedo": el feature no tiene enum explícito de estados. Ahí el cierre es decir exactamente eso y que v1 no lo soporta (extensión futura), no un intento de best-effort sobre estado implícito.

## Extensión futura (fuera de v1)

Extracción de estado implícito o disperso (flags booleanos combinados, estado reconstruido desde múltiples columnas sin enum, máquinas que solo existen en documentación) — grado-investigación, no cubierto por este skill. Si aparece un caso así, se documenta como decisión abierta para una futura iteración del skill, no se improvisa una heurística.
