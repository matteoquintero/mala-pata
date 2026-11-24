# Domain rule — mala-pata single source of truth

> **Re-read on apply (stale-context guard).** This is a PROCESS canonical — no output signature a hook can check — so the guard is explicit: at the moment you APPLY this rule, re-read THIS file from disk (it is a live symlink; it may have changed since it entered your context) and apply the on-disk version — it wins over any stale copy you hold.

Canonical rule for the `domain` frontmatter field (research, kickoffs, seeds, icebox,
diagrams, walkthroughs, gaps…). `mala-pata-domain-radar` groups every artifact by it,
so a wrong or blank domain breaks the domain view. Every skill that writes `domain`
applies THIS verbatim.

## The rule

- Base `feature/<X>` → domain `<X>` — **even when the change touches sub-areas or integrations of that feature**; those sub-areas are NOT the domain.
- Base `main` / `development` → the functional **AREA** the change touches.
- No clear area → `main`.
- Research / icebox (no base branch yet) → infer from what the work is FOR (the feature or area it anchors to in the code).

## Hard constraint

**NEVER blank.** On ANY doubt → ASK the human ONE question before writing; never guess.
