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
            spec = G.load_spec(path)
            before = copy.deepcopy(spec)
            G.bind_rule(path, spec)
            for original, row in zip(before['items'], spec['items']):
                self.assertEqual(original['prompt'], row['prompt'])
                self.assertEqual(row['identifiers']['condition_id'], row['id'])
                self.assertEqual(row['identifiers']['rule_id'], key)

    def test_wrong_rule_selection_fails_before_output(self):
        path = ASSETS / 'p7-5-10-bfs-proportion-input-pool-v1.json'
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, 'different rule'):
                G.generation_plan(Path(folder), path, G.load_spec(path),
                                  {'rule_id': 'P710-RULE-TARGET-002'})
            self.assertEqual(list(Path(folder).iterdir()), [])

    def test_empty_selection_never_requests_generation(self):
        path = ASSETS / 'p7-5-10-bfs-proportion-input-pool-v1.json'
        with tempfile.TemporaryDirectory() as folder:
            _, pending = G.generation_plan(Path(folder), path, G.load_spec(path),
                                          {'include_ids': [], 'rule_id': 'P710-RULE-INPUT-002',
                                           'rule_revision': 4})
            self.assertEqual(pending, [])

    def test_result_identity_is_shared_and_pending_is_null(self):
        data = json.loads((ASSETS / 'p7-5-10-paired-dataset.json').read_text())
        for row in data['items']:
            self.assertEqual(G.result_id(row['control_sha256']), row['input_result_id'])
            self.assertEqual(G.result_id(row['sha256']), row['target_result_id'])
        with self.assertRaises(ValueError):
            G.result_id('short-hash')


if __name__ == '__main__':
    unittest.main()
