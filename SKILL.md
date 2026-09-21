---
name: casa-readiness
version: 1.1.0
description: >
  Perform a rigorous, evidence-backed readiness assessment against the current
  App Defense Alliance CASA specification for web applications and web-accessible
  APIs. Includes Google OAuth scope/data-flow review, static and dynamic security
  testing, control-by-control AL2 validation, findings, remediation guidance,
  retesting and formal assurance-style reporting. Never represents the result as
  official CASA certification.
---

# CASA Readiness Security Assurance Skill

## 1. Purpose

Use this skill when a developer wants to prepare a web application or web-accessible API for a Google OAuth security assessment or an App Defense Alliance CASA assessment, or wants a CASA-aligned application security review.

This is an **independent readiness methodology**, not an ADA laboratory assessment and not a certification mechanism.

## 2. Non-negotiable principles

1. **Official source first.** The current released App Defense Alliance CASA Specification and CASA Test Guide are the primary criteria. Community mappings and generic OWASP advice are secondary.
2. **Pin the standard.** Every assessment must record upstream repository, release tag, CASA component version, source file hashes and assessment date.
3. **Pin the application.** Record repository URL/name, branch, commit SHA, deployment URL/environment and material configuration used for testing.
4. **No unsupported Pass.** A control cannot be marked Pass merely because no scanner alert exists. Pass requires evidence that directly supports the official verification criterion.
5. **No casual N/A.** N/A requires a documented, objectively verifiable applicability rationale.
6. **Dynamic controls need dynamic evidence.** If the official AL2 procedure requires runtime behavior, source review alone is insufficient unless the test guide explicitly permits it.
7. **Failed controls remain failed regardless of finding severity.** Severity prioritizes remediation; it does not waive CASA requirements.
8. **No destructive testing.** Follow `references/authorized-testing.md`.
9. **Preserve evidence.** Raw tool output, test inputs, relevant responses, screenshots and code/config references must be indexed and reproducible.
10. **Render professional deliverables.** A full/retest assessment must automatically produce the final report as Markdown, DOCX and PDF from one frozen source of truth. Before rendering, discover and invoke any installed professional report-writing/document-generation, document-layout and PDF-generation capability available in the executing AI environment. Follow `references/report-artifact-generation.md`.
11. **Do not claim certification.** Allowed terms are readiness assessment, pre-assessment, internal assessment, independent preparation review and similar wording.

## 3. Required files to read before work starts

Read, in this order:

1. `official/upstream-manifest.json`
2. `references/assessment-methodology.md`
3. `references/authorized-testing.md`
4. `references/evidence-standard.md`
5. `references/severity-methodology.md`
6. `references/scanner-matrix.md`
7. `references/google-oauth-verification.md`
8. `references/reporting-standard.md`
9. `references/report-design.md`
10. `references/report-artifact-generation.md`
11. `references/casa-control-catalog.json`
12. `references/control-test-strategy.json`
13. the current official CASA Specification and CASA Test Guide fetched/pinned by `scripts/sync_official_spec.py`

If the official files are absent or the upstream check is older than 45 days and internet access exists, run:

```bash
python scripts/sync_official_spec.py --sync
python scripts/validate_repo.py
```

If internet access is unavailable, continue only against the pinned baseline and state the age of that baseline prominently in the report.

## 4. Assessment modes

Support these modes:

- `scope`: application, OAuth, data-flow and applicability review only.
- `full`: complete CASA readiness assessment.
- `retest`: validate previously failed/blocked controls and findings only, plus regression testing needed to support closure.
- `evidence-pack`: normalize existing results into the formal output package without claiming unperformed tests.
- `delta`: assess security impact of changes since a prior pinned commit and identify which CASA controls need retesting.

Default to `full` unless the user clearly requests another mode.

## 5. Phase 0: Access, authorization and immutable baseline

Before testing:

1. Verify full read access to the application repository. Abort the affected test area rather than guessing if access is partial.
2. Record the exact application commit SHA.
3. Identify whether generated, vendored, minified or inaccessible code exists and record limitations.
4. Identify the authorized test target. Prefer staging or a dedicated test environment.
5. Confirm the operator is authorized to test the target. If authorization is not established, perform source/configuration review only and mark runtime controls Blocked where necessary.
6. Record test accounts/roles required, without storing live passwords or secrets in report files.
7. Run/verify the CASA upstream sync and record the official baseline.
8. Create the assessment directory and `00-assessment-manifest.json`.

