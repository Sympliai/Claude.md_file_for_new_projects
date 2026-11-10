---
description: Run or resume one approved phase end to end following the build workflow (interactive alternative to /goal). Works on the phase branch and stops at the phase gate.
argument-hint: "[phase number, e.g. 03]"
---

Run phase: $ARGUMENTS   (e.g. `03` or the phase file name)

1. Locate `docs/phases/PHASE-$ARGUMENTS*.md` and read its Status:
   - APPROVED → start it.
   - IN PROGRESS → resume it: switch to its branch and continue from the
     first unticked Progress line. Do not redo ticked work.
   - AWAITING REVIEW → do not rebuild. Summarise the checkpoint and ask me
     for the gate decision.
   - PLANNED → stop and ask me to approve it.
   - DONE → say so and name the next phase.
2. State the plan in ≤10 lines (included work, flows to test, reviewers,
   checks, branch name) and proceed only if I have approved this phase. If
   this is an unattended `/goal` run, the approval already exists; proceed.
3. Follow `.claude/rules/build-workflow.md` steps 1–10 exactly. All work
   happens on the phase branch; `main` is not touched.
4. Run each reviewer once, after implementation. Fix valid findings, record
   rejected ones with reasons, re-run affected checks.
5. End by running `phase-auditor`. If it says NOT READY, fix and re-audit
   once; if still not ready, stop and report.
6. Write and commit CHECKPOINT-NN.md, set Status to AWAITING REVIEW and push
   the phase branch. Stop at the gate and report: what changed, checks run
   with observed outcomes, flows tested, screenshots, findings and fixes,
   anything fixed in passing, backlog entries added, unresolved risks,
   whether acceptance criteria are met, and the branch and preview URL to
   review. Never claim anything passed that you did not observe.
7. When I approve the phase, follow "Phase gate" in the build workflow: merge
   the branch to `main`, mark the phase DONE, push.
