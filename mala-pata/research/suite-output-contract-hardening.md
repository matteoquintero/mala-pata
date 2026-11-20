---
idea_slug: suite-output-contract-hardening
project: mala-pata-skills
domain: mala-pata-meta
roadmap: none
verdict: PROCEED
created_at: 2026-11-20T10:47:59-0500
next: triage
size_signal: multi-unit
kind: research
---
# Research: make the mala-pata suite tables-only (no narrative), idempotent, and safe

## Verdict: PROCEED
The objective is sound and multi-unit, but with a SHARP caveat the evidence forces: **a prompt rule alone does not enforce tables-only** — `mala-pata-roadmap-radar` ALREADY declares "Fixed, immutable output format" and the roadmap skill ALREADY bans the stacked `#: N` block, yet the triggering run emitted narrative paragraphs + that exact banned block. Three shared contracts + a suite sweep will materially raise compliance and consistency, but **full enforcement needs a harness-level validator** (a hook that rejects non-table output), which is the real backstop and a named spike. Proceed with the shared contracts now, with that enforcement truth stated, not hidden.

**User refocus (2026-11-20):** the CORE ask is **tables-only / no narrative, made RELIABLE** ("muy seguro" = output reliably IS tables, not best-effort). **Idempotency and safety are NOT the goal** — they become OPPORTUNISTIC fixes (done only when a skill being touched already shows a blind-append or an ungated mutation), never a dedicated sweep. DoD-1 + the enforcement mechanism (DoD-4) are core; DoD-2/DoD-3 are optional. See the Spike finding below.

## Spike finding (Phase 0) — enforcement mechanism [resolved]
The pivotal unknown: what makes tables-only RELIABLE, not best-effort. Evaluated against the real runtime:

| Option | Feasible here? | Verdict |
|---|---|---|
| **Fill-in template** — the skill's close is an EXACT table skeleton the model fills, with "emit ONLY this filled block" | yes, zero-infra | **CHOSEN (primary)** — removes the room to narrate; strongest simple lever |
| **Pre-emit self-check** — the skill's last step re-reads its own output and rewrites any line that is not a table row / labeled block / the single BLUF line | yes, zero-infra | **CHOSEN** — catches drift the template misses |
| **Self-review subagent** — the skill delegates its drafted deliverable to a fresh reviewer that returns pass / rewrite | yes, costs one subagent call | fallback for the worst offenders only (cost) |
| **Scoped Stop-hook validator** — a mala-pata-scoped Stop hook lints the deliverable and BLOCKS on narrative → forces re-emit | yes — Stop hooks exist, CAN block + feed a reason, user already runs Stop hooks (verified in settings.json); needs a marker so it fires ONLY on mala-pata output | **OPTIONAL hard backstop** — its own slice, added only if template+self-check still drift |
| Global tables-only Stop hook | no | REJECTED — fires on every reply, would block ordinary chat prose |
| Provider constrained-decoding / forced tool schema | no | REJECTED — skills emit chat TEXT, not tool calls; no decoding access in the Claude Code skill runtime |

**Chosen mechanism:** fill-in template + pre-emit self-check (core, zero-infra) → scoped Stop-hook as an OPTIONAL hard backstop. **Residual unknown:** how much narrative template+self-check actually remove on the worst offenders (the radars) — measure after Phase 1; add the Stop-hook backstop ONLY if drift remains. **Effect on decomposition:** phases = (1) output contract + fill-in templates, (2) sweep (reference + rewrite closes, priority radars/orchestrators/research), (3) OPTIONAL scoped Stop-hook backstop; idempotency/safety stay opportunistic, not phases.

## Raw idea (what you asked)
"Haz un research de cómo podemos hacer [la suite] más idempotente, más segura, que no haya narrativa… necesito que mala-pata sea SOLO TABLAS, todo." Trigger: a `roadmap-radar` run (image) emitted long narrative prose ("Four of the five phases are already in development…", "On the icebox: there isn't one for this…") followed by the BANNED per-phase stacked block (`#: 1` / `Phase:` / `slug:` / `Route:` / `Status:` / `Evidence:`).

