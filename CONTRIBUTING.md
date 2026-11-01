# Contributing

Thank you for helping. Keep the kit small, portable and honest.

## Principles

- **Portable.** No dependency on a specific model, runtime, network service, web font, CDN or private path.
- **Self-contained skills.** Every link inside `skills/<name>/` must resolve when only that folder is copied.
- **Honest claims.** No invented metrics, contrast ratios, user research or runtime-support guarantees.
- **Synthetic data only** in examples and templates. No personal data, credentials or internal hostnames.
- **Standard library only** for scripts.

## Before opening a pull request

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
```

Both must pass. If you add a file to a skill, add it to `manifest.json`.

## Versioning

- Semantic versioning. The version appears in `manifest.json` and in each `SKILL.md` under `metadata.version`; the validator checks they match.
- Record changes in `CHANGELOG.md`.
- Users update by fresh clone and review; the installer refuses to overwrite a differing skill rather than replacing it. Do not add `--force`, auto-update or deletion features.

## Security boundaries for contributions

- No install hooks, post-install scripts or executable files inside `skills/`.
- No telemetry or network calls.
- No configuration edits to any agent runtime.
- Do not claim the installer is a sandbox.

See [docs/security.md](docs/security.md).
