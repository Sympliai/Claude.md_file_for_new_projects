# Phased build workflow (loaded every session)

## Sources of truth
- `docs/PRODUCT-SPEC.md`, `docs/USER-FLOWS.md`, `docs/ACCEPTANCE-CRITERIA.md`
  define WHAT. `docs/ARCHITECTURE.md` defines HOW. `docs/DECISIONS.md` records
  settled choices — do not reopen them without a new entry.
- The current phase file `docs/phases/PHASE-NN-*.md` is the ONLY scope for
  implementation work. Anything outside it is out of scope, however small.
- Scope creep, a new dependency, or an external service needed mid-phase →
  stop, add a `DECISIONS.md` entry marked PROPOSED, and ask. Never add silently.

## Phase procedure (same whether run by `/run-phase` or under `/goal`)
1. Read the phase file, `ACCEPTANCE-CRITERIA.md` items it references, and
   `ARCHITECTURE.md`. Confirm `git status` is clean before starting.
2. Implement only what the phase lists. Keep commits small; commit at each
   working increment (`feat(phase-NN): ...`).
3. Run every command in `CLAUDE.md` → Commands: typecheck, lint, test, build.
   Fix failures. Never weaken, skip or delete a test to get green.
4. Start the app and execute each user flow the phase names, using the
   verification tooling recorded in `CLAUDE.md` → Verification tooling
   (Playwright/Chrome for web, Maestro + emulator/simulator for mobile).
   Where a flow file exists (`e2e/` or `.maestro/`), run it; where it
   doesn't, write one — flows are assets, not throwaway.
5. Capture screenshots of the phase's required screens and states into
   `artifacts/phase-NN/` at the sizes `CLAUDE.md` specifies. Inspect console
   / device logs for errors.
6. Invoke reviewers listed in the phase file (`workflow-tester`,
   `visual-reviewer`, `security-reviewer`, `accessibility-reviewer`,
   `content-reviewer`, `phase-auditor`). Run each ONCE per phase, after
   implementation is otherwise complete — not every turn. Reviewers report;
   they do not fix.
7. Fix valid findings; record rejected findings with a reason. Re-run the
   checks affected by the fixes (steps 3–5 as relevant).
8. Docs housekeeping: if `CLAUDE.md` is over ~150 lines, do the automatic
   verbatim split per the global rules in its own `docs:` commit now, before
   the checkpoint commit.
   Then write `docs/phases/CHECKPOINT-NN.md` from the template. Every claim in it
   must cite an observed result (command + exit code, test counts, file path).
9. Commit the checkpoint and artifacts: `docs(phase-NN): checkpoint report`.
   Push.
10. STOP. Report the checkpoint summary and wait. Do not start the next phase
    unless the user approved it explicitly or listed it in an approved chain.

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
