# Security

## What the kit is

Plain Markdown and self-contained HTML, plus two optional Python standard-library scripts. There are no install hooks, no package dependencies, no telemetry and no auto-update mechanism.

## Before installing

1. **Review the files.** Read the `SKILL.md` files and their templates. Skills are instructions your agent will follow; treat them like code.
2. **Pin a commit.** Install from a specific, reviewed commit, not a moving branch.
3. **Prefer project scope** until you trust the skills; user scope affects every project.

## What `scripts/install.py` does

- Copies files from this local checkout into a destination you specify explicitly.
- Refuses to run without an explicit destination context (`--agent` with `--scope` and `--project`/`--home`, or `--dest`). It has no current-directory or global default.
- Checks every destination **before** copying anything; if any skill would conflict, nothing is written.
- Refuses an existing destination skill directory whose contents differ. Identical contents are accepted (idempotent).
- Reads each skill only from `skills/<name>` in the kit, where `<name>` must be a lowercase-hyphenated token, and refuses manifest paths that leave the skill folder.
- Refuses symlinks in the source (including `skills/` and the skill folder), destination or destination ancestors, path escapes and unknown skill names.
- Verifies copied files by SHA-256 and prints a JSON receipt to stdout. It does not save the receipt.
- `--dry-run` performs no filesystem writes.
- Copying is not transactional. Conflicts are caught before copying, but an I/O error part-way through (for example, a full disk or a permission change) can leave some files copied. The installer reports this and does not delete them; inspect the destination before retrying.

## What it never does

No `--force`, no deletion, no overwrite, no downloads, no configuration edits, no activation, no network access.

## Limitations

- The installer is **not** a sandbox and does not defend against a hostile filesystem (for example, a path swapped for a symlink between checks and copy). Run it only on directories you control.
- `scripts/validate.py` runs simple pattern checks for obvious private data and secrets. It is defence in depth, **not** comprehensive secret detection.
- The skills ask agents to behave carefully (synthetic data, no publishing), but an agent may still err. Keep your runtime's own permission controls enabled.

## Updating

There is no auto-update. To update: fresh clone or download, review the diff against your pinned commit, then install into a clean destination. The installer will refuse to overwrite a differing existing skill; move or remove the old one yourself after review.

## Reporting a problem

Open an issue on the repository without including secrets or personal data. For a sensitive report, ask in an issue for a private contact route.
