# Unattended policy (RUN-MODE + PARK) — mala-pata single source of truth

> **Re-read on apply (stale-context guard).** This is a PROCESS canonical — no output signature a hook can check — so the guard is explicit: at the moment you APPLY this rule, re-read THIS file from disk (it is a live symlink; it may have changed since it entered your context) and apply the on-disk version — it wins over any stale copy you hold.

Canonical for how a skill behaves when it runs UNATTENDED — an orchestrated tab, a batch wave, any
run where no human is watching to answer a gate. Applied by every skill that would otherwise
ask-and-wait at a gate (`*-orchestrate-start`, `organic-start`, `loop-start`, `triage`, `shot`).

## RUN-MODE

- An orchestrator (`*-orchestrate-start`) INJECTS `RUN-MODE: unattended` into each phase's launch
  prompt. A directly-invoked run with a human present is `RUN-MODE: interactive` — the DEFAULT when
  the token is absent.
- A skill reads the token ONCE at start. `unattended` changes only how it handles a point where
  interactive mode would ask a human; it never changes WHAT the skill does.

## PARK instead of ask-and-wait (unattended)

Under `RUN-MODE: unattended`, a gate that interactive mode would put to a human does NOT block and
wait (nobody is there). It PARKS the decision and continues every OTHER in-scope step:
- Record it: `phase-status` `parked_decisions[]` for an orchestrated run, OR the mirror file
  `mala-pata/parked-decisions/<change>.md` for a non-orchestrated unattended run.
- Each parked item names: the **question**, the **options**, the **safe default taken** (if one
  exists) or **blocked** (none), and **what it blocks**. The run finishes everything that does NOT
  depend on the parked item.
- The orchestrator surfaces the queue ONCE at the end (one list), never mid-run. The human resolves
  the parked items in a single pass.

## What ALWAYS parks blocked (irreducibly human — never auto-answered)

A consent-gated or destructive decision NEVER gets a silent default — it parks as **blocked** (no
default) and the run does everything else:
- an RDD medium/high consent while RDD is ON,
- a `high`-delicacy smoke (`_shared/mala-pata-delicacy.md`),
- any push / PR / merge / destructive git op,
- any open PRODUCT decision (scope, behavior, who-can-do-it).

## Rules

- Unattended NEVER invents a product decision to avoid parking — inventing scope under RUN-MODE is
  the failure this closes (class 4). A product fork with no safe default parks blocked; it is not guessed.
- Unattended NEVER lowers a consent gate (RDD, delicacy, delivery) — those always park, never auto-run.
- A safe default is only taken where the decision is reversible AND has an obvious non-destructive
  choice (e.g. a formatting default); otherwise park blocked.
