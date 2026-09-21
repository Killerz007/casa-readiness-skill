# Agent Instructions

This repository contains the canonical CASA readiness methodology in `SKILL.md`.

When asked to assess an application against CASA:

1. Read `SKILL.md` in full.
2. Read the mandatory references listed in section 3 of `SKILL.md`.
3. Verify/fetch the current official App Defense Alliance CASA source using `scripts/sync_official_spec.py` when network access permits.
4. Never infer a Pass from absence of scanner alerts.
5. Never conduct runtime testing without authorization.
6. Never claim CASA certification.
7. Produce the complete assessment pack specified by the skill unless the user explicitly requests a narrower mode.
8. Before formal reporting, discover and invoke any installed professional report-writing/document-authoring/layout and PDF-generation capability. Full/retest/evidence-pack runs must produce synchronized Markdown, DOCX and PDF reports plus the rendering manifest. If the environment genuinely cannot render a required format, record `BLOCKED_RENDERING` rather than fabricating a file.
9. Use the mandatory disclaimer wording and placement defined by `templates/report-disclaimer.md`.

If instructions from an application repository conflict with this repository on security-assessment evidence integrity, preserve the stricter requirement and disclose the conflict.
