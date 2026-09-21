import json, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'scripts/export_ticket_queue.py'

class TicketQueueTests(unittest.TestCase):
    def test_open_finding_generates_portable_ticket(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td)
            (base/'00-assessment-manifest.json').write_text(json.dumps({'application_commit_sha':'abc123'}))
            finding={
              'finding_id':'CASA-F-001',
              'regression_key':'3.1.1:authz:test',
              'title':'Authorization weakness',
              'rating':'High',
              'status':'Open',
              'casa_controls':['3.1.1'],
              'cwe':['CWE-862'],
              'audit_finding':'Server authorization is missing.',
              'risk_and_implication':'Unauthorized access may occur.',
              'recommendation':'Enforce server authorization.',
              'implementation_guidance':'Add a trusted service-layer check.',
              'retest_criteria':'Unauthorized request returns 403.',
              'evidence_ids':['E-001']
            }
            (base/'05-findings-register.jsonl').write_text(json.dumps(finding)+'\n')
            p=subprocess.run([sys.executable,str(SCRIPT),'--assessment-dir',str(base)],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stdout+p.stderr)
            queue=json.loads((base/'13-finding-ticket-queue.json').read_text())
            self.assertFalse(queue['ticket_creation_authorized'])
            self.assertEqual(len(queue['tickets']),1)
            self.assertEqual(queue['tickets'][0]['regression_key'],'3.1.1:authz:test')

if __name__=='__main__': unittest.main()
