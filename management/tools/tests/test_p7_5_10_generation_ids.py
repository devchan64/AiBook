"""공통 ID가 재생성·규칙 혼용으로 이어지지 않는지 CPU에서 확인한다."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
ASSETS = ROOT / 'docs/assets/part-07/chapter-05/sec-10'
sys.path.insert(0, str(ASSETS))
import p7_5_10_generate_supplements as G


class GenerationIdTests(unittest.TestCase):
    def test_registered_rules_preserve_prompts_and_resolve_components(self):
        registry = json.loads((ASSETS / 'p7-5-10-paired-dataset.json').read_text())
        for key, rule in registry['generation_rules'].items():
            path = ROOT / rule['spec']
            spec = G.load_spec(path, key)
            before = copy.deepcopy(spec)
            G.bind_rule(path, spec)
            for original, row in zip(before['items'], spec['items']):
                self.assertEqual(original['prompt'], row['prompt'])
                self.assertEqual(row['identifiers']['condition_id'], row['id'])
                self.assertEqual(row['identifiers']['rule_id'], key)

    def test_wrong_rule_selection_fails_before_output(self):
        path = ASSETS / 'p7-5-10-image-generation.json'
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, 'different rule'):
                G.generation_plan(Path(folder), path, G.load_spec(path),
                                  {'rule_id': 'P710-RULE-TARGET-002'})
            self.assertEqual(list(Path(folder).iterdir()), [])

    def test_empty_selection_never_requests_generation(self):
        path = ASSETS / 'p7-5-10-image-generation.json'
        with tempfile.TemporaryDirectory() as folder:
            _, pending = G.generation_plan(Path(folder), path, G.load_spec(path),
                                          {'include_ids': [], 'rule_id': 'P710-RULE-INPUT-002',
                                           'rule_revision': 6})
            self.assertEqual(pending, [])

    def test_result_identity_is_shared_and_pending_is_null(self):
        data = json.loads((ASSETS / 'p7-5-10-paired-dataset.json').read_text())
        for row in data['items']:
            self.assertEqual(G.result_id(row['control_sha256']), row['input_result_id'])
            self.assertEqual(G.result_id(row['sha256']), row['target_result_id'])
        with self.assertRaises(ValueError):
            G.result_id('short-hash')

    def test_completed_groups_are_reused_with_exclusions(self):
        path = ASSETS / 'p7-5-10-image-generation.json'
        for key in json.loads(path.read_text())['rules']:
            spec = G.load_spec(path, key)
            state, pending = G.generation_plan(ROOT / spec['output_dir'], path, spec)
            self.assertEqual(pending, [])
            self.assertTrue(state['reuse_catalog'])

    def test_unknown_management_id_is_rejected(self):
        data = json.loads((ASSETS / 'p7-5-10-image-generation.json').read_text())
        data['selection']['include_management_ids'] = ['P710-PROP-999']
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'generation.json'
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, 'management IDs'):
                G.load_spec(path)

    def test_storage_cannot_be_redirected(self):
        data = json.loads((ASSETS / 'p7-5-10-image-generation.json').read_text())
        data['storage']['input_images'] = '.tmp/another-image-folder'
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'generation.json'
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, 'canonical'):
                G.load_spec(path)

    def test_rules_share_role_directories(self):
        path = ASSETS / 'p7-5-10-image-generation.json'
        first = G.load_spec(path, 'P710-RULE-INPUT-001')
        second = G.load_spec(path, 'P710-RULE-INPUT-002')
        self.assertEqual(first['_image_dir'], second['_image_dir'])
        self.assertTrue(first['_image_dir'].endswith('training-images/input-images'))
        for key in json.loads(path.read_text())['rules']:
            spec = G.load_spec(path, key)
            self.assertEqual(Path(spec['output_dir']).parent, ASSETS.relative_to(ROOT) / 'generation-records')


if __name__ == '__main__':
    unittest.main()
