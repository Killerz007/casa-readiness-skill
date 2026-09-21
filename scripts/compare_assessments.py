#!/usr/bin/env python3
"""Compare a current CASA assessment with an accepted baseline.

Exit codes:
  0 - no blocking regression detected
  1 - input/processing error
  2 - blocking regression detected (or strict scope change)

The script never promotes controls to PASS. It only compares recorded assessment
outputs and is intended for regression CI, not as a replacement for AL2 testing.
"""
import argparse, csv, json, sys
from datetime import datetime, timezone
from pathlib import Path

CONTROL_FILE='04-casa-control-matrix.csv'
FINDING_FILE='05-findings-register.jsonl'
MANIFEST_FILE='00-assessment-manifest.json'
NEGATIVE={'FAIL','BLOCKED','NOT_TESTED'}
SEVERITY={'Observation':0,'Low':1,'Medium':2,'High':3,'Critical':4}

def norm_status(value):
    value=(value or '').strip().upper().replace(' ','_')
    if value in {'NA','N_A','NOT_APPLICABLE'}: return 'N/A'
    return value

def read_controls(base):
    path=base/CONTROL_FILE
    if not path.exists(): raise FileNotFoundError(path)
    with path.open(newline='',encoding='utf-8-sig') as f:
        rows=list(csv.DictReader(f))
    result={}
    for row in rows:
        cid=(row.get('control_id') or '').strip()
        if not cid: continue
        if cid in result: raise ValueError(f'duplicate control {cid} in {path}')
        row=dict(row); row['status']=norm_status(row.get('status'))
        result[cid]=row
    return result

def read_findings(base):
    path=base/FINDING_FILE
    if not path.exists(): return {}
    result={}
    for lineno,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
        if not line.strip(): continue
        item=json.loads(line)
        key=item.get('regression_key') or item.get('finding_id')
        if not key: raise ValueError(f'finding without regression_key/finding_id at {path}:{lineno}')
        result[str(key)]=item
    return result

def read_manifest(base):
    path=base/MANIFEST_FILE
    if not path.exists(): return {}
    return json.loads(path.read_text(encoding='utf-8'))

def finding_open(item):
    return str(item.get('status','')).lower() not in {'closed','resolved','accepted-risk'}

