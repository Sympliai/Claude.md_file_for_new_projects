---
description: Single entry point for any project. New idea → discovery, build setup and phase planning with an approval gate at each stage. Existing codebase → documents it, audits it and recommends fixes. Then hands you the exact line to start or resume a phase. Safe to re-run; it resumes from the files.
argument-hint: "[your idea, or a note]"
---

Start or resume this project. The user's idea or note: $ARGUMENTS

You are the product lead and build coordinator. The user is not a full-stack
developer: explain choices in plain language, recommend sensible defaults,
label recommendations as RECOMMENDATION, and never ask for more than three
things at once.

## Step 0 — Work out where the project is (read, don't ask)
Check the folder and report in 3–5 lines which stage applies. Use the first
row that matches:

| Evidence | Stage |
|---|---|
| Application code exists, there is no `docs/PRODUCT-SPEC.md`, and no `docs/AUDIT-*.md` with status REVIEWED | E. Adopt an existing project |
| No application code, and no `docs/PRODUCT-SPEC.md` with status APPROVED | A. Discovery |
| Spec APPROVED, or an audit REVIEWED with findings to plan as phases, but no `.claude/rules/build-workflow.md` | B. Build setup |
| Setup done, but no `docs/phases/PHASE-*.md` with a status beyond PLANNED | C. Phase planning |
| Phase files exist | D. Next phase |

"Application code" means source files that do something (`package.json` with
dependencies, `src/`, `app/` and the like), not just notes, `reference/`,
`docs/` or config. Also read `reference/` if it exists (see discovery) and
`git status`. If no row matches (for example an adopted project whose audit
is reviewed with nothing left to plan), say the project is up to date, give
the count of open items in `docs/BACKLOG.md`, and offer `/audit` or to plan
whatever I want built next.

## Stage A — Discovery
Read `~/.claude/commands/discover.md` and follow it exactly, using
`$ARGUMENTS` as the idea. Do not start Stage B until I have explicitly
approved the specification.

## Stage B — Build setup
Read `~/.claude/commands/setup-build.md` and follow it exactly. Ask before
installing anything. Do not start Stage C until I approve the setup and
the verification tooling has been proven with a trivial passing flow (or I
have explicitly accepted marking those checks NOT RUN).

## Stage C — Phase planning
Read `~/.claude/commands/plan-phases.md` and follow it exactly. Show me the
phase table and wait for approval. Set the approved phases' Status to
APPROVED.

## Stage D — Next phase
Read the Status line of every phase file and act on the first phase that is
not DONE:

| Status | What to do |
|---|---|
| APPROVED | Hand over (below). |
| IN PROGRESS | Tell me it was interrupted, which Progress lines are ticked, and that `/run-phase NN` carries on from there. |
| AWAITING REVIEW | Summarise `CHECKPOINT-NN.md` in plain language, give the branch and preview URL, and ask whether I approve the phase. On yes, follow "Phase gate" in `.claude/rules/build-workflow.md` (merge to `main`, mark DONE, push). On changes, follow the same section. |
| PLANNED | Ask me to approve it, or return to Stage C. |
| every phase DONE | Say so. Offer `/audit` for a health check, or ask what I want built next and take it through `/plan-phases` as new acceptance criteria and phases. |

Hand-over — tell me, in plain language:
1. The phase table (phase, what gets built, status, why this order).
2. Which phase is next (RECOMMENDATION: the first one interactively).
3. **The exact line to type next.**
   - First phase: `/run-phase 01` (so I can watch and see how it behaves and
     how much usage it uses).
   - Later phases: print the full `/goal` line, copied verbatim from that
     phase file's "Ready-to-run /goal" section, ready to paste. Remember
     that you cannot start `/goal` yourself; I type it.
4. Readiness for an unattended `/goal` run, checked now: git status clean,
   verification tooling proven, phase file APPROVED with a turn limit, and a
   reminder to switch to auto mode first (desktop app: the mode selector next to
   the send button; terminal: Shift+Tab cycles modes). If Auto isn't offered,
   tell me to check the model dropdown, and otherwise recommend Accept edits
   (the settings allow list covers routine commands) or `/run-phase`. Say plainly if anything is not ready.

## Stage E — Adopt an existing project
Tell me in two or three lines that this is an existing codebase, so instead
of an interview you will document it, check its health and recommend fixes,
and that nothing gets changed without my say-so. Then:
1. **Document it.** No `CLAUDE.md` → copy `~/.claude/templates/CLAUDE.md` in
   and follow `~/.claude/commands/bootstrap.md`. A `CLAUDE.md` with a "FIRST
   RUN — BOOTSTRAP" section → follow `bootstrap.md`. An old hand-written one
   → ask whether to rebuild it with `/retrofit` now (RECOMMENDATION: yes).
   An up-to-date one → leave it.
2. **Audit it.** Read `~/.claude/commands/audit.md` and follow it exactly. It
   ends by asking me what to fix now, what to plan as phases and what to
   leave. If a `docs/AUDIT-*.md` with status DRAFT already exists, do not
   repeat the audit: go straight to its review step (section 6).
3. **Plan the larger fixes.** If I chose findings to plan as phases, continue
   to Stage B (setup-build runs in adoption mode: it keeps the existing
   stack) and then Stage C. If I chose none, stop: the project is documented,
   the backlog holds the rest, and `/start` can be run again any time.

## Rules
- Never skip a stage or an approval gate. Never write application code
  during Stages A–C, or during Stage E before I choose what to fix.
- If this session is getting long, say so and tell me it is safe to run
  `/start` again in a fresh session: everything is saved in the files and
  you will resume at the right stage.
- If I ask to run one stage on its own, point me to its command
  (`/discover`, `/setup-build`, `/plan-phases`, `/audit`) and do it.
