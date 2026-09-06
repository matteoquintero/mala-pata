# Reglas base del SDD — invariantes universales (agnósticas de stack y proyecto)

Aplican a **todos los perfiles** (FULL / STANDARD / LITE / MINIMAL) y a **todos los proyectos**.

## Método (no negociable)

- **Ejecución interactiva fase por fase**: cada fase cierra con resumen y **pausa** esperando OK del humano antes de la próxima. **El ritmo NO se pregunta como gate aparte** — este es el único ritmo, siempre. El perfil activo (FULL/STANDARD/LITE/MINIMAL) ya define cuánta explicitud tiene cada gate humano puntual (ver perfiles); no hay una pregunta separada de "¿interactivo o automático?". Un modo automático solo existe si el humano lo pide explícitamente y sin que se le ofrezca como opción (ej. "corré automático hasta X") — nunca se presenta como menú.
- **Artifact store: SIEMPRE `engram`**. NUNCA preguntar `openspec`/`hybrid`/`none` — no es una decisión que se exponga en este setup.
- **Return envelope por fase**: cada fase devuelve `{ status, resumen, artefactos, riesgos, next_recommended }`.
- **Init guard**: antes de arrancar, `mem_search("sdd-init/<project>")`. Si no existe, correr `sdd-init` para detectar stack, testing, convenciones y herramientas del proyecto. Esas quedan en engram como contexto del proyecto — **NO en las reglas del SDD**.
- **Fase 0 (si el change toca UI)**: audit REUSA/ADAPTA/NUEVO + Atomic Design + workshop de componentes (Storybook o el que use el proyecto). El nivel de gate humano lo define el perfil.
- **TDD**: siempre presente. Granularidad (por task vs por feature) la define el perfil.
- **Verify**: siempre presente. Profundidad (liviano/normal/pesado): el perfil da el **default**, pero la EVIDENCIA la puede subir — el perfil se eligió por tamaño/costo ANTES de explore, así que no puede ser la última palabra sobre riesgo. Si el self-assessment de `sdd-preview` detectó señales de riesgo real (auth/pagos/permisos/shell/CI/migración de datos, o patrón sin precedente), el verify sube al menos a **normal** aunque el perfil diga liviano. Un fix de auth de 3 archivos es MINIMAL por tamaño pero NO merece el verify más liviano — el volumen nunca decide el riesgo (mismo principio que el conteo de reviewers).
- **Idempotencia del kickoff**: `mem_search("sdd/<change-name>/kickoff")` antes de crear.
- **Conflicto en vuelo**: `git worktree list` + revisar branches activos. Si hay solape → confirmar con el humano antes de generar.
- **Migraciones (si aplican)**: identificador reservado en engram (`migrations/registry`) — nunca leer de la carpeta.

## Principios de ingeniería (aplican a todo change)

- `clean-architecture` — dependencia hacia adentro; dominio sin framework/ORM/web; screaming architecture.
- `clean-ddd-hexagonal` — `Infrastructure → Application → Domain`; un agregado por transacción; repository por agregado; ports & adapters (nunca controller→repo directo).
- `solid` — SOLID + object calisthenics; Value Objects para conceptos de dominio (nunca primitivos crudos); YAGNI / KISS / DRY-tras-Rule-of-Three.
- `design-patterns` — patrones **emergen del refactor**, no se fuerzan; usar vocabulario de patrón al nombrar.
- `heuristics-and-checklists` — usar **forcing functions** ("no avanza hasta que X"), no recordatorios blandos.
- **SSOT** — todo literal de dominio vive en UN solo lugar; cero duplicación de la verdad.

## Convenciones universales (aplican a todos los proyectos)

### Nombres

- **`change-name`**: kebab-case, conciso, prefijo de dominio/BC cuando ayude. **Sin** sufijos de versión (`-v2`, `-nuevo` → dejan dead code huérfano). Máx ~40 chars.
- **Branch**: `<tipo>/<change-name>` — el **tipo se aconseja según el trabajo y el humano lo confirma** (igual que la branch base). Tipos convencionales (Conventional Branch / git-flow): `feature/` (funcionalidad nueva), `fix/` o `bugfix/` (corrección), `hotfix/` (urgencia en prod), `refactor/` (refactor sin cambio de comportamiento), `chore/` (tooling/build/deps), `docs/` (documentación), `release/` (preparar release). lowercase + guiones, corto y descriptivo. **PROHIBIDO `sdd/...`** como prefijo de rama o worktree — es la convención de topic_keys de engram, NO de git. El `<change-name>` (sufijo) es único e igual pase lo que pase con el prefijo — por eso el radar puede localizar la rama por el `branch:` registrado en el kickoff o por sufijo `*/<change-name>`, sin depender del prefijo.
- **Worktree**: un worktree **por SDD** para aislamiento. **Ruta ÚNICA**: `<ABS-repo>/.claude/worktrees/<change-name>` — el dir es solo `<change-name>` (sin prefijo de tipo, sin `sdd/`), estable para que radar y limpieza lo encuentren.
- **Engram topic keys**: `sdd/<change-name>/{kickoff,explore,proposal,spec,design,tasks,apply-progress,verify-report,archive-report}`.

