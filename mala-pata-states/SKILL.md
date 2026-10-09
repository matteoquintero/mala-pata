---
name: mala-pata-states
description: Given a feature by name, extracts its state machine(s) from the code (enum + guards) and draws them with archify (lifecycle) as a faithful HTML for human visual inspection — onboarding and detection of broken transitions. Read-only on the project's code (does not modify it); does NOT dispatch sdd-*.
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "1.2.0"
---

# mala-pata-states — Faithful state machine diagram

Trigger: "máquina de estados de \<feature\>", "diagramá los estados de X", "mala-pata-states \<feature\>".

This skill produces a diagram, not an analysis. It is read-only on the target project's code: it reads the state enum and the real transitions, and draws them — it does not modify a single line of the code it inspects. It uses ODD workers (direct/delegated) for its own execution; it does NOT dispatch `sdd-*` agents — the gentle-ai preflight hook does not apply here. Absolute paths always, both for reading the target project and for invoking archify.

## Requirements (orchestrate, do not reinvent)

mala-pata orchestrates community tools — it does not reimplement them. Check at startup:

- **Mandatory** (no fallback — if missing, STOP and ask to install it, do not start):
  - `archify` — diagram renderer (it is a skill, not a binary), no fallback. Install: `npx skills add tt-a1i/archify -g`.
- **Recommended** (with fallback — if missing, warn in one line and continue degraded):
  - `codegraph` — code graph (anchoring and structure). Fallback: grep/Read. Install: global npm CLI; per-project init with `gentle-ai codegraph init --cwd <repo>`.
  - `serena` — extract enum and transitions. Fallback: grep/Read. Install: `uv tool install -p 3.13 serena-agent && serena setup claude-code`.

Check: `command -v <tool>` (CLI) or `claude mcp list` (MCP, e.g. serena). If a mandatory tool is missing, do not continue.

## Hard principles (non-negotiable)

- **FIDELITY over tidiness**: you draw what the code DOES, not what it should do. If a transition is missing in the code, it is missing in the diagram — states or transitions are never invented to make it look complete. A diagram that lies is worse than no diagram.
- **ORTHOGONAL**: one small machine per concern, never a god-machine. If a feature mixes dimensions (e.g.: fulfillment state + payment state), they are separated into distinct machines or columns.
- **MINIMAL**: a state exists ONLY if it changes which actions are allowed. Everything else is metadata, not state. Pseudo-states (flags, timestamps, combined labels) are degraded to metadata/cards, not drawn as nodes.
- **The skill does NOT judge nor report** ("don't tell me what is broken") — it produces the faithful visual; the HUMAN detects the problem by looking. Never an output like "transition X is broken".
- **v1 scope = state machines with an explicit enum** (states live in an enum/union and transitions in domain guards/services). Implicit or scattered state is OUT of v1 — it is documented as a future extension, and if a feature has no explicit enum, the skill says so and stops, instead of guessing.

## Phase 0 — Input + guard

The input is a feature name (e.g.: `pedido`). Read-only on the target project's code — this skill does not write nor edit anything of the project it inspects.

1. Resolve the target project's project root: `git rev-parse --show-toplevel`.
2. If CodeGraph is available for that project (`<project-root>/.codegraph/`), use it to locate the state enum and its references (global CodeGraph rule: prefer `codegraph_explore` / the read-only CLI before broad Grep/Read). If it is not available, use direct Grep/Read.
3. If the feature does not exist or there is no state enum candidate, say so and stop — there is no diagram to produce.

## Phase 1 — Extract from the code (anchored, v1 = explicit enum)

Locate the feature's state enum(s) (e.g.: `PedidoEstado`) and the real transitions: guards, domain services, compare-and-swap on the state field (`WHERE estado = <esperado>`), or any other guard mechanism the code uses.

For each transition record: `from`, `to`, and the condition/guard/action that triggers it (including any relevant note, e.g. the error a guard throws).

If the feature has NO explicit state enum — say so and STOP. v1 does not support implicit nor scattered state; it stays as a future extension, not as best-effort.

You draw the REAL: a transition that does not exist in the code is not drawn, even if it "would make sense" for it to exist.

## Phase 2 — Orthogonal + minimal (the quality filter)

Apply the hard principles before touching the JSON:

- Are there combined dimensions? (e.g.: fulfillment state + payment state of the same feature) → they are separated into distinct machines or columns/lanes, never a single machine mixing them.
- Does any candidate "state" not change which actions are allowed? → it is metadata: it goes to `cards`, not to `states`.
- Is there a combined/hinge state (e.g.: `enviado_a_caja_parcialmente`)? → it is evaluated the same as in bodega: if it does not enable/disable actions different from its neighbors, it is described in a `card`, not drawn as its own node.

The result is 1..N small, readable machines, never a god-machine.

## Phase 3 — Build the archify `lifecycle` JSON

Map the result of phases 1-2 to archify's `lifecycle` schema (`schema_version: 1`, `diagram_type: "lifecycle"`):

