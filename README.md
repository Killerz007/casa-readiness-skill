# Google CASA Readiness Skill

An open-source AI-agent skill for preparing web applications and APIs for **Google OAuth security review** and the **App Defense Alliance CASA AL2 lab assessment**. It turns code review, authorized runtime testing and scanner output into control-by-control evidence, remediation guidance, regression checks, ticket-ready findings and synchronized Markdown, DOCX and PDF reports.

> **Status:** community project. Not affiliated with, endorsed by, or an approved laboratory of Google or the App Defense Alliance. It does not issue CASA certification.

## What this repository does

The skill gives an AI coding/security agent a controlled methodology for:

- determining whether an application's Google OAuth usage may trigger additional verification or security assessment requirements;
- establishing the exact CASA specification version used for the review;
- scoping first-party and applicable third-party components;
- inspecting source code, architecture, authentication, authorization, sessions, OAuth, secrets, cryptography, input handling, dependencies, configuration and data flows;
- orchestrating SAST, secret, dependency, configuration and DAST tooling where available;
- executing the applicable CASA AL2 test procedures in a controlled, authorized test environment;
- producing control-by-control evidence and defensible Pass / Fail / N/A / Blocked conclusions;
- formally adjudicating conflicts between scanners, source review, runtime testing and reviewers;
- documenting findings with stable regression keys, severity, evidence, reproduction steps, CASA mapping, CWE mapping, remediation and retest criteria;
- comparing future commits against an accepted CASA readiness baseline through optional regression CI;
- generating a portable GitHub/Jira-ready finding queue and, when explicitly authorized, creating/updating external work items;
- producing a formal assurance-style report and evidence index suitable for management review and external-assessor preparation;
- automatically rendering the final report as synchronized Markdown, DOCX and PDF using the executing AI environment's professional report/document-generation capabilities;
- tracking official CASA specification changes monthly and opening a review pull request when released CASA material changes.

## Current pinned CASA baseline

The repository is initially pinned to **CASA v2.1.1 (2026-06-03)**. The latest upstream repository release at the time this project was prepared is **ASA-WG v2.2.0**, which explicitly states that CASA itself remains v2.1.1.

The source of truth is always the App Defense Alliance repository:

- `appdefensealliance/ASA-WG/CASA/CASA Specification.md`
- `appdefensealliance/ASA-WG/CASA/CASA Test Guide.md`
- `appdefensealliance/ASA-WG/CASA/ADA Burp Audit Scan Configuration.json`

See `official/upstream-manifest.json` for the pinned provenance.

## Quick start

1. Clone this repository next to the application you want to review:

   ```bash
   git clone https://github.com/Killerz007/casa-readiness-skill.git
   ```

2. Give your AI coding/security agent access to both repositories, then ask:

   ```text
   Use the CASA Readiness Skill from this repository to perform a complete CASA readiness assessment of this application. Follow SKILL.md exactly. Use the latest released App Defense Alliance CASA specification, preserve raw scan evidence, and produce the complete formal assessment package. Do not claim certification.
   ```

3. If the agent supports repository skills, point it directly at [`SKILL.md`](SKILL.md). Otherwise, use the [`portable-agent-prompt.md`](prompts/portable-agent-prompt.md).

Dynamic testing is performed only against targets the operator is authorized to test. A source/configuration-only review can still proceed, with unsupported runtime conclusions marked Blocked.

## Expected output

Each assessment creates a dedicated evidence pack, for example:

```text
casa-assessment/
  2026-09-21-project-name/
    00-assessment-manifest.json
    01-executive-summary.md
    02-scope-and-architecture.md
    03-google-oauth-assessment.md
    04-casa-control-matrix.csv
    04-adjudication-log.jsonl
    05-findings-register.jsonl
    05-detailed-findings.md
    06-remediation-register.csv
    07-retest-results.md
    08-scanner-register.csv
    09-evidence-index.csv
    10-casa-readiness-report.md
    10-casa-readiness-report.docx
    10-casa-readiness-report.pdf
    11-test-procedure-traceability.csv
    12-report-rendering-manifest.json
    13-finding-ticket-queue.json
    13-finding-ticket-queue.md
    14-regression-summary.json   # regression mode / CI
    14-regression-summary.md     # regression mode / CI
    evidence/
      raw/
      normalized/
      screenshots/
      runtime/
      code/
```

