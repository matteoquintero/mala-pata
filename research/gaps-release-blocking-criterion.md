---
idea_slug: gaps-release-blocking-criterion
project: mala-pata-skills
verdict: PROCEED
created_at: 2026-10-15
next: triage
size_signal: one-unit
---
# Research: a real criterion for "does this gap block the release?" in mala-pata-gaps

## Verdict: PROCEED
There is NO need to invent a bespoke scale — the industry already has the exact criterion the user is reaching for: the **MoSCoW Must-test + the workaround test**. It gives a defined blocker gate (not a vibe) AND a middle tier WITH a criterion (not a vague "medium"). Adopt it on top of the existing `open/deferred/closed` disposition.

## Raw idea (what you asked)
Make gaps able to say, for real, which gaps **block going to production** and which don't — without the binary "blocker / nothing" (because then nothing ever counts) and without a "medium" that has no criterion. The notificaciones alert (#3: a quality-rating alert) is the live example: not a mega-blocker, but not nothing either.

## Discover

### How it's done today + limits (with sources)
Three established frameworks, and they converge:

- **MoSCoW — the Must-test.** A requirement is **Must** when WITHOUT it the delivery misses the deadline, is non-compliant/illegal, is unsafe, or **fails to deliver an effective solution** — and, decisively: *"if there is any way to work around a particular requirement, teams should consider it a should-have or could-have."* `Must` = the **Minimum Usable Subset / MVP**. [TechTarget](https://www.techtarget.com/searchsoftwarequality/definition/MoSCoW-method), [Wikipedia](https://en.wikipedia.org/wiki/MoSCoW_method). Guardrail: Must should be ≤60% of scope, or it is scope creep ([ClickUp](https://clickup.com/learn/?p=71081)).
- **Go/No-Go release readiness.** Decision is **GO / NO-GO / GO-with-conditions**, on **predefined, evidence-based** criteria; a release is not approved while any accepted **blocker** is unaddressed; *"green means evidence, not opinion."* [Fedora](https://fedoraproject.org/wiki/Engineering_Readiness_Meetings), [OneUptime](https://oneuptime.com/blog/post/2026-08-06-launch-day-go-no-go/view), [WooCommerce](https://developer.woocommerce.com/docs/contribution/releases/readiness/).
- **Severity vs Priority.** Severity = **harm if it happens** (crash, data loss, money, privacy); only the **top severity tier gates a release**, the next tier "should be fixed but doesn't block". Chromium gates by a **severity × prevalence** matrix. [Chromium](https://chromium.googlesource.com/chromium/src.git/+show/fafff21/docs/process/release_blockers.md), [StarlingX](https://lists.starlingx.io/pipermail/starlingx-discuss/2019-July/005372.html).

**The limit of gaps today**: it has `Severity ▲●▼` (harm) and `Disposition open/deferred/closed` (scope). It has **no axis for "does this block go-live"**. Severity gets read AS blocking — but they are different: a high-harm gap WITH a workaround does NOT block. That conflation is exactly the user's pain.

### What exists in the code (real anchoring)
`mala-pata-gaps` (v1.7.0) already has: evidence-anchored findings, `▲ high · ● medium · ▼ low` severity, `[noted]/[inferred]` provenance, and the new `open/deferred/closed` disposition (gate-based). The MECE/100%-rule coverage table defines the domain objective. Everything needed to run the Must-test is already produced — the blocker gate reads the SAME evidence; it is one more column + definitions, not new analysis (same shape as the disposition split #13).

### Jobs-to-be-done
As the person deciding whether to ship a domain, I need gaps to tell me **which open gaps actually block go-live, by a defensible criterion**, so I neither over-block (everything "blocker", nothing ships) nor under-signal (vague "medium" that means nothing).

### Problem dimension (scope / frequency / severity)
- **Scope**: every gaps run where the domain is being readied for release (not just notificaciones).
- **Frequency**: every readiness assessment — recurring, exactly like the notificaciones case now.
- **Severity/impact**: high — a wrong classification either blocks shipping needlessly or ships something genuinely broken. (All three from the live notificaciones session; not measured per-project.)

### Problem vs proposed solution
| Piece | Class | Evidence | Provenance |
|---|---|---|---|
| MoSCoW tier `Must / Should / Could` per open gap | necessary | TechTarget/Wikipedia MoSCoW | [noted] |
| **Workaround test** as the decisive blocker criterion | necessary | TechTarget ("any workaround → not Must") | [noted] |
| Keep `▲●▼` severity as "harm if it happens" (separate axis from blocking) | already-exists | gaps v1.7.0 + Chromium severity≠gating | [inferred] |
| `deferred` disposition stays orthogonal (scope gate, not blocking) | already-exists | gaps v1.7.0 | [noted] |
| Domain-level **GO / NO-GO / GO-with-conditions** verdict line | extra | Fedora/OneUptime go-no-go | [noted] |
| Severity × prevalence weighting (Chromium matrix) | extra | Chromium | [inferred] — likely overkill for gaps |

## Heilmeier Catechism
| # | Question | Answer | Provenance |
|---|---|---|---|
| 1 | What are you trying to do? | Classify each OPEN gap by whether it blocks go-live, with a defined test (MoSCoW Must + workaround), plus an optional domain GO/NO-GO line. | [noted] |
| 2 | How is it done today + limits? | gaps has severity (harm) + disposition (scope) but NO go-live axis; severity gets misread as blocking. | [inferred] |
| 3 | What's new + why it works? | Adopt MoSCoW's Must-test: the workaround test makes the middle criterion-based, not a vibe. It's the standard definition. | [noted] |
| 4 | Who cares? | The person deciding go-live (you). | [assumed — obvious here] |
| 5 | Risks? | Over-tagging Must (scope creep — keep ≤60%); "workaround exists?" can be subjective → mitigate by naming the workaround as evidence. | [noted] |
| 6 | Cost / time? | Small — a classification column + definitions in the gaps skill, same shape as the disposition split. | [inferred] |
| 7 | Success / what counts as done? | **Human-only**: what "salir/release" scopes to (prod deploy of the whole domain vs a feature's DoD), and whether gaps should emit a domain GO/NO-GO line or only tag each gap. | [asked] |

**Assumption challenge**: premise = "we need a new middle scale with its own criterion." Evidence contradicts it — MoSCoW already IS that scale, and its Must-test already carries the workaround criterion. So the idea is right but the implementation is **adopt MoSCoW, do not invent**. That strengthens PROCEED.

## Define — sharpened idea (draft for triage)
- **What**: add a **release-blocking classification** to each OPEN gap in mala-pata-gaps — `Must (blocks go-live) · Should (ship with a workaround) · Could (cosmetic)` — decided by the **workaround test**, kept SEPARATE from `▲●▼` severity (harm) and from `deferred` (scope).
- **Why**: so gaps answers "what really blocks salir" with a defensible criterion, not binary-or-vibe.
- **DoD**: Given an open gap, When gaps classifies it, Then it is `Must` ONLY if without it the release fails its DoD/core job OR causes harm with **no workaround** (data loss, wrong money, security/legal, broken user path) — and every `Must` names WHY no workaround exists; `Should` names the workaround; a domain line reports `GO / NO-GO / GO-with-conditions` = NO-GO iff ≥1 `Must`.
- **Decisions already made (by research)**: use MoSCoW Must/Should/Could + workaround test; severity stays a separate "harm" axis; deferred stays orthogonal; evidence-anchored (name the workaround).
- **Open decisions**: (a) what "release" scopes to; (b) domain GO/NO-GO line — yes or just per-gap tags.
- **Risk**: over-tagging Must (keep ≤60%); subjectivity of "workaround" — mitigated by requiring the workaround as named evidence.
- **Size signal**: one-unit (extend mala-pata-gaps, like the disposition split).

## DoR (hand-off gate): What ✓ · Why ✓ · DoD ✓ · Decisions ✓ (two open, named)

## Handoff
Meta-work: applying this = an inline edit to `mala-pata-gaps` (add the MoSCoW/workaround column + a domain GO/NO-GO line), same way the disposition split (#13) was applied — NOT a real-project worktree. Confirm the two open decisions, then edit the skill.

Structure: Heilmeier Catechism (DARPA) + Double Diamond (Design Council). Verdict / size-signal / Left-OUT = house method.
