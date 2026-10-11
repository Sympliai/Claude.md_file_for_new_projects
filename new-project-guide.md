# Starting a new project: step-by-step guide (Claude Code desktop app, Mac)

This guide assumes you have never done any of this before. Every step says
where to click, what to type, and what you should see when it worked. If what
you see is different, stop and read "If something goes wrong" (section 5).

The example is a bonsai-care app for Android and iPhone. It is only an
illustration. The same steps work for any web or phone app.

---

## Words used in this guide

- **Folder**: a normal Mac folder, the kind you see in Finder.
- **Terminal**: the Mac app where you type commands as text. You only need it
  once, for the setup in section 1.
- **Code tab**: the part of the Claude Desktop app where you build software
  with Claude. It sits next to the Chat and Cowork tabs.
- **Session**: one conversation in the Code tab. Each session works inside one
  folder.
- **Slash command**: a shortcut you type in the message box that starts with
  `/`, for example `/start`. When you type `/`, a list pops up. You can pick
  from the list or keep typing the name.
- **Agent** (reviewer): a helper Claude calls to check the work, for example
  one that checks the screenshots. You don't operate them.
- **Phase**: one small chunk of the build (for example "add and edit trees").
  The app is built one phase at a time.
- **Approve**: type the word "approved" in the message box and send it.

---

## The short version

**Once per computer:** install the kit (section 1).

**Every new project:**
1. In Finder, make a project folder. Put a folder called `reference` inside it and drop your notes and screenshots into that.
2. In Claude Desktop, open the **Code** tab, choose your project folder, start a new session.
3. Type `/start` followed by a sentence about your idea, and press Enter.
4. Answer Claude's questions. Approve at each of the three stages: the spec, the tools and technology, and the phase plan.
5. Claude then tells you exactly what to type to build Phase 1.
6. After each phase, read the report and approve the next one.

You never copy files into your project by hand. The commands do that.

---

## 1. One-time setup (per computer)

You do this once on each computer. The setup copies the kit's files into a
hidden folder in your home folder called `.claude`. Claude Code reads that
folder every time it starts.

### Step 1: Download the kit from GitHub
1. Open your GitHub repository in your web browser.
2. Click the green **Code** button.
3. Click **Download ZIP**.
4. Wait for the download to finish. The file lands in your **Downloads** folder.

### Step 2: Unzip it
1. Open **Finder** and click **Downloads** in the sidebar.
2. Double-click the file you just downloaded. Its name ends in `.zip`.
3. A new folder appears next to it. Its name ends in `-main`.
4. Double-click that new folder to open it.
5. Check that you can see these items directly inside: `CLAUDE.md`, `README.md`, `global-CLAUDE.md`, `settings.json`, and folders called `commands`, `agents` and `build-template`. If you only see one more folder, open that one and check again.

Leave this Finder window open. You'll need it in step 4.

### Step 3: Open Terminal
1. Press **Command + Space**. A search box appears.
2. Type `Terminal` and press **Enter**.
3. A window opens with a line of text ending in `%`. That is where you type.

### Step 4: Point Terminal at the kit folder
Terminal needs to know which folder to work in. You'll tell it by dragging.

1. In the Terminal window, type the letters `cd` and then press the **spacebar** once. (`cd` means "change directory", which means "go to this folder".) **Do not press Enter yet.**
2. Go to your Finder window. Take the folder you opened in step 2 (the one with `CLAUDE.md` inside) and **drag it onto the Terminal window**. Let go. Terminal types the folder's location after `cd ` for you.
3. Click in the Terminal window and press **Enter**. Nothing visible happens. That's normal.
4. Check you're in the right place: type `ls` and press **Enter**. Terminal lists the names in the folder. You should see `CLAUDE.md`, `README.md`, `commands`, `agents`, `build-template`. If you don't, repeat steps 1 to 3.

If macOS shows a pop-up saying Terminal would like to access files in your Downloads folder, click **OK** or **Allow**.

