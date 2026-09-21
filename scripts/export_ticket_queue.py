#!/usr/bin/env python3
"""Generate a portable GitHub/Jira-ready queue from structured CASA findings.

This script does not create external tickets. External mutation remains an explicitly
authorized agent/connector action as defined in references/ticket-integration.md.
"""
import argparse, json, sys
from datetime import datetime, timezone
from pathlib import Path

SEVERITY={'Observation':0,'Low':1,'Medium':2,'High':3,'Critical':4}
PRIORITY={'Critical':'highest','High':'high','Medium':'normal','Low':'low','Observation':'backlog'}

def open_finding(item):
    return str(item.get('status','')).lower() not in {'closed','resolved','accepted-risk'}

def body(item,commit):
    controls=', '.join(item.get('casa_controls') or [])
    cwe=', '.join(item.get('cwe') or [])
    evidence=', '.join(item.get('evidence_ids') or [])
    return f"""**Finding ID:** {item.get('finding_id','')}
**Regression key:** `{item.get('regression_key') or item.get('finding_id','')}`
**Severity:** {item.get('rating','')}
**CASA requirements:** {controls}
**CWE:** {cwe or 'N/A'}
**Assessment commit:** `{commit or 'not recorded'}`

## Finding

{item.get('audit_finding','')}

## Risk and implication

{item.get('risk_and_implication','')}

## Remediation

{item.get('recommendation','')}

## Implementation guidance

{item.get('implementation_guidance','')}

## Retest criteria

{item.get('retest_criteria','')}

## Evidence references

{evidence or 'See assessment evidence index.'}

> This work item tracks remediation of an independent CASA readiness finding. Ticket closure does not itself establish CASA control closure; retest evidence is required.
"""

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--assessment-dir',required=True)
    ap.add_argument('--output',default='')
    ap.add_argument('--minimum-severity',choices=list(SEVERITY),default='Low')
    ap.add_argument('--include-observations',action='store_true')
    args=ap.parse_args()
    base=Path(args.assessment_dir)
    fpath=base/'05-findings-register.jsonl'
    if not fpath.exists(): raise FileNotFoundError(fpath)
    manifest={}
    mpath=base/'00-assessment-manifest.json'
    if mpath.exists(): manifest=json.loads(mpath.read_text(encoding='utf-8'))
    commit=manifest.get('application_commit_sha')
    threshold=SEVERITY[args.minimum_severity]
    queue=[]
    for lineno,line in enumerate(fpath.read_text(encoding='utf-8').splitlines(),1):
        if not line.strip(): continue
        item=json.loads(line)
        sev=item.get('rating','Observation')
        if not open_finding(item): continue
        if sev=='Observation' and not args.include_observations: continue
        if SEVERITY.get(sev,0)<threshold: continue
        key=item.get('regression_key') or item.get('finding_id')
        if not key: raise ValueError(f'finding at line {lineno} has no regression key/id')
        queue.append({
          'finding_id':item.get('finding_id'),
          'regression_key':key,
          'title':f"[CASA] {item.get('finding_id','')} - {item.get('title','')}",
          'severity':sev,
          'recommended_priority':PRIORITY.get(sev,'normal'),
          'casa_controls':item.get('casa_controls',[]),
          'dedupe_search_terms':[item.get('finding_id'),key],
          'body':body(item,commit)
        })
    out=Path(args.output) if args.output else base
    out.mkdir(parents=True,exist_ok=True)
    payload={
      'generated_at':datetime.now(timezone.utc).isoformat(),
      'assessment_commit':commit,
      'ticket_creation_authorized':False,
      'note':'Portable queue only. Search/deduplicate and obtain explicit authorization before creating external tickets.',
      'tickets':queue
    }
    (out/'13-finding-ticket-queue.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    md=['# CASA Finding Ticket Queue','',f"Open queued findings: **{len(queue)}**",'',
        '> Queue generation does not authorize external ticket creation.','']
    for t in queue:
        md += [f"## {t['title']}",'',f"- Severity: **{t['severity']}**",f"- Recommended priority: `{t['recommended_priority']}`",f"- Regression key: `{t['regression_key']}`",'',t['body'],'']
    (out/'13-finding-ticket-queue.md').write_text('\n'.join(md),encoding='utf-8')
    print(json.dumps({'queued':len(queue),'output':str(out)}))
    return 0

if __name__=='__main__':
    try: sys.exit(main())
    except Exception as e:
        print(f'ERROR: {type(e).__name__}: {e}',file=sys.stderr); sys.exit(1)
