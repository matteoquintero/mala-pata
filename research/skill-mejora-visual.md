---
idea_slug: skill-mejora-visual
project: mala-pata-skills
verdict: PROCEDER
created_at: 2026-10-09
next: triage
size_signal: una-unidad
---
# Research: skill de mejora visual a medida del usuario

## Veredicto: PROCEDER
La idea es sólida y es sobre todo **orquestación, no invención**: las reglas duras del usuario (no emoji, SVG-only, contraste, tokens) YA están codificadas tanto en el sistema de diseño de bodega (ESLint-enforced) como en las "leyes" de `ui-ux-pro-max`. El skill nuevo las compone + aplica reglas modernas/anti-cliché + usa el criterio visual del humano como gate final. Entra en **una-unidad**.

## Idea cruda (lo que pediste)
Un skill de mala-pata que, cuando algo visualmente no te gusta, lo **mejore** — muy a tu medida/gusto (confiás mucho en tu criterio visual). Fuentes a investigar: (1) las reglas de diseño de bodega-ferreteria-colombia (sistema visualmente muy bueno), (2) internet — reglas para que se vea moderno, destaque, no viejo ni cliché, (3) qué hace `ui-ux-pro-max` para apoyarse. Restricciones duras: odiás los emoticones; solo SVG para iconos; contraste; retícula; regla del espacio en blanco; principios de Gestalt.

## Discover

