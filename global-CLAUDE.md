# Global Claude Instructions — all projects
# Install at: ~/.claude/CLAUDE.md
# These apply to every Claude Code session. Project CLAUDE.md files override
# these where they conflict (more specific wins).

## Who you're working with

Solo operator running multiple unrelated workstreams (agency client work, app
builds, personal projects). Sessions are often short and context-switched —
optimise for a future session with zero memory of this one: leave the repo,
the docs, and the CLAUDE.md in a state a stranger could pick up.

## Project documentation contract

- Every project gets a `CLAUDE.md` at its root. If a new project folder has
  the template version (contains a "FIRST RUN — BOOTSTRAP" section), execute
  that bootstrap before any feature work.
- If a project folder has **no** CLAUDE.md at all, offer to create one from
  the template before substantial work begins.
- Structural changes (new integration, route, schema change, dependency,
  shared convention, design-token change) update the project's CLAUDE.md in
  the same turn, unprompted. The code change is incomplete until the file
  reflects it.
- Monitoring CLAUDE.md size is Claude's responsibility in every project:
  whenever updating a project's CLAUDE.md, check its length, and if it has
  grown past ~250 lines, propose moving the largest self-contained section
  into that project's `.claude/rules/` folder. Never leave this for the user
  to notice.

## Safety & hygiene (all projects)

- Commit and push at natural checkpoints (feature working, task complete,
  before risky changes, end of session). Routine add/commit/push to the
  project's own main branch is pre-authorised; force-push, history rewriting,
  and hard resets always require explicit approval.
- Never print, log, or commit secret values. Env var *names* may appear in
  docs; values never leave `.env.local` / the project's designated secrets
  file.
- Never edit an already-committed migration in place — add a new numbered one.
- Do not refactor, rename, or "clean up" outside the current task's scope.
- Do not build speculative features or anything from planning docs unless
  explicitly asked.
- Destructive operations (dropping columns/tables, deleting files in bulk,
  irreversible API calls) always get confirmed first, regardless of any
  standing pre-authorisation.

## Working style

- Plain English, direct. When giving edits, itemise them specifically —
  copy-paste-ready over open-ended feedback.
- When docs and live code disagree, live code wins; flag the discrepancy
  instead of silently reconciling toward the doc.
- Verify UI changes in the running app before reporting done.
- Any SQL the user must run manually gets a filename stated first.
- Prefer direct fixes over workarounds that create new problems; when
  debugging, isolate by testing one variable at a time.

## Defaults (override per-project)

- Preferred stack when proposing greenfield builds: React + TypeScript +
  Vite + Tailwind; Supabase (Postgres + Auth, RLS on by default); Vercel via
  GitHub integration; TanStack Query for server state via hooks (no raw
  client calls in components).
- Shareable documents as `.docx`; developer/Claude-facing files as `.md`.
