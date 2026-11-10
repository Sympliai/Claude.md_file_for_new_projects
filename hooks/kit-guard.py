#!/usr/bin/env python3
"""kit-guard: guard rails for Claude Code sessions (Claude Code setup kit).

Modes
  secrets    PreToolUse hook for every session. Blocks tool calls that would
             read or write a secret file (.env*, key folders), and scans what
             is about to be committed for key-shaped strings.
  readonly   PreToolUse hook for reviewer subagents that have Bash. Does the
             secrets checks, and also blocks commands that change files or
             git state.
  scan-repo  Not a hook. Scans the tracked files of the current repository
             and prints `file:line: pattern name`. Never prints the value.

Hook modes read the tool call as JSON on stdin. Printing nothing means "no
opinion": the normal permission rules still decide. A crash also means "no
opinion", so a bug here can never lock a session.

These are guard rails, not a sandbox. They catch the commands Claude normally
writes; a deliberately obscure command can get round them. For OS-level
blocking, turn on the Claude Code sandbox as well.
"""
import base64
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile

# --------------------------------------------------------------- secret paths

ALLOWED_NAMES = {".env.example"}          # names-only file: safe to read
KEY_DIRS = {"project keys"}               # compared lower-case
SECRET_NAME = re.compile(r"^\.env($|[.*?\[{])|^\.envrc$")
KEY_FILE = re.compile(r"\.(pem|p12|pfx|keystore|jks)$|^id_(rsa|dsa|ecdsa|ed25519)$")
# ".env" as its own word inside a longer string: matches `cat .env`,
# `open('.env.local')`, `--env-file=.env`; not `process.env.X`.
MENTION = re.compile(r"(?<![A-Za-z0-9_.\-])\.env(?:rc\b|\.[A-Za-z0-9_.\-*?]+|[*?]|\b)")
KEY_DIR_MENTION = re.compile(r"project keys", re.I)


def is_secret_path(path):
    """True when the path names a secret file or sits in a key folder."""
    parts = [p for p in re.split(r"[\\/]+", str(path).strip().strip("'\"")) if p]
    if not parts:
        return False
    if any(p.lower() in KEY_DIRS for p in parts):
        return True
    return parts[-1] not in ALLOWED_NAMES and bool(SECRET_NAME.match(parts[-1]))


def secret_mentions(text):
    """Secret file names mentioned anywhere in a piece of shell text."""
    found = [m.group(0) for m in MENTION.finditer(text) if m.group(0) not in ALLOWED_NAMES]
    if KEY_DIR_MENTION.search(text):
        found.append("PROJECT KEYS")
    return found


# -------------------------------------------------------------- shell parsing

HEREDOC = re.compile(r"(?<!<)<<(?!<)-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")
WRAPPERS = {"env", "command", "builtin", "time", "nice", "nohup", "stdbuf", "timeout", "xargs", "exec"}
ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")


def split_segments(cmd):
    """Split a shell command into simple commands, respecting quotes.

    Splits on ; | & && || and newlines. A command substitution, $(...) or
    backticks, becomes its own segment even inside double quotes.
    """
    segs, cur, stack = [], [], []   # stack holds open contexts: ' " $( `
    i, n = 0, len(cmd)

    def flush():
        text = "".join(cur).strip()
        del cur[:]
        if text:
            segs.append(text)

    while i < n:
        c = cmd[i]
        top = stack[-1] if stack else ""
        if top == "'":
            cur.append(c)
            if c == "'":
                stack.pop()
            i += 1
        elif c == "\\" and i + 1 < n:
            cur.append(cmd[i:i + 2])
            i += 2
        elif cmd.startswith("$(", i):
            stack.append("$(")
            flush()
            i += 2
        elif c == "`":
            if top == "`":
                stack.pop()
            else:
                stack.append("`")
            flush()
            i += 1
        elif top == '"':
            cur.append(c)
            if c == '"':
                stack.pop()
            i += 1
        elif c == ")" and top == "$(":
            stack.pop()
            flush()
            i += 1
        elif c in "\"'":
            stack.append(c)
            cur.append(c)
            i += 1
        elif c == "&" and ((i > 0 and cmd[i - 1] == ">") or cmd.startswith("&>", i)):
            cur.append(c)           # part of a redirect such as 2>&1 or &>file
            i += 1
        elif c in ";\n|&()":
            flush()
            i += 1
        else:
            cur.append(c)
            i += 1
    flush()
    return segs


