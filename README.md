# Claude Code Setup — Global Memory + Project Template

Personal Claude Code configuration. One global rules file, one enforced
permissions file, three slash commands, and a self-bootstrapping project
template — giving every machine and every project a consistent,
self-maintaining `CLAUDE.md` setup.

| File in this repo | What it is | Where it goes |
|---|---|---|
| `global-CLAUDE.md` | Universal rules for **all** projects on a device | `~/.claude/CLAUDE.md` (rename required) |
| `settings.json` | Enforced permissions: allow routine git/npm, deny force-push, hard reset, `rm -rf`, reading `.env.local` | `~/.claude/settings.json` |
| `commands/bootstrap.md` | `/bootstrap` — fills a template CLAUDE.md from a live audit or kickoff interview | `~/.claude/commands/bootstrap.md` |
| `commands/retrofit.md` | `/retrofit` — rebuilds an old CLAUDE.md on the current template | `~/.claude/commands/retrofit.md` |
| `commands/checkpoint.md` | `/checkpoint` — checks, doc update, commit, push | `~/.claude/commands/checkpoint.md` |
| `CLAUDE.md` | Self-bootstrapping template for **each** project | `~/.claude/templates/CLAUDE.md` (so Claude can find it) **and** copied to the root of each project |

Claude Code loads `~/.claude/CLAUDE.md` and the project's `CLAUDE.md` (plus
any `.claude/rules/*.md`) at session start. They are concatenated, not
layered — so the two files are written to **not overlap**: universal rules
live only in the global file, project facts only in the project file.

---

## Why it's split this way

- **CLAUDE.md is context, not enforcement.** Claude reads it and tries to
  follow it. Anything that must be *guaranteed* (no force-push, no reading
  secrets) lives in `settings.json` deny rules, which Claude Code enforces
  regardless of permission mode. Anything routine (checkpoint commits) is
  allow-listed so Claude isn't prompted every time.
- **Every line of CLAUDE.md costs context every session.** Anthropic's
  guidance is under ~200 lines per file. Heavy reference material (database
  tables, enums, design tokens, component class strings) goes into
  `.claude/rules/*.md` with `paths:` frontmatter, which only loads when Claude
  touches matching files. The bootstrap creates these for you.
- **One-off procedures are commands, not memory.** The bootstrap and
  retrofit steps run once per project, so they live in `~/.claude/commands/`
  and are invoked by name instead of being pasted from this README.

---

## Setting up a new device (once per machine)

1. Clone or download this repo.
2. Install the pieces:

   ```bash
   mkdir -p ~/.claude/commands ~/.claude/templates
   cp global-CLAUDE.md   ~/.claude/CLAUDE.md          # note the rename
   cp settings.json      ~/.claude/settings.json
   cp commands/*.md      ~/.claude/commands/
   cp CLAUDE.md          ~/.claude/templates/CLAUDE.md
   ```

   If `~/.claude/settings.json` already exists, merge the `permissions`
   block rather than overwriting (you may have other settings in there).
3. Verify: open Claude Code in any folder and run
   - `/context` — `~/.claude/CLAUDE.md` should appear under Memory files
   - `/permissions` — the allow and deny rules should be listed
   - type `/boot` — `/bootstrap` should autocomplete

---

## Starting a new project

1. Copy the template into the new project folder:

   ```bash
   cp ~/.claude/templates/CLAUDE.md /path/to/new-project/CLAUDE.md
   ```

2. Launch Claude Code in that folder and run:

   > `/bootstrap`

   For a folder that already has code (e.g. built in Replit/Bolt before
   adopting this system), add a note so Claude does the full audit path:

   > `/bootstrap existing codebase — do the full live audit, verify everything against the actual code, don't trust the README`

3. Claude then:
   - **Existing code** → audits the live codebase (package.json, routes,
     schema/migrations, env, config) and fills every placeholder with
     verified facts only, or
   - **Empty folder** → runs the kickoff interview, fills what's decided,
     marks the rest `TBD`.
   - Creates `.claude/rules/database.md` and `.claude/rules/design-system.md`
     (only if they apply), prunes sections that don't apply, deletes the
     bootstrap block, and commits.

   Run this as the only task in a fresh session — the audit reads a lot of
   files and works best with a full context window.

---

## Retrofitting a project that already has an old CLAUDE.md

Launch Claude Code in the project and run:

> `/retrofit`

Claude reads the old file, rebuilds it on the current template with a fresh
live-code audit, carries over anything still true (stamped `CONFIRMED`),
drops anything stale, moves heavy sections into `.claude/rules/`, removes
anything that duplicates the global file, cleans up the temporary
`CLAUDE-template.md`, and commits. It reports what it dropped so you can
review. If you ever spot a leftover `CLAUDE-template.md`, the retrofit didn't
finish — re-run it or delete the file by hand.

---

## How it maintains itself after setup

- **Same-turn updates.** Structural changes (new integration, route, schema,
  dependency, shared convention, design token) update `CLAUDE.md` or the
  relevant rule in the same turn — the code change counts as incomplete until
  the docs reflect it.
- **Session-start checklist.** Staleness check (>30 days or code disagrees →
  re-verify), backlog check, uncommitted-work check, migration-drift check
  after gaps.
- **Audit trail.** `CONFIRMED (month year, via how)` and
  `RESOLVED (month year)` markers instead of silent rewrites.
- **Size self-check.** Past ~150 lines, Claude moves the largest section
  into a path-scoped rule in the same turn and says so.
- **`/checkpoint`** at any point runs checks, updates docs if needed,
  commits and pushes.

Periodically run `/doctor prompt-audit` (recent Claude Code versions) — it
flags stale, contradictory or missing-file references across all your
instruction files and proposes edits without applying them.

---

## Keeping devices in sync

The global file, settings and commands are per-device. When you improve them:

1. Edit in this repo, commit, push.
2. On each machine:

   ```bash
   git pull
   cp global-CLAUDE.md ~/.claude/CLAUDE.md
   cp settings.json    ~/.claude/settings.json
   cp commands/*.md    ~/.claude/commands/
   cp CLAUDE.md        ~/.claude/templates/CLAUDE.md
   ```

Template improvements reach new projects on their next bootstrap. Already-
bootstrapped projects keep their filled files; run `/retrofit` if you want
one brought up to the latest structure.

---

## Layout reference

```
This repo                         A machine                          A project
──────────────────                ─────────────────────────          ────────────────────────────
global-CLAUDE.md  ──rename──▶     ~/.claude/CLAUDE.md
settings.json     ──copy────▶     ~/.claude/settings.json
commands/*.md     ──copy────▶     ~/.claude/commands/*.md
CLAUDE.md (tmpl)  ──copy────▶     ~/.claude/templates/CLAUDE.md ──▶  project/CLAUDE.md
                                                                     project/.claude/rules/database.md
                                                                     project/.claude/rules/design-system.md
                                                                     project/CLAUDE.local.md (optional, gitignored)
README.md
```

Same filename, different jobs — the location determines scope.
