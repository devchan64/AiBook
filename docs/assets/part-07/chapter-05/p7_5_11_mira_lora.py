#!/usr/bin/env python3
"""Prepare reviewed Mira pairs and run a pinned Musubi Edit-2511 LoRA pipeline.

Preparation uses only Python's standard library; no GPU or model download.
See P7-5.11 for the identity-learning hypothesis and held-out evaluation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
PIN = "e0cbd8f3dfe38365b10f8bc790b980f8894e8ba1"
MODEL = "Qwen/Qwen-Image-Edit-2511"
CONFIG = Path(__file__).parent / "p7-5-11/datasets/p7-5-11-mira-lora-config.json"


def sha(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local(path):
    p = Path(path)
    return (ROOT / p).resolve() if not p.is_absolute() else p.resolve()


def weight_path(path):
    # HF snapshot names carry the format; their blob targets have no extension.
    p = Path(path)
    return ROOT / p if not p.is_absolute() else p


def inventory(output):
    """Only currently embedded manuscript images, not discarded experiment globs."""
    require(not output.exists(), f"Output already exists: {output}")
    rows, seen = [], set()
    for section in (2, 9):
        manuscript = ROOT / f"docs/parts/part-07/chapter-05/section-{section:02}.md"
        for label, url in re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", manuscript.read_text()):
            image = (manuscript.parent / url).resolve()
            require(image.is_relative_to(ROOT / 'docs/assets'), f"Not a local asset: {url}")
            digest = sha(image)
            if digest in seen:
                continue
            seen.add(digest)
            record = image.with_name(image.stem + "-result.json")
            require(record.is_file(), f"Missing generation record: {record}")
            data = read(record)
            design = data.get('design', {})
            # Group suggestions are reviewed together with captions, never automatic labels.
            group = design.get('family') or ("camera" if "yaw-" in image.name else "reference")
            rows.append({"id": image.stem, "source_section": f"P7-5.{section}",
                         "image": str(image.relative_to(ROOT)), "sha256": digest,
                         "record": str(record.relative_to(ROOT)), "record_sha256": sha(record),
                         "label": label, "group": group, "split": "pending",
                         "caption": "", "review_note": ""})
    output.parent.mkdir(parents=True, exist_ok=True)
    write(output, {"schema_version": 1, "model_id": MODEL, "trigger": "mira_person", "items": rows})
    return {"status": "candidate_inventory", "count": len(rows), "manifest": str(output)}


def validate(manifest):
    require(manifest.get('model_id') == MODEL, "Expected Edit-2511 manifest")
    require(manifest.get('schema_version') == 1, "Unsupported manifest schema")
    trigger = manifest.get('trigger', '')
    require(trigger and isinstance(trigger, str), "Missing trigger")
    ids, hashes, groups = set(), set(), {}
    selected = {"train": [], "validation": []}
    for item in manifest['items']:
        key = item['id']
        require(key not in ids, f"Duplicate id: {key}")
        ids.add(key)
        split = item['split']
        require(split in ('pending', 'exclude', 'train', 'validation'), f"Invalid split: {key}")
        if split not in selected:
            continue
        require(item.get('review_note', '').strip(), f"Review note required: {key}")
        caption = item.get('caption', '').strip()
        require(trigger in caption and '\n' not in caption, f"Single-line caption with trigger required: {key}")
        require(item.get('group', '').strip(), f"Group required: {key}")
        group = item['group']
        require(groups.setdefault(group, split) == split, f"Group leakage: {group}")
        image, record = local(item['image']), local(item['record'])
        require(image.is_relative_to(ROOT / 'docs/assets'), f"Image outside assets: {key}")
        require(record.is_relative_to(ROOT / 'docs/assets'), f"Record outside assets: {key}")
        require(sha(image) == item['sha256'], f"Image changed: {key}")
        require(sha(record) == item['record_sha256'], f"Generation record changed: {key}")
        require(read(record).get('output', {}).get('sha256') == item['sha256'], f"Record/image mismatch: {key}")
        require(item['sha256'] not in hashes, f"Duplicate image content: {key}")
        hashes.add(item['sha256'])
        selected[split].append(item)
    require(len(selected['train']) >= 2, "Select at least two reviewed train images")
    require(selected['validation'], "Select at least one held-out validation image")
    return selected


def settings(config):
    require(config['model_id'] == MODEL and config['trainer_commit'] == PIN, "Model or trainer pin mismatch")
    t = config['training']
    for key in ('resolution', 'control_resolution', 'rank', 'alpha', 'steps', 'save_every'):
        require(type(t[key]) is int and t[key] > 0, f"Positive integer required: {key}")
    require(t['resolution'] % 32 == 0 and t['control_resolution'] % 32 == 0, "Resolutions must be multiples of 32")
    require(type(t['blocks_to_swap']) is int and 0 <= t['blocks_to_swap'] <= 59, "blocks_to_swap must be 0..59")
    require(math.isfinite(t['learning_rate']) and t['learning_rate'] > 0, "Invalid learning rate")
    require(type(t['seed']) is int and t['seed'] >= 0, "Invalid seed")
    for key in ('fp8_base', 'fp8_scaled', 'fp8_vl'):
        require(type(t[key]) is bool, f"Boolean required: {key}")
    require(not t['fp8_scaled'] or t['fp8_base'], "fp8_scaled requires fp8_base")
    require(t.get('text_encoder_device', 'cuda') in ('cpu', 'cuda'), 'Invalid text encoder device')
    require(t.get('text_encoder_device', 'cuda') != 'cpu' or not t['fp8_vl'], 'CPU text caching requires BF16, not fp8_vl')
    return t


def prepare(manifest_path, config_path, output):
    manifest, config = read(manifest_path), read(config_path)
    selected, t = validate(manifest), settings(config)
    require(not output.exists(), f"Output already exists: {output}")
    train = sorted(selected['train'], key=lambda x: x['id'])
    pairs = {"train": [], "validation": []}
    for split in pairs:
        for i, target in enumerate(sorted(selected[split], key=lambda x: x['id'])):
            # Validation controls come only from training, never from held-out targets.
            choices = [x for x in train if x['sha256'] != target['sha256']]
            control = choices[i % len(choices)]
            pairs[split].append({"image_path": str(local(target['image'])),
                                 "control_path": str(local(control['image'])),
                                 "caption": target['caption']})
    output.mkdir(parents=True)
    for split, rows in pairs.items():
        (output / f'{split}.jsonl').write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in rows))
    # Only train.jsonl is referenced by the training configuration.
    toml = ('[general]\n' + f'resolution = [{t["resolution"]}, {t["resolution"]}]\n'
            'batch_size = 1\nenable_bucket = true\nbucket_no_upscale = true\n\n[[datasets]]\n'
            f'image_jsonl_file = {json.dumps(str(output / "train.jsonl"))}\n'
            f'cache_directory = {json.dumps(str(output / "cache"))}\n'
            f'control_resolution = [{t["control_resolution"]}, {t["control_resolution"]}]\nnum_repeats = 1\n')
    (output / 'dataset.toml').write_text(toml)
    write(output / 'manifest.json', manifest)
    write(output / 'config.json', config)
    lock = {"status": "prepared_not_trained", "trainer_commit": PIN,
            "counts": {k: len(v) for k, v in pairs.items()},
            "files": {n: sha(output / n) for n in ('train.jsonl', 'validation.jsonl', 'dataset.toml', 'manifest.json', 'config.json')}}
    write(output / 'package.json', lock)
    return lock


def commands(package, trainer, python):
    c = read(package / 'config.json')
    t = settings(c)
    model_paths = {k: str(weight_path(v['path'])) if v['path'] else f'<{k.upper()}_SAFETENSORS>' for k, v in c['weights'].items()}
    common = ['--dataset_config', str(package / 'dataset.toml'), '--model_version', 'edit-2511']
    script = lambda n: str(trainer / 'src/musubi_tuner' / n)
    latent = [str(python), script('qwen_image_cache_latents.py'), *common, '--vae', model_paths['vae'], '--batch_size', '1', '--num_workers', '1']
    text = [str(python), script('qwen_image_cache_text_encoder_outputs.py'), *common, '--text_encoder', model_paths['text_encoder'], '--batch_size', '1', '--num_workers', '1']
    text.extend(['--device', t.get('text_encoder_device', 'cuda')])
    if t['fp8_vl']:
        text.append('--fp8_vl')
    train = [str(python), '-m', 'accelerate.commands.launch', '--num_processes', '1', '--num_machines', '1', '--mixed_precision', 'bf16',
             '--num_cpu_threads_per_process', '1', script('qwen_image_train_network.py'), *common,
             '--dit', model_paths['dit'], '--vae', model_paths['vae'], '--text_encoder', model_paths['text_encoder'],
             '--sdpa', '--mixed_precision', 'bf16', '--timestep_sampling', 'shift', '--discrete_flow_shift', '2.2',
             '--weighting_scheme', 'none', '--optimizer_type', 'adamw8bit', '--learning_rate', str(t['learning_rate']),
             '--gradient_checkpointing', '--max_data_loader_n_workers', '0', '--network_module', 'networks.lora_qwen_image',
             '--network_dim', str(t['rank']), '--network_alpha', str(t['alpha']), '--max_train_steps', str(t['steps']),
             '--save_every_n_steps', str(min(t['save_every'], t['steps'])), '--seed', str(t['seed']),
             '--blocks_to_swap', str(t['blocks_to_swap']), '--output_dir', str(package / 'checkpoints'), '--output_name', 'mira_identity']
    for key in ('fp8_base', 'fp8_scaled', 'fp8_vl'):
        if t[key]:
            train.append('--' + key)
    return [('cache_latents', latent), ('cache_text', text), ('train', train)]


def check_package(package):
    lock = read(package / 'package.json')
    for name, digest in lock['files'].items():
        require(sha(package / name) == digest, f"Prepared file changed: {name}; create a new package")
    validate(read(package / 'manifest.json'))
    require(lock['trainer_commit'] == PIN, "Package trainer mismatch")


def run(package, trainer, python, execute):
    check_package(package)
    plan = commands(package, trainer, python)
    if not execute:
        return {"status": "plan_only", "commands": {k: shlex.join(v) for k, v in plan},
                "note": "No model or GPU loaded; local weights/environment still require preflight."}
    require(python.is_file(), f"Missing trainer Python: {python}")
    revision = subprocess.check_output(['git', '-C', str(trainer), 'rev-parse', 'HEAD'], text=True).strip()
    require(revision == PIN, f"Expected Musubi commit {PIN}, got {revision}")
    require(not subprocess.check_output(['git', '-C', str(trainer), 'status', '--porcelain', '--untracked-files=no'], text=True).strip(), 'Trainer tracked files are modified')
    config = read(package / 'config.json')
    for role in ('dit', 'vae', 'text_encoder'):
        w = config['weights'][role]
        require(w['path'] and w['sha256'] and w['repo_id'] and w['revision'], f"Configure path/hash/source revision for {role}")
        path = weight_path(w['path'])
        require(path.suffix == '.safetensors' and path.is_file(), f"Expected local safetensors file: {path}")
        require(not re.search(r'-\d+-of-\d+', path.name), 'Use a complete single-file checkpoint, not one shard')
        require(sha(path) == w['sha256'], f"Weight checksum mismatch: {role}")
    # The wrapper does not download weights or tokenizer assets during training.
    env = os.environ.copy()
    env.update({'HF_HUB_OFFLINE': '1', 'TRANSFORMERS_OFFLINE': '1',
                'HF_HOME': str(ROOT / '.tmp/download/huggingface'),
                'HF_HUB_CACHE': str(ROOT / '.tmp/download/huggingface/hub'),
                'PYTHONUNBUFFERED': '1', 'PYTHONPATH': str(trainer / 'src'),
                'TOKENIZERS_PARALLELISM': 'false'})
    for name in ('cache', 'checkpoints', 'logs', 'run-result.json'):
        require(not (package / name).exists(), f"Existing run artifact: {name}; prepare a new package")
    subprocess.run([str(python), '-c', 'import torch, accelerate, bitsandbytes; assert torch.cuda.is_available(), "CUDA required"; assert torch.cuda.is_bf16_supported(), "BF16 required"'], check=True, env=env, cwd=trainer)
    subprocess.run([str(python), '-c',
                    'from transformers import Qwen2Tokenizer, Qwen2VLProcessor; '
                    'Qwen2Tokenizer.from_pretrained("Qwen/Qwen-Image", subfolder="tokenizer", local_files_only=True); '
                    'Qwen2VLProcessor.from_pretrained("Qwen/Qwen-Image-Edit", subfolder="processor", local_files_only=True)'],
                   check=True, env=env, cwd=trainer)
    # Check the installed CLI before loading any weights.
    for _, cmd in plan:
        entry = next(x for x in cmd if x.endswith('.py'))
        help_text = subprocess.check_output([str(python), entry, '--help'], text=True, env=env, cwd=trainer)
        for flag in cmd[cmd.index(entry) + 1:]:
            if flag.startswith('--'):
                require(flag in help_text, f"Unsupported option: {flag}")
    (package / 'logs').mkdir()
    result = {'status': 'running', 'trainer_commit': revision, 'wrapper_sha256': sha(__file__),
              'package_sha256': sha(package / 'package.json'), 'steps': []}
    write(package / 'run-result.json', result)
    try:
        for stage, cmd in plan:
            started = time.time()
            print(f'Running {stage}; log: {package / "logs" / (stage + ".log")}', flush=True)
            with (package / 'logs' / (stage + '.log')).open('w') as log:
                proc = subprocess.run(cmd, cwd=trainer, env=env, stdout=log, stderr=subprocess.STDOUT)
            result['steps'].append({'stage': stage, 'command': cmd, 'returncode': proc.returncode,
                                    'elapsed_seconds': round(time.time() - started, 2)})
            write(package / 'run-result.json', result)
            require(proc.returncode == 0, f"{stage} failed: inspect its log")
        checkpoints = sorted((package / 'checkpoints').glob('*.safetensors'))
        require(checkpoints, 'Trainer exited without a LoRA checkpoint')
        result.update(status='trained_not_evaluated', checkpoints=[{'path': str(p), 'sha256': sha(p)} for p in checkpoints])
    except BaseException as error:
        result.update(status='failed', error=str(error))
        raise
    finally:
        write(package / 'run-result.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    p = sub.add_parser('inventory')
    p.add_argument('--output', type=Path, default=ROOT / '.tmp/p7-5-11/mira-candidates.json')
    p = sub.add_parser('prepare')
    p.add_argument('--manifest', type=Path, required=True)
    p.add_argument('--config', type=Path, default=CONFIG)
    p.add_argument('--output', type=Path, required=True)
    p = sub.add_parser('run')
    p.add_argument('--package', type=Path, required=True)
    p.add_argument('--trainer', type=Path, required=True)
    p.add_argument('--python', type=Path, required=True, help='Python executable in the separate Musubi environment')
    p.add_argument('--execute', action='store_true', help='Run GPU caching and training; default prints plan only')
    args = parser.parse_args()
    try:
        if args.action == 'inventory':
            result = inventory(args.output.resolve())
        elif args.action == 'prepare':
            result = prepare(args.manifest, args.config, args.output.resolve())
        else:
            result = run(args.package.resolve(), args.trainer.resolve(), args.python.absolute(), args.execute)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        parser.exit(2, f'Error: {error}\n')


if __name__ == '__main__':
    main()
