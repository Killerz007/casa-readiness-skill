# Assessment Methodology

## Objective

Assess whether the scoped web application/web-accessible API meets the current released App Defense Alliance CASA requirements and identify gaps before an external assessment.

## Assurance model

The methodology combines:

- repository and architecture review;
- control design assessment;
- secure-code review;
- dependency, secret and configuration scanning;
- runtime/manual application-security testing;
- OAuth and token-lifecycle review;
- evidence normalization and adjudication;
- remediation and retesting.

Automated scanners provide leads and supporting evidence. The conclusion for each CASA control must be based on the official test procedure and verification criteria.

## Assessment lifecycle

1. **Initiation**: access, authorization, scope, commit/environment pinning.
2. **Discovery**: architecture, trust boundaries, roles, endpoints, data flows, Google integrations.
3. **Applicability**: all CASA requirements assessed for applicability.
4. **Testing**: static/configuration/dependency/secret review plus applicable AL2 runtime procedures.
5. **Adjudication**: false-positive review and evidence sufficiency checks.
6. **Reporting**: control matrix, findings and formal report.
7. **Remediation**: developer fixes managed separately from original evidence.
8. **Retest**: verify fixes against the original failing procedure and relevant regressions.

## Sampling

Where the population is too large for exhaustive manual testing, sampling must be risk-based and disclosed. Sampling is not permitted as a reason to ignore an entire distinct authorization model, identity provider, externally exposed application/API, tenant boundary or materially different security implementation.

## Third-party components

Apply the official CASA scoping guidance. Testing must not exceed authorization. Where a third-party service is in scope but cannot be directly tested, assess configured integration behavior and record any blocked procedures.

## Evidence hierarchy

Strongest evidence normally consists of reproducible runtime results plus code/configuration evidence. Documentation alone is weaker unless the official procedure explicitly permits it or runtime verification is impossible and the status is reported accordingly.

## Independence of severity and compliance

A vulnerability rating prioritizes risk remediation. A CASA requirement conclusion addresses conformance. A Low-rated defect can still result in a CASA control failure.
