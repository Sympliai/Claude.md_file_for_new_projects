---
description: Turn the approved spec and architecture into small, independently testable phase files, each with a ready-to-run /goal. Planning only; no implementation.
---

Plan the phases for this project. Extra context: $ARGUMENTS

Read `docs/PRODUCT-SPEC.md`, `docs/USER-FLOWS.md`,
`docs/ACCEPTANCE-CRITERIA.md`, `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`
and `CLAUDE.md`. Do not write application code.

## Rules for good phases
- Each phase has ONE measurable end state and is independently testable.
- Order: foundation → auth/data layer → one complete vertical slice → feature
  batches (one bounded feature set each) → hardening → release readiness.
  Build one end-to-end journey before breadth.
- Every phase references acceptance-criteria IDs from ACCEPTANCE-CRITERIA.md.
  If a feature has no criterion, add one (and tell me) before planning it.
- Size a phase to finish within roughly 20–40 turns of agent work. Split if
  larger.
- Dependencies between phases must be explicit.

## Output
1. Create `docs/phases/PHASE-NN-<slug>.md` for each phase from
   `docs/phases/PHASE-TEMPLATE.md` (copy from
   `~/.claude/templates/build/docs/phases/` if missing), plus
   `CHECKPOINT-TEMPLATE.md`.
2. In each phase file, fill every section including Reviewers (choose from
   `workflow-tester`, `visual-reviewer`, `security-reviewer`,
   `accessibility-reviewer`, `content-reviewer`, `phase-auditor`; add
   security for anything touching auth/data/storage, content for guidance
   copy) and a **Turn / stop limit**.
3. Add a `## Ready-to-run /goal` section to each phase containing a bounded
   condition (under 4,000 characters) that: names this phase file; states the
   measurable end state; lists the exact commands that must exit 0 and the
   flows that must pass, with results shown in the transcript (the evaluator
   can only read what Claude prints); requires reviewer findings to be fixed
   or documented; forbids weakening tests, unrelated changes, exposing
   secrets and touching production data; requires CHECKPOINT-NN.md committed;
   and ends with `or stop after N turns and report what remains`.
4. Show me a one-table summary: phase, goal, depends on, reviewers, turn
   limit. Do not start implementing. Ask me to approve the plan, then stop.
Commit approved plans as `docs: add phase plan`.
