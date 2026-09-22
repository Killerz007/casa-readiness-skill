# Sanitized CASA Readiness Assessment Example

> **Illustrative example only:** This document uses a fictional application and synthetic evidence references to demonstrate report structure. No real application was tested. This is not an official CASA assessment, CASA certification, assurance-level determination, Google OAuth verification or Google approval.

## Executive summary

| Field | Example value |
| --- | --- |
| Application | Acme Notes (fictional) |
| Assessment mode | Full readiness assessment |
| Application revision | `7b1c9e2` (synthetic) |
| CASA baseline | CASA v2.1.1, pinned to ASA-WG release v2.2.0 |
| Environment | Authorized staging environment |
| Result | **Not ready for independent CASA assessment** |

The fictional application did not satisfy control 3.2.2 because its OAuth callback accepted a redirect target that was not matched against an exact allowlist. All other applicable procedures in this example were completed, and the failed control maps to the open finding below. Remediation and a successful retest are required before the conclusion can change.

## Control results

| Status | Count |
| --- | ---: |
| Pass | 45 |
| Fail | 1 |
| N/A | 2 |
| Blocked | 0 |
| Not tested | 0 |
| **Total** | **48** |

N/A decisions would include an objective applicability rationale and indexed evidence in a real assessment. A high pass count does not override the failed requirement.

## Example finding

### CASA-F-001 — OAuth redirect target is not restricted to an exact allowlist

| Field | Example value |
| --- | --- |
| Status | Open |
| Rating | High |
| Regression key | `oauth.redirect_uri.exact_allowlist` |
| CASA mapping | 3.2.2 |
| Affected component | `/oauth/callback` |
| Evidence | `EVID-RUNTIME-014`, `EVID-CODE-008` (synthetic) |

**Observation.** An authorized staging test supplied a redirect target under an attacker-controlled subdomain. The callback accepted the value because validation used a suffix comparison rather than an exact match against a server-side allowlist.

**Remediation.** Compare the complete normalized redirect URI against a server-controlled set of exact approved values. Reject unregistered schemes, hosts, ports and paths. Add negative tests for subdomains, encoded host separators, scheme changes and path confusion.

**Retest condition.** Repeat the original request and the negative redirect corpus against the remediated revision. Preserve the requests, redacted responses and relevant configuration as new evidence. A code change or closed ticket alone is not sufficient to close the finding.

## Evidence package shape

The real assessment package would include the complete control matrix, adjudication log, findings and remediation registers, retest results, scanner provenance, evidence index, AL2 procedure traceability, ticket queue, rendering manifest and synchronized Markdown, DOCX and PDF reports. See the [README](../README.md#expected-output) for the full output tree.

## Reliance limitation

This fictional example illustrates the repository's reporting approach only. Actual conclusions are limited to the documented scope, pinned application revision, environment, evidence and procedures performed. Google, the App Defense Alliance and authorized laboratories independently determine verification, assessment and certification outcomes and may request additional evidence or testing. No security review guarantees that an application is free of vulnerabilities or future compromise.
