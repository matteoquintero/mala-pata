# MINIMAL profile — small fix / known refactor

> **MINIMAL ≠ `/mala-pata-organic`** (deliberate decision, not duplication): MINIMAL
> **runs the SDD cycle** — lightweight version, but with artifacts, phases and gates
> (traceability in engram). Organic does NOT do SDD at all: a single direct pass
> without planning artifacts. If the small change merits an SDD trail →
> MINIMAL; if it does not merit SDD → organic.
> **Lane vs depth**: `/mala-pata-triage` owns the LANE choice (loop vs organic); this profile only sets the DEPTH within an already-chosen loop (architecture decided elsewhere → organic, not loop).

## When to choose MINIMAL
- Targeted bug fix (1-3 files).
- Mechanical refactor (rename, move, extract).
- Type migration (add a field, update types generated from the contract).
- Regression fix in a module touched this week.
- Change without new business logic.

## Adjustments relative to the base method

- **Phase 0 components**: mandatory — the REUSA/ADAPTA/NUEVO audit is **NOT skipped**. Auto-approve if audit = 0 NEW. **If the audit marks ≥1 NEW component, escalate to LITE** — do not continue in MINIMAL with new components.
- **TDD granularity**: **per feature**. Never per task in MINIMAL.
- **Explore**: minimal, never skipped (Explore is phase 1 of loop-start) — if the module was touched this week, a quick pass over the prior explore; otherwise 1 grep pass.
- **Spec + Design**: **merged and short** (target 1-2 markdown pages).
- **sdd-preview**: typically 0 reviewers via its own self-assessment (mechanical change, no risk signals).
- **Verify**: light — suite + build. No mandatory live smoke unless it touches visible UI. (Default by size: rises to normal if `sdd-preview` detected risk signals — see `_base.md`.)
- **Apply**: a single batch (no `/clear` between tasks).
- **Storybook / MSW / fixtures**: only if the change touches UI.

## `/clear` nudges

- At the human's discretion. In a true MINIMAL, the whole cycle fits in one session with no need for `/clear`.

## Cost order of magnitude

~70K tokens end-to-end.
