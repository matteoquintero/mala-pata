---
name: mala-pata-roadmap
description: >
  Capa de planeación por ENCIMA de los carriles (organic/loop), ruteada por /mala-pata-triage.
  Recibe UN objetivo grande, lo analiza, investiga cómo se resuelve (web + cómo lo hacen los
  grandes), lee el .codegraph/ del proyecto para anclarlo al código real, hace preguntas si falta
  contexto, y lo descompone en un DAG de fases unit-sized (cada fase = corte vertical shippeable
  que entra en UNA unidad: un organic o un loop). A cada fase le asigna una RUTA TENTATIVA
  (organic o loop:PERFIL) como acercamiento — pero triage es el que decide al llegar, con la info
  ya actualizada por las fases previas. Escribe un roadmap .md versionable en el repo. NO ejecuta,
  NO corre ningún carril, NO toca código: solo produce el mapa de fases que después vos pasás una
  por una a /mala-pata-triage.
  Trigger: "roadmap de <objetivo>", "descomponé este objetivo grande", "armá el plan de fases",
  o cualquier objetivo demasiado grande para una sola unidad.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "2.1.1"
---

# /mala-pata-roadmap — objetivo grande → DAG de fases unit-sized (organic o loop)

Objetivo del usuario: **entrada entregada por el CLI**

Tu trabajo: convertir un objetivo GRANDE en un **DAG de fases**, donde cada fase es tan chica que
entra en **UNA unidad** — un `/mala-pata-organic` o un `/mala-pata-loop`. A cada fase le asignás una
**ruta tentativa** (organic o loop) como acercamiento. Producís un `.md` con ese roadmap y **nada
más** — no escribís código, no corrés ningún carril, no aplicás. Después el humano toma cada fase y
se la pasa a `/mala-pata-triage`, que decide el carril final con la info del momento.

> ⛔ **Regla dura #1 — NO ejecutás nada.** Ni código, ni migraciones, ni corrés `/mala-pata-triage`,
> `/mala-pata-loop` ni `/mala-pata-organic`. Tu único entregable es el roadmap `.md` (+ un puntero en
> engram). El DAG es un plan, no una orden de implementar.
>
> ⛔ **Regla dura #2 — si el objetivo YA entra en UNA unidad, NO inventes fases.** Si al analizarlo
> ves que es un cambio que cabe en un solo organic o un solo loop, **PARÁ y redirigí a
> `/mala-pata-triage`** — él decide el carril. Este skill es solo para objetivos que NO caben en una
> sola unidad. Sobre-descomponer algo chico es el anti-patrón que este skill debe evitar.
>
> 🧭 **Regla dura #3 — la ruta por fase es un PRONÓSTICO, no un compromiso.** Clasificás cada fase
> como organic o loop con tu mejor lectura de HOY, pero **triage re-decide al llegar** (ver Paso 4-bis):
> las fases previas resuelven incógnitas, así que una fase pronosticada loop puede volverse organic
> (o al revés). Vos pronosticás; triage manda.

## Paso 0 — ¿Amerita roadmap? (gate de tamaño + vaguedad)

- **¿Es lo bastante grande?** Si el objetivo cabe en UNA unidad (un organic o un loop) → Regla dura
  #2 (redirigí a `/mala-pata-triage`).
