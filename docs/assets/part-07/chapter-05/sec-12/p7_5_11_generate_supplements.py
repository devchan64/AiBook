#!/usr/bin/env python3
"""방향별 참조와 JSON 생성 목록으로 Mira 학습 후보를 순차 생성한다.

조작: --spec의 장면·시드·참조를 바꾸고 --output-dir을 새로 지정한다.
관찰: PNG의 얼굴·헤어·지시 준수와 결과 JSON의 입력·출력 해시를 비교한다.
--dry-run은 목록만 확인한다. 생성 완료는 학습 후보의 채택을 뜻하지 않는다.
가중치는 model_weight_manager.py로 준비한 .tmp/download 캐시만 읽는다.
"""

from p7_5_12_asset_paths import asset_path

import argparse
import fcntl
import json
import re
import time
import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sec-02"))
from p7_5_2_qwen_edit_2511_generate_mira_torso import (
    ASSETS,
    ROOT,
    CACHE_DIR,
    MODEL_ID,
    sha256,
    runtime_record,
)


def write(path, data):
    """중간 저장 파일을 교체해 불완전한 JSON이 상태 파일로 남지 않게 한다."""
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(path)


def catalog(out, spec, fingerprint):
    """생성물 전체를 나열한다. 검수와 학습 분할은 별도 목록에서 결정한다."""
    rows = []
    for item in spec["items"]:
        png = out / (item["id"] + ".png")
        record = out / (item["id"] + "-result.json")
        if not png.exists() or not record.exists():
            continue
        data = json.loads(record.read_text())
        if data["fingerprint"] != fingerprint or data["output"]["sha256"] != sha256(png):
            raise ValueError(f"Result mismatch: {item['id']}")
        rows.append({
            "id": item["id"], "image": str(png.relative_to(ROOT)),
            "sha256": sha256(png), "record": str(record.relative_to(ROOT)),
            "record_sha256": sha256(record), "category": item.get("category", "input"),
            "condition": item.get("condition", ""), "reference": item["reference"],
            "group": item.get("group", item["id"]),
            "reference_sha256": spec["references"][item["reference"]]["sha256"],
            "review_status": "pending", "split": "pending", "caption": "",
            "reserved_split": item.get("reserved_split"),
            "target": item.get("training_target"),
            "target_sha256": item.get("training_target_sha256"),
            "suggested_caption": item.get("training_caption", ""),
        })
    write(out / "candidate-catalog.json", {
        "schema_version": 1, "model_id": MODEL_ID, "fingerprint": fingerprint,
        "planned_count": len(spec["items"]), "generated_count": len(rows),
        "items": rows,
    })


