---
idea_slug: edd-as-mala-pata-method
project: mala-pata-skills
domain: mala-pata-suite
roadmap: none
icebox: mala-pata-lanes
verdict: SHARPEN
created_at: 2026-11-03T12:17:06-0500
next: triage
size_signal: small (one optional verification mode; not a lane, not a roadmap)
---

# EDD as a mala-pata method (deep, source-verified)

Evidence tags: [S] fetched and read this session; [M] model memory, unverified; [U] no source found.
Supersedes the shallow 2026-11-02 version. Every claim below tagged [S] was read from the page itself, not from a search snippet.

## Verdict: SHARPEN
"EDD" has four real, distinct meanings and no single official definition. Three have verified, tested material. One (Eval-Driven) is a real gap in mala-pata and has a ready-to-reuse agent skill. The owner must choose the meaning before any house name or structure is decided.

## Raw question
Which "EDD" does mala-pata adopt, and how (lane, orthogonal mode, or nothing)?

## 1. Eval-Driven Development (LLM / agent quality gates)
- **What it is** [S]: top-down approach for AI apps: define what "good" looks like first (about 100 goldens, 3-5 metrics), iterate prompt/model/logic until the metrics pass. DeepEval warns not to map it 1:1 onto TDD: evals are subjective (often LLM-as-judge), costly and slow, so prefer a small high-quality dataset (100 to 500). Source: DeepEval blog, https://deepeval.com/blog/eval-driven-development (no author named). Academic framing [S]: "EDDOps", Xia, Lu, Zhu et al., arXiv 2411.13768, evaluation as a continuous governing function linking offline (dev) and online (runtime) evaluation.
- **Tested source to reuse**:
  - `edd` skill in AndurilCode/craftwork, https://github.com/andurilcode/craftwork, path `plugins/craftwork-context-engineering/skills/edd/SKILL.md`. Verified [S]: repo "63 agent skills", MIT, 8 stars, 2 forks, 112 commits; page https://skills.sh/andurilcode/skills/edd shows 7 installs, security audits passed. Its framing: "TDD is for code. EDD is for context"; applies to prompts/tool defs/retrieval/instructions; use it if a prompt runs more than about 20 times; not for feature code. Caveat: the SKILL.md body was truncated on skills.sh, so the detailed workflow is NOT verified. Low maturity (8 stars).
  - thekevinscott/skillet, https://github.com/thekevinscott/skillet. Verified [S]: MIT, 2 stars, `pip install pyskillet`; evals for Claude Code skills (pass@k, pass^k, lint of SKILL.md). It evals skills, not product LLM features. Very low maturity.
  - Seen only in search, NOT fetched: antongulin/opencode-skill-creator, xbklairith/kisune eval-harness, basecamp/dev-skills skill-crafting, BretFisher/skills.
- **Fit with mala-pata**: REAL GAP. No lane step gates probabilistic-output quality. Neighbours: `tdd_mode` (code tests, deterministic), RDD (reviews code, not behavior scores), `mala-pata-walkthrough` (human/browser QA, not scored evals). Suite skills that mention evaluation do so only as routing pointers to external `evaluation` / `advanced-evaluation` skills [M, grep matched "eval" loosely; not read in full].

