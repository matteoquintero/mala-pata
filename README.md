# mala-pata-skills

Skills propias del sistema **mala-pata** (capa de orquestación SDD sobre Claude Code + gentle-ai). Versionado para respaldo e historial.

## Skills

| Skill | Qué hace |
|---|---|
| `mala-pata-loop` | Genera el kickoff (archivo `.md` en carpeta hermana del proyecto + puntero en engram). |
| `mala-pata-loop-start` | Corre el ciclo SDD completo desde el kickoff (explore → … → archive) con gate por fase. |
| `mala-pata-loop-orchestrate` | Planifica un lote de kickoffs (olas, conflictos, splits) — read-only. |
| `mala-pata-loop-orchestrate-start` | Lanza el lote en paralelo (worktree + tab por kickoff). |
| `mala-pata-radar` | Descubre (engram) y diagnostica (git) los SDD por proyecto o `global` — read-only. |
| `mala-pata-organic` | Fast-lane para cambios chicos ya entendidos, sin ciclo SDD completo. |
| `sdd-preview` | Override custom de la fase preview: resumen en cristiano + self-assessment 0/1/2 reviewers + gate anti-sello (una sola pasada). |

## Relación con la instalación viva

⚠️ **Esto es una COPIA para versionar, no la fuente viva.** Los skills que Claude Code / Codex ejecutan viven en `~/.agent-skills/<skill>` y están symlinkeados desde `~/.claude/skills/` y `~/.codex/skills/`.

Este repo **no está symlinkeado** — puede quedar desactualizado respecto a `~/.agent-skills`. Para sincronizar la copia con lo vivo:

```bash
for s in mala-pata-loop mala-pata-loop-start mala-pata-loop-orchestrate \
         mala-pata-loop-orchestrate-start mala-pata-radar mala-pata-organic sdd-preview; do
  rm -rf "$s" && cp -R "$HOME/.agent-skills/$s" "$s"
done
git add -A && git commit -m "sync: snapshot de ~/.agent-skills"
```
