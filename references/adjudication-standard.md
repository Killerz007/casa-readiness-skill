# Evidence Adjudication Standard

## Purpose

Adjudication prevents the last scanner, reviewer or AI agent to run from silently overriding stronger contradictory evidence.

## When adjudication is mandatory

Create a formal adjudication record when:

1. static review and runtime behavior conflict;
2. different scanners/reviewers disagree on exploitability or control status;
3. a material scanner alert is proposed as a false positive;
4. PASS depends on indirect or incomplete evidence;
5. N/A is disputed, high-impact, or changes readiness;
6. severity/confidence differs materially between reviewers;
7. a FAIL/BLOCKED/NOT_TESTED becomes PASS and the new supporting evidence is not self-evident;
8. a regression comparison identifies a material change requiring interpretation.

Routine consistent evidence does not need adjudication.

## Evidence precedence

There is no automatic "runtime always wins" rule. Evaluate:

- the exact official CASA verification criterion;
- representativeness of the tested environment;
- whether source/configuration evidence covers all paths;
- whether runtime tests actually exercised the relevant path/role/tenant;
- scanner reliability and known false-positive/false-negative patterns;
- timing/version/commit of the evidence;
- compensating controls and whether they satisfy the criterion.

Newer evidence should not replace older evidence merely because it is newer if it tested a different scope.

## Independence

Prefer a fresh reviewer/agent context for adjudication. The original finding author may provide clarification but should not be the only reviewer of a material dispute where another context is available.

Record the independence limitation when a fresh reviewer is unavailable.

## Decision rules

The adjudicator may conclude:

- `PASS`
- `FAIL`
- `N/A`
- `BLOCKED`
- `NOT_TESTED`

If contradictory evidence cannot be reconciled, the result must not be PASS. Use BLOCKED when the required evidence cannot currently be obtained, or NOT_TESTED when the required procedure has not been executed.

## False positives

A finding may be dismissed only when the record explains:

- why the observed scanner/tool result does not violate the CASA criterion;
- the compensating/framework behavior relied upon;
- evidence supporting dismissal.

Do not delete the original evidence. Preserve it and link the adjudication.

## Severity disputes

Adjudication may change finding severity/confidence independently of CASA status. A Low finding can still cause FAIL, and a High-severity observation cannot create a CASA failure unless it violates an applicable requirement.

## Output record

Use `schemas/adjudication-record.schema.json`.

Every affected control row should reference the adjudication ID(s) in `adjudication_ids`.
