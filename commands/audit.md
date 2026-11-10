---
description: Health check for an existing codebase. Runs the project's own checks, reviews security, UX, accessibility and workflow across the whole project, and writes a ranked report with a recommended fix for each finding. Changes no product code.
argument-hint: "[area or folder to limit the audit to]"
---

Audit this project. Optional scope or note from the user: $ARGUMENTS

## Rules (AUDIT MODE)
- This is a report. Do not fix, refactor, upgrade or reformat anything during
  the audit. The only files you write are under `docs/` and
  `artifacts/audit-<date>/`.
- Every finding needs evidence: a file and line, a command and its output, or
  a screenshot path. Nothing from memory or assumption. A check you could not
  run is recorded `NOT RUN — <reason>`.
- Never print, quote or copy a secret value. Give the file, line and variable
  name.
- A critical security finding (an exposed key, data readable without signing
  in, one user able to read another's data) is reported to me the moment you
  confirm it, before the audit continues, with what I should do right now
  (for a leaked key: rotate it).
- Ask before installing anything.

## 0. Preconditions
- `CLAUDE.md` must exist and be bootstrapped. If there is none, or it still
  has a "FIRST RUN — BOOTSTRAP" section, run the bootstrap procedure first
  (read `~/.claude/commands/bootstrap.md` and follow it). If it is an old
  hand-written file, carry on and recommend `/retrofit` in the report.
- Report `git status`. Uncommitted work is fine: say so and leave it alone.
- Create `artifacts/audit-<YYYY-MM-DD>/`.

## 1. Baseline (run, observe, record)
- Run each command in `CLAUDE.md` → Commands: typecheck, lint, test, build.
  Record the exit code and counts. A failing baseline is a finding, not
  something to fix now.
- Dependencies: `npm audit --omit=dev` (or the stack's equivalent), saved to
  `artifacts/audit-<date>/dependency-audit.txt`; `npm outdated` for packages a
  major version or more behind.
- Secrets: `python3 ~/.claude/hooks/kit/kit-guard.py scan-repo` (prints
  locations only, never values). Check `.gitignore` covers `.env*` (allowing
  `.env.example`) and any key folder.

## 2. Evidence for the UI (skip if the project has no UI)
- If verification tooling is recorded in `CLAUDE.md` and works: start the app
  and capture each main route or screen in its main states (loaded, empty,
  error where reachable), at the sizes `CLAUDE.md` lists, into
  `artifacts/audit-<date>/`. Web: if an accessibility scanner (axe) is set
  up, save its results to `artifacts/audit-<date>/axe/`.
- If the app cannot be run or no tooling is set up: say what is missing and
  what it would take, mark the visual checks `NOT RUN`, and carry on with a
  code-only review. Do not install tooling now; `/setup-build` does that.

## 3. Reviewers (once each, launched together in one message)
Give each one the scope "audit" and the artifacts folder.
- `security-reviewer` — always.
- `ux-reviewer` and `accessibility-reviewer` — if the project has a UI.
- `visual-reviewer` — only if screenshots were captured.
- `workflow-tester` — only if the app runs and the main journeys are known.
- `content-reviewer` — only if `docs/CONTENT-REVIEW.md` exists.

Check each finding they return against the code before accepting it. Drop
what you cannot confirm and say how many you dropped.

## 4. Workflow and code health (you do this part yourself)
Check and record, with evidence:
- **Tests**: do they exist, what do they cover, and which critical paths
  (sign-in, payments, data writes) have none.
- **Safety nets**: typecheck and lint configured and passing; anything
  running them automatically on push; whether a push to the main branch
  deploys to production with no check in between.
- **Data**: migrations in the repo and numbered; drift between migrations,
  types and code; backups.
- **Setup**: could a new machine run this from the README and `.env.example`
  alone? Variables used in code but missing from `.env.example`.
- **Operations**: error reporting, logging of failures, what happens when an
  external service is down.
- **Code health**, high level only: dead routes, more than one pattern for
  the same job (data access, forms, state), files that everything depends on
  and nothing tests. No style opinions.
- **Docs**: where `CLAUDE.md` or the README disagree with the code.

## 5. Write the report
Copy `~/.claude/templates/build/audit/AUDIT-TEMPLATE.md` to
`docs/AUDIT-<YYYY-MM-DD>.md` and fill it:
- one entry per confirmed finding: ID (A-001 …), area, severity, effort,
  evidence, what can go wrong, recommended fix, and route (quick fix / needs
  a phase / needs a decision from me);
- severity: critical = data or money at risk now; high = likely to hurt users
  or block work soon; medium = fix in the normal run of work; low = polish;
- "Fix first": the five that remove the most risk for the least effort;
- "What is in good shape", so I know what not to worry about.

Add every finding to `docs/BACKLOG.md` (create it from
`~/.claude/templates/build/docs/BACKLOG.md` if missing) with its A-ID at the
start of the Issue column. Commit the report, backlog and artifacts:
`docs: add codebase audit <date>`.

## 6. Review with me, then stop
Show me, in plain language and at most 20 lines: the summary table, the "fix
first" list, and anything `NOT RUN`. Then ask which findings I want to:
- **fix now** — quick fixes only (small, one area, no new dependency, no
  schema change). One commit each; re-run the checks each one touches.
- **plan as phases** — anything larger. The next step is `/setup-build` (if
  this project has no `.claude/rules/build-workflow.md` yet) and then
  `/plan-phases`, which turns the chosen findings into acceptance criteria
  and phase files.
- **leave on the backlog**, or mark **won't fix** with a reason.

Record my answers in the report's Decisions table, set its Status to
`REVIEWED (<date>)`, update the backlog statuses, and commit
`docs: record audit decisions`. Fix nothing I have not chosen.
