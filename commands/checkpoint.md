---
description: Checkpoint the current work — run typecheck, lint and tests, update CLAUDE.md/rules and the backlog if needed, commit with a Conventional Commits message, and push the current branch.
argument-hint: "[optional note for the commit]"
---

Checkpoint now. Optional note from the user: $ARGUMENTS

1. Run the project's typecheck, lint and test commands (from `CLAUDE.md` →
   Commands). If any fails, stop and report; do not commit broken work
   unless the user says so. If a command does not exist, say which.
2. Review `git diff` and `git status`. If any change is structural (new
   integration, route/page, schema change, dependency, shared convention,
   design token), update `CLAUDE.md` or the relevant `.claude/rules/*.md`
   first. If you noticed problems outside this work that are not yet in
   `docs/BACKLOG.md`, add them now.
3. `git add` the relevant files (never `.env*` other than `.env.example`)
   and commit with a Conventional Commits message (`feat:` / `fix:` /
   `docs:` / `chore:`, imperative, ≤72-char subject). The commit guard scans
   what is being committed for key-shaped strings. If it blocks the commit,
   do not work round it: unstage the file and tell the user the file and
   line it named.
4. Push the branch you are on (`git branch --show-current`):
   - a phase branch → `git push -u origin <branch>`;
   - `main` in a project with `.claude/rules/build-workflow.md` and a phase
     IN PROGRESS or AWAITING REVIEW → stop and say so: phase work belongs on
     its branch, and `main` moves only at an approved gate;
   - otherwise → `git push origin main`.
5. Report in one or two lines: commit hash, branch, what changed, whether
   docs or the backlog were updated.
