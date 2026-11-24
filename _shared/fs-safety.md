# Filesystem safety (destructive ops near real repos) — mala-pata single source of truth

> **Re-read on apply (stale-context guard).** This is a PROCESS canonical — no output signature a hook can check — so the guard is explicit: at the moment you APPLY this rule, re-read THIS file from disk (it is a live symlink; it may have changed since it entered your context) and apply the on-disk version — it wins over any stale copy you hold.

Canonical guard against destroying a real file by running a destructive op with an ASSUMED cwd. The
sibling of `_shared/mala-pata-test-db-guard.md` (never let a runner drop a real DB), for the
filesystem. Born from a real incident: an `ln -sf <abs>/.env .env` run with the cwd mistakenly on the
real repo overwrote a real `.env` with a self-referential symlink — irrecoverable (no backup existed).

## The rule — before ANY create / overwrite / move / delete of a file

A file whose name is GENERIC or REAL (`.env`, `.env.*`, `.venv`, `credentials`, `secrets`, `*.pem`,
`*.key`, `id_rsa`, `.npmrc`, `.netrc`, `.git`, `node_modules`, a DB file):

1. **Confirm the directory FIRST.** Run `pwd`, or use an absolute path. NEVER rely on an assumed prior
   `cd`: a chained `cd && <op>` whose `cd` failed or landed elsewhere runs the op in the WRONG dir —
   the exact incident.
2. **Use ABSOLUTE paths for the target.** A bare relative name (`.env`) means "whatever the cwd is";
   that is the trap. Spell the full path so the target cannot shift under you.
3. **A symlink must point to a DIFFERENT real file.** `ln -s A B` where A resolves to B is always a bug
   (a self-referential link with no content). Never create one.
4. **Never clobber a real secret/config file.** If the destination already exists as a REGULAR file
   with a protected name, do not overwrite it — least of all with a symlink. Move/rename it first if
   you truly must replace it.
5. **Temp-clone workflows** operate with absolute paths rooted at the temp dir; verify the clone exists
   and that you are inside it before any `ln` / `rm` / `>`. Do not chain unverified `cd`s, and prefer
   `git -C <abs>` / `--prefix <abs>` over `cd`.

## Mechanical backstop

`bin/mala-pata-fs-guard.py` is a `PreToolUse` `Bash` hook that BLOCKS the two highest-confidence
disasters — a self-referential symlink, and a symlink clobbering a real protected file — while
tracking `cd` within the command. It is FAIL-OPEN and NARROW (only `ln` symlink creation): it never
gates `rm` / `mv` / `>` (too many legitimate uses), which rules 1-2 cover by discipline. Wire it as a
`PreToolUse` `Bash` command hook (runtime copy: `~/.mala-pata/bin/mala-pata-fs-guard.py`).
