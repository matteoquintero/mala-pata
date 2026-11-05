# mala-pata

*No inventamos la rueda — la orquestamos.*

**mala-pata es una capa de orquestación — una metodología ejecutable — para desarrollo asistido por IA (Claude Code / Codex): decide *cómo* encarar cada cambio y lo corre por su propio flujo de trabajo — carriles y fases, con gates humanos y aislamiento por worktree.**

No es un *copilot* ni un autocompletado: **gatea** (checkpoints humanos donde importa) y **verifica** (nada se da por hecho sin prueba). Orquesta un **motor SDD/ODD** en vez de reinventarlo — hoy **[gentle-ai](https://github.com/Gentleman-Programming/gentle-ai)**, aunque empezó sobre **[Spec Kit](https://github.com/github/spec-kit)** de GitHub — y le pone encima el flujo. Cada decisión se apoya en un **marco estándar de la industria** (no en criterio inventado), y está **investigada y probada en proyectos reales**.

## Qué es — y qué no

- **Es:** una capa de orquestación / metodología sobre un motor SDD/ODD (hoy gentle-ai). Enruta el trabajo, genera el contexto, corre el ciclo con gates y worktrees aislados, y radiografía el estado contra git.
- **No es:** un copilot, un autocompletado, ni "generá código y listo". No adivina: **gatea** (checkpoints humanos donde importa) y **verifica** (nada se da por hecho sin prueba).

## El flujo (el corazón)

La puerta de entrada es `triage`; antes, si la idea es cruda, `research` la afila. Triage decide el **carril**:

- **`shot`** — cambio trivial, entendido, sin ceremonia.
- **`organic`** (ODD) — el carril por defecto: explorar → implementar task-by-task.
- **`loop`** (SDD) — cambio que **necesita diseño**, con un **preview** humano antes de aplicar.
- **`roadmap`** — objetivo grande → **DAG** de fases del tamaño de una unidad.
- **`spike`** — cuando *no sabés cómo*: una investigación acotada (read-only) que devuelve una decisión antes de comprometer trabajo.

Transversal a todo: **worktree aislado** por cambio, **gates humanos** en los puntos sensibles, **RDD** (review por commit) y un **barrido de completitud** que detecta lo que falta ("profesionalmente te falta X") antes de rutear.

## Origen — de Spec Kit a su propio flujo

mala-pata nació como un **flujo SDD propio sobre [Spec Kit](https://github.com/github/spec-kit)** (GitHub): solo el ciclo de especificación *antes* de tocar código. Después **trasladé el motor a [gentle-ai](https://github.com/Gentleman-Programming/gentle-ai)** (sin reinventarlo) y construí encima **mi flujo**. Hoy mala-pata es **mucho más que SDD**: un pipeline completo (`research → triage → carriles`), radars de estado, orquestadores por olas, un **icebox** (backlog diferido), una familia de **documentación**, **spikes** por tipo de incógnita, y un **centro de verdad** de reglas compartidas que todos los skills aplican igual.

## Qué es de quién (atribución honesta)

- **gentle-ai = el motor** (NO incluido en este repo, se instala aparte): fases `sdd-*`, `engram` (memoria persistente), **RDD** (receipt-driven review), **ODD** (organic-driven development), judgment-day, integración con CodeGraph.
- **mala-pata = el flujo**: toda la capa `mala-pata-*` (30+ skills propios) + **`sdd-preview`** (gate humano de plan entre `tasks` y `apply`, que gentle-ai no tiene). El SDD de gentle-ai está **vendorizado** como `mala-pata-sdd-*` para sobrevivir a sus syncs.

> En una línea: **gentle-ai pone el motor; mala-pata pone el flujo.**

## Los skills, por familia (30+ propios)

- **Carriles (ejecución):** `shot` · `organic` (+`-start`) · `loop` (+`-start`)
- **Pipeline / ruteo:** `research` (afila la idea; + modo `--spike`) · `triage` (puerta de entrada) · `roadmap` (descompone)
- **Radars (estado read-only vs git):** `radar` · `roadmap-radar` · `domain-radar` · `icebox-radar`
- **Orquestadores (lotes por olas):** `organic-orchestrate` (+`-start`) · `roadmap-orchestrate` (+`-start`)
- **Icebox (backlog diferido):** `icebox` (congelar) · `icebox-defrost` (+`-start`) (descongelar → rutear)
- **Documentación:** `dossier` (discovery) · `runbook` (+`-start`) · `playbook` (+`-start`) · `walkthrough` (+`-start`) · `standards` · `states` · `gaps`
- **Visual:** `art` (design director)
- **Testing / fixtures:** `seed`
- **Meta:** `skill` (autoría de los propios skills, con context-leak gate)

→ Mapa completo *skill → fundamento*: [`mala-pata/skill-structure-index.md`](mala-pata/skill-structure-index.md).

## En qué nos paramos (no inventamos el criterio)

Cada skill se apoya en un marco estándar de la industria:

| Familia | Marco |
|---|---|
| `research` | Heilmeier Catechism (DARPA) + Double Diamond + JTBD + barrido de completitud (gap analysis / MECE / ISO 25010) |
| `triage` / gates | Definition of Ready + INVEST + el discriminador de carril (Cynefin: loop vs spike) |
| `roadmap` | Minto / MECE + regla del 100% + vertical slices (INVEST) + DAG de dependencias |
| spikes | XP Spike (investigación acotada) + perfiles por tipo (infra / data / integración) |
| doc-authoring | Diátaxis + BDD living documentation + runbooks-as-instructions |
| `art` | Gestalt + Swiss + Bauhaus + Rams + Norman + Laws of UX + Refactoring UI + Atomic Design + Value-Sensitive Design |
| entrega | work-unit commits / chained PRs (presupuesto de review ~400 líneas) |

El motor (SDD/ODD/RDD/engram) es de gentle-ai; los frameworks son estándar de la industria; mala-pata pone el **flujo** que los une.

## `_shared/` — el centro de verdad

Reglas canónicas que los skills aplican **verbatim** (una sola fuente, sin drift entre skills): `lane-gate` (ruteo + discriminador loop/spike), `objective-completeness` (qué falta + fork test), `domain-rule`, `git-truth` (done = git, nunca un checkbox), `test-db-guard`, `execution-strategies` (interface-first), `bug-entry-check` (`kind: bug`), `spike-catalog` (+ perfiles `spike-infra` / `-data` / `-integration`), `structural-labels`.

## Relación con la instalación viva

**Este repo es una COPIA para versionar, no la fuente viva.** Los skills que Claude Code / Codex ejecutan viven en `~/.agent-skills/<skill>`, symlinkeados desde `~/.claude/skills/` y `~/.codex/skills/`. Este repo **no está symlinkeado** — puede quedar desactualizado respecto a `~/.agent-skills`. Para sincronizar la copia con lo vivo:

```bash
cd <este-repo>
for d in ~/.agent-skills/mala-pata-* ~/.agent-skills/_shared; do
  name=$(basename "$d"); rm -rf "$name" && cp -R "$d" "$name"
done
git add -A && git commit -m "sync: snapshot de ~/.agent-skills"
```

## Crédito

Construido sobre **[gentle-ai](https://github.com/Gentleman-Programming/gentle-ai)** de Gentleman Programming. El motor SDD / ODD / RDD / engram / judgment-day / CodeGraph es de gentle-ai; la capa de orquestación `mala-pata-*` y `sdd-preview` son aporte propio.
