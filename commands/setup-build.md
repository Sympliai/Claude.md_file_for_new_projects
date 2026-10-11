---
description: After the spec is approved — agree the stack, install the phased build workflow, verification tooling and reviewer agents, and fill CLAUDE.md. Asks before installing anything.
---

Set up the build workflow for this project. Extra context: $ARGUMENTS

## Preconditions
- `docs/PRODUCT-SPEC.md` must exist and be APPROVED. If not, stop and tell
  me to run `/discover`.
- Run `claude --version` and `git status`. Report both.

## Step 1 — Propose, don't change (wait for my approval)
Present, in chat:
1. **Stack recommendation** with trade-offs and why it fits the spec
   (web / mobile / both; framework; backend; auth; storage; hosting). Use my
   global defaults unless the spec argues otherwise. Mark it RECOMMENDATION.
2. **Verification tooling** for the platform:
   - Web: Playwright (committed e2e tests) and/or Claude Code's Chrome
     integration for interactive checks.
   - Mobile: simulator/emulator + Maestro flows (Maestro MCP optional).
   - If I'm using the Claude Code desktop app on a Mac and the product has an
     iOS version: the desktop app has a built-in iOS Simulator pane where
     Claude can run and test the app. Read the current docs page
     (https://code.claude.com/docs/en/desktop-ios-simulator) for prerequisites
     and limits before proposing it, and propose it as the route for
     interactive iOS checks. Still propose committed flow files (Maestro or
     equivalent) for repeatable regression tests, and cover Android
     separately (the pane is iOS only). Say plainly what each route can and
     cannot verify.
   - For each: prerequisites, what is already installed (check, don't
     assume), install steps, and cost/permission implications.
3. **Design reference**: ask whether I have a UI design export (Antigravity,
   Stitch, Figma: `DESIGN.md`, `code.html`, `screen.png`). If yes, record its
   path in `CLAUDE.md` and propose a `design.md` rule built from it. If it
   sits outside the repo, ask before copying it into `design/`.
4. **Reviewer agents**: generic ones are in `~/.claude/agents/`. List which
   apply, and propose any project-specific agent the spec needs that none of
   them covers (name, purpose, tools, model).
5. **Files to be created** and **commands to be run**, in order.
Then ask: "Approve this setup?" and stop.

## Step 2 — After approval
1. Create `docs/ARCHITECTURE.md`, `docs/DECISIONS.md` (record the stack
   decisions as ACCEPTED) from the templates in
   `~/.claude/templates/build/docs/`.
2. Copy `~/.claude/templates/build/rules/build-workflow.md` to
   `.claude/rules/build-workflow.md`. Create `artifacts/` with `.gitkeep`
   and add `artifacts/**/*.mp4` to `.gitignore` if recordings are used.
3. Run `/bootstrap` logic as needed to scaffold `CLAUDE.md` for the project
   (or, if the project folder is new, copy `~/.claude/templates/CLAUDE.md`
   and run `/bootstrap`). Ensure CLAUDE.md has a filled **Commands** and
   **Verification tooling** section.
4. Install and configure the approved verification tools. Ask before each
   install; report the exact command and its observed result. Do not claim
   a tool works until you have run a trivial flow with it and seen it pass.
5. Create any approved project-specific agents in `.claude/agents/` with
   valid frontmatter for the installed version. Reviewers get no Edit/Write.
6. Run the foundation checks once (typecheck/lint/test/build if a project
   exists) and report observed results.
7. Commit `chore: configure phased build workflow`.
8. Tell me the next step is `/plan-phases` and stop.
