---
description: Turn the approved spec and architecture — or the findings chosen from an audit — into small, independently testable phase files, each with a ready-to-run /goal. Planning only; no implementation.
---

Plan the phases for this project. Extra context: $ARGUMENTS

Read `CLAUDE.md` and whichever of these exist: `docs/PRODUCT-SPEC.md`,
`docs/USER-FLOWS.md`, `docs/ACCEPTANCE-CRITERIA.md`, `docs/ARCHITECTURE.md`,
`docs/DECISIONS.md`, the latest `docs/AUDIT-*.md` and `docs/BACKLOG.md`. Do
not write application code.

## What is being planned
- **New product**: the first-release features in the spec.
- **Adopted project or later work**: the audit findings and backlog items I
  chose to plan, plus anything new I ask for. For each one, first write an
  acceptance criterion in `docs/ACCEPTANCE-CRITERIA.md` that says how we will
  know it is fixed (quote the finding's ID, e.g. "AC-014 (A-003) …"), and
  show me the new criteria with the phase table. Group related findings into
  one phase; put critical and high security findings in the first phase.
  When a phase is approved, set its backlog lines to `PLANNED (PHASE-NN)`.

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
   `CHECKPOINT-TEMPLATE.md`. Number on from the highest existing phase.
2. In each phase file, fill every section including Progress (one line per
   Included item), Reviewers (choose from `workflow-tester`,
   `visual-reviewer`, `ux-reviewer`, `security-reviewer`,
   `accessibility-reviewer`, `content-reviewer`, `phase-auditor`; add
   security for anything touching auth/data/storage, ux for any new or
   changed user flow, content for guidance copy; `phase-auditor` always,
   last) and a **Turn / stop limit**.
3. Add a `## Ready-to-run /goal` section to each phase containing a bounded
   condition (under 4,000 characters) that: names this phase file and its
   branch `phase-NN-<slug>`; states the measurable end state; lists the exact
   commands that must exit 0 and the flows that must pass, with results shown
   in the transcript (the evaluator can only read what Claude prints);
   requires reviewer findings to be fixed or documented; forbids weakening
   tests, unrelated changes, exposing secrets, touching production data and
   merging or pushing to `main`; requires CHECKPOINT-NN.md committed, Status
   set to AWAITING REVIEW and the phase branch pushed; and ends with
   `or stop after N turns and report what remains`.
4. Show me a one-table summary: phase, goal, depends on, reviewers, turn
   limit. Do not start implementing. Ask me to approve the plan, then stop.
Commit approved plans as `docs: add phase plan`.
