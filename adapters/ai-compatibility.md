# AI Compatibility

There is no universal skill-installation standard across every AI product. This repository therefore uses a portable core:

- `SKILL.md`: canonical methodology, with Agent Skills style frontmatter (`name`, `description`) so skill loaders can index it;
- `AGENTS.md`: generic repository-agent instructions;
- `prompts/portable-agent-prompt.md`: fallback prompt for systems that can read GitHub files but do not support skills or instruction files;
- `.claude/commands/casa-audit.md`: thin Claude Code command adapter (copy into the application's `.claude/commands/`);
- `.cursor/rules/casa-readiness.mdc`: thin Cursor adapter (copy into the application's `.cursor/rules/`).

The adapters shipped in this repository only take effect once they are placed inside the **application** repository or the agent's own skills/rules directory. They do nothing while they sit here.

## One-line pointer for instruction-file agents

For agents that read a project-level instruction file (`AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.windsurfrules`, `CLAUDE.md`), add this line to the application's file, adjusting the path to where you cloned the skill:

```text
When performing a CASA, App Defense Alliance or Google OAuth security readiness review, read and follow ../casa-readiness-skill/SKILL.md in full. Do not infer Pass from a clean scanner, do not run runtime tests without authorization, and do not claim certification.
```

## Per-agent notes

| Agent | Discovery mechanism | Notes |
|---|---|---|
| Claude Code | `SKILL.md` under `~/.claude/skills/<name>/` or `<app>/.claude/skills/<name>/` | Clone this repo directly as the skill folder. The `description` frontmatter drives automatic triggering. |
| OpenAI Codex | `AGENTS.md` in the app repo | Use the one-line pointer, or copy this repo's `AGENTS.md`. |
| Cursor | `.cursor/rules/*.mdc` in the app repo | Copy the shipped `.mdc` and fix the path. |
| GitHub Copilot | `.github/copilot-instructions.md` in the app repo | One-line pointer. |
| Gemini CLI | `GEMINI.md` in the app repo | One-line pointer. |
| Windsurf | `.windsurfrules` in the app repo | One-line pointer. |
| Agent Skills loaders (`npx skills add` and similar) | tool-specific skills directory | Install as `casa-readiness`. |
| ChatGPT / browser agents with GitHub access | none | Provide the repository URL and the portable prompt. |

## Capability differences that affect output

The skill asks the agent to discover and use installed document-generation capabilities for the DOCX/PDF report. Where none exist, `references/report-artifact-generation.md` names a plain toolchain fallback (Pandoc, LibreOffice, a headless browser). An agent with no shell at all must record `BLOCKED_RENDERING` rather than fabricate binaries.

The assessment quality still depends on the agent having the necessary repository, shell/scanner and authorized runtime access.
