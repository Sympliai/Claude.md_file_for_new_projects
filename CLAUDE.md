# Claude Code setup kit — Claude Instructions
# Last verified: November 2026 — live repo audit

This repo is the source for a personal Claude Code setup: global rules,
permissions, a guard hook, slash commands, reviewer agents and project
templates. `install.sh` copies it into `~/.claude/`. It is a kit of
instruction files, not an application: there is no build and nothing to
deploy. Used by one person; the repo is public, so nothing private goes in it.

Universal rules live in `global-CLAUDE.md` (installed as `~/.claude/CLAUDE.md`)
and apply here too.

## Source of truth

- The repo is the source; `~/.claude/` is a copy. Edit here, then install.
  Never edit the installed copy directly.
- `README.md` is the reference for the layout and pipeline;
  `new-project-guide.md` is the beginner walkthrough; `GOAL-GUIDE.md` covers
  unattended runs.
- Backlog: `docs/BACKLOG.md` — improvements not yet made and behaviours not
  yet verified in a live session. Skim it before starting work on the kit.

## Commands (run before reporting done)

| Purpose | Command |
|---|---|
| Test the guard hook | `python3 tests/test_kit_guard.py` |
| Compare repo with installed copy | `bash install.sh --check` |
| Install into `~/.claude/` | `bash install.sh` (ask the user first: it changes their live setup) |

Definition of done for any change: the tests pass, `settings.json` and
`build-template/settings/project-settings.json` parse as JSON, and every
place that describes the changed behaviour says the same thing (see Repo map).

## Repo map

| Path | Installs to | Notes |
|---|---|---|
| `global-CLAUDE.md` | `~/.claude/CLAUDE.md` | Loaded in every session on this machine. Keep it under 200 lines. |
| `settings.json` | merged into `~/.claude/settings.json` | Permission rules and the hook entry. The installer only adds; it never removes a rule. |
| `hooks/kit-guard.py` | `~/.claude/hooks/kit/` | Secret-file guard, commit scan, read-only mode for reviewers. |
| `commands/*.md` | `~/.claude/commands/` | Slash commands. They read each other by installed path (`~/.claude/commands/<name>.md`). |
| `agents/*.md` | `~/.claude/agents/` | Reviewer subagents. |
| `templates/CLAUDE.md` | `~/.claude/templates/CLAUDE.md` | The project template. |
| `build-template/` | `~/.claude/templates/build/` | Docs skeleton, build-workflow rule, audit template, project settings. |
| `scripts/install.py` | not installed | The installer; its `file_map()` is the list above in code. |

## Project-specific rules

- `templates/CLAUDE.md` is a template. Its `{{PLACEHOLDER}}` fields and its
  "FIRST RUN — BOOTSTRAP" section are intentional. Do not fill them in, and
  do not run `/bootstrap` or `/retrofit` in this repo.
- One behaviour is usually described in several files. When changing one,
  search for the others: a command, `build-template/rules/build-workflow.md`,
  the phase and checkpoint templates, `global-CLAUDE.md`, `README.md`,
  `new-project-guide.md` and `GOAL-GUIDE.md`. The list of reviewers, for
  one, appears in most of them.
- A new file under `commands/`, `agents/`, `hooks/` or `build-template/` is
  picked up by the installer automatically. A new top-level file needs a line
  in `file_map()` and in the Repo map.
- `hooks/kit-guard.py` must never block because of its own bug: any internal
  error means "no decision". Add a test for every new rule, and build sample
  keys in tests by joining strings so the file holds no key-shaped text.
- Check claims about Claude Code behaviour (frontmatter fields, permission
  syntax, hook output) against https://code.claude.com/docs before writing
  them into the kit. Mark anything unconfirmed `UNVERIFIED:`.
- Bump `VERSION` when installed behaviour changes.