The manifest must include:

- project name;
- repository and commit SHA;
- assessment mode;
- target environment and URL if applicable;
- start date/time and timezone;
- CASA component version;
- upstream release tag and commit if available;
- specification/test-guide hashes;
- tester/agent identity description;
- authorization status;
- scanner names and versions as they become known.

## 6. Phase 1: Application discovery and architecture

Inspect the full repository and relevant deployment configuration. Document:

- languages and frameworks;
- frontend/backend/API boundaries;
- authentication providers;
- session/token model;
- authorization model, roles and tenant boundaries;
- databases and storage;
- file-upload paths;
- queues/background jobs;
- external APIs;
- admin interfaces;
- secrets management;
- logging/monitoring;
- CI/CD and deployment platform;
- public domains/subdomains;
- security middleware/headers;
- cryptographic use;
- third-party dependencies;
- Google OAuth/API integration;
- data lifecycle for confidential and Google user data.

Produce `02-scope-and-architecture.md` with a textual data-flow/trust-boundary description. Generate diagrams only if the available environment can do so accurately.

## 7. Phase 2: Google OAuth and Google user-data assessment

Search source code, configuration and documentation for Google OAuth clients, scopes, callback routes, token handling and Google API usage.

Produce `03-google-oauth-assessment.md` containing:

- OAuth clients/environments identified;
- requested scopes exactly as configured;
- scope classification where authoritative Google documentation supports it;
- API operations actually used;
- whether Google user data passes through a backend/server;
- where access and refresh tokens are stored;
- encryption and secret-management controls;
- retention/deletion behavior;
- account disconnect/revocation behavior;
- consent-screen/privacy-policy consistency where evidence is available;
- least-privilege analysis and any unused/excess scopes;
- clear statement that Google determines the actual verification pathway.

Never state that a sensitive scope automatically requires AL2. Distinguish Google OAuth verification requirements from CASA technical conformance.

## 8. Phase 3: CASA applicability matrix

Load the current generated control catalogue and official test guide. For every CASA control:

1. determine applicability to the scoped architecture using the official scope and test-guide wording;
2. record `Applicable`, `Not Applicable`, or `Needs Clarification`;
3. for N/A, write the objective reason and supporting evidence;
4. identify the AL2 test procedure and verification criterion;
5. identify evidence needed to support the conclusion;
6. assign planned test methods: code review, configuration review, documentation review, runtime/manual test, scanner evidence or combined.

No control may disappear from the matrix.

## 9. Phase 4: Static, dependency, secret and configuration testing

Use available tools appropriate to the detected stack. Prefer reproducible machine-readable output. At minimum, consider:

- SAST: Semgrep, CodeQL or equivalent;
- secrets: Gitleaks or equivalent;
- dependency/CVE scanning: Trivy, OSV-Scanner, native ecosystem audit tools;
- IaC/container scanning where applicable;
- repository history review for exposed secrets where authorized and practical;
- manual review of authentication, authorization, session, OAuth and data-access code.

For every scanner run record:

- tool and version;
- exact command/configuration;
- scope/path;
- start/end timestamp;
- exit status;
- output file;
- output SHA-256;
- exclusions/suppressions;
- whether results were manually adjudicated.

Store raw output under `evidence/raw/`. Do not edit raw scanner files.

## 10. Phase 5: Dynamic application testing

Only run against an explicitly authorized target.

Where available:

- use the current ADA-published Burp audit scan configuration with an appropriately licensed Burp deployment;
- otherwise use OWASP ZAP and manual tests as supporting coverage, clearly distinguishing them from ADA's Burp configuration;
- execute the official CASA AL2 test procedure for each applicable runtime control;
- use controlled test accounts and inert test data;
- cap authentication/anti-automation probes to the minimum needed to establish behavior;
- avoid service degradation and third-party targets.

Examples include controlled tests for authentication throttling, logout invalidation, authorization bypass, IDOR/BOLA, CSRF, OAuth state/redirect validation, TLS, injection, XSS, SSRF using controlled callbacks, file upload handling, debug exposure, subdomain takeover indicators and browser-storage cleanup.

