#!/usr/bin/env python3
"""Validate repository integrity: pinned manifest, generated catalogues, schemas and required files."""
import json, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def fail(msg): print('ERROR:',msg,file=sys.stderr); return False

def main():
    ok=True
    m=json.loads((ROOT/'official/upstream-manifest.json').read_text(encoding='utf-8'))
    c=json.loads((ROOT/'references/casa-control-catalog.json').read_text(encoding='utf-8'))
    controls=c.get('controls',[]); ids=[x.get('id') for x in controls]
    if len(controls)!=m.get('control_count'): ok=fail(f"manifest control_count={m.get('control_count')} but catalog={len(controls)}") and ok
    if len(ids)!=len(set(ids)): ok=fail('duplicate control IDs') and ok
    if not all(re.fullmatch(r'\d+\.\d+\.\d+',x or '') for x in ids): ok=fail('invalid control ID format') and ok
    domains={x.get('domain') for x in controls}
    if len(domains)<6: ok=fail(f'expected at least 6 CASA domains, found {len(domains)}') and ok

    # Generated test cases must cover every control with usable AL2 procedure/verification text.
    t=json.loads((ROOT/'references/casa-test-cases.generated.json').read_text(encoding='utf-8'))
    tests=t.get('controls',{})
    if t.get('casa_component_version')!=m.get('casa_component_version'):
        ok=fail(f"test-case file is for CASA {t.get('casa_component_version')} but manifest pins {m.get('casa_component_version')}") and ok
    missing=sorted(set(ids)-set(tests))
    if missing: ok=fail(f'controls without test-case entries: {missing}') and ok
    incomplete=sorted(k for k,v in tests.items() if not v.get('test_procedure',{}).get('AL2') or not v.get('verification',{}).get('AL2'))
    if incomplete: ok=fail(f'controls with empty AL2 test procedure/verification: {incomplete}') and ok

    # Control test strategy must reference only real controls and cover all of them.
    s=json.loads((ROOT/'references/control-test-strategy.json').read_text(encoding='utf-8'))
    strategy_ids=[x.get('id') for x in s.get('controls',[])]
    if set(strategy_ids)!=set(ids): ok=fail(f'control-test-strategy mismatch: missing={sorted(set(ids)-set(strategy_ids))} extra={sorted(set(strategy_ids)-set(ids))}') and ok

    # Every JSON schema and template must at least parse.
    for path in sorted((ROOT/'schemas').glob('*.json'))+sorted((ROOT/'templates').glob('*.json')):
        try: json.loads(path.read_text(encoding='utf-8'))
        except ValueError as e: ok=fail(f'{path.relative_to(ROOT)} is not valid JSON: {e}') and ok

    required=['README.md','SKILL.md','AGENTS.md','references/evidence-standard.md','references/authorized-testing.md','references/report-artifact-generation.md','templates/casa-readiness-report.md','templates/report-disclaimer.md','schemas/finding.schema.json','schemas/report-rendering-manifest.schema.json','references/adjudication-standard.md','references/regression-ci.md','references/ticket-integration.md','agents/adjudication-reviewer.md','scripts/compare_assessments.py','scripts/export_ticket_queue.py','schemas/adjudication-record.schema.json','schemas/regression-summary.schema.json','schemas/ticket-queue.schema.json','templates/ci/casa-regression.yml','examples/sample-assessment/00-assessment-manifest.json','examples/sample-assessment/04-casa-control-matrix.csv','examples/sample-assessment/05-findings-register.jsonl']
    for f in required:
        if not (ROOT/f).exists(): ok=fail(f'missing {f}') and ok
    print(f'Validated {len(controls)} controls across {len(domains)} domains; CASA {m.get("casa_component_version")}; {len(tests)} test-case entries complete.')
    return 0 if ok else 1
if __name__=='__main__': sys.exit(main())
