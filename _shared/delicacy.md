# Delicacy — mala-pata single source of truth

Canonical for the **delicacy** level that decides WHO runs a smoke / walkthrough / manual
step: the agent, or the human. A skill that reads or writes a delicacy applies THIS verbatim.
It is the risk dial of the QA lanes (`/mala-pata-walkthrough(-start)`, `/mala-pata-atlas(-start)`,
`/mala-pata-seed`, and the in-cycle smoke gate of `organic-start` / `loop-start`), carried in a
walkthrough's `smoke_delicacy` field.

> **The level decides, not the agent.** An agent never decides on its own that a flow is too
> risky to touch; it reads the declared level and acts on it. For anything `high`, the human
> runs the sensitive steps.

## The levels (frozen — low | medium | high)

| Level | Who runs it | Behavior |
|---|---|---|
| `low` | the AGENT | objective, reversible, no money / prod data. The agent runs it end to end, reports with evidence, asks **no question**. |
| `medium` | the AGENT, then a human review | the agent runs it and the report **flags "review the evidence"** before the human confirms. |
| `high` | the HUMAN (delicate) | the agent does **NOT** execute the sensitive steps. It seeds, brings the app up, and hands the human the **step list + access block** with the line "this smoke is delicate — better you run it", then **stops at the human gate**. |

## The rule

1. **Pick the level by consequence, not by effort.** `high` is for money, prod data, or an
   irreversible / hard-to-detect effect; `low` is objective and reversible; `medium` is the
   middle — runnable by the agent but worth a human's eyes on the evidence.
2. **The level binds who acts.** `low` → agent, silent. `medium` → agent + "review the
   evidence". `high` → human runs the sensitive steps; the agent only seeds + opens + hands
   off.
3. **Degrade to `high` when the driver is missing.** If the browser driver (Playwright MCP)
   is unavailable, do NOT fake a pass — treat the run as `high`: seed, give the human the step
   list, and stop. (Same spirit as the test-DB guard: never let a tool substitute a real
   verification it cannot do.)
4. **`high` never auto-runs.** No automation mode or batch flag downgrades a `high` step to an
   agent-run; the human gate is not optional.
