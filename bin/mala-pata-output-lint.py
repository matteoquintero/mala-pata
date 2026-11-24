#!/usr/bin/env python3
"""
mala-pata-output-lint — Stop hook that enforces the tables-only / no-narrative
output contract on mala-pata skill deliverables.

Contract: _shared/mala-pata-output-contract.md. Prompt rules are a soft
preference the model drops under load; this hook is the mechanical backstop.

Design invariants:
- FAIL-OPEN: any error, unparseable input, or doubt -> exit 0 (never block). A
  linter must never wedge a session.
- SCOPED: only acts on a mala-pata DELIVERABLE (identified by a `Structure:`
  house-method footer, the status banner, or the banned stacked block). Ordinary
  chat is never touched.
- BLOCK ONCE: respects stop_hook_active so it can never loop.
- NARROW: flags only (1) the banned per-item stacked `#: N` block, (2)
  standalone narrative paragraphs inside a structured deliverable, and (3) a
  frozen structural label emitted in another language (structural-labels.md).
  Multi-sentence table cells and borderline prose are left to the self-check.

Contracts: _shared/mala-pata-output-contract.md + _shared/mala-pata-structural-labels.md.
"""
import sys, json, re

def _exit_ok():
    sys.exit(0)

def _block(reason):
    print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        _exit_ok()

    # Never loop: if we already blocked once this stop, let it pass.
    if data.get("stop_hook_active"):
        _exit_ok()

    tp = data.get("transcript_path")
    if not tp:
        _exit_ok()

    # Extract the last assistant text message from the transcript (fail-open).
    text = ""
    try:
        with open(tp, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for raw in reversed(lines):
            raw = raw.strip()
            if not raw:
                continue
            try:
                ev = json.loads(raw)
            except Exception:
                continue
            if ev.get("type") != "assistant":
                continue
            msg = ev.get("message", {})
            parts = msg.get("content", [])
            chunks = [p.get("text", "") for p in parts if isinstance(p, dict) and p.get("type") == "text"]
            text = "\n".join(c for c in chunks if c).strip()
            if text:
                break
    except Exception:
        _exit_ok()

    if not text:
        _exit_ok()

    body = text.split("\n")

    # --- A frozen structural label emitted translated (structural-labels.md). ---
    # Computed FIRST: a translated frozen label is BOTH a deliverable signal and a
    # violation — a fully-translated close would otherwise escape the English gate.
    # Only the most unambiguous labels, in clearly-structural positions. Fail-open.
    TRANSLATED_LABELS = [
        (r"(?mi)^\s*\*{0,2}(Estructura|Estrutura)\*{0,2}:\s", "Structure"),
        (r"(?mi)^\s*\*{0,2}(Siguiente paso|Pr[oó]ximo paso)\*{0,2}:\s", "Next step"),
        (r"(?mi)^\s*\*{0,2}Leyenda\*{0,2}:\s", "Legend"),
        (r"(?mi)\|\s*Campo\s*\|\s*Valor\s*\|", "Field | Value"),
        (r"(?mi)\|\s*Hito\s*\|\s*Estado\s*\|", "Milestone | Status"),
    ]
    translated = None
    for _pat, _canon in TRANSLATED_LABELS:
        if re.search(_pat, text):
            translated = _canon
            break

    # --- Scope: is this a mala-pata DELIVERABLE? ---
    is_deliverable = (
        re.search(r"(?mi)^\s*Structure:\s", text) is not None
        or re.search(r"(?mi)^\s*(Roadmap|Source|Bottom line|Timeline|Plan):\s", text) is not None
        or re.search(r"(?m)^#:?\s*\d+\b", text) is not None
        or translated is not None
    )
    if not is_deliverable:
        _exit_ok()

    STACK_LABELS = r"(Phase|slug|Route|Route \(actual\)|Depends on|Status|Evidence|Kind|Tentative route|Vertical slice|Wave|Parallelizes with|Note|Finding|Principle violated|Severity|Change|Disposition)"

    # --- Defect 1: the banned per-item stacked block (#: N then stacked labels) ---
    stacked = False
    for i, ln in enumerate(body):
        if re.match(r"^\s*#:?\s*\d+\b", ln):
            lookahead = body[i + 1 : i + 4]
            if any(re.match(r"^\s*\*{0,2}" + STACK_LABELS + r"\*{0,2}:\s", x) for x in lookahead):
                stacked = True
                break

    # --- Defect 2: standalone narrative paragraphs in a structured deliverable ---
    def is_structural(ln):
        s = ln.strip()
        if not s:
            return True
        if "|" in s:                                  # table row
            return True
        if s[0] in "#-*>`✓◐○✗⚑|·▲●▼":                 # heading/list/quote/code/glyph/banner
            return True
        if re.match(r"^\*{0,2}[A-Z][A-Za-z /()#-]{1,40}\*{0,2}:\s", s):  # labeled block line
            return True
        if re.match(r"^\s*(Structure|Legend|Next step|Bottom line|Ready to start now|In progress now|Blocked|Source|Timeline|Roadmap|Plan|Banner):", s):
            return True
        return False

    def wordcount(ln):
        return len(re.findall(r"\b\w+\b", ln))

    has_table = any("|" in ln for ln in body)
    narrative = False
    narrative_lines = 0
    for ln in body:
        if not is_structural(ln) and wordcount(ln) >= 14:
            narrative_lines += 1
    # Only a structured deliverable (has a table) with real prose paragraphs is flagged.
    if has_table and narrative_lines >= 1:
        narrative = True

    if not (stacked or narrative or translated):
        _exit_ok()

    reasons = []
    if stacked:
        reasons.append("a banned per-item stacked `#: N` block (one label per line) — emit items as TABLE ROWS, one row per item, one line per cell")
    if narrative:
        reasons.append("standalone narrative prose — the deliverable is tables + fixed blocks only; reason internally and emit ONLY the block (no preamble/recap outside the single BLUF line)")
    if translated:
        reasons.append("a frozen structural label emitted in another language (e.g. `" + translated + "`) — structural labels are verbatim English per _shared/mala-pata-structural-labels.md; only values and prose are localized. Re-emit with the English label")

    _block(
        "Output-contract violation (_shared/mala-pata-output-contract.md): "
        + "; ".join(reasons)
        + ". Re-emit the deliverable now as tables-only, nothing before the first block or after the last."
    )

if __name__ == "__main__":
    main()
