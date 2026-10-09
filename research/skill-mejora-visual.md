---
idea_slug: skill-mejora-visual
project: mala-pata-skills
verdict: AFILAR
created_at: 2026-10-09
next: ninguno (AFILAR — faltan tus picks + nombre + modalidad)
size_signal: una-unidad
---
# Research: skill de mejora visual (obra de mala-pata, a medida del usuario)

## Veredicto: AFILAR
La idea es sólida y es **obra de mala-pata** (mucho es criterio propio del usuario), que **reusa selectivamente** ui-ux-pro-max — no es un wrapper. Falta que el usuario: (1) elija qué de ui-ux-pro-max entra, (2) ponga el nombre, (3) confirme las 3 modalidades (HTML/shot · artifact · roadmap de mejora visual). No rutear hasta eso.

## Idea cruda (lo que pediste)
Un skill que, cuando algo visualmente no te gusta, lo mejore — muy a tu medida/gusto (confiás mucho en tu criterio visual). Es obra de mala-pata: reusa ui-ux-pro-max donde conviene, pero mucho es TU criterio. Restricciones duras: no emoticones; solo SVG para iconos; contraste; retícula; regla del espacio en blanco; Gestalt. Querés un catálogo INMENSO de principios (pre-digitales y digitales, citando diseñadores/artistas de todo). Y que te liste TODO ui-ux-pro-max para elegir.

## Modalidades del skill (confirmar)
No es editar-vs-proponer binario; es **multi-modal según el alcance** (alimenta los carriles existentes):
- **Mejorar un HTML / componente** → carril **shot** (cambio chico, in-situ).
- **Mejorar un artifact** → mejora puntual sobre el artefacto.
- **Proponer un roadmap de mejora visual de un proyecto completo** → carril **roadmap** (DAG de fases de mejora).
El skill es el LENTE/criterio; el carril (shot/organic/roadmap) lo decide triage según el alcance.

## Discover

### A. Catálogo de principios visuales (el "cuerpo de criterio" del skill, citado)

