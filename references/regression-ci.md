# CASA Regression CI

## Purpose

A complete AL2 assessment cannot be reduced to a CI job. Regression CI is a narrower control designed to detect changes against a previously accepted CASA readiness baseline and force targeted retesting.

It does **not** certify the new commit and does not automatically carry forward PASS conclusions where the underlying evidence is no longer representative.

## Baseline

After a completed assessment is accepted by the application owner, retain at minimum:

- `04-casa-control-matrix.csv`
- `05-findings-register.jsonl`
- assessment manifest and pinned commit
- any repeatable scanner/test scripts needed for the controls selected for CI

The baseline should identify the CASA version used.

## CI workflow

For a new commit:

1. run the project's repeatable security checks/scanners;
2. produce/update a current control matrix and structured findings register for the controls actually retested;
3. compare current results to the accepted baseline using `scripts/compare_assessments.py`;
4. fail CI on configured control regressions/new or reopened findings;
5. flag scope/specification changes for human review;
6. require targeted manual/runtime retesting for controls CI cannot validate.

## What counts as a regression

Examples:

- PASS -> FAIL/BLOCKED/NOT_TESTED;
- N/A -> FAIL/BLOCKED/NOT_TESTED because a feature became applicable;
- previously Closed finding reopens;
- new open finding at or above the configured severity threshold;
- loss of required evidence for a previously accepted control;
- a security-relevant scope change that invalidates the old evidence.

## What CI must not do

- assume unchanged code means unchanged security;
- treat absence of scanner alerts as PASS;
- silently promote BLOCKED/NOT_TESTED to PASS;
- reuse evidence from a different environment without documenting representativeness;
- claim the application remains CASA certified/approved.

## Recommended repository layout in a target application

```text
.casa/
  baseline/
    00-assessment-manifest.json
    04-casa-control-matrix.csv
    05-findings-register.jsonl
  current/
    04-casa-control-matrix.csv
    05-findings-register.jsonl
  regression/
    regression-summary.json
    regression-summary.md
```

Use `templates/ci/casa-regression.yml` as a starting point and adapt the project-specific scanner/test command.
