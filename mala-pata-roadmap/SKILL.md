---
name: mala-pata-roadmap
description: >
  Capa de planeación por ENCIMA de /mala-pata-loop. Recibe UN objetivo grande, lo analiza,
  investiga cómo se resuelve (web + cómo lo hacen los grandes), lee el .codegraph/ del proyecto
  para anclarlo al código real, hace preguntas si falta contexto, y lo descompone en un DAG de
  fases loop-sized (cada fase = corte vertical shippeable que entra en un solo loop). Escribe un
  roadmap .md versionable en el repo. NO ejecuta, NO corre el loop, NO toca código: solo produce
  el mapa de fases que después vos pasás una por una a /mala-pata-loop.
  Trigger: "roadmap de <objetivo>", "descomponé este objetivo grande", "armá el plan de fases",
  o cualquier objetivo demasiado grande para un solo loop.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.0.0"
---

# /mala-pata-roadmap — objetivo grande → DAG de fases loop-sized

Objetivo del usuario: **entrada entregada por el CLI**

Tu trabajo: convertir un objetivo GRANDE en un **DAG de fases**, donde cada fase es tan chica que
entra en un solo ciclo de `/mala-pata-loop`. Producís un `.md` con ese roadmap y **nada más** —
no escribís código, no corrés el loop, no aplicás. Después el humano toma cada fase y se la pasa a
`/mala-pata-loop` para su kickoff.

> ⛔ **Regla dura #1 — NO ejecutás nada.** Ni código, ni migraciones, ni corrés `/mala-pata-loop`,
> ni `/mala-pata-organic`. Tu único entregable es el roadmap `.md` (+ un puntero en engram). El DAG
> es un plan, no una orden de implementar.
>
> ⛔ **Regla dura #2 — si el objetivo YA entra en un loop, NO inventes fases.** Si al analizarlo
> ves que es un cambio chico/mediano que cabe en un solo ciclo (mapea a un perfil FULL o menor sin
> partir), **PARÁ y redirigí a `/mala-pata-loop` directo**. Este skill es solo para objetivos que
> NO caben en un loop. Sobre-descomponer algo chico es el anti-patrón que este skill debe evitar.

## Paso 0 — ¿Amerita roadmap? (gate de tamaño + vaguedad)

