# Domain rule — mala-pata single source of truth

> **Re-read on apply (stale-context guard).** This is a PROCESS canonical — no output signature a hook can check — so the guard is explicit: at the moment you APPLY this rule, re-read THIS file from disk (it is a live symlink; it may have changed since it entered your context) and apply the on-disk version — it wins over any stale copy you hold.

Canonical rule for the `domain` frontmatter field (research, kickoffs, seeds, icebox,
diagrams, walkthroughs, gaps…). `mala-pata-domain-radar` groups every artifact by it,
so a wrong or blank domain breaks the domain view. Every skill that writes `domain`
applies THIS verbatim.

## The rule

- Base `feature/<X>` → domain `<X>` — **even when the change touches sub-areas or integrations of that feature**; those sub-areas are NOT the domain.
- Base `main` / `development` → the functional **AREA** the change touches.
- No clear area → propose `main`.
- Research / icebox (no base branch yet) → infer from what the work is FOR (the feature or area it anchors to in the code).

## Confirmation gate (MANDATORY — every write, no exceptions)

The model NEVER decides the domain alone. Inferring is only how you build the PROPOSAL; the human decides.
Confidence is not an exemption: a domain that "looks obvious" is exactly the one that gets invented
(a sub-area like a screen, a UX facet or an entity name passed off as the domain).

Before writing ANY artifact that carries `domain:`:

1. **List the existing domains** in the repo — the distinct `domain:` values already used under `mala-pata/`
   (`grep -rhoE '^domain: *[^ #]+' <repo>/mala-pata | sort | uniq -c`).
2. **Propose ONE value**, with its source in a few words (`from base feature/<X>` / `area touched: <Y>` / `what it is for: <Z>`).
   Prefer an EXISTING domain; propose a NEW one only when none fits, and say it is new.
3. **Ask the human to confirm it — ONE question, then STOP and wait**:
   `Domain: <proposed> (<source>) · existing: <d1>, <d2>, … · confirm, or tell me the right one`.
4. Write the artifact only with the value the human confirmed (or gave). Never write a domain the human did not confirm.

Exceptions (no question, because the value was ALREADY human-confirmed): the domain is copied verbatim from an
upstream artifact that carries it (e.g. a kickoff inherits the research/roadmap `domain:`, a defrost plan inherits
its icebox `domain:`). Even then, say the inherited value in one line so the human can correct it.

## Hard constraint

**NEVER blank, NEVER invented.** No artifact is written with an unconfirmed domain. A sub-area, screen, component
or facet of a feature is NOT a domain.
