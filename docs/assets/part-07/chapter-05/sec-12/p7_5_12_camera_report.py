"""새 입력의 LoRA 출력 비교표를 갱신한다. --watch는 생성 종료까지 갱신한다."""
import argparse
import hashlib
import json
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent


def update():
    """완료 기록과 해시가 일치하는 출력만 비교표에 표시한다."""
    folder = BASE / "codex-camera-lora-v1"
    jobs = json.loads((BASE / "codex-camera-inputs-v1/generation-manifest.json").read_text())["jobs"]
    state_path = folder / "state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    rows, completed = [], 0
    for index, job in enumerate(jobs, 1):
        key = job["id"] + "-lora"
        image, record = folder / (key + ".png"), folder / (key + "-result.json")
        result = "생성 대기"
        if record.exists():
            data = json.loads(record.read_text())
            assert hashlib.sha256(image.read_bytes()).hexdigest() == data["output_sha256"]
            result = f'![LoRA 적용]({image.name})'
            completed += 1
        rows.append(f'| P712-CAM-{index:03d} · {job["id"]} | ![입력](../codex-camera-inputs-v1/{job["image"]}) | {result} |')
    content = ["# P7-5.12 새 합성 입력 45장 LoRA 적용", "",
               f'생성 완료: **{completed}/{len(jobs)}장** · 상태: `{state.get("status", "waiting")}`. 생성 완료는 시각 검수 통과를 뜻하지 않는다.', "",
               "최종 1600스텝 LoRA, 강도 1.0, 시드 62294, 20스텝, CFG 4.0, 출력·참조 VAE 512×512. 입력 한 장만 전달하며 목표 얼굴 참조는 사용하지 않는다. 남성·여성·유아 모두 같은 편집 지시를 사용한다.", "",
               "각도는 생성 요청 범주이며 측정값이 아니다. 얼굴·헤어·화풍 변화와 자세·표정·배경 보존을 나누어 확인한다.", "",
               "[실행 조건 JSON](plan.json)", "", "[진행 상태 JSON](state.json)", "",
               "| 관리번호·입력 | 입력 | LoRA 적용 |", "| --- | --- | --- |", *rows, ""]
    target = folder / "README.md"
    value = "\n".join(content)
    if not target.exists() or target.read_text() != value:
        temp = target.with_suffix(".tmp")
        temp.write_text(value)
        temp.replace(target)
    return state.get("status")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--watch", action="store_true")
    args = parser.parse_args()
    while True:
        status = update()
        if not args.watch or status in ("failed", "generated_pending_visual_review"):
            break
        time.sleep(15)
