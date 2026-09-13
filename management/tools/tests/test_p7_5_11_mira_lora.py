"""CPU-only packaging regressions. Synthetic review flags are test fixtures only."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location('mira_lora', ROOT / 'docs/assets/part-07/chapter-05/p7_5_11_mira_lora.py')
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest_path = self.root / 'candidates.json'
        M.inventory(self.manifest_path)
        self.manifest = M.read(self.manifest_path)
        self.manifest['items'] = self.manifest['items'][:3]
        for i, item in enumerate(self.manifest['items']):
            item.update(split='train' if i < 2 else 'validation', group=f'fixture-{i}',
                        caption='Create a front portrait of mira_person from Picture 1.',
                        review_note='Synthetic packaging test, not a visual approval')

    def package(self):
        M.write(self.manifest_path, self.manifest)
        output = self.root / 'package'
        M.prepare(self.manifest_path, M.CONFIG, output)
        return output

    def test_train_pairs_and_validation_are_disjoint(self):
        p = self.package()
        rows = [json.loads(x) for x in (p / 'train.jsonl').read_text().splitlines()]
        heldout = str(M.local(self.manifest['items'][2]['image']))
        for row in rows:
            self.assertNotEqual(row['image_path'], row['control_path'])
            self.assertNotIn(heldout, (row['image_path'], row['control_path']))
        config = tomllib.loads((p / 'dataset.toml').read_text())
        self.assertEqual(config['datasets'][0]['image_jsonl_file'], str(p / 'train.jsonl'))
        result = M.run(p, Path('/no-trainer'), Path('/no-python'), False)
        self.assertEqual(result['status'], 'plan_only')
        self.assertFalse((p / 'run-result.json').exists())
        self.assertEqual(set(result['commands']), {'cache_latents', 'cache_text', 'train'})
        self.assertIn('--model_version edit-2511', result['commands']['train'])

    def test_group_leakage_rejected(self):
        self.manifest['items'][2]['group'] = self.manifest['items'][0]['group']
        with self.assertRaisesRegex(ValueError, 'Group leakage'):
            self.package()
        self.assertFalse((self.root / 'package').exists())

    def test_pending_does_not_become_training_data(self):
        for row in self.manifest['items']:
            row['split'] = 'pending'
        with self.assertRaisesRegex(ValueError, 'two reviewed'):
            self.package()

    def test_hash_drift_rejected(self):
        self.manifest['items'][0]['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Image changed'):
            self.package()

    def test_duplicate_pixels_rejected(self):
        x = copy.deepcopy(self.manifest['items'][0])
        x['id'] = 'duplicate-with-new-name'
        self.manifest['items'].append(x)
        with self.assertRaisesRegex(ValueError, 'Duplicate image content'):
            self.package()

    def test_no_overwrite_or_mutable_prepared_config(self):
        p = self.package()
        with self.assertRaisesRegex(ValueError, 'already exists'):
            M.prepare(self.manifest_path, M.CONFIG, p)
        with (p / 'config.json').open('a') as f:
            f.write(' ')
        with self.assertRaisesRegex(ValueError, 'Prepared file changed'):
            M.check_package(p)

    def test_invalid_hyperparameters(self):
        config = M.read(M.CONFIG)
        config['training']['learning_rate'] = float('nan')
        with self.assertRaisesRegex(ValueError, 'learning rate'):
            M.settings(config)

    def test_weight_snapshot_link_keeps_format_and_checks_target(self):
        blob = self.root / 'blob-without-extension'
        blob.write_bytes(b'weight fixture')
        snapshot = self.root / 'vae.safetensors'
        snapshot.symlink_to(blob)
        path = M.weight_path(snapshot)
        self.assertEqual(path.suffix, '.safetensors')
        self.assertTrue(path.is_file())
        self.assertEqual(M.sha(path), M.sha(blob))
        p = self.package()
        config = M.read(p / 'config.json')
        config['weights']['vae']['path'] = str(snapshot)
        M.write(p / 'config.json', config)
        cmds = dict(M.commands(p, Path('/trainer'), Path('/python')))
        self.assertIn(str(snapshot), cmds['cache_latents'])
        self.assertNotIn(str(blob), cmds['cache_latents'])

    def test_cpu_text_cache_rejects_fp8_and_is_in_plan(self):
        config = M.read(M.CONFIG)
        config['training']['text_encoder_device'] = 'cpu'
        with self.assertRaisesRegex(ValueError, 'CPU text caching'):
            M.settings(config)
        config['training']['fp8_vl'] = False
        config_path = self.root / 'cpu-config.json'
        M.write(config_path, config)
        M.write(self.manifest_path, self.manifest)
        output = self.root / 'cpu-package'
        M.prepare(self.manifest_path, config_path, output)
        cmd = M.run(output, Path('/trainer'), Path('/python'), False)['commands']['cache_text']
        self.assertIn('--device cpu', cmd)
        self.assertNotIn('--fp8_vl', cmd)


if __name__ == '__main__':
    unittest.main()
