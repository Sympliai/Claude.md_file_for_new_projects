# Global Claude Instructions — all projects
# Install at: ~/.claude/CLAUDE.md
# Companions: ~/.claude/settings.json (enforced permissions),
#             ~/.claude/commands/ (/bootstrap, /retrofit, /checkpoint, /start, /discover,
#             /setup-build, /plan-phases, /run-phase, /new-agent),
#             ~/.claude/agents/ (reviewer subagents),
#             ~/.claude/templates/CLAUDE.md + templates/build/ (project templates).
# Project CLAUDE.md files ADD to this file; they should not repeat it.

## Who you're working with

Solo operator running multiple unrelated workstreams (agency client work, app
builds, personal projects). Sessions are short and context-switched —
optimise for a future session with zero memory of this one: leave the repo,
the docs and the CLAUDE.md in a state a stranger could pick up.

## Project documentation contract

- Every project has a `CLAUDE.md` at its root. If it still contains a
  "FIRST RUN — BOOTSTRAP" section, run `/bootstrap` before any feature work.
- No `CLAUDE.md` at all → before substantial work, offer to copy
  `~/.claude/templates/CLAUDE.md` in and run `/bootstrap`. An old, hand-written
  `CLAUDE.md` → offer `/retrofit`.
- Structural changes (new integration, top-level route/page, schema change,
  new dependency, new shared convention, design-token change) update the
  project's `CLAUDE.md` or the relevant `.claude/rules/*.md` **in the same
  turn, unprompted**. The code change is incomplete until the docs reflect it.
- Put each fact where its scope says: needed every session → `CLAUDE.md`;
  detailed reference needed only for some work → a topic file in
  `.claude/rules/` named for its section (`database.md`, `design.md`,
  `routes.md`, `integrations.md` …). Keep `CLAUDE.md` under ~150 lines.
- **Size check (automatic).** Whenever you update a `CLAUDE.md`, check its
  length. If it is over ~150 lines, split it yourself at the next commit
  checkpoint, without pausing to ask:
  - Move one whole, self-contained reference section **verbatim** (largest
    first: database, design, routes, integrations …) into
    `.claude/rules/<section-name>.md`, creating the file if needed, and leave
    a one-line pointer in `CLAUDE.md`. Never rewrite, summarise or drop
    content while moving it.
  - Never move: Commands, Project-specific rules, Session-start checklist,
    Source of truth. They are needed every session.
  - Add `paths:` frontmatter only when the scope is obviously file-bound
    (migrations, UI code); if unsure, omit it. If unsure whether a section is
    self-contained, leave it where it is.
  - Do the move in its own commit (`docs: move <section> to
    .claude/rules/<name>.md`), never bundled with feature work, and report it
    in one line (checkpoint report, or end of reply in an interactive session).
  - Automation covers growth only: never rename, merge or reorganise a rules
    folder that already exists.
- Rules files with no `paths:` frontmatter load every session, same as
  `CLAUDE.md`, so they organise but don't save context.
- A convention, gotcha or correction a future session needs goes into
  `CLAUDE.md` or a rule — not only into auto memory. Ask if unsure whether it
  is project-level.

## Safety & hygiene (all projects)

- Commit and push at natural checkpoints (feature working, task complete,
  before a risky change, end of session), in the same turn the work is
  verified — never deferred. Routine `git add` / `git commit` /
  `git push origin main` on the project's own repo is allow-listed in
  `~/.claude/settings.json`. Force-push, history rewriting and hard resets are
  denied there; if one is ever needed, explain why and let the user run it.
- Secrets: never print, log or commit secret values, and never ask for or
  accept them in chat. When a key is needed, name the variable, say it goes
  in `.env.local`, and stop. Env var *names* may appear in docs and
  `.env.example`; values live only in `.env.local` (or the host's environment
  settings). Do not read `.env*` other than `.env.example`, or any
  `PROJECT KEYS/` folder, and do not create files of key values inside a repo.
- Never edit an already-committed migration in place — add a new numbered one.
  Ask before any migration that alters or drops existing columns.
- Do not refactor, rename or "clean up" outside the current task's scope.
- Do not build speculative features or anything from planning docs unless
  explicitly asked.
- Destructive operations (dropping columns/tables, bulk file deletion,
  irreversible API calls) always get confirmed first.

## Working style

- Plain English, direct. Itemise edits specifically — copy-paste-ready over
  open-ended feedback.
- Non-trivial tasks (touches 3+ files, schema, a new integration, or anything
  ambiguous): state a short plan first and wait for a go-ahead. Trivial fixes:
  just do them.
- Definition of done: run the project's typecheck, lint and test commands
  (see the project `CLAUDE.md` → Commands) before reporting done. If a check
  can't be run, say which one and why.
- UI changes: verify in the running app when a browser tool is available;
  otherwise run the build and state plainly that it was not visually verified.
- When docs and live code disagree, live code wins; flag the discrepancy
  instead of silently reconciling toward the doc.
- Any SQL the user must run manually gets a filename stated first.
- Prefer direct fixes over workarounds; when debugging, change one variable
  at a time.
- Commit messages: Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`),
  imperative mood, subject ≤ 72 characters.
- Australian/UK spelling in prose, docs and UI copy. Code identifiers follow
  whatever the codebase already uses.

## Phased builds and subagents

- New product from an idea: `/start` runs `/discover` → `/setup-build` →
  `/plan-phases` with approval gates, then hands over `/run-phase` or a
  bounded `/goal`. Implementation never starts before the
  spec, stack and the phase are approved.
- Generic reviewer agents live in `~/.claude/agents/` (workflow-tester,
  visual-reviewer, security-reviewer, accessibility-reviewer,
  content-reviewer, phase-auditor). Reviewers report; they never edit.
- If a task needs a specialist none of them covers, propose a new agent
  (`/new-agent`) and ask before creating it.
- Subagents cost usage. Run reviewers once per phase after implementation,
  not every turn. Prefer `model: sonnet`; `haiku` only for light checks.
- Never claim a test, build, screenshot review or device flow passed unless
  it was run in this session and the result observed.

## Defaults (override per-project)

- Greenfield stack: React + TypeScript + Vite + Tailwind; Supabase (Postgres +
  Auth, RLS on by default); Vercel via GitHub integration; TanStack Query for
  server state via hooks (no raw client calls in components).
- Shareable documents as `.docx`; developer/Claude-facing files as `.md`.
- Design handoff: when a UI design export exists (Antigravity, Stitch, Figma;
  typically `DESIGN.md`, `code.html`, `screen.png`), treat it as a reference,
  not source code. Record its path in the project `CLAUDE.md` → Source of
  truth, build from it, and where the shipped code differs, the live code
  wins — flag the drift.
