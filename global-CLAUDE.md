# Global Claude Instructions — all projects
# Install at: ~/.claude/CLAUDE.md
# Companions: ~/.claude/settings.json (enforced permissions),
#             ~/.claude/commands/ (/bootstrap, /retrofit, /checkpoint),
#             ~/.claude/templates/CLAUDE.md (project template).
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
  needed only when touching certain files → a path-scoped rule in
  `.claude/rules/` (`paths:` frontmatter). Keep `CLAUDE.md` under ~150 lines.
  If an update pushes it past that, move the largest section into a rule in
  the same turn and say so. Monitoring size is your job, not the user's.
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
- Never print, log or commit secret values. Env var *names* may appear in
  docs; values never leave `.env.local` or the project's designated secrets
  file. Do not read `.env.local`; read `.env.example` for names.
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

## Defaults (override per-project)

- Greenfield stack: React + TypeScript + Vite + Tailwind; Supabase (Postgres +
  Auth, RLS on by default); Vercel via GitHub integration; TanStack Query for
  server state via hooks (no raw client calls in components).
- Shareable documents as `.docx`; developer/Claude-facing files as `.md`.
