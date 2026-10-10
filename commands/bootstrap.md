---
description: Fill this project's template CLAUDE.md from a live codebase audit (or a kickoff interview if the folder is empty), split heavy sections into path-scoped rules, and commit.
---

Bootstrap this project's `CLAUDE.md`. Run this as the only task in this
session. Extra context from the user: $ARGUMENTS

## 0. Preconditions

- Read `CLAUDE.md` with the Read tool. If it has no "FIRST RUN — BOOTSTRAP"
  section, stop and tell the user it is already bootstrapped (suggest
  `/retrofit` if they want it rebuilt).
- If there is no `CLAUDE.md`, copy `~/.claude/templates/CLAUDE.md` to
  `./CLAUDE.md` first.

## 1. Detect project state

**Existing code present** (anything beyond config/README): do a **live
codebase audit**. Read, at minimum: `package.json` (or equivalent), entry
points, router, every migration / schema file, `.env.example` and env
references in code, build/lint/test config, hosting config, `.gitignore`,
`git remote -v`. Fill every `{{PLACEHOLDER}}` from what the code actually
does. Treat any existing README, spec or old docs as *claims to verify*, not
facts to copy.

**Empty / greenfield folder**: run the kickoff interview from the template's
bootstrap section, in one batch. Fill what is decided; mark the rest `TBD`.

## 2. Verification discipline

- A fact goes in only once verified. Unconfirmed → prefix `UNVERIFIED:`.
  Never delete or guess.
- Header: `Last verified: <month year> — live codebase audit` (or
  `initial interview`).
- Where TypeScript types, docs and real schema disagree, record a `WARNING:`
  and state which one the code actually uses.

## 3. Split by scope — create path-scoped rules

Create `.claude/rules/` and write these files **only if they apply**:

**`.claude/rules/database.md`** — frontmatter:
```
---
paths:
  - "supabase/**"
  - "**/migrations/**"
  - "src/hooks/**"
  - "src/types/**"
---
```
Contents: one block per table (columns, types, constraints, defaults, which
migration introduced it); every string-literal enum in one place
(`field: 'value' · 'value'`, plus storage keys and defaults); RLS status per
table and the policy pattern; migration rules (new numbered file per change,
never edit a committed one, dashboard changes must be reported so a matching
migration is written). Adjust `paths` to the real folders.

**`.claude/rules/design-system.md`** — frontmatter:
```
---
paths:
  - "src/**/*.{tsx,jsx,css}"
  - "tailwind.config.*"
---
```
Contents: colour tokens (dark + light if themed) as a table; typography
(fonts, loading method, icon set + "do not introduce another icon set");
spacing, radius and font-size scales; exact copy-paste class strings / JSX
skeletons for primary button, secondary button, text input, modal,
destructive action; any KNOWN DRIFT between spec docs and shipped code,
stated as "use the code, not the doc". Read live values from the token
files, not from reference docs.

In `CLAUDE.md` → "Detailed references", mark each rule `present` or `n/a`.

## 4. Prune and fill

- Delete any `CLAUDE.md` section that genuinely doesn't apply. Accurate and
  short beats aspirational and long.
- Fill the Commands table with the real scripts from `package.json`.
- Target: `CLAUDE.md` under ~150 lines after filling.

## 5. Safety rails

- `git init` + first commit if no repo exists.
- `.env.example` with names only (never values).
- `.gitignore` covers: `.env*` with `!.env.example`, build output,
  `CLAUDE.local.md`, `.claude/settings.local.json`.

## 6. Finish

- Confirm no `{{` remains anywhere in `CLAUDE.md` or the rules.
- Delete the entire "FIRST RUN — BOOTSTRAP" section.
- Commit: `docs: bootstrap CLAUDE.md from template` (include `.claude/rules/`).
- Push if a remote exists.
- Report in ≤10 lines: what was verified, what is `UNVERIFIED:` or `TBD`,
  which rules files were created, and any `WARNING:` items the user should
  look at.
