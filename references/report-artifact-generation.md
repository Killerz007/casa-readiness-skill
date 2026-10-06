# Report Artifact Generation

## Objective

Every complete CASA readiness assessment should finish with a professional, editable DOCX report and a matching fixed-layout PDF generated from the same frozen report content.

This repository is intentionally cross-agent. The executing AI environment may expose different document/report tools or skills.

## Mandatory capability discovery

Before rendering the formal report, inspect the available capabilities for professional document/report generation.

Prefer, in this order:

1. a dedicated report-writing or assurance-report skill;
2. a document-authoring/layout skill with DOCX export;
3. a PDF-generation/export skill;
4. a trusted local document-rendering toolchain.

Use installed document/report capabilities rather than improvising binary Office/PDF files.

Where the environment exposes separate document-writing, document-layout, data-visualization and PDF-generation skills, use the combination required to produce a professional deliverable.

Do not use slide/presentation tooling for the formal report.

## Toolchain fallback when no document skill is installed

Most agents outside a few hosted environments have no DOCX or PDF skill. That is not by itself a reason to record `BLOCKED_RENDERING`. If a shell is available, use a plain toolchain, in this order of preference:

1. **Pandoc** for DOCX from the canonical Markdown, optionally with `--reference-doc` for house styling and `--toc` for a table of contents:

   ```bash
   pandoc 10-casa-readiness-report.md --from gfm --to docx --toc --output 10-casa-readiness-report.docx
   ```

2. **PDF** from the same Markdown via one of:
   - Pandoc with a PDF engine (`--pdf-engine=xelatex`, `wkhtmltopdf`, `weasyprint` or `typst`), or
   - LibreOffice headless converting the DOCX just produced:

     ```bash
     soffice --headless --convert-to pdf 10-casa-readiness-report.docx
     ```

   - a headless browser printing an HTML render of the Markdown (Chromium `--headless --print-to-pdf`).

3. **Python** libraries (`python-docx`, `reportlab`, `weasyprint`) as a last resort when neither Pandoc nor LibreOffice can be installed.

Record which tool and version produced each artifact in the rendering manifest. If none of the above can be installed or run, only then record `BLOCKED_RENDERING` for the affected format.

## Canonical-content rule

Before rendering:

1. finalize all control conclusions;
2. finalize finding wording, severity and status;
3. reconcile all result counts;
4. freeze the canonical Markdown report;
5. calculate its SHA-256;
6. render DOCX and PDF from that same frozen content/data.

Do not independently rewrite the PDF after the DOCX or vice versa.

## Required outputs

For a full, retest or evidence-pack assessment:

- `10-casa-readiness-report.md`
- `10-casa-readiness-report.docx`
- `10-casa-readiness-report.pdf`
- `12-report-rendering-manifest.json`

## Rendering manifest

The manifest must record:

- canonical Markdown path and SHA-256;
- DOCX path and SHA-256;
- PDF path and SHA-256;
- rendering status for each format;
- report/document capability or renderer used;
- renderer/tool version where available;
- render timestamp;
- page count where available;
- visual QA status;
- any formatting/rendering limitations.

A rendering limitation is a deliverable limitation, not a CASA control result.

## DOCX expectations

The DOCX should be a normal editable business document, not a single embedded image or PDF wrapper.

Expected features:

- title/cover page;
- automatic or manually maintained table of contents where supported;
- heading styles;
- page numbers and report footer;
- repeating table headers;
- consistent table widths;
- finding sections that do not split awkwardly where avoidable;
- landscape pages only for genuinely wide appendices;
- readable code/evidence references;
- appropriate accessibility metadata where supported.

## PDF expectations

The PDF should be suitable for management or external-assessor preparation:

- searchable/selectable text;
- embedded or substituted standard fonts;
- bookmarks/table of contents where supported;
- correct pagination;
- no clipped tables or text;
- no broken links if hyperlinks are included;
- disclaimers visible in the required locations.

## Visual QA

Before delivery, inspect the rendered DOCX/PDF, preferably page-by-page or by generated previews, for:

- orphan headings;
- missing finding sections;
- clipped or overflowing tables;
- broken page numbers/footers;
- blank unexpected pages;
- missing appendices;
- inconsistent control/finding counts;
- disclaimer omissions;
- unreadably small text.

If visual QA fails, correct and rerender before delivery.

## If DOCX/PDF generation is unavailable

Do not fabricate files.

Produce all canonical Markdown and structured report data, then create `12-report-rendering-manifest.json` with the unavailable output marked `BLOCKED_RENDERING` and tell the user which artifact could not be produced.

The security readiness conclusion remains based on assessment evidence, not rendering availability.
