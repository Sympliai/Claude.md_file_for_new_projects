#!/usr/bin/env python3
"""Tests for hooks/kit-guard.py. Run: python3 tests/test_kit_guard.py

Each case feeds the hook the same JSON Claude Code sends before a tool call
and checks whether the hook blocks it. Sample keys are assembled at run time
so this file never contains a key-shaped string.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARD = os.path.join(ROOT, "hooks", "kit-guard.py")

FAKE_AWS = "AKIA" + "ABCDEFGHIJKLMNOP"
FAKE_SK = "sk-" + "proj-" + "a1B2c3D4e5F6g7H8i9J0k1L2m3N4"
FAKE_STRIPE = "sk_" + "live_" + "abcdefghijklmnop1234"


def run_hook(mode, tool, tool_input, cwd=None):
    event = {"tool_name": tool, "tool_input": tool_input, "cwd": cwd or ROOT}
    result = subprocess.run([sys.executable, GUARD, mode], input=json.dumps(event),
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    if not result.stdout.strip():
        return None
    return json.loads(result.stdout)["hookSpecificOutput"]["permissionDecisionReason"]


def bash(mode, command, cwd=None):
    return run_hook(mode, "Bash", {"command": command}, cwd)


class SecretFiles(unittest.TestCase):
    def test_file_tools_blocked_on_secret_files(self):
        for path in (".env", ".env.local", "apps/web/.env.production", "/abs/proj/.env.staging",
                     ".envrc", "PROJECT KEYS/stripe.txt", "Project Keys/notes.md"):
            for tool in ("Read", "Edit", "Write"):
                self.assertIsNotNone(run_hook("secrets", tool, {"file_path": path}), (tool, path))

    def test_file_tools_allowed_elsewhere(self):
        for path in (".env.example", "src/env.ts", "docs/environment.md", ".gitignore",
                     "src/config/.environment/readme.md"):
            self.assertIsNone(run_hook("secrets", "Read", {"file_path": path}), path)

    def test_grep(self):
        self.assertIsNotNone(run_hook("secrets", "Grep", {"pattern": "KEY", "path": ".env.local"}))
        self.assertIsNotNone(run_hook("secrets", "Grep", {"pattern": "KEY", "glob": "**/.env*"}))
        self.assertIsNone(run_hook("secrets", "Grep", {"pattern": r"\.env", "path": ".gitignore"}))
        self.assertIsNone(run_hook("secrets", "Grep", {"pattern": "process.env", "glob": "*.ts"}))

    def test_bash_blocked(self):
        for command in (
            "cat .env",
            "cat apps/web/.env.local | head -3",
            "head -n 5 .env.production",
            "grep SUPABASE .env.local",
            "source .env && npm run dev",
            "export $(cat .env | xargs)",
            "echo \"$(cat .env.local)\"",
            "python3 -c \"print(open('.env').read())\"",
            "cp .env.local /tmp/copy.txt",
            "git add .env.local",
            "git show HEAD:.env",
            "git log -p -- .env",
            "docker compose --env-file=.env.staging up",
            "echo 'KEY=1' > .env.local",
            "cat > .env.local <<EOF\nKEY=1\nEOF",
            "cat 'PROJECT KEYS/stripe.txt'",
            "cat .env*",
            "python3 <<EOF\nprint(open('.env').read())\nEOF",
            "cat <<'EOF' | python3\nprint(open('.env').read())\nEOF",
        ):
            self.assertIsNotNone(bash("secrets", command), command)

    def test_bash_allowed(self):
        for command in (
            "cat .env.example",
            "ls -la .env*",
            "test -f .env.local && echo present",
            "[ -f .env ] || echo missing",
            "git check-ignore -v .env.local",
            "git rm --cached .env",
            "git log --all --oneline -- .env",
            "git status --short",
            "grep -rn 'process.env.API_URL' src",
            "node -e \"console.log(import.meta.env)\"",
            "echo 'Put the key in .env.local, then restart'",
            "npm run build",
            "git commit -m 'docs: explain where .env.local values go (not in git)'",
            "git commit -m \"$(cat <<'EOF'\nfeat: read config\n\nValues live in .env.local only.\nEOF\n)\"",
        ):
            self.assertIsNone(bash("secrets", command), command)


class CommitScan(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = self.tmp.name
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test")
        self.write("README.md", "hello\n")
        self.git("add", "README.md")
        self.git("commit", "-q", "-m", "init")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args):
        subprocess.run(["git"] + list(args), cwd=self.repo, check=True, capture_output=True)

    def write(self, name, text):
        with open(os.path.join(self.repo, name), "w") as fh:
            fh.write(text)

    def test_clean_commit_passes(self):
        self.write("app.js", "const url = process.env.API_URL;\n")
        self.git("add", "app.js")
        self.assertIsNone(bash("secrets", "git commit -m 'feat: add app'", self.repo))

    def test_staged_key_blocks_and_value_is_not_echoed(self):
        self.write("config.js", "const a = 1;\nconst key = '%s';\n" % FAKE_AWS)
        self.git("add", "config.js")
        reason = bash("secrets", "git commit -m 'feat: config'", self.repo)
        self.assertIn("config.js:2", reason)
        self.assertIn("AWS access key", reason)
        self.assertNotIn(FAKE_AWS, reason)

    def test_add_and_commit_in_one_command_scans_untracked(self):
        self.write("client.ts", "export const k = '%s'\n" % FAKE_SK)
        reason = bash("secrets", "git add -A && git commit -m 'feat: client'", self.repo)
        self.assertIn("client.ts:1", reason)

    def test_commit_all_scans_unstaged(self):
        self.write("README.md", "hello\npay = '%s'\n" % FAKE_STRIPE)
        self.assertIsNone(bash("secrets", "git commit -m 'docs: readme'", self.repo))
        self.assertIn("Stripe", bash("secrets", "git commit -am 'docs: readme'", self.repo))

    def test_key_file_name_blocks(self):
        self.write("server.pem", "not really a key\n")
        self.git("add", "server.pem")
        self.assertIn("key file", bash("secrets", "git commit -m 'chore: cert'", self.repo))

    def test_allow_marker(self):
        self.write("fixture.js", "const fake = '%s'; // secret-scan:allow\n" % FAKE_AWS)
        self.git("add", "fixture.js")
        self.assertIsNone(bash("secrets", "git commit -m 'test: fixture'", self.repo))

    def test_scan_repo_reports_location_only(self):
        self.write("old.js", "const key = '%s';\n" % FAKE_AWS)
        self.git("add", "old.js")
        self.git("commit", "-q", "-m", "add old")
        result = subprocess.run([sys.executable, GUARD, "scan-repo"], cwd=self.repo,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("old.js:1", result.stdout)
        self.assertNotIn(FAKE_AWS, result.stdout)


class ReadOnlyReviewer(unittest.TestCase):
    def test_blocked(self):
        for command in (
            "rm -rf dist",
            "mv a.ts b.ts",
            "git add -A",
            "git commit -m 'x'",
            "git checkout -- src/app.ts",
            "git stash",
            "git push origin main",
            "git -C . reset --hard",
            "git branch -D old",
            "sed -i '' 's/a/b/' src/app.ts",
            "echo fixed > src/app.ts",
            "npm install left-pad",
            "npm audit fix",
            "cp src/a.ts src/b.ts",
            "mkdir src/new",
            "bash -c 'rm x'",
            "python3 -c \"open('x','w').write('1')\"",
            "find . -name '*.log' -delete",
            "npm test && rm -rf coverage",
            "cat .env.local",
        ):
            self.assertIsNotNone(bash("readonly", command), command)

    def test_allowed(self):
        for command in (
            "git diff main...HEAD",
            "git log --oneline -20",
            "git status --short",
            "git branch --show-current",
            "git stash list",
            "git diff main...HEAD > artifacts/phase-01/changes.diff",
            "npm test",
            "npm run typecheck 2>&1 | tail -20",
            "npx playwright test e2e/login.spec.ts",
            "maestro test .maestro/add-tree.yaml",
            "mkdir -p artifacts/phase-02/defects",
            "cp /tmp/shot.png artifacts/phase-02/defects/login.png",
            "xcrun simctl io booted screenshot artifacts/phase-02/defects/home.png",
            "curl -s http://localhost:5173/api/health",
            "npm audit --omit=dev > /dev/null",
            "ls -la src && cat package.json",
        ):
            self.assertIsNone(bash("readonly", command), command)

    def test_secrets_mode_does_not_apply_readonly_rules(self):
        self.assertIsNone(bash("secrets", "rm -rf dist"))


class Robustness(unittest.TestCase):
    def test_bad_input_never_blocks(self):
        result = subprocess.run([sys.executable, GUARD, "secrets"], input="not json",
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "")


if __name__ == "__main__":
    unittest.main(verbosity=1)
