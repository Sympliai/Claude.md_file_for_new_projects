---
description: Rebuild an existing, old-style CLAUDE.md using the current template structure and a fresh live-code audit, treating the old file's contents as claims to re-verify.
---

Retrofit this project's existing `CLAUDE.md`. Run this as the only task in
this session. Extra context from the user: $ARGUMENTS

1. Read the current `CLAUDE.md` with the Read tool and keep its full contents
   in mind — this is the **old file**. Also read any existing
   `.claude/rules/*.md`.
2. Copy `~/.claude/templates/CLAUDE.md` to `./CLAUDE-template.md` and read it.
3. Rebuild `CLAUDE.md` using the template's structure by following the full
   `/bootstrap` procedure (live codebase audit, path-scoped rules, pruning,
   safety rails). Old-file contents are **claims to re-verify, not facts to
   copy** — old CLAUDE.md files are where stale facts hide.
   If `.claude/rules/` already has files, **keep their names and structure**.
   Re-verify their contents; propose (don't apply) adding `paths:`
   frontmatter or reorganising anything. Automatic splitting applies only to
   future growth, never to restructuring these.
4. Carry over anything still true, especially project-specific behavioural
   rules, known traps and warnings. Anything you confirm gets
   `CONFIRMED (<month year>, via <how>)`. Anything that no longer matches the
   code is dropped.
5. Anything that now duplicates `~/.claude/CLAUDE.md` is dropped from the
   project file (universal rules live globally).
6. Delete `CLAUDE-template.md`. Confirm no `{{` remains and no bootstrap
   section remains.
7. Commit: `docs: retrofit CLAUDE.md to current template` (include
   `.claude/rules/`). Push if a remote exists.
8. Report in ≤15 lines: what was carried over, what was **dropped and why**
   (so the user can review), what is `UNVERIFIED:`, and any `WARNING:` items.
