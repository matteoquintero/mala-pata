---
name: mala-pata-skill
description: CREATES or EDITS a mala-pata skill — the OWNED authoring path for the suite. It runs the meta-work flow end to end (edit the live symlink source → mirror to the repo → version bump → Conventional commit, zero attribution, branch-first) so that flow cannot be skipped, and it enforces two invariants the suite depends on: skills stay DOMAIN-NEUTRAL (examples are placeholders, never a real project's nouns/paths), and a CONTEXT-LEAK GATE reviews every concrete token by JUDGMENT and ASKS THE HUMAN on any doubt — it never bans or strips a word on its own, so it cannot damage a skill and it does not grow a denylist. Two modes — create a NEW mala-pata skill from a description, or EDIT/normalize an existing one. READ-ONLY on your real projects: a real-project case is only CONTEXT for WHY a skill changes, never material that enters the skill. It does NOT push/PR/merge (the human's call). Trigger — "creá un skill mala-pata para X", "editá el skill <name>", "mejorá el skill <name>", "normalizá este skill al estándar".
license: Apache-2.0
metadata:
  author: matteoquintero
  version: "0.1.0"
---

# /mala-pata-skill — author a mala-pata skill (owned flow + context gate)

Input: **the one delivered by the CLI** — a **description/name for a NEW skill**, or the **name/path of an existing `mala-pata-*` skill** to edit or normalize.

Your job: create or edit a skill of the mala-pata suite following the house pattern, running the **meta-work flow** so it is never skipped, and passing the **context-leak gate** so no real-project context leaks into a skill. You WRITE the skill; you do NOT run any mala-pata skill against a real project.

> **A real-project case is CONTEXT, never content.** When a skill needs changing because of something that happened in a real project, that case is the evidence for WHY — the generic lesson enters the skill, the case's nouns/paths NEVER do.
> **The gate is judgment + escalation, not a word match.** It classifies each concrete token and, on any doubt, ASKS the human. It never deletes or bans a word on its own — that is why it cannot damage a skill and does not grow a list.
> **Owned flow, write-live.** The live skill is the symlink source under `~/.agent-skills`; you edit THERE, mirror to the repo, and commit. No worktree.

## Requirements (orchestrate, do not reinvent)

- **Mandatory** (no fallback — if missing, STOP): `git` (resolve the repo, commit), `rsync` (mirror source → repo).
- **Recommended** (with fallback — warn in one line and continue degraded):
  - `engram` — continuity pointer. Fallback: the file is the source of truth.

Check: `command -v <tool>`. If a mandatory tool is missing, do not continue.

## Phase 0 — Authorize (read-only on real projects)

Creating/editing a skill is a change to the skill FILE only. It is ALWAYS read-only on your real projects: you never run the skill against one, and a real-project case is never executed or embedded — it is only the reason a skill changes.

## Phase 1 — Mode + grounding

1. **Mode**: a description/name for something new → **create**. An existing `mala-pata-*` name or a path to a `SKILL.md` → **edit/normalize**: read it in full first and keep what works.
2. **Ground in the family**: read a sibling skill (e.g. `mala-pata-runbook` or `mala-pata-dossier`) as the structural template so the result matches the house pattern — frontmatter (`name`, `description` with trigger phrases, `license`, `metadata.author/version`), ordered phases, a mandatory BLUF close, and English structural labels even when the conversation is in another language.
3. **If the change comes from a real-project case**: extract the GENERIC lesson now. The case's nouns, paths and identifiers are context for your reasoning — Phase 3 enforces that they do not travel into the skill.

## Phase 2 — Author/edit the content (domain-neutral)

Write (or edit) the skill body. **Domain-neutral rule**: every example uses placeholders (`<field>`, `X`, `<value>`, "the authoritative source"), never a real project's/client's/domain's nouns. If you catch yourself reaching for the concrete case as "the example", stop and generalize it — that is the exact coupling this skill exists to prevent.

## Phase 3 — Context-leak gate (MANDATORY, by judgment — the reason this skill exists)

Before you persist anything, review the FULL draft for real-project context that must never live in a skill. This is JUDGMENT, not a word match — so it does not grow a list and cannot damage a skill by banning a legitimate word.