def words(segment):
    try:
        return shlex.split(segment, posix=True)
    except ValueError:              # unbalanced quotes: fall back to spaces
        return [w.strip("'\"") for w in segment.split()]


def program(segment):
    """(program name, arguments), skipping VAR=value prefixes and wrappers."""
    w = words(segment)
    i = 0
    while i < len(w):
        base = os.path.basename(w[i])
        if ASSIGNMENT.match(w[i]):
            i += 1
        elif base in WRAPPERS:
            i += 1
            while i < len(w) and (w[i].startswith("-") or ASSIGNMENT.match(w[i])
                                  or (base == "timeout" and w[i][:1].isdigit())):
                i += 1
        else:
            return base, w[i + 1:]
    return "", []


def git_subcommand(args):
    i = 0
    while i < len(args):
        if args[i] in ("-C", "-c", "--git-dir", "--work-tree"):
            i += 2
        elif args[i].startswith("-"):
            i += 1
        else:
            return args[i], args[i + 1:]
    return "", []


def fold_heredocs(cmd):
    """Fold each heredoc into the line that starts it.

    A heredoc that `cat` simply prints is plain text (a commit message, say),
    so its body is dropped. Any other heredoc, including one piped onwards or
    redirected into a file, is code or input for a command and stays attached
    to it, so the checks see it.
    """
    lines = cmd.split("\n")
    out, i = [], 0
    while i < len(lines):
        m = HEREDOC.search(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        j, body = i + 1, []
        while j < len(lines) and lines[j].strip() != m.group(2):
            body.append(lines[j])
            j += 1
        head = split_segments(lines[i][:m.start()])
        receiver = program(head[-1])[0] if head else ""
        tail = lines[i][m.end():]
        plain_text = (receiver == "cat" and "|" not in tail and ">" not in tail
                      and ">" not in head[-1])
        out.append(lines[i] if plain_text else lines[i] + " " + " ".join(body))
        i = j + 1
    return "\n".join(out)


def unquote(token):
    return token.strip("'\"")


# -------------------------------------------------- secrets mode: Bash checks

NAMES_ONLY = {"ls", "test", "[", "[[", "stat", "touch"}       # never show contents
NAMES_ONLY_GIT = {"check-ignore", "ls-files", "status"}
TEXT_ARGS = {"echo", "printf"}                               # arguments are text
PATCH_FLAGS = {"-p", "-u", "--patch", "--cc", "-c"}


def bash_secret_problem(command):
    """Why a Bash command would expose a secret file, or None."""
    for seg in split_segments(fold_heredocs(command)):
        mentions = secret_mentions(seg)
        if not mentions:
            continue
        prog, args = program(seg)
        whole_tokens = [unquote(re.sub(r"^[0-9&]*[<>]+", "", a.split("=", 1)[-1])) for a in args]
        names_a_file = any(is_secret_path(t) for t in whole_tokens if t)
        if prog in NAMES_ONLY:
            continue
        if prog in TEXT_ARGS and not names_a_file:
            continue
        if prog == "git":
            sub, rest = git_subcommand(args)
            if sub in NAMES_ONLY_GIT:
                continue
            if sub == "rm" and "--cached" in rest:
                continue            # untracking a committed secret is a fix
            if sub == "commit" and not names_a_file:
                continue            # only mentioned in the message
            if sub == "log" and not any(a in PATCH_FLAGS or a.startswith(("-L", "--patch")) for a in rest):
                continue            # history of the name, not the contents
        return mentions[0]
    return None


# ------------------------------------------------------------- secret scanning

def _jwt_is_service_role(match):
    try:
        payload = match.group(0).split(".")[1]
        decoded = base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4))
        return b"service_role" in decoded
    except Exception:
        return False


def _has_digit(match):
    return any(ch.isdigit() for ch in match.group(0))