## 2. Example-Driven Development (GT / Pharo)
- **What it is** [S]: Nierstrasz, Chis, Girba, "Example-driven development: bridging tests and documentation", arXiv 2409.00514 (2024). Tests are "examples" that return the object under test, so they can be inspected and reused to build further tests; examples stay live and are embedded in live documentation; extends TDD with live programming.
- **Tested source to reuse**: Glamorous Toolkit (https://book.gtoolkit.com/example-driven-development-tutorial-4zfv1bc6gqxy4x08qwpy710f8) returned 404 on fetch [S: failed]; Nierstrasz's post https://www.oscar.nierstrasz.org/posts/2024-04-25-EDD failed TLS verification [S: failed]. So only the arXiv abstract is verified. No agent-skill implementation found [U]. The practice depends on a live-programming environment (GT/Pharo).
- **Fit with mala-pata**: MOSTLY COVERED / n-a. Test-first is `tdd_mode`; "living docs from examples" is `mala-pata-walkthrough` (Given/When/Then that both verifies and documents). Without a live-programming environment there is nothing extra to adopt.

## 3. Experiment-Driven Development (hypothesis + metric + flag)
- **What it is**: change = hypothesis ("believe, cause, because"), one primary metric plus guardrails, sample size from a minimum detectable effect, A/B behind a feature flag, pre-agreed ship/rollback rule. Verified only through a search summary [S: search only] that cites Kohavi (online controlled experiments); I did NOT fetch Kohavi. Fetched https://split.io/?p=6949 [S]: it is a vendor page and does NOT define the method (only product text and SDK steps), so it is not evidence. Sama blog and the GitNation talk returned 404/unfetchable or were not fetched.
- **Tested source to reuse**: `exp-driven-dev` skill in menkesu/awesome-pm-skills (listed on skills.sh, tessl, smithery, lobehub, playbooks.com). Seen in search only; playbooks.com fetch failed TLS [S: failed]. Maturity unverified. Treat as practitioner guidance, not a standard.
- **Fit with mala-pata**: OUT OF SCOPE / n-a. Needs production traffic, flags and analytics; mala-pata is a delivery-process suite with no rollout/analytics step. At most a DoD note in a roadmap.

## 4. Event-Driven Development / Architecture
- **What it is** [S]: not a development methodology under this name. Fowler, "What do you mean by Event-Driven?" (https://martinfowler.com/articles/201701-event-driven.html): "event-driven" is an umbrella over four patterns: Event Notification, Event-Carried State Transfer, Event Sourcing, CQRS. It is an architecture style.
- **Tested source to reuse**: only architecture skills exist, e.g. athola/claude-night-market `architecture-paradigm-event-driven` (fetched [S]: MIT, install via `npx skills add athola/claude-night-market --skill architecture-paradigm-event-driven`; skill body not shown, maturity unverified). Also seen in search only: ddd-event-driven, architecture-event-driven, spring-boot-event-driven-patterns. No "event-driven development" workflow found [U].
- **Fit with mala-pata**: N-A as a method. Architecture choice already handled by the `clean-ddd-hexagonal` skill (domain events, event sourcing, CQRS, outbox in its triggers).

## 5th candidate
None found as a distinct, established meaning. (Search hint only: "Evaluation-Driven" is the same family as meaning 1, EDDOps.)

## Orthogonality (anchor to the suite)
Lanes (shot / organic / loop / roadmap) answer how big and how uncertain a change is. Every EDD meaning is about how a change is verified, like `tdd_mode` and RDD. So the right shape is an optional mode beside lanes, never a fifth lane.

## Recommendation
Most likely intended AND most valuable: **Eval-Driven Development**. It is the dominant current meaning in LLM/agent work, has academic and vendor sources plus a real (if small) SKILL.md, and is the only meaning that is a genuine gap. Shape: an optional `eval_mode` (like `tdd_mode`): DoD includes a versioned eval set (goldens + 3-5 metrics) written before implementation and a recorded pass result before close, applied only to LLM/agent/prompt changes. Reuse-first: study/adapt craftwork `edd` (MIT) rather than invent; verify its full SKILL.md before copying, and keep the DeepEval caveats (cost, small datasets, not 1:1 with TDD). Example-Driven is covered by `tdd_mode` + walkthrough; Experiment-Driven and Event-Driven are out of scope.
Honest caveat: maturity of every eval-skill source is low (8 and 2 stars); authority comes from DeepEval, EDDOps and Anthropic-style guidance, not from the skills.

## Open decision (owner's call)
Which EDD meaning does mala-pata adopt? (a) Eval-Driven as an optional `eval_mode` (recommended); (b) Example-Driven as a note on `tdd_mode`/walkthrough; (c) none. Everything downstream (house name and structure) depends on this. Secondary: do the owner's projects ship LLM/agent features often enough to justify it?

## Unverified / failed fetches
GT book tutorial (404), Nierstrasz post (TLS error), Sama blog (404), playbooks.com exp-driven-dev (TLS error), Split.io (fetched, did not define the method). Search results contained no embedded instructions.

## Structure
Optional mode field (not a lane); would be authored through `/mala-pata-skill` (domain-neutral). Next: `/mala-pata-triage` after the owner picks the meaning.
