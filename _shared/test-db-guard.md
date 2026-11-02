# Test-DB guard — mala-pata single source of truth

Canonical safety rule for any skill that seeds fixtures or runs a test suite
(`mala-pata-seed`, `mala-pata-loop-start`, `mala-pata-organic-start`, and the smoke
gate). A drift here can DROP a real database — apply it verbatim.

## Never prod

Seeding and test suites run ONLY against the project's **test DB** (`TEST_DB_URL` or
the equivalent that `sdd-init` states) — **NEVER prod**. Confirm the target before
writing; if you cannot confirm it → **STOP**.

## Isolation guard (before running ANY test suite)

- The test DB **NAME and HOST** must be distinct from every real (dev/prod) DB.
- The **anti-recreation protection** must be in place (`--reuse-db` for pytest-django, or the stack's equivalent).
- If the test DB name/host **COLLIDES** with a real DB, OR the suite would run **WITHOUT** that protection (e.g. an `addopts` override that clobbers `--reuse-db`) → **STOP, do NOT run.** The runner can DROP and recreate the DB and destroy real data.
- Forward this guard into any writer/worker delegation.

## In-cycle smoke

The smoke gate runs against an **ephemeral FORK of the test DB** (never the shared base), created for the run and always dropped in cleanup. Standalone `mala-pata-seed` outside a cycle keeps its own test-DB persistence choice.
