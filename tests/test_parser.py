import importlib.util, json, unittest
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

    def test_shared_level_heading_applies_to_both_levels(self):
        # The official guide uses "*AL1 and AL2*" when one block covers both assurance levels.
        block="**Verification**\n\n*AL1 and AL2*\n1. shared rule\n2. second rule\n\n\n---\n"
        levels=mod.split_levels(mod.section_text(block,'Verification',[]))
        self.assertEqual(levels['AL1'],'1. shared rule\n2. second rule')
        self.assertEqual(levels['AL2'],'1. shared rule\n2. second rule')

    def test_trailing_horizontal_rule_is_stripped(self):
        levels=mod.split_levels("*AL2*\n1. only\n\n---\n")
        self.assertEqual(levels['AL2'],'1. only')
        self.assertEqual(levels['AL1'],'')

    def test_version(self):
        self.assertEqual(mod.component_version('Version 2.1.1 - 2026-06-03\n'),('2.1.1','2026-06-03'))

class PinnedOfficialFilesTests(unittest.TestCase):
    """Parse the pinned official files so a regression in the parser cannot ship silently."""
    def setUp(self):
        self.spec_text=(ROOT/'official/current/CASA-Specification.md').read_text(encoding='utf-8')
        self.guide_text=(ROOT/'official/current/CASA-Test-Guide.md').read_text(encoding='utf-8')

    def test_every_control_has_complete_al2_data(self):
        controls,tests=mod.build_catalogues(self.spec_text,self.guide_text)
        self.assertEqual(len(controls),len(tests))
        for cid,entry in tests.items():
            for field in ('test_procedure','verification'):
                self.assertTrue(entry[field]['AL2'],f'{cid} has empty AL2 {field}')
                self.assertFalse(entry[field]['AL2'].rstrip().endswith('---'),f'{cid} {field} leaks separator')

    def test_generated_file_matches_pinned_source(self):
        controls,tests=mod.build_catalogues(self.spec_text,self.guide_text)
        generated=json.loads((ROOT/'references/casa-test-cases.generated.json').read_text(encoding='utf-8'))['controls']
        self.assertEqual(generated,tests,'references/casa-test-cases.generated.json is stale; run scripts/sync_official_spec.py --rebuild-local')

if __name__=='__main__': unittest.main()
