# mala-pata-sdd-* — owned snapshot of gentle-ai's SDD

House-owned adoption of gentle-ai's SDD phase agents/skills + the orchestrator
manual, for the `own-sdd-into-mala-pata` migration (see
`research/own-sdd-into-mala-pata.md`). gentle-ai 4.1+ `sync` DELETES the
gentle-owned `sdd-*` from `~/.claude`; this owned copy survives it.

- Source: gentle-ai gentle-ai 3.7.0 (snapshot 2026-10-30).
- House touch so far is LIGHT: frontmatter `name:` renamed to the
  `mala-pata-sdd-<phase>` namespace (zero collision with the active `sdd-*`).
  Bodies are VERBATIM — they still reference gentle's `sdd-*` names and
  `gentle-ai sdd-*` commands. The deep decouple is the DEFERRED rewire phase.
- NOT wired, NOT symlinked into `~/.claude`: `loop`/`loop-start` still dispatch
  gentle's `sdd-*`, so these cannot affect the live loops. Activation + rewire
  is a later, deliberate step.

Phases: explore · propose · spec · design · tasks · apply · verify · archive ·
init · onboard · research. (`sdd-preview` is already user-owned — not copied.)