def wait_for_gpu(state, path, enabled):
    """다른 CUDA 작업의 종료를 기다린다. 실행 중인 학습을 중단하지 않는다."""
    while True:
        result = subprocess.run(
            ["nvidia-smi", "--query-compute-apps=pid", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, check=True,
        )
        if not result.stdout.strip():
            return
        if not enabled:
            raise RuntimeError("GPU busy: rerun with --wait-for-gpu")
        state["status"] = "waiting_for_gpu"
        state["blocking_pids"] = result.stdout.strip().splitlines()
        write(path, state)
        time.sleep(30)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--spec",
        type=Path,
        default=ASSETS / "sec-12/p7-5-11-mira-supplement-spec-v2.json",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=ROOT / ".tmp/p7-5-11/supplements-v2"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="모델을 로드하지 않고 참조 해시와 생성 순서만 확인",
    )
    parser.add_argument("--limit", type=int, help="이번 실행에서 생성할 미완료 후보 수")
    parser.add_argument("--wait-for-gpu", action="store_true", help="다른 CUDA 작업 종료 후 시작")
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be positive")
    # 얼굴 외형을 다시 정의하지 않고 목록의 변경 대상과 방향별 참조를 사용한다.
    spec = json.loads(args.spec.read_text())
    assert spec["schema_version"] == 1 and spec["model_id"] == MODEL_ID
    cfg = spec["settings"]
    assert cfg["extra_lora"] is None and cfg["size"] >= 32 and cfg["size"] % 32 == 0
    assert cfg["steps"] > 0 and cfg["true_cfg_scale"] >= 1
    ids = [x["id"] for x in spec["items"]]
    assert len(ids) == len(set(ids)) and all(
        re.fullmatch(r"[a-z0-9-]+", x) for x in ids
    )
    assert [x["order"] for x in spec["items"]] == list(range(1, len(ids) + 1))
    for ref in spec["references"].values():
        assert sha256(asset_path(ref["path"])) == ref["sha256"], "Reference changed"
    for item in spec["items"]:
        assert item["reference"] in spec["references"] and item["prompt"].strip()
    if args.dry_run:
        print(
            json.dumps(
                {
                    "model": MODEL_ID,
                    "count": len(ids),
                    "order": ids,
                    "output_dir": str(args.output_dir),
                },
                indent=2,
            )
        )
        return
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    with (out / ".lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        run(out, args.spec, spec, args.limit, args.wait_for_gpu)


def run(out, spec_path, spec, limit=None, wait_gpu=False):
    """완료 항목의 해시를 확인하고 남은 후보만 같은 순서로 생성한다."""
    # 코드·목록이 바뀌면 과거 출력과 섞지 않고 새 폴더에서 비교한다.
    fingerprint = {
        "spec_sha256": sha256(spec_path),
        "code_sha256": sha256(Path(__file__)),
        "helper_sha256": sha256(
            ASSETS / "sec-02/p7_5_2_qwen_edit_2511_generate_mira_torso.py"
        ),
    }
    state_path = out / "generation-state.json"
    if state_path.exists():
        old = json.loads(state_path.read_text())
        assert old["fingerprint"] == fingerprint, (
            "Changed spec/code: use a new output directory"
        )
    state = {
        "model_id": MODEL_ID,
        "fingerprint": fingerprint,
        "status": "preflight",
        "completed": [],
        "current": None,
    }
    pending = []
    for item in spec["items"]:
        png = out / (item["id"] + ".png")
        record = out / (item["id"] + "-result.json")
        if png.exists() or record.exists():
            assert png.exists() and record.exists(), (
                f"Partial output: {item['id']}; preserve it and use a new directory"
            )
            data = json.loads(record.read_text())
            assert data["fingerprint"] == fingerprint and data["output"][
                "sha256"
            ] == sha256(png), "Existing result mismatch"
            state["completed"].append(item["id"])
        else:
            pending.append(item)
    write(state_path, state)
    catalog(out, spec, fingerprint)
    try:
        if not pending:
            state["status"] = "generated_pending_review"
            return
        wait_for_gpu(state, state_path, wait_gpu)
        import torch
        from PIL import Image
        from diffusers import QwenImageEditPlusPipeline

        if not torch.cuda.is_available():
            raise RuntimeError(
                "CUDA unavailable: no image generated; restore GPU/driver access and rerun the same command"
            )
        cfg = spec["settings"]
        size = cfg["size"]
        # 8GB 환경의 메모리 배치다. 모델 정체성이나 학습 품질을 바꾸는 옵션으로 해석하지 않는다.
        pipe = QwenImageEditPlusPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.bfloat16,
            cache_dir=CACHE_DIR,
            local_files_only=True,
        )
        pipe.enable_sequential_cpu_offload()
        pipe.vae.enable_slicing()
        for item in pending[:limit]:
            state["current"] = item["id"]
            state["status"] = "generating"
            write(state_path, state)
            print("Generating " + item["id"], flush=True)
            ref = spec["references"][item["reference"]]
            with Image.open(asset_path(ref["path"])) as opened:
                assert opened.width == opened.height
                image = opened.convert("RGB").resize(
                    (size, size), Image.Resampling.LANCZOS
                )
            started = time.monotonic()
            # 각 항목의 시드를 고정해 반복 실행의 입력 조건을 추적한다.
            with torch.inference_mode():
                result = pipe(
                    image=[image],
                    prompt=item["prompt"],
                    negative_prompt=" ",
                    width=size,
                    height=size,
                    num_inference_steps=cfg["steps"],
                    true_cfg_scale=cfg["true_cfg_scale"],
                    guidance_scale=1.0,
                    generator=torch.Generator(device="cuda").manual_seed(item["seed"]),
                ).images[0]
            assert result.size == (size, size)
            png = out / (item["id"] + ".png")
            result.save(png)
            write(
                out / (item["id"] + "-result.json"),
                {
                    "status": "generated_pending_review",
                    "model_id": MODEL_ID,
                    "fingerprint": fingerprint,
                    "design": item,
                    "input": ref,
                    "settings": cfg,
                    "reference_preprocessing": "RGB Lanczos square resize to target size",
                    "runtime": runtime_record(),
                    "gpu": torch.cuda.get_device_name(),
                    "dtype": "bfloat16",
                    "device_placement": "sequential_cpu_offload",
                    "elapsed_seconds": round(time.monotonic() - started, 2),
                    "output": {"path": str(png), "sha256": sha256(png)},
                },
            )
            state["completed"].append(item["id"])
            write(state_path, state)
            catalog(out, spec, fingerprint)
        state["current"] = None
        state["status"] = (
            "generated_pending_review" if len(state["completed"]) == len(spec["items"])
            else "paused_at_limit"
        )
    except Exception as error:
        state["status"] = "failed"
        state["error"] = str(error)
        raise
    finally:
        write(state_path, state)


if __name__ == "__main__":
    main()