### Commits

- **Conventional Commits**: `<tipo>(<scope>): <descripción>` — tipos estándar (`feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `build`, `ci`, `style`). El scope lo define el proyecto (detectado por sdd-init).
- **SIN atribución de asistente IA** en commits (`Co-Authored-By: Claude`, `Generated with Claude Code`, cualquier trailer similar). El commit lo firma el humano.
- **NO `git stash`** durante el flujo del SDD — mueve trabajo fuera del historial y complica recuperación en caso de rollback. Usar commits reales (incluso WIP) o dejar en el working tree.
- **NO `--no-verify`** ni `--no-gpg-sign` — respetar hooks del proyecto salvo pedido explícito del humano.
- **NO amend a commits publicados** — cada corrección va en un commit nuevo.

### Branches y PRs

- **NUNCA `git push` directo a `main` / `master` / branch de integración**. Siempre por PR (o el mecanismo de review del repo).
- **PR title**: Conventional Commits format, mismo estilo que los commits.
- **PR body**: incluir (a) resumen de qué cambia, (b) test plan verificable, (c) link/referencia al kickoff en engram (`sdd/<change-name>/kickoff · engram #<id>`).
- **Branch base**: default/recomendado `main` o `development`, pero **cualquier rama es válida si el humano la confirma** (ej.: trabajo que construye sobre una feature en curso sale de ESA feature). Lo NO NEGOCIABLE es la **confirmación**: la base SIEMPRE se propone con su razón ("el código vive en X" / "default de integración") y se espera el OK del humano antes de fijarla — nunca se asume en silencio, nunca se bloquea solo por no ser main. Queda registrada explícita en el kickoff (frontmatter `branch_base`), y esa confirmación vale para todo el ciclo.

### Rutas

- **En código**: rutas relativas al workspace (según el resolver del stack — `tsconfig`, `pyproject.toml`, etc.).
- **En comunicación con el humano**: rutas relativas al repo (no absolutas al filesystem).
- **En comandos de shell**: rutas absolutas (`git -C <abs>`, `--prefix`, paths absolutos), no `cd` para operar en otro directorio.

## Estructura del kickoff (SSOT)

Todo kickoff **DEBE** tener:

1. **Perfil activo** — FULL/STANDARD/LITE/MINIMAL, confirmado por el humano en Paso 1.5. Con reasoning de la propuesta y costo estimado (orden de magnitud).
2. **Metadatos de orquestación** — change-name, branch, worktree, tamaño, depends_on, paralelizable_con, branch base, comando de arranque.
3. **Contrato del change** — endpoints, shapes, tipos, migraciones del BE si aplica. Específico del change, NO del método.
4. **Reinterpretación técnica** — objetivo, problema, IN/OUT, criterios de éxito medibles.
5. **Arquitectura y capas afectadas** — con refs al ARCHITECTURE.md del proyecto (detectado por sdd-init).
6. **Plan de fases alto nivel** — por objetivo, NO por task. Las tasks las produce `sdd-tasks` en la fase correspondiente.
7. **Definition of Done** — criterios verificables de cierre.
8. **Riesgos / decisiones abiertas** — para resolver dentro del SDD.

## Qué NO va en las reglas base

- Herramientas específicas del stack (regen de tipos, comandos de build/test, librerías de UI/testing, formato de archivos) → las detecta sdd-init y viven en el contexto del proyecto en engram.
- Contratos concretos de endpoints, tipos, o payloads → viven en el kickoff del change específico.
- Reglas de proyectos concretos (formato del scope de commits, patrón de branches con prefijos custom, ubicación de worktrees) → viven en el CLAUDE.md del proyecto o en sdd-init.
- Número de reviewers de `sdd-preview` → lo decide el propio `sdd-preview` en su self-assessment (blast-radius / reuse-first / smells de arquitectura), `sdd-tasks` ya no lo recomienda. El perfil no fuerza número.
