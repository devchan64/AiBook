#!/usr/bin/env python3
"""생성 후보를 검수 목록으로 고르고, 선택한 항목만 데이터셋 JSON으로 만든다.

조작: review JSON의 status, split, caption, review_note를 수정한다.
관찰: 선택 수·분할 분포와 같은 목표/조건의 분할 누수를 확인한다.
이미지는 복사하지 않는다. 생성 목록과 별도로 여러 학습 목록을 만들 수 있다.
"""
import argparse
import json
from collections import Counter
from pathlib import Path

from p7_5_10_generate_supplements import ROOT, sha256, asset_path, result_id


def read(path):
    return json.loads(path.read_text())


def save_new(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as handle:
        handle.write(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def checked(path, digest):
    resolved = asset_path(path)
    if not resolved.is_relative_to(ROOT) or sha256(resolved) != digest:
        raise ValueError(f'File changed or outside repository: {path}')
    return resolved


def select(catalog, reviews, trigger):
    """채택 여부는 사람이 기록한다. 코드는 파일 무결성과 분할만 검사한다."""
    candidates = {x['id']: x for x in catalog['items']}
    if len(candidates) != len(catalog['items']):
        raise ValueError('Duplicate catalog IDs')
    selected, seen, groups, hashes = [], set(), {}, set()
    for review in reviews['items']:
        key = review['id']
        if key in seen or key not in candidates:
            raise ValueError(f'Duplicate or unknown review ID: {key}')
        seen.add(key)
        status = review['status']
        if status not in ('pending', 'accepted', 'rejected'):
            raise ValueError(f'Invalid review status: {key}')
        if status != 'accepted':
            continue
        row = candidates[key]
        if review.get('image_sha256') != row['sha256']:
            raise ValueError(f'Review belongs to a different image: {key}')
        split, caption = review['split'], review['caption'].strip()
        if split not in ('train', 'validation') or not review['review_note'].strip():
            raise ValueError(f'Split and review note required: {key}')
        if not caption or trigger not in caption or '\n' in caption:
            raise ValueError(f'Single-line caption containing {trigger} required: {key}')
        if row.get('reserved_split') not in (None, split):
            raise ValueError(f'Previously reserved target split cannot change: {key}')
        group = row['group']
        if groups.setdefault(group, split) != split:
            raise ValueError(f'Group leakage: {group}')
        checked(row['image'], row['sha256'])
        record = checked(row['record'], row['record_sha256'])
        if read(record)['output']['sha256'] != row['sha256']:
            raise ValueError(f'Record/image mismatch: {key}')
        if row['sha256'] in hashes:
            raise ValueError(f'Duplicate image content: {key}')
        hashes.add(row['sha256'])
        item = {k: row[k] for k in ('id','image','sha256','record','record_sha256','group')}
        item.update(split=split, caption=caption, review_note=review['review_note'])
        # 입력 생성은 역방향이다. 학습에서는 원래 Mira 이미지가 목표다.
        if row.get('target'):
            checked(row['target'], row['target_sha256'])
            target_group = 'target:' + row['target_sha256']
            if groups.setdefault(target_group, split) != split:
                raise ValueError(f'Target leakage: {key}')
            item.update(control_image=item.pop('image'), control_sha256=item.pop('sha256'),
                        image=row['target'], sha256=row['target_sha256'])
        item["input_result_id"] = result_id(item.get("control_sha256"))
        item["target_result_id"] = result_id(item["sha256"])
        side = "input" if row.get("target") else "target"
        identity = row.get("identifiers", {})
        for field in ("rule_id", "rule_revision", "condition_id"):
            item[side + "_" + field] = identity.get(field)
        selected.append(item)
    if not selected:
        raise ValueError('No accepted candidates; review images before exporting')
    paired = [bool(x.get('control_image')) for x in selected]
    if any(paired) and not all(paired):
        raise ValueError('Export paired inputs and target-only datasets separately')
    return {'schema_version':1, 'model_id':catalog['model_id'], 'trigger':trigger,
            'purpose':'paired_edit_training' if all(paired) else 'identity_training',
            'items':selected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['review-template','export'])
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--review', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--trigger', default='mira_person')
    args = parser.parse_args()
    catalog = read(args.catalog)
    if args.command == 'review-template':
        result = {'schema_version':1, 'catalog':str(args.catalog), 'items':[
            {'id':x['id'], 'status':'pending', 'split':'pending',
             'image_sha256':x['sha256'], 'caption':'', 'review_note':''}
            for x in catalog['items']]}
    else:
        if not args.review:
            parser.error('--review is required for export')
        result = select(catalog, read(args.review), args.trigger)
        result['catalog_sha256'] = sha256(args.catalog)
        result['review_sha256'] = sha256(args.review)
    save_new(args.output, result)
    print(json.dumps({'output':str(args.output), 'count':len(result['items']),
                      'splits':dict(Counter(x['split'] for x in result['items']))}))


if __name__ == '__main__':
    main()
