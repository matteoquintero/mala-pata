# mala-pata — skill → structure (frameworks / research) index

Reference map of every skill and the methodology/research it is grounded in (its `Structure:` footer).
Goal: no skill without a declared foundation. 43 skills total — 32 house + 11 vendored SDD.

## Shared canonical refs (`_shared/` — the "centro de verdad" skills defer to)
| Ref | Grounding |
|---|---|
| `lane-gate.md` | Lane selection + loop-vs-spike discriminator (Cynefin) + roadmap discriminator |
| `objective-completeness.md` | Gap analysis + MECE/100% rule + ISO/IEC 25010 prompts + Story-Map walk + fork test |
| `domain-rule.md` | Domain derivation (feature→X, else area, else main) |
| `git-truth.md` | done-derivation (git = truth) + `Mala-Pata-*` trailer schema |
| `test-db-guard.md` | Test-DB isolation / never-prod |

## Lanes (execution)
| Skill | Grounding |
|---|---|
| `mala-pata-shot` | Definition of Done + Conventional Commits + information radiator (Cockburn) |
| `mala-pata-organic` | DoR-style brief + BLUF + Given/When/Then (Fowler) |
| `mala-pata-organic-start` | Definition of Done + information radiator (Cockburn) |
| `mala-pata-loop` | DoR-style brief + BLUF |
| `mala-pata-loop-start` | Definition of Done + information radiator (Cockburn) |

## Routing / planning
| Skill | Grounding |
|---|---|
| `mala-pata-triage` | Definition of Ready + INVEST |
| `mala-pata-research` | Heilmeier Catechism (DARPA) + Double Diamond (Design Council) + objective-completeness ref (gap analysis / MECE / ISO 25010) + spike mode (Cynefin / XP spike) |
| `mala-pata-roadmap` | Minto Pyramid / MECE + INVEST / vertical slices + WBS 100% rule + dependency DAG + objective-completeness ref + spike phase type |

## Radars (read-only status)
| Skill | Grounding |
|---|---|
| `mala-pata-radar` | information radiator (Cockburn) + workflow-state lexicon + attention set + urgency order + phase pipeline — su `Structure:` vive en `references/table-format.md` |
| `mala-pata-roadmap-radar` | information radiator (Cockburn) + workflow-state lexicon |
| `mala-pata-domain-radar` | information radiator (Cockburn) + workflow-state lexicon |
| `mala-pata-icebox-radar` | information radiator (Cockburn) + workflow-state lexicon |

## Orchestrators (batch / waves)
| Skill | Grounding |
|---|---|
| `mala-pata-organic-orchestrate` | precedence diagramming + wave layering |
| `mala-pata-organic-orchestrate-start` | batch worktree + Warp launch + hybrid-by-waves central delivery |
| `mala-pata-roadmap-orchestrate` | precedence diagramming + wave layering + live-git state derivation |
| `mala-pata-roadmap-orchestrate-start` | route-aware batch worktree + Warp launch + hybrid-by-waves central delivery |

## Icebox family
| Skill | Grounding |
|---|---|
| `mala-pata-icebox` | deferred backlog (capture-now / route-later) + BLUF |
| `mala-pata-icebox-defrost` | plan/run split + triage form-gate classification |
| `mala-pata-icebox-defrost-start` | plan/run split + Double Diamond + lane routing + WBS grouping |

## Doc-authoring
| Skill | Grounding |
|---|---|
| `mala-pata-dossier` | 6-question discovery (ACLARAR→PROTEGER) + Diátaxis (Procida) + JTBD switch interview (Moesta) + BRD/RAID (BABOK-adjacent) |
| `mala-pata-runbook` | runbooks-as-agent-instructions + executable decision tree + SRE runbook metadata |
| `mala-pata-runbook-start` | executable decision tree (action/expected/if-not) + sequential abort-after-N + verify-then-rollback |
| `mala-pata-playbook` | decision-tree playbook (first-match + Others) + diagnostic triage + crystallization |
| `mala-pata-playbook-start` | decision-tree walk + stop-on-ambiguity + delegate deterministic leaves to runbook |
| `mala-pata-walkthrough` | Diátaxis (Procida) + BDD Given/When/Then (North) + Living Documentation (Adzic/Martraire) |
| `mala-pata-walkthrough-start` | Playwright-MCP a11y-first + assertion-as-verdict + screenshot/trace evidence + console/network gate |
| `mala-pata-standards` | pattern-mining + inconsistency-as-question + evidence/confidence capture |
| `mala-pata-states` | Harel statecharts / UML state machine (via archify) |
| `mala-pata-gaps` | gap analysis + MECE/100% rule + MoSCoW tiers (Clegg/DSDM) + go/no-go release readiness |

## Visual
| Skill | Grounding |
|---|---|
| `mala-pata-art` | Gestalt + Swiss grid (Müller-Brockmann) + Bauhaus + Dieter Rams + Norman + Laws of UX (Yablonski) + Refactoring UI (Wathan/Schoger) |

## Testing / fixtures
| Skill | Grounding |
|---|---|
| `mala-pata-seed` | xUnit Test Patterns — fixture setup (Meszaros) + test-DB-never-prod |

## Meta (authoring)
| Skill | Grounding |
|---|---|
| `mala-pata-skill` | owned meta-work flow (write-live → mirror → branch commit) + judgment context-leak gate + domain-neutral authoring |

## Vendored (gentle-ai SDD — NOT house-grounded)
`mala-pata-sdd-apply`, `-archive`, `-design`, `-explore`, `-init`, `-onboard`, `-propose`, `-research`, `-spec`, `-tasks`, `-verify` (11).
These are vendored gentle-ai SDD phase agents; they do not follow the house `Structure:` convention. The house SDD *experience* is grounded in `mala-pata-loop` / `mala-pata-loop-start` (which orchestrate them).

## Gaps / follow-ups
1. **`mala-pata-roadmap-radar`** — does not yet understand `Kind: spike` phases (status derivation for a spike phase). Open.

Resueltos esta sesión:
- `mala-pata-research` footer — `Structure:` line updated to cite objective-completeness + spike.
- `mala-pata-radar` — was NOT a gap; its `Structure:` lives in `references/table-format.md` (false negative of the initial grep, which only scanned `SKILL.md`).
