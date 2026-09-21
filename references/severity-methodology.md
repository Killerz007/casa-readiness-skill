# Finding Severity Methodology

CASA control status and finding severity are separate concepts.

## Ratings

Use CVSS v4.0 where it meaningfully represents a confirmed vulnerability. Supplement with application context rather than inflating the technical score.

Suggested reporting bands:

| Rating | Typical basis |
|---|---|
| Critical | Credible severe compromise with broad confidentiality/integrity/availability impact or privileged takeover, normally supported by a very high CVSS score and demonstrated path |
| High | Material unauthorized access, sensitive-data exposure, authentication/authorization bypass or similarly serious exploit with practical conditions |
| Medium | Exploitable weakness with constrained impact/prerequisites, or a significant control deficiency that meaningfully increases attack likelihood |
| Low | Limited-impact weakness, defense-in-depth failure or narrow exploitability |
| Observation | Improvement/evidence/documentation matter that is not itself a confirmed security vulnerability |

Do not assign a higher rating simply because the issue maps to CASA. Do not reduce a CASA Fail to Pass because the vulnerability is Low.

## Finding confidence

Also record confidence when useful:

- Confirmed: reproduced or directly evidenced.
- High confidence: strong code/config evidence, runtime reproduction unnecessary or unavailable.
- Needs validation: credible indication but insufficient evidence. This should not be presented as a confirmed vulnerability.
