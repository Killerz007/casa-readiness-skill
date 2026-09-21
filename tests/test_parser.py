import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('sync',ROOT/'scripts/sync_official_spec.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

class ParserTests(unittest.TestCase):
    def test_spec_parser(self):
        text="""# App Defense Alliance CASA Specification\nVersion 9.9.9 - 2099-01-01\n# 1 Authentication\n## 1.1 Example section\n### Scope\n- Web application\n### Audit\n| Spec | Description |\n| --- | --- |\n| [1.1.1](x) | Example requirement |\n""" + '\n'.join(f'| [1.1.{i}](x) | Requirement {i} |' for i in range(2,25))
        controls=mod.parse_spec(text)
        self.assertEqual(controls[0]['id'],'1.1.1')
        self.assertIn('Web application',controls[0]['scope'])

    def test_section_text_final_section(self):
        block="**Verification**\n\n*AL1*\n1. one\n\n*AL2*\n1. two\n"
        levels=mod.split_levels(mod.section_text(block,'Verification',[]))
        self.assertIn('one', levels['AL1'])
        self.assertIn('two', levels['AL2'])

    def test_version(self):
        self.assertEqual(mod.component_version('Version 2.1.1 - 2026-06-03\n'),('2.1.1','2026-06-03'))

if __name__=='__main__': unittest.main()
