#!/usr/bin/env bash
# deploy-shared.sh — deploy mala-pata's _shared rules to each compatibility skill root.
#
# Why this exists: mala-pata skills are symlinked into the agent skill roots (so skill
# edits are live), and each root's `_shared/` holds mala-pata's shared rules as PREFIXED
# SYMLINKS back to the source (`mala-pata-<name>.md` -> ~/.agent-skills/_shared/<name>.md).
# The prefix avoids colliding with the agent's own unprefixed `_shared` files; the symlink
# keeps every rule live (editing a source rule is immediately in effect — no re-deploy).
# `gentle-ai sync` does NOT create these links — this script is the deploy step, needed
# when a NEW `_shared` rule is added (existing links stay live on their own). Idempotent.
#
# Usage:
#   bash _shared/deploy-shared.sh                 # auto-detect roots where mala-pata is installed
#   bash _shared/deploy-shared.sh <root> [<root>] # deploy to explicit skill root(s)
#   MALA_PATA_SHARED_SRC=<dir> bash _shared/deploy-shared.sh   # override the source dir
#
# A root receives the deploy ONLY if a `mala-pata-*` skill is installed there, so unused
# agent roots are never touched. Only `*.md` rules are linked; scripts invoked by absolute
# source path (e.g. link-worktree-deps.sh) are intentionally not linked.
set -euo pipefail

SRC="${MALA_PATA_SHARED_SRC:-$HOME/.agent-skills/_shared}"
case "$SRC" in /*) ;; *) echo "error: source must be an absolute path: $SRC" >&2; exit 1;; esac
[ -d "$SRC" ] || { echo "error: source _shared not found: $SRC" >&2; exit 1; }

if [ "$#" -gt 0 ]; then
  ROOTS=("$@")
else
  ROOTS=(
    "$HOME/.claude/skills"
    "$HOME/.config/opencode/skills"
    "$HOME/.kiro/skills"
    "$HOME/.codex/skills"
  )
fi

deployed_any=0
for root in "${ROOTS[@]}"; do
  # deploy only where mala-pata skills actually live (avoid touching unused roots)
  ls "$root"/mala-pata-* >/dev/null 2>&1 || continue
  mkdir -p "$root/_shared"
  n=0
  for f in "$SRC"/*.md; do
    [ -e "$f" ] || continue
    b=$(basename "$f" .md)
    ln -sf "$SRC/$b.md" "$root/_shared/mala-pata-$b.md"   # prefixed symlink, overwrites copy or stale link
    n=$((n + 1))
  done
  echo "linked $n rules -> $root/_shared/ (prefixed mala-pata-* symlinks)"
  deployed_any=1
done

if [ "$deployed_any" -eq 0 ]; then
  echo "error: no skill root with mala-pata-* skills found (nothing deployed)" >&2
  exit 1
fi

# Verify: every source rule has its prefixed twin in each root that received the deploy.
miss=0
for root in "${ROOTS[@]}"; do
  ls "$root"/mala-pata-* >/dev/null 2>&1 || continue
  for f in "$SRC"/*.md; do
    [ -e "$f" ] || continue
    b=$(basename "$f" .md)
    [ -e "$root/_shared/mala-pata-$b.md" ] || { echo "MISSING: $root/_shared/mala-pata-$b.md" >&2; miss=1; }
  done
done
[ "$miss" -eq 0 ] && echo "verified: all mala-pata _shared rules resolve in every target root" || exit 1
