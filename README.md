# Claude Code Setup v3 — Global Rules, Guard Hook, Project Template, Phased Build Kit

Three layers in one repo:

1. **Base layer**: global rules, enforced permissions, a guard hook for
   secrets, a self-filling project `CLAUDE.md`, `/bootstrap`, `/retrofit`,
   `/checkpoint`.
2. **Build layer**: idea → approved spec → approved stack → phased plan →
   unattended phase runs on their own branch, with independent reviewer
   agents, evidence, and a human gate before anything reaches `main`. Works
   for web, mobile or both.
3. **Adopt layer** (new in v3): an existing codebase → documented from live
   code → audited for security, UX, accessibility and workflow problems →
   a ranked report with a recommended fix for each → you choose what gets
   fixed. A backlog catches whatever Claude notices later.

## Repo layout → where it installs
```
global-CLAUDE.md        → ~/.claude/CLAUDE.md
settings.json           → merged into ~/.claude/settings.json
hooks/kit-guard.py      → ~/.claude/hooks/kit/
commands/*.md           → ~/.claude/commands/
agents/*.md             → ~/.claude/agents/              (generic reviewers)
templates/CLAUDE.md     → ~/.claude/templates/CLAUDE.md  (project template)
build-template/         → ~/.claude/templates/build/     (docs skeleton, build rule,
                                                          audit template, project settings)
CLAUDE.md               (instructions for working on this kit; not installed)
install.sh, scripts/, tests/, VERSION   (installer and tests; not installed)
GOAL-GUIDE.md           (reference; keep in repo)
new-project-guide.md    (plain-English walkthrough; keep in repo)
```

## Install or update (once per machine, and after every `git pull`)
```bash
bash install.sh
```
It copies the files above into place, **merges** the kit's permission rules
and hook into your existing `~/.claude/settings.json` (nothing you already
have is removed), saves the previous version of any file it replaces under
`~/.claude/kit-backups/`, and records the installed version. It needs
`python3`, which the guard hook uses too.

To see whether the installed copy matches this folder, without changing
anything:
```bash
bash install.sh --check
```

Verify after installing (start a new session first):
- Type `/`: `/start`, `/audit`, `/discover` and the other commands should be listed.
- Ask Claude: "List the subagents you can use." Seven reviewers should appear.
- In a scratch folder containing a file named `.env.local`, ask Claude to
  read it. It should be refused with a "Blocked by kit-guard" message.
- Terminal only: `/context`, `/permissions`, `/hooks` and `/agents` also work.
  In the desktop app, commands that open a terminal panel (such as
  `/permissions`) reply "isn't available in this environment".
- Terminal only, optional: `/doctor prompt-audit` after changes to catch
  contradictions between instruction files.

## The pipeline for a new product
Simplest: put your material in `reference/`, run `/start <idea>`. It works out
where the project is and runs the stages below in order, asking for approval at
each, and finishes by printing the exact line to type for the next phase. Safe
to re-run in a new session. The individual commands remain available:

| Step | Command | You do | Output |
|---|---|---|---|
| 1 | `/discover <idea>` | Answer short questions, approve the draft | `docs/PRODUCT-SPEC.md`, `USER-FLOWS.md`, `ACCEPTANCE-CRITERIA.md`, `RISKS.md`, `BACKLOG.md` |
| 2 | `/setup-build` | Approve stack, tooling and design system | `ARCHITECTURE.md`, `DECISIONS.md`, `.claude/rules/build-workflow.md`, `.claude/settings.json`, `CLAUDE.md` filled, verification tools proven |
| 3 | `/plan-phases` | Approve the phase table | `docs/phases/PHASE-NN-*.md`, each with a Ready-to-run `/goal` |
| 4 | `/goal …` (auto mode) or `/run-phase NN` | Walk away | code on branch `phase-NN-<slug>` + `CHECKPOINT-NN.md` + `artifacts/phase-NN/` |
| 5 | Review the checkpoint and the preview | Approve the phase | branch merged to `main`, phase marked DONE; repeat 4 |

## The pipeline for an existing project
Open the project folder and run `/start`. It sees application code with no
spec and takes the adopt route:

| Step | Command | You do | Output |
|---|---|---|---|
| 1 | `/bootstrap` (or `/retrofit` for an old `CLAUDE.md`) | Nothing | `CLAUDE.md` filled from live code, baseline check results, `docs/BACKLOG.md` |
| 2 | `/audit` | Read the summary; choose what to fix now, plan, or leave | `docs/AUDIT-<date>.md`, findings added to the backlog, evidence in `artifacts/audit-<date>/` |
| 3 | `/setup-build` then `/plan-phases` (only if you chose fixes to plan) | Approve tooling and the phase table | the same phase files as a new product, built from the findings you chose |
| 4 | As steps 4–5 above | | |

The audit never changes product code. Run `/audit` again whenever you want a
fresh health check.

Quick save point any time: `/checkpoint`. Missing a specialist reviewer:
`/new-agent <what for>`.

## Problems Claude notices along the way
The global rules tell Claude what to do when it spots a problem the task did
not ask about:
- a few-line defect in a file it is already editing → fix it and report it in
  one line;
- anything else → one line in `docs/BACKLOG.md` with area, severity, location
  and a recommended fix;
- a critical or high security problem → raised at the top of the reply, never
  only logged.

Checkpoints list what was fixed in passing and what was added to the backlog.

