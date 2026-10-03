---
name: mala-pata-shot
description: Carril MÍNIMO de ODD — el "direct inline" de ODD sin worktree ni ceremonia, para el cambio más chico y ya entendido (un color, un copy, un flag, un fix de una línea). Corre en una sola pasada — autorizar → entrar a la rama segura → entender (1-3 archivos) → editar con el modo TDD del proyecto → work-unit commit (+ RDD por commit si está on). NO crea worktree, NO escribe feature-doc, NO hace preview ni smoke test, NO despacha sdd-*. Si a mitad aparece una decisión, el blast radius crece o hace falta diseñar → PARA y rebota a /mala-pata-organic. Trigger — cambio trivial + entendido + blast radius mínimo, o cuando /mala-pata-triage rutea acá.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.2.0"
---

# /mala-pata-shot — ODD en una sola pasada, sin worktree

Pedido del usuario: **entrada entregada por el CLI** (o el borrador de campos que pasó `/mala-pata-triage` al decidir shot)

Es el carril más chico de mala-pata: **ODD desnudo**. Mismo método que `/mala-pata-organic-start` (authorize → explore → implementar → cerrar, con work-unit commit y RDD por commit), pero **sin worktree, sin feature-doc, sin split kickoff/start, sin preview ni smoke test**. Un tiro y listo (*one-shot*) para el cambio tan chico y tan entendido que toda esa ceremonia es puro overhead.

> **El protocolo ODD es la fuente de verdad.** Sus pasos, los work-unit commits y la evaluación RDD por commit viven en tu **CLAUDE.md global** (`## Implementation Routing → ### ODD protocol`). Este skill corre el subconjunto mínimo de ese protocolo — la ruta **direct inline**. Si el CLAUDE.md y este skill difieren, **manda el CLAUDE.md**.

> **Usa workers de ODD (direct inline), NUNCA agentes `sdd-*`.** El preflight `PreToolUse:Agent` de gentle-ai no aplica acá, igual que en `/mala-pata-organic`.

## Requisitos (orquestar, no reinventar)

mala-pata orquesta herramientas de comunidad — no las reimplementa. Chequeá al arrancar:

- **Obligatorias** (sin fallback — si falta, PARÁ y pedí instalarla, no arranques):
  - `git` — control de versiones; el work-unit commit es parte del carril. Siempre presente.
  - `gentle-ai` — motor de RDD por commit (carril ODD). Instalar: `brew install gentleman-programming/tap/gentle-ai`.
- **Recomendadas** (con fallback — si falta, avisá en una línea y seguí degradado):
  - `codegraph` — ubicar el símbolo/archivo a tocar sin leer de más. Fallback: grep/Read. Instalar: CLI npm global; init por proyecto con `gentle-ai codegraph init --cwd <repo>`.
  - `serena` — navegación/edición a nivel símbolo. Fallback: codegraph/grep. Instalar: `uv tool install -p 3.13 serena-agent && serena setup claude-code`.
  - `engram` — continuidad opcional. Fallback: ninguna — shot no deja artefacto durable por diseño. Instalar: viene con gentle-ai (`brew install gentleman-programming/tap/gentle-ai`).

Chequeo: `command -v <tool>` (CLI) o `claude mcp list` (MCP, p.ej. serena). Si falta una obligatoria, no sigas.

## Reglas duras

> **#1 — Gate de entrada: shot es para lo TRIVIAL y ENTENDIDO, no para lo chico-pero-incierto.** Shot aplica solo si: el Qué/Done son obvios, no hay decisiones que **necesiten diseño**, el blast radius es mínimo (1-3 archivos), no hay migración, ni contrato/endpoint nuevo, ni UI nueva. Una decisión **decidible con una pregunta** (opciones conocidas, el humano elige) NO te saca de shot: hacé esa pregunta y seguí. Solo una decisión que **necesita diseño** (arquitecturas con tradeoffs a investigar) sube a organic/loop. El criterio NO es el conteo de líneas — es la **ausencia de incertidumbre y de ceremonia necesaria**. Si falta algo de eso → NO es shot: rebotá a `/mala-pata-organic` (o `/mala-pata-loop` si hay decisiones de diseño, `/mala-pata-roadmap` si es multi-unidad).

