# FIXED radar format (immutable contract)

> Contract version: v2

> Scope: radar tracks `sdd/…` changes only. ODD changes (`odd/…`) are tracked via their feature-doc (`mala-pata/odd/<change>.md`), not radar.

> This format does NOT change. Same banner, same 8 columns in the same order,
> same State + Attention lexicon, same row order. It is mechanical memory: the
> human reacts without rereading.

> **Emit this block's structural labels verbatim in English** — section headers, field labels, table/column headers, and enum/option tokens stay English even when the conversation is in the user's language; only the values and content are localized.

## 1. Freshness banner (mandatory, always at the top)

```
RADAR · <n> SDD · <YYYY-MM-DD HH:MM>
Fresh: fetched <repo>@<sha7>[ · <repo2>@<sha7>] · integration=<branch> · live memory · READ-ONLY
```

Visual proof that it is NOT cache: the SHAs are those of the integration branch
freshly fetched in this run.

## 2. Table (exactly these 8 columns, this order)

Immediately ABOVE the table, one mandatory plain-text BLUF line (not fenced), counted by Attention, each count carrying glyph + number + word:

Bottom line: <n> need you now · <n> awaiting gate · <n> parked

| # | State | Attention | SDD | Phase | Git | Depends | Next action |
|---|-------|-----------|-----|-------|-----|---------|-------------|

- **#** — index.
- **State** — a glyph from the shared workflow lexicon, §3.
- **Attention** — a glyph from the closed Attention set, §3 — what the human must do now.
- **SDD** — change-name in `code`.
- **Phase** — most advanced phase reached in the pipeline (§4), with progress if
  partial. E.g.: `preview OK`, `apply 12/18`, `verify OK`.
- **Git** — branch/merge reality: `no branch` · `live branch` · `worktree`
  · `PR#N merged` · `in <integr>` · `stale +A/-B` (ahead/behind integr).
- **Depends** — another SDD in the list it depends on (+ `BLOCKED` if that one is not yet
  merged) or `—`.
- **Next action** — ONE single imperative step (what has to be done now).

## 3. State + Attention lexicon (closed — never add new symbols)

> Two closed sets, typographic glyphs only (no emoji). SDDs still in planning (kickoff … preview) are `◐ in progress · ∅ none` unless a gate/blocker applies.

**State** (shared workflow lexicon)

| State | Meaning |
|-------|---------|
| ✓ done | Merged into integration (cleanup may still be pending) |
| ◐ in progress | Cycle advancing, or waiting on a step/gate |
| ○ pending | Not started |
| ✗ blocked | Cannot advance (depends on unmerged SDD, stale, paused, or stuck) |
| ∅ n/a | Not applicable — cancelled (manual/legacy marker, e.g. `ABANDONED`) |

**Attention** (what the human must do)

| Attention | The human reacts |
|-----------|------------------|
| → needs you now | do the step (PR/close) or define the next step |
| ◆ awaiting gate | review and approve (preview, or verify with findings) |
| ‖ parked | unblock (depends on unmerged SDD, stale, or paused) |
| ⊗ cleanup pending | merged but worktree/branch still alive → remove the leftover |
| ∅ none | nothing to do — auto-advances or terminal |

## 4. Phase pipeline (canonical cycle order)

```
kickoff → explore → propose → spec → design → tasks → preview(gate)
→ apply → verify → archive → PR → merge → cleanup
```

## 5. Row order (ALWAYS by urgency, top to bottom)

```
1. → needs you now  + ◐ in progress
2. ◆ awaiting gate
3. ‖ parked
4. → needs you now  + ✗ blocked
5. ∅ none           + ◐ in progress
6. ⊗ cleanup pending + ✓ done
7. ∅ none           + ✓ done
8. ∅ n/a
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

Bottom line: → 1 need you now · ◆ 1 awaiting gate · ‖ 1 parked

| # | State | Attention | SDD | Phase | Git | Depends | Next action |
|---|-------|-----------|-----|-------|-----|---------|-------------|
| 1 | ◐ in progress | → needs you now | `cartas-datos-instancia-firme` | apply OK 18/18 | live branch, no PR | — | verify → archive → PR |
| 2 | ◐ in progress | ◆ awaiting gate | `gate-verde` | preview OK | worktree | — | human gate: approve apply |
| 3 | ✗ blocked | ‖ parked | `foo-bar` | tasks OK | no branch | #1 BLOCKED | waiting for merge of #1 |
| 4 | ✓ done | ⊗ cleanup pending | `mora-actuarial` | merge OK PR#426 | in development | — | CLEANUP: remove worktree/branch |
| 5 | ∅ n/a | ∅ none | `reintegro-pila` | cancelled (preview) | — | — | none |

```
Evidence:
- cartas-datos-instancia-firme — memory: sdd/.../apply-progress #7311 · git: feature/... (not in development) · 18/18 tasks, no PR
- gate-verde — memory: sdd/.../preview #… · git: worktree present · preview approved without apply
- foo-bar — memory: sdd/.../tasks #… · git: no branch · depends on #1 not merged
- mora-actuarial — memory: archive-report #7078 · git: PR#426 in development, branch deleted · merged
- reintegro-pila — memory: state #7284 = ABANDONED · git: no branch · cancelled at preview
```

Structure: information radiator (Cockburn) + workflow-state lexicon. Attention set + urgency order + phase pipeline = house method.
