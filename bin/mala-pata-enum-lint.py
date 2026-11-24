#!/usr/bin/env python3
"""mala-pata-enum-lint — single-source enum drift checker (sibling of output-lint).

Class-6 (producer/consumer vocabulary drift) enforcement: a skill that EMITS a
shared enum vocabulary must REFERENCE that vocabulary's canonical (directly, or
through a hub canonical that references it). Three vocabularies are governed:

  - verdict/status glyphs  -> _shared/mala-pata-verdict-glyphs.md
  - delicacy (low/med/high)-> _shared/mala-pata-delicacy.md
  - phase kind (code/ops/spike) -> _shared/mala-pata-phase-kind.md

FAIL-OPEN by design: any internal error prints a warning and exits 0, so it can
never break a deploy or a hook. `--strict` makes DETECTED drift exit 1 (for CI);
an internal error still exits 0 even under --strict.

Usage:
  python3 bin/mala-pata-enum-lint.py [--root <dir>] [--strict] [--quiet]
Default <root> is the repo root inferred from this script's location.
"""
import os
import re
import sys
import glob

# vocab -> (emitter detector, accepted canonical references)
# An emitter that references ANY accepted token (a direct canonical or a hub that
# itself carries the canonical) is compliant.
VOCABS = {
    "glyphs": {
        # distinctive status-lexicon glyphs (plain checklists use only the common three)
        "detect": lambda s: ("◐" in s) or ("∅" in s),  # ◐ or ∅
        "accept": ("mala-pata-verdict-glyphs", "mala-pata-output-contract",
                   "mala-pata-structural-labels"),
        "canonical": "_shared/verdict-glyphs.md",
    },
    "delicacy": {
        "detect": lambda s: ("delicacy" in s) and re.search(r"\blow\b", s)
                            and re.search(r"\bhigh\b", s),
        "accept": ("mala-pata-delicacy", "mala-pata-walkthrough-start",
                   "mala-pata-walkthrough"),
        "canonical": "_shared/delicacy.md",
    },
    "phase_kind": {
        "detect": lambda s: ("`code`" in s) and ("`ops`" in s) and ("`spike`" in s),
        "accept": ("mala-pata-phase-kind",),
        "canonical": "_shared/phase-kind.md",
    },
}

# Hub canonicals must carry the leaf canonical, or the transitive claim is false.
HUBS = {
    "_shared/output-contract.md": "mala-pata-verdict-glyphs",
    "_shared/structural-labels.md": "mala-pata-verdict-glyphs",
}


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def run(root, strict, quiet):
    findings = []  # (severity, message)

    # 1. hub integrity — the transitive chain only holds if the hub references the leaf
    for hub, needed in HUBS.items():
        p = os.path.join(root, hub)
        if not os.path.exists(p):
            continue
        if needed not in read(p):
            findings.append(("DRIFT", f"{hub}: hub does not reference `{needed}` "
                                      f"(transitive compliance via this hub is broken)"))

    # 2. consumer scan — every emitter must reference an accepted canonical
    for skill in sorted(glob.glob(os.path.join(root, "mala-pata-*", "SKILL.md"))):
        s = read(skill)
        rel = os.path.relpath(skill, root)
        for name, v in VOCABS.items():
            try:
                emits = v["detect"](s)
            except Exception:
                emits = False
            if not emits:
                continue
            if not any(tok in s for tok in v["accept"]):
                findings.append(("DRIFT", f"{rel}: emits `{name}` but references no "
                                          f"canonical (expected one of {v['accept']})"))

    if not quiet:
        if findings:
            for sev, msg in findings:
                print(f"enum-lint {sev}: {msg}", file=sys.stderr)
            print(f"enum-lint: {len(findings)} drift finding(s).", file=sys.stderr)
        else:
            print("enum-lint: OK — every emitter references its canonical.", file=sys.stderr)

    return 1 if (findings and strict) else 0


def main(argv):
    root = None
    strict = "--strict" in argv
    quiet = "--quiet" in argv
    if "--root" in argv:
        i = argv.index("--root")
        if i + 1 < len(argv):
            root = argv[i + 1]
    if root is None:
        # repo root = parent of this script's bin/ dir
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        return run(root, strict, quiet)
    except Exception as e:  # FAIL-OPEN: never break a deploy/hook on an internal error
        print(f"enum-lint: internal error, failing open (exit 0): {e}", file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
