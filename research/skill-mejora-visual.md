---
idea_slug: skill-mejora-visual
skill_name: mala-pata-art
project: mala-pata-skills
verdict: PROCEDER
created_at: 2026-10-09
next: triage
size_signal: una-unidad
---
# Research: mala-pata-art — skill de criterio visual (obra de mala-pata)

## Veredicto: PROCEDER
`mala-pata-art` es un **skill de criterio/guía visual** (como `clean-architecture`/`solid` son para el código, pero para diseño). Es **obra de mala-pata** — su núcleo es un catálogo de principios citado (criterio propio); **reusa de ui-ux-pro-max solo el delta operacional** (números + reglas de a11y/interacción/perf + anti-patrones), NO lo prescriptivo. Entra en **una-unidad**. Listo para triage.

## Qué ES el skill (y qué NO)
- **ES** un **director/acompañante de diseño**: se carga para guiar CÓMO diseñar/mejorar con criterio. Puede (a) guiar al agente en vivo, o (b) ante un prompt tipo "usá este skill para mejorar este artefacto", **generar un MD de consejos** (el criterio aplicado a ESE caso) y, en la misma corrida, **mejorar la cosa** en base a esos consejos.
- **NO** es un carril ni un router: no propone ni decide organic/loop/shot. Es ortogonal a esos flujos — el humano o triage deciden el flujo; `mala-pata-art` solo aporta el criterio. Después de su MD, el humano decide si hace un shot, un prompt que siga el MD, o lo mete en un loop.
- **Read del proyecto, write acotado**: lee el sistema de diseño del proyecto; el único artefacto que escribe es su MD de consejos (+ la mejora si se la piden). No ejecuta fases, no despacha `sdd-*`.

## Discover

### A. Catálogo de principios (el criterio — NÚCLEO del skill, adoptado en 3 niveles de USO)
Todo el catálogo se adopta; se organiza por CÓMO se usa (para ser accionable, no bibliografía).

