# Running a phase unattended with /goal

`/goal` is built into Claude Code (no skill to install). It sets a completion
condition; after every turn a small fast model (Haiku by default) reads the
transcript and says met / not yet / impossible. Not yet → Claude takes
another turn. It only judges what Claude has *printed*, so the condition must
make Claude run the checks and show results.

## What "fully unattended" actually requires
| Need | How |
|---|---|
| Next turn starts automatically | `/goal <condition>` |
| Tool calls don't prompt you | Run the session in Auto mode (desktop: the mode selector next to the send button; terminal: Shift+Tab or `--permission-mode auto`). `/goal` does NOT change permission mode. In Manual mode it stops and asks. |
| Hard guardrails regardless of mode | `~/.claude/settings.json` deny rules (force-push, `rm -rf`, `.env` reads, hard reset), enforced by Claude Code in every mode. The guard hook blocks any other secret-file read and any commit containing a key-shaped string. The project's `ask` rule stops a push to `main` for your click. |
| Bounded run | A turn clause inside the condition: `or stop after 25 turns`. |
| Recoverable | Clean `git status` first. The phase runs on its own `phase-NN-<slug>` branch, so `main` is untouched until you approve the gate. Commits at each increment tick the phase's Progress list; checkpoint report at the end. |
| Subagents finish before judging | If a subagent/background command is running, evaluation is skipped until it ends. Normal. |

## Before you start a run (2-minute checklist)
1. `git status` clean on `main`. The run creates (or resumes) the
   `phase-NN-<slug>` branch itself.
2. Phase file is `APPROVED`, has a Ready-to-run /goal, and a turn limit.
3. Verification tooling proven: dev server, emulator/browser, one trivial
   flow, all passing.
4. Usage headroom: reviewers and screenshots multiply token use. Don't
   assume unlimited usage.
5. Nothing in the phase touches production data, billing or real
   credentials. Those phases are interactive only.

## Run it
Desktop app: Code tab → choose the project folder → set the mode selector
(next to the send button) to Auto → type the `/goal` line.

Auto mode needs a supported model (Sonnet 4.6+, Opus 4.6+, Haiku 5.5 or a
Fable model) and must not be switched off by an organisation admin. It
appears in the selector when available, in the desktop app and the terminal
alike. If it's missing, check the model dropdown first. If it's still missing,
use **Accept edits**: the allow list in `settings.json` already approves
routine git/npm/test commands, so the run only pauses on commands not on that
list. `/run-phase` also works.

Local runs use your computer: if the Mac sleeps, work pauses, so keep it awake
for long runs. Cloud sessions keep going with the app closed but cannot use
your local simulators. The desktop app is interactive only; headless
`claude -p` runs are terminal-only.

Terminal version:

```
claude                      # interactive session in the project
# switch to auto mode, then:
/goal <paste the phase file's "Ready-to-run /goal" text>
```
Check on it: `/goal` (turns, token spend, last evaluator reason).
Stop it: `/goal clear`. Headless: `claude -p "/goal …"` (add
`--output-format stream-json --verbose` or it prints nothing until done).

## Goal shape that works
One phase, one measurable end state, named commands that must exit 0 shown
in the transcript, flows that must pass, reviewers run once and findings
fixed or documented, constraints (no weakened tests, no unrelated changes,
no secrets, no production data), `CHECKPOINT-NN.md` committed, and
`or stop after N turns and report what remains`.

## When NOT to use /goal
Discovery, architecture choices, anything needing your judgement; production
migrations; billing/payroll/sensitive-data changes; visual quality that no
check can assert; vague "make it good" work.

## Known failure modes
- Weak condition → premature "done". Fix: name the commands and flows.
- Fixes one test, breaks another, loops. The turn limit and the
  `phase-auditor` are your brakes.
- Credit exhaustion, auth failure, context overflow or unavailable model
  clear the goal. Re-set it after fixing the cause; progress is in git, and
  the phase file's Status and Progress ticks tell the next run where to
  resume.
- The run stops on a permission prompt to push `main`. That prompt is the
  gate working: a phase run should never push `main`. Decline it, and look
  at why the run tried.
- Reviewers are only as read-only as their tools. `security-reviewer`,
  `visual-reviewer`, `ux-reviewer`, `accessibility-reviewer` and
  `content-reviewer` have no Bash. `workflow-tester` and `phase-auditor`
  need Bash; the guard hook's read-only mode blocks the commands that change
  files or git state (writing evidence under `artifacts/` is allowed). It is
  a guard rail, not a sandbox, so still review their output, not just their
  verdict.
