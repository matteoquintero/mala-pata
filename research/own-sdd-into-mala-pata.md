---
idea_slug: own-sdd-into-mala-pata
project: mala-pata-skills
domain: mala-pata-sdd
roadmap: none
verdict: PROCEED
created_at: 2026-10-29T00:00:00Z
next: triage
size_signal: multi-unit
---
# Research: own SDD into mala-pata (survive gentle-ai 4.x SDD retirement)

## Verdict: PROCEED
gentle-ai 4.1+ `sync` DELETES the 12 `sdd-*` agents, the `sdd-*` skills and the canonical
orchestrator manual; mala-pata's `loop` lane depends on them, so ownership must happen BEFORE the
upgrade. The idea is solid and sized as a roadmap (several open architecture decisions). One design
fork was resolved with the user (manual placement = lazy-load, mala-pata-owned).

## Raw idea (what you asked)
Bring gentle-ai's retiring SDD (12 `sdd-*` agents + `sdd-*` skills + `_shared/sdd-orchestrator-workflow.md`)
INTO mala-pata — NOT copy-paste, but ADAPTED to the family so it runs in any project without gentle-ai
installed. gentle-ai is ODD-only now; mala-pata routes via research + triage, so SDD is the `loop` lane.
Own the orchestrator knowledge as `## Mala Pata Workflow` (lazy-load, mala-pata-owned). `preview` stops
being an override injected into the SDD workflow and becomes a NATIVE phase. `loop`/`loop-start` keep
their shape; document how they drive this now-owned SDD. Must survive the 4.1+ sync and not leave a
dangling pointer in the global CLAUDE.md.

## Discover

### How it's done today + limits (with sources)
- gentle-ai `v4.0.0` ("SDD Retires, ODD Leads", 2026-10-01) removed SDD from the product: `/sdd-*`
  commands, phases/profiles, OpenSpec, and the subcommands `sdd-status` / `sdd-continue` / `sdd-attempt`
  / `sdd-preflight-hook`. `v4.1.0` ("Clean SDD Exit", 2026-10-12) makes `sync`/`install` DELETE the
  Gentle-owned SDD agents, skills, commands, the Claude preflight hook, and profiles from disk.
  (Source: GitHub Gentleman-Programming/gentle-ai release notes v4.0.0 / v4.1.0.)
- Limit of "just keep the old binary": staying on 3.7.0 freezes every other fix; the files survive only
  until the next `sync`. Ownership is the only durable path.
- The config-ownership pattern (keep your agent's workflow instructions in files YOU own, so a tool's
  uninstall cannot delete them) is the standard answer; external research adds little beyond that — the
  value here is anchoring to the real files, done below.

### What exists in the code (real anchoring)
- **Canonical manual** `~/.claude/skills/_shared/sdd-orchestrator-workflow.md` (276 ln): most complete,
  but HEAVILY coupled to gentle-ai — 17 references to `gentle-ai sdd-status/continue`, `sdd-preflight-hook`,
  the native dispatcher (`artifactStore` / `nextRecommended` / `blockedReasons`) and the `AskUserQuestion`
  SDD Session Preflight hard-gate. Uses `/gentle-sdd-*` command names. Gentle-owned → deleted on sync.
- **Embedded copy** `~/AGENTS.md` `## SDD Workflow` (ln 267-640): lighter (2 gentle-ai references), uses
  old `/sdd-*` command names, includes a "Small Model" variant. User-owned → survives sync. Diverged from
  canonical: 141 lines only-canonical, 76 only-AGENTS (same substance, different wording/headers).
- **Global pointer** `~/.claude/CLAUDE.md` ln 348 `## SDD Workflow (lazy-loaded)`: does NOT embed detail,
  only points to the `_shared/` file. User-owned → survives, but becomes a DANGLING pointer after sync.
- **12 executors** `~/.claude/agents/sdd-*.md` (apply, archive, design, explore, init, onboard, propose,
  research, spec, tasks, verify) — Gentle-owned → deleted on sync. `sdd-preview` is a symlink to the
  user's `.agent-skills/sdd-preview/` → user-owned, survives.
- **12 skills** `~/.claude/skills/sdd-*/` — the user-invocable/loadable twins of the agents.
- **mala-pata family already wraps this**: `loop` (writes the SDD kickoff) + `loop-start` (runs the cycle,
  dispatching the `sdd-*` agents), plus `sdd-preview` as the mandatory human gate between tasks and apply.
  So mala-pata already ORCHESTRATES SDD; what it does not yet OWN is the executors + the manual.

### Jobs-to-be-done
As the owner of the mala-pata suite, I need the SDD cycle to keep running after gentle-ai drops it, so that
my `loop` lane (the design-first path for changes with open architecture) does not break when I upgrade.

### Problem dimension (scope / frequency / severity)
- **Scope**: 24 files (12 agents + 12 skills) + 1 canonical manual + 2 owned docs to edit (CLAUDE.md,
  AGENTS.md) + the `loop`/`loop-start`/`sdd-preview` wiring. The whole `loop` lane depends on it.
- **Frequency**: one-time migration, but the trigger (sync deletion) fires the moment the user upgrades —
  so it is time-boxed BEFORE `brew upgrade gentle-ai && gentle-ai sync`.
- **Severity**: high. If sync runs first, the executors and manual are gone and `loop`/`loop-start` break
  with no local source to recover from (only the AGENTS.md copy of the manual survives, not the agents).

