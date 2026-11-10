# Phased build workflow (loaded every session)

## Sources of truth
- `docs/PRODUCT-SPEC.md`, `docs/USER-FLOWS.md`, `docs/ACCEPTANCE-CRITERIA.md`
  define WHAT. `docs/ARCHITECTURE.md` defines HOW. `docs/DECISIONS.md` records
  settled choices — do not reopen them without a new entry.
- Adopted project (started from `/audit`, so there is no product spec):
  `CLAUDE.md` and the live code stand in for the spec and architecture docs.
  Do not invent a spec to fill the gap.
- The current phase file `docs/phases/PHASE-NN-*.md` is the ONLY scope for
  implementation work. Anything outside it is out of scope, however small.
- Noticed a problem outside the phase? Follow the global rule: a small fix in
  a file the phase is already editing may be made and listed under "Fixed in
  passing" in the checkpoint; everything else gets a line in
  `docs/BACKLOG.md`. Neither is a reason to widen the phase.
- Scope creep, a new dependency, or an external service needed mid-phase →
  stop, add a `DECISIONS.md` entry marked PROPOSED, and ask. Never add silently.

## Branches
- Each phase is built on its own branch, `phase-NN-<slug>`, created from an
  up-to-date `main`. Push that branch freely; a host such as Vercel builds a
  preview from it.
- `main` changes only at the phase gate, after the user approves. Never merge
  or push to `main` during a phase, including under `/goal`. In this project a
  push to `main` always asks the user first (`.claude/settings.json`).

## Phase procedure (same whether run by `/run-phase` or under `/goal`)
1. Read the phase file, the `ACCEPTANCE-CRITERIA.md` items it references, and
   `ARCHITECTURE.md`. Confirm `git status` is clean. Then:
   - Status APPROVED → `git switch main`, `git pull`,
     `git switch -c phase-NN-<slug>`, set Status to IN PROGRESS, commit
     `docs(phase-NN): start`.
   - Status IN PROGRESS → `git switch phase-NN-<slug>` and continue from the
     first unticked item under Progress. Do not redo ticked work.
2. Implement only what the phase lists. Commit at each working increment
   (`feat(phase-NN): ...`) and tick its line under Progress in the same commit.
3. Run every command in `CLAUDE.md` → Commands: typecheck, lint, test, build.
   Fix failures. Never weaken, skip or delete a test to get green.
4. Start the app and execute each user flow the phase names, using the
   verification tooling recorded in `CLAUDE.md` → Verification tooling
   (Playwright/Chrome for web, Maestro + emulator/simulator for mobile).
   Where a flow file exists (`e2e/` or `.maestro/`), run it; where it
   doesn't, write one — flows are assets, not throwaway.
5. Capture screenshots of the phase's required screens and states into
   `artifacts/phase-NN/` at the sizes `CLAUDE.md` specifies. Inspect console
   / device logs for errors. Web: if an accessibility scanner (axe) is
   recorded in Verification tooling, run it on each required screen and save
   the results to `artifacts/phase-NN/axe/`.
6. Save the evidence reviewers cannot produce themselves:
   `git diff main...HEAD > artifacts/phase-NN/changes.diff` and the dependency
   audit (`npm audit --omit=dev`, or the stack's equivalent) to
   `artifacts/phase-NN/dependency-audit.txt`. Then invoke the reviewers
   listed in the phase file (`workflow-tester`, `visual-reviewer`,
   `ux-reviewer`, `security-reviewer`, `accessibility-reviewer`,
   `content-reviewer`, `phase-auditor`), giving each its scope: the phase
   file path and `artifacts/phase-NN/`. Run each ONCE per phase, after
   implementation is otherwise complete — not every turn. Reviewers report;
   they do not fix.
7. Fix valid findings; record rejected findings with a reason. Re-run the
   checks affected by the fixes (steps 3–5 as relevant).
8. Docs housekeeping: if `CLAUDE.md` is over ~150 lines, do the automatic
   verbatim split per the global rules in its own `docs:` commit now, before
   the checkpoint commit.
   Then write `docs/phases/CHECKPOINT-NN.md` from the template. Every claim in it
   must cite an observed result (command + exit code, test counts, file path).
   List anything fixed in passing and every backlog entry added.
9. Set the phase Status to AWAITING REVIEW. Commit the checkpoint and
   artifacts: `docs(phase-NN): checkpoint report`. Push the phase branch:
   `git push -u origin phase-NN-<slug>`. Do not push `main`.
10. STOP. Report the checkpoint summary, the branch name and the preview URL
    if the host built one, and wait. Do not start the next phase unless the
    user approved it explicitly or listed it in an approved chain.

## Evidence rules
- Never state that a test, build, screenshot review or device flow passed
  unless it was run in this session and the result was observed.
- A screenshot is supporting evidence, not proof. Pair it with an executable
  assertion (test, flow step) wherever practical.
- If tooling is unavailable (no emulator, no browser tool), say so, mark the
  check `NOT RUN — <reason>` in the checkpoint, and do not substitute a guess.

## Reviewers
- Reviewer agents live in `~/.claude/agents/` (generic) and
  `.claude/agents/` (project-specific). Reviewers default to `model: sonnet`.
- If a phase needs a review the existing agents don't cover (performance,
  data migration, i18n, payments, offline sync, a domain expert), propose a
  new agent — name, purpose, tools, model — and ask before creating it under
  `.claude/agents/`. Reviewers get no Edit/Write tools.

## Phase gate
- A phase is done only when its Definition of done is met and the checkpoint
  is committed. The gate is a human review; `/goal` bounds one phase and must
  stop at its gate.
- When the user approves the phase: `git switch main`, `git pull`,
  `git merge --no-ff phase-NN-<slug>`, set the phase Status to
  `DONE (<date>)`, commit `docs(phase-NN): mark done`, then
  `git push origin main`. Where `main` auto-deploys, that push is the release:
  say so before pushing.
- If the user asks for changes instead: stay on the phase branch, set Status
  back to IN PROGRESS, fix, re-run the affected checks, update the
  checkpoint, and return to the gate.
