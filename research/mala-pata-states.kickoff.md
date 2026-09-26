---
change_name: mala-pata-states
project: mala-pata
route: organic
base: "repo espejo mala-pata-skills @ main; authoring live en ~/.agent-skills/mala-pata-states/"
branch: "N/A — sin worktree; commit directo a main del repo espejo (patrón del suite)"
worktree: "N/A — el skill vive en ~/.agent-skills/ (runtime, no git); el repo es el espejo"
tdd_mode: "N/A — un SKILL.md es instrucciones, no código; verificación por test-run"
created_at: 2026-09-26
---

# Kickoff ODD: mala-pata-states

## Qué
Crear el skill `mala-pata-states`: dado un feature por nombre, extrae del código su(s) máquina(s) de estado (enum de estados + transiciones/guards) y las renderiza con archify (`diagram_type: "lifecycle"`) como HTML fiel, para inspección visual humana.

## Why
Ver la máquina de estados REAL de un feature sin leer el código a mano — onboarding + detectar transiciones rotas/faltantes visualmente. (Fluye al feature-doc y al PR.)

## Done
- Dado un feature con estados explícitos (enum), el comando produce un HTML archify que refleja estados y transiciones REALES del código: si falta una transición en el código, falta en el diagrama — no inventa.
- Las máquinas son ORTOGONALES (una por concern, nunca god-machine) y MÍNIMAS (un estado existe solo si cambia qué acciones se permiten; el resto es metadata). Dimensión combinada → se parte en su propia máquina/columna, o se degrada a campo de metadata.
- El skill NO juzga ni reporta ("no me digas qué está roto") — solo produce el visual fiel; el humano detecta.
- Pasa `archify validate` + `visual-check`.
- Test-run de aceptación: `mala-pata-states pedido` sobre `bodega-ferreteria-colombia` produce el lifecycle de `PedidoEstado`; si se mete a propósito una transición rota en el código, se ve rota en el diagrama.

## Decisiones ya tomadas
- Renderer = archify `lifecycle` (no se reinventa el dibujo); esquema probado en `bodega/docs/diagrams/lifecycle.json`.
- Extracción anclada al código (enum + guards) vía codegraph/read; se dibuja lo REAL.
- El skill no analiza ni reporta; solo produce el visual. Principio **ortogonal + mínimo** = regla dura del propio skill.
- Delivery = authoring live en `~/.agent-skills/mala-pata-states/` → symlink a `~/.claude/skills` + `~/.codex/skills` → sync al repo `mala-pata-skills` + commit a `main`. Sin worktree.
- Sin emojis (preferencia del usuario, aplica al SKILL.md y a cualquier salida).

## Riesgo
Diagrama que miente por extracción incompleta → falso positivo/negativo al detectar transiciones rotas. Mitigación: anclaje estricto al código + dibujar lo real (huecos incluidos) + ortogonal/mínimo (legibilidad) + `visual-check`.

## Dónde (hint opcional — a descubrir en Explore)
- Nuevo: `~/.agent-skills/mala-pata-states/SKILL.md` (+ `references/` si hace falta documentar el esquema `lifecycle` de archify).
- Referencia: la skill archify instalada (`~/.claude/skills/archify`) y el ejemplo `bodega/docs/diagrams/lifecycle.json`.
- Decisión abierta a confirmar al arrancar: **v1 solo enum-explícito, o también estado implícito/scattered.**
