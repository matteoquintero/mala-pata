# `_shared/` references and the sync — maintainer note

How the suite's `_shared/` references resolve, the naming convention to follow, and the command that deploys new `_shared` files to the runtime. Read this before adding, renaming, or referencing a `_shared/` file.

## Where `_shared/` resolves at runtime

Skills reference shared rules as `_shared/<name>.md`. At runtime those resolve from each **compatibility skill root** that has mala-pata installed — e.g. `~/.claude/skills/_shared/` and `~/.codex/skills/_shared/`. That directory is real (not a symlink) and holds two kinds of file:

- **gentle-owned** references, deployed **unprefixed** by gentle-ai: `engram-convention.md`, `persistence-contract.md`, `skill-resolver.md`, `research-lifecycle.md`, `review-ledger-contract*.md`, `README.md`.
- **mala-pata-owned** references, as **prefixed symlinks** to the source (`mala-pata-<name>.md` → `~/.agent-skills/_shared/<name>.md`), created by `_shared/deploy-shared.sh` (see below). The `mala-pata-` prefix avoids colliding with the gentle-owned files; the symlink keeps each rule live.

The source of the mala-pata-owned files is **unprefixed** in the suite: `~/.agent-skills/_shared/<name>.md` (and its repo mirror `_shared/<name>.md`). The `mala-pata-` prefix is added on deploy, not in the source.

## The reference convention (follow this, or the ref dangles)

| Target | Reference it as | Why |
|---|---|---|
| A mala-pata-owned `_shared` rule (`domain-rule`, `structural-labels`, `lane-gate`, `standard-grounding`, `sdd-phase-common`, `phase-status`, `rdd-base-ref`, `sdd-state`, `spike-*`, `test-db-guard`, `wave-launch`, `route-resolution`, `git-truth`, `execution-strategies`, `bug-entry-check`, `objective-completeness`) | `` `_shared/mala-pata-<name>.md` `` | that is how it is deployed to the runtime root; an unprefixed ref does not resolve |
| A gentle-owned reference (`research-lifecycle`, `engram-convention`, `persistence-contract`, `skill-resolver`, `review-ledger-contract`) | `` `_shared/<name>.md` `` (unprefixed) | gentle deploys these unprefixed |
| `link-worktree-deps.sh` (a script, not a rule) | absolute source path `~/.agent-skills/_shared/link-worktree-deps.sh` | it is executed from source, not resolved as a runtime rule |

Rule of thumb: a `_shared` file that lives in the suite source (`~/.agent-skills/_shared/`) is mala-pata-owned → reference it **prefixed**.

## Deploying a `_shared` file to the runtime

Each compatibility skill root holds mala-pata's `_shared` rules as **prefixed symlinks** to the source. Because they are symlinks, editing a source rule is **immediately live — no re-deploy needed**. You run the deploy only when **adding a new** `_shared` rule (to create its prefixed link in each root):

```
bash _shared/deploy-shared.sh
```

It auto-detects every skill root where mala-pata is installed (e.g. `~/.claude/skills`, `~/.codex/skills`) and links all source `_shared/*.md` rules there, prefixed; roots without mala-pata installed are left untouched. Idempotent. Pass explicit roots as args, or override the source dir with `MALA_PATA_SHARED_SRC`. It verifies every rule resolves before exiting.

> **`gentle-ai sync` does NOT do this (confirmed empirically).** A `gentle-ai sync` only refreshes gentle-ai's own managed config/skills (e.g. `settings.json`, gemini guidance); it never touches the mala-pata `_shared` links. Use `deploy-shared.sh`, not the sync.

## Post-deploy verification

After deploying, confirm every mala-pata-owned `_shared` source file has a prefixed twin in the runtime root:

```
for f in ~/.agent-skills/_shared/*.md; do
  b=$(basename "$f" .md)
  [ -f ~/.claude/skills/_shared/mala-pata-$b.md ] || echo "MISSING in runtime: mala-pata-$b.md"
done
```

No output = every rule resolves. Any `MISSING` line = that rule's prefixed refs will not resolve until it is deployed.

## History

Before `deploy-shared.sh` existed, the mala-pata `_shared` links were present only in `~/.claude/skills/_shared/`, and even there the five newest rules (`standard-grounding`, `phase-status`, `rdd-base-ref`, `sdd-phase-common`, `sdd-state`) were missing. `~/.codex/skills/_shared/` had the mala-pata skills installed but **none** of the `_shared` rules — every reference there dangled. The script now links all 19 rules into every root where mala-pata is installed (claude + codex), as symlinks, and the verification passes.
