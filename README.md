# CASA Readiness Skill

An AI-agent security assurance skill for assessing web applications and web-accessible APIs against the **current App Defense Alliance CASA specification** and preparing an evidence-backed readiness package for Google OAuth / CASA review.

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
- documenting findings with severity, evidence, reproduction steps, CASA mapping, CWE mapping, remediation and retest criteria;
- producing a formal assurance-style report and evidence index suitable for management review and external-assessor preparation;
- tracking official CASA specification changes monthly and opening a review pull request when released CASA material changes.

## Current pinned CASA baseline

The repository is initially pinned to **CASA v2.1.1 (2026-06-03)**. The latest upstream repository release at the time this project was prepared is **ASA-WG v2.2.0**, which explicitly states that CASA itself remains v2.1.1.

The source of truth is always the App Defense Alliance repository:

- `appdefensealliance/ASA-WG/CASA/CASA Specification.md`
- `appdefensealliance/ASA-WG/CASA/CASA Test Guide.md`
- `appdefensealliance/ASA-WG/CASA/ADA Burp Audit Scan Configuration.json`

See `official/upstream-manifest.json` for the pinned provenance.

## Quick use with an AI agent

Give the agent access to both this skill repository and the application repository, then ask:

```text
Use the CASA Readiness Skill from this repository to perform a complete CASA readiness assessment of this application. Follow SKILL.md exactly. Use the latest released App Defense Alliance CASA specification, preserve raw scan evidence, and produce the complete formal assessment package. Do not claim certification.
```

If the AI supports repository skills, point it directly at `SKILL.md`. If it does not, use `prompts/portable-agent-prompt.md`.

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
    05-detailed-findings.md
    06-remediation-register.csv
    07-retest-results.md
    08-scanner-register.csv
    09-evidence-index.csv
    10-casa-readiness-report.md
    11-test-procedure-traceability.csv
    evidence/
      raw/
      normalized/
      screenshots/
      runtime/
      code/
```

The report conclusion must use readiness language such as **Ready for independent CASA assessment**, **Not ready**, or **Assessment incomplete**. It must never state that the application is CASA certified unless an authorized external body has actually issued that certification.

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

## Licensing

Original repository content is licensed under Apache-2.0. Material downloaded from the App Defense Alliance remains subject to its upstream **CC BY-SA 4.0** license. See `NOTICE` and `official/README.md`.
