# Starting a new project — plain-English guide (Claude Code desktop app)

Written for the **Claude Code desktop app** (the **Code** tab inside the Claude
Desktop app on your Mac). No terminal is needed to run a project. The only
place a terminal helps is the one-time install in section 1.

Example used throughout: a bonsai-care app for Android and iOS. It is only an
illustration. The same steps work for any web or mobile project.

---

## The short version

**Once per computer:** install the kit (section 1).

**Every new project:**
1. In Finder, make a project folder and put your reference material in a `reference` folder inside it.
2. In Claude Desktop, open the **Code** tab, choose that folder, and start a new session.
3. Type `/start` plus your idea. Claude runs three stages and stops for your approval at each: the interview and spec, the tools and technology, the phase plan.
4. It then tells you the exact line to type for Phase 1 (`/run-phase 01`).
5. From Phase 2 on, it gives you a `/goal` line to paste.
6. After each phase, read the checkpoint report and approve the next phase.

You never copy files into the project by hand. The commands do that.

---

## 1. One-time setup (per computer)

The kit lives in a hidden folder called `.claude` in your home folder. The
desktop app reads it, the same as the terminal version does.

**Easiest way (copy and paste, about a minute):**
1. Download the repo from GitHub and unzip it.
2. Open the **Terminal** app (Cmd+Space, type Terminal) and move into the unzipped folder: type `cd ` (with a space), drag the folder onto the Terminal window, press Enter.
3. Paste this block and press Enter:

```bash
mkdir -p ~/.claude/commands ~/.claude/agents ~/.claude/templates/build
cp global-CLAUDE.md ~/.claude/CLAUDE.md
cp CLAUDE.md        ~/.claude/templates/CLAUDE.md
cp commands/*.md    ~/.claude/commands/
cp agents/*.md      ~/.claude/agents/
cp -R build-template/. ~/.claude/templates/build/
```

4. The `settings.json` file needs care. If you **don't** already have
   `~/.claude/settings.json`, copy it in: `cp settings.json ~/.claude/settings.json`.
   If you **do** already have one, don't overwrite it. Instead, in a Claude
   session, say: "Merge the permissions in settings.json from this repo into my
   ~/.claude/settings.json without removing anything I already have."

**Without Terminal:** in Finder press Shift+Cmd+G, type `~/.claude`, and
copy the files across by hand into the same places as above. Creating the
folders `commands`, `agents` and `templates/build` first if they don't exist.

**Check it worked:** quit and reopen Claude Desktop, start a new session in the
Code tab, and type `/`. You should see `/start`, `/discover`, `/setup-build`,
`/plan-phases`, `/run-phase`, `/new-agent`, `/checkpoint`. Then ask: "List the
subagents you can use." You should see six reviewers (workflow-tester,
visual-reviewer, security-reviewer, accessibility-reviewer, content-reviewer,
phase-auditor).

You only repeat this when you update the repo.

---

## 2. Starting the bonsai project

### Step 1: make the folder and add your reference material
In Finder, create a folder, for example `Projects/bonsai-app`. Inside it,
create a folder called `reference`. Put in anything that helps explain what
you want:

- your old project spec document
- screenshots of apps you like or of your own sketches
- a design export from Antigravity or Stitch (DESIGN.md, code.html, screen.png)
- notes, saved web pages, anything else

Messy is fine. Claude reads it and only asks what's missing.

### Step 2: open the folder in the Code tab
In Claude Desktop, click the **Code** tab, choose your project folder
(`bonsai-app`), and start a new session. Each session is tied to one folder,
so use a new session for each project. Don't copy any CLAUDE.md in yourself.
The setup stage does it.

Leave the permission mode selector (next to the send button) on its default
for now.

### Step 3: start (stage 1 — discovery)
Type:

> /start A mobile app for Android and iOS to manage bonsai trees.

Claude first works out where the project is, then reads everything in your
`reference` folder by itself. It starts the interview and asks a few questions
at a time (who it's for, what it must do on day one, whether it works offline,
whether it needs accounts, and so on). You can answer "you decide" to any
question. Claude will recommend an answer and label it as a recommendation.

When it has enough, it shows you a draft spec in the chat. Nothing is written
yet. Read it, change anything, then say "approved". Only then does Claude
create `docs/PRODUCT-SPEC.md` and the other spec files.

No code is written in this step.

### Step 4: choose the technology and testing tools (stage 2)
After you approve the spec, `/start` carries on here by itself. (To run this
stage alone, type `/setup-build`.)

Claude proposes, in plain terms:
- the technology to build with (for example one codebase that runs on both Android and iOS)
- how it will test the app (pretend phones on your computer, called simulators and emulators)
- which reviewer agents will be used

It asks before installing anything. For phone apps, testing on a pretend iPhone
needs Apple's Xcode, and a pretend Android needs Android Studio. Both are big
downloads. Claude tells you what is missing and what to click. If you'd rather
not install them yet, tell it, and it will plan around that and mark those
checks "not run".

When you say yes, it sets everything up and proves the testing tools actually
work before moving on. For a web app, the desktop app can start your app and
show it in a built-in preview.

### Step 5: plan the phases (stage 3)
`/start` carries on here by itself after you approve the setup. (To run this
stage alone, type `/plan-phases`.)

Claude splits the build into small phases and shows you a table. Illustration
only, since your real plan depends on your answers:

| Phase | What gets built |
|---|---|
| 1 | App shell, navigation, saving data on the phone |
| 2 | Add, view and edit a tree |
| 3 | Care tasks and reminders |
| 4 | Photos and a journal for each tree |
| 5 | Polish, accessibility, release checks |

