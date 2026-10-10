---
description: Checkpoint the current work — run checks, update CLAUDE.md/rules if anything structural changed, commit with a Conventional Commits message, and push to main.
---

Checkpoint now. Optional note from the user: $ARGUMENTS

1. Run the project's typecheck and lint commands (from `CLAUDE.md` →
   Commands). If either fails, stop and report; do not commit broken work
   unless the user says so.
2. Review `git diff` and `git status`. If any change is structural (new
   integration, route/page, schema change, dependency, shared convention,
   design token), update `CLAUDE.md` or the relevant `.claude/rules/*.md`
   first.
3. `git add` the relevant files (never `.env*` other than `.env.example`),
   commit with a Conventional Commits message (`feat:` / `fix:` / `docs:` /
   `chore:`, imperative, ≤72-char subject), and `git push origin main`.
4. Report in one or two lines: commit hash, what changed, whether docs were
   updated.
