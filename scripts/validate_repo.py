#!/usr/bin/env python3
import json, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def fail(msg): print('ERROR:',msg,file=sys.stderr); return False

def main():
    ok=True
    m=json.loads((ROOT/'official/upstream-manifest.json').read_text())
    c=json.loads((ROOT/'references/casa-control-catalog.json').read_text())
    controls=c.get('controls',[]); ids=[x.get('id') for x in controls]
    if len(controls)!=m.get('control_count'): ok=fail(f"manifest control_count={m.get('control_count')} but catalog={len(controls)}") and ok
    if len(ids)!=len(set(ids)): ok=fail('duplicate control IDs') and ok
    if not all(re.fullmatch(r'\d+\.\d+\.\d+',x or '') for x in ids): ok=fail('invalid control ID format') and ok
    domains={x.get('domain') for x in controls}
    if len(domains)<6: ok=fail(f'expected at least 6 CASA domains, found {len(domains)}') and ok
    required=['README.md','SKILL.md','AGENTS.md','references/evidence-standard.md','references/authorized-testing.md','templates/casa-readiness-report.md','schemas/finding.schema.json']
    for f in required:
        if not (ROOT/f).exists(): ok=fail(f'missing {f}') and ok
    print(f'Validated {len(controls)} controls across {len(domains)} domains; CASA {m.get("casa_component_version")}.')
    return 0 if ok else 1
if __name__=='__main__': sys.exit(main())
