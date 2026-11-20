# `_shared/` references and the sync — maintainer note

How the suite's `_shared/` references resolve, the naming convention to follow, and the command that deploys new `_shared` files to the runtime. Read this before adding, renaming, or referencing a `_shared/` file.

## Where `_shared/` resolves at runtime

Skills reference shared rules as `_shared/<name>.md`. At runtime those resolve from the **gentle-ai compatibility skill root**: `~/.claude/skills/_shared/`. That directory is a real copy (not a symlink), populated by gentle-ai's install/sync, and it holds two kinds of file:

- **gentle-owned** references, deployed **unprefixed**: `engram-convention.md`, `persistence-contract.md`, `skill-resolver.md`, `research-lifecycle.md`, `review-ledger-contract*.md`, `README.md`.
- **mala-pata-owned** references, deployed **prefixed** with `mala-pata-` (to avoid colliding with the gentle-owned ones): e.g. `mala-pata-domain-rule.md`, `mala-pata-structural-labels.md`, `mala-pata-lane-gate.md`.

The source of the mala-pata-owned files is **unprefixed** in the suite: `~/.agent-skills/_shared/<name>.md` (and its repo mirror `_shared/<name>.md`). The `mala-pata-` prefix is added on deploy, not in the source.

## The reference convention (follow this, or the ref dangles)

| Target | Reference it as | Why |
|---|---|---|
| A mala-pata-owned `_shared` rule (`domain-rule`, `structural-labels`, `lane-gate`, `standard-grounding`, `sdd-phase-common`, `phase-status`, `rdd-base-ref`, `sdd-state`, `spike-*`, `test-db-guard`, `wave-launch`, `route-resolution`, `git-truth`, `execution-strategies`, `bug-entry-check`, `objective-completeness`) | `` `_shared/mala-pata-<name>.md` `` | that is how it is deployed to the runtime root; an unprefixed ref does not resolve |
| A gentle-owned reference (`research-lifecycle`, `engram-convention`, `persistence-contract`, `skill-resolver`, `review-ledger-contract`) | `` `_shared/<name>.md` `` (unprefixed) | gentle deploys these unprefixed |
| `link-worktree-deps.sh` (a script, not a rule) | absolute source path `~/.agent-skills/_shared/link-worktree-deps.sh` | it is executed from source, not resolved as a runtime rule |

Rule of thumb: a `_shared` file that lives in the suite source (`~/.agent-skills/_shared/`) is mala-pata-owned → reference it **prefixed**.

## Deploying a `_shared` file to the runtime

The mala-pata skills themselves are **symlinked** into `~/.claude/skills/` (so skill edits are live automatically), but the runtime `_shared/` is a real **copy** directory — a new or changed mala-pata `_shared` file must be deployed to it explicitly, **prefixed**:

```
cp ~/.agent-skills/_shared/<name>.md ~/.claude/skills/_shared/mala-pata-<name>.md
```

> **`gentle-ai sync` does NOT do this (confirmed empirically).** A `gentle-ai sync` only refreshes gentle-ai's own managed config/skills (e.g. `settings.json`, gemini guidance); it does NOT deploy the user-authored mala-pata `_shared` files. The original prefixed mala-pata `_shared` files were put in the runtime root by a separate deploy step — not `gentle-ai sync`, and no tooling for it lives in this repo. Until a dedicated deploy tool is set up, copy new/changed `_shared` files by hand as above.

> **The runtime files are copies, not symlinks** — editing `~/.agent-skills/_shared/<name>.md` later does NOT auto-update the runtime copy. Re-run the `cp` after any edit, for every compatibility skill root in use.

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

`standard-grounding`, `phase-status`, `rdd-base-ref`, `sdd-phase-common`, `sdd-state` were deployed to the runtime root by hand (the `cp` above) after a `gentle-ai sync` was observed NOT to deploy them. The verification above then passed for every mala-pata-owned `_shared` file.
