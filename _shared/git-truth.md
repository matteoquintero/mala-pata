# Git = truth: done-derivation + Mala-Pata-* trailers — single source of truth

Canonical rules for (1) how a radar decides a unit is `done`, and (2) the commit
trailers that tie a landed change to its phase/domain. Producers and consumers
below MUST agree — a drift here silently breaks radar matching.

## done-derivation (consumers: `mala-pata-roadmap-radar`, `mala-pata-domain-radar`, `mala-pata-icebox-radar`)

- A **`code`** unit is `done` ONLY when it landed in the **freshly fetched integration branch**, confirmed by ANY ONE of these (all equal weight): the `Mala-Pata-Phase` trailer, a merged PR, a merged branch / slug commit that is an ancestor, a delivering artifact present, or a recorded sha that is an ancestor. **Never** a DoD checkbox or an archive-report. The trailer is OPTIONAL; its absence never downgrades a confirmed match. A confirmed match is `[git]`, never `[weak]`.
- **`ops`** units leave no git artifact → `done` is **attested** in the `.md` with evidence (URL/id/health/date), tagged `[attested]`, never `[git]`.
- Work clearly exists but cannot be tied to the unit → `? unbound (confirm)`, never a false `pending`.
- **Zero cache, zero memory**: re-derive every run from the `.md` + live git.

## Mala-Pata-* trailers (producers: `mala-pata-shot`, `mala-pata-organic-start`, `mala-pata-loop-start`)

On the landing commit (the squash message for a PR; the merge commit for a merge-to-feature), each trailer on its OWN line, after a blank line:

```
Mala-Pata-Phase: <change-name>
Mala-Pata-Domain: <domain>
Mala-Pata-Roadmap: <slug | none>
Mala-Pata-Lane: <shot | organic | loop>
```

- Producers MUST emit all four. `<domain>` follows `_shared/domain-rule.md`.
- Keep the key names EXACT — a rename silently breaks every radar's matching.