- `states[]`: each real state → `id`, `type` (`start` / `active` / `decision` / `waiting` / `success` / `failure`, as appropriate), `label`, `sublabel` (the real enum value), `lane`, `col`, and optionally `step`, `tag`, `width`.
- `transitions[]`: each real transition → `id`, `from`, `to`, `label`, `variant` (e.g. `security` for rejections, `dashed` for conditional branches, `emphasis` for transitions with a relevant guard), `guard`/`note` when applicable, `fromSide`/`toSide`, and `route` only if needed.
- `lanes[]`: one lane per orthogonal dimension or per logical grouping (main flow, branches, terminals), according to what came out of Phase 2.
- `cards[]`: the degraded metadata (combined states, invariants, guard notes) and any clarifying note — never conclusions like "this is broken".
- `meta`: descriptive `title`, `quality_profile: "showcase"`, and a `viewBox` matching the real size of the diagram.

Respect the gotchas documented by archify for `lifecycle`: phase columns `0..4` occupy the main rail; an event/terminal column `N` in `0..2` aligns exactly below main column `N + 2`; a recoverable state uses `type: "failure"` plus a real transition back to the active state (not a phantom terminal state).

### Known-good archify envelope (build INSIDE it, do not thrash)

The viewport that squeezes is **1440x900** (the others — 1600/1920/2048 — fit on their own). Build inside this envelope so that `visual-check` passes on the FIRST render, instead of iterating blindly:

- **`viewBox` height = 566 fixed.** It is archify's hard floor (it rejects any smaller value with `viewBox/1 must be >= 566`). It is not a lever — do not try to lower it.
- **`viewBox` width ~1040-1100 (default 1080).** archify scales the font with `930 / viewBoxWidth`; widths in that band keep the projected font `>= 6px`. Widening too much lowers the font below 6px and fails readability.
- **Maximum 3 cards.** The 4th card wraps to a second row (~+62px) and overflows 1440x900 (`scrollHeight` 962 > 900). If you have more than 3 findings, **merge them into 3 cards** (several items per card), do not add a 4th.
- **Height budget:** at 1440 width, `SVG_height = 1440 x 566 / viewBoxW` (~754px with 1080) + chrome (title/toolbar/cards, ~146px) must end up `<= 900`.
- **Overflow = SPLIT signal (ORTHOGONAL principle).** If a single machine does not fit even in the envelope, it is evidence of a god-machine → split it into several machines/diagrams (Phase 2), do not force it in. The overflow fix IS the skill's principle, not an exception.

## Phase 4 — Validate and deliver with archify

Run these commands with absolute paths, from the archify skill's directory (`/Users/matteoquintero/.agents/skills/archify`):

```bash
node bin/archify.mjs validate lifecycle <absolute-path-json> --quality showcase --json
```

It must give `ok: true` (full showcase: 9 artifact checks, 0 composition errors, 0 warnings — a receipt with only 4 checks is basic validation, not showcase acceptance).

```bash
node bin/archify.mjs deliver lifecycle <absolute-path-json> <absolute-path-html> --quality showcase --json
```

It is the final acceptance command: it freezes the exact JSON, renders and checks that snapshot, and commits the HTML atomically.

```bash
node bin/archify.mjs visual-check <absolute-path-html>
```

It must pass — it is real-browser evidence on the delivered HTML, without re-rendering.

### Remediation playbook (if `visual-check` gives `containment fail` — ordered, no blind loops)

archify only detects height overflow in this slow step (Chrome), not in `validate`. If containment fails, follow this exact order (do not tune at random):

1. **First shrink the chrome:** merge to `<= 3` cards and shorten the items. It is the most common cause (the card that wraps to a 2nd row) and touches neither font nor geometry. Re-deliver and re-check.
2. If it persists and the one that does not fit is the SVG: **widen `viewBoxW`** (lowers the projected height at 1440). NEVER lower the 566 height (hard floor) nor the 6px font.
3. If it still does not fit in the envelope: it is a god-machine → **split the machine** (Phase 2, orthogonal principle), do not keep tuning geometry.
4. **A single `visual-check` run per change** — never blind loops. Read `scrollHeight` vs `innerHeight` in the `.visual-check.json` to know how many px are left over before touching anything.

Default output (if the user does not ask for another path): `<project-root>/docs/diagrams/<feature>-states.{json,html}` (same pattern as `bodega-ferreteria-colombia/docs/diagrams/lifecycle.json`). The `.json` is versionable and editable; the `.html` is the deliverable.

## Phase 5 — Close (without judging)

Present:

- The absolute path of the delivered HTML.
- A summary of WHAT was drawn: how many machines, how many states and transitions per machine, and what was degraded to metadata/cards and why (e.g.: "`enviado_a_caja_parcialmente` was degraded to a card because it does not enable any action different from `cerrado`").

Never a verdict of "this is broken" nor a list of findings — the human does that by opening the HTML.

The only "I cannot" case: the feature has no explicit state enum. There the close is to say exactly that and that v1 does not support it (future extension), not a best-effort attempt on implicit state.

## Future extension (out of v1)

Extraction of implicit or scattered state (combined boolean flags, state reconstructed from multiple columns without an enum, machines that exist only in documentation) — research-grade, not covered by this skill. If such a case appears, it is documented as an open decision for a future iteration of the skill, not an improvised heuristic.