### Step 5: Copy the kit into place
1. Select all of the text in the box below and copy it (Command + C).
2. Click in the Terminal window and paste it (Command + V).
3. Press **Enter**. If Terminal asks you to confirm pasting several lines, choose **Paste**.

```bash
mkdir -p ~/.claude/commands ~/.claude/agents ~/.claude/templates/build
cp global-CLAUDE.md ~/.claude/CLAUDE.md
cp CLAUDE.md        ~/.claude/templates/CLAUDE.md
cp commands/*.md    ~/.claude/commands/
cp agents/*.md      ~/.claude/agents/
cp -R build-template/. ~/.claude/templates/build/
```

**What you should see:** nothing. Terminal just shows a new empty prompt. Silence
means it worked. You don't need to understand these lines. They copy the kit's
files into the right places.

**To double-check:** type `ls ~/.claude/commands` and press Enter. You should
see a list of names including `start.md`, `discover.md` and `run-phase.md`.

### Step 6: Add the permissions file
This file lists what Claude may do without asking and what it must never do
(for example reading your secret keys). First check whether you already have one:

1. In Terminal, type `ls ~/.claude/settings.json` and press **Enter**.
2. If Terminal replies `No such file or directory`, you don't have one. Type this and press **Enter**:
   `cp settings.json ~/.claude/settings.json`
3. If Terminal prints the file path instead, you **already have one**. Do **not** copy over it. Instead, after you finish section 1, open the Code tab, choose any folder, start a session, and send this message:

   > Merge the permissions in settings.json from my Downloads kit folder into ~/.claude/settings.json without removing anything I already have.

   Claude will show you the change and ask permission before it edits.

### Step 7: Check it worked
1. Quit Claude Desktop completely (Claude menu, then Quit) and open it again. This makes it load the new files.
2. Click the **Code** tab, choose any folder, and start a new session.
3. In the message box, type `/`. A list should pop up that includes `/start`, `/discover`, `/setup-build`, `/plan-phases`, `/run-phase`, `/new-agent` and `/checkpoint`.
4. Type this and send it: `List the subagents you can use.` Claude should name six: workflow-tester, visual-reviewer, security-reviewer, accessibility-reviewer, content-reviewer and phase-auditor.

If both checks pass, the kit is installed. You only repeat section 1 when you
update the kit on GitHub.

---

## 2. Starting the bonsai project

### Step 1: Make the project folder and the reference folder
1. In Finder, go to where you keep projects, for example your **Documents** folder.
2. Press **Shift + Command + N** to make a new folder. Type a name, for example `bonsai-app`, and press **Enter**.
3. Double-click `bonsai-app` to open it.
4. Press **Shift + Command + N** again. Type `reference` (all lowercase) and press **Enter**.
5. Drag anything useful into the `reference` folder: your old project spec, screenshots, a design export from Antigravity or Stitch, notes. Messy is fine. Claude reads it all and only asks about what's missing.

### Step 2: Open the folder in the Code tab
1. Open **Claude Desktop** and click the **Code** tab.
2. Before you type anything, look at the area around the message box. Find the **project folder** choice and select your `bonsai-app` folder. Make sure the environment says **Local**.
3. Leave the permission mode (the selector next to the send button) on its default.
4. Don't copy any `CLAUDE.md` file into the folder yourself. The setup stage does that.

### Step 3: Start the project (stage 1 of 3: the interview)
1. Click in the message box and type `/start`, then a space.
2. Type a sentence about your idea. For example:

   > A mobile app for Android and iPhone to manage bonsai trees.

3. Press **Enter**.

**What happens next:** Claude checks the folder, reads everything in `reference`,
and tells you what it found. Then it asks a few questions at a time (who the app
is for, what it must do on day one, whether it works without internet, whether
people need accounts, and so on).

- You can answer in plain language.
- You can say **"you decide"** to any question. Claude will choose something sensible and label it a recommendation.
- No code is written in this stage.

