#!/usr/bin/env python3
"""Static checks for design-agent-kit. Standard library only.

Checks: SKILL.md frontmatter (minimal line-based reading, not a YAML parser),
version consistency, manifest file lists, local Markdown and HTML links
(including Markdown heading fragments), skill self-containment, remote
resources in HTML, symlinks, executable files in skills, and a short list of
private-data patterns.

The pattern checks are defence in depth. They are NOT comprehensive secret or
personal-data detection.

Usage: python3 scripts/validate.py [--root PATH]
"""

import argparse
import fnmatch
import json
import os
import re
import stat
import sys

DEFAULT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths never published (kept in .gitignore) and therefore not scanned.
IGNORED_GLOBS = ("*.private.md", ".agent-handoffs", "__pycache__", "*.pyc", ".git",
                 "receipts", "evidence", ".local", "*.receipt.json")
REQUIRED_GITIGNORE = ("BUILD-CONTRACT.private.md", "BUILD-REPORT.private.md", ".agent-handoffs/")
SKILL_ALLOWED_EXT = (".md", ".html")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_REF_RE = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']""", re.I)
REMOTE_RESOURCE_RES = (
    re.compile(r"""<script[^>]+src\s*=\s*["'](?:https?:)?//""", re.I),
    re.compile(r"""<link[^>]+href\s*=\s*["'](?:https?:)?//""", re.I),
    re.compile(r"""<img[^>]+src\s*=\s*["'](?:https?:)?//""", re.I),
    re.compile(r"""@import\s+(?:url\()?["']?(?:https?:)?//""", re.I),
    re.compile(r"""url\(\s*["']?(?:https?:)?//""", re.I),
)

