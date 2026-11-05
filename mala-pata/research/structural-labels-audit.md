---
type: audit
scope: mala-pata skill suite, structural-label contract (close / summary / output blocks)
mode: read-only static audit (no skill edited, nothing committed)
source: ~/.agent-skills/mala-pata-*/SKILL.md (+ references/*.md where present)
---

# Structural-labels audit: are close-table labels frozen English?

**Summary: 28 requested skills audited (plus 4 orchestrate skills sampled); 10 NEEDS-FIX, 17 OK (4 of them "OK, soft": hardening recommended), 1 n/a.**

NEEDS-FIX: `research`, `roadmap`, `organic-start`, `loop-start`, `shot`, `dossier`, `runbook`, `playbook`, `walkthrough-start`, `standards`.

## Method and honesty notes

- Static read of each skill's close/output block and its language clause. No skill was executed; verdicts predict risk, they do not observe behavior (the one observed failure is `research`).
- "Field-labels frozen" = the left/label entries (or the header row) are presented as a fixed set the agent must emit as-is, not as an example to adapt.
- "Clause covers field labels" = a clause names the labels of THAT table (or the Field/Milestone column explicitly), not merely the generic phrase "field labels".
- Key finding: `research` ALREADY carries the generic clause ("section headers, field labels, table/column headers, and enum/option tokens stay English") and still failed. So the generic clause is empirically insufficient. It never says "the left column of the table", and the label set is shown as an inline `<placeholder>` table, which the agent treats as adaptable. A clause only works when the table's own labels are enumerated or explicitly declared frozen.
- Not assessed: the `mala-pata-sdd-*` family (out of the requested list; its tables are SDD artifact templates, no language clause found by grep). Mirror in the repo vs live source was not diffed.
- The 4 orchestrate skills (organic/roadmap orchestrate and -start) were checked only at their clause line: each enumerates its table headers explicitly, so they look OK.
- Verdict `OK (soft)` = acceptable today (headers are literal and a clause names most of them) but the clause does not say "never translate / never swap"; hardening is cheap.

## Audit table

| Skill | Has close table? | Field-labels frozen? | Clause covers field labels? | Verdict |
|---|---|---|---|---|
| research | yes (`Field \| Value` summary) | No: labels shown as an example set inside the table, not declared fixed | Generic only ("field labels"); Field column not named; this is the observed failure | NEEDS-FIX |
| triage | yes (`Field \| Value \| Provenance` draft) | Yes: What / Why / DoD / Decisions / Risk (+ conditional `change_name`, `kind`, `research`); "same lines, same columns" | Yes: names the draft field labels explicitly | OK |
| roadmap | yes (DAG, coverage, split tables; Step-5 gate and written `.md`) | Mostly: DAG columns fixed, but see fix list (coverage-table columns, `Vertical slice`, `#`, status tokens not enumerated; two different coverage-table shapes) | Partial: long enumerated list that omits several column names and enum tokens | NEEDS-FIX |
| organic | yes (`Field \| Value` kickoff summary) | Yes: What / Lane / Base → branch / Worktree / DoD | Yes: enumerates every label incl. `Field`, `Value`, "they are structural" | OK |
| organic-start | yes (`Milestone \| Status \| Evidence`) | No: rows are "rows that apply", names carry placeholders, nothing says the milestone names are fixed | Generic only ("field labels"); row labels not covered | NEEDS-FIX |
| loop | yes (`Field \| Value` kickoff summary) | Yes: What / Profile / Base → branch / Worktree / DoD / Migration / Phases | Yes: enumerates every label, "they are structural" | OK |
| loop-start | yes (`Milestone \| Status \| Evidence`) | No: explicitly "Adapt the rows to the real change"; names can be dropped, merged (`Spec+Design`) or edited | Generic only; row labels not covered | NEEDS-FIX |
| shot | yes (`Milestone \| Status \| Evidence`) | No: rows "that apply"; milestone names not declared fixed | Weak one-liner "Labels verbatim English"; row labels not named | NEEDS-FIX |
| radar | yes (8-column table, `table-format.md`) | Yes: "FIXED radar format (immutable contract)", exact columns and order | Yes: clause sits in the immutable-contract block | OK |
| roadmap-radar | yes (7-column table + banner/BLUF/legend) | Yes: "Fixed format ALWAYS", literal header row and banner labels | Generic clause, but the whole block is an "ALWAYS identical" literal format | OK |
| domain-radar | yes (inventory, completeness, runbooks, playbooks tables) | Yes: literal header rows, "fixed format ALWAYS identical" | Yes: clause names headers, field labels, enum tokens | OK |
| icebox | yes (bulk cubes table) | Yes (literal header row `# \| Cube (DoD) \| size-hint \| Status`) | Enumerates title/BLUF/Icebox/Next step/Structure but not the table headers | OK (soft) |
| icebox-defrost | yes (approval table, also written to plan doc) | Yes: `cube \| DoD \| size-hint \| handling \| why`; `handling` values are machine-read identifiers | Enumerates block labels; table headers not named | OK (soft) |
| icebox-defrost-start | yes (`Cube \| Sharpened (What) \| Handling \| Verdict \| Route (forecast) \| Next step`) | Yes: literal header row | Enumerates most headers (Cube, Handling, Verdict, Route); not `Sharpened (What)` / `Route (forecast)` exactly | OK (soft) |
| icebox-radar | yes (6-column table + banner) | Yes: "Fixed format ALWAYS" | Yes: clause + fixed-format rule | OK |
| gaps | yes (coverage + 3 findings tables) | Yes: "emit EXACTLY these tables", "render EVERY defined column" | Generic clause, but the "exact columns" rule backs it | OK |
| art | yes (findings table) | Yes: 5 headers declared; vertical `Finding:` blocks banned | Yes: enumerates every label | OK |
| dossier | yes (readback `Q \| Captured?`) | Partly: question labels Q1..Q6 are house-fixed but several are Spanish by design (see fix) | No clause on the close block; the clause covers only the Rendering-1 body labels | NEEDS-FIX |
| runbook | yes (readback `# \| Action \| Expected output`) | Partly: columns literal, close labels (`Runbook:`, `OPEN`, `File`, `Next step`) not declared fixed | No clause on the close block; "labels verbatim English" only on the document body | NEEDS-FIX |
| runbook-start | yes (Run record `# \| Step \| Status \| Evidence`) | Yes | Yes: clause names `#`, `Step`, `Status`, `Evidence` | OK |
| playbook | yes (readback `Condition \| Branch \| Action`; decision-tree table in body) | Partly: columns literal; tree headers and close labels not declared fixed | No clause on the close block or on the tree columns (only "Body labels") | NEEDS-FIX |
| playbook-start | yes (Run record `Step \| Branch / action \| Evidence \| Outcome`) | Yes (literal header row; first-column `triage` row is a constant) | Generic one-liner directly under the table; does not list the headers | OK (soft) |
| walkthrough | yes (test table) + access-block Field list | Yes: `Given (path)/When/Then/Pass/Fail/Failure signal/Evidence`, access-block labels | Yes: enumerates every label incl. Access block fields | OK |
| walkthrough-start | yes (Run record `# \| Phase \| Assert (Then) \| Evidence \| Result`) | Literal header row, but nothing says it is frozen | NO clause anywhere in the skill | NEEDS-FIX |
| states | yes (`Machine \| States \| Transitions \| Degraded (reason)`) | Yes | Yes: names all four headers | OK |
| standards | yes (readback `Area \| Status \| Evidence`) | Partly: columns literal; status tokens approved/proposed/OPEN defined elsewhere | No clause on the close block (only on the body Section labels) | NEEDS-FIX |
| seed | yes (fixture table) | Yes | Yes: names all six headers | OK |
| skill | no table (bulleted close block) | n/a | Clause present and explicit (Skill ready, Context gate, Branch / commit, Next step, Structure) | n/a |
| (sampled) organic-orchestrate, organic-orchestrate-start, roadmap-orchestrate, roadmap-orchestrate-start | yes | Yes | Yes: each clause enumerates its table headers | OK (clause-line check only) |

## Recommended fixes (NEEDS-FIX only)

For every skill below, add the shared clause (next section). It must say, in substance: "the Field-column labels are structural — emit them EXACTLY as listed, verbatim in English; never translate, never swap for case-specific ones; only the Value is localized." Plus the frozen set listed for each.

### research (priority 1, observed failure)

Frozen Field set, in this order:
`What it proposes` · `Why` · `What it will do` · `Problem size` · `What matters` · `Size signal`
Change: replace the "required ≥1 table" example with a declared-frozen table; list the six labels in the clause; state that case-specific labels (for example "what was measured", "good news", "what shrinks") are a defect. `Size signal` values stay the enum `one-unit | multi-unit`; `Verdict` tokens `PROCEED / SHARPEN / RECONSIDER` and the labels `Verdict`, `Left OUT / pending`, `Doc`, `Next step`, `Structure` are part of the same frozen block.

### roadmap

Frozen sets to add to the existing clause:
- Coverage table (gate presentation): `Axis (desired state)` · `Covered by` · `Status`; status tokens `covered` · `extra-proposal` · `deferred` · `→ Level 2`.
- DAG table: add `#` and `Vertical slice (one line)`.
- Written `.md` coverage table uses a different shape (`Axis (desired state) | Status | Phases / reason`). Pick ONE shape for both places and freeze it.
- Per-phase detail labels (`Tentative route`, `Depends on`, `Deferrable?`, `Kind`) are already listed; keep.
Change: extend the enumerated list; remove the gate-vs-file column mismatch.

### organic-start

Frozen Milestone set (the row label column; a row may be omitted when it does not apply, never renamed):
`Authorization` · `Worktree + base` · `Explore (Where)` · `Feature-doc (if substantial)` · `Apply (TDD if applies)` · `Migrations (if any)` · `Smoke test (fixtures)` · `Work-unit commits` · `RDD per commit (if enabled)` · `PR #<n> → <branch>` · `CI post-merge` · `Cleanup (worktree + branch)`
Columns: `Milestone` · `Status` · `Evidence`. Status tokens: `✓ done` · `◐ partial: <reason>` · `○ pending` · `✗ blocked: <reason>` · `∅ n/a`.
Change: say "omit rows that do not apply; never rename or translate a Milestone".

### loop-start

Frozen Milestone set (omit-only, never rename):
`Worktree + base` · `Explore` · `Propose` · `Spec` · `Design` · `Tasks` · `Preview gate` · `Apply (TDD)` · `Verify` · `Review per candidate (if RDD on)` · `Migrations (if any)` · `Smoke test (fixtures + human confirmation)` · `e2e real case <id>` · `No-regression` · `PR #<n> → <branch>` · `CI post-merge` · `Archive` · `Cleanup (worktree + local/remote branch)` (LITE/MINIMAL merged row: `Spec+Design`).
Columns: `Milestone` · `Status` · `Evidence`. Status tokens as above, plus `✗ red: <reason>`.
Change: replace "Adapt the rows to the real change" with "Omit rows that do not apply; never rename or translate a row label (only the Evidence value is free)". Note the sentence about `CI` row `○ N/A (project without pipeline)` as an allowed Value, not a new label.

### shot

Frozen Milestone set:
`Safe branch` · `Change + check` · `Work-unit commit` · `RDD per commit (if on)` · `CI (if any)` · `PR / merge` · `Repo state`
Columns: `Milestone` · `Status` · `Evidence`. BLUF label `Result:` is frozen too.
Change: replace "Labels verbatim English" with the full clause and name the Milestone column.

### dossier

Frozen close labels: Title `Discovery ready`, BLUF `Discovery:`, readback columns `Question` · `Captured?` (currently `Q | Captured?`), plus `OPEN`, `File`, `Next step`, `Structure`.
Decision needed from the human (not guessed here): the Rendering-1 question labels (`Q1 ¿Para qué? [ACLARAR]` ... `Q6 ¿Qué puede salir mal? [PROTEGER]`) and the client questionnaire sections are Spanish by design. Either (a) freeze them as the house labels and say so (they are a framework name, not a translation), or (b) switch the internal traceability doc to English labels and keep Spanish only in the client-facing questionnaire. Today the clause "labels verbatim English" contradicts the Spanish labels it governs.
Change: add the close-block clause; resolve (a) or (b).

### runbook

Frozen close labels: Title `Runbook ready`, BLUF `Runbook:`, readback columns `#` · `Action` · `Expected output`, `OPEN`, `File`, `Next step`, `Structure`. Steps table columns (body): `#` · `Action` · `Expected output` · `If not as expected`.
Change: the existing clause covers only the document Body; extend it to the close block and the Steps table headers.

### playbook

Frozen close labels: Title `Playbook ready`, BLUF `Playbook:`, readback columns `Condition` · `Branch` · `Action`, `OPEN`, `File`, `Next step`, `Structure`. Decision-tree columns (body): `Condition (observed, measurable)` · `Branch` · `Action (inline steps or runbook)` · `Expected outcome` · `Owner` · `Rollback`; fallback row label `Others (fallback)`.
Change: same as runbook (clause covers Body section labels only today).

### walkthrough-start

Frozen Run-record set: BLUF label `Smoke —`; columns `#` · `Phase` · `Assert (Then)` · `Evidence` · `Result`; tokens `✓ pass` · `✗ fail`; BLUF fields `console/network`, `delicacy` (`low` / `medium` / `high`), `evidence →`. If the walkthrough declares an Outputs "Declared report", its own labels follow the walkthrough's pinned format, not this clause.
Change: the skill has no language clause at all; add the shared clause and the set above.

### standards

Frozen close labels: Title `Standard ready`, BLUF `Standard:`, readback columns `Area` · `Status` · `Evidence`, status tokens `approved` · `proposed` · `OPEN`, plus `OPEN`, `File`, `Next step`, `Structure`.
Change: extend the Body-only clause to the close block and readback table.

## Proposed shared clause (canonical sentence)

> **Structural labels are frozen.** Every label of this block (section and block titles, BLUF labels, the left-column Field/Milestone/Row labels, table column headers, and enum/status tokens) is structural: emit it EXACTLY as listed in this skill, verbatim in English, even when the conversation is in another language. Never translate a label, never replace it with a case-specific one, never add or rename rows (omit a row only where the skill says it may be omitted); only the Value / Evidence content and the surrounding prose are localized.

Why this wording: it names the left column explicitly (the observed failure), forbids "swap for case-specific" (the second observed failure mode), and separates omit (allowed) from rename (forbidden), which resolves the `loop-start` "adapt the rows" ambiguity.

### Delivery option (not created here)

Option A: put the sentence once in a shared reference (e.g. `_shared/mala-pata-structural-labels.md`, same pattern as the existing "Canonical ... single source of truth" blocks such as the lane-gate and domain rule) and have each close-table skill carry one line: "Apply `_shared/mala-pata-structural-labels.md` verbatim." Caveat from this audit: a pointer alone may reproduce the `research` failure, because the generic clause already exists and was ignored. So each skill must still enumerate its own frozen set next to its table (the lists above); the shared file only carries the rule, the skill carries the data.
Option B: restate the sentence in each skill (about 20 copies; drift risk, higher token cost).
Recommendation: Option A plus a per-skill enumerated frozen set, with the list placed immediately under the table, not in a distant paragraph.

## Suggested fix order

1. `research` (observed failure).
2. `loop-start`, `organic-start`, `shot` (row-label tables with explicit "adapt/apply" wording).
3. `walkthrough-start` (no clause at all).
4. `runbook`, `playbook`, `standards`, `dossier` (clause only covers the document body, not the close block; resolve the dossier Spanish-label decision first).
5. `roadmap` (complete the enumerated list, unify the coverage-table shape).
6. Optional hardening of the `OK (soft)` skills (`icebox`, `icebox-defrost`, `icebox-defrost-start`, `playbook-start`): append the shared sentence.
