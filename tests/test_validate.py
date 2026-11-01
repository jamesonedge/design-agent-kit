"""Tests for scripts/validate.py. Each case runs on a temporary copy of the kit."""

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KIT, "scripts"))
import validate  # noqa: E402

# Marker fragments are joined at runtime so this file does not trip the
# validator's own pattern checks.
SYNTHETIC_EMAIL = "synthetic.person" + "@" + "example-mail" + ".test"
SYNTHETIC_KEY_ID = "AK" + "IA" + "Q" * 16


class ValidateTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="dak-validate-")
        self.addCleanup(self._tmp.cleanup)
        self.root = os.path.join(os.path.realpath(self._tmp.name), "kit")
        shutil.copytree(KIT, self.root, ignore=shutil.ignore_patterns(
            "*.private.md", "__pycache__", ".git"))

    def path(self, rel):
        return os.path.join(self.root, *rel.split("/"))

    def append(self, rel, text):
        with open(self.path(rel), "a", encoding="utf-8") as fh:
            fh.write(text)

    def replace(self, rel, old, new):
        with open(self.path(rel), encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn(old, text)
        with open(self.path(rel), "w", encoding="utf-8") as fh:
            fh.write(text.replace(old, new))

    def manifest(self):
        with open(self.path("manifest.json"), encoding="utf-8") as fh:
            return json.load(fh)

    def errors(self):
        return validate.validate(self.root)[0]

    def assert_error(self, fragment):
        errors = self.errors()
        self.assertTrue(any(fragment in e for e in errors), errors)
        return errors

    def test_actual_kit_is_clean(self):
        errors, checked = validate.validate(KIT)
        self.assertEqual(errors, [])
        self.assertGreater(checked, 0)

    def test_clean_copy_succeeds_via_main(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = validate.main(["--root", self.root])
        self.assertEqual(code, 0, out.getvalue())
        self.assertIn("not comprehensive", out.getvalue())

    def test_fake_png_rejected(self):
        with open(self.path("docs/images/fake.png"), "wb") as fh:
            fh.write(b"not a png")
        self.assert_error("not a valid PNG file")

    def test_png_in_skills_rejected(self):
        shutil.copy(self.path("docs/images/example-before.png"),
                    self.path("skills/interactive-mockup/x.png"))
        self.assert_error("only .md and .html files are allowed in skills/")

    def test_missing_doc(self):
        os.remove(self.path("docs/security.md"))
        self.assert_error("docs.security missing")

    def test_missing_support_file(self):
        os.remove(self.path("skills/senior-design-review/references/review-lenses.md"))
        self.assert_error("files differ")

    def test_unlisted_support_file(self):
        self.append("skills/interactive-mockup/templates/extra.md", "# Extra\n")
        self.assert_error("files differ")

    def test_broken_link(self):
        self.append("docs/prompts.md", "\n[gone](missing-file.md)\n")
        self.assert_error("broken link missing-file.md")

    def test_missing_fragment(self):
        self.append("docs/prompts.md", "\n[gone](compatibility.md#no-such-heading)\n")
        self.assert_error("missing fragment")

    def test_link_leaving_skill_folder(self):
        self.append("skills/senior-design-review/SKILL.md", "\n[x](../../README.md)\n")
        self.assert_error("leaves the skill folder")

    def test_changelog_version_mismatch(self):
        manifest = self.manifest()
        self.replace("CHANGELOG.md", "## %s" % manifest["version"], "## 9.9.9")
        self.assert_error("CHANGELOG.md: no entry")

    def test_skill_version_mismatch(self):
        manifest = self.manifest()
        self.replace("skills/interactive-mockup/SKILL.md",
                     "version: \"%s\"" % manifest["version"], "version: \"9.9.9\"")
        self.assert_error("metadata.version")

    def test_remote_resource_in_html(self):
        self.append("examples/reading-list/comparison.html",
                    '\n<script src="https://cdn.example/x.js"></script>\n')
        self.assert_error("remote resource")

    def test_symlink_rejected(self):
        os.symlink(self.path("README.md"), self.path("docs/link.md"))
        self.assert_error("symlinks are not allowed")

    def test_private_patterns_report_location_not_content(self):
        self.append("docs/prompts.md", "\nContact " + SYNTHETIC_EMAIL + "\n")
        self.append("docs/security.md", "\nkey " + SYNTHETIC_KEY_ID + "\n")
        errors = self.errors()
        joined = "\n".join(errors)
        self.assertTrue(any(e.startswith("docs/prompts.md:") and "email address" in e for e in errors), errors)
        self.assertTrue(any(e.startswith("docs/security.md:") and "AWS access key id" in e for e in errors), errors)
        self.assertNotIn(SYNTHETIC_EMAIL, joined)
        self.assertNotIn(SYNTHETIC_KEY_ID, joined)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            validate.main(["--root", self.root])
        self.assertNotIn(SYNTHETIC_EMAIL, out.getvalue())
        self.assertNotIn(SYNTHETIC_KEY_ID, out.getvalue())

    def test_placeholder_paths_allowed(self):
        self.append("docs/prompts.md", "\nUse /path/to/project or /home/user/project.\n")
        self.assertEqual(self.errors(), [])

    def test_unsafe_manifest_paths_fail_closed(self):
        outside = os.path.join(os.path.dirname(self.root), "outside")
        os.makedirs(outside)
        manifest = self.manifest()
        manifest["skills"][0]["path"] = "../outside"
        manifest["skills"][1]["files"].append("../../outside/x.md")
        manifest["docs"]["security"] = "../outside/x.md"
        with open(self.path("manifest.json"), "w", encoding="utf-8") as fh:
            json.dump(manifest, fh)
        errors = self.errors()
        self.assertTrue(any("path must be skills/" in e for e in errors), errors)
        self.assertTrue(any("unsafe file path" in e for e in errors), errors)
        self.assertTrue(any("docs.security is not a safe relative path" in e for e in errors), errors)

    def test_unsafe_manifest_name(self):
        manifest = self.manifest()
        manifest["skills"][0]["name"] = "../outside"
        with open(self.path("manifest.json"), "w", encoding="utf-8") as fh:
            json.dump(manifest, fh)
        self.assert_error("not a safe lowercase-hyphenated token")


if __name__ == "__main__":
    unittest.main()