# (label, regex). Patterns are written so they do not match this file.
PRIVATE_PATTERNS = (
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE" + r" KEY-----")),
    ("AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("API key-like token", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("Slack token", re.compile(r"\bxox[abpr]-[A-Za-z0-9-]{10,}\b")),
    ("email address", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b")),
    ("personal home path", re.compile(r"(?:/home/|/Users/|C:\\Users\\)([A-Za-z0-9._-]+)")),
    ("private network address", re.compile(r"\b(?:10|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}(?:\.\d{1,3})?\b")),
)
# Generic placeholders that are fine in public docs.
ALLOWED_HOME_NAMES = {"user", "username", "you", "me", "example", "name", "your-name", "<user>"}
ALLOWED_EMAILS = {"you@example.com"}


def safe_relpath(rel):
    """True for a plain relative POSIX path with no '.', '..' or empty parts."""
    if not isinstance(rel, str) or not rel or "\\" in rel or rel.startswith("/"):
        return False
    if os.path.isabs(rel) or re.match(r"^[A-Za-z]:", rel):
        return False
    return all(part not in ("", ".", "..") for part in rel.split("/"))


def is_ignored(rel):
    parts = rel.split("/")
    return any(fnmatch.fnmatch(part, g) for part in parts for g in IGNORED_GLOBS)


def list_files(root):
    out = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = [d for d in dirnames
                       if not is_ignored(os.path.relpath(os.path.join(dirpath, d), root).replace(os.sep, "/"))]
        for name in dirnames + filenames:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            if not is_ignored(rel):
                out.append((rel, full))
    return sorted(out)


def read_frontmatter(text):
    """Return (dict of top-level keys, dict of metadata keys) or None.

    Supports only the simple `key: value` form used by this kit plus one
    nested `metadata:` block. Anything else is reported by the caller.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None
    top, meta, in_meta = {}, {}, False
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indented = line.startswith((" ", "\t"))
        key, sep, value = line.strip().partition(":")
        if not sep:
            continue
        value = value.strip().strip('"').strip("'")
        if indented and in_meta:
            meta[key] = value
        else:
            in_meta = key == "metadata" and value == ""
            top[key] = value
    return top, meta


def slugify(heading):
    """GitHub-style heading anchor (close approximation)."""
    text = re.sub(r"`", "", heading.strip().lower())
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def md_anchors(text):
    anchors, counts, in_code = set(), {}, False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        m = None if in_code else re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", line)
        if m:
            slug = slugify(m.group(1))
            n = counts.get(slug, 0)
            anchors.add(slug if n == 0 else "%s-%d" % (slug, n))
            counts[slug] = n + 1
    return anchors


def strip_code(text):
    out, in_code = [], False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            out.append("")
            continue
        out.append("" if in_code else re.sub(r"`[^`]*`", "", line))
    return "\n".join(out)


def check_links(root, rel, text, errors):
    if rel.endswith(".md"):
        targets = MD_LINK_RE.findall(strip_code(text))
    else:
        targets = HTML_REF_RE.findall(text)
    base = os.path.dirname(os.path.join(root, rel))
    skill_root = None
    if rel.startswith("skills/") and rel.count("/") >= 2:
        skill_root = os.path.join(root, *rel.split("/")[:2])
    for target in targets:
        if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("//"):
            continue
        path, _, frag = target.partition("#")
        dest = os.path.normpath(os.path.join(base, path)) if path else os.path.join(root, rel)
        if os.path.commonpath([root, os.path.abspath(dest)]) != root:
            errors.append("%s: link leaves the kit: %s" % (rel, target))
            continue
        if not os.path.exists(dest):
            errors.append("%s: broken link %s" % (rel, target))
            continue
        if skill_root and os.path.commonpath([skill_root, os.path.abspath(dest)]) != os.path.abspath(skill_root):
            errors.append("%s: link leaves the skill folder: %s" % (rel, target))
        if frag and dest.endswith(".md") and os.path.isfile(dest):
            with open(dest, encoding="utf-8") as fh:
                if frag not in md_anchors(fh.read()):
                    errors.append("%s: missing fragment #%s in %s" % (rel, frag, path or rel))


def check_private(rel, text, errors):
    """Report file, line and category only; never echo the matched text."""
    for label, regex in PRIVATE_PATTERNS:
        for m in regex.finditer(text):
            if label == "personal home path" and m.group(1).lower() in ALLOWED_HOME_NAMES:
                continue
            if label == "email address" and m.group(0).lower() in ALLOWED_EMAILS:
                continue
            line = text.count("\n", 0, m.start()) + 1
            errors.append("%s:%d: possible %s" % (rel, line, label))


def validate(root):
    errors = []
    root = os.path.abspath(root)
    try:
        with open(os.path.join(root, "manifest.json"), encoding="utf-8") as fh:
            manifest = json.load(fh)
    except (OSError, ValueError) as exc:
        return ["manifest.json unreadable: %s" % exc], 0
    version = manifest.get("version", "")
    if not re.match(r"^\d+\.\d+\.\d+$", version):
        errors.append("manifest.json: version must be MAJOR.MINOR.PATCH")

    try:
        with open(os.path.join(root, "CHANGELOG.md"), encoding="utf-8") as fh:
            if "## %s" % version not in fh.read():
                errors.append("CHANGELOG.md: no entry for %s" % version)
    except OSError:
        errors.append("CHANGELOG.md missing")

    try:
        with open(os.path.join(root, ".gitignore"), encoding="utf-8") as fh:
            ignore = fh.read().splitlines()
        for entry in REQUIRED_GITIGNORE:
            if entry not in ignore:
                errors.append(".gitignore: must list %s" % entry)
    except OSError:
        errors.append(".gitignore missing")

    for key, rel in manifest.get("docs", {}).items():
        if not safe_relpath(rel):
            errors.append("manifest.json: docs.%s is not a safe relative path" % key)
        elif not os.path.isfile(os.path.join(root, rel)):
            errors.append("manifest.json: docs.%s missing: %s" % (key, rel))

    skills_dir = os.path.join(root, "skills")
    on_disk = sorted(d for d in os.listdir(skills_dir)) if os.path.isdir(skills_dir) else []
    declared = [s.get("name") for s in manifest.get("skills", [])]
    if sorted(declared) != on_disk:
        errors.append("manifest skills %s do not match skills/ folders %s" % (sorted(declared), on_disk))

    for skill in manifest.get("skills", []):
        name = skill.get("name", "")
        if not isinstance(name, str) or not NAME_RE.match(name) or len(name) > 64:
            errors.append("manifest: skill name %r is not a safe lowercase-hyphenated token" % (name,))
            continue
        if skill.get("path") != "skills/" + name:
            errors.append("manifest: skill %s path must be skills/%s" % (name, name))
            continue
        unsafe = [f for f in skill.get("files", []) if not safe_relpath(f)]
        if unsafe:
            errors.append("manifest: skill %s lists %d unsafe file path(s)" % (name, len(unsafe)))
            continue
        sdir = os.path.join(root, "skills", name)
        actual = set()
        for dirpath, _, filenames in os.walk(sdir):
            for fn in filenames:
                actual.add(os.path.relpath(os.path.join(dirpath, fn), sdir).replace(os.sep, "/"))
        if actual != set(skill.get("files", [])):
            errors.append("manifest: skill %s files differ (missing %s, extra %s)" % (
                name, sorted(set(skill.get("files", [])) - actual), sorted(actual - set(skill.get("files", [])))))
        skill_md = os.path.join(sdir, "SKILL.md")
        if not os.path.isfile(skill_md):
            errors.append("%s: SKILL.md missing" % name)
            continue
        with open(skill_md, encoding="utf-8") as fh:
            text = fh.read()
        fm = read_frontmatter(text)
        if fm is None:
            errors.append("%s/SKILL.md: missing or unterminated frontmatter" % name)
            continue
        top, meta = fm
        if top.get("name") != name or not NAME_RE.match(name) or len(name) > 64:
            errors.append("%s/SKILL.md: name must equal folder name and be lowercase-hyphenated" % name)
        desc = top.get("description", "")
        if not desc or len(desc) > 1024:
            errors.append("%s/SKILL.md: description required (max 1024 chars)" % name)
        if top.get("license") != "MIT":
            errors.append("%s/SKILL.md: license must be MIT" % name)
        if meta.get("version") != version:
            errors.append("%s/SKILL.md: metadata.version %r != manifest %r" % (name, meta.get("version"), version))
        for support in skill.get("files", []):
            if support != "SKILL.md" and "](%s" % support not in text:
                errors.append("%s/SKILL.md: does not link support file %s" % (name, support))

    checked = 0
    for rel, full in list_files(root):
        if os.path.islink(full):
            errors.append("%s: symlinks are not allowed" % rel)
            continue
        if os.path.isdir(full):
            continue
        checked += 1
        if rel.startswith("skills/"):
            if not rel.endswith(SKILL_ALLOWED_EXT):
                errors.append("%s: only .md and .html files are allowed in skills/" % rel)
            if os.stat(full).st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
                errors.append("%s: executable files are not allowed in skills/" % rel)
        if rel.endswith(".png") and not rel.startswith("skills/"):
            # Documentation screenshots: must be real PNG files; no text checks apply.
            with open(full, "rb") as fh:
                if fh.read(8) != b"\x89PNG\r\n\x1a\n":
                    errors.append("%s: not a valid PNG file" % rel)
            continue
        try:
            with open(full, encoding="utf-8") as fh:
                text = fh.read()
        except UnicodeDecodeError:
            errors.append("%s: not UTF-8 text" % rel)
            continue
        # HTML templates link to placeholder files the user will create.
        is_html_template = rel.endswith(".html") and "/templates/" in rel
        if rel.endswith((".md", ".html")) and not is_html_template:
            check_links(root, rel, text, errors)
        if rel.endswith(".html"):
            for regex in REMOTE_RESOURCE_RES:
                if regex.search(text):
                    errors.append("%s: remote resource reference (must be self-contained)" % rel)
                    break
        check_private(rel, text, errors)
    return errors, checked


def main(argv=None):
    parser = argparse.ArgumentParser(description="Static checks for design-agent-kit.")
    parser.add_argument("--root", default=DEFAULT_ROOT, help="kit root (default: this checkout)")
    args = parser.parse_args(argv)
    errors, checked = validate(args.root)
    for err in errors:
        print("FAIL: %s" % err)
    if errors:
        print("%d problem(s) found in %d files." % (len(errors), checked))
        return 1
    print("OK: %d files checked. Pattern checks are defence in depth, not comprehensive secret detection." % checked)
    return 0


if __name__ == "__main__":
    sys.exit(main())
