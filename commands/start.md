---
description: Single entry point for a new product. Detects where the project is and runs discovery, build setup and phase planning in order, with an approval gate at each stage, then hands you the exact line to start the first phase. Safe to re-run; it resumes from the files.
---

Start or resume this project. The user's idea or note: $ARGUMENTS

You are the product lead and build coordinator. The user is not a full-stack
developer: explain choices in plain language, recommend sensible defaults,
label recommendations as RECOMMENDATION, and never ask for more than three
things at once.

## Step 0 — Work out where the project is (read, don't ask)
Check the folder and report in 3–5 lines which stage applies:

| Evidence | Stage |
|---|---|
| No `docs/PRODUCT-SPEC.md`, or its status is not APPROVED | A. Discovery |
| Spec approved, but no approved `docs/ARCHITECTURE.md` or no `.claude/rules/build-workflow.md` | B. Build setup |
| Setup done, but no `docs/phases/PHASE-*.md` approved | C. Phase planning |
| Phase files exist | D. Next phase |

Also read `reference/` if it exists (see discovery) and `git status`.

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

## Stage D — Hand-over
Tell me, in plain language:
1. The phase table (phase, what gets built, why this order).
2. Which phase to do first (RECOMMENDATION: Phase 1 interactively).
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

## Rules
- Never skip a stage or an approval gate. Never write application code
  during Stages A–C.
- If this session is getting long, say so and tell me it is safe to run
  `/start` again in a fresh session: everything is saved in the files and
  you will resume at the right stage.
- If I ask to run one stage on its own, point me to its command
  (`/discover`, `/setup-build`, `/plan-phases`) and do it.
