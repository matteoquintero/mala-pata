# Project policy (declared, versioned) — mala-pata single source of truth

> **Re-read on apply (stale-context guard).** This is a PROCESS canonical — no output signature a hook can check — so the guard is explicit: at the moment you APPLY this rule, re-read THIS file from disk (it is a live symlink; it may have changed since it entered your context) and apply the on-disk version — it wins over any stale copy you hold.

Canonical for the per-project POLICY file `mala-pata/project-policy.md` — a VERSIONED repo file (not
memory) that declares how THIS project delivers, so the lanes stop relying on an agent REMEMBERING it.
`/mala-pata-sdd-init` detects and WRITES it; the lanes and orchestrators READ it. Policy in a declared
field, not in a model's memory (closes class 7).

## The file (`<repo>/mala-pata/project-policy.md`)

```yaml
---
project: <name>
integration_base: main | development | <the branch features merge into>
ci:
  present: true | false        # does the repo run CI on PRs/pushes?
  gate: true | false           # must CI be green before a change lands?
code_delivery: pr | direct     # code changes: open a PR, or push direct to the base?
delivery_strategy: ask-on-risk | auto-chain | single-pr | exception-ok
model_tiers:                   # optional — override the shipped model-policy default (rule: model-policy.md)
  claude: { heavy: opus, standard: sonnet, light: sonnet }   # omit a tier to keep its default
  codex:  { heavy: high, standard: medium, light: low }       # effort levels: low|medium|high|xhigh|max
---
<one paragraph of any project-specific delivery notes a field cannot capture>
```

## Delivery is a 2-entry rule (fork F3)

Delivery depends on the NATURE of the change, not one blanket setting:
1. **Passive / docs-only** — computed from the diff, reusing the existing `passive` verification tier
   (no executable effect) → **direct push** to the base. No PR ceremony for a markdown-only change.
2. **Code / CI / migration** → follow the declared `code_delivery` (`pr` | `direct`). `direct` is legal
   ONLY where the project declares it (a solo repo with no CI may legitimately push to the base); `pr`
   otherwise.

A push / PR / merge is STILL a human decision — the lane never delivers on its own. This field tells
the lane which SHAPE to prepare; it does not grant the act.

## Model tiers (optional override)

`model_tiers` overrides the shipped per-phase model/effort default (canonical: `model-policy.md`). It is
OPTIONAL — omit the whole block to keep the default, or omit a single tier/runtime to keep that one's
default. Resolution is per tier, per runtime: the project value wins, else the default. A value must be a
real Claude model alias or a real Codex effort level (`low|medium|high|xhigh|max`); on an unrecognized
value the lane falls back to the default for that tier and warns in one line (never blocks). This is how a
project runs its own models — e.g. point `light: haiku` to save cost on the read-only lanes.

## Who writes / reads it

- **Writes:** `/mala-pata-sdd-init` detects the fields (integration base from git; `ci` from the repo's
  workflow files; `code_delivery` / `delivery_strategy` from the project's convention — ASK the human on
  ambiguity) and writes the file. Idempotent: re-init updates in place, never duplicates.
- **Reads:** kickoffs inherit it; `organic-start` / `loop-start` read it at delivery; the orchestrators
  read it for the per-tab prompt and the post-merge CI check, and read `model_tiers` to resolve each
  tab's `--model` / reasoning effort at launch (per `model-policy.md` → `wave-launch.md`).

## strict_tdd is NOT a policy field (gentle-ai v4)

Do NOT put `strict_tdd` here. gentle-ai v4 retired SDD and made `strict_tdd` a no-op (test-first is the
default). It stays where sdd-init already computes it for legacy readers, but it is not project delivery
policy and is not migrated into this file.