When Claude has enough, it shows a **draft spec** in the chat. Nothing is saved yet.
Read it. If you want changes, say what to change. When you're happy, type
**approved** and send. Only then does Claude save the spec files into a `docs`
folder inside your project.

### Step 4: Choose the technology and testing tools (stage 2 of 3)
After you approve the spec, Claude carries on to this stage by itself.

Claude will explain, in plain language:
- what technology it recommends building the app with
- how it will test the app by running pretend phones on your Mac (called simulators and emulators)
- which reviewer agents it will use

**Claude asks before installing anything.** For phone apps you may need big free
downloads: Apple's **Xcode** (for the pretend iPhone) and **Android Studio** (for
the pretend Android phone). Claude tells you what's missing and what to click.
If you don't want to install them yet, say so. Claude plans around it and
marks those checks "not run".

When you say yes, Claude sets things up and runs a tiny test to prove the tools
really work. Then it moves on.

### Step 5: Plan the phases (stage 3 of 3)
After you approve the setup, Claude carries on to this stage by itself.

It splits the build into small phases and shows you a table. This one is only an
example. Your real plan depends on your answers:

| Phase | What gets built |
|---|---|
| 1 | App shell, navigation, saving data on the phone |
| 2 | Add, view and edit a tree |
| 3 | Care tasks and reminders |
| 4 | Photos and a journal for each tree |
| 5 | Polish, accessibility, release checks |

Say if you want the order changed, or phases merged or split. When you're happy,
type **approved**. Claude saves one file per phase in the `docs/phases` folder.
Each file says exactly what's included, what counts as done, and which
reviewers check it.

### Step 6: Build Phase 1
When planning is approved, Claude tells you in plain words which phase to do
first, **the exact line to type next**, and whether everything is ready.

For Phase 1 the line is:

> /run-phase 01

1. Click in the message box, type exactly that, and press **Enter**.
2. Claude builds the phase while you watch. You may see **permission requests**: small prompts asking if Claude may run a command or change a file. Read them and approve if they look right.
3. Claude runs the tests, starts the app, takes screenshots, calls the reviewer agents, fixes what they find, and writes a report. Then it stops by itself. It never carries on to the next phase without you.

Watching the first phase teaches you how Claude behaves and how much of your
usage allowance a phase uses.

### Step 7: Read the report and approve the next phase
1. When Claude stops, it summarises the phase in the chat. It also names a report file called `CHECKPOINT-01.md`. Click that file name in the chat to open it, or ask: **"Summarise the Phase 1 report."**
2. The report says what changed, what was tested and passed, what was **not run** and why, and what the reviewers found.
3. Open the app yourself and try it.
4. If something's wrong, tell Claude exactly what you saw (see section 5). If it's good, type **"Approved, go to Phase 2"**.

### Step 8: Later phases: letting Claude work on its own with `/goal`
From Phase 2 on, you can have Claude work without you watching, using a command
called `/goal`. Claude can't start it for you. You type it.

1. Ask Claude: **"Give me the /goal line for Phase 2."** (Claude also prints this line at the end of planning.) It will give you a block of text that starts with `/goal`.
2. Set the permission mode to **Auto**: click the permission mode selector next to the send button and choose **Auto**. (Auto lets Claude work without asking permission for every action.)
3. Copy the whole `/goal ...` block, paste it into the message box, and press **Enter**.
4. Keep your Mac awake and the app open. A sleeping Mac pauses the work.

**Check progress:** type `/goal` and press Enter.
**Stop it:** type `/goal clear` and press Enter, or click the stop button.

**If Auto isn't in the mode selector:**
- Check the **model** dropdown next to the send button. Auto needs a recent model (Sonnet 4.6 or later, Opus 4.6 or later, Haiku 5.5, or a Fable model).
- If it's still missing, choose **Accept edits** instead. Your settings already pre-approve everyday commands (git, npm, tests), so a run only pauses on commands that aren't on that list.
- Or just use `/run-phase 02`, `/run-phase 03` and so on for every phase.