## Reviewer agents (generic, user-level)
| Agent | Tools | Purpose |
|---|---|---|
| workflow-tester | Read, Grep, Glob, Bash (read-only guard) | Runs user flows in browser/emulator; defect report |
| visual-reviewer | Read, Grep, Glob | Screenshot review: layout, contrast, states, safe areas |
| ux-reviewer | Read, Grep, Glob | Ease of use: next step, effort, feedback, errors, consistency |
| security-reviewer | Read, Grep, Glob | Auth, data access, RLS, secrets, storage, dependencies, privacy |
| accessibility-reviewer | Read, Grep, Glob | WCAG 2.2 AA / platform a11y; reads axe scan results when present |
| content-reviewer | Read, Grep, Glob (haiku) | Domain-copy claims; rules in `docs/CONTENT-REVIEW.md` |
| phase-auditor | Read, Grep, Glob, Bash (read-only guard) | Adversarial check of the checkpoint against the diff |

Reviewers run once per phase after implementation, never per turn, and once
each in an audit. Each takes a scope from the session that calls it: a phase
or a whole-project audit. Project-specific agents go in `.claude/agents/`.

## Branches and the phase gate
- Each phase is built on `phase-NN-<slug>` and pushed there. A host such as
  Vercel builds a preview from the branch for you to review.
- `main` moves only when you approve the phase. `/setup-build` adds an `ask`
  rule to the project's `.claude/settings.json`, so a push to `main` in a
  phased project stops for your click, including in auto mode.
- Phase files carry a Status (PLANNED → APPROVED → IN PROGRESS → AWAITING
  REVIEW → DONE) and a Progress checklist ticked commit by commit. `/start`
  and `/run-phase NN` use them to resume an interrupted phase.

## Secrets
- Values live only in `.env.local` (gitignored) or the host's environment
  settings. Claude never asks for or accepts keys in chat; it names the
  variable and where it goes.
- Two layers keep secret files out of the session. `settings.json` denies
  Claude's file tools from reading the common `.env*` names (except
  `.env.example`) and any `PROJECT KEYS/` or `Project Keys/` folder. The
  guard hook (`hooks/kit-guard.py`) then blocks **any** `.env*` file other
  than `.env.example` for Read, Edit, Write, Grep and Bash commands that name
  one (`cat .env`, `source .env`, `git add .env.local`, a script that opens
  it).
- Before every `git commit`, the hook scans what is being committed for
  key-shaped strings (AWS, GitHub, Stripe, OpenAI/Anthropic, Google, Slack,
  SendGrid and Supabase service-role keys, private-key blocks) and for secret
  files. A hit blocks the commit and reports the file and line, never the
  value. A confirmed false positive can be let through with a
  `secret-scan:allow` comment on that line.
- These are guard rails, not a sandbox. They catch the commands Claude
  normally writes; an unusual command can still get round them (a script
  that builds the file name at run time, for instance). For OS-level
  blocking as well, turn on the Claude Code sandbox (`/sandbox` in the
  terminal, or `"sandbox": {"enabled": true}` with
  `sandbox.filesystem.denyRead` in `~/.claude/settings.json`). Best of all,
  don't keep key files in repos.
- Retiring an old keys folder: store keys in a password manager or a folder
  outside your projects, then delete the in-repo folder.
- One-off history check per project:
  `python3 ~/.claude/hooks/kit/kit-guard.py scan-repo`. It lists key-shaped
  strings in tracked files and secret files that were ever committed. Any
  output means a key should be rotated.

## Automatic CLAUDE.md splitting
When a `CLAUDE.md` passes ~150 lines Claude moves one whole reference section
verbatim into `.claude/rules/<name>.md` at the next checkpoint, in its own
`docs:` commit, and reports it in one line. Commands, Project-specific rules,
the Session-start checklist and Source of truth never move. Existing rules
folders are never reorganised. It never pauses a run to ask.

## Design decisions worth knowing
- **Spec is files, not prompt text.** The workflow lives in the repo so every
  project starts identical; the only prompt you type is the idea.
- **Phase file = scope; `/goal` = engine.** `/goal` is a completion loop run
  in a session; it is never written into the spec. See `GOAL-GUIDE.md`.
- **Evidence over assertion.** Checkpoints and audits cite observed results;
  unrun checks are marked `NOT RUN`. Screenshots support executable flows,
  they do not replace them.
- **Recommend, then fix.** Audits and the backlog recommend; the user chooses.
  The only unprompted fixes are few-line defects in a file already being
  edited, and each one is reported.
- **Unattended is bounded.** Auto mode + deny rules + the guard hook + turn
  limit + a phase branch + a human gate before `main`.
- **Enforce what matters, instruct the rest.** Rules Claude must not break
  (secret files, committing keys, reviewers changing code, pushing `main` in
  a phased project) are backed by settings or the hook, not only by prose.
- **Web and mobile both supported.** `/setup-build` picks Playwright/Chrome
  (web) or simulator + Maestro (mobile) per project and records it in
  `CLAUDE.md` → Verification tooling.

## Working on the kit itself
`CLAUDE.md` at the repo root holds the rules for editing this kit. After any
change: `python3 tests/test_kit_guard.py`, then `bash install.sh` to put it
live. Bump `VERSION` when installed behaviour changes.

## Keeping machines in sync
`git pull`, then `bash install.sh`. Bootstrapped projects keep their files;
`/retrofit` brings an old `CLAUDE.md` up to date. A project set up before v3
keeps its old build rule until you ask Claude to "copy the current
build-workflow rule and project settings from `~/.claude/templates/build/`
into this project" (steps 2 and 3 of `/setup-build`).