**Objective (the OUTCOME, not the wording):** every mala-pata skill emits a **deterministic, scannable, structured deliverable** — tables + fixed labeled blocks, no narrative paragraphs — AND behaves **idempotently** (re-runs don't drift/duplicate) and **safely** (no silent mutation; a gate before anything outward/destructive). The gap is the distance between that and what the suite does today.

## Discover

### How it's done today + limits (with sources)
Enforcing prose-free / structured LLM output is a known, UNSOLVED-by-prompt-alone problem:
- Natural-language format instructions are treated as a **soft preference**, not a hard constraint; compliance **erodes in long conversations and on unusual inputs** ([synapse-ai troubleshooting note](https://ddaekeu3-cyber.github.io/synapse-ai/solutions/prompt-engineering/agent-generates-inconsistent-output-format-across-sessions), anecdotal). Benchmarks report models **emit explanations despite explicit instructions forbidding it** ([Embodied Agent Interface, arXiv 2410.07166](https://arxiv.org/pdf/2410.07166)).
- The RELIABLE enforcement is **outside the model**: provider-level constrained decoding (only possible with decoding access, breaks through adapters — [RL-Struct, arXiv 2512.00319](https://arxiv.org/pdf/2512.00319)), a **forced tool schema** (`tool_choice=any`), or **validate-and-retry/reject in code** ([Think Inside the JSON, arXiv 2502.14905](https://arxiv.org/pdf/2502.14905)). A "tables-only" rule is **mechanically checkable** (reject any non-table line) → the VALIDATOR should own the contract, not the prompt.
- **Idempotency / safety** (general engineering, not novel): upsert-by-stable-id (never blind append), derive-state-live (don't accumulate), idempotency key / near-duplicate detection; write-only defaults, explicit confirmation gates before irreversible/outward actions, dry-run/preview. The suite already applies these in places (see below) — the gap is UNIVERSALITY, not invention.

### What exists in the code (real anchoring) — survey of 48 skills (`~/.agent-skills/*/SKILL.md`)
| Dimension | Evidence (grep) | Reading |
|---|---|---|
| Output format rule present | 37/48 mention `table`; 32 "one line per"; 8 "fixed format"; only **17/48 reference `_shared/mala-pata-structural-labels.md`** | Rules exist but are **INCONSISTENT** — half the suite has no shared label/format anchor. [verified] |
| Anti-prose rule present | 22/48 mention "narrative"/"prose"; the radars (`roadmap-radar`, `domain-radar`, `icebox-radar`) each declare "Fixed, immutable output format" / "ONE real Markdown table (NEVER fenced, never prose)" | The strongest offenders in the image ALREADY have the rule → **salience/enforcement failure, not absence**. [verified] |
| "BANNED" shape named | only **2/48** (`roadmap`, roadmap's radar neighborhood) | The banned-block rule is local, not a shared contract. [verified] |
| Idempotency | only **12/48** mention `idempoten` (icebox, standards, seed, walkthrough, loop/organic, xray, runbook…) | 36/48 say nothing about re-run behavior. [verified] |
| Safety | **27/48** have write-only/"do NOT commit"; **10/48** have `GATE`; the 9 git-mutating skills are the lanes/orchestrators (expected, gated) | Safety is the **best-covered** dimension; the gap is the non-lane file-writers without an explicit idempotency+write-only statement. [verified] |
| No `table` word at all | `create-image-explain`, the **sdd-* agents** (design/spec/verify/propose/explore/archive/onboard/research), `mala-pata-skill` | sdd-* agents are JSON/delegated (may be fine); the rest are candidates for free narrative. [verified] |

**Existing reuse to build on (reuse-first):** `_shared/mala-pata-structural-labels.md` is already the canonical "frozen labels, verbatim English" rule referenced by 17 skills — the SAME pattern a new output/idempotency/safety contract would use. `deploy-shared.sh` + the prefixed-symlink mechanism already distributes shared rules to every skill root. So the delivery mechanism EXISTS; what is missing is the contracts themselves + universal referencing + the enforcement backstop.

### Jobs-to-be-done
As the suite owner (and every human/agent reading mala-pata output), I need **every** skill's deliverable to be a deterministic table/block I can scan in seconds and trust — never a wall of narrative I have to parse — so the suite reads "architecturally, like the big teams," and re-runs/writes never corrupt state or do something irreversible silently.

### Problem dimension (scope / frequency / severity)
- **Scope**: the whole suite — 48 skills; output-format inconsistency affects ~31/48 (no shared anchor), idempotency ~36/48 (unstated). [verified via grep]
- **Frequency**: every single skill run produces output → felt constantly; the narrative drift recurs on the long-reasoning skills (radars, orchestrators, research). [inferred]
- **Severity**: medium-high for usability/trust (unscannable output defeats the suite's purpose), low-to-medium for correctness (idempotency/safety gaps are real but partly covered); the narrative drift is the acute, visible pain. [inferred]

### Problem vs proposed solution
| Piece | Class | Evidence | Provenance |
|---|---|---|---|
| Tables-only / no-narrative output | **necessary** | 31/48 lack a shared format anchor; radars have a rule that still failed | [verified] |
| A universal shared OUTPUT contract (`_shared`) | **necessary** | `structural-labels` proves the pattern; referencing is inconsistent | [verified] |
| A shared IDEMPOTENCY contract | **necessary** | only 12/48 mention it | [verified] |
| A shared SAFETY contract | **necessary** (lighter) | 27/48 already write-only; consolidate + fill gaps | [verified] |
| "SOLO TABLAS" taken literally (zero prose) | **derivable→sharpen** | would break research's verdict line, triage's decision line, mandated questions | [noted] — sharpen to "no narrative paragraphs; ≤1 BLUF/decision line; everything else tabular/blocks" |
| A harness-level output VALIDATOR (hook rejects non-table output) | **necessary for FULL enforcement, but a spike** | web evidence: prompt alone is a soft preference; roadmap-radar proves it | [verified] — the real backstop; sized separately |
| Rewriting each skill's close to a table | **necessary** (the sweep) | ~31 skills to align | [verified] |

## Heilmeier Catechism
| # | Question | Answer | Provenance |
|---|---|---|---|
| 1 | What are you trying to do? | Make every mala-pata skill emit tables + fixed blocks (no narrative), behave idempotently on re-run, and never mutate/act outward silently. | [asked] |
| 2 | How is it done today + limits? | Per-skill prose rules, inconsistently applied (17/48 share labels; 12/48 idempotency); prose rules are a soft preference the model drops under load — proven by the roadmap-radar run. | [verified] |
| 3 | What is new + why it works? | THREE shared canonical contracts (output / idempotency / safety) referenced by every skill (reuse the `structural-labels` + `deploy-shared.sh` pattern) + a fill-in template + a pre-emit self-check; PLUS a harness validator as the enforcement backstop. Consistency + salience + a mechanical check is what prompt-only is missing. | [noted + sourced] |
| 4 | Who cares? | The suite owner and every reader/agent of mala-pata output; the value is felt on every run. | [asked] |
| 5 | Risks? | A shared rule that is referenced but still ignored (the exact failure observed) → the strategy MUST include the self-check + the harness-validator spike, or it repeats the roadmap outcome. Over-literal "zero prose" would break legitimate BLUF/verdict/question lines. | [verified] |
| 6 | Cost / time? | The STRATEGY is this doc. Adoption = 3 shared contracts + referencing + a close-rewrite sweep across ~31–48 skills + 1 validator spike → multi-unit, a roadmap with per-skill-class phases. | [noted] |
| 7 | Exams of success? | A re-run of any skill emits only tables/blocks + ≤1 BLUF line (no paragraph, no `#: N` block); writing a file twice yields an identical file; no skill commits/pushes/deletes without a gate. | [asked] |

**Assumption challenge:** the idea's premise is "a shared tables-only rule will make the suite tables-only." The evidence **contradicts it**: `roadmap-radar` already has "immutable output format" and the roadmap already bans the stacked block, yet both failed in the triggering run, and external sources say prompt-level format is a soft preference. → The shared contract is NECESSARY but NOT SUFFICIENT; the strategy only works if it also lands the pre-emit self-check and the harness-validator backstop. This reframing is the research's contribution (it stops the fix from being "add another rule nobody follows").

## Define — sharpened idea (draft for triage)
- **What** — three shared canonical contracts referenced by every skill + a per-skill close aligned to tables + a harness-validator spike: deterministic tables-only output, idempotent writes, safe (gated) mutation across the whole suite.
- **Why** — every run must be scannable and trustworthy; the current prose-drift + inconsistency defeats the suite's purpose.
- **DoD(s)** (one per requested rule — none dropped):
  - **DoD-1 (tables-only / no-narrative):** Given any skill run, When it emits its deliverable, Then the body is tables + fixed labeled blocks with **at most one BLUF/decision line**, with **no narrative paragraph** and **no banned stacked `#: N` block**; each skill references `_shared/mala-pata-output-contract.md` and runs a **pre-emit self-check** (scan own output; any non-table/non-block/non-BLUF line → rewrite).
  - **DoD-2 (idempotent) — OPTIONAL / opportunistic, NOT a phase:** When a skill being touched for the output work already shows a blind append or re-run drift, fix it to upsert-by-stable-id / derive-state-live in passing. Not a dedicated sweep; a shared idempotency contract only if the opportunistic fixes converge on one.
  - **DoD-3 (safe) — OPTIONAL / opportunistic, NOT a phase:** When a skill being touched already shows an ungated commit/push/PR/merge/delete/prod mutation, add the gate / make it write-only in passing. Not a dedicated sweep (safety is already the best-covered dimension: 27/48 write-only, the 9 git-mutating skills are gated lanes).
  - **DoD-4 (enforcement — RESOLVED by the spike):** reliability comes from **fill-in templates + a pre-emit self-check** in the output contract (core, zero-infra), with a **scoped Stop-hook validator** as an optional hard backstop only if drift remains after Phase 1. Not a global hook (would block ordinary chat), not provider decoding (skills emit text, not tool calls).
- **Decisions already made** — reuse the `_shared` canonical-rule + `deploy-shared.sh` distribution pattern (do NOT invent a new mechanism); "SOLO TABLAS" = no narrative paragraphs + ≤1 BLUF line, not literal zero prose; the radars/orchestrators/research are the priority offenders.
- **Open decisions** — the enforcement mechanism (harness hook vs self-review vs self-check only) is a real fork → **spike**; whether to touch the sdd-* agents (JSON/delegated — may be out of scope); the exact BLUF-line allowance per skill class.
- **Risk** — a shared rule nobody follows (repeat of the observed failure) if the self-check + validator are skipped; touching every skill's close is broad (contract item 3 — output others consume).
- **Spike candidates** — the output-enforcement mechanism (harness validator vs self-review subagent vs pre-emit self-check); profile: `generic`/`integration`.
- **Size signal** — **multi-unit**: 3–4 shared contracts + a sweep across ~31–48 skills + 1 enforcement spike. Independent vertical slices (output / idempotency / safety / validator) → roadmap with per-dimension phases. Triage/roadmap rule; research does not route.

## DoR (hand-off gate): What ✓ · Why ✓ · DoD(s) ✓ (every requested rule covered) · Decisions ✓
Completeness: lenses swept 4 (output / idempotency / safety / enforcement) · missing 0 critical · forks 1 (enforcement mechanism → spike)

## Handoff
`/mala-pata-triage suite-output-contract-hardening` — pass the DoDs above. Triage owns the roadmap-or-not call; the `multi-unit` signal + four independent DoDs is the hypothesis (a roadmap with phases: output-contract, idempotency-contract, safety-contract, enforcement-spike, then the per-skill-class sweep). The enforcement-validator is the phase that decides whether tables-only is actually achievable or stays best-effort.

Structure: Heilmeier Catechism (DARPA) + Double Diamond (Design Council) + objective-completeness (gap analysis / MECE / ISO 25010) + spike (Cynefin / XP spike). Verdict / size-signal / shared-contract / enforcement-backstop = house method.
