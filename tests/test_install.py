"""Tests for scripts/install.py. All writes go to temporary directories."""

import contextlib
import hashlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KIT, "scripts"))
import install  # noqa: E402

with open(os.path.join(KIT, "manifest.json"), encoding="utf-8") as _fh:
    MANIFEST = json.load(_fh)
SKILLS = [s["name"] for s in MANIFEST["skills"]]
FILES = {s["name"]: s["files"] for s in MANIFEST["skills"]}


def run(argv, environ=None, kit_root=KIT):
    """Return (exit code, stdout, stderr). parser.error exits are returned as codes."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = install.main(argv, environ=environ or {}, kit_root=kit_root)
        except SystemExit as exc:
            code = exc.code
    return code, out.getvalue(), err.getvalue()


def snapshot(root):
    """All paths under root with file hashes, to prove nothing was written."""
    seen = {}
    for dirpath, dirnames, filenames in os.walk(root):
        for name in dirnames:
            seen[os.path.relpath(os.path.join(dirpath, name), root)] = "dir"
        for name in filenames:
            full = os.path.join(dirpath, name)
            with open(full, "rb") as fh:
                seen[os.path.relpath(full, root)] = hashlib.sha256(fh.read()).hexdigest()
    return seen


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


class TempCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="dak test ")  # space on purpose
        self.tmp = os.path.realpath(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def mkdir(self, *parts):
        path = os.path.join(self.tmp, *parts)
        os.makedirs(path, exist_ok=True)
        return path

    def fake_kit(self):
        """A copy of the kit's manifest and skills that a test may tamper with."""
        kit = self.mkdir("kit")
        shutil.copy(os.path.join(KIT, "manifest.json"), kit)
        shutil.copytree(os.path.join(KIT, "skills"), os.path.join(kit, "skills"))
        return kit

    def write_manifest(self, kit, manifest):
        with open(os.path.join(kit, "manifest.json"), "w", encoding="utf-8") as fh:
            json.dump(manifest, fh)

    def assert_installed(self, skills_dir, names=SKILLS):
        self.assertEqual(sorted(os.listdir(skills_dir)), sorted(names))
        for name in names:
            for rel in FILES[name]:
                src = os.path.join(KIT, "skills", name, *rel.split("/"))
                dst = os.path.join(skills_dir, name, *rel.split("/"))
                self.assertEqual(sha(src), sha(dst), rel)


class DestinationTests(TempCase):
    def test_claude_project(self):
        project = self.mkdir("my project")
        code, out, _ = run(["--agent", "claude", "--scope", "project", "--project", project])
        self.assertEqual(code, 0)
        self.assert_installed(os.path.join(project, ".claude", "skills"))
        self.assertEqual(json.loads(out)["destination"], os.path.join(project, ".claude", "skills"))

    def test_codex_project_uses_agents_not_codex(self):
        project = self.mkdir("proj")
        code, _, _ = run(["--agent", "codex", "--scope", "project", "--project", project])
        self.assertEqual(code, 0)
        self.assert_installed(os.path.join(project, ".agents", "skills"))
        self.assertFalse(os.path.exists(os.path.join(project, ".codex")))

    def test_user_scope_paths(self):
        for agent, sub in (("claude", ".claude"), ("codex", ".agents"), ("hermes", ".hermes")):
            with self.subTest(agent=agent):
                home = self.mkdir("home " + agent)
                code, _, _ = run(["--agent", agent, "--scope", "user", "--home", home])
                self.assertEqual(code, 0)
                self.assert_installed(os.path.join(home, sub, "skills"))

    def test_hermes_home_env_used_only_for_hermes_user_scope(self):
        hermes_home = self.mkdir("hermes home")
        code, _, _ = run(["--agent", "hermes", "--scope", "user"], environ={"HERMES_HOME": hermes_home})
        self.assertEqual(code, 0)
        self.assert_installed(os.path.join(hermes_home, "skills"))

    def test_explicit_home_overrides_hermes_home(self):
        hermes_home = self.mkdir("env hermes")
        home = self.mkdir("explicit home")
        code, _, _ = run(["--agent", "hermes", "--scope", "user", "--home", home],
                         environ={"HERMES_HOME": hermes_home})
        self.assertEqual(code, 0)
        self.assert_installed(os.path.join(home, ".hermes", "skills"))
        self.assertEqual(os.listdir(hermes_home), [])

    def test_hermes_home_ignored_for_other_agents(self):
        hermes_home = self.mkdir("hermes")
        code, _, _ = run(["--agent", "claude", "--scope", "user"], environ={"HERMES_HOME": hermes_home})
        self.assertEqual(code, 2)
        self.assertEqual(os.listdir(hermes_home), [])

    def test_missing_hermes_home_dir_refused_cleanly(self):
        code, _, err = run(["--agent", "hermes", "--scope", "user"],
                           environ={"HERMES_HOME": os.path.join(self.tmp, "absent")})
        self.assertEqual(code, install.EXIT_REFUSED)
        self.assertIn("HERMES_HOME", err)

    def test_generic_dest(self):
        dest = os.path.join(self.tmp, "offline copy", "skills")
        code, _, _ = run(["--agent", "generic", "--dest", dest])
        self.assertEqual(code, 0)
        self.assert_installed(dest)

    def test_single_skill(self):
        dest = os.path.join(self.tmp, "one")
        code, _, _ = run(["--agent", "generic", "--dest", dest, "--skill", "interactive-mockup"])
        self.assertEqual(code, 0)
        self.assert_installed(dest, ["interactive-mockup"])


