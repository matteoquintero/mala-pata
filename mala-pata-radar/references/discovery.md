# Radar Phase A — engram-ONLY discovery, focused on ACTIVE ones

> This phase does NOT use git. It reads ONLY the SDD cycle in memory (engram) and builds
> the list of **ACTIVE candidates** — those that are NOT clearly closed nor
> cancelled. That list goes to **Phase B** (same radar,
> `state-derivation.md`), which confirms merge/branch/stale with git.
>
> **Phase A proposes, Phase B confirms.** A candidate that was actually
> merged (with no `archive-report` in memory) may show up here as active; it is NOT
> an error — Phase B reclassifies it with git downstream.
>
> Stack: memory = engram MCP (`mem_search`, `mem_get_observation`).

## Known limit (ALWAYS declare it in the output banner)

`mem_search` is semantic (FTS5), caps at **20 results** per search and has NO
enumeration by topic_key nor pagination. **There is no way to list 100% of the SDDs
with engram.** That is why this phase targets the ACTIVE set (small and
recent, where recall is enough), NOT an exhaustive inventory. If the human
needs the picture of a specific SDD that did not show up, they should pass it via an explicit
list (Phase B takes it directly, without this limit).

---

## Step 1 — Discover active candidates (engram, systematic)

Run anchor searches for the phases that indicate ACTIVITY, with `limit: 20` and
`match_mode: "any"` (more recall):

```
mem_search(query="sdd apply-progress",  limit=20, match_mode="any")
mem_search(query="sdd verify-report",   limit=20, match_mode="any")
mem_search(query="sdd preview",          limit=20, match_mode="any")
mem_search(query="sdd tasks",            limit=20, match_mode="any")
mem_search(query="sdd kickoff",          limit=20, match_mode="any")
```
If you know the domain, add the term (`sdd <domain> preview`, etc.).
From each hit, extract `<change>` from the title `sdd/<change>/<phase>`. Union =
candidates. **Loop-until-dry**: repeat with varied terms until 2
consecutive searches contribute no new `<change>`.

## Step 2 — Cycle of each candidate `C` (never a single hit)

```
mem_search(query="C", limit=20)
```
Keep ALL the `sdd/C/<phase>`. `phase(C)` = the most advanced. Order:
```
kickoff · explore · proposal · spec · design · spec-design · tasks · preview
· apply-progress · verify-report · archive-report · state
```
Confirm closure/cancellation with the content:
```
mem_get_observation(id=<most advanced phase>)
mem_get_observation(id=<state, if it exists>)
```

## Step 3 — Filter (cycle only)

Discard from the table (they are NOT active candidates):
- `CANCELLED`: a `state`/decision explicitly marks it cancelled (a manual/legacy marker — no skill emits `ABANDONED` anymore) → count it separately.
- `cerrado en ciclo`: an `archive-report` exists → count it separately (Phase B will say whether
  it is also merged/clean).

The ones that remain = **ACTIVE candidates**, with their State · Attention:
| State · Attention | phase(C) |
|-------------------|----------|
| ◐ in progress · ∅ none | apply-progress / verify-report (with code) |
| ◐ in progress · ∅ none | kickoff … preview (in planning; the closed lexicon has no separate planning state) |

---

## Output of this phase — the LIST, not a table

This phase does NOT print its own table: its result is the **filtered list of
active candidates** (+ the count of "others seen": archived/cancelled),
which goes straight to Phase B (`state-derivation.md`). The ONLY table the
human sees is the final one from `table-format.md`, already diagnosed with git.

What this phase contributes to the final banner: the **best-effort (engram
≤20/search)** disclaimer when discovery ran, and the count line
`Others seen (non-exhaustive): ✓ <n> done · ∅ none (CLOSED, with archive-report) · ∅ <m> n/a · ∅ none (CANCELLED).`

If a datum could not be read live, `?`; do NOT invent.
