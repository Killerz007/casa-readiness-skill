import csv, json, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'scripts/compare_assessments.py'
HEADER=['control_id','domain','requirement','scope','applicability','status','test_method','evidence_ids','finding_ids','adjudication_ids','rationale','assessor_notes']

def write_matrix(path,status,control='3.1.1'):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(HEADER); w.writerow([control,'3 Access Control','Least privilege','','Applicable',status,'runtime','E-1','','','',''])

class RegressionTests(unittest.TestCase):
    def test_pass_to_fail_blocks_ci(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); baseline=root/'baseline'; current=root/'current'; out=root/'out'
            baseline.mkdir(); current.mkdir()
            write_matrix(baseline/'04-casa-control-matrix.csv','PASS')
            write_matrix(current/'04-casa-control-matrix.csv','FAIL')
            (baseline/'05-findings-register.jsonl').write_text('')
            (current/'05-findings-register.jsonl').write_text('')
            p=subprocess.run([sys.executable,str(SCRIPT),'--baseline',str(baseline),'--current',str(current),'--output',str(out)],capture_output=True,text=True)
            self.assertEqual(p.returncode,2,p.stdout+p.stderr)
            result=json.loads((out/'regression-summary.json').read_text())
            self.assertEqual(result['result'],'FAIL')
            self.assertEqual(result['blocking_regressions'][0]['control_id'],'3.1.1')

    def test_partial_comparison_ignores_unretsted_absent_control(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); baseline=root/'baseline'; current=root/'current'; out=root/'out'
            baseline.mkdir(); current.mkdir()
            write_matrix(baseline/'04-casa-control-matrix.csv','PASS','3.1.1')
            with (current/'04-casa-control-matrix.csv').open('w',newline='',encoding='utf-8') as f:
                csv.writer(f).writerow(HEADER)
            (baseline/'05-findings-register.jsonl').write_text('')
            (current/'05-findings-register.jsonl').write_text('')
            p=subprocess.run([sys.executable,str(SCRIPT),'--baseline',str(baseline),'--current',str(current),'--output',str(out),'--partial'],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stdout+p.stderr)

if __name__=='__main__': unittest.main()
