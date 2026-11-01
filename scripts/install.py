#!/usr/bin/env python3
"""Copy design-agent-kit skills from this local checkout into an agent skills folder.

Standard library only. Copies local files, verifies them by SHA-256 and prints a
JSON receipt to stdout. It never downloads, deletes, overwrites a differing
skill, edits configuration or activates anything. It is not a sandbox: run it
only on directories you control.

Examples:
  python3 scripts/install.py --agent claude --scope project --project /path/to/project --dry-run
  python3 scripts/install.py --agent codex --scope user --home /path/to/home
  python3 scripts/install.py --agent hermes --scope user
  python3 scripts/install.py --agent generic --dest /path/to/folder --skill senior-design-review
"""

import argparse
import hashlib
import json
import os
import re
import sys

KIT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTS = ("claude", "codex", "hermes", "generic")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

EXIT_IO = 1
EXIT_REFUSED = 3


class Refusal(Exception):
    """A safety check failed; nothing should be written."""


def load_manifest(kit_root):
    with open(os.path.join(kit_root, "manifest.json"), encoding="utf-8") as fh:
        return json.load(fh)


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def walk_tree(root):
    """Return {relative posix path: sha256} for a tree, refusing symlinks."""
    files = {}
    if os.path.islink(root):
        raise Refusal("symlink not allowed: %s" % root)
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        for name in sorted(dirnames + filenames):
            full = os.path.join(dirpath, name)
            if os.path.islink(full):
                raise Refusal("symlink not allowed: %s" % full)
        for name in filenames:
            full = os.path.join(dirpath, name)
            if not os.path.isfile(full):
                raise Refusal("not a regular file: %s" % full)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            files[rel] = sha256_file(full)
    return files


def safe_relpath(rel):
    """True for a plain relative POSIX path with no '.', '..' or empty parts."""
    if not isinstance(rel, str) or not rel or "\\" in rel or rel.startswith("/"):
        return False
    if os.path.isabs(rel) or re.match(r"^[A-Za-z]:", rel):
        return False
    return all(part not in ("", ".", "..") for part in rel.split("/"))


def check_manifest_skill(skill):
    """Refuse unsafe manifest entries before any file outside the kit is opened."""
    name = skill.get("name")
    if not isinstance(name, str) or not NAME_RE.match(name) or len(name) > 64:
        raise Refusal("manifest skill name is not a safe token: %r" % (name,))
    if skill.get("path") != "skills/" + name:
        raise Refusal("manifest path for %s must be skills/%s" % (name, name))
    for rel in skill.get("files", []):
        if not safe_relpath(rel):
            raise Refusal("manifest file path escapes the skill folder: %r" % (rel,))


def check_source(kit_root, name):
    """Return kit_root/skills/<name>, refusing symlinks at or below the kit root."""
    skills_dir = os.path.join(kit_root, "skills")
    source = os.path.join(skills_dir, name)
    for path in (skills_dir, source):
        if os.path.islink(path):
            raise Refusal("symlink in source path not allowed: %s" % path)
    if not os.path.isdir(source):
        raise Refusal("source skill folder missing: %s" % source)
    return source


def check_no_symlink_ancestors(path):
    """Refuse if the path or any existing ancestor is a symlink."""
    current = os.path.abspath(path)
    while True:
        if os.path.islink(current):
            raise Refusal("symlink in destination path not allowed: %s" % current)
        parent = os.path.dirname(current)
        if parent == current:
            return
        current = parent


def within(base, target):
    base = os.path.abspath(base)
    target = os.path.abspath(target)
    return os.path.commonpath([base, target]) == base


def require_dir(path, flag):
    if not os.path.isdir(path):
        raise Refusal("%s does not exist or is not a directory: %s" % (flag, path))


def resolve_destination(args, parser, environ):
    """Return the absolute skills directory, enforcing explicit context."""
    if args.dest is not None:
        if args.scope or args.project or args.home:
            parser.error("--dest cannot be combined with --scope, --project or --home")
        return os.path.abspath(args.dest)

    if args.agent == "generic":
        parser.error("--agent generic requires --dest")
    if not args.scope:
        parser.error("--scope project|user (or --dest) is required")

    if args.scope == "project":
        if args.home:
            parser.error("--home is not used with --scope project")
        if args.agent == "hermes":
            parser.error("--agent hermes supports --scope user or --dest only")
        if not args.project:
            parser.error("--scope project requires --project PATH")
        project = os.path.abspath(args.project)
        require_dir(project, "--project")
        sub = ".claude" if args.agent == "claude" else ".agents"
        return os.path.join(project, sub, "skills")

    # user scope
    if args.project:
        parser.error("--project is not used with --scope user")
    if args.home:
        home = os.path.abspath(args.home)
        require_dir(home, "--home")
        sub = {"claude": ".claude", "codex": ".agents", "hermes": ".hermes"}[args.agent]
        return os.path.join(home, sub, "skills")
    if args.agent == "hermes" and environ.get("HERMES_HOME"):
        hermes_home = os.path.abspath(environ["HERMES_HOME"])
        require_dir(hermes_home, "HERMES_HOME")
        return os.path.join(hermes_home, "skills")
    if args.agent == "hermes":
        parser.error("--scope user requires --home PATH (or HERMES_HOME set for hermes)")
    parser.error("--scope user requires --home PATH")


