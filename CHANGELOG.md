# Changelog

## 1.3.0 - 2026-10-06

- **Fixed:** the test-guide parser ignored the official `*AL1 and AL2*` shared heading, leaving 8 of 48 controls (1.1.1, 1.1.3, 1.3.1, 3.1.6, 3.3.1, 6.5.1, 6.6.1, 6.7.1) with empty AL2 procedure/verification text in `references/casa-test-cases.generated.json`. Shared blocks now populate both levels, and trailing `---` separators are stripped. Catalogue regenerated.
- Sync now refuses to write a catalogue with empty AL2 data; validator and a new test parse the pinned official files on every run.
- Added `scripts/sync_official_spec.py --rebuild-local` (offline catalogue rebuild) and `--summary-json` (machine-readable CI summary); monthly workflow uses it instead of parsing the log.
- Added `examples/sample-assessment/`, a fictional 48-control evidence pack used by tests and usable as a trial regression baseline.
- README and `adapters/ai-compatibility.md` now give per-agent install locations (Claude Code, Codex, Cursor, Copilot, Gemini CLI, Windsurf, generic skill loaders) and state that shipped adapters must be copied into the application repository.
- `SKILL.md` description now lists trigger terms; required reading is mode-specific and points at the per-control JSON instead of the full test guide.
- Report generation documents a Pandoc/LibreOffice/headless-browser fallback so agents without a document skill can still produce DOCX/PDF.
- Assessment manifest records the pinned specification/test-guide SHA-256 and release URL.
- `control-test-strategy.json` carries the shared minimum rule once at top level.

## 1.2.0 - 2026-09-21

- Improved repository discovery and onboarding with a focused Google CASA/AL2 quick start, terminology FAQ and sanitized assessment example.
- Added a formal evidence-adjudication stage with independent-review guidance, structured adjudication records and control/finding traceability.
- Added stable finding regression keys and a structured findings register for cross-release matching.
- Added CASA regression CI methodology, comparison tooling, reusable workflow template and tests.
- Added portable finding-to-ticket queue generation for GitHub/Jira workflows.
- Added explicit external-ticket authorization and deduplication requirements; ticket closure does not equal security closure.
- Extended formal reports to include adjudication, regression/baseline status and work-item traceability.

## 1.1.0 - 2026-09-21

- Made Markdown, DOCX and PDF formal reports mandatory for full, retest and evidence-pack assessments.
- Added mandatory discovery/invocation of installed professional report-writing, document-layout and PDF-generation capabilities.
- Added cross-format consistency, rendering provenance and visual-QA requirements.
- Added a report-rendering manifest schema/template.
- Added comprehensive independent-assessment, non-affiliation, non-certification, scope/reliance and no-security-guarantee disclaimers with mandatory cover, executive-summary, conclusion and footer placement.

## 1.0.0 - 2026-09-21

- Initial public skill architecture.
- Pinned CASA component baseline v2.1.1 (2026-06-03) from ASA-WG release v2.2.0.
- Added 48-control catalogue, formal assessment workflow, evidence standards, scanner guidance, safe-testing guardrails, Google OAuth review, report templates and monthly upstream synchronization workflow.
