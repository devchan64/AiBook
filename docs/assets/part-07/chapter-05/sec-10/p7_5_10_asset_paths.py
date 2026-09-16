"""생성 당시 경로를 현재 자산으로 연결하며 과거 기록의 바이트·해시를 보존한다."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = Path(__file__).resolve().parent
ALIASES = json.loads((BASE / 'p7-5-10-asset-migration.json').read_text())['path_aliases']


def asset_path(value):
    """sec-11/sec-12의 이전 경로와 파일명을 이관 목록으로 해석한다."""
    path = Path(value)
    path = ROOT / path if not path.is_absolute() else path
    path = path.resolve()
    if path.is_relative_to(ROOT):
        destination = ALIASES.get(path.relative_to(ROOT).as_posix())
        if destination:
            return (ROOT / destination).resolve()
    return path