PATTERNS = [
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b"), None),
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), None),
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{40,})\b"), None),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}"), None),
    ("Stripe live key", re.compile(r"\b[sr]k_live_[A-Za-z0-9]{16,}\b"), None),
    ("API secret key (sk-...)", re.compile(r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_\-]{24,}"), _has_digit),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"), None),
    ("SendGrid key", re.compile(r"\bSG\.[A-Za-z0-9_\-]{22}\.[A-Za-z0-9_\-]{43}\b"), None),
    ("Supabase secret key", re.compile(r"\bsb_secret_[A-Za-z0-9_\-]{20,}"), None),
    ("Supabase service-role JWT",
     re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"), _jwt_is_service_role),
]
ALLOW_MARKER = "secret-scan:allow"
MAX_FILE_BYTES = 1_000_000


def line_findings(line):
    if ALLOW_MARKER in line:
        return []
    return [name for name, rx, confirm in PATTERNS
            if any(confirm is None or confirm(m) for m in rx.finditer(line))]


def name_finding(path):
    base = os.path.basename(path)
    if is_secret_path(path):
        return "secret file"
    if KEY_FILE.search(base):
        return "key file"
    return None


def git(args, cwd, timeout=20):
    try:
        r = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True,
                           errors="replace", timeout=timeout)
        return r.stdout if r.returncode == 0 else ""
    except Exception:
        return ""


def scan_diff(diff_text):
    """Findings in the added lines of a unified diff: (path, line, name)."""
    hits, path, lineno = [], None, 0
    for line in diff_text.splitlines():
        if line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else None
        elif line.startswith("@@"):
            m = re.match(r"@@ -\S+ \+(\d+)", line)
            lineno = int(m.group(1)) if m else 0
        elif line.startswith("+") and path:
            hits += [(path, lineno, name) for name in line_findings(line[1:])]
            lineno += 1
        elif line.startswith(" "):
            lineno += 1
    return hits


def scan_file(root, rel):
    full = os.path.join(root, rel)
    try:
        if os.path.getsize(full) > MAX_FILE_BYTES:
            return []
        with open(full, "rb") as fh:
            data = fh.read()
    except OSError:
        return []
    if b"\0" in data[:8000]:
        return []                   # binary
    hits = []
    for number, line in enumerate(data.decode("utf-8", "replace").splitlines(), 1):
        hits += [(rel, number, name) for name in line_findings(line)]
    return hits


def scan_commit(cwd, include_unstaged, include_untracked):
    """Findings in what a `git commit` is about to record."""
    hits = scan_diff(git(["diff", "--cached", "-U0"], cwd))
    names = git(["diff", "--cached", "--name-only", "--diff-filter=AMR"], cwd).splitlines()
    if include_unstaged:
        hits += scan_diff(git(["diff", "-U0"], cwd))
    if include_untracked:
        untracked = git(["ls-files", "--others", "--exclude-standard"], cwd).splitlines()[:300]
        names += untracked
        for rel in untracked:
            hits += scan_file(cwd, rel)
    hits += [(n, 0, name_finding(n)) for n in names if name_finding(n)]
    return sorted(set(hits))


def describe(hits, limit=8):
    lines = ["  %s%s: %s" % (p, (":%d" % n) if n else "", name) for p, n, name in hits[:limit]]
    if len(hits) > limit:
        lines.append("  ... and %d more" % (len(hits) - limit))
    return "\n".join(lines)


def commit_problem(command, cwd):
    """Message when a commit in this command would record a secret, or None."""
    commits, adds, commit_all = False, False, False
    for seg in split_segments(fold_heredocs(command)):
        prog, args = program(seg)
        if prog != "git":
            continue
        sub, rest = git_subcommand(args)
        if sub == "add":
            adds = True
        if sub == "commit":
            commits = True
            commit_all = commit_all or any(
                a == "--all" or (a.startswith("-") and not a.startswith("--") and "a" in a) for a in rest)
    if not commits:
        return None
    hits = scan_commit(cwd, include_unstaged=adds or commit_all, include_untracked=adds)
    if not hits:
        return None
    return ("Blocked by kit-guard: this commit would record what looks like a secret.\n"
            + describe(hits)
            + "\nDo not print the value. Unstage the file, tell the user which file and line, and let"
              " them decide. A confirmed false positive can be marked by the user with a '"
            + ALLOW_MARKER + "' comment on that line.")