- **¿Es lo bastante grande?** Si el objetivo cabe en un solo loop → Regla dura #2 (redirigí a loop).
- **¿Es lo bastante claro para descomponer?** Necesitás inferir **qué** se quiere lograr, **para
  quién/dónde** (módulo/dominio) y **cómo se ve el éxito**. Si falta el objeto mismo ("mejorá la
  app") → pedí lo mínimo y esperá; no inventes alcance.
- Recuperable (falta 1-2 datos) → hacé preguntas concretas y esperá. Este es el gate de preguntas.

## Paso 1 — Entender + investigar + anclar al código real

En paralelo, sin escribir nada:

1. **Proyecto activo**: detectá el repo/cwd y leé su arquitectura (`CLAUDE.md`, `ARCHITECTURE.md`,
   o equivalentes). `mem_search` por trabajo previo relacionado.
2. **.codegraph/**: si el proyecto tiene índice, usá `codegraph_explore` (o los comandos read-only
   de CodeGraph) para mapear los módulos, símbolos y dependencias reales que el objetivo toca.
   Si no hay `.codegraph/`, mapeá con Read/Grep/Glob lo mínimo para entender las costuras reales.
3. **Investigación externa** (WebSearch/WebFetch): cómo se resuelve este tipo de objetivo, cómo lo
   hacen equipos maduros, qué patrones/errores conocidos hay. **Anclá lo que traés a TU código** —
   la best-practice que ignora lo que ya existe no sirve (reuse-first, igual que preview).
4. **Preguntas**: si después de esto quedan decisiones abiertas que cambian la forma del DAG,
   preguntá ANTES de descomponer (no las resuelvas adivinando).

## Paso 2 — Pase de arquitectura ANTES de descomponer

Antes de cortar en fases, definí las **costuras reales** por donde va a partir el trabajo
(interfaces, módulos, límites de datos), ancladas al `.codegraph/` del Paso 1. Esto es lo que hace
que las fases salgan por bordes limpios y no por temas arbitrarios — la lección de los planners que
descomponen sin visión de arquitectura y terminan con fases que no son shippeables solas.

## Paso 3 — Descomponer a un DAG de fases

Producí el grafo de fases con estas reglas (todas, no opcionales):

- **Cada fase es un corte VERTICAL shippeable** — una rebanada end-to-end que deja el sistema
  funcionando, no una capa horizontal ("toda la DB", "toda la UI"). Si la fase no se puede mergear
  y quedar sola en verde, no es una fase válida.
- **El perfil es el TECHO duro del tamaño.** Cada fase debe mapear a un perfil de `/mala-pata-loop`
  (FULL/STANDARD/LITE/MINIMAL). **Si una fase sería más grande que FULL → se PARTE.** Sin excepción.
- **El disparador del split es la COMPLEJIDAD / AISLAMIENTO DE CONTEXTO, no las líneas.** La prueba
  de "¿entra en un loop?" es: ¿el contexto de esta fase se aísla limpio del resto? Si para entender
  o hacer la fase necesitás cargar el contexto de media otra fase, todavía está demasiado grande.
- **Cada nodo lleva un borde EXPLÍCITO IN / OUT** — qué entra y qué queda afuera — para que dos
  fases no se pisen ni dupliquen trabajo.
- **Dependencias como DAG**: cada fase declara de qué otras fases depende. El grafo no tiene ciclos.
  Da el orden topológico sugerido (qué se puede hacer en paralelo, qué es secuencial).
- **Anti-sobre-descomposición**: la MENOR cantidad de fases posible con la condición de que cada una
  entre en un loop. No 40 micro-fases; no una fase gigante. Si dudás entre 3 fases grandes o 8
  chicas, elegí el mínimo que respete el techo de perfil y el aislamiento de contexto.

## Paso 4 — Gate humano del DAG

Presentá el DAG propuesto (las fases, sus perfiles, sus dependencias, el orden) y **esperá OK antes
de escribir el `.md`**. Opciones: **Aprobar** (escribís el roadmap), **Ajustar** (el humano corrige
fases/bordes/orden y re-presentás), **Detener**. No escribas el archivo sin aprobación.

## Paso 5 — Dónde guardar + escribir el roadmap

1. **Preguntá dónde guardarlo**, sugiriendo el default **`docs/planning/roadmaps/<slug>.md`**
   (dentro del repo — este roadmap SÍ se versiona/commitea, a diferencia del kickoff transitorio de
   `/mala-pata-loop` que va fuera del repo). Permití override.
2. Escribí el `.md` con el formato de abajo (rutas absolutas para operar; `mkdir -p` la carpeta).
3. **Puntero liviano en engram** para descubribilidad: `mem_save` topic_key `sdd/<slug>/roadmap`,
   contenido de una línea `Roadmap en archivo: <ruta absoluta>`. No dupliques el contenido.
4. Respondé con la ruta del archivo + el orden sugerido de fases para pasar a `/mala-pata-loop`.

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

## Arquitectura / costuras (Paso 2)
<los bordes reales por donde parte el trabajo, anclados al .codegraph/ — módulos/interfaces/datos>

## Contexto e investigación
<hallazgos relevantes: cómo se resuelve esto / patrones / qué reusar del repo — con refs>

## DAG de fases

| # | Fase | Perfil | Depende de | Corte vertical (una línea) |
|---|------|--------|-----------|----------------------------|
| 1 | <nombre> | STANDARD | — | <qué entrega end-to-end> |
| 2 | <nombre> | LITE | 1 | ... |
| 3 | <nombre> | STANDARD | 1 | ... |

Orden sugerido (topológico): 1 → (2 ∥ 3) → …   ·   Paralelizables: {2, 3}

## Fases en detalle

### Fase 1 — <nombre>
- **Perfil**: STANDARD  ·  **Depende de**: —
- **IN**: <qué incluye esta fase>
- **OUT**: <qué NO incluye — queda para otra fase>
- **DoD** (Given/When/Then):
  - [ ] Given <estado>, When <acción>, Then <resultado observable>.
- **Para arrancar**: `/mala-pata-loop <descripción de esta fase>` (una fase = un kickoff).

### Fase 2 — …
(idem por cada fase)
```

## Reglas

- **NO ejecutás**: ni loop, ni organic, ni código. Solo el roadmap.
- **Rutas absolutas** en comandos; relativas al hablarle al humano.
- **Únicas preguntas válidas**: las del gate de vaguedad (Paso 0), las decisiones abiertas que
  cambian el DAG (Paso 1), dónde guardar (Paso 5) y el gate del DAG (Paso 4). Nada de "ritmo" ni
  "artifact store".
- **Redirigí a `/mala-pata-loop`** si el objetivo ya es loop-sized (Regla dura #2).
- Cada fase del roadmap es insumo para UN kickoff de `/mala-pata-loop` — nunca las agrupes.