There is also a "Bypass permissions" option in Settings. Leave it off. It removes the safety prompts.

I couldn't confirm from the documentation that `/goal` shows up in every
version of the desktop app. Type `/` and look for it in the list. If it isn't
there, use `/run-phase` for every phase. You get the same work and the same
reviews.

---

## 3. The agents: do I need to do anything?

No. You never switch them on. The phase files tell Claude which reviewers to
call near the end of each phase. You'll see messages in the session such as
"running workflow-tester".

| Agent | What it does, in plain terms |
|---|---|
| workflow-tester | Uses the app like a real person and reports what breaks |
| visual-reviewer | Looks at the screenshots for layout and design problems |
| security-reviewer | Checks logins, data access and secrets |
| accessibility-reviewer | Checks the app works with screen readers, large text and so on |
| content-reviewer | Checks the wording, for example that bonsai advice isn't stated with false certainty |
| phase-auditor | Double-checks the phase report against what really changed |

The reviewers only report. They don't change your code. Claude fixes the valid
findings afterwards.

If you want one by hand, type: **"Use the security-reviewer on this."**

Agents use extra usage allowance, which is why they run once per phase and not
at every step.

If a project needs a specialist that doesn't exist, type `/new-agent` and say
what it's for. Claude proposes one and asks before creating it.

---

## 4. What you do by hand, and what Claude does

**You:**
- Make the project folder and the `reference` folder in Finder.
- In the Code tab, choose the folder and start a new session.
- Type `/start` once. Then type `/run-phase 01`, and `/run-phase` or `/goal` for each later phase.
- Type "approved" at each stage and each phase.
- Switch the permission mode to Auto before a `/goal` run.
- Put secret keys in a file called `.env.local` when Claude tells you to. Never type or paste them into the chat.
- Try the app yourself after each phase.

**Claude:** the interview, the planning, the building, the testing, the reviews
and the reports.

---

## 5. If something goes wrong

| What happened | What to do |
|---|---|
| You closed the window or the session ended halfway | Open the Code tab, choose the same folder, start a new session, type `/start`. Claude reads the files, works out which stage you were in, and carries on. |
| A run is going the wrong way | Type `/goal clear` or click the stop button. Your work is saved. |
| Claude says a check was "NOT RUN" | That's honest reporting. Ask: "What do I need to install to run it?" |
| A phase isn't right | Tell Claude exactly what you saw, for example "the add-tree button is hidden behind the keyboard on the iPhone screen". Specific beats general. |
| Your usage allowance ran out | The run stops itself. In your next session, type `/start` and it continues from the last saved point. |
| A command isn't in the `/` list | Quit Claude Desktop completely, reopen it, and start a new session. If it's still missing, repeat section 1. |
| Terminal says `No such file or directory` | You're probably not inside the kit folder. Repeat section 1, step 4. |

---

## 6. What your project folder looks like afterwards

```
bonsai-app/
  CLAUDE.md                 short instructions Claude reads every session
  reference/                your starting material
  docs/
    PRODUCT-SPEC.md         what you're building
    USER-FLOWS.md           the journeys a user takes
    ACCEPTANCE-CRITERIA.md  the "done" checks
    ARCHITECTURE.md         the technology choices
    DECISIONS.md            why choices were made
    RISKS.md
    phases/                 one file per phase, plus the reports
  artifacts/                screenshots and test evidence
  .claude/rules/            extra instructions, added as the project grows
  src/ ...                  the actual app
```

---

## 7. Be realistic about the first run

This kit hasn't been run end to end on a real project yet, and it hasn't been
tested inside the desktop app. Expect to adjust it after your first project. If
a command misbehaves, note exactly what you typed and what happened, and bring
it back to be fixed. That's how the kit gets better.
