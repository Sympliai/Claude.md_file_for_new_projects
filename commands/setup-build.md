---
description: After the spec is approved (or an audit is reviewed) — agree the stack, install the phased build workflow, verification tooling and reviewer agents, and fill CLAUDE.md. Asks before installing anything.
---

Set up the build workflow for this project. Extra context: $ARGUMENTS

## Preconditions
- One of these must be true; otherwise stop and tell me which command to run:
  - **New product**: `docs/PRODUCT-SPEC.md` exists and is APPROVED (if not:
    `/discover`).
  - **Adopted project**: a `docs/AUDIT-*.md` is REVIEWED and I chose findings
    to plan as phases (if not: `/audit`). This is *adoption mode*.
- Run `claude --version` and `git status`. Report both.

## Step 1 — Propose, don't change (wait for my approval)
Present, in chat:
1. **Stack.**
   - New product: a recommendation with trade-offs and why it fits the spec
     (web / mobile / both; framework; backend; auth; storage; hosting). Use my
     global defaults unless the spec argues otherwise. Mark it RECOMMENDATION.
   - Adoption mode: no recommendation. The stack is what the code uses.
     Summarise it in a few lines from `CLAUDE.md`; it will be recorded as
     ACCEPTED decisions. Changing any part of it is a finding to plan, not
     something to do here.
2. **Verification tooling** for the platform:
   - Web: Playwright (committed e2e tests) and/or Claude Code's Chrome
     integration for interactive checks. Add an accessibility scan
     (`@axe-core/playwright`) so every phase saves measured results for the
     accessibility reviewer.
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
3. **Design.** Ask whether I have a UI design export (Antigravity, Stitch,
   Figma: `DESIGN.md`, `code.html`, `screen.png`).
   - If yes: record its path in `CLAUDE.md` and propose a `design.md` rule
     built from it. If it sits outside the repo, ask before copying it into
     `design/`.
   - If no, and the product has a UI, and there is no
     `.claude/rules/design.md` yet: propose a small design system for my
     approval, so the first screen is not styled ad hoc — colour tokens
     (light and dark if both are needed) with text/background pairs that
     meet 4.5:1 contrast; type scale; spacing and radius scales; one icon
     set; and the basic parts (button variants, text input, card, modal,
     toast, and the loading, empty and error states). Use a design skill if
     this session has one. Adoption mode: build `design.md` from the live
     code instead, and list inconsistencies as findings.
4. **Reviewer agents**: generic ones are in `~/.claude/agents/`. List which
   apply, and propose any project-specific agent the spec needs that none of
   them covers (name, purpose, tools, model).
5. **Branches and deploys**: say which branch deploys to production (usually
   `main`), that each phase is built on its own `phase-NN-<slug>` branch, and
   that this project will ask me before any push to `main`.
6. **Files to be created** and **commands to be run**, in order.
Then ask: "Approve this setup?" and stop.

## Step 2 — After approval
1. Create `docs/ARCHITECTURE.md`, `docs/DECISIONS.md` (record the stack
   decisions as ACCEPTED) from the templates in
   `~/.claude/templates/build/docs/`. Adoption mode: fill ARCHITECTURE.md
   from the live code and mark it `AS BUILT (<date>)`; also copy
   `ACCEPTANCE-CRITERIA.md`, `BACKLOG.md` and the `phases/` templates if
   they are missing.
2. Copy `~/.claude/templates/build/rules/build-workflow.md` to
   `.claude/rules/build-workflow.md`. Create `artifacts/` with `.gitkeep`.
   Add `artifacts/**/changes.diff` to `.gitignore`, and
   `artifacts/**/*.mp4` if recordings are used.
3. Make pushes to `main` ask first: merge the `ask` rules from
   `~/.claude/templates/build/settings/project-settings.json` into
   `.claude/settings.json` (create it if missing; keep anything already
   there). Commit that file.
4. Run `/bootstrap` logic as needed to scaffold `CLAUDE.md` for the project
   (or, if the project folder is new, copy `~/.claude/templates/CLAUDE.md`
   and run `/bootstrap`; with an approved spec it fills from the docs and
   does not interview again). Ensure CLAUDE.md has a filled **Commands** and
   **Verification tooling** section. Write the approved design system to
   `.claude/rules/design.md` with `paths:` frontmatter.
5. Install and configure the approved verification tools. Ask before each
   install; report the exact command and its observed result. Do not claim
   a tool works until you have run a trivial flow with it and seen it pass.
6. Create any approved project-specific agents in `.claude/agents/` with
   valid frontmatter for the installed version. Reviewers get no Edit/Write.
7. Run the foundation checks once (typecheck/lint/test/build if a project
   exists) and report observed results.
8. Commit `chore: configure phased build workflow`.
9. Tell me the next step is `/plan-phases` and stop.