class FlagTests(TempCase):
    def assert_usage_error(self, argv, environ=None):
        before = snapshot(self.tmp)
        code, _, _ = run(argv, environ)
        self.assertEqual(code, 2, argv)
        self.assertEqual(snapshot(self.tmp), before)

    def test_dest_conflicts(self):
        dest = os.path.join(self.tmp, "d")
        project = self.mkdir("p")
        for extra in (["--scope", "user"], ["--scope", "project"], ["--project", project], ["--home", project]):
            with self.subTest(extra=extra):
                self.assert_usage_error(["--agent", "claude", "--dest", dest] + extra)

    def test_explicit_context_required(self):
        project = self.mkdir("p")
        self.assert_usage_error(["--agent", "claude"])
        self.assert_usage_error(["--agent", "generic", "--scope", "user", "--home", project])
        self.assert_usage_error(["--agent", "claude", "--scope", "project"])
        self.assert_usage_error(["--agent", "claude", "--scope", "user"])
        self.assert_usage_error(["--agent", "claude", "--scope", "project", "--project", project, "--home", project])
        self.assert_usage_error(["--agent", "claude", "--scope", "user", "--home", project, "--project", project])

    def test_hermes_has_no_project_scope(self):
        project = self.mkdir("p")
        self.assert_usage_error(["--agent", "hermes", "--scope", "project", "--project", project])

    def test_missing_project_dir_refused(self):
        code, _, _ = run(["--agent", "claude", "--scope", "project", "--project", os.path.join(self.tmp, "nope")])
        self.assertEqual(code, install.EXIT_REFUSED)
        self.assertEqual(os.listdir(self.tmp), [])


