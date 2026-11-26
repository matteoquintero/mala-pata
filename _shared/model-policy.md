# Model policy — per-phase cognitive tier → model/effort (mala-pata single source of truth)

> **Re-read on apply (stale-context guard).** This is a PROCESS canonical — no output signature a hook
> can check — so the guard is explicit: at the moment you APPLY this rule (resolve a model for a phase,
> inject a launch flag, or write an agent's `model:`), re-read THIS file from disk (it is a live symlink;
> it may have changed since it entered your context) and apply the on-disk version — it wins over any
> stale copy you hold.

Canonical for assigning a MODEL (Claude) or REASONING EFFORT (Codex) to each mala-pata phase/lane by its
**cognitive weight**, so the suite deliberately spends the heavy model where it pays and the cheap one
where it does not — across BOTH the Claude and Codex runtimes. A phase pins a **tier**, never a model;
the tier→model mapping is **configurable** (a project overrides the shipped default). This is the single
source: a skill, agent, or orchestrator that chooses a model applies THIS verbatim.

## The three tiers (frozen — heavy | standard | light)

The taxonomy is stable; only the mapping to a concrete model/effort is configurable.

| Tier | Cognitive load | What belongs here |
|---|---|---|
| `heavy` | design / open-ended reasoning / an irreversible-if-wrong decision | the work is to DECIDE or DESIGN, and a subtle mistake is costly and hard to see. |
| `standard` | execution / spec / analysis against a known target | the work is to DO a specified change, or analyze with the approach already settled. |
| `light` | mechanical / read-only status / deterministic bookkeeping | the output is trivially checkable and low-consequence if slightly off. |

## Phase / lane → tier (the assignment)

Grounded in published coding/agentic benchmarks (see **Why these tiers**, below): the heavy model earns
its premium only on the hardest reasoning; agentic execution does not need it.

| Tier | Phases / lanes |
|---|---|
| `heavy` | `sdd-design`, `sdd-propose`, `sdd-preview`, `research` (+ spike), `roadmap`, `bug` (root-cause diagnosis), `art` |
| `standard` | `triage`, `organic`(+`-start`), `loop`(+`-start`), `shot`, `sdd-apply`, `sdd-spec`, `sdd-tasks`, `sdd-explore`, `sdd-verify`, `sdd-init`, `sdd-research`, `walkthrough`(+`-start`), `atlas`(+`-start`), `gaps`, `dossier`, `playbook`(+`-start`), `runbook`(+`-start`), `standards`, `states`, `xray`, `icebox-defrost`(+`-start`), `organic-orchestrate`(+`-start`), `roadmap-orchestrate`(+`-start`), `skill` |
| `light` | `roadmap-radar`, `domain-radar`, `radar`, `icebox-radar`, `icebox`, `seed`, `sdd-archive`, `sdd-onboard` |

A phase not listed defaults to `standard` (the safe middle). The `light` bucket is deliberately the
read-only / mechanical lanes: because the shipped default maps `light`→sonnet (see below) it costs
nothing in quality by default, and it is the ONE safe place to point a cheaper model when a project
wants to save cost.

## Tier → model / effort (the DEFAULT — configurable)

This is the shipped default. It uses **only opus + sonnet** on Claude (haiku is a documented, valid
choice for `light`, not the default) and the **reasoning-effort knob on the session's own model** for
Codex (Codex is one model with an effort dial, not several models — the effort is what moves measured
pass@1).

| Tier | Claude (`--model`) | Codex (`model_reasoning_effort`) |
|---|---|---|
| `heavy` | `opus` | `high` |
| `standard` | `sonnet` | `medium` |
| `light` | `sonnet` | `low` |

Aliases (`opus`/`sonnet`/`haiku`) are preferred over pinned 5-family ids so the policy survives model
updates. A project that wants the cheapest `light` sets `light: haiku` (Claude) in its override.

## Override — anyone configures their own models

The default above is overridden per project in `mala-pata/project-policy.md` (the existing declared-policy
file — rule: `project-policy.md`), under a `model_tiers:` block. A declared field, not an agent's memory.

```yaml
model_tiers:            # optional; omit any tier to keep its default
  claude: { heavy: opus, standard: sonnet, light: sonnet }
  codex:  { heavy: high, standard: medium, light: low }
```

**Resolution order (first that exists wins):** the project's `model_tiers.<runtime>.<tier>` → the DEFAULT
table above. Resolve per tier, per runtime — a partial override keeps the default for the tiers it omits.
A value must be a real model alias (Claude) or a real effort level `low|medium|high|xhigh|max` (Codex);
on an unrecognized value, fall back to the default for that tier and warn in one line (never block).

## How it is applied (per surface)

The tier is enforceable only where a model can actually be chosen; elsewhere it is a recommendation.

1. **Agents (`sdd-*`, Claude) — static default in frontmatter.** An agent's `model:` is the DEFAULT for
   its phase's tier, baked in (a subagent cannot read this config at dispatch). This is the one surface
   that is not live-configurable: to change it a project edits the agent frontmatter. Keep the pins
   consistent with the DEFAULT table (heavy→opus, everything else→sonnet).
2. **Orchestrated lanes — injected at launch (`wave-launch.md`).** The orchestrator resolves the phase's
   tier → model/effort (override → default) and passes it so the tab command carries it:
   - Claude: `claude --model <model> "$(cat '<prompt-file>')"`
   - Codex: `codex -c model_reasoning_effort=<effort> "$(cat '<prompt-file>')"`
   This is the real enforcement point for the skill-lanes (a skill cannot change its own session model).
3. **Direct invocation — recommendation only.** A skill invoked directly runs on whatever model the human
   already opened the session with; it cannot force one. Its header may state its tier so the human (or an
   orchestrator) opens it on the right model. Honest limit: enforcement = agents + orchestrated launches.

## Why these tiers (evidence, not guess)

Published coding/agentic benchmarks for the installed families (secondary sources — directional, not
system-card gospel; no SWE-bench Verified reported for these):

- **Claude 5.5, SWE-bench Pro:** Opus 89.9% · Sonnet 81.3% · Haiku 64.8%. Opus's edge is real only on the
  hardest reasoning. On **Terminal-Bench 4.0 (agentic terminal work — what the lanes actually do) Sonnet
  70.6% BEATS Opus 66.4%**, and Sonnet costs ~1/5. So: opus for pure design/reasoning, sonnet for all
  agentic execution. Haiku's agentic drop (39.2%) is why it is not the default for anything autonomous.
- **Codex / GPT-5.6:** the terra/sol/luna models sit within ~2pts on SWE-bench Pro; the **effort dial** is
  the lever that moves pass@1 (higher effort → more tokens → higher pass@1, monotonic). Hence tier→effort
  on one model, not tier→model.

The cutpoints are NOT load-bearing: the mechanism is a declared tier → a configurable mapping, trivially
re-tuned when official numbers land or a project disagrees. The structure (3 tiers, this phase→tier map,
effort-for-Codex) is what is stable.
