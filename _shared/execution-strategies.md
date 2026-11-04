# Execution strategies — mala-pata single source of truth

Canonical definition of the **execution strategy** dial, read by the lane runners
(`mala-pata-organic-start` and `mala-pata-loop-start`; not `shot`). A drift here changes
what gets built first — apply it verbatim, do not restate it in a skill.

## The 3 dials (orthogonal)

| Dial | Answers | Scope | Set by |
|---|---|---|---|
| `lane` | How big / how uncertain is this? (size x uncertainty) | per change | the lane gate (`mala-pata-triage`) |
| `tdd_mode` | How do you test? | per project | `sdd-init` |
| `execution_strategy` | What do you build FIRST, given the nature of THIS change? | per change | the kickoff author proposes, the human confirms |

The dials are independent: any `execution_strategy` can sit in any lane under any `tdd_mode`.
`execution_strategy` is **not** coupled to `smoke_test` — choosing one never implies the other.

## Values (`execution_strategy` in the kickoff frontmatter)

- **`none`** (default) — no special ordering; build in whatever order the tasks dictate.
- **`interface-first`** — for very visual work (UI-first): the interface is the hardest thing to get right by description alone, so make it concrete first.

## `interface-first`

1. **Agree the contract** — the data/props/events the interface consumes and emits, written down before building.
2. **Build the interface against fixtures** — the screen/interface renders from static fixtures that honor the contract; no real logic behind it yet.
3. **Human checkpoint** — the human looks at it and approves or adjusts before any logic is written.
4. **Wire the real logic behind it, test-first** — replace the fixtures with the real implementation, following the project's `tdd_mode`.

> **GUARDRAIL (mandatory).** `interface-first` MUST end with step 4. The fixture/mock interface is **never** the deliverable. If the change stops after step 3, it is not done — the work is a tracer bullet / walking skeleton (Hunt & Thomas, *The Pragmatic Programmer*; Cockburn): a thin, end-to-end path that is then made real. The DoD is only met once the real logic is wired and the fixtures are gone from the shipped path.

## Not yet (speculative — NOT shipped, do NOT wire)

`data-first` and `contract-first` are plausible future values. They are named here only so the dial has a clear extension point; no skill reads or applies them. Do not accept them as a value until they are designed and shipped.

## Applies to

**Organic + loop.** `mala-pata-organic` / `mala-pata-loop` propose it in the kickoff; `mala-pata-organic-start` / `mala-pata-loop-start` apply it and forward it to the writer (`sdd-apply` in the loop). **NOT `shot`**: shot is too minimal (a trivial 1-3 file change, no kickoff, no ceremony) — a change that needs `interface-first` is an organic, not a shot.