For each dynamic test save a reproducible evidence record containing request/response details with secrets redacted, actor/role, expected result, actual result and conclusion.

## 11. Phase 6: Manual contextual review

Scanner output must be adjudicated in application context. Review:

- framework protections that may invalidate a scanner alert;
- server-side authorization behind client-side checks;
- ORM/query parameterization;
- template auto-escaping;
- environment-specific configuration;
- test fixtures versus production code;
- compensating controls;
- exploitable paths from untrusted input to sensitive sinks;
- multi-tenant boundary enforcement;
- OAuth/token lifecycle and state management;
- sensitive logging and browser storage;
- error handling/fail-closed behavior.

False positives must be documented rather than silently deleted if they were material scanner alerts.

## 12. Phase 7: Control conclusions

Allowed statuses:

- `PASS`: official verification criterion satisfied with sufficient evidence.
- `FAIL`: official requirement is not satisfied or a confirmed exploitable weakness defeats it.
- `N/A`: control objectively does not apply, with supporting rationale/evidence.
- `BLOCKED`: required test could not be performed because evidence/access/environment was unavailable.
- `NOT_TESTED`: assessment has not yet executed the required procedure.

`BLOCKED` and `NOT_TESTED` prevent a Ready conclusion.

Populate `04-casa-control-matrix.csv` for all controls.

## 13. Phase 8: Findings

Create a finding for each material failed control or distinct vulnerability/control weakness. Related controls may be referenced by one finding, but every failed control must map to at least one finding.

Each finding must contain:

- unique ID, e.g. `CASA-F-001`;
- title;
- rating;
- status;
- affected components/endpoints;
- CASA requirement(s);
- CWE(s) where applicable;
- CVSS vector/score where meaningful;
- observation/factual condition;
- evidence;
- reproduction/test procedure;
- risk and implication;
- root cause where supported by evidence;
- specific remediation;
- stack-specific implementation guidance/examples;
- compensating controls if present;
- retest criteria;
- evidence references.

Do not overstate exploitability. Distinguish confirmed vulnerabilities from control-design gaps and documentation/evidence deficiencies.

## 14. Phase 9: Remediation guidance

Remediation must be actionable. For each finding:

1. state the control objective;
2. explain the required technical change;
3. identify likely files/components based on actual evidence;
4. provide implementation examples appropriate to the detected framework where safe and useful;
5. identify tests that should be added to prevent regression;
6. identify any deployment/configuration change;
7. state the exact retest condition.

Do not make automatic code changes unless the user separately authorizes remediation. Assessment and remediation should remain distinguishable in the evidence trail.

## 15. Phase 10: Retest

For closed findings:

- inspect the remediation commit/diff;
- rerun the original failing procedure;
- run focused regression tests;
- preserve new evidence;
- record `Closed`, `Partially Remediated`, `Open`, or `Unable to Retest`;
- never mark a finding closed solely because code changed.

Produce `07-retest-results.md`.

## 16. Phase 11: Formal reporting and document generation

Follow `references/reporting-standard.md`, `references/report-design.md`, `references/report-artifact-generation.md`, `templates/casa-readiness-report.md` and `templates/report-disclaimer.md`.

Before drafting/rendering, inspect the executing environment for installed professional report-writing, document-authoring, document-layout, DOCX and PDF-generation skills/tools. If available, **invoke those capabilities** rather than improvising binary document generation. Prefer capabilities specifically intended for reports/documents and PDF export. Do not use presentation/slide tooling for the formal report.

Create one canonical, frozen report content set after control conclusions and findings are finalized. Render that same content into all required formats so section text, figures, tables, findings, control counts, conclusion and disclaimers are identical in substance.

The final package must include:

1. executive summary;
2. objectives and scope;
3. criteria and pinned standard;
4. architecture and data-flow summary;
5. Google OAuth assessment;
6. methodology and tools;
7. limitations;
8. overall control results;
9. findings summary;
10. detailed findings;
11. full CASA control matrix;
12. remediation register;
13. retest results where applicable;
14. scanner register;
15. evidence index;
16. test-procedure traceability showing official AL2 procedure versus work actually performed;
17. appendices/provenance;
18. `10-casa-readiness-report.docx`;
19. `10-casa-readiness-report.pdf`;
20. `12-report-rendering-manifest.json`, recording the canonical report hash, renderer/capability used, output hashes and rendering status.

