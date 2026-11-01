# Compatibility

The skills use the Agent Skills layout: a folder containing `SKILL.md` with YAML frontmatter (`name`, `description`, `license`, `metadata.version`) plus supporting files referenced by relative links. Each skill folder is self-contained, so copying just one folder works.

The paths below come from each vendor's public documentation at the time of writing. They are documentation sources, **not** tested support guarantees from this kit. Before claiming a skill is loaded, check in the running agent (for example, ask it to list available skills).

## Claude Code

| Scope | Destination |
| --- | --- |
| Project | `<project>/.claude/skills/<skill-name>/` |
| User | `~/.claude/skills/<skill-name>/` |

Explicit invocation: `/senior-design-review`, `/interactive-mockup`. Documentation: <https://code.claude.com/docs/en/skills>

```sh
python3 scripts/install.py --agent claude --scope project --project /path/to/project
python3 scripts/install.py --agent claude --scope user --home "$HOME"
```

## Codex

| Scope | Destination |
| --- | --- |
| Project | `<project>/.agents/skills/<skill-name>/` |
| User | `~/.agents/skills/<skill-name>/` |

Use `.agents/skills`, not the older `.codex/skills` location. Explicit invocation: `$senior-design-review`, `$interactive-mockup`. Documentation: <https://developers.openai.com/codex/skills/>

```sh
python3 scripts/install.py --agent codex --scope project --project /path/to/project
python3 scripts/install.py --agent codex --scope user --home "$HOME"
```

## Hermes

| Scope | Destination |
| --- | --- |
| User (active home) | `$HERMES_HOME/skills/<skill-name>/` if `HERMES_HOME` is set, otherwise `~/.hermes/skills/<skill-name>/` (the installer needs `--home` for the latter) |
| Named profile | Pass the profile's skills directory explicitly with `--dest` |

Hermes has no project scope. When the bootstrap prompt defaults to project scope, a Hermes agent should load the skills for the session only, or copy them to a project-local folder you have agreed (with `--dest`) and that your Hermes setup is configured to read. It should not silently install into the active profile or `~/.hermes`: that is global and needs your explicit choice.

The installer reads `HERMES_HOME` only when you pass `--agent hermes --scope user` and no `--home`; with neither, it refuses rather than guessing. It never scans or writes to other profiles. Hermes has no project scope in this installer; use `--dest` for anything else. Invoke with natural language, or `/senior-design-review` when installed. Documentation: <https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/>

```sh
python3 scripts/install.py --agent hermes --scope user            # uses $HERMES_HOME (global; explicit choice)
python3 scripts/install.py --agent hermes --scope user --home "$HOME"   # uses ~/.hermes/skills
python3 scripts/install.py --agent generic --dest /path/to/profile/skills
```

## Generic agents (chat-only or no skill folder)

If the agent cannot install skills, attach or paste the relevant `SKILL.md` and the templates/references it links to, and say "follow this skill for this session". This is **session-only** use: nothing persists, and the agent may need reminding in long conversations. No native skill folder is assumed for such agents, including GrokBot-style chat agents.

For an offline copy anywhere:

```sh
python3 scripts/install.py --agent generic --dest /path/to/folder
```

## Automatic triggering

Runtimes decide whether to load a skill from its `description`. That decision is probabilistic and can miss. Naming the skill explicitly is the reliable path. The kit does not require or recommend a particular model.

## Specification

Agent Skills format: <https://agentskills.io/specification>