You can reorder, merge or split phases. Say what you want changed, then
"approved". Each phase gets its own file in `docs/phases/` that says exactly
what is included, what counts as done, and which reviewers check it.

### Step 6: build a phase
When planning is approved, `/start` ends by telling you the exact line to type
next and whether everything is ready. Claude can't start `/goal` for you. You
type it. Here is when and how:

- **First phase: use `/run-phase 01`.** Claude builds it while you watch, so
  you see how it behaves and how much usage it takes. You'll get permission
  pop-ups to approve.
- **Later phases: use `/goal`.** Open `docs/phases/PHASE-02-...md`, find the
  section called "Ready-to-run /goal", copy it, and type `/goal` followed by
  that text. (`/start` also prints this line for you.)

**Before a `/goal` run, set the permission mode to Auto.** In the Code tab, use
the mode selector next to the send button. Auto mode is what lets Claude work
for a long time without asking permission for every action. Two things to know:

- Auto mode needs a supported model (Sonnet 4.6 or later, Opus 4.6 or later,
  Haiku 5.5, or a Fable model) and must not be switched off by an
  organisation admin. For a solo user on a current model it should simply be
  in the selector. If it isn't, check the model dropdown next to the send
  button. If it's still missing, use **Accept edits** mode: your settings
  already approve routine commands (git, npm, tests), so a run only pauses on
  commands that aren't on that list. `/run-phase` also works.
- Local runs use your Mac. If it goes to sleep, the work pauses, so keep it
  awake for long runs. Cloud sessions carry on with the app closed, but they
  can't use your local simulators.
- There is also a "bypass permissions" option, off by default, in Settings →
  Claude Code. I'd leave it off. It removes the safety prompts.

The deny rules in your settings (no force-pushing, no reading your `.env`
files or `PROJECT KEYS` folder) still apply.

I couldn't confirm from the documentation that `/goal` appears in every
version of the desktop app. Type `/` and look for it. If it isn't there, use
`/run-phase` for every phase. You get the same work and the same reviews, you
just aren't running unattended.

During a run Claude builds, runs the tests, launches the app, takes
screenshots, calls the reviewer agents, fixes what they find, and writes a
checkpoint report. Then it stops.

To check progress, type `/goal`. To stop it, type `/goal clear` or press the
stop button.

### Step 7: review and continue
Read the checkpoint report (`docs/phases/CHECKPOINT-01.md`). It lists what
changed, what was tested, what passed, what was not run and why, and what the
reviewers found. Open the app yourself too. Then tell Claude to go ahead with
the next phase. It never moves on by itself.

---

## 3. The agents: do I need to do anything?

No. You don't switch them on. The phase files tell Claude which reviewers to
call near the end of each phase, and you'll see messages in the session like
"running workflow-tester".

What each one does:

| Agent | In plain terms |
|---|---|
| workflow-tester | Uses the app like a person would and reports what breaks |
| visual-reviewer | Looks at the screenshots for layout and design problems |
| security-reviewer | Checks logins, data access and secrets |
| accessibility-reviewer | Checks the app works for people using screen readers, large text etc |
| content-reviewer | Checks wording, for example that bonsai advice isn't stated with false certainty |
| phase-auditor | Double-checks the checkpoint report against what really changed |

The reviewers only report. They don't change your code. Claude fixes valid
findings afterwards.

If you want one by hand, just ask: "use the security-reviewer on this".
Agents use extra usage, which is why they run once per phase, not every step.

If a project needs a specialist that doesn't exist, type `/new-agent` and say
what for. It proposes one and asks before creating it.

---

## 4. What you still do by hand

- Create the project folder and the `reference` folder in Finder.
- In the Code tab, choose the folder and start a new session.
- Type `/start` once, then `/run-phase` or `/goal` for each phase.
- Approve the spec, the setup, the phase plan, and each phase.
- Switch the mode selector to Auto before a `/goal` run.
- Store API keys in `.env.local` as Claude tells you, never in chat.
- Look at the finished app after each phase.

Claude does the interview, the planning, the building, the testing, the
reviews and the reports.

---

## 5. If something goes wrong

- **Session ended or you closed the window midway:** open the Code tab, choose
  the same folder, start a new session and type `/start` again. It reads the
  files, works out which stage you were in, and carries on.
- **A run is going off track:** type `/goal clear` or press the stop button.
  Your work is saved in git.
- **Claude says a check was "NOT RUN":** that's honest reporting. Ask what's
  needed to run it (usually an emulator or a tool not installed yet).
- **A phase isn't right:** tell Claude exactly what you saw ("the add-tree
  button is hidden behind the keyboard on the iPhone screen"). Specific beats general.
- **Usage is running out:** `/goal` stops itself, and the next session picks
  up from the last commit and the phase file.
- **A command isn't in the `/` list:** quit and reopen Claude Desktop and start
  a new session. If it's still missing, re-check the install in section 1.

---

## 6. What the project looks like afterwards

```
bonsai-app/
  CLAUDE.md                 short project instructions Claude reads every session
  reference/                your starting material
  docs/
    PRODUCT-SPEC.md         what you're building
    USER-FLOWS.md           the journeys a user takes
    ACCEPTANCE-CRITERIA.md  testable "done" checks
    ARCHITECTURE.md         the technology choices
    DECISIONS.md            why choices were made
    RISKS.md
    phases/                 one file per phase, plus checkpoint reports
  artifacts/                screenshots and test evidence per phase
  .claude/rules/            extra instructions, created as the project grows
  src/ ...                  the actual app
```

---

## 7. Be realistic about the first run

This kit hasn't been run end to end on a real project yet, and I haven't
tested it inside the desktop app. Expect to tweak it after the first one. If a
command misbehaves, note exactly what happened and bring it back to be fixed.
That is how the kit improves.
