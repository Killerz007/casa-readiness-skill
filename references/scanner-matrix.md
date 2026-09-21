# Scanner and Test Tool Matrix

Tools are supporting mechanisms. The agent must verify installed versions and current CLI syntax before execution.

| Area | Preferred tools / techniques | Typical CASA coverage |
|---|---|---|
| SAST | Semgrep, CodeQL, framework-aware static review | Access control, injection, XSS, SSRF, command execution, crypto misuse, logging, secret handling |
| Secret scanning | Gitleaks, TruffleHog where authorized | 6.7.1 and supporting security hygiene |
| Dependency/CVE | Trivy, OSV-Scanner, npm/pnpm/yarn/pip/poetry/maven/gradle native audit | 6.1.1 |
| IaC/container | Trivy and platform-native configuration checks | Configuration evidence and supporting exposure analysis |
| DAST | ADA Burp configuration when licensed/available; OWASP ZAP as open-source supporting coverage | Runtime controls, input handling, security configuration |
| OAuth | Manual flow testing, proxy capture, unit/integration tests | 3.2.1, 3.2.2 and token/session controls |
| Authorization | Two-role/two-user manual/API tests | 3.1.1–3.1.4 |
| TLS | Qualys SSL Labs where appropriate, testssl.sh/sslyze/curl/openssl | 4.1.1, 4.1.2 |
| Browser/client storage | Browser devtools/automation plus logout tests | 6.6.1 |
| Subdomain takeover | DNS inventory, provider-binding validation, safe takeover indicators | 6.4.1 |
| Headers/config | Browser/proxy/curl plus server/config review | Supporting evidence across several controls |

## Evidence collection

For each tool record version, command/config, scope, timestamps, output, SHA-256 and manual adjudication status.

## Scanner limitations

- SAST can miss runtime authorization logic and configuration.
- DAST can miss authenticated/role-specific paths without good crawling and accounts.
- dependency scanners report package vulnerability intelligence, not application exploitability by themselves.
- secret scanners can report test fixtures and false positives.
- generic ZAP scans are not identical to the ADA-published Burp configuration.

The report must disclose these limitations.
