# FIXED radar format (immutable contract)

> Scope: radar tracks `sdd/…` changes only. ODD changes (`odd/…`) are tracked via their feature-doc (`mala-pata/odd/<change>.md`), not radar.

> This format does NOT change. Same banner, same 7 columns in the same order,
> same status-light lexicon, same row order. It is mechanical memory: the
> human reacts without rereading.

## 1. Freshness banner (mandatory, always at the top)

```
RADAR · <n> SDD · <YYYY-MM-DD HH:MM>
Fresh: fetched <repo>@<sha7>[ · <repo2>@<sha7>] · integration=<branch> · live memory · READ-ONLY
```

Visual proof that it is NOT cache: the SHAs are those of the integration branch
freshly fetched in this run.

## 2. Table (exactly these 7 columns, this order)

| # | Light | SDD | Phase | Git | Depends | Next action |
|---|-------|-----|-------|-----|---------|-------------|

- **#** — index.
- **Light** — a single word from the closed lexicon (§3).
- **SDD** — change-name in `code`.
- **Phase** — most advanced phase reached in the pipeline (§4), with progress if
  partial. E.g.: `preview OK`, `apply 12/18`, `verify OK`.
- **Git** — branch/merge reality: `no branch` · `live branch` · `worktree`
  · `PR#N merged` · `in <integr>` · `stale +A/-B` (ahead/behind integr).
- **Depends** — another SDD in the list it depends on (+ `BLOCKED` if that one is not yet
  merged) or `—`.
- **Next action** — ONE single imperative step (what has to be done now).

## 3. Status-light lexicon (closed — never add new symbols)

> Closed set of 8 lights. There is NO BLUE: SDDs still in planning (kickoff … preview) are shown GREEN (in progress) unless a gate/blocker applies.

| Light | State | The human reacts |
|-------|-------|------------------|
| RED | **Your action NOW** — ready for PR, or apply/verify done without closing | do the step |
| YELLOW | **Human gate** — awaiting your approval/decision (preview, or verify with findings) | review and approve |
| ORANGE | **Parked/blocked** — depends on another SDD without merge, stale branch, or pause | unblock |
| BLACK | **No instruction** — cycle stuck, no clear next step | define what is next |
| GREEN | **In progress** — advances normally, next phase auto-runnable | run the next phase |
| MERGED | **Merged, cleanup pending** (CLEANUP) — code in integration but worktree/branch alive | clean up |
| CLOSED | **Closed** — merged + clean | nothing |
| CANCELLED | **Cancelled** — a state/decision marks it cancelled (manual/legacy marker, e.g. `ABANDONED`) | nothing |

## 4. Phase pipeline (canonical cycle order)

```
kickoff → explore → propose → spec → design → tasks → preview(gate)
→ apply → verify → archive → PR → merge → cleanup
```

## 5. Row order (ALWAYS by urgency)

```
RED → YELLOW → ORANGE → BLACK → GREEN → MERGED → CLOSED → CANCELLED
```

The human's eye goes straight to what is on top.

## 6. Evidence block (below the table, mandatory)

One line per SDD, so the state is auditable:

```
Evidence:
- <SDD> — memory: <#id/topic_key> · git: <branch|sha7|PR#N> · <1-line basis for the verdict>
```

## Example (illustrates the format; the data is sample data)

```
RADAR · 5 SDD · 2026-07-30 17:40
Fresh: fetched <repo>@3f090a3 · integration=development · live memory · READ-ONLY
```

| # | Light | SDD | Phase | Git | Depends | Next action |
|---|-------|-----|-------|-----|---------|-------------|
| 1 | RED | `cartas-datos-instancia-firme` | apply OK 18/18 | live branch, no PR | — | verify → archive → PR |
| 2 | YELLOW | `gate-verde` | preview OK | worktree | — | human gate: approve apply |
| 3 | ORANGE | `foo-bar` | tasks OK | no branch | #1 BLOCKED | waiting for merge of #1 |
| 4 | MERGED | `mora-actuarial` | merge OK PR#426 | in development | — | CLEANUP: remove worktree/branch |
| 5 | CANCELLED | `reintegro-pila` | cancelled (preview) | — | — | none |

```
Evidence:
- cartas-datos-instancia-firme — memory: sdd/.../apply-progress #7311 · git: feature/... (not in development) · 18/18 tasks, no PR
- gate-verde — memory: sdd/.../preview #… · git: worktree present · preview approved without apply
- foo-bar — memory: sdd/.../tasks #… · git: no branch · depends on #1 not merged
- mora-actuarial — memory: archive-report #7078 · git: PR#426 in development, branch deleted · merged
- reintegro-pila — memory: state #7284 = ABANDONED · git: no branch · cancelled at preview
```
