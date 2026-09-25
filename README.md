# mala-pata

*No inventamos la rueda — la orquestamos.*

Capa de orquestación para desarrollo asistido por IA (Claude Code / Codex): toma el motor de **gentle-ai** y lo organiza en un flujo de trabajo propio — por fases, con gates humanos y aislamiento por worktree.

## Origen

mala-pata empezó como un **SDD (Spec-Driven Development) propio**, read-only, hecho enteramente por mí — solo el ciclo de especificación *antes* de tocar código. Más adelante conocí **[gentle-ai](https://github.com/Gentleman-Programming/gentle-ai)** (de Gentleman Programming) y decidí **no reinventar el motor**: adopté su base (las fases `sdd-*`, `engram`, el modelo de review) y **la acoplé a mi flujo de trabajo** en esta capa.

Hoy mala-pata es esa capa — más una pieza que sigue siendo **100% mía y que gentle-ai no tiene: `sdd-preview`**, un gate humano de plan (en cristiano) entre `tasks` y `apply`.

## Qué es de quién (atribución honesta)

**Enteramente mío (original):**
- El **SDD original** — el concepto y la primera versión, read-only, previa a gentle-ai.
- **`sdd-preview`** — fase de recorrido + gate anti-sello que **no existe** en el SDD de gentle-ai.
- Toda la **capa `mala-pata-*`** (los skills de abajo): cómo se orquesta, los perfiles de ejecución, la disciplina de worktree/rutas, el radar, los roadmaps y la documentación de flujo.

**Base de gentle-ai (el motor — NO incluido en este repo, se instala aparte):**
- Las fases `sdd-*` (`explore → propose → spec → design → tasks → apply → verify → archive`), `engram` (memoria persistente), **RDD** (receipt-driven review), **ODD** (organic-driven development), judgment-day, integración con CodeGraph.

> En una línea: **gentle-ai pone el motor; mala-pata pone el flujo.**

## Skills (esta capa)

| Skill | Qué hace | Origen |
|---|---|---|
| `mala-pata-research` | Prepara una idea cruda (Heilmeier + Double Diamond + JTBD), escribe un doc de research y hace handoff a triage/roadmap. Read-only. | mala-pata |
| `mala-pata-triage` | **Puerta de entrada.** Lee cualquier pedido, aplica el gate de forma y responde qué carril correr (organic/loop/roadmap). No genera ni ejecuta. | mala-pata |
| `mala-pata-loop` | Toma el **SDD** de gentle-ai y arma el kickoff (contexto técnico completo) en tu flujo. | mala-pata |
| `mala-pata-loop-start` | Corre el ciclo SDD desde el kickoff (explore → … → archive), con gate por fase. | mala-pata |
| `mala-pata-organic` | Genera el kickoff de un cambio **ODD** con gate de formato estricto (Qué/Why/Done/Decisiones); rutea a loop/roadmap si no pasa. NO ejecuta. | mala-pata |
| `mala-pata-organic-start` | Corre el ciclo **ODD** desde el kickoff de organic (worktree → explorar → task-by-task + RDD → cerrar). | mala-pata |
| `mala-pata-loop-orchestrate` | Planifica un lote de kickoffs (olas, conflictos, splits) — read-only. | mala-pata |
| `mala-pata-loop-orchestrate-start` | Lanza el lote en paralelo (un worktree + una sesión por kickoff). | mala-pata |
| `mala-pata-radar` | Descubre (engram) y diagnostica (git) los SDD por proyecto o `global` — read-only. | mala-pata |
| `mala-pata-roadmap` | Objetivo grande → DAG de fases loop-sized → roadmap `.md` versionable. | mala-pata |
| `mala-pata-walkthrough` | De un PR/roadmap: recorrido de prueba (Given/When/Then) → QA interno + doc para cliente. | mala-pata |
| `sdd-preview` | Gate humano de plan entre `tasks` y `apply` (resumen en cristiano + anti-duplicación, una sola pasada). | **100% mío** |

> El motor `sdd-*` / `engram` / RDD / ODD **no está en este repo**: lo provee gentle-ai. Estos skills lo orquestan.

## En qué nos paramos (no inventamos la rueda)

Cada skill se apoya en un marco estándar de la industria, no en un criterio inventado:

| Skill | Framework en el que se para |
|---|---|
| `mala-pata-research` | Heilmeier Catechism (DARPA) + Double Diamond (Discover/Define) + Jobs-to-be-Done. |
| `mala-pata-triage` / gate de `mala-pata-organic` | Gate de forma Qué/Why/Done(=when)/Decisiones + INVEST (Testable). |
| `mala-pata-loop` (Paso 0 DoR) | Example Mapping / Three Amigos + INVEST. |
| `mala-pata-roadmap` | MECE + regla del 100% + Gap Analysis + JTBD + checklist de dominio (estilo ISO/IEC 25010). |
| `mala-pata-walkthrough` | Diátaxis + BDD living documentation (Given/When/Then). |
| Estructura del kickoff | Best-practice de prompts largos de Anthropic (contexto primero, instrucción al final). |
| Entrega | Work-unit commits / chained PRs (presupuesto de review ~400 líneas). |

El motor (SDD/ODD/RDD/engram) es de gentle-ai; los frameworks son estándar de la industria; mala-pata pone el FLUJO que los une.

## Relación con la instalación viva

**Esto es una COPIA para versionar, no la fuente viva.** Los skills que Claude Code / Codex ejecutan viven en `~/.agent-skills/<skill>` y están symlinkeados desde `~/.claude/skills/` y `~/.codex/skills/`.

Este repo **no está symlinkeado** — puede quedar desactualizado respecto a `~/.agent-skills`. Para sincronizar la copia con lo vivo:

```bash
for s in mala-pata-research mala-pata-triage mala-pata-loop mala-pata-loop-start mala-pata-loop-orchestrate \
         mala-pata-loop-orchestrate-start mala-pata-radar mala-pata-organic \
         mala-pata-organic-start mala-pata-roadmap mala-pata-walkthrough sdd-preview; do
  rm -rf "$s" && cp -R "$HOME/.agent-skills/$s" "$s"
done
git add -A && git commit -m "sync: snapshot de ~/.agent-skills"
```

## Crédito

Construido sobre **[gentle-ai](https://github.com/Gentleman-Programming/gentle-ai)** de Gentleman Programming. mala-pata es una capa de orquestación encima; el motor SDD / ODD / RDD / engram es de gentle-ai. El SDD original y `sdd-preview` son aporte propio.