### Problem vs proposed solution
| Piece | Class | Evidence | Provenance |
|---|---|---|---|
| Own + adapt the orchestrator manual (lazy-load, mala-pata-owned file) | necessary | canonical `_shared/` deleted on sync; user chose lazy-load | [noted] |
| Short `## Mala Pata Workflow` pointer in CLAUDE.md + AGENTS.md | necessary | replaces the dangling `## SDD Workflow (lazy-loaded)` pointer at CLAUDE.md:348 | [noted] |
| Bring the 12 `sdd-*` executors (adapted, decoupled) | necessary | `~/.claude/agents/sdd-*.md`, Gentle-owned, deleted on sync; loop-start dispatches them | [inferred] |
| Make `preview` a native phase (not an override) | necessary | user decision; `sdd-preview` already a user symlink | [noted] |
| Fix the dangling CLAUDE.md:348 pointer | necessary | points to a file sync will delete | [inferred] |
| Strip gentle-ai native dispatcher coupling (`sdd-status`/`continue`/preflight-hook) | necessary (DROP, not bring) | 17 refs in canonical; subcommands removed in 4.x | [inferred] |
| The 12 `sdd-*` skills (twins of the agents) | verify (dedup) | agents vs skills overlap; loop-start uses the AGENTS as executors | [inferred] |
| gentle-ai `AskUserQuestion` SDD Session Preflight hard-gate | derivable | mala-pata `loop` already has its own profile/gates | [inferred] |
| OpenSpec artifact store | already-exists / drop | mala-pata uses engram + in-repo .md, not openspec | [inferred] |
| Multi-runtime rendering (Codex/OpenCode/Pi) | extra (out) | mala-pata family is Claude-Code-only; "entorno" = any project, not any runtime (assumption to confirm) | [inferred] |

## Heilmeier Catechism
| # | Question | Answer | Provenance |
|---|---|---|---|
| 1 | What are you trying to do? | Own gentle-ai's SDD inside mala-pata (12 executors + the manual, adapted) so the `loop` lane keeps working without gentle-ai. | [noted] |
| 2 | How is it done today + limits? | Today mala-pata orchestrates gentle-ai's SDD via loop/loop-start; limit: the executors + manual are Gentle-owned and deleted on the 4.1+ sync. | [noted] |
| 3 | What is new + why will it work? | Move the manual to a mala-pata-owned lazy-load file + pointer; bring the executors decoupled from the dead native dispatcher. Works because CLAUDE.md/AGENTS.md and mala-pata paths are user-owned, untouched by sync. | [noted] |
| 4 | Who cares? | The user — to not lose the design-first `loop` lane when upgrading gentle-ai. | [asked] |
| 5 | Risks? | Touching global CLAUDE.md/AGENTS.md; 24 files; decoupling the executors from the native dispatcher without breaking the cycle; doing it AFTER sync (too late). | [noted] |
| 6 | Cost / time? | Roadmap of ~6 phases; medium-large meta-work. | [noted] |
| 7 | Success exams? | Intermediate: executors + manual owned, decoupled, preview native. Final: `loop-start` runs explore→archive in a repo with NO gentle-ai; CLAUDE.md pointer resolves; sync does not break anything. | [assumed] |

## Define — sharpened idea (draft for triage)
- **What**: a mala-pata-owned SDD (the `loop` lane) that runs without gentle-ai and survives its sync.
- **Why**: gentle-ai 4.1+ deletes the Gentle-owned SDD executors + manual on the next sync.
- **DoD**: Given a repo with NO gentle-ai installed, When `loop`/`loop-start` run the cycle, Then
  explore→propose→spec→design→tasks→preview→apply→verify→archive completes using mala-pata-owned
  executors + the lazy-load manual, preview is a native gate (not an override), and the global
  CLAUDE.md `## Mala Pata Workflow` pointer resolves to an existing mala-pata-owned file.
- **Decisions already made**: SDD = `loop` lane; routing via research+triage (not ODD-only); manual =
  lazy-load mala-pata-owned + short pointer in CLAUDE.md/AGENTS.md; preview becomes native; loop/loop-start
  keep their shape; strip gentle-ai native-dispatcher coupling.
- **Open decisions** (for triage → roadmap/loop to design): (a) where the 12 executors live to be
  environment-agnostic (keep as Claude Code sub-agents under a mala-pata-owned path vs fold into skills);
  (b) exact decoupling of the native dispatcher (what replaces `nextRecommended`/`blockedReasons` — the
  kickoff file + loop-start phase gates); (c) how preview is wired as a native phase; (d) whether the 12
  `sdd-*` skills are redundant with the agents (dedup).
- **Risk**: medium-high — edits global CLAUDE.md/AGENTS.md and ~24 files; a bad migration breaks the whole
  `loop` lane.
- **Size signal**: multi-unit (roadmap). ~6 phases: (1) own+adapt manual + pointer; (2) bring+decouple the
  12 executors; (3) bring/dedup the skills; (4) preview-native; (5) rewire loop-start docs; (6) fix the
  dangling pointer + sync-survival check.

## DoR (hand-off gate): What ✓ · Why ✓ · DoD ✓ · Decisions ✓

## Handoff
`/mala-pata-triage own-sdd-into-mala-pata` — size signal is multi-unit; triage will likely route to
`/mala-pata-roadmap` to decompose the ~6 phases. Assumption to confirm at triage: "entorno" = any
PROJECT (Claude Code runtime), NOT multi-runtime (Codex/OpenCode/Pi).

Structure: Heilmeier Catechism (DARPA) + Double Diamond (Design Council). Verdict / size-signal / Left-OUT = house method.
