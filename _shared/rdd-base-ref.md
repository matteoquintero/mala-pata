# RDD base-ref — scope the review to YOUR change, never the whole branch

gentle-ai's `review assess` / `review status` / `review start` take an **optional** `--base-ref`. **With no `--base-ref`, gentle bases the candidate on the merge-base against the repo's default branch (`main`).** It has NO awareness of umbrella / integration branches.

So on a branch cut from an **umbrella / integration branch** (e.g. `feature/<integration>`), a bare review takes as its candidate EVERYTHING that branch has and `main` does not — hundreds of unrelated commits and files — and marks it `applicability: unrelated`. (Observed repeatedly: `feature/rutas` → ~374 commits; `feature/compras` → 895 files based at the old fork point.)

## Rule — always pass an explicit, scoped `--base-ref`

- **Single work-unit commit** (a `shot`): `--base-ref HEAD~1 --committed-only`.
- **Multi-commit cycle** (organic / loop): `--base-ref <last reviewed boundary> --committed-only` — the first boundary is the **branch point** (where your branch left its `base`, which is the **umbrella** when `delivery_mode: ff-umbrella`, never `main`); each acknowledged review advances it.
- **NEVER** run a bare `gentle-ai review status` / `assess` (no `--base-ref`) on an umbrella/integration branch — it mis-bases to `main`.

## The whole-branch review is a different, deliberate action

Reviewing an entire umbrella/integration branch only makes sense at **`umbrella → main`** time, run explicitly with the umbrella as base — it is NOT part of per-commit RDD. If gentle's closing notice proposes a huge `unrelated` candidate, that is this mis-basing: evaluate YOUR change with the scoped `--base-ref` instead; if it returns `review_due: false`, skip, and leave the umbrella-wide review for its own moment. The pre-approved per-commit consent covers your commits, not a review of the whole integration branch.
