# {{PROJECT_NAME}} — Claude Instructions
# Last verified: {{DATE}} — {{SOURCE: "live codebase audit" | "initial interview" | "template, unverified"}}

{{ONE_PARAGRAPH_DESCRIPTION: what this project is, who uses it, the core model
(e.g. single-tenant per user), and one sentence on what is PLANNED but NOT
BUILT so it never gets assumed into existence.}}

---

## ⚠️ FIRST RUN — BOOTSTRAP (delete this entire section once complete)

If this section still exists, this file is an unfilled template. **Do this
before any feature work**, in this order:

1. **Detect project state.**
   - Existing codebase in this folder → do a **live codebase audit**: read
     `package.json` (or equivalent), entry points, router, schema/migrations,
     env examples, config files. Fill every `{{PLACEHOLDER}}` below from what
     the code *actually does* — never from assumptions or from docs alone.
   - Empty/greenfield folder → run the **kickoff interview** (below), then
     fill in what's decided and mark everything else `TBD`.
2. **Verification discipline.** Every factual claim gets filled only when
   verified. If something can't be confirmed, write `UNVERIFIED:` in front of
   it rather than deleting or guessing. Date the header
   (`Last verified: <month year> — <how>`).
3. **Prune.** Delete any section below that genuinely doesn't apply (e.g. no
   database → delete Database, Enums, RLS). An accurate short file beats an
   aspirational long one.
4. **Initialise safety rails** if missing: `git init` + first commit; create
   `.env.example` with names only; confirm `.gitignore` covers `.env*`,
   secrets, and build output.
5. **Delete this BOOTSTRAP section**, update the header date, and commit the
   filled file with message `docs: bootstrap CLAUDE.md from template`.

**Kickoff interview (greenfield only)** — ask, in one batch:
- What are we building, for whom, and what does "done for v1" look like?
- Stack preferences, or should I propose one? (Default assumption if none:
  React + TypeScript + Vite + Tailwind, Supabase backend, Vercel hosting,
  GitHub repo — override freely.)
- Is there a design reference (screenshots, existing site, hex palette, fonts)?
- Any external services/APIs from day one? Any that are planned-but-later
  (record under Integrations as NOT WIRED)?
- Where do secrets live, and what's the repo name/visibility?

---

## Keeping this file current (non-negotiable)