class BehaviourTests(TempCase):
    def test_dry_run_writes_nothing(self):
        project = self.mkdir("p")
        before = snapshot(self.tmp)
        code, out, _ = run(["--agent", "claude", "--scope", "project", "--project", project, "--dry-run"])
        self.assertEqual(code, 0)
        self.assertEqual(snapshot(self.tmp), before)
        receipt = json.loads(out)
        self.assertTrue(receipt["dry_run"])
        self.assertEqual({s["status"] for s in receipt["skills"]}, {"would-install"})

    def test_receipt_lists_every_file_and_hash(self):
        dest = os.path.join(self.tmp, "d")
        code, out, _ = run(["--agent", "generic", "--dest", dest])
        self.assertEqual(code, 0)
        receipt = json.loads(out)
        self.assertEqual(receipt["version"], MANIFEST["version"])
        for skill in receipt["skills"]:
            self.assertEqual(sorted(f["path"] for f in skill["files"]), sorted(FILES[skill["name"]]))
            for f in skill["files"]:
                self.assertEqual(f["sha256"], sha(os.path.join(dest, skill["name"], f["path"])))
            self.assertTrue(any(p.startswith("references/") for p in FILES[skill["name"]]))
            self.assertTrue(any(p.startswith("templates/") for p in FILES[skill["name"]]))

    def test_identical_copy_is_idempotent(self):
        dest = os.path.join(self.tmp, "d")
        self.assertEqual(run(["--agent", "generic", "--dest", dest])[0], 0)
        before = snapshot(dest)
        code, out, _ = run(["--agent", "generic", "--dest", dest])
        self.assertEqual(code, 0)
        self.assertEqual({s["status"] for s in json.loads(out)["skills"]}, {"already-present"})
        self.assertEqual(snapshot(dest), before)

    def test_different_existing_skill_refused(self):
        dest = os.path.join(self.tmp, "d")
        run(["--agent", "generic", "--dest", dest])
        with open(os.path.join(dest, "senior-design-review", "SKILL.md"), "a", encoding="utf-8") as fh:
            fh.write("\nlocal edit\n")
        before = snapshot(dest)
        code, _, err = run(["--agent", "generic", "--dest", dest])
        self.assertEqual(code, install.EXIT_REFUSED)
        self.assertIn("differs", err)
        self.assertEqual(snapshot(dest), before)

    def test_extra_file_in_existing_skill_refused(self):
        dest = os.path.join(self.tmp, "d")
        run(["--agent", "generic", "--dest", dest])
        with open(os.path.join(dest, "interactive-mockup", "notes.md"), "w", encoding="utf-8") as fh:
            fh.write("mine")
        self.assertEqual(run(["--agent", "generic", "--dest", dest])[0], install.EXIT_REFUSED)

    def test_preflight_across_both_skills(self):
        # The second skill conflicts, so the first must not be copied either.
        dest = self.mkdir("d")
        conflict = os.path.join(dest, "interactive-mockup")
        os.makedirs(conflict)
        with open(os.path.join(conflict, "SKILL.md"), "w", encoding="utf-8") as fh:
            fh.write("someone else's skill")
        before = snapshot(self.tmp)
        code, _, _ = run(["--agent", "generic", "--dest", dest,
                          "--skill", "senior-design-review", "--skill", "interactive-mockup"])
        self.assertEqual(code, install.EXIT_REFUSED)
        self.assertEqual(snapshot(self.tmp), before)
        self.assertFalse(os.path.exists(os.path.join(dest, "senior-design-review")))

    def test_destination_is_a_file_refused(self):
        dest = self.mkdir("d")
        with open(os.path.join(dest, "senior-design-review"), "w", encoding="utf-8") as fh:
            fh.write("x")
        self.assertEqual(run(["--agent", "generic", "--dest", dest])[0], install.EXIT_REFUSED)
        self.assertFalse(os.path.exists(os.path.join(dest, "interactive-mockup")))

    def test_unknown_and_unsafe_skill_names(self):
        dest = os.path.join(self.tmp, "d")
        for name in ("not-a-skill", "../outside", "/abs"):
            with self.subTest(name=name):
                code, _, err = run(["--agent", "generic", "--dest", dest, "--skill", name])
                self.assertEqual(code, install.EXIT_REFUSED)
                self.assertIn("unknown skill", err)
        self.assertFalse(os.path.exists(dest))

    @unittest.skipIf(hasattr(os, "geteuid") and os.geteuid() == 0, "root ignores permissions")
    def test_io_failure_reports_non_transactional(self):
        dest = self.mkdir("readonly")
        os.chmod(dest, 0o500)
        self.addCleanup(os.chmod, dest, 0o700)
        code, out, err = run(["--agent", "generic", "--dest", dest])
        self.assertEqual(code, install.EXIT_IO)
        self.assertEqual(out, "")
        self.assertIn("not transactional", err)


