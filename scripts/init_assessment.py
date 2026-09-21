#!/usr/bin/env python3
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--project', required=True)
    ap.add_argument('--commit', required=True)
    ap.add_argument('--repository', default='')
    ap.add_argument('--environment', default='')
    ap.add_argument('--target-url', default='')
    ap.add_argument('--mode', choices=['scope','full','retest','evidence-pack','delta','regression'], default='full')
    ap.add_argument('--authorization', choices=['authorized-runtime','source-review-only','unknown'], default='unknown')
    ap.add_argument('--ticket-mode', choices=['off','queue','github','jira','auto'], default='queue')
    ap.add_argument('--authorize-ticket-creation', action='store_true')
    ap.add_argument('--output-root', default='casa-assessment')
    args=ap.parse_args()
    root=Path(__file__).resolve().parents[1]
    manifest=json.loads((root/'official/upstream-manifest.json').read_text())
    date=datetime.now(timezone.utc).date().isoformat()
    slug=''.join(c.lower() if c.isalnum() else '-' for c in args.project).strip('-')
    out=Path(args.output_root)/f'{date}-{slug}'
    for d in ['evidence/raw','evidence/normalized','evidence/screenshots','evidence/runtime','evidence/code']:
        (out/d).mkdir(parents=True,exist_ok=True)
    assessment={
      'project_name':args.project,
      'repository':args.repository or None,
      'application_commit_sha':args.commit,
      'assessment_mode':args.mode,
      'target_environment':args.environment or None,
      'target_url':args.target_url or None,
      'authorization_status':args.authorization,
      'ticket_mode':args.ticket_mode,
      'external_ticket_creation_authorized':bool(args.authorize_ticket_creation),
      'started_at_utc':datetime.now(timezone.utc).isoformat(),
      'casa_component_version':manifest['casa_component_version'],
      'upstream_release':manifest['latest_repository_release'],
      'upstream_release_commit_sha':manifest.get('release_commit_sha'),
      'official_source_last_checked_utc':manifest.get('last_checked_utc')
    }
    (out/'00-assessment-manifest.json').write_text(json.dumps(assessment,indent=2)+'\n')
    templates=root/'templates'
    for src,dst in [
      ('control-matrix.csv','04-casa-control-matrix.csv'),
      ('adjudication-log.jsonl','04-adjudication-log.jsonl'),
      ('findings-register.jsonl','05-findings-register.jsonl'),
      ('scanner-register.csv','08-scanner-register.csv'),
      ('evidence-index.csv','09-evidence-index.csv'),
      ('remediation-register.csv','06-remediation-register.csv'),
      ('test-procedure-traceability.csv','11-test-procedure-traceability.csv'),
      ('report-rendering-manifest.json','12-report-rendering-manifest.json')]:
        (out/dst).write_text((templates/src).read_text())
    print(out)
if __name__=='__main__': main()
