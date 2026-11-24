# Doc resolution (worktree-aware) — mala-pata single source of truth

> **Re-read on apply (stale-context guard).** This is a PROCESS canonical — no output signature a hook can check — so the guard is explicit: at the moment you APPLY this rule, re-read THIS file from disk (it is a live symlink; it may have changed since it entered your context) and apply the on-disk version — it wins over any stale copy you hold.

Canonical for LOCATING a mala-pata doc (research, kickoff, roadmap, QA, finding, gaps, standard)
when the suite runs across MULTIPLE worktrees. A skill must never assume a doc lives under the
current cwd: an orchestrated phase, a feature worktree, and a radar reading from the main
checkout each see a different tree. Applied by every skill that READS a doc it did not just write.

## Resolution order (first hit wins)

1. **Declared pointer.** If the referencing artifact (or the invocation) declares `branch:`
   and/or `worktree:`, trust it: `git -C <repo> show <branch>:mala-pata/<kind>/<slug>.md` reads
   the doc from that branch WITHOUT checking it out. The declared pointer is authoritative.
2. **Current worktree.** `<repo> = git -C <cwd> rev-parse --show-toplevel`; look under
   `<repo>/mala-pata/<kind>/<slug>.md`.
3. **Sibling worktrees.** If not found, enumerate `git -C <repo> worktree list --porcelain` and
   look in each worktree's `mala-pata/<kind>/` — the doc may live in a feature worktree while you
   run from main, or the reverse.
4. **Any local branch (no checkout).** Last resort: for each local branch,
   `git show <branch>:mala-pata/<kind>/<slug>.md`. Never check a branch out to read a doc.

## Rules

- **Never assume the cwd holds the doc; never `cd` or checkout to find it.** Resolution is
  read-only against git.
- **A write-only planning doc lives on its DURABLE branch.** research / kickoff / roadmap are
  written write-only to a base branch (`main` / `development` / the feature base), not committed
  to an ephemeral worktree — so resolve via the declared `branch:` first, not the cwd.
- **Producers DECLARE where they wrote.** roadmap / kickoff / research / QA frontmatter carries
  `branch:` (the durable branch the doc was written to); an orchestrated run also carries
  `worktree:`. Readers trust that pointer; the fallback (2-4) is only for docs with no pointer.
- **Ambiguity is reported, never guessed.** If several candidates resolve and no declared pointer
  disambiguates, list the candidates and ask which worktree is authoritative — do not pick one.
