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
facts to copy. Then run the typecheck, lint and test commands you found,
once each, and record what you observed under the Commands table as
`Baseline (<date>): typecheck PASS · lint 3 errors · tests 41/41`. Do not
fix failures here; add each one to the backlog (section 5).

**Approved spec, no application code yet** (`docs/PRODUCT-SPEC.md` is
APPROVED): do not interview. Fill the file from `docs/PRODUCT-SPEC.md`,
`docs/ARCHITECTURE.md` and `docs/DECISIONS.md`, and mark whatever they do
not settle `TBD`. Header source: `approved spec, no code yet`.

**Empty / greenfield folder with no approved spec**: run the kickoff
interview from the template's bootstrap section, in one batch. Fill what is
decided; mark the rest `TBD`.

## 2. Verification discipline

- A fact goes in only once verified. Unconfirmed → prefix `UNVERIFIED:`.
  Never delete or guess.
- Header: `Last verified: <month year> — live codebase audit` (or
  `initial interview`).
- Where TypeScript types, docs and real schema disagree, record a `WARNING:`
  and state which one the code actually uses.

## 3. Split by scope — create path-scoped rules

Create these automatically (no need to ask). If `.claude/rules/` already
exists, keep its files and names (do not rename or merge them); verify and
fill them instead. Report in the final summary which rule files were created.
Write them **only if they
apply**:

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

**`.claude/rules/design.md`** — frontmatter:
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

**Design reference.** If the folder contains a design export (a `DESIGN.md`,
`code.html`, `screen.png` or similar, in any folder name), read it, record
its path in `CLAUDE.md` → Source of truth, and note whether it is historical
only. Do not copy its tokens into `design.md` unless they match the live
code.

In `CLAUDE.md` → "Detailed references", mark each rule `present` or `n/a`.

## 4. Prune and fill

- Delete any `CLAUDE.md` section that genuinely doesn't apply. Accurate and
  short beats aspirational and long.
- Fill the Commands table with the real scripts from `package.json`.
- Target: `CLAUDE.md` under ~150 lines after filling.

## 5. Safety rails

- `git init` + first commit if no repo exists.
- `.env.example` with names only (never values).
- Check the repo root for folders that hold keys or credentials (e.g.
  `PROJECT KEYS/`). Confirm each is gitignored and add it if missing.
  `PROJECT KEYS/` and `Project Keys/` are already read-denied globally; for
  any other name, add a `Read(<folder>/**)` deny to the project's
  `.claude/settings.json`. Do not create new key folders: secrets belong in
  `.env.local` only.
- `.gitignore` covers: `.env*` with `!.env.example`, build output,
  `CLAUDE.local.md`, `.claude/settings.local.json`.
- Backlog: if the project has no backlog file, copy
  `~/.claude/templates/build/docs/BACKLOG.md` to `docs/BACKLOG.md` and record
  its path in `CLAUDE.md` → Source of truth. Add a line for every failing
  baseline command and every `WARNING:` you recorded. This is where problems
  noticed later get logged (see the global rules), so it must exist.

## 6. Finish

- Confirm no `{{` remains anywhere in `CLAUDE.md` or the rules.
- Delete the entire "FIRST RUN — BOOTSTRAP" section.
- Commit: `docs: bootstrap CLAUDE.md from template` (include `.claude/rules/`).
- Push if a remote exists.
- Report in ≤10 lines: what was verified, what is `UNVERIFIED:` or `TBD`,
  the baseline results, which rules files were created, and any `WARNING:`
  items the user should look at. For an existing codebase, finish by
  recommending `/audit` for a full health check.
