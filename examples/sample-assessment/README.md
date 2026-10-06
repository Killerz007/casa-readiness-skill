# Sample assessment fixture

A **fictional**, minimal evidence pack showing the machine-readable files the scripts consume:

- `00-assessment-manifest.json` - pinned application, mode and CASA version;
- `04-casa-control-matrix.csv` - one row per official control (48 for CASA 2.1.1), with one FAIL, one N/A and one BLOCKED;
- `04-adjudication-log.jsonl` - the adjudication record behind the BLOCKED control;
- `05-findings-register.jsonl` - the finding that explains the FAIL.

It is used by the test suite and can be used as a regression baseline when trying the scripts:

```bash
python scripts/export_ticket_queue.py --assessment-dir examples/sample-assessment --output /tmp/queue
python scripts/compare_assessments.py --baseline examples/sample-assessment --current examples/sample-assessment --output /tmp/regression
```

Nothing here represents a real application or a real assessment outcome.
