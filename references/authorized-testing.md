# Authorized and Safe Testing Rules

Runtime testing must only be performed against assets the operator is authorized to assess.

## Required boundary

Before DAST/manual attack simulation, record:

- target URL/host;
- environment owner;
- authorization basis;
- permitted test window if one exists;
- test accounts and roles;
- excluded endpoints/services;
- whether third-party systems are reachable through the application.

## Prohibited activity

Do not perform:

- denial-of-service or resource-exhaustion tests;
- high-volume brute force, credential stuffing or password spraying;
- destructive data modification outside dedicated test data;
- persistence, malware deployment or backdoors;
- lateral movement into unrelated systems;
- extraction of real customer/personal data;
- testing of unrelated third-party services;
- bypass of rate limits by distributing traffic;
- cloud metadata/service exploitation that retrieves real credentials;
- social engineering.

## Safe control-validation patterns

- **Brute-force resistance:** use the smallest controlled sequence sufficient to observe throttling/lockout behavior.
- **IDOR/BOLA:** use two authorized test identities and records created for the assessment.
- **CSRF:** use benign state changes in test accounts.
- **SSRF:** use an assessor-controlled callback or harmless endpoint; do not retrieve cloud credentials.
- **File upload:** use inert files and safe polyglot/test samples; do not upload executable malware.
- **Injection:** use non-destructive payloads and stop once vulnerability is established.
- **OAuth:** use designated test clients/accounts and never capture tokens belonging to uninvolved users.

If safe testing cannot establish the official verification criterion, mark the control Blocked rather than escalating test aggressiveness without explicit authorization.
