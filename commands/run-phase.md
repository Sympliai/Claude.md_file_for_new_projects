---
description: Run one approved phase end to end following the build workflow (interactive alternative to /goal). Stops at the phase gate.
---

Run phase: $ARGUMENTS   (e.g. `03` or the phase file name)

1. Locate `docs/phases/PHASE-$ARGUMENTS*.md`. If its Status is not APPROVED,
   stop and ask me to approve it.
2. State the plan in ≤10 lines (included work, flows to test, reviewers,
   checks) and proceed only if I have approved this phase. If this is an
   unattended `/goal` run, the approval already exists; proceed.
3. Follow `.claude/rules/build-workflow.md` steps 1–10 exactly.
4. Run each reviewer once, after implementation. Fix valid findings, record
   rejected ones with reasons, re-run affected checks.
5. End by running `phase-auditor`. If it says NOT READY, fix and re-audit
   once; if still not ready, stop and report.
6. Write and commit CHECKPOINT-NN.md. Stop at the gate and report: what
   changed, checks run with observed outcomes, flows tested, screenshots,
   findings and fixes, unresolved risks, and whether acceptance criteria are
   met. Never claim anything passed that you did not observe.
