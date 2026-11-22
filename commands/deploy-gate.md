---
description: Gate this project's Vercel production deploys, so a failing typecheck, lint or unit test fails the deployment and the last good version stays live. Works on any plan (GitHub branch protection needs GitHub Pro on private repositories).
argument-hint: [anything unusual about this project's build]
---

Add a quality gate to this project's Vercel production build. Extra context: $ARGUMENTS

Why this exists: a push to `main` deploys to production through the Vercel
integration, and by default Vercel only checks that the app builds. GitHub's
branch protection and required status checks need GitHub Pro (or a public
repository) on a private repository, so the gate lives inside the Vercel
build instead. It does NOT block the push to `main`; it blocks the going-live.

## Step 1 — Inspect, don't assume (report before changing anything)
- Read `package.json` scripts, `vercel.json` (if any), the framework, the
  package manager and lockfile, and the test runner.
- Use the Vercel tools (if this session has them) to see whether the project's
  dashboard overrides the Build Command; a dashboard override beats
  `vercel.json`.
- Tell me what you found in a few lines.

## Step 2 — Decide the command from what actually exists
- Typecheck script, lint script, unit-test script (one-shot, NOT watch mode,
  NOT browser or end-to-end tests), then the project's existing build command
  as the LAST step, joined with `&&`. For an npm project with the kit's script
  names: `npm run check && npm run lint && npm test && npm run build`.
- If a typecheck, lint or unit-test script does not exist, say so instead of
  inventing one. If lint or tests already fail today, say exactly what fails
  and stop for my decision. Never weaken, skip or delete a check to make it
  pass.

## Step 3 — Put it in `vercel.json`
- Set `"buildCommand"` in `vercel.json` (create the file if needed) so the gate
  is saved in the repository and follows it to any device. Keep every other
  setting as it is (outputDirectory, framework, rewrites, headers,
  installCommand).
- Check that devDependencies are installed on Vercel (the tools the checks
  need must be available there).

## Step 4 — Prove it
1. Run the exact command end to end and show the result.
2. Temporarily add a deliberate error (for example a type error in a scratch
   file), run the command, show that it stops before the build step with a
   non-zero exit, then delete the scratch file and confirm `git status` shows
   only the intended change.
3. If a test reads `vercel.json` or the build command, update it to expect the
   new command.
4. Offer the CI workflow template `~/.claude/templates/build/ci/ci.yml`
   (copy to `.github/workflows/ci.yml`) unless the project already has one.

## Step 5 — Record it and finish
- Add a short decision entry (why: GitHub required checks need Pro on private
  repositories; the gate runs inside the Vercel build; the push to `main` is
  still accepted) and update the stack or deploy notes, following this
  project's `CLAUDE.md` rules.
- Work on a branch and commit. Do NOT push to `main` without asking me: a push
  to `main` deploys to production. After I approve and you push, check the
  deployment state with the Vercel tools and tell me whether it is READY or
  failed; if it failed, read the build log and explain why.
- Report: the final command, what you ran, what passed or failed, and anything
  I need to decide.
