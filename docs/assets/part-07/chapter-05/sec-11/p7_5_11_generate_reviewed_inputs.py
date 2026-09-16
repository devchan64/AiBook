#!/usr/bin/env python3
"""폐기 목록을 적용하여 입력 후보를 생성한다.

원래 생성 목록과 생성 코드를 보존한다. --dry-run으로 제외 ID와 실행 대상을 확인한다.
"""
import argparse
import fcntl
import json
from pathlib import Path

import p7_5_11_generate_supplements as generator

BASE = Path(__file__).resolve().parent


def main(policy_name='p7-5-11-input-generation-exclusions.json',
         spec_name='p7-5-11-bfs-input-pool-v2.json', output_name='input-images'):
    """입력·목표별 제외 정책을 적용하고 기존 생성기로 전달한다."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec', type=Path, default=BASE / spec_name)
    parser.add_argument('--output-dir', type=Path, default=BASE / output_name)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--limit', type=int)
    parser.add_argument('--wait-for-gpu', action='store_true')
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error('--limit must be positive')
    policy = json.loads((BASE / policy_name).read_text())
    spec = json.loads(args.spec.read_text())
    assert generator.sha256(args.spec) == policy['spec_sha256'], 'Unexpected generation spec'
    excluded = {x['id'] for x in policy['items']}
    original_count = len(spec['items'])
    assert excluded <= {x['id'] for x in spec['items']}
    spec['items'] = [x for x in spec['items'] if x['id'] not in excluded]
    for ref in spec['references'].values():
        assert generator.sha256(generator.ROOT / ref['path']) == ref['sha256']
    print(json.dumps({'planned_count': original_count, 'eligible_count': len(spec['items']),
                      'excluded_ids': sorted(excluded)}, ensure_ascii=False))
    if args.dry_run:
        return
    # 필터링한 목록만 원래 생성기에 전달한다. 기존 생성물의 원본 지문은 바꾸지 않는다.
    original_catalog = generator.catalog

    def catalog(out, active_spec, fingerprint):
        original_catalog(out, active_spec, fingerprint)
        path = out / 'candidate-catalog.json'
        data = json.loads(path.read_text())
        data.update(planned_count=original_count, discarded_count=len(excluded),
                    discarded_items=policy['items'])
        generator.write(path, data)

    generator.catalog = catalog
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    with (out / '.lock').open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        generator.run(out, args.spec, spec, args.limit, args.wait_for_gpu)


if __name__ == '__main__':
    main()
