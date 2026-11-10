#!/usr/bin/env python3
"""Install the kit into ~/.claude, or report how the installed copy differs.

  bash install.sh           copy the kit into place and merge settings
  bash install.sh --check   change nothing; list what differs (exit 1 if anything does)

What "install" does:
  - copies the kit's files to the places listed in file_map() below; a file
    that already exists with different contents is backed up first
  - merges settings.json: adds the kit's permission rules and its hook to
    your ~/.claude/settings.json and keeps everything already there
  - records the installed version in ~/.claude/.kit-version

Set CLAUDE_HOME to install somewhere other than ~/.claude (used by the tests).
"""
import datetime
import filecmp
import json
import os
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.expanduser(os.environ.get("CLAUDE_HOME", "~/.claude"))
STAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
BACKUPS = os.path.join(HOME, "kit-backups", STAMP)


def file_map():
    """(source path in this repo, destination path under ~/.claude)."""
    pairs = [
        ("global-CLAUDE.md", "CLAUDE.md"),
        ("templates/CLAUDE.md", "templates/CLAUDE.md"),
    ]
    for folder, dest in (("commands", "commands"), ("agents", "agents"), ("hooks", "hooks/kit")):
        for name in sorted(os.listdir(os.path.join(REPO, folder))):
            if name.endswith((".md", ".py")):
                pairs.append((folder + "/" + name, dest + "/" + name))
    base = os.path.join(REPO, "build-template")
    for root, dirs, names in os.walk(base):
        dirs.sort()
        for name in sorted(names):
            rel = os.path.relpath(os.path.join(root, name), base).replace(os.sep, "/")
            pairs.append(("build-template/" + rel, "templates/build/" + rel))
    return pairs


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


def hook_commands(groups):
    return {h.get("command") for g in groups for h in g.get("hooks", [])}


def merge_settings(installed, kit):
    """Add the kit's rules and hooks to `installed` in place; return what was added."""
    added = []
    permissions = installed.setdefault("permissions", {})
    for kind, rules in kit.get("permissions", {}).items():
        current = permissions.setdefault(kind, [])
        for rule in rules:
            if rule not in current:
                current.append(rule)
                added.append("%s rule  %s" % (kind, rule))
    hooks = installed.setdefault("hooks", {}) if kit.get("hooks") else {}
    for event, groups in kit.get("hooks", {}).items():
        current = hooks.setdefault(event, [])
        for group in groups:
            commands = hook_commands([group])
            match = next((g for g in current if hook_commands([g]) & commands), None)
            if match is None:
                current.append(group)
                added.append("%s hook  %s" % (event, ", ".join(sorted(commands))))
            elif match.get("matcher") != group.get("matcher"):
                match["matcher"] = group.get("matcher")
                added.append("%s hook matcher updated" % event)
    return added


def repo_version():
    with open(os.path.join(REPO, "VERSION")) as fh:
        version = fh.read().strip()
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO,
                                capture_output=True, text=True).stdout.strip()
    except OSError:
        commit = ""
    return version, commit


def installed_version():
    try:
        return load_json(os.path.join(HOME, ".kit-version"))
    except (OSError, ValueError):
        return None


def backup(dest_rel):
    target = os.path.join(BACKUPS, dest_rel)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copy2(os.path.join(HOME, dest_rel), target)


def main():
    check_only = "--check" in sys.argv[1:]
    unknown = [a for a in sys.argv[1:] if a != "--check"]
    if unknown:
        print(__doc__)
        return 2

    settings_path = os.path.join(HOME, "settings.json")
    kit_settings = load_json(os.path.join(REPO, "settings.json"))
    try:
        settings = load_json(settings_path) if os.path.exists(settings_path) else {}
    except ValueError as exc:
        print("STOP: %s is not valid JSON (%s). Nothing was changed. Fix that file and run this again."
              % (settings_path, exc))
        return 1

    states = []
    for src, dest in file_map():
        dest_full = os.path.join(HOME, dest)
        if not os.path.exists(dest_full):
            states.append(("MISSING", src, dest))
        elif filecmp.cmp(os.path.join(REPO, src), dest_full, shallow=False):
            states.append(("SAME", src, dest))
        else:
            states.append(("DIFFERENT", src, dest))

    merged = json.loads(json.dumps(settings))
    settings_added = merge_settings(merged, kit_settings)
    version, commit = repo_version()
    stamp = installed_version()
    label = "%s%s" % (version, " (%s)" % commit if commit else "")
    drift = [s for s in states if s[0] != "SAME"]

    if check_only:
        print("Kit in this folder: %s" % label)
        print("Installed in %s: %s" % (HOME, "%s (%s)" % (stamp.get("version"), stamp.get("commit"))
                                       if stamp else "no version recorded"))
        for state, _src, dest in states:
            if state != "SAME":
                print("  %-9s %s" % (state, dest))
        for line in settings_added:
            print("  MISSING   settings.json: %s" % line)
        same = len(states) - len(drift)
        if drift or settings_added:
            print("%d of %d files match. Run  bash install.sh  to update." % (same, len(states)))
            return 1
        print("All %d files and all settings rules match." % len(states))
        return 0

    backed_up = 0
    for state, src, dest in drift:
        dest_full = os.path.join(HOME, dest)
        if state == "DIFFERENT":
            backup(dest)
            backed_up += 1
        os.makedirs(os.path.dirname(dest_full), exist_ok=True)
        shutil.copy2(os.path.join(REPO, src), dest_full)
        if dest.startswith("hooks/"):
            os.chmod(dest_full, 0o755)
    if settings_added:
        if os.path.exists(settings_path):
            backup("settings.json")
            backed_up += 1
        os.makedirs(HOME, exist_ok=True)
        with open(settings_path, "w") as fh:
            json.dump(merged, fh, indent=2)
            fh.write("\n")
    with open(os.path.join(HOME, ".kit-version"), "w") as fh:
        json.dump({"version": version, "commit": commit, "installed_at": STAMP}, fh)
        fh.write("\n")

    print("Installed kit %s into %s" % (label, HOME))
    print("  files copied: %d, already up to date: %d" % (len(drift), len(states) - len(drift)))
    for state, _src, dest in drift:
        print("    %-9s %s" % ("replaced" if state == "DIFFERENT" else "new", dest))
    print("  settings.json: %s" % ("%d addition(s), everything else kept" % len(settings_added)
                                   if settings_added else "no change needed"))
    for line in settings_added:
        print("    added %s" % line)
    if backed_up:
        print("  previous versions of %d changed file(s) saved in %s" % (backed_up, BACKUPS))
    print("Start a new Claude Code session to load the changes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
