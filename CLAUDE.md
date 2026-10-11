# {{PROJECT_NAME}} — Claude Instructions
# Last verified: {{DATE}} — {{SOURCE: "live codebase audit" | "initial interview" | "template, unverified"}}

{{ONE_PARAGRAPH: what this project is, who uses it, the core model (e.g.
single-tenant per user), and one sentence on what is PLANNED but NOT BUILT so
it never gets assumed into existence.}}

Universal rules (git checkpoints, secrets, scope discipline, working style)
live in `~/.claude/CLAUDE.md` and are not repeated here. This file holds only
what is specific to this project.

---

## ⚠️ FIRST RUN — BOOTSTRAP (delete this entire section once complete)

If this section exists, this file is an unfilled template. Run `/bootstrap`
(preferred — it contains the full procedure) or follow this summary **before
any feature work**:

1. **Detect state.** Existing code → live audit of `package.json`, entry
   points, router, schema/migrations, `.env.example`, config. Fill every
   `{{PLACEHOLDER}}` from what the code *actually does* — never from a README
   or assumptions. Empty folder → run the kickoff interview, fill what is
   decided, mark the rest `TBD`.
2. **Verify or mark.** Unconfirmed claims get `UNVERIFIED:` in front, never
   deleted or guessed. Date the header.
3. **Split by scope.** Where they apply, create database tables, enums, RLS →
   `.claude/rules/database.md` and design tokens, component standards →
   `.claude/rules/design.md`. Add `paths:` frontmatter where a rule only
   matters for certain files. If `.claude/rules/` already exists, keep its
   files and names. Delete any section that doesn't apply.
4. **Safety rails.** `git init` + first commit if needed; `.env.example` with
   names only; `.gitignore` covers `.env*` (allow `!.env.example`), build
   output, `CLAUDE.local.md`, `.claude/settings.local.json`.
5. **Finish.** No `{{` may remain. Delete this section, update the header, and
   commit: `docs: bootstrap CLAUDE.md from template`.

**Kickoff interview (greenfield only)** — ask in one batch:
- What are we building, for whom, and what does "done for v1" look like?
  What is explicitly out of scope for v1?
- Stack preferences, or should I propose one? (Default: React + TypeScript +
  Vite + Tailwind, Supabase, Vercel, GitHub.)
- Design reference (screenshots, existing site, palette, fonts)?
- External services/APIs from day one? Any planned-but-later (record under
  Integrations as NOT WIRED)?
- Where do secrets live? Repo name and visibility?

---

## Session-start checklist (silent, every session)

1. **Staleness.** If `Last verified` is >30 days old, or the first task touches
   an area this file describes and the code disagrees — re-verify that section
   against live code before building on it, update it, flag the drift in one
   line.
2. **Backlog.** If a backlog file exists (below), skim it before assuming any
   feature is done. It is a backlog, not a changelog.
3. **Uncommitted work.** If `git status` shows meaningful work from a prior
   session, say so before starting anything new.
4. **Migration drift** (after a gap, or before a big feature, if a DB exists):
   sanity-check committed migrations against the live schema.

---

## Keeping this file current

Structural change → update this file or the relevant `.claude/rules/*.md` in
the same turn (see global rules). Stamp `RESOLVED (<month year>)` and
`CONFIRMED (<month year>, via <how>)` rather than silently rewriting — the
audit trail is the point. If this file passes ~150 lines, split it automatically at the next
checkpoint per the global rules: verbatim move of one self-contained
reference section into `.claude/rules/<name>.md`, one-line pointer left
here, its own `docs:` commit, noted `RESOLVED`. Commands, Project-specific
rules, Session-start checklist and Source of truth never move.

---

## Source of truth & docs

- This file wins for "how we work"; live code wins for "what exists".
- Build spec: {{PATH + one line on status/drift, or "none"}}
- Design reference: {{PATH to the design export (e.g. `design/` with
  `DESIGN.md`, `code.html`, `screen.png` from Antigravity/Stitch/Figma) and
  whether it is historical-only, or "none"}}. Live code wins where they differ.
