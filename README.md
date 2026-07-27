# Claude Code Setup — Global Memory + Project Template

Personal Claude Code configuration system. Two files that give every machine
and every project a consistent, self-maintaining `CLAUDE.md` setup:

| File in this repo | What it is | Where it goes |
|---|---|---|
| `global-CLAUDE.md` | Universal rules for **all** projects on a device | `~/.claude/CLAUDE.md` (rename required) |
| `CLAUDE.md` | Self-bootstrapping template for **each** project | Copied to the root of every project folder |

Claude Code loads both automatically at session start. Where they conflict,
the project file wins (more specific beats more general).

---

## Setting up a new device (once per machine)

1. Clone or download this repo.
2. Copy `global-CLAUDE.md` into the `.claude` folder in your home directory:

   ```bash
   cp global-CLAUDE.md ~/.claude/CLAUDE.md
   ```

   Note the **rename to `CLAUDE.md`** — Claude Code only recognises that
   exact filename. It sits at the top level of `~/.claude/`, alongside
   `settings.json`, not inside any subfolder.
3. Verify: open Claude Code in any folder and run `/memory`. The user-level
   `~/.claude/CLAUDE.md` should appear in the loaded files list.

The global file covers: checkpoint commit/push rules, secrets hygiene,
migration discipline, working style, greenfield stack defaults, and the
contract that every project maintains its own `CLAUDE.md`.

---

## Starting a new project

1. Copy the template into the new project folder as `CLAUDE.md`:

   ```bash
   cp /path/to/this-repo/CLAUDE.md /path/to/new-project/CLAUDE.md
   ```

2. Launch Claude Code in that folder and use the prompt for your situation:

   **Empty/greenfield folder — nothing built yet:**

   > Read CLAUDE.md and execute the FIRST RUN bootstrap section.

   The bootstrap detects there's no existing code and runs the kickoff
   interview instead, so the short prompt is enough here.

   **Folder already has code, but no proper setup yet** (e.g. something
   built in Replit/Bolt/elsewhere before adopting this system) — be explicit,
   so Claude audits the real code instead of skimming a README or leaning on
   assumptions:

   > Read CLAUDE.md and execute the FIRST RUN bootstrap section. This is an
   > existing codebase, so do the full live audit path — verify everything
   > against the actual code, don't assume anything from README or docs.

3. Either way, Claude then:
   - **Existing code in the folder** → audits the live codebase
     (package.json, routes, schema/migrations, env files, config) and fills
     every placeholder with verified facts only, or
   - **Empty folder** → runs the kickoff interview, fills in what's decided,
     and marks the rest `TBD`.

   It prunes sections that don't apply, deletes the bootstrap block, and
   commits the filled file. Run this as the only task in a fresh session —
   the audit reads a lot of files and works best with a full context window.

---

## Retrofitting an existing project that already has an old CLAUDE.md

Don't overwrite the old file. Copy the template in as `CLAUDE-template.md`,
then tell Claude Code:

> This project has an existing CLAUDE.md. Read both it and
> CLAUDE-template.md, then rebuild CLAUDE.md using the template's structure
> and its FIRST RUN bootstrap process. Do a fresh audit of the live code to
> fill the placeholders — but treat the old file's contents as claims to
> re-verify, not facts to copy. Carry over anything still true (especially
> project-specific behavioural rules and known warnings), stamp anything you
> confirm as CONFIRMED with this month's date, drop anything that no longer
> matches the code, and flag what you dropped so I can review. Delete
> CLAUDE-template.md when done and commit.

The "re-verify, don't copy" instruction matters — old CLAUDE.md files are
where stale facts hide.

No manual cleanup afterwards: the prompt's final step has Claude delete
`CLAUDE-template.md` itself once the rebuilt CLAUDE.md is committed. The
template copy is only there temporarily so Claude can read both files side
by side. If you ever spot a leftover `CLAUDE-template.md` in a project, the
retrofit didn't finish — re-run it or just delete the file by hand.

---

## How it maintains itself after setup

Once bootstrapped, no manual upkeep is needed. The filled file instructs
Claude Code to:

- **Update itself in the same turn** whenever a change is structural (new
  integration, route, schema change, dependency, shared convention, or
  design-token change) — the code change counts as incomplete until the file
  reflects it.
- **Run a session-start checklist** silently: staleness check (>30 days old
  or code disagrees → re-verify), backlog check, migration-drift check after
  gaps, and uncommitted-work check.
- **Stamp its own audit trail** — `CONFIRMED (month year, via how)` and
  `RESOLVED (month year)` markers instead of silent rewrites.
- **Monitor its own size** — past ~250 lines it proposes splitting the
  largest section into that project's `.claude/rules/` folder (created
  automatically on approval; never pre-create it).

---

## Keeping devices in sync

The global file is per-device. When you improve it:

1. Edit `global-CLAUDE.md` in this repo, commit, push.
2. On each machine, pull and re-copy:

   ```bash
   git pull && cp global-CLAUDE.md ~/.claude/CLAUDE.md
   ```

Template improvements only need a commit here — new projects pick them up
the next time you copy the template in. Already-bootstrapped projects keep
their filled files and are unaffected.

---

## Layout reference

```
This repo                          A machine                 A project
─────────────                      ─────────────             ─────────────
global-CLAUDE.md  ──rename──▶      ~/.claude/CLAUDE.md
CLAUDE.md (template) ──copy──▶                               project/CLAUDE.md
README.md                                                    project/.claude/rules/*.md
                                                             (created later, only if needed)
```

Same filename, three different jobs — the location is what determines scope.
