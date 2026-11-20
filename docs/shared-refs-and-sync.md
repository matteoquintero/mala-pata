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

## The sync command

The runtime root is refreshed by gentle-ai (there is no sync tooling in this repo — it is gentle-managed):

```
gentle-ai sync --dry-run   # preview the plan first (read-only)
gentle-ai sync             # deploy managed skills + the _shared compat root to the current version
```

`skills` is one of gentle-ai's managed components, and the sync deploys the `_shared` references to each compatibility skill root. Run it after adding or renaming a `_shared/` file so the new file reaches the runtime.

> **Caveat (verify, do not assume).** The `--dry-run` plan is reported at component level, so it was not confirmed file-by-file that `gentle-ai sync` deploys the mala-pata-**prefixed** `_shared` files. After running the sync, verify the new files actually landed (below). If they did not, the deploy of user-authored `_shared` files may be a separate step — check your install setup.

## Post-sync verification

After a sync, confirm every mala-pata-owned `_shared` source file has a prefixed twin in the runtime root:

```
for f in ~/.agent-skills/_shared/*.md; do
  b=$(basename "$f" .md)
  [ -f ~/.claude/skills/_shared/mala-pata-$b.md ] || echo "MISSING in runtime: mala-pata-$b.md"
done
```

No output = every rule resolves. Any `MISSING` line = that rule's prefixed refs will not resolve until it is deployed.

## Files awaiting their first deploy

As of this note, these mala-pata-owned `_shared` files are newer than the last runtime refresh and need a sync to appear in the runtime root: `standard-grounding`, `phase-status`, `rdd-base-ref`, `sdd-phase-common`, `sdd-state`. Until the sync runs, their (correctly prefixed) references do not resolve at runtime.
