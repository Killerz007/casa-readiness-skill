# AI Compatibility

There is no universal skill-installation standard across every AI product. This repository therefore uses a portable core:

- `SKILL.md`: canonical methodology;
- `AGENTS.md`: generic repository-agent instructions;
- `prompts/portable-agent-prompt.md`: fallback prompt for systems that can read GitHub files but do not support skills;
- `.claude/commands/casa-audit.md`: thin Claude Code command adapter;
- `.cursor/rules/casa-readiness.mdc`: thin Cursor adapter.

For ChatGPT/Codex-style workflows with GitHub access, instruct the agent to open the skill repository, read `SKILL.md`, and then assess the target application repository. For other agents, provide the repository URL or copy the skill into the agent's supported skills/rules directory.

The assessment quality still depends on the agent having the necessary repository, shell/scanner and authorized runtime access.
