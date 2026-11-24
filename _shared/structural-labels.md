# Structural labels — mala-pata single source of truth

Canonical rule for the labels of every close / summary / output block. Every skill
that emits such a block applies THIS verbatim and never paraphrases or re-derives
it. Each skill ALSO enumerates its own frozen label set right next to its table —
this file carries the rule, the skill carries the data. A pointer to this file
without the enumerated set is not enough.

> **Part of the output contract.** This labels rule works together with `_shared/mala-pata-output-contract.md` — the deliverable is tables + fixed blocks, NO narrative; reason INTERNALLY and emit ONLY the block (nothing before it, nothing after it); run its pre-emit self-check. A skill that applies this rule applies that one too.

## The rule

**Structural labels are frozen.** Every label of the block — section and block
titles, BLUF labels, the **left-hand label column of a table** (Field / Milestone /
Row labels), table column headers, and enum / status tokens — is structural. Emit
it EXACTLY as listed in the skill, **verbatim in English**, even when the
conversation is in another language.

- **Never translate** a label, in any language.
- **Never swap** a listed label for a case-specific one (a label that describes this
  particular run instead of the listed one is a defect, not an improvement).
- **Never add or rename** rows. A row may be **OMITTED** only where the skill says it
  applies conditionally; it is never RENAMED.
- **Only the Value / Evidence content and the surrounding prose are localized.**

> **Status glyphs are single-sourced separately.** The glyph that leads a status token (`✓ ◐ ○ ✗ ∅ ?`) follows `_shared/mala-pata-verdict-glyphs.md` — this file freezes the label WORDS, that one freezes the glyph→meaning. A skill that emits status tokens applies both.

## Why the left column is named

A generic "labels stay English" clause was observed to fail: the agent read the
label set shown in a table as an adaptable example and re-wrote the left column in
the user's language. The label column is data the skill freezes, not a template
the agent fills with its own words.

## Scope boundary

This rule covers the skill's STRUCTURAL labels only. Content that is addressed to a
third party in its own language (for example a client-facing handout) is Value
content, not a structural label, and stays in the language the skill states for it.
