# Claude Code Setup v2 — Global Memory + Project Template + Phased Build Kit

Two layers in one repo:

1. **Base layer** (v1): global rules, enforced permissions, a self-filling
   project `CLAUDE.md`, `/bootstrap`, `/retrofit`, `/checkpoint`.
2. **Build layer** (new): idea → approved spec → approved stack → phased
   plan → unattended phase runs with independent reviewer agents, evidence,
   and a human gate between phases. Works for web, mobile or both.

## Repo layout → where it installs
```
global-CLAUDE.md        → ~/.claude/CLAUDE.md            (rename)
settings.json           → ~/.claude/settings.json        (merge if one exists)
CLAUDE.md               → ~/.claude/templates/CLAUDE.md  (project template)
commands/*.md           → ~/.claude/commands/
agents/*.md             → ~/.claude/agents/              (generic reviewers)
build-template/         → ~/.claude/templates/build/     (docs skeleton, build rule)
GOAL-GUIDE.md           (reference; keep in repo)
new-project-guide.md    (plain-English walkthrough; keep in repo)
```

## Install (once per machine)
```bash
mkdir -p ~/.claude/commands ~/.claude/agents ~/.claude/templates/build
cp global-CLAUDE.md ~/.claude/CLAUDE.md
cp settings.json    ~/.claude/settings.json       # merge permissions if you already have one
cp CLAUDE.md        ~/.claude/templates/CLAUDE.md
cp commands/*.md    ~/.claude/commands/
cp agents/*.md      ~/.claude/agents/
cp -R build-template/. ~/.claude/templates/build/
```
Verify after installing (start a new session first):
- Type `/`: `/start`, `/discover` and the other commands should be listed.
- Ask Claude: "List the subagents you can use." Six reviewers should appear.
- Open `~/.claude/settings.json` and confirm the allow and deny rules are there.
- Terminal only: `/context`, `/permissions` and `/agents` also work. In the
  desktop app, commands that open a terminal panel (such as `/permissions`)
  reply "isn't available in this environment".
- Terminal only, optional: `/doctor prompt-audit` after changes to catch
  contradictions between instruction files.

## The pipeline for a new product
Simplest: put your material in `reference/`, run `/start <idea>`. It works out
where the project is and runs the stages below in order, asking for approval at
each, and finishes by printing the exact line to type for the next phase. Safe
to re-run in a new session. The individual commands remain available:

| Step | Command | You do | Output |
|---|---|---|---|
| 1 | `/discover <idea>` | Answer short questions, approve the draft | `docs/PRODUCT-SPEC.md`, `USER-FLOWS.md`, `ACCEPTANCE-CRITERIA.md`, `RISKS.md` |
| 2 | `/setup-build` | Approve stack + tooling proposal | `ARCHITECTURE.md`, `DECISIONS.md`, `.claude/rules/build-workflow.md`, `CLAUDE.md` filled, verification tools proven |
| 3 | `/plan-phases` | Approve the phase table | `docs/phases/PHASE-NN-*.md`, each with a Ready-to-run `/goal` |
| 4 | `/goal …` (auto mode) or `/run-phase NN` | Walk away | code + `CHECKPOINT-NN.md` + `artifacts/phase-NN/` |
| 5 | Review the checkpoint | Approve next phase | repeat 4 |

Existing project with an old CLAUDE.md: `/retrofit`. Quick save point any
time: `/checkpoint`. Missing a specialist reviewer: `/new-agent <what for>`.

## Reviewer agents (generic, user-level)
| Agent | Tools | Purpose |
|---|---|---|
| workflow-tester | Read, Grep, Glob, Bash (no Edit/Write) | Runs user flows in browser/emulator; defect report |
| visual-reviewer | Read, Grep, Glob | Screenshot review: layout, contrast, states, safe areas |
| security-reviewer | Read, Grep, Glob | Auth, data access, RLS, secrets, storage, privacy |
| accessibility-reviewer | Read, Grep, Glob | WCAG 2.2 AA / platform a11y |
| content-reviewer | Read, Grep, Glob (haiku) | Domain-copy claims; rules in `docs/CONTENT-REVIEW.md` |
| phase-auditor | Read, Grep, Glob, Bash (no Edit/Write) | Adversarial check of the checkpoint against the diff |

Reviewers run once per phase after implementation, never per turn.
Project-specific agents go in `.claude/agents/`.

## Secrets
- Values live only in `.env.local` (gitignored) or the host's environment
  settings. Claude never asks for or accepts keys in chat; it names the
  variable and where it goes.
- `settings.json` denies Claude's file tools from reading `.env*`
  (except `.env.example`) and any `PROJECT KEYS/` or `Project Keys/` folder.
  This reduces exposure; it does not stop a Bash `cat`, so don't keep key
  files in repos at all. Test: ask Claude to read a file in such a folder and
  confirm it is refused.
- Retiring an old keys folder: store keys in a password manager or a folder
  outside your projects, then delete the in-repo folder.
- One-off history check per project: `git log --all --oneline -- "PROJECT KEYS"`.
  Any output means a key was committed once and should be rotated.

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
- **Evidence over assertion.** Checkpoints cite observed results; unrun
  checks are marked `NOT RUN`. Screenshots support executable flows, they do
  not replace them.
- **Unattended is bounded.** Auto mode + deny rules + turn limit + git
  checkpoints + a human gate at the end of each phase.
- **Web and mobile both supported.** `/setup-build` picks Playwright/Chrome
  (web) or simulator + Maestro (mobile) per project and records it in
  `CLAUDE.md` → Verification tooling.

## Keeping machines in sync
`git pull`, then repeat the copy lines above. Bootstrapped projects keep
their files; `/retrofit` brings one up to date.