Whenever a change in a session is **structural** — a new integration, new
top-level route/page, schema change, new third-party dependency, a new
global/shared convention or standard pattern, or a global styling/design-token
change — **update this file in the same turn, without being asked.** Treat the
code change as incomplete until this file reflects it. Small/local edits (one
component's copy, a single bug fix, a one-off style tweak) don't require an
update.

When updating: stamp resolved items `RESOLVED (<month year>)` and confirmed
facts `CONFIRMED (<month year>, via <how>)` rather than silently rewriting —
the audit trail is the point.

**Size self-check (Claude's job, not the user's).** Every time this file is
updated, check its length. If it exceeds ~250 lines, propose splitting the
largest self-contained section (usually Component standards or Database) into
`.claude/rules/<section>.md` in this project folder, leaving a one-line
pointer here. Do the split only after the user approves, commit it, and note
it as `RESOLVED`. The user never needs to monitor line counts.

---

## Session-start checklist (run silently at the start of every session)

1. **Staleness check.** If `Last verified` is >30 days old, or the first task
   of the session touches an area this file describes and the code disagrees
   with the file — re-verify that section against the live code *before*
   building on it, and update the file. Flag the drift to the user in one line.
2. **Backlog check.** If a backlog/punch-list file exists (see Source of
   truth), skim it before assuming any feature is "done". It's a backlog, not
   a changelog — items may be superseded by later instructions.
3. **Gap check.** If picking the project up after a gap (or before a big new
   feature) and a database exists: sanity-check committed migrations against
   the live schema rather than assuming they're in sync.
4. **Uncommitted-work check.** If `git status` shows meaningful uncommitted
   work from a prior session, tell the user before starting anything new.

---

## Disaster mitigation — periodic backups (non-negotiable)

1. **Code — commit and push at every natural checkpoint, in the same turn the
   work is verified.** A checkpoint is: a requested feature/fix is working, a
   task is complete, or meaningful work is about to be interrupted (context
   compaction, end of session, before a risky change). **Do not defer the
   push** — if the session ends before it happens the changes are lost.
   This rule **pre-authorises routine `git add` / `git commit` /
   `git push origin main`** at checkpoints without asking each time. It does
   **not** extend to force-push, history rewriting, `git reset --hard`, or
   pushing to any other branch/remote — those stay gated by normal safety rules.
2. **Schema — every change gets a migration file; drift gets audited.**
   - Any schema change made in a session gets its own new, numbered migration
     file in `{{MIGRATIONS_PATH}}` in the same turn. Never edit an
     already-committed migration in place — add a new one.
   - Schema changes made outside a session (dashboard/SQL editor) are
     invisible to me — user: mention them so a matching migration gets
     written.
   - Provider automatic backups protect *data*; committed migrations protect
     the ability to *reconstruct the schema* elsewhere. Both are needed;
     neither replaces the other.

---

## Source of truth & docs

- **This file wins for "how we work"; the live code wins for "what exists".**
  Where any spec/design doc disagrees with the live code, the live code wins —
  flag the discrepancy rather than silently "fixing" toward the old doc.
- {{BUILD_SPEC: path + one line on status/drift, or "none"}}
- {{DESIGN_REFERENCE: path + whether historical-only, or "none"}}
- {{BACKLOG_FILE: path to punch list, or "none"}}
- {{PLANNING_DOCS: paths for planned-but-NOT-built features — state explicitly
  that nothing in them is implemented and none should be built unless asked}}

---

## Stack

{{STACK: framework + language + build tool; styling approach; routing; state/
data-fetching approach and the rule for it (e.g. "every backend read/write
goes through a hook in src/hooks/, never raw client calls in components");
key libraries with major versions; backend; hosting + deploy trigger; lint/
format/test commands; repo URL + branch + where the git root actually is.}}

Dev server: `{{DEV_COMMAND}}` ({{DEV_URL}}).

---

## AI model usage

{{AI_USAGE: "None — no LLM API calls, keys, or SDK deps (verified by grep)" |
list of providers, where called, which env vars. If none: note that adding one
later is new infrastructure and a structural change per the update rule.}}

---

## Database — actual tables

{{DB_TABLES: one block per table — columns, types, constraints, defaults,
which migration introduced each. Include WARNINGs for any mismatch between
TypeScript types and real columns (dead fields, columns referenced in code
but absent from migrations). If no database, delete this section.}}

---

## Exact status / enum values

{{ENUMS: every string-literal enum in one place — field: 'value' · 'value'.
Include storage keys and defaults (e.g. theme persisted to localStorage).}}

---

## Routes

{{ROUTES: route → page component map, auth wrapper noted. Include a WARNING
block for any nav inconsistencies (e.g. desktop vs mobile nav drift), and the
rule: adding a top-level route means updating every nav surface.}}

---

## Design system — use these exact values

Read live values from {{DESIGN_TOKEN_FILES}} — not from reference docs.

{{DESIGN_TOKENS: core color tokens as a table (dark + light if themed);
typography (fonts, loading method, icon set + "do not introduce another icon
set"); spacing scale; radius conventions; custom font-size scale; any KNOWN
DRIFT between spec docs and shipped code, stated explicitly with "use the
code, not the doc".}}

---

## Component standards

{{STANDARDS: exact copy-paste class strings / JSX skeletons for the dominant
patterns — primary button, secondary button, text input, modal, destructive
action. Each is a rule, not a suggestion. When a genuinely new pattern is
designed, document it here in the same turn per the update rule.}}

---

## Env vars (names only — never print or log values)

{{ENV_VARS: complete list of names, grouped by runtime. State where actual
values live (e.g. `.env.local`, gitignored) — treat as secrets, never paste
values into chat, commits, or this file.}}

---

## Integrations

{{INTEGRATIONS: every service, one line each, tagged WIRED or NOT WIRED with
one clause of evidence. NOT WIRED items must say "no code, no env vars,
nothing scaffolded" so they're never assumed built.}}

---

## Security / RLS

{{SECURITY: for Supabase — RLS status per table, the policy pattern, and the
rule for new tables. For other backends — auth model, authorization pattern,
and the rule new endpoints must follow. CONFIRMED-date anything verified.}}

---

## Behavioural rules

- Do not refactor, rename, or clean up code outside the current task scope.
- Ask before any schema migration that alters or drops existing columns.
- Do not add speculative features, validation, or guardrails not explicitly
  requested; do not start building anything from planning docs unless asked.
- Always give a filename before any SQL block the user will run manually
  (e.g. "Run this as `006_xyz.sql`").
- Secrets stay in {{SECRETS_LOCATIONS}} only. Never log, print, or commit
  values.
- When a UI/design detail is unclear or docs conflict with live code, trust
  the live code and flag the discrepancy.
- For UI changes, verify in the actual running app (dev server + browser)
  before reporting done.
- {{PROJECT_SPECIFIC_RULES: anything learned the hard way in this project.}}