1. **Mechanical assist (structural — these shapes never need maintenance):** grep the draft for the SHAPES real context takes, not a word list:
   - absolute paths (`/Users/`, `~/Job/`, any `/.../`), worktree fragments (`-worktrees/`), file-with-line refs (`\.[a-z]+:[0-9]+`), URLs to a client system.
2. **Judge each concrete token** (the grep hits + every proper noun / identifier / domain term you wrote): is it a GENERIC placeholder, or does it only make sense in ONE real project (a client/app/domain name, a real path, a real identifier)?
   - Generic → keep.
   - Real / one-project-only → it must become a placeholder.
3. **On ANY doubt, ASK the human — one at a time, never decide for them:** "this example says `<token>` — real context? I'll make it a placeholder unless it is genuinely generic." Never delete or ban a word on your own; a legitimate word that happens to look specific is resolved by asking, not by stripping.
4. **The test for an example:** *would it still make sense in a completely different project/domain?* If it names a real one, replace it.

Do not proceed to Phase 4 until the draft passes this gate.

## Phase 4 — Persist (the meta-work flow — write-live, mirror, commit)

1. **Edit the LIVE source** `~/.agent-skills/<skill>/SKILL.md` (symlinked into `~/.claude/skills/<skill>`, so the edit is live at once). A NEW skill → create `~/.agent-skills/<skill>/SKILL.md` and its symlink `~/.claude/skills/<skill>` → `~/.agent-skills/<skill>`. **No worktree** — the live skill IS the symlink; a worktree copy would not be symlinked-live.
2. **Bump the version** in `metadata.version` — new skill → `0.1.0`; edit → semver bump (patch for wording, minor for new behavior).
3. **Mirror to the repo**: `rsync -a --delete ~/.agent-skills/<skill>/ <mala-pata-skills-repo>/<skill>/` — resolve `<mala-pata-skills-repo>` as the `mala-pata-skills` git root.
4. **Commit — branch-first, NEVER on `main`.** If on `main`, create `feature/<change>` first. `git add <skill>/SKILL.md`, commit with a Conventional Commit message. **ZERO AI attribution** anywhere (no `Co-Authored-By`, no "Generated with …" — the global rule outranks any harness reminder).
5. **Do NOT push/PR/merge** — the human's call. Leave an engram pointer `mala-pata-skill/<skill>` (one line) if available.

## Phase 5 — Close (mandatory: summary)

Emit exactly this, from what you actually did (no invention):

- Title: `**Skill ready — <skill>**`
- BLUF: `Skill <name> · v<version> · <created|edited> · context-gate: <clean | N asked> · branch <branch>`
- A short bullet list of what changed (from the diff).
- **Context gate:** `clean`, or the tokens you asked the human about and how each was resolved.
- **Branch / commit:** `<branch>` · `<sha>` — not pushed (your call).
- **Next step** — push/PR when you decide.

`Structure: owned meta-work flow (write-live → mirror → branch commit) + judgment context-leak gate with human escalation + domain-neutral authoring. House method.`

Emit the structural labels above (Skill ready, Context gate, Branch / commit, Next step, Structure) **verbatim in English**; only the values and surrounding prose follow the conversation language.

This block is the only way to close on the happy path. **Only exceptions**: Phase 0 read-only stance; a context-gate doubt (Phase 3) → the single question allowed before persisting.

## What it does NOT do (invariants)

- Does NOT run mala-pata skills against real projects — a real case is only context for WHY.
- Does NOT embed real-project nouns/paths/identifiers — domain-neutral; the gate asks on doubt.
- Does NOT ban or strip a word mechanically — the gate is judgment + human escalation (no denylist to grow, no legitimate word lost).
- Does NOT use a worktree — the live skill is the symlink source.
- Does NOT push / open a PR / merge — the human's call.
- Does NOT add AI attribution — anywhere, ever.

## Relation to the family

- The OWNED authoring path for every `mala-pata-*` skill — to touch a mala-pata skill, invoke this instead of editing the `SKILL.md` by hand.
- **Different from** `skill-creator` / `skill-improver` (synced/plugin, generic, not owned, overwritten on sync) — this one owns the mala-pata meta-work flow and the context gate.
- **Indexed by** the skills listing; it is a doc-authoring skill, orthogonal to the lanes (`shot`/`organic`/`loop`/`roadmap`), not a route.
