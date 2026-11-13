# mala-pata-sdd-* — owned SDD (survives gentle-ai 4.x)

House-owned SDD for the mala-pata `loop` lane, decoupled from gentle-ai. gentle-ai 4.x retired SDD and its `sync` deletes the gentle-owned `sdd-*`; this copy is self-contained and survives.

- **Executors**: `mala-pata-sdd-<phase>/` (each has a `SKILL.md` + an `agent.md`) for explore · propose · spec · design · tasks · apply · verify · archive · init · onboard · research, plus the user-owned `sdd-preview`. Registered as `mala-pata-sdd-<phase>` agents (symlinked into `~/.claude/agents/`).
- **Shared**: `~/.agent-skills/_shared/sdd-phase-common.md` (engram retrieval / persistence / return envelope) + `~/.agent-skills/_shared/sdd-state.md` (in-house state). Both mala-pata-owned.
- **Manual**: `sdd-orchestrator-workflow.md` (this dir) — the lazy-load orchestration surface the global `CLAUDE.md` points at.
- **State**: engram topics `sdd/<change>/*` + kickoff + git. No native engine, no OpenSpec, no `gentle-ai sdd-*` command.
- **Driven by**: `/mala-pata-loop` (writes the kickoff) + `/mala-pata-loop-start` (runs the cycle).

Decouple COMPLETE: bodies were once a verbatim gentle snapshot (3.7.0, 2026-10-30); they are now rewired to full mala-pata ownership with zero gentle references.