class SymlinkAndEscapeTests(TempCase):
    def test_symlinked_destination_refused(self):
        real = self.mkdir("real")
        link = os.path.join(self.tmp, "link")
        os.symlink(real, link)
        self.assertEqual(run(["--agent", "generic", "--dest", link])[0], install.EXIT_REFUSED)
        self.assertEqual(os.listdir(real), [])

    def test_symlinked_destination_ancestor_refused(self):
        real = self.mkdir("real")
        link = os.path.join(self.tmp, "link")
        os.symlink(real, link)
        dest = os.path.join(link, "nested", "skills")
        self.assertEqual(run(["--agent", "generic", "--dest", dest])[0], install.EXIT_REFUSED)
        self.assertEqual(os.listdir(real), [])

    def test_symlinked_project_skills_dir_refused(self):
        project = self.mkdir("p")
        elsewhere = self.mkdir("elsewhere")
        os.makedirs(os.path.join(project, ".claude"))
        os.symlink(elsewhere, os.path.join(project, ".claude", "skills"))
        code, _, _ = run(["--agent", "claude", "--scope", "project", "--project", project])
        self.assertEqual(code, install.EXIT_REFUSED)
        self.assertEqual(os.listdir(elsewhere), [])

    def test_symlinked_source_skill_dir_refused(self):
        kit = self.fake_kit()
        moved = os.path.join(self.tmp, "moved-skill")
        os.rename(os.path.join(kit, "skills", "senior-design-review"), moved)
        os.symlink(moved, os.path.join(kit, "skills", "senior-design-review"))
        dest = os.path.join(self.tmp, "d")
        code, _, err = run(["--agent", "generic", "--dest", dest], kit_root=kit)
        self.assertEqual(code, install.EXIT_REFUSED)
        self.assertIn("symlink", err)
        self.assertFalse(os.path.exists(dest))

    def test_symlinked_source_skills_ancestor_refused(self):
        kit = self.fake_kit()
        moved = os.path.join(self.tmp, "moved-skills")
        os.rename(os.path.join(kit, "skills"), moved)
        os.symlink(moved, os.path.join(kit, "skills"))
        dest = os.path.join(self.tmp, "d")
        self.assertEqual(run(["--agent", "generic", "--dest", dest], kit_root=kit)[0], install.EXIT_REFUSED)
        self.assertFalse(os.path.exists(dest))

    def test_symlinked_file_inside_source_refused(self):
        kit = self.fake_kit()
        target = os.path.join(kit, "skills", "interactive-mockup", "references", "graft-rules.md")
        os.rename(target, os.path.join(self.tmp, "graft-rules.md"))
        os.symlink(os.path.join(self.tmp, "graft-rules.md"), target)
        dest = os.path.join(self.tmp, "d")
        self.assertEqual(run(["--agent", "generic", "--dest", dest], kit_root=kit)[0], install.EXIT_REFUSED)
        self.assertFalse(os.path.exists(dest))

    def test_malicious_manifest_refused_before_reading_outside(self):
        outside = self.mkdir("outside")
        with open(os.path.join(outside, "SKILL.md"), "w", encoding="utf-8") as fh:
            fh.write("not part of the kit")
        cases = {
            "dotdot name and path": {"name": "../outside", "path": "../outside", "files": ["SKILL.md"]},
            "absolute path": {"name": "senior-design-review", "path": outside, "files": ["SKILL.md"]},
            "path escape with safe name": {"name": "senior-design-review",
                                           "path": "skills/../../outside", "files": ["SKILL.md"]},
            "file escape": {"name": "senior-design-review", "path": "skills/senior-design-review",
                            "files": ["SKILL.md", "../../outside/SKILL.md"]},
            "absolute file": {"name": "senior-design-review", "path": "skills/senior-design-review",
                              "files": [os.path.join(outside, "SKILL.md")]},
        }
        for label, skill in cases.items():
            with self.subTest(label):
                kit = self.fake_kit()
                manifest = json.loads(json.dumps(MANIFEST))
                manifest["skills"][0] = dict(skill)
                self.write_manifest(kit, manifest)
                dest = os.path.join(self.tmp, "d")
                code, _, err = run(["--agent", "generic", "--dest", dest, "--skill", skill["name"]],
                                   kit_root=kit)
                self.assertEqual(code, install.EXIT_REFUSED, err)
                self.assertIn("manifest", err)
                self.assertFalse(os.path.exists(dest))
                shutil.rmtree(kit)

    def test_source_not_matching_manifest_refused(self):
        kit = self.fake_kit()
        os.remove(os.path.join(kit, "skills", "interactive-mockup", "templates", "comparison.html"))
        dest = os.path.join(self.tmp, "d")
        code, _, err = run(["--agent", "generic", "--dest", dest], kit_root=kit)
        self.assertEqual(code, install.EXIT_REFUSED)
        self.assertIn("does not match manifest", err)
        self.assertFalse(os.path.exists(dest))


if __name__ == "__main__":
    unittest.main()