> **#2 — NUNCA un worktree. Esto es lo que hace a shot rápido — es el único carril que trabaja in-place.** NO crees ni uses un worktree bajo ninguna circunstancia; crear un worktree es exactamente lo que shot evita (si creés que hace falta uno, no era shot → rebotá a organic/loop). Trabajás in-place, pero **NUNCA tocás `main` directo**. Si estás parado en una rama protegida (`main`/`development`), **branch-first**: creá una rama corta `<tipo>/<slug>` (`fix`/`chore`/`refactor`/`docs`) y commiteá ahí. Si ya estás en una feature branch, commiteá en esa misma. El worktree se saltea; la rama segura NO.

> **#3 — Rutas absolutas SIEMPRE** en todo comando git/lectura/escritura (`git -C <ABS-repo> …`). Antes de editar o commitear: `git -C <ABS-repo> rev-parse --abbrev-ref HEAD` debe devolver una rama que NO sea `main`/`development`. Si devuelve una protegida, aplicá #2 antes de escribir.

> **#4 — Una sola pasada.** No hay kickoff, no hay fase de start, no hay gates ceremoniales. Si te encontrás queriendo abrir un feature-doc, un preview o un smoke test, es señal de que el cambio NO era shot (ver #1) — rebotá a organic.

## Flujo (ODD direct-inline, en una pasada)

1. **Autorizar (ODD paso 1).** ¿El pedido autoriza un cambio? Investigación/explicación/review/comparación = read-only → respondé directo, sin tocar nada. Solo si autoriza cambio, seguís.
2. **Rama segura (sin worktree) — Regla #2/#3.** `git -C <ABS-repo> rev-parse --abbrev-ref HEAD`. Si es `main`/`development` → `git -C <ABS-repo> switch -c <tipo>/<slug>` (branch-first) y confirmá el tipo en una línea. Si ya estás en una feature → quedate ahí. No se crea worktree.
3. **Entender (1-3 archivos).** Ubicá lo que hay que tocar (codegraph/serena, o grep/Read de fallback). **Si necesitás 4+ archivos, o aparece una decisión de diseño, o el blast radius crece → PARÁ** (Regla #1): no es shot, rebotá a `/mala-pata-organic`.
4. **Editar + checks.** Aplicá el cambio con el **modo TDD del proyecto**: si strict TDD está on, Red → Green → Refactor; si no, checks funcionales puntuales. Corré el **check que prueba este cambio** (no la suite entera, salvo que sea barata). Nunca des por hecho sin ver el check en verde.
5. **Work-unit commit.** `git -C <ABS-repo>` con pathspec explícito y Conventional Commit. Si **RDD está on**, tras el commit corré `gentle-ai review assess --cwd <ABS-repo> --json` y seguí el plan nativo (en trivial casi siempre da passive). El detalle completo del RDD vive en el ODD protocol del CLAUDE.md — no lo reimplementes.
6. **Cerrar.** Reportá el resultado verificado + el check que corriste + próximo paso en 1-2 líneas. **Push, PR y merge quedan a decisión del humano** (shot no abre PR solo salvo que lo pidas). Sin feature-doc ni tabla ceremonial — un cierre de una línea alcanza.

## Guard de escape (Regla #1, pero a mitad de camino)

Si arrancaste como shot y a mitad descubrís que el cambio NO era trivial (apareció una decisión, el blast radius creció, hace falta diseñar o migrar) → **PARÁ, no fuerces shot**. No commitees algo a medias o roto; dejá el trabajo en la rama y recomendá subir a `/mala-pata-organic` (o `/mala-pata-loop` si hay decisiones de diseño). Forzar shot sobre algo que creció es exactamente lo que este carril evita.

## Qué NO hace shot

- NO crea worktree.
- NO escribe feature-doc ni kickoff.
- NO hace preview ni smoke test (si el cambio los necesita, no era shot).
- NO despacha agentes `sdd-*`.
- NO pushea, abre PR ni mergea por su cuenta — eso queda al humano.