The tone must be professional, factual and assurance-oriented. Avoid marketing language, unsupported confidence and generic advice.

The DOCX and PDF are mandatory deliverables for `full`, `retest` and `evidence-pack` modes. For `scope` and `delta`, produce them unless the user explicitly requests lightweight output.

If the executing environment genuinely cannot create DOCX or PDF:
- do not fabricate, rename or fake binary files;
- still produce the complete canonical Markdown report and structured source tables;
- mark the missing artifact(s) as `BLOCKED_RENDERING` in `12-report-rendering-manifest.json`;
- clearly disclose the rendering limitation to the user;
- do **not** change the CASA readiness conclusion solely because of a rendering limitation.

## 17. Readiness conclusion logic

Use one of these conclusions:

### Ready for independent CASA assessment
Only when:
- every applicable control is Pass;
- all N/A decisions are substantiated;
- no controls are Blocked or Not Tested;
- no open finding causes a control failure;
- official source provenance is current and validated;
- required runtime testing was completed against an authorized representative environment.

### Not ready for independent CASA assessment
Use when one or more applicable controls Fail.

### Assessment incomplete
Use when there are Blocked/Not Tested controls, material scope uncertainty, stale/unverified upstream criteria or insufficient evidence.

Never substitute a percentage score for the conclusion. A high pass percentage does not override a failed requirement.

## 18. Mandatory report disclaimers

Every rendered Markdown, DOCX and PDF report must include the approved disclaimer wording from `templates/report-disclaimer.md` in these locations:

1. **Cover page:** full independent-assessment / non-affiliation / non-certification notice.
2. **Executive summary:** concise readiness and reliance disclaimer.
3. **Conclusion section:** explicit statement that the readiness conclusion is preparatory and does not bind Google, the App Defense Alliance or an authorized laboratory.
4. **Footer:** short form such as `Independent CASA Readiness Assessment | Not Certification`.

At minimum the disclaimer must state that:
- the review is an independent readiness/pre-assessment and is not an official CASA assessment unless expressly performed and issued by an ADA-authorized laboratory;
- the project/author/AI agent is not affiliated with, endorsed by, or acting on behalf of Google or the App Defense Alliance;
- the report does not grant CASA certification, Google OAuth verification, Google approval, or any assurance level;
- Google, the App Defense Alliance and authorized laboratories determine their own verification/assessment outcomes and may request additional evidence or testing;
- conclusions are limited to the stated scope, pinned application version/commit, environment, evidence and procedures performed as of the report date;
- no security review can guarantee that an application is free of vulnerabilities or future compromise;
- blocked, not-tested and out-of-scope areas remain limitations;
- the report is not a substitute for any official laboratory report, contractual assurance, legal advice or regulatory determination.

Do not use third-party audit/consulting logos or wording that implies Big Four, Google, ADA or laboratory authorship.

## 19. Evidence and confidentiality

Never place live passwords, OAuth client secrets, access tokens, refresh tokens, API keys, production personal data or other secrets in the report repository. Redact sensitive values and store only the minimum evidence necessary.

## 20. Completion quality gate

Before final delivery verify:

- application commit SHA is recorded;
- CASA upstream version and hashes are recorded;
- all official controls exist in the matrix exactly once;
- every applicable control has official-to-actual test-procedure traceability;
- every Pass has supporting evidence;
- every Fail maps to a finding;
- every N/A has rationale;
- every Blocked/Not Tested control is disclosed;
- all scanner runs have provenance;
- raw evidence hashes are indexed;
- remediation guidance is specific;
- report contains the mandatory cover, executive-summary, conclusion and footer disclaimers;
- canonical Markdown, DOCX and PDF report content are substantively synchronized;
- `12-report-rendering-manifest.json` records renderer/capability and hashes, or explicitly records `BLOCKED_RENDERING`;
- DOCX and PDF open successfully and have been visually inspected for broken tables, clipped text, page-number/footer issues and missing appendices;
- no secrets are present in outputs.