def plan(kit_root, manifest, skills, dest_root):
    """Preflight every skill. Returns a list of plan entries or raises Refusal."""
    for skill in manifest.get("skills", []):
        check_manifest_skill(skill)
    known = {s["name"]: s for s in manifest["skills"]}
    check_no_symlink_ancestors(dest_root)
    if os.path.exists(dest_root) and not os.path.isdir(dest_root):
        raise Refusal("destination exists and is not a directory: %s" % dest_root)

    entries = []
    problems = []
    for name in skills:
        if name not in known:
            raise Refusal("unknown skill: %s (known: %s)" % (name, ", ".join(sorted(known))))
        source = check_source(kit_root, name)
        source_files = walk_tree(source)
        expected = set(known[name]["files"])
        if set(source_files) != expected:
            raise Refusal(
                "source skill %s does not match manifest (missing: %s, extra: %s)"
                % (name, sorted(expected - set(source_files)), sorted(set(source_files) - expected))
            )
        target = os.path.join(dest_root, name)
        if not within(dest_root, target):
            raise Refusal("path escape: %s" % target)
        for rel in source_files:
            if not within(target, os.path.join(target, rel)):
                raise Refusal("path escape: %s" % rel)

        status = "install"
        if os.path.lexists(target):
            if os.path.islink(target) or not os.path.isdir(target):
                problems.append("destination exists and is not a plain directory: %s" % target)
                continue
            try:
                existing = walk_tree(target)
            except Refusal as exc:
                problems.append(str(exc))
                continue
            if existing == source_files:
                status = "already-present"
            else:
                problems.append(
                    "destination skill differs from this kit; refusing to overwrite: %s" % target
                )
                continue
        entries.append({"name": name, "source": source, "target": target,
                        "files": source_files, "status": status})

    if problems:
        raise Refusal("; ".join(problems))
    return entries


def copy_skill(entry):
    for rel in sorted(entry["files"]):
        src = os.path.join(entry["source"], *rel.split("/"))
        dst = os.path.join(entry["target"], *rel.split("/"))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        check_no_symlink_ancestors(os.path.dirname(dst))
        with open(src, "rb") as fin, open(dst, "xb") as fout:
            fout.write(fin.read())
        if sha256_file(dst) != entry["files"][rel]:
            raise OSError("hash mismatch after copy: %s" % dst)


def build_parser():
    parser = argparse.ArgumentParser(
        description="Copy design-agent-kit skills into an explicit destination.")
    parser.add_argument("--agent", required=True, choices=AGENTS)
    parser.add_argument("--scope", choices=("project", "user"))
    parser.add_argument("--project", help="project directory (with --scope project)")
    parser.add_argument("--home", help="home directory (with --scope user)")
    parser.add_argument("--dest", help="explicit skills directory; skill folders are created inside it")
    parser.add_argument("--skill", action="append", dest="skills",
                        help="skill to install; repeatable (default: all skills)")
    parser.add_argument("--dry-run", action="store_true",
                        help="check and report without writing anything")
    return parser


def main(argv=None, environ=None, kit_root=KIT_ROOT):
    environ = os.environ if environ is None else environ
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        manifest = load_manifest(kit_root)
    except (OSError, ValueError) as exc:
        print("install.py: cannot read manifest.json: %s" % exc, file=sys.stderr)
        return EXIT_IO

    try:
        dest_root = resolve_destination(args, parser, environ)
        skills = args.skills or [s.get("name") for s in manifest.get("skills", [])]
        skills = list(dict.fromkeys(skills))
        entries = plan(kit_root, manifest, skills, dest_root)
    except Refusal as exc:
        print("install.py: refused: %s" % exc, file=sys.stderr)
        print("install.py: nothing was written.", file=sys.stderr)
        return EXIT_REFUSED

    if not args.dry_run:
        try:
            for entry in entries:
                if entry["status"] == "install":
                    copy_skill(entry)
                    entry["status"] = "installed"
        except (OSError, Refusal) as exc:
            print("install.py: error while copying: %s" % exc, file=sys.stderr)
            print("install.py: copying is not transactional; files copied before the error "
                  "were left in place. Inspect %s before retrying." % dest_root, file=sys.stderr)
            return EXIT_IO
    else:
        for entry in entries:
            if entry["status"] == "install":
                entry["status"] = "would-install"

    receipt = {
        "kit": manifest["name"],
        "version": manifest["version"],
        "agent": args.agent,
        "dry_run": args.dry_run,
        "destination": dest_root,
        "skills": [
            {
                "name": e["name"],
                "destination": e["target"],
                "status": e["status"],
                "files": [{"path": p, "sha256": e["files"][p]} for p in sorted(e["files"])],
            }
            for e in entries
        ],
    }
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