The report conclusion must use readiness language such as **Ready for independent CASA assessment**, **Not ready**, or **Assessment incomplete**. It must never state that the application is CASA certified unless an authorized external body has actually issued that certification.

For full assessments, the AI must first discover and use an available professional report-writing/document-layout capability to generate the DOCX and PDF from the same frozen report content. The report includes mandatory independent-assessment, non-affiliation, non-certification, scope/reliance and no-security-guarantee disclaimers. See `references/report-artifact-generation.md` and `templates/report-disclaimer.md`.

## Sanitized example assessment

The [sanitized assessment summary](examples/sanitized-assessment-summary.md) shows the shape of a completed review: pinned scope and criteria, control totals, an evidence-linked finding, remediation and the permitted readiness conclusion. It is fictional and does not represent a certification or a completed assessment of any real application.

## FAQ

### What is Google CASA?

CASA originated as the Cloud Application Security Assessment program. The current App Defense Alliance specification continues those application-security requirements under the ADA certification scheme. Google may use CASA as part of an application's OAuth verification or security-assessment pathway, but Google determines the pathway for each application.

### Is “Tier 2” or “T2” the same as AL2?

“Tier 2” and “T2” are legacy CASA terms. The current specification uses **ADA Assurance Level 2 (AL2)** for a lab assessment in which an ADA-approved lab evaluates the applicable audit test cases directly against the application. When an older request says T2, confirm the exact current requirement with Google or the assigned lab rather than assuming the terminology is interchangeable in every context.

### What does AL2 mean for this skill?

The skill prepares the application and evidence package against the current AL2 procedures. It can identify gaps and rehearse applicable tests, but its results remain an independent readiness assessment. Only an authorized lab can perform and issue the official lab assessment.

### Does using sensitive or restricted Google OAuth scopes automatically require AL2?

No. Scope classification alone does not establish the assessment path. The application's scopes, data use and architecture inform Google's verification decision; Google and the authorized lab determine the actual requirements.

### Does this replace an authorized CASA lab or grant Google OAuth verification?

No. It does not replace a laboratory assessment and cannot grant CASA certification, an assurance level, Google OAuth verification or Google approval. It is preparation material designed to make an eventual independent assessment more complete and reproducible.

## Monthly upstream tracking

`.github/workflows/monthly-casa-upstream-sync.yml` runs on the first day of each month. It:

1. checks the latest published `appdefensealliance/ASA-WG` release;
2. fetches the released CASA specification, test guide and ADA Burp configuration;
3. extracts the CASA component version and control catalogue;
4. compares file hashes and control/test-case mappings against the pinned baseline;
5. validates the generated catalogue;
6. opens a pull request if released CASA material has changed;
7. opens an issue instead if the upstream format changed and automated parsing can no longer be trusted.

The bot **does not silently merge specification changes**. Human review is intentionally required before revised assurance logic becomes the repository baseline.

## Security testing boundary

Dynamic testing is only permitted against systems the operator is authorized to test. The skill prohibits destructive tests, denial-of-service activity, credential stuffing, uncontrolled brute force, persistence, data exfiltration and testing unrelated third-party infrastructure. See `references/authorized-testing.md`.

## Recommended tooling

The skill is tool-agnostic. Where available it can orchestrate:

- Semgrep or equivalent SAST
- Gitleaks or equivalent secret scanning
- Trivy / OSV-Scanner / native package audits for vulnerable dependencies
- OWASP ZAP for DAST
- Burp Suite using the ADA-published audit scan configuration where licensed and available
- TLS/security-header tooling
- framework-native tests and custom authorization/OAuth tests

Scanner output is supporting evidence. A scanner alone cannot mark a CASA control Pass.

## Adjudication, regression CI and work-item integration

Material conflicts between static review, runtime evidence, scanners or reviewers are recorded in a formal adjudication log rather than being silently overwritten.

A completed assessment can be retained as an accepted internal baseline. Future CI runs can compare repeatable security procedures against that baseline with `scripts/compare_assessments.py`. A regression PASS only means no configured regression was detected in the procedures compared; it is not a fresh full CASA assessment.

Open findings can be converted into a portable ticket queue with `scripts/export_ticket_queue.py`. External GitHub Issues or Jira tickets are created only when explicitly authorized, and closing a ticket never substitutes for security retesting.

## Licensing

Original repository content is licensed under Apache-2.0. Material downloaded from the App Defense Alliance remains subject to its upstream **CC BY-SA 4.0** license. See `NOTICE` and `official/README.md`.
