---
description: Propose and create a new specialist subagent when no existing one covers a review or task the project needs.
---

A specialist is needed for: $ARGUMENTS

1. List the existing agents in `~/.claude/agents/` and `.claude/agents/` and
   say why none of them fit.
2. Propose the new agent in chat: `name` (lowercase-hyphen), a `description`
   written so Claude knows exactly when to delegate to it, `tools` (allowlist;
   no Edit/Write/Bash for reviewers unless justified), `model` (sonnet by
   default, haiku for light checks), what it reads, what it must output, and
   its explicit limits.
3. Check the installed Claude Code version's supported frontmatter fields
   before writing — use only fields that exist.
4. After I approve, write it to `.claude/agents/<name>.md` (project) or
   `~/.claude/agents/<name>.md` if I say it is generic. Confirm it appears
   (ask me to list the available subagents, or use `/agents` in the terminal).
5. Add it to the relevant phase files' Reviewers lists if I ask.
