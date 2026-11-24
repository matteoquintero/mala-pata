# Verdict glyphs — mala-pata single source of truth

Canonical lexicon for the **status / verdict glyph** that leads a state token in every
close, summary, radar and gate table across the suite. A skill that emits such a token
applies THIS verbatim: the **glyph is frozen to its meaning**; only the word paired with
it follows the skill's context. This file carries the glyph→meaning rule; each skill still
enumerates its own frozen word set next to its table (the twin of
`_shared/mala-pata-structural-labels.md`, which freezes the labels — this one freezes the
glyphs).

> **Part of the output contract.** Works together with `_shared/mala-pata-output-contract.md`
> (tables + fixed blocks, no narrative) and `_shared/mala-pata-structural-labels.md` (frozen
> English labels). A skill that applies either applies this one.

## The glyph lexicon (frozen — glyph ↔ meaning)

| Glyph | Meaning (semantics) | Context words it leads |
|---|---|---|
| `✓` | terminal POSITIVE — landed / finished / passed, proven | `done` · `complete` · `pass` |
| `◐` | STARTED but not terminal — live, partial, under way | `partial` (a close) · `in progress` (a radar) |
| `○` | NOT started — no evidence at all, nothing yet | `pending` |
| `✗` | terminal NEGATIVE — blocked, failed, stuck | `blocked` · `fail` |
| `∅` | does NOT apply to this run | `n/a` |
| `?` | work EXISTS but is not bound to this unit — confirm | `unbound` |

## The rule

1. **The glyph is frozen to its meaning.** Pick the glyph by the semantics above, never by
   the word. A positive terminal is always `✓`; a non-terminal in-flight state is always
   `◐`; nothing-yet is always `○`; a negative terminal is always `✗`; not-applicable is
   always `∅`; unbound-to-the-unit is always `?`. Never invent a glyph, never use an emoji,
   never attach a color.
2. **The word follows the skill's context, the glyph does not.** A completion table says
   `◐ partial`; a radar says `◐ in progress` — SAME glyph, because both mean "started, not
   terminal". A skill enumerates the exact word it uses (per `structural-labels`); it does
   NOT get to change the glyph that word's meaning maps to.
3. **Pair, don't bare.** Always emit the glyph AND its word together (`✓ done`, never a bare
   `✓` and never a bare `done`). The reason in `Status` / `Evidence` carries the specifics —
   a glyph is never a substitute for the evidence.
4. **No false green.** `✓` asserts a proven terminal positive. A partial, blocked, pending,
   unbound or n/a state keeps its own glyph with its reason; never round a non-terminal up to
   `✓`.

## Why this is single-sourced

The glyph set was observed to drift: `◐` meant `in progress` in the radars and `partial` in
the close tables, `✓` meant `done` in some skills and `complete` in others, and a skill could
silently omit `∅` or re-map a glyph. Freezing the glyph→meaning mapping in ONE file (while
each skill keeps its context word) stops a producer and a consumer from disagreeing on what a
glyph asserts, without flattening the legitimate word difference between a radar and a close.
