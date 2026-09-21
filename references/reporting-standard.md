# Professional Reporting Standard

Reports should resemble a mature external assurance deliverable in structure and discipline without implying affiliation with any accounting, consulting or certification firm.

## Style

- factual, concise and evidence-led;
- clear distinction between criteria, procedure, observation, risk and recommendation;
- no marketing language;
- no unsupported statements such as "fully secure";
- no invented management responses;
- tables for control matrices and registers, prose for analysis;
- consistent finding IDs, severity labels and statuses;
- explicit limitations and non-certification statement.

## Executive summary

Include:

- purpose and scope;
- application/environment/commit assessed;
- CASA version and provenance;
- procedures performed;
- control results by status;
- findings by severity;
- key themes;
- readiness conclusion;
- material limitations.

## Adjudication and engineering traceability

The formal report should disclose material adjudications that changed or confirmed a control/finding conclusion. Summarize the disputed evidence, final decision and limitations without reproducing the entire internal review log.

For each open finding, include the stable regression key and any external GitHub/Jira work-item reference that was created. Work-item status is project-management context only; security closure remains based on retest evidence.

When the run is a regression/CI assessment, include a prominent limitation that a regression PASS is not a fresh full CASA readiness conclusion.

## Detailed finding structure

**Finding ID and title**

**Rating / Status**

**CASA criteria**

**Affected components**

**Audit Finding**: objective condition and evidence.

**Risk and Implication**: credible impact tied to the application.

**Recommendation**: specific corrective action.

**Implementation Guidance**: stack-specific examples/locations where supported.

**Retest Criteria**: exact condition/procedure required for closure.

**Evidence References**: indexed artifacts.

## Formal caveat

Every final report must state that it is a readiness/pre-assessment review and is not an App Defense Alliance laboratory certification or Google approval.


## Mandatory deliverable formats

For full, retest and evidence-pack assessments, the formal report must be delivered as:

- `10-casa-readiness-report.md` — canonical report source;
- `10-casa-readiness-report.docx` — professionally formatted editable report;
- `10-casa-readiness-report.pdf` — fixed-layout distribution copy;
- `12-report-rendering-manifest.json` — rendering provenance and hashes.

The DOCX and PDF must contain the same substantive content, findings, counts, conclusion and disclaimers as the canonical Markdown source. Differences may be limited to pagination, table splitting, typography and other presentation mechanics.

## Mandatory disclaimer placement

Use the approved language in `templates/report-disclaimer.md`.

The full disclaimer belongs on the cover or immediately following it. A concise reliance/non-certification reminder belongs in the executive summary and conclusion. The footer must carry a short non-certification notice.

Do not describe the review as an audit opinion, attestation, certification, Google verification, ADA approval or laboratory assessment unless that status is factually supported by an authorized external issuer.

## Reliance wording

The report must state that conclusions:

- are limited to the scoped application, pinned commit/version, environment, evidence and procedures performed;
- speak only as of the assessment date;
- may change if the application, infrastructure, integrations or official CASA criteria change;
- do not guarantee the absence of undiscovered vulnerabilities or future compromise;
- do not bind Google, the App Defense Alliance or an authorized lab;
- do not replace official assessment evidence where an external assessor is required.