def scan_repo(cwd):
    files = git(["ls-files"], cwd).splitlines()
    hits = []
    for rel in files:
        hits += scan_file(cwd, rel)
        if name_finding(rel):
            hits.append((rel, 0, name_finding(rel) + " is tracked by git"))
    history = git(["log", "--all", "--diff-filter=A", "--name-only", "--format="], cwd).splitlines()
    for rel in sorted(set(h for h in history if h and name_finding(h) and h not in files)):
        hits.append((rel, 0, name_finding(rel) + " was committed in the past (rotate any keys it held)"))
    hits = sorted(set(hits))
    if not hits:
        print("kit-guard scan-repo: no key-shaped strings or secret files in %d tracked files." % len(files))
        return 0
    print("kit-guard scan-repo: %d finding(s). Values are not shown." % len(hits))
    print(describe(hits, limit=200))
    return 1


# ------------------------------------------------- readonly mode: Bash checks

READ_ONLY_GIT = {
    "diff", "log", "status", "show", "ls-files", "ls-tree", "ls-remote", "rev-parse", "rev-list",
    "blame", "grep", "describe", "cat-file", "merge-base", "shortlog", "name-rev", "check-ignore",
    "for-each-ref", "show-ref", "count-objects", "whatchanged", "help", "version",
}
BRANCH_WRITE_FLAGS = {"-d", "-D", "-m", "-M", "-c", "-C", "-f", "-u", "--delete", "--move", "--copy",
                      "--force", "--set-upstream-to", "--unset-upstream", "--edit-description"}
ALWAYS_BLOCKED = {"rm", "rmdir", "mv", "ln", "chmod", "chown", "dd", "truncate", "patch", "shred",
                  "unlink", "sudo", "eval"}
WRITERS_LAST_ARG = {"cp", "rsync", "install"}                # destination is the last argument
WRITERS_ALL_ARGS = {"mkdir", "touch", "tee"}                 # every argument is a destination
SHELLS = {"bash", "sh", "zsh", "dash", "fish"}
INTERPRETERS = {"python", "python3", "node", "deno", "bun", "ruby", "perl", "php"}
INLINE_FLAGS = {"-c", "-e", "-p", "--eval", "--print"}
PACKAGE_MANAGERS = {"npm", "pnpm", "yarn", "bun", "pip", "pip3", "brew", "gem"}
PACKAGE_WRITES = {"install", "i", "add", "remove", "rm", "uninstall", "un", "update", "up", "upgrade",
                  "ci", "publish", "link", "unlink", "dedupe", "prune", "init", "version", "rebuild",
                  "create", "set", "config"}
REDIRECT = re.compile(r"^(?:[0-9]+|&)?>>?(.*)$")


def scratch_ok(path, cwd):
    """Reviewers may write evidence under artifacts/ and to temp folders."""
    path = unquote(path)
    if path in ("/dev/null", "/dev/stdout", "/dev/stderr", "-"):
        return True
    full = os.path.realpath(os.path.join(cwd, os.path.expanduser(path)))
    roots = [os.path.join(os.path.realpath(cwd), "artifacts"), "/tmp", "/private/tmp",
             "/var/folders", "/private/var/folders", os.path.realpath(tempfile.gettempdir())]
    return any(full == r or full.startswith(r.rstrip(os.sep) + os.sep) for r in roots)


def git_is_read_only(sub, rest):
    if sub in READ_ONLY_GIT:
        return True
    if sub == "branch":
        return not any(a in BRANCH_WRITE_FLAGS or not a.startswith("-") for a in rest)
    if sub == "stash":
        return rest[:1] in (["list"], ["show"])
    if sub == "remote":
        return not rest or rest[0] in ("-v", "show", "get-url")
    if sub == "tag":
        return not rest or rest[0] in ("-l", "--list")
    if sub == "config":
        return any(a in ("--get", "--list", "-l", "--get-all") for a in rest)
    if sub == "worktree":
        return rest[:1] == ["list"]
    return False


