"""이관 전 생성 기록의 경로를 현재 자산 위치로 연결한다."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
OLD = ROOT / "docs/assets/part-07/chapter-05/sec-11"
NEW = OLD.with_name("sec-12")


def asset_path(value):
    """기존 기록의 바이트·해시를 유지하면서 이관된 파일을 찾는다."""
    path = Path(value)
    path = ROOT / path if not path.is_absolute() else path
    if path.is_relative_to(OLD):
        moved = NEW / path.relative_to(OLD)
        if moved.is_file():
            return moved.resolve()
    return path.resolve()