**Nivel 1 — Operacional (checklist de casi toda mejora):**
- **Gestalt** (Wertheimer/Koffka/Köhler; Wagemans 2012): proximidad, similitud, cierre, continuidad, destino común, figura-fondo, Prägnanz, región común, conexión. ([ref](https://www.simplypsychology.org/what-is-gestalt-psychology.html))
- **Grilla + ritmo espacial** (Estilo Suizo / Müller-Brockmann *Grid Systems* 1981; Hofmann, Max Bill, Keller): grilla, alineación, sans-serif, layout asimétrico. ([ref](https://www.printmag.com/?p=1387))
- **Composición** (bellas artes): balance, ritmo, proporción (áureo 1:1.618, tercios), énfasis/focal, unidad, escala, espacio negativo. ([ref](https://momaa.org/composition/))
- **Color relativo + contraste** (Albers *Interaction of Color* 1963; Itten 7 contrastes). ([ref](https://modernism101.com/?p=68810))
- **Tipografía** (escala, peso para jerarquía, restricción — Vignelli Canon, Bringhurst). ([ref](https://lars-mueller-publishers.com/vignelli-canon))
- **Refactoring UI** (Wathan/Schoger): jerarquía por peso/color no solo tamaño, escala de espaciado, limitar opciones, empezar con mucho blanco/poco contraste.
- **Laws of UX aplicables** (Yablonski): Hick, Fitts, Miller (7±2), aesthetic-usability, Von Restorff, posición serial.
- **Norman**: affordances, signifiers, mapping, feedback, constraints.
- **Craft moderno 2025-26**: minimalismo expresivo, tokens-first, detalle de firma, evitación de anti-patrones generativos. ([ref](https://www.inspoai.io/blog/why-ai-websites-look-generic))

**Nivel 2 — Filosofía/criterio (el "por qué"/el gusto — guían dirección, no checklist):**
- **Bauhaus** (Gropius 1919; Itten, Albers, Moholy-Nagy): forma sigue función, verdad de materiales.
- **Dieter Rams**: 10 principios, "menos pero mejor". ([ref](https://crm.org/articles/less-but-better-dieter-rams-10-principles))
- **Vignelli**: disciplina, adecuación, intangibles+tangibles.
- **Tschichold / Nueva Tipografía**: asimetría, blanco estructural (y su viraje al clasicismo).
- **Paul Rand**: simplicidad, memorabilidad, ingenio.

**Nivel 3 — Contextual (solo cuando aplica):**
- **Tufte** (data-ink ratio, chartjunk, lie factor, small multiples) → solo con datos/charts. ([ref](https://spectrum.ieee.org/tufteisms))
- **Munsell** (orden hue/value/chroma) → background de color.
- **Nielsen** (10 heurísticas de usabilidad) → cuando se evalúa usabilidad, no solo estética.

### B. ui-ux-pro-max — reuso = SOLO el delta operacional (lo demás ya es nuestro o es prescriptivo)
Decisión del usuario: de ui-ux-pro-max **se toman los NÚMEROS y un par de reglas que faltan**; NADA prescriptivo.
- **DENTRO — umbrales operacionales** (vuelven testeable el principio): contraste **4.5:1 (AA) / 7:1 (AAA)**; spacing **4/8pt**; motion **150-300ms** (complejo ≤400, evitar >500); touch-target **44×44pt / 48×48dp**; body **≥16px**; line-length ~45-75 car.
- **DENTRO — reglas a11y/interacción/perf que NO están en el catálogo**: `color-not-only` (nunca significado solo por color); `visible-focus`; `cursor-pointer` en clickeables; viewport sin disable-zoom; `no-layout-shift-hover`; animar **solo transform/opacity**.
- **DENTRO — anti-patrones como checklist de salida** (los tells: gradientes morados, Inter por default, glassmorphism decorativo, bento por default, simetría perfecta, hero+3-cards…).
- **Opcional — styles (84) como VOCABULARIO** para nombrar una dirección (no para "aplicá este estilo").
- **FUERA — todo lo prescriptivo**: colors (161 paletas hex), typography (73 pairings), products→paleta, y los 84 estilos como recomendación. Los concretos los decide el **sistema del proyecto + el criterio del usuario**.
- **Conclusión**: no se usa el motor `search.py` para prescribir; ui-ux-pro-max queda reducido a su capa de números + reglas + anti-patrones. El skill se para sobre el criterio propio (sección A).

### C. Sistema del proyecto (agnóstico)
El skill **lee el sistema de diseño del proyecto actual** si existe (tokens, retícula, reglas, primitivas) y lo trata como **autoritativo**. `bodega-ferreteria-colombia` es el **ejemplar de referencia** (sistema ESLint-enforced: tokens HSL, overlay WCAG, `<Num>` tabular, `<Icon>` SVG, variantes por acción) — NO se hardcodea.

### D. Invariantes duras del usuario (no negociables, enforced siempre)
Sin emoji · iconos **SVG-only** · contraste AA · retícula + escala de espaciado · regla del espacio en blanco · Gestalt.

### JTBD · Dimensión · Problema-vs-solución
- **JTBD**: como dev con buen criterio visual, necesito un skill que me guíe (y opcionalmente aplique) la mejora de algo que no me gusta, con mi criterio + el sistema del proyecto + un cuerpo de principios citado, con mi ojo como gate final.
- **Dimensión**: 1 skill (criterio propio + delta de ui-ux-pro-max); frecuencia alta; severidad = calidad visual de todo lo tuyo, riesgo bajo.
- **Problema-vs-solución**: criterio+principios citados = NUEVO (núcleo); números/reglas de ui-ux-pro-max = reuso; lectura del sistema del proyecto = necesaria; prescriptivo de ui-ux-pro-max = FUERA.

## Define — idea afinada (para triage)
- **Qué**: `mala-pata-art`, skill de criterio/guía visual que guía (y opcionalmente aplica, generando un MD de consejos) la mejora de una UI, componiendo un catálogo de principios citado (3 niveles) + invariantes duras + el delta operacional de ui-ux-pro-max + el sistema del proyecto; el ojo del humano es el gate final.
- **Why**: subir el piso estético de todo con criterio propio, sin re-derivar reglas ni caer en el look genérico/IA.
- **Done**: dado "mejorá esto", el skill produce un MD de consejos (y aplica si se lo piden) que: sin emoji + SVG; contraste AA; alineado a grilla+espaciado; respeta el sistema del proyecto si existe; aplica principios del catálogo; evita los tells; y el humano lo aprueba a ojo.
- **Decisiones ya tomadas**: nombre `mala-pata-art`; skill de criterio/guía (NO router, ortogonal a los carriles); genera MD de consejos + aplica opcional; agnóstico de proyecto; reuso de ui-ux-pro-max = solo delta operacional (no prescriptivo); catálogo de principios en 3 niveles; invariantes duras; ojo del humano = gate.
- **Decisiones abiertas**: ninguna bloqueante. (Detalle fino — formato exacto del MD de consejos, dónde se guarda — se resuelve al construir.)
- **Riesgo**: bajo.
- **Señal de tamaño**: una-unidad.

## Handoff
→ `/mala-pata-triage mala-pata-art` (o directo a construir el skill — es meta-work de mala-pata, una-unidad). Pasá este doc como borrador de campos.