def markdown(summary):
    lines=[
      '# CASA Regression Summary','',
      f"Generated: {summary['generated_at']}",'',
      f"Baseline: `{summary['baseline']}`  ",
      f"Current: `{summary['current']}`",'',
      f"**Blocking regressions:** {len(summary['blocking_regressions'])}  ",
      f"**Scope/specification changes:** {len(summary['scope_changes'])}  ",
      f"**Improvements:** {len(summary['improvements'])}",''
    ]
    def section(title,items):
        lines.extend([f'## {title}',''])
        if not items:
            lines.extend(['None.','']); return
        for x in items:
            lines.append(f"- **{x.get('type','change')}**: {x.get('message','')}")
        lines.append('')
    section('Blocking regressions',summary['blocking_regressions'])
    section('Scope/specification changes requiring review',summary['scope_changes'])
    section('Improvements / closures',summary['improvements'])
    lines += ['## Important limitation','',
      'This comparison detects differences in recorded CASA assessment outputs. It does not perform an AL2 assessment and does not carry forward a prior PASS where new evidence is required.','']
    return '\n'.join(lines)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--baseline',required=True)
    ap.add_argument('--current',required=True)
    ap.add_argument('--output',required=True)
    ap.add_argument('--minimum-severity',choices=list(SEVERITY),default='Medium')
    ap.add_argument('--partial',action='store_true',help='Current matrix may contain only controls actually retested; absent controls are not treated as regressions.')
    ap.add_argument('--strict-scope',action='store_true',help='Fail CI when scope/specification changes require review.')
    args=ap.parse_args()
    baseline=Path(args.baseline); current=Path(args.current); out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    b_controls=read_controls(baseline); c_controls=read_controls(current)
    b_findings=read_findings(baseline); c_findings=read_findings(current)
    b_manifest=read_manifest(baseline); c_manifest=read_manifest(current)
    regressions=[]; scope=[]; improvements=[]

    bv=b_manifest.get('casa_component_version'); cv=c_manifest.get('casa_component_version')
    if bv and cv and bv!=cv:
        scope.append({'type':'casa-version-change','message':f'CASA component changed from {bv} to {cv}; baseline requires human review/re-establishment.'})

    for cid,b in sorted(b_controls.items()):
        if cid not in c_controls:
            if not args.partial:
                regressions.append({'type':'missing-current-control','control_id':cid,'message':f'{cid} exists in baseline but is missing from the current matrix.'})
            continue
        c=c_controls[cid]; bs=b['status']; cs=c['status']
        if bs=='PASS' and cs in NEGATIVE:
            regressions.append({'type':'control-regression','control_id':cid,'from':bs,'to':cs,'message':f'{cid} regressed {bs} -> {cs}.'})
        elif bs=='N/A' and cs in NEGATIVE:
            regressions.append({'type':'applicability-regression','control_id':cid,'from':bs,'to':cs,'message':f'{cid} became applicable/incomplete: {bs} -> {cs}.'})
        elif bs in {'PASS','N/A'} and cs in {'PASS','N/A'} and bs!=cs:
            scope.append({'type':'applicability-change','control_id':cid,'message':f'{cid} changed {bs} -> {cs}; review applicability/evidence.'})
        elif bs in NEGATIVE and cs in {'PASS','N/A'}:
            improvements.append({'type':'control-improvement','control_id':cid,'message':f'{cid} improved {bs} -> {cs}; closure still depends on valid current evidence.'})
        elif bs=='FAIL' and cs in {'BLOCKED','NOT_TESTED'}:
            regressions.append({'type':'evidence-regression','control_id':cid,'from':bs,'to':cs,'message':f'{cid} changed {bs} -> {cs}; prior failure has not been shown remediated and current validation is incomplete.'})

    for cid in sorted(set(c_controls)-set(b_controls)):
        scope.append({'type':'new-control','control_id':cid,'message':f'{cid} is present in current assessment but not baseline; review specification/scope change.'})

    threshold=SEVERITY[args.minimum_severity]
    for key,cur in c_findings.items():
        base=b_findings.get(key)
        sev=SEVERITY.get(str(cur.get('rating','Observation')),0)
        if finding_open(cur) and sev>=threshold:
            if base is None:
                regressions.append({'type':'new-finding','finding_key':key,'message':f"New open {cur.get('rating','')} finding {cur.get('finding_id',key)}: {cur.get('title','')}"})
            elif not finding_open(base):
                regressions.append({'type':'reopened-finding','finding_key':key,'message':f"Previously closed finding reopened: {cur.get('finding_id',key)} {cur.get('title','')}"})
    for key,base in b_findings.items():
        cur=c_findings.get(key)
        if cur and finding_open(base) and not finding_open(cur):
            improvements.append({'type':'finding-closed','finding_key':key,'message':f"Finding closed: {cur.get('finding_id',key)} {cur.get('title','')}"})

    summary={
      'generated_at':datetime.now(timezone.utc).isoformat(),
      'baseline':str(baseline),
      'current':str(current),
      'partial_comparison':args.partial,
      'minimum_finding_severity':args.minimum_severity,
      'blocking_regressions':regressions,
      'scope_changes':scope,
      'improvements':improvements,
      'result':'FAIL' if regressions or (args.strict_scope and scope) else 'PASS'
    }
    (out/'regression-summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    (out/'regression-summary.md').write_text(markdown(summary),encoding='utf-8')
    print(json.dumps({'result':summary['result'],'regressions':len(regressions),'scope_changes':len(scope),'improvements':len(improvements)}))
    return 2 if summary['result']=='FAIL' else 0

if __name__=='__main__':
    try: sys.exit(main())
    except Exception as e:
        print(f'ERROR: {type(e).__name__}: {e}',file=sys.stderr); sys.exit(1)
