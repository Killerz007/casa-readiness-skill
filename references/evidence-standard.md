# Evidence Standard

Every control conclusion and finding must be traceable to evidence.

## Evidence record fields

Each normalized record should contain:

- evidence ID;
- CASA control ID(s);
- evidence type;
- source/tool;
- application commit SHA;
- environment/target;
- timestamp;
- tester/agent;
- procedure performed;
- expected result;
- observed result;
- conclusion supported;
- raw artifact path;
- SHA-256 of raw artifact where applicable;
- redaction note;
- limitations.

## Preferred evidence types

- source/configuration excerpt with file and line references;
- request/response transcript with secrets redacted;
- screenshot where visual state matters;
- machine-readable scanner output;
- dependency lockfile and resolved vulnerable package evidence;
- DNS/TLS/configuration result;
- architecture/data-flow evidence;
- test execution log.

## Pass standard

A Pass must show why the official verification criterion is satisfied. "No findings" is insufficient.

## N/A standard

N/A must explain why the functionality addressed by the requirement is absent or outside the official scope, with objective supporting evidence.

## Raw evidence integrity

Never edit raw tool output after collection. Normalize/cite it separately. Hash material artifacts and list the hash in the evidence index.

## Sensitive information

Redact secrets and personal data. Record that redaction occurred. Never commit live credentials or tokens.