### Cómo se hace hoy + límites (con fuentes)
Lo que distingue un diseño moderno en 2025-26 es **restricción + criterio**, no apilar efectos de moda:
- **Minimalismo expresivo** (no vacío): pocos elementos, pero con energía — color fuerte, tipografía con carácter, un focal claro. [tubik/LinkedIn](https://www.linkedin.com/pulse/whats-next-7-ui-design-trends-2026-tubik-dd82f), [Envato](https://elements.envato.com/learn/ux-ui-design-trends)
- **Tokens primero** (color/espaciado/tipografía) = el "contrato" que evita el look promedio de lo generado por IA. [gitnexa](https://www.gitnexa.com/blogs/modern-ui-ux-design-principles)
- **Tells de diseño genérico/IA a evitar**: gradientes morados, Inter por default, glassmorphism decorativo, bento grid por default, simetría perfecta, el patrón hero+3-cards+testimonios+pricing+CTA. [inspoai](https://www.inspoai.io/blog/why-ai-websites-look-generic), [managed-code](https://managed-code.com/blog-post/why-ai-websites-look-the-same)
- **Una dirección con punto de vista** + **un detalle de firma** por pantalla; cortar secciones que no se ganan el lugar. [gist NovCog](https://gist.github.com/NovCog/c3c9d70ddafb3da451ca3d2a316f324d)
- **Gestalt** (proximidad/similitud/cierre/continuidad/figura-fondo). [uxplanet](https://uxplanet.org/gestalt-principles-in-ux-design-2e0f423bfcb5)
- **Jerarquía** (tamaño+peso, 3-4 niveles, un focal por pantalla), **contraste** (WCAG ≥4.5:1 body, no solo color), **espacio en blanco** (más entre lo no-relacionado), **retícula** (12 col, todo alineado a grilla + escala de espaciado). [magicui](https://magicui.design/blog/visual-hierarchy-in-web-design), [freecodecamp](https://www.freecodecamp.org/news/learn-ui-design-in-5-minutes-tutorial/)
- *Caveat*: casi todas las fuentes son blogs de tendencia/vendor — tomar los específicos como opinión, no ley. El núcleo (intención + restricción + decisiones deliberadas) es consistente entre todas.

### Qué existe en el código (anclaje real)
**(a) bodega-ferreteria-colombia** tiene un sistema de diseño explícito y **enforced por ESLint** ("Lulo G Design System"). Canónico: `DESIGN.md`, `client/ARCHITECTURE.md` §10-12.5, Storybook. Reglas concretas:
- **Tokens HSL de 2 capas** con canales separados (`client/src/index.css`, mapeados en `tailwind.config.ts`). Tokens semánticos (success/info/warning/destructive/…), cada uno con `-foreground` + `-soft`. Marca Lulo fija (coral #cb5239, etc.). Light primario, dark override.
- **Contraste**: overlay WCAG-strict opt-in (`data-wcag-strict`), redeclara SOLO los tokens que fallan AA (≥4.5:1), con invariante de minimalidad testeado (`token-contrast.test.ts`).
- **Retícula/espaciado**: escala nombrada `--space-2xs…2xl`, breakpoints definidos, alturas single-sourced, `svh/dvh` nunca `vh`.
- **Espacio en blanco/densidad**: shell de scroll único (invariante), padding de card `p-6`, jerarquía por tamaño/peso/espacio, NO por color.
- **Tipografía**: Montserrat/Geist; **`<Num>`** (JetBrains Mono, tabular-nums) obligatorio SOLO para plata/cantidades/IDs — enforced por `require-num-for-currency.js`.
- **Iconos SVG-only enforced**: todo pasa por `<Icon name>` (registry de lucide SVG); `no-raw-lucide-import.js` prohíbe imports crudos; cero emoji-como-icono. **Coincide exacto con tu mandato.**
- **Componentes**: `button.tsx` (cva, matriz de variantes por acción), `card.tsx` (static/hoverable/interactive). Reglas de color NO negociables enforced (`no-ad-hoc-semantic-colors.js`, `no-bespoke-ui.js`, etc.).
- Stack: React+Vite+Tailwind+shadcn (new-york) + Storybook (Atoms/Molecules/Organisms).

**(b) `ui-ux-pro-max`** (`~/.claude/plugins/marketplaces/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/SKILL.md`, v2.5.0): catálogo data-driven — 50+ estilos, 161 paletas, 57 pairings de fuente, 161 product types, 99 guidelines UX, 25 charts, 10 stacks. Se invoca por CLI: `python3 scripts/search.py "<product> <keywords>" --design-system [--domain …] [--stack …]` → devuelve pattern/style/colors/typography + **anti-patterns**. Ya trae leyes duras alineadas con tu mandato: `no-emoji-icons` (SVG only), `color-semantic` (tokens no hex), `color-accessible-pairs` (4.5:1 AA / 7:1 AAA), `spacing-scale` (4/8pt), `number-tabular`, reduced-motion, 150-300ms. *Gotcha*: su body hardcodea "React Native" en algunos pasos aunque el frontmatter y los CSV cubren web — para web se invoca con `--stack shadcn|react|html-tailwind`.

### Jobs-to-be-done
Como **desarrollador con buen criterio visual pero sin ganas de re-derivar las reglas cada vez**, necesito **un skill que tome una UI que no me gusta y la mejore respetando mis reglas duras + el sistema del proyecto + lo que se ve moderno**, para **subir el piso estético de todo lo que hago sin pelear con los detalles, dejando la decisión final a mi ojo**.

### Dimensión del problema (alcance / frecuencia / severidad)
- **Alcance**: un skill nuevo (1 SKILL.md + symlinks), mayormente orquestación de herramientas ya instaladas (ui-ux-pro-max + el sistema del proyecto). No infra nueva.
- **Frecuencia**: alta — cada vez que algo visual no te gusta.
- **Severidad/impacto**: calidad y consistencia visual de TODO lo que producís; riesgo bajo (es un skill de guía/mejora, read sobre el sistema). Impacto alto, blast radius bajo.

### Problema vs solución propuesta (cada pieza)
- Restricciones duras (no emoji / SVG / contraste / grid / espacio / Gestalt) → **necesaria**, pero **ya-existe** en ui-ux-pro-max + bodega → el skill las ORQUESTA/enforcea, no las reimplementa.
- "Leer reglas de bodega" → **derivable** a lo genérico: el skill lee el **sistema de diseño del PROYECTO ACTUAL** (DESIGN.md/tokens/eslint/primitivas) si existe; bodega es el EJEMPLAR de referencia, no un hardcode (las skills mala-pata son agnósticas de proyecto).
- "Apoyarse en ui-ux-pro-max" → **necesaria** (capa de principios generales + anti-patterns, vía su CLI).
- "A mi medida/gusto" → **necesaria**; se define como: enforcar las reglas duras + el sistema del proyecto + las reglas modernas, y tu **criterio visual como gate final** (vos aprobás/ajustás).

## Heilmeier Catechism
1. **Qué**: un skill que mejora una UI que no te gusta, a tu medida, componiendo tus reglas duras + el sistema de diseño del proyecto + reglas modernas/anti-cliché.
2. **Cómo se hace hoy / límites**: a ojo o pidiéndole a un modelo "hacelo lindo" → sale el look promedio/IA (gradiente morado, Inter, bento por default). Límite: sin reglas que lo aten, el modelo devuelve lo más probable, no lo distintivo.
3. **Qué hay de nuevo**: atar la mejora a (i) tus reglas duras, (ii) el sistema real del proyecto (tokens/eslint/primitivas), (iii) anti-patterns explícitos — y dejar tu ojo como gate. No es "otro generador", es un enforcer con criterio.
4. **A quién le importa** *(tu prioridad)*: a vos; que todo lo tuyo se vea intencional y moderno sin re-pensar las reglas. [asunción a confirmar: sos el único usuario objetivo por ahora]
5. **Riesgos**: que degenere en "generador genérico" (mitigado por anti-patterns + sistema del proyecto); que choque con ui-ux-pro-max si duplica sus reglas (mitigado: apoyarse en su CLI, no copiarlo).
6. **Costo**: una-unidad — 1 SKILL.md + symlinks, orquestación.
7. **Done testeable**: dada una UI que no te gusta, el skill produce una mejora que (a) no usa emoji y usa SVG, (b) cumple contraste AA, (c) alinea a retícula + escala de espaciado, (d) respeta tokens/sistema del proyecto si existe, (e) evita los tells de cliché, y (f) vos la aprobás a ojo.

## Define — idea afinada (borrador para triage)
- **Qué**: skill mala-pata de mejora visual que toma una UI y la mejora componiendo reglas duras del usuario + el sistema de diseño del proyecto actual + reglas modernas/anti-cliché, apoyándose en `ui-ux-pro-max`.
- **Why**: subir el piso estético de todo sin re-derivar reglas, con el criterio visual del humano como gate final.
- **Done (when)**: los 7 criterios de arriba (Heilmeier 7).
- **Decisiones ya tomadas**: agnóstico de proyecto (lee el sistema del proyecto; bodega = ejemplar, no hardcode); se apoya en `ui-ux-pro-max` (CLI `search.py`, capa general) + el sistema del proyecto (capa autoritativa cuando existe); reglas duras no negociables (no emoji, SVG-only, contraste AA, retícula, espacio en blanco, Gestalt) + reglas modernas/anti-cliché; criterio del humano = gate final.
- **Decisiones abiertas**: (1) **¿el skill EDITA la UI in-situ (transformer que mejora el código) o produce un PLAN/crítica de mejora que aplica shot/organic?** — decidible con una pregunta al construir. (2) el **nombre** del skill (como shot/gaps, lo elegís vos).
- **Riesgo**: bajo — skill de guía/mejora; el enforcement real del sistema lo da el proyecto (ESLint en bodega).
- **Señal de tamaño**: **una-unidad** (orquestación; no multi-unidad — no hay varias decisiones de arquitectura abiertas ni cortes verticales independientes).

## Handoff
→ `/mala-pata-triage skill-mejora-visual` con el borrador de campos de arriba. Las 2 decisiones abiertas (editar-vs-proponer, nombre) son decidibles con una pregunta cada una al construir — no fuerzan loop.