- Backlog / punch list: {{PATH, or "none"}}
- Planning docs (NOT built): {{PATHS — nothing in them is implemented; build
  nothing from them unless asked}}

---

## Commands (run before reporting done)

| Purpose | Command |
|---|---|
| Dev server | `{{DEV_COMMAND}}` → {{DEV_URL}} |
| Typecheck | `{{TYPECHECK_COMMAND}}` |
| Lint | `{{LINT_COMMAND}}` |
| Test | `{{TEST_COMMAND}}` |
| Build | `{{BUILD_COMMAND}}` |
| New migration | `{{MIGRATION_COMMAND or "create <NNN>_<name>.sql in <path>"}}` |

Definition of done for any code change: typecheck + lint + relevant tests
pass. {{ADDITIONAL_DONE_CRITERIA, e.g. "preview deploy green on Vercel"}}

---

## Verification tooling

How the running app is exercised and evidenced (filled by `/setup-build`;
verify each tool actually runs before listing it as available).

| Platform | Tool | Launch command | Flow files | Screenshot command / sizes |
|---|---|---|---|---|
| {{web / ios / android}} | {{Playwright | Chrome integration | Maestro + simulator}} | `{{LAUNCH_COMMAND}}` | `{{e2e/ | .maestro/}}` | `{{COMMAND}}` · {{e.g. 390px & 1440px | iPhone 15 & Pixel 7}} |

Not available / not set up: {{list, or "none"}}. A check that cannot be run
is recorded `NOT RUN — <reason>`, never assumed.

---

## Phased build workflow

If `.claude/rules/build-workflow.md` exists, this project is built in
approved phases: `docs/phases/PHASE-NN-*.md` is the only scope, every phase
ends at a human-reviewed gate with a committed `CHECKPOINT-NN.md`, and
reviewer agents run once per phase. Commands: `/discover` → `/setup-build` →
`/plan-phases` → `/run-phase` (or `/goal` using the phase file's Ready-to-run
section). {{"present" | "n/a — not a phased build"}}

---

## Stack

{{STACK: framework + language + build tool; styling; routing; state/data
fetching and its rule (e.g. "every backend read/write goes through a hook in
src/hooks/, never raw client calls in components"); key libraries with major
versions; backend; hosting + deploy trigger; repo URL + branch + where the git
root actually is.}}

## Repo map

{{REPO_MAP: 5–10 lines — where things live and the rule for each, e.g.
`src/hooks/` — all Supabase access; `supabase/migrations/` — numbered SQL;
`src/components/ui/` — shared primitives only. Skip anything obvious from
the folder names.}}

---

## Routes

{{ROUTES: route → page component, auth wrapper noted. WARNING block for any
nav inconsistency (desktop vs mobile drift). Rule: a new top-level route means
updating every nav surface.}}

---

## Env vars (names only — never print or log values)

{{ENV_VARS: complete list, grouped by runtime. State where values live
(e.g. `.env.local`, gitignored).}}

---

## Integrations & AI usage

{{INTEGRATIONS: one line per service, tagged WIRED or NOT WIRED with one
clause of evidence. NOT WIRED items say "no code, no env vars, nothing
scaffolded".}}

AI/LLM: {{"None — no LLM API calls, keys or SDK deps (verified by grep)" |
providers, where called, which env vars. Adding one later is a structural
change.}}

---

## Security / auth

{{SECURITY: Supabase — RLS status per table, policy pattern, rule for new
tables. Other backends — auth model, authorisation pattern, rule new
endpoints must follow. CONFIRMED-date anything verified. Full per-table RLS
detail lives in `.claude/rules/database.md`.}}

---

## Detailed references (path-scoped rules, load on demand)

- `.claude/rules/database.md` — tables, columns, enums, migrations, RLS.
  {{"present" | "n/a — no database"}}
- `.claude/rules/design.md` — tokens, typography, icon set, component
  class strings. {{"present" | "n/a — no UI"}}
- {{OTHER_RULES, or remove}}

---

## Project-specific rules

{{PROJECT_SPECIFIC_RULES: anything learned the hard way here — known traps,
things that look wrong but are intentional, areas not to touch. Do not
repeat global rules.}}