**A1. Fundaciones perceptuales — Gestalt** (Wertheimer, Koffka, Köhler, ~1920; revisión Wagemans 2012): proximidad, similitud, cierre, continuidad, destino común, figura-fondo, **Prägnanz/buena forma**, región común, conexión/uniform connectedness. ([simplypsychology](https://www.simplypsychology.org/what-is-gestalt-psychology.html))

**A2. Bauhaus** (Gropius 1919; Itten, Albers, Moholy-Nagy, Kandinsky): forma sigue función, verdad de los materiales, unión arte+oficio, geometría elemental.

**A3. Estilo Suizo / Tipográfico Internacional** (1950s; Ernst Keller, Armin Hofmann, Max Bill, **Josef Müller-Brockmann**): claridad objetiva, **sistema de grilla matemática**, sans-serif como material, layout asimétrico, foto objetiva, diseño como comunicación no autoexpresión. Müller-Brockmann *Grid Systems in Graphic Design* (1981). ([printmag](https://www.printmag.com/?p=1387), [opentextbc](https://opentextbc.ca/graphicdesign/chapter/1-6-its/))

**A4. Nueva Tipografía / tipografía** — **Jan Tschichold** (*Die Neue Typographie* 1928: asimetría, sans, blanco estructural; luego vira al clasicismo en *The Form of the Book*); **Robert Bringhurst** (*The Elements of Typographic Style*: legibilidad, la tipografía se muestra y luego se borra para ser leída); **Massimo Vignelli** (*Vignelli Canon*: intangibles [semántica, sintaxis, disciplina, adecuación] + tangibles [grilla, tipo, color, layout]; restricción de tipografías); **Otl Aicher** (sistemas, pictogramas Múnich 72). ([vignelli canon](https://lars-mueller-publishers.com/vignelli-canon), [bringhurst review](https://oss.adm.ntu.edu.sg/kyong009/review-the-elements-of-typographic-style/))

**A5. Color** — **Johannes Itten** (7 tipos de contraste, esfera cromática); **Josef Albers** (*Interaction of Color* 1963: contraste simultáneo, "el color es relativo — todo fondo resta su propio tono"); **Albert Munsell** (orden por hue/value/chroma). ([modernism101](https://modernism101.com/?p=68810), [mitchellino](https://mitchellino.substack.com/p/albers-versus-itten))

**A6. Composición (bellas artes / foto, siglos)**: balance (simétrico/asimétrico), ritmo (repetición), proporción (**áureo 1:1.618**, **regla de tercios**), énfasis/focal, unidad, contraste tonal, escala, peso visual, espacio negativo. ([momaa](https://momaa.org/composition/))

**A7. Diseño de producto / "menos pero mejor"** — **Dieter Rams** (10 principios: innovador, útil, estético, comprensible, discreto, honesto, durable, minucioso, ecológico, lo menos posible). ([crm.org](https://crm.org/articles/less-but-better-dieter-rams-10-principles))

**A8. Visualización de datos** — **Edward Tufte** (data-ink ratio, chartjunk, lie factor, small multiples, densidad de datos). ([IEEE](https://spectrum.ieee.org/tufteisms))

**A9. Identidad / marca** — **Paul Rand** (simplicidad, memorabilidad, ingenio), **Saul Bass**, **Lester Beall**.

**A10. Interacción / usabilidad (digital)** — **Don Norman** (affordances, signifiers, mapping, feedback, constraints); **Jakob Nielsen** (10 heurísticas de usabilidad).

**A11. Leyes de UX** (Jon Yablonski, *Laws of UX*): Fitts, Hick, Miller (7±2), Jakob, Tesler (conservación de la complejidad), Postel, efecto estética-usabilidad, Von Restorff (aislamiento), posición serial, umbral de Doherty (<400ms), ley de Prägnanz, ley de proximidad/región común.

**A12. Práctica web contemporánea** — *Refactoring UI* (Wathan & Schoger: jerarquía por peso/color no solo tamaño; escala de espaciado; empezar con mucho blanco y poco contraste y agregar donde haga falta; limitar opciones — Hick); **design tokens** como contrato.

**A13. Craft moderno 2025-26 (técnico, no "anti-cliché a secas")**:
- **Minimalismo expresivo** (restricción en cantidad, no en energía).
- **Tipografía como identidad** (variable fonts, grotescas distintivas, type fluido sin saltos por breakpoint).
- **Tokens-first** (evita el "look promedio" de lo generado por IA).
- **Motion como explicación** (estado, no decoración; 150-300ms; respetar reduced-motion).
- **Un detalle de firma** por pantalla; cortar secciones que no se ganan el lugar.
- **Evitación de anti-patrones generativos** (los *tells* de IA): gradientes morados, Inter por default, glassmorphism decorativo, bento-grid por default, simetría perfecta, el patrón hero+3-cards+testimonios+pricing+CTA. ([inspoai](https://www.inspoai.io/blog/why-ai-websites-look-generic), [tubik 2026](https://www.linkedin.com/pulse/whats-next-7-ui-design-trends-2026-tubik-dd82f))

**Invariantes duras del usuario (no negociables, enforced):** sin emoji · iconos SVG-only · contraste ≥4.5:1 (AA) · retícula + escala de espaciado · regla del espacio en blanco · Gestalt.

### B. Qué existe en el código (anclaje real)
**bodega-ferreteria-colombia** = ejemplar de referencia (sistema ESLint-enforced: tokens HSL 2 capas, overlay WCAG-strict, `<Num>` tabular, `<Icon>` SVG-registry, variantes por acción). El skill NO lo hardcodea — lee el sistema del PROYECTO ACTUAL si existe (agnóstico).

**ui-ux-pro-max** (v2.5.0, `~/.claude/plugins/marketplaces/ui-ux-pro-max-skill/`) — inventario COMPLETO para elegir:

- **Motor**: `search.py` (BM25) + CSVs en `src/ui-ux-pro-max/data/`. Flags: `--design-system`, `--domain {style,color,chart,landing,product,ux,typography,icons,google-fonts,react,web}`, `--stack`, `--persist` (escribe `design-system/<proj>/MASTER.md` + `pages/`), `-f markdown`.
- **UI Styles (84)** — General: Minimalism/Swiss · Neumorphism · Glassmorphism · Brutalism · 3D/Hyperrealism · Dark Mode OLED · Claymorphism · Aurora UI · Retro-Futurism · Flat · Skeuomorphism · Liquid Glass · Motion-Driven · Micro-interactions · Neubrutalism · Bento Box · Y2K · Cyberpunk · Organic Biophilic · AI-Native · Memphis · Vaporwave · Dimensional Layering · Exaggerated Minimalism · Kinetic Typography · Parallax Storytelling · Swiss Modernism 2.0 · HUD/Sci-Fi · Pixel Art · Spatial/VisionOS · E-Ink · Gen Z Maximalism · Anti-Polish/Raw · Tactile/Deformable · Editorial Grid/Magazine · Chromatic Aberration · Vintage Analog (+ landing/dashboard/mobile variants). 
- **UX guidelines — 10 categorías**: 1 Accessibility(14) · 2 Touch/Interaction(17) · 3 Performance(19) · 4 Style Selection(13) · 5 Layout/Responsive(16) · 6 Typography/Color(15) · 7 Animation(24) · 8 Forms/Feedback(31) · 9 Navigation(26) · 10 Charts/Data(30).
- **Leyes duras**: no-emoji-icons · color-semantic · color-accessible-pairs(4.5:1/7:1) · color-not-only · spacing-scale(4/8pt) · number-tabular · reduced-motion · duration 150-300ms · transform/opacity-only · touch-target 44/48 · viewport-meta · readable-font-size · cursor-pointer · visible-focus · no-layout-shift-hover. **(coinciden con tus invariantes)**
- **Charts (25)**, **Stacks (16)** (react/next/vue/svelte/astro/swiftui/rn/flutter/nuxt/nuxt-ui/html-tailwind/shadcn/jetpack/threejs/angular/laravel).
- **Lookups parametricos**: colors(161, por product-type, token-sheet shadcn completo) · typography(73 pairings) · products(161, mapea product→estilo+paleta).
- **Siblings**: `design` (logos/CIP/banners/icons SVG) · `design-system` (tokens 3 capas primitive→semantic→component) · `ui-styling` (shadcn/radix/tailwind build) · `brand` (voz) · `slides` (decks).

### C. Jobs-to-be-done
Como dev con buen criterio visual, necesito un skill que tome algo que no me gusta y lo mejore **con mi criterio + el sistema del proyecto + un cuerpo citado de principios**, en la modalidad que corresponda al alcance (HTML/artifact/roadmap), para subir el piso estético de todo, con mi ojo como gate final.

### D. Dimensión del problema
- **Alcance**: 1 skill (orquestación + cuerpo de criterio propio). Reusa ui-ux-pro-max + sistema del proyecto.
- **Frecuencia**: alta.
- **Severidad**: calidad visual de todo lo tuyo; riesgo bajo.

### E. Problema vs solución propuesta
- Invariantes duras → **ya-existe** (ui-ux-pro-max + bodega) → reusar/enforcar.
- Cuerpo de principios citado → **necesaria + NUEVO** (es el criterio propio de mala-pata; no lo da ui-ux-pro-max — su catálogo es de estilos/UX, no de principios citados históricos).
- Multi-modalidad (shot/artifact/roadmap) → **necesaria** (reusa carriles existentes).
- Lectura del sistema del proyecto → **necesaria** (agnóstico).

## Heilmeier Catechism
1. **Qué**: skill de mejora visual multi-modal, obra de mala-pata, que compone criterio propio (principios citados + invariantes duras) + el sistema del proyecto + lo reusable de ui-ux-pro-max.
2. **Hoy/límites**: "hacelo lindo" a un modelo → look promedio/IA; ui-ux-pro-max da catálogo pero no TU criterio ni el cuerpo de principios citado.
3. **Nuevo**: atar la mejora a un cuerpo de principios con autores + invariantes duras + sistema del proyecto + tu ojo como gate; multi-modal por alcance.
4. **A quién le importa** *(solo-humano)*: a vos; [asunción a confirmar: único usuario objetivo].
5. **Riesgos**: degenerar en generador genérico (mitigado: anti-patrones + sistema del proyecto + criterio); duplicar ui-ux-pro-max (mitigado: reuso selectivo elegido por vos).
6. **Costo**: una-unidad.
7. **Done**: dada una UI que no te gusta, el skill produce/propone una mejora que (a) sin emoji, SVG; (b) contraste AA; (c) alineada a grilla+espaciado; (d) respeta el sistema del proyecto si existe; (e) aplica principios del catálogo y evita los tells; (f) en la modalidad correcta (shot/artifact/roadmap); (g) vos la aprobás a ojo.

## Define — idea afinada (borrador para triage)
- **Qué / Why / Done**: ver arriba.
- **Decisiones ya tomadas**: obra de mala-pata con criterio propio; agnóstico de proyecto; multi-modal (shot/artifact/roadmap); invariantes duras; cuerpo de principios citado (sección A); tu ojo = gate final.
- **Decisiones abiertas (AFILAR — solo-humano)**:
  1. **Picks de ui-ux-pro-max**: qué módulos reusa (motor/CSVs, cuáles categorías de las 10 UX-guidelines, leyes duras, styles como referencia, charts, siblings). → el usuario elige del pick-list.
  2. **Nombre del skill** (técnico; el usuario elige).
  3. **Confirmar las 3 modalidades** y cómo rutea cada una (shot/artifact/roadmap).
- **Riesgo**: bajo.
- **Señal de tamaño**: una-unidad.

## Handoff
AFILAR — no rutear. Esperar: picks de ui-ux-pro-max + nombre + confirmación de modalidades. Con eso → `/mala-pata-triage`.
