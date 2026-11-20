# Canonical output contract (tables-only / no-narrative) — single source of truth

Apply this verbatim wherever a skill references it. A skill's DELIVERABLE (its status / result / close block) is a fixed set of TABLES and labeled blocks — NOT narrative prose. Reasoning happens internally and is NEVER emitted.

## What may be emitted
- **Tables** — a real Markdown table (never fenced), one ROW per item, one line per cell.
- **Fixed labeled blocks** — the exact banner / BLUF / legend / footer lines the skill defines, verbatim.
- **At most ONE BLUF / decision line** of prose (a verdict, a bottom-line), plus any question the skill EXPLICITLY mandates. Nothing else is prose.

## Banned shapes (never emit)
- **Narrative paragraphs** — any free-flowing prose that recaps, explains, contextualizes, or editorializes ("Four of the five phases are already in development…", "I mentioned it as an option…", "Let me explain…"). The deliverable has none.
- **Preamble / trailing commentary** — NOTHING before the first block and NOTHING after the last. No "Here's the status:", no closing remark, no "¿arranco?".
- **The per-item stacked block** — one label per line (`#: 1` / `Field:` / `Field:` …), items split by `---` rules. Items ALWAYS go in table ROWS (one row per item, one line per cell). This stacked shape is the single most common defect; it is never acceptable.

## The two enforcement mechanisms (both mandatory)
1. **Fill-in template.** The skill gives the EXACT skeleton to fill. Reason internally FIRST, then emit ONLY the filled skeleton and stop. The template leaves no room to narrate — do not add any line it does not define.
2. **Pre-emit self-check.** Before emitting, scan your own output line by line. Any line that is NOT (a) a table row / header, (b) one of the skill's fixed labeled-block lines, or (c) the single allowed BLUF line / a mandated question is NARRATIVE → rewrite it into the table, or delete it. Emit only after the output passes this check.

This contract is mechanically checkable: a line is a table row, a known block line, or the single BLUF — otherwise it is narrative and must not ship. The self-check is the gate; no narrative passes it.
