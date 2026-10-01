---
idea_slug: herramientas-comunidad-faltantes
project: mala-pata
verdict: PROCEDER
created_at: 2026-09-30
next: triage
size_signal: multi-unidad
---

# Research: herramientas de comunidad muy usadas que podrían faltarte

## Veredicto: PROCEDER (shortlist corta y de alto impacto) — pero la premisa amplia es falsa
No "te faltan muchas". Estás **over-covered** en casi todo. El único hueco real es **inteligencia de código / análisis estático**. Ahí sí hay 1 herramienta clara que te falta (Serena) y 2 que ya convergen con tu idea de guards (ast-grep, Semgrep). El resto de lo "popular" son alternativas a lo que ya tenés, no complementos.

## Idea cruda (lo que pediste)
> "¿Habrá más herramientas de comunidad muy usadas que me recomiendes y que me falte usar?"

## Discover

### Cómo se hace hoy (tu stack actual, para no recomendar lo que ya tenés)
- **Orquestación / spec:** gentle-ai (SDD/ODD/RDD) + tu capa mala-pata. **Memoria:** engram. **Docs de libs:** Context7. **Browser:** Playwright MCP. **PM:** ClickUp MCP. **Diagramas:** archify + diagram-design. **Código (lectura/grafo):** codegraph. **Agente extra:** Pi.
- Para tocar código, hoy usás **grep/Read + codegraph** (grafo + blast-radius). No tenés una capa **semántica a nivel símbolo** (LSP) ni **transform estructural por AST**.

### Dónde SÍ te falta (gaps reales) — con fuentes
1. **Serena** (MCP, MIT) — le da al agente las herramientas de un IDE vía LSP: *find symbol · find references · reemplazar exactamente un function body*, 40+ lenguajes, para Claude Code/Codex. Es el fin del "grep-and-read-the-whole-file". **Complementa** codegraph (grafo) con navegación/edición a nivel símbolo — no lo duplica. ([Serena guide](https://mcp.directory/blog/serena-mcp-complete-guide-2026), [vibecodinghub](https://vibecodinghub.org/tools/serena))
2. **ast-grep** — búsqueda y codemod **estructural por AST** (distingue `ilike(col,x)` de la palabra en un comentario). Potencia directo tu idea de guards (arch-lint, reglas AST) y refactors masivos. ([search-tools-mastery](https://cc.bruniaux.com/guide/workflows/search-tools-mastery/))
3. **Semgrep** — SAST + patrones custom rápidos, reglas aprobables sin ser compiler-engineer. Para security-review y guards deterministas. ([SAST 2026](https://www.aikido.dev/blog/top-sast-tools), [open-source security 2026](https://www.wiz.io/academy/application-security/open-source-code-security-tools))
   - Nota: `dependency-cruiser`, `jscpd`, `eslint-plugin-boundaries` ya aparecieron en el research de **endurecer-guards-deterministas** — no son "nuevos", ya están en esa cola. ([JS/TS deps compared](https://rev-dep.com/docs/comparison-with-other-tools/overview))

### Dónde NO te falta nada (over-covered — adoptar reinventaría)
- **Spec-driven dev**: spec-kit (GitHub), Kiro (Amazon), OpenSpec, BMAD son **alternativas** a gentle-ai + mala-pata, no complementos. Adoptarlas sería reinventar lo tuyo. ([SDD tools 2026](https://dev.to/filiksyos/i-tested-the-top-spec-driven-dev-tools-in-2026-4gdm))
- **GitHub MCP** (30k+ estrellas, "el único mandatorio"): útil, pero ya cubrís el 80% con `gh` CLI + git. Opcional, baja prioridad. ([best MCP 2026](https://www.tembo.io/blog/best-mcp-servers))
- **Memoria** (Mem0/Letta/Zep): tenés engram. **Docs**: Context7. **Browser**: Playwright. **PM**: ClickUp. Todo cubierto.

### Jobs-to-be-done
> "Como dev con un stack ya potente, necesito saber qué POCAS herramientas de alto impacto me faltan — no una lista genérica — para dejar de hacer grep-and-read cuando ya existe algo semántico."

## Heilmeier Catechism (7)
1. **Qué:** identificar herramientas de comunidad muy usadas que no usás y que valgan la pena.
2. **Cómo se hace hoy + límites:** stack fuerte, pero el carril de código es grep/Read/codegraph; falta semántico (LSP) y AST.
3. **Novedad:** recomendar solo los 3 de alto impacto del hueco real, no una laundry list.
4. **A quién le importa (asunción a confirmar):** a vos; velocidad y precisión al editar código.
5. **Riesgos:** sumar MCPs infla contexto/tooling; adoptar de más. Mitigar = solo los de alto impacto, uno por vez.
6. **Costo:** cada adopción es chica (instalar un MCP/CLI); Serena = instalar MCP + opcional referenciarlo en skills.
7. **Exámenes de éxito:** con Serena instalado, el agente ubica un símbolo y sus referencias sin leer archivos enteros; con ast-grep, una regla AST atrapa el patrón que el grep no distinguía.

## Define — idea afinada (borrador para triage)
- **Qué** — adoptar una shortlist de 3 herramientas del hueco de inteligencia de código: **Serena** (MCP LSP, top), **ast-grep** (codemod AST), **Semgrep** (SAST/patrones).
- **Why** — es el único carril donde de verdad te falta algo; el resto está cubierto.
- **Done (when)** — Serena instalado y respondiendo (find symbol/references) en Claude Code; ast-grep/Semgrep enganchados a la cola de guards.
- **Decisiones ya tomadas (por research):** Serena es #1 y es complemento de codegraph (no reemplazo); ast-grep/Semgrep convergen con `endurecer-guards-deterministas`; los spec-tools se descartan (over-covered).
- **Decisiones abiertas (confirma el humano):** ¿cuántas sumás ya? (recomiendo arrancar solo con **Serena**) · ¿Serena se adopta como MCP a secas, o además mala-pata lo referencia (p.ej. states/loop-start usan Serena para edición símbolo-nivel)?
- **Riesgo** — inflar tooling; mitigado adoptando de a una, empezando por Serena.
- **Señal de tamaño** — multi-unidad (son 3 adopciones independientes); cada una chica. Serena sola = una-unidad.

## Handoff

```
/mala-pata-triage herramientas-comunidad-faltantes
```
(o adoptá solo Serena directo: instalar su MCP y probar. ast-grep/Semgrep ya caen bajo el research de guards.)