- **¿Es lo bastante claro para descomponer?** Necesitás inferir **qué** se quiere lograr, **para
  quién/dónde** (módulo/dominio) y **cómo se ve el éxito**. Si falta el objeto mismo ("mejorá la
  app") → pedí lo mínimo y esperá; no inventes alcance.
- Recuperable (falta 1-2 datos) → hacé preguntas concretas y esperá. Este es el gate de preguntas.

## Paso 1 — Definir el ESTADO DESEADO: las dimensiones del objetivo completo

El objetivo del roadmap NO es cubrir lo que el humano LISTÓ — es cubrir lo que el objetivo NECESITA.
La solicitud casi siempre queda incompleta; tu trabajo es cerrar el hueco. **Sesgo: mejor que sobre,
no que falte.** Hay dos errores simétricos a evitar:

⛔ **Encoger a lo fácil de medir** — anclarte al primer inventario que el código deja grepear (una
métrica, un report) y planificar solo esa faceta.
⛔ **Cubrir solo lo que el humano dijo** — la solicitud es incompleta por default; si no buscás lo que
falta, el humano lo termina descubriendo en producción.

Definí el **estado deseado** (el objetivo COMPLETO) uniendo TRES fuentes:

1. **Lo que el humano dijo** — releé el objetivo literal, listá cada faceta. ¿Qué "tipos de cosa"
   abarca? ¿Qué implica "todo / cualquier / completo"?
2. **Lo que el DOMINIO necesita** (investigación externa, Paso 2.3) — el **feature-set canónico** de
   cómo equipos maduros resuelven este tipo de objetivo. Es la red anti-olvido (checklist de dominio,
   estilo ISO/IEC 25010 para software). En **dos niveles** (ver Paso 4-ter): *adyacente-implicado* (lo
   que completa o implica directamente lo pedido) vs *dominio amplio* (el resto del universo del dominio).
3. **Lo que la doc de intención del repo YA anticipa** — leé la documentación de arquitectura/intención
   que exista, **esté donde esté** (`CLAUDE.md`, `ARCHITECTURE.md`, READMEs, RFCs, notas de diseño). NO
   asumas una carpeta fija; si el repo tiene pendientes documentados, suelen ser huecos que el humano olvidó.

Expresá el objetivo también como **jobs-to-be-done** ("como <usuario>, necesito <trabajo> para <beneficio>"):
cacha huecos de cara al usuario que la lista de features no muestra (p.ej. una pantalla que hace falta y
nadie nombró).

**Chequeo MECE + regla del 100%**: el set de dimensiones debe ser *mutuamente excluyente* (sin solape) y
*colectivamente exhaustivo* (cubre TODO el objetivo, sin huecos). Si no es exhaustivo, faltan dimensiones
— seguí buscando. Este es el chequeo que fuerza completitud.

Esta lista de dimensiones es el **contrato de cobertura** contra el que se mide el DAG (Paso 5). Si el
objetivo resulta enorme, NO asumas que va todo en un roadmap: en el gate (Paso 5) ofrecés scope. Vos no
acotás en silencio.

## Paso 2 — Inventariar CADA dimensión + investigar + anclar al código real

En paralelo, sin escribir nada. **Inventariá TODAS las dimensiones del Paso 1, no solo la fácil:**

1. **Proyecto activo**: detectá el repo/cwd y leé su arquitectura (`CLAUDE.md`, `ARCHITECTURE.md`,
   o equivalentes). `mem_search` por trabajo previo relacionado.
2. **.codegraph/ + inventario por dimensión**: si el proyecto tiene índice, usá `codegraph_explore`
   (o los comandos read-only de CodeGraph) para mapear módulos, símbolos y dependencias. Corré un
   inventario por CADA dimensión del Paso 1 (qué existe ya, qué está crudo, cuánto), no solo por la
   que grepeás en un comando. Si una dimensión no se deja medir por código (p.ej. inventario de un
   tipo de artefacto que no tiene marca única), decilo explícito y estimá — no la borres del mapa.
   Si no hay `.codegraph/`, mapeá con Read/Grep/Glob lo mínimo para entender las costuras reales.
3. **Investigación externa** (WebSearch/WebFetch): el **feature-set canónico** del dominio — cómo lo
   resuelven equipos maduros, qué patrones/errores conocidos hay. Separalo en **dos niveles**:
   *adyacente-implicado* (completa/implica lo pedido) y *dominio amplio* (el resto). **Anclá lo que traés
   a TU código** — la best-practice que ignora lo que ya existe no sirve (reuse-first, igual que preview).
4. **Preguntas**: si después de esto quedan decisiones abiertas que cambian la forma del DAG —
   incluida cualquier dimensión que no pudiste inventariar bien — preguntá ANTES de descomponer
   (no la resuelvas adivinando).

## Paso 3 — Pase de arquitectura ANTES de descomponer

Antes de cortar en fases, definí las **costuras reales** por donde va a partir el trabajo
(interfaces, módulos, límites de datos), ancladas al `.codegraph/` del Paso 1. Esto es lo que hace
que las fases salgan por bordes limpios y no por temas arbitrarios — la lección de los planners que
descomponen sin visión de arquitectura y terminan con fases que no son shippeables solas.

## Paso 4 — Descomponer a un DAG de fases

Producí el grafo de fases con estas reglas (todas, no opcionales):

- **El DAG debe CUBRIR todas las dimensiones del Paso 1**, no solo la más fácil de medir. Cada
  dimensión aparece cubierta por al menos una fase, o queda explícitamente marcada como diferida /
  fuera de scope (para el gate del Paso 5). Nunca dejes una dimensión afuera sin nombrarla.

- **Cada fase es un corte VERTICAL shippeable** — una rebanada end-to-end que deja el sistema
  funcionando, no una capa horizontal ("toda la DB", "toda la UI"). Si la fase no se puede mergear
  y quedar sola en verde, no es una fase válida.
- **Cada fase recibe una RUTA TENTATIVA, con la frontera de triage** (la misma que usa
  `/mala-pata-organic`):
  - ¿Se puede enunciar **Qué + Done + Decisiones** de la fase, dado lo que sus dependencias ya van a
    haber resuelto cuando llegue su turno? → tentativa **organic**.
  - ¿Falta **diseño / decisión de arquitectura sin resolver** en ese punto? → tentativa **loop:PERFIL**
    (FULL/STANDARD/LITE/MINIMAL).
  - Para cada fase-loop, anotá **cuál decisión abierta** la hace loop — es exactamente lo que triage
    va a re-chequear al llegar (si ya se resolvió, la fase pasa a organic).
- **El TECHO duro del tamaño es "entra en UNA unidad".** Un `loop:FULL` es el techo de una
  fase-loop; una fase-organic entra si el cambio ya es especificable. **Si una fase sería más grande
  que un FULL → se PARTE.** Sin excepción.
- **El disparador del split es la COMPLEJIDAD / AISLAMIENTO DE CONTEXTO, no las líneas.** La prueba
  de "¿entra en una unidad?" es: ¿el contexto de esta fase se aísla limpio del resto? Si para entender
  o hacer la fase necesitás cargar el contexto de media otra fase, todavía está demasiado grande.
- **Cada nodo lleva un borde EXPLÍCITO IN / OUT** — qué entra y qué queda afuera — para que dos
  fases no se pisen ni dupliquen trabajo.
- **Dependencias como DAG**: cada fase declara de qué otras fases depende. El grafo no tiene ciclos.
  Da el orden topológico sugerido (qué se puede hacer en paralelo, qué es secuencial).
- **Anti-sobre-descomposición**: la MENOR cantidad de fases posible con la condición de que cada una
  entre en una unidad. No 40 micro-fases; no una fase gigante. Si dudás entre 3 fases grandes o 8
  chicas, elegí el mínimo que respete el techo (loop:FULL) y el aislamiento de contexto.

## Paso 4-bis — Ruta tentativa vs decisión de triage (contrato)

La ruta que asignás a cada fase (organic o loop) es un **acercamiento con la info de HOY**, no un
compromiso. La verdad se decide al EJECUTAR:

- Al avanzar el roadmap, **cada fase se pasa por `/mala-pata-triage`** (no directo a un carril).
  Triage aplica su gate con la info ACTUAL del repo y de las fases ya completadas.
- Como las fases previas **resuelven incógnitas** (una decisión de arquitectura tomada en la fase A
  puede cerrar la que tenía abierta la fase D), una fase pronosticada **loop** puede llegar como
  **organic** — o una que parecía organic puede revelar complejidad y volverse **loop**.
- Por eso cada fase-loop declara **la decisión abierta que la hace loop**: es exactamente lo que
  triage re-chequea. Si esa decisión ya está resuelta al llegar, triage la manda a organic.
- **El roadmap pronostica; triage manda.** No trates la ruta tentativa como fija ni saltees triage
  "porque el roadmap ya dijo loop".

## Paso 4-ter — Gap analysis: validar que el DAG cubre el objetivo completo

El roadmap **SOBRE-descubre y propone; el humano RECORTA** en el gate. Nunca al revés (que el humano
descubra lo que faltó). Hacé el análisis de brecha:

- **Estado deseado** (Paso 1: humano + dominio + doc de intención, MECE) **vs estado actual** (lo que el
  código ya resuelve, medido en Paso 2 con codegraph) = **el gap**. El gap es lo que el roadmap tiene que
  cubrir con fases.
- Toda dimensión del estado deseado que el humano **NO pidió** pero el objetivo implica → va marcada como
  **propuesta-extra** (no como algo que decidiste solo). **Nunca la agregues en silencio ni la descartes en
  silencio**: va al gate marcada.
- **Dos niveles de propuesta** (amplitud de la fuente de dominio, resuelta):
  - **Nivel 1 — núcleo + adyacente-implicado**: dimensiones que el objetivo NECESITA o implica
    directamente → se vuelven **fases candidatas** en el DAG (marcadas propuesta-extra si el humano no las
    pidió).
  - **Nivel 2 — dominio amplio**: el resto del feature-set canónico del dominio → **NO infla el DAG**; se
    lista **compacto como checklist** ("existe en el dominio, este roadmap NO lo cubre") para que el humano
    marque si algo sube a fase. No se esconde nada, pero no se vuelve fase por default.
- Aprovechá lo que el código YA tiene para habilitar más de lo que el humano imaginó (p.ej. infra ya
  instalada que abre una capacidad): eso también es gap que vale proponer.

## Paso 5 — Gate de cobertura + gate humano del DAG

Antes de pedir OK, validá **MECE** sobre las dimensiones (sin solapes, sin huecos) y mostrá la **tabla de
cobertura OBLIGATORIA**: **cada eje del estado deseado (Paso 1) aparece en la tabla con EXACTAMENTE UN
estado.** Ningún eje puede faltar ni "colarse" a Nivel 2 sin quedar mapeado primero — un eje del deseado
que no está en la tabla es un **drop silencioso** (falla el gate). **Chequeo duro: nº de ejes en la tabla
== nº de ejes del Paso 1.**

Estados posibles por eje:
- **cubierta** → la(s) fase(s) que la cubren.
- **propuesta-extra** → la(s) fase(s); el humano no la pidió pero el objetivo la implica.
- **diferida** → con motivo (o "roadmap aparte").
- **→ Nivel 2** → con motivo: es un eje del deseado que se decide dejar en el checklist de dominio amplio,
  NO que desaparece. Debe figurar acá **Y** en la lista Nivel 2 de abajo.

```
Cobertura del objetivo (estado deseado → DAG) — TODOS los ejes del Paso 1, uno por renglón:
- Eje 1 <nombre> → Fases 1, 3        [cubierta]
- Eje 2 <nombre> → Fase 4            [cubierta]
- Eje 3 <nombre> → Fase 7            [PROPUESTA-EXTRA — no la pediste; el objetivo la implica]
- Eje 4 <nombre> → DIFERIDA (motivo) / roadmap aparte
- Eje 5 <nombre> → Nivel 2 (motivo)  [queda como checklist, no como fase]
(… un renglón por CADA eje del Paso 1, sin excepción — el conteo debe coincidir)

Nivel 2 — dominio amplio NO cubierto (checklist, marcá si algo sube a fase):
- [ ] <capacidad del dominio 1>   - [ ] <capacidad del dominio 2>   - [ ] …
```

El humano firma qué queda dentro (incluidas las propuestas-extra), qué se difiere, y si algo del Nivel 2
(o un eje mandado a Nivel 2) sube a fase. **Vos proponés de más; el humano recorta.**

Si el objetivo es enorme (varias dimensiones grandes), ofrecé explícitamente la decisión de scope:
**(a)** un roadmap multi-dimensión (todas), o **(b)** acotar este roadmap a una/unas dimensiones y
las otras en roadmaps aparte. El humano elige el scope; vos no lo decidís solo.

Después presentá el DAG (fases, **rutas tentativas** organic/loop, dependencias, orden) y **esperá OK
antes de escribir el `.md`**. Opciones: **Aprobar** (escribís el roadmap con el scope confirmado),
**Ajustar** (el humano corrige dimensiones/fases/rutas/bordes/orden/scope y re-presentás), **Detener**.
No escribas sin aprobación.

## Paso 6 — Dónde guardar + escribir el roadmap

1. **Preguntá dónde guardarlo**, sugiriendo el default **`docs/planning/roadmaps/<slug>.md`**
   (dentro del repo — este roadmap SÍ se versiona/commitea, a diferencia del kickoff transitorio de
   los carriles que va fuera del repo). Permití override.
2. Escribí el `.md` con el formato de abajo (rutas absolutas para operar; `mkdir -p` la carpeta).
3. **Puntero liviano en engram** para descubribilidad: `mem_save` topic_key `sdd/<slug>/roadmap`,
   contenido de una línea `Roadmap en archivo: <ruta absoluta>`. No dupliques el contenido.
4. Respondé con la ruta del archivo + el orden sugerido de fases para pasar a `/mala-pata-triage`.

### Formato del roadmap `.md`

```markdown
---
objetivo: <título corto del objetivo grande>
slug: <kebab-case>
project: <project>
created_at: <ISO 8601>
fases_total: <N>
---

# Roadmap: <objetivo>

## Objetivo grande
<qué se quiere lograr, para quién/dónde, cómo se ve el éxito — medible>

## Arquitectura / costuras (Paso 3)
<los bordes reales por donde parte el trabajo, anclados al .codegraph/ — módulos/interfaces/datos>

## Contexto e investigación
<hallazgos relevantes: cómo se resuelve esto / patrones / qué reusar del repo — con refs>

## DAG de fases

| # | Fase | Ruta tentativa | Depende de | Corte vertical (una línea) |
|---|------|----------------|-----------|----------------------------|
| 1 | <nombre> | loop:STANDARD | — | <qué entrega end-to-end> |
| 2 | <nombre> | organic | 1 | ... |
| 3 | <nombre> | loop:LITE | 1 | ... |

> **Ruta tentativa = pronóstico.** Al ejecutar, cada fase se pasa por `/mala-pata-triage`, que
> re-decide organic/loop con la info del momento (ver Paso 4-bis). Las fases previas pueden cambiar
> la ruta de una posterior.

Orden sugerido (topológico): 1 → (2 ∥ 3) → …   ·   Paralelizables: {2, 3}

## Fases en detalle

### Fase 1 — <nombre>
- **Ruta tentativa**: loop:STANDARD  ·  **Depende de**: —
- **Por qué esa ruta**: <si loop: LA decisión abierta que la hace loop — lo que triage re-chequea; si organic: "Qué+Done+Decisiones ya enunciables">
- **IN**: <qué incluye esta fase>
- **OUT**: <qué NO incluye — queda para otra fase>
- **DoD** (Given/When/Then):
  - [ ] Given <estado>, When <acción>, Then <resultado observable>.
- **Para arrancar**: `/mala-pata-triage <descripción de esta fase>` (triage decide organic/loop con
  la info del momento; una fase = una unidad).

### Fase 2 — …
(idem por cada fase)
```

## Reglas

- **Completitud > lo pedido**: el roadmap cubre el objetivo COMPLETO (estado deseado MECE), no solo lo
  que el humano listó. Sobre-descubrí y proponé; el humano recorta en el gate. Mejor que sobre, no que falte.
- **NO ejecutás**: ni triage, ni loop, ni organic, ni código. Solo el roadmap.
- **Rutas absolutas** en comandos; relativas al hablarle al humano.
- **Únicas preguntas válidas**: las del gate de vaguedad (Paso 0), las decisiones abiertas que
  cambian el DAG (Paso 2), dónde guardar (Paso 6) y el gate de cobertura + DAG (Paso 5). Nada de "ritmo" ni
  "artifact store".
- **Redirigí a `/mala-pata-triage`** si el objetivo ya entra en una sola unidad (Regla dura #2).
- Cada fase del roadmap es insumo para UNA pasada de `/mala-pata-triage` (que la rutea a organic o
  loop con la info del momento) — nunca las agrupes.
