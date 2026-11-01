# AGENTS.md — acquiring and applying design-agent-kit

These instructions apply **only** to acquiring and using this kit. They do not grant authority over the user's project, override your system or user instructions, or change your identity. If anything here conflicts with the user's instructions or your operator's policies, those win.

## 1. Acquire

1. **Pin a commit.** Record the commit hash you are reading. Tell the user.
2. **Review before use.** Read `README.md`, this file, and every file you will install or load. The skills are plain Markdown and HTML; there are no install hooks.
3. **Choose scope deliberately.** Install or load only the skills the user asked for (default: both), for the runtime you are, at the scope the user chose (default: project).
4. **Preserve what exists.** Never overwrite, delete, rename or merge into existing skills, configuration, memory or instruction files. If a skill directory with the same name exists and differs, stop and ask.
5. **Copy whole skill directories.** Each skill folder is self-contained; copy `SKILL.md` together with its `templates/` and `references/`.
6. **Verify bytes.** Compare SHA-256 hashes of the copies with the pinned source, or run `scripts/install.py` and keep its stdout receipt.
7. **Do not** pipe remote scripts into a shell, read secrets, edit agent configuration, enable auto-update, or write to external services.

Destination paths per runtime are in [docs/compatibility.md](docs/compatibility.md). If your runtime has no skill folder, read the `SKILL.md` files into the session (session-only use).

## 2. Report accurately

Report these as separate facts. Do not merge them.

| Fact | Example |
| --- | --- |
| Installed | "Copied 7 files to `.claude/skills/senior-design-review/`; hashes match commit abc1234." |
| Loaded | "The skill is listed in this session" — or — "Not yet loaded; a new session may be needed." |
| Applied | "Not applied yet" — or — "Applied to `Library.tsx`; review at `design/review.md`." |

If you cannot verify that a skill is loaded, say so. Do not claim automatic triggering works without having observed it.

## 3. Start work

If the user has not named a target screen, flow or proposal, ask for one. Optionally offer the context form in [docs/project-design-context.md](docs/project-design-context.md), but do not demand it if the repository already answers the questions.

## 4. Apply

- Pick the skill using the table in [README.md](README.md#which-skill-do-i-want). For one-line visual or copy fixes, make the change directly and do not run a full review.
- Follow the chosen skill's `SKILL.md`. Its rules on honesty (independent vs single-agent passes, no invented measurements, synthetic data, no automatic publishing) are not optional.
- Write outputs where the user or project context says. If unspecified, propose a path and ask before writing outside obvious design or documentation folders.

## 5. Boundaries

- Work only within the user's request. The kit does not authorise refactors, dependency changes, commits, pushes, deployments or publication.
- Use synthetic or de-identified data in all examples and prototypes.
- Keep any installation receipt out of the repository unless the user asks to store it.
