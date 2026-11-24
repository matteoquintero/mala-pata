#!/usr/bin/env python3
"""mala-pata-fs-guard — PreToolUse(Bash) guard against the .env symlink-clobber disaster.

Blocks ONLY the two highest-confidence catastrophic symlink patterns, so it cannot
wedge ordinary work across sessions:

  1. a SELF-REFERENTIAL symlink — `ln -s A B` where A resolves to B. A symlink that
     points to itself is ALWAYS a bug; this is exactly the pattern that destroyed a
     real .env (an `ln -sf <abs>/.env .env` run with the wrong cwd).
  2. a symlink CLOBBERING a real protected file — `ln -s[f] A B` where basename(B) is
     a secret/config name AND B already exists as a REGULAR file (not a symlink).

Design invariants (mirrors mala-pata-output-lint):
- FAIL-OPEN: any parse error, missing field, or doubt -> exit 0 (ALLOW). Only a
  positively-identified disaster exits 2 (DENY) with a reason on stderr.
- NARROW: `ln` symlink creation only. rm / mv / `>` are left to the fs-safety canonical
  (prose), never mechanically blocked here — too many legitimate uses to gate safely.
- Re-pointing an existing SYMLINK is allowed (only a real regular file is protected).
"""
import sys, json, os, shlex, re

# Generic real-config / secret names an agent must never clobber with a symlink.
PROTECTED = re.compile(
    r"^(\.env(\..+)?|\.npmrc|\.netrc|credentials.*|secrets?.*|"
    r"id_rsa.*|id_ed25519.*|.*\.pem|.*\.key|.*\.keystore|\.git)$", re.I)


def allow():
    sys.exit(0)


def deny(msg):
    print(msg, file=sys.stderr)
    sys.exit(2)


def _abs(p, base):
    if not os.path.isabs(p):
        p = os.path.join(base, p)
    return os.path.normpath(p)


def check_ln(tokens, cwd):
    opts, operands = [], []
    for t in tokens[1:]:
        if t.startswith("-") and t != "-":
            opts.append(t)
        else:
            operands.append(t)
    is_symlink = any("s" in o.lstrip("-") for o in opts if not o.startswith("--")) or ("--symbolic" in opts)
    if not is_symlink or len(operands) < 2:
        return  # not a symlink, or `ln -s target` only (ambiguous) -> fail-open

    target, linkname = operands[0], operands[-1]
    link_abs = _abs(linkname, cwd)
    # linkname is an existing dir -> the link is created inside it
    if os.path.isdir(link_abs):
        link_abs = os.path.normpath(os.path.join(link_abs, os.path.basename(target)))
    # a symlink's relative target resolves against the LINK's directory
    tgt_abs = target if os.path.isabs(target) else _abs(target, os.path.dirname(link_abs))
    tgt_abs = os.path.normpath(tgt_abs)

    if tgt_abs == link_abs:
        deny("fs-guard BLOCKED a self-referential symlink: `ln` would make "
             f"'{linkname}' point to itself ({link_abs}). This is the exact pattern that "
             "destroyed a real .env. Run `pwd` to confirm your directory, use ABSOLUTE paths, "
             "and ensure the symlink target is a DIFFERENT real file.")

    base = os.path.basename(link_abs)
    if PROTECTED.match(base) and os.path.lexists(link_abs) and not os.path.islink(link_abs):
        deny("fs-guard BLOCKED overwriting a real protected file with a symlink: "
             f"'{link_abs}' exists as a regular {base} file and `ln` would replace it. If this is "
             "truly intended, move/rename the real file first — never clobber a secret/config file.")


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        allow()
    cwd = data.get("cwd") or os.getcwd()
    cmd = (data.get("tool_input") or {}).get("command", "")
    if not cmd or "ln" not in cmd:
        allow()
    tracked = cwd  # model the shell's cwd as it moves through a `cd && ... && ln` chain
    try:
        for seg in re.split(r"&&|\|\||;|\n", cmd):
            seg = seg.strip()
            try:
                toks = shlex.split(seg)
            except Exception:
                continue
            if not toks:
                continue
            if toks[0] == "cd" and len(toks) >= 2:
                cand = toks[1] if os.path.isabs(toks[1]) else os.path.normpath(os.path.join(tracked, toks[1]))
                if os.path.isdir(cand):
                    tracked = cand  # only follow a cd whose target really exists
                continue
            if toks[0] == "ln":
                check_ln(toks, tracked)
    except SystemExit:
        raise
    except Exception:
        allow()
    allow()


if __name__ == "__main__":
    main()