def bash_write_problem(command, cwd):
    """Why a Bash command would change files or git state, or None."""
    for seg in split_segments(fold_heredocs(command)):
        prog, args = program(seg)
        plain = [a for a in args if not a.startswith("-")]
        if prog in ALWAYS_BLOCKED:
            return prog
        if prog == "git":
            sub, rest = git_subcommand(args)
            if not git_is_read_only(sub, rest):
                return "git " + sub
        if prog in WRITERS_LAST_ARG and not (plain and scratch_ok(plain[-1], cwd)):
            return prog + " (outside artifacts/)"
        if prog in WRITERS_ALL_ARGS and not all(scratch_ok(a, cwd) for a in plain):
            return prog + " (outside artifacts/)"
        if prog in ("sed", "gsed", "perl", "ruby") and any(
                a == "--in-place" or re.match(r"^-[A-Za-z]*i", a) for a in args):
            return prog + " in-place edit"
        if prog in ("awk", "gawk") and "inplace" in args:
            return prog + " in-place edit"
        if prog == "find" and any(a in ("-delete", "-exec", "-execdir", "-ok") or a.startswith("-fprint")
                                  for a in args):
            return "find with -delete/-exec"
        if prog in SHELLS and ("-c" in args or "<<" in seg):
            return prog + " with inline code"
        if prog in INTERPRETERS and (any(a in INLINE_FLAGS for a in args) or "<<" in seg):
            return prog + " with inline code"
        if prog in PACKAGE_MANAGERS:
            if (plain[:1] and plain[0] in PACKAGE_WRITES) or (prog == "yarn" and not plain) \
                    or (plain[:1] == ["audit"] and "fix" in plain):
                return prog + " " + (plain[0] if plain else "install")
        if prog == "wget" and not any(a in ("-O-", "-qO-") for a in args):
            return "wget download"
        if prog == "curl":
            for k, a in enumerate(args):
                if a in ("-O", "--remote-name") or (a in ("-o", "--output") and not (
                        k + 1 < len(args) and scratch_ok(args[k + 1], cwd))):
                    return "curl download (outside artifacts/)"
        tokens = words(seg)
        for k, tok in enumerate(tokens):
            m = REDIRECT.match(tok)
            if not m:
                continue
            target = m.group(1) or (tokens[k + 1] if k + 1 < len(tokens) else "")
            if target.startswith("&") or not target:
                continue            # 2>&1 and friends
            if not scratch_ok(target, cwd):
                return "redirect to " + target
    return None


# ------------------------------------------------------------------ hook entry

def deny(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}))
    sys.exit(0)


SECRET_FILE_MESSAGE = (
    "Blocked by kit-guard: %s is a secret file. Secret values must never enter the session."
    " Name the variable, say it belongs in .env.local, and ask the user to set or check it."
    " (.env.example is allowed. To edit .gitignore, use the Edit tool.)")


def hook(mode):
    event = json.load(sys.stdin)
    tool = event.get("tool_name", "")
    data = event.get("tool_input") or {}
    cwd = event.get("cwd") or os.getcwd()

    if tool in ("Read", "Edit", "Write", "MultiEdit", "NotebookEdit"):
        path = data.get("file_path") or data.get("notebook_path") or ""
        if is_secret_path(path):
            deny(SECRET_FILE_MESSAGE % os.path.basename(str(path)))
    elif tool == "Grep":
        for key in ("path", "glob"):
            if data.get(key) and is_secret_path(data[key]):
                deny(SECRET_FILE_MESSAGE % data[key])
    elif tool == "Bash":
        command = data.get("command") or ""
        found = bash_secret_problem(command)
        if found:
            deny(SECRET_FILE_MESSAGE % found)
        message = commit_problem(command, cwd)
        if message:
            deny(message)
        if mode == "readonly":
            problem = bash_write_problem(command, cwd)
            if problem:
                deny("Blocked by kit-guard (read-only reviewer): `%s` changes files or git state."
                     " Reviewers report; they do not change anything. Evidence may be written under"
                     " artifacts/. If this command is needed for the check, say so in your report and"
                     " the parent session will run it." % problem)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "scan-repo":
        sys.exit(scan_repo(os.getcwd()))
    if mode not in ("secrets", "readonly"):
        sys.stderr.write("usage: kit-guard.py secrets|readonly|scan-repo\n")
        sys.exit(1)
    try:
        hook(mode)
    except SystemExit:
        raise
    except Exception as exc:        # never lock a session because of a bug here
        sys.stderr.write("kit-guard: internal error, no decision made: %r\n" % (exc,))
    sys.exit(0)


if __name__ == "__main__":
    main()
