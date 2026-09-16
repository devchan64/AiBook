#!/usr/bin/env python3
"""방향별 참조와 JSON 생성 목록으로 Mira 학습 후보를 순차 생성한다.

조작: --spec의 장면·시드·참조를 바꾸고 --output-dir을 새로 지정한다.
관찰: PNG의 얼굴·헤어·지시 준수와 결과 JSON의 입력·출력 해시를 비교한다.
--dry-run은 목록만 확인한다. 생성 완료는 학습 후보의 채택을 뜻하지 않는다.
가중치는 model_weight_manager.py로 준비한 .tmp/download 캐시만 읽는다.
"""

import argparse
import fcntl
import json
import re
import time
import sys
import subprocess
import copy
import hashlib
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


ALIASES = json.loads(
    (Path(__file__).parent / "p7-5-10-asset-migration.json").read_text()
)["path_aliases"]


def asset_path(value):
    """과거 생성 기록의 경로를 현재 자산으로 연결해 원본 기록을 보존한다."""
    path = Path(value)
    path = (ROOT / path if not path.is_absolute() else path).resolve()
    if path.is_relative_to(ROOT):
        destination = ALIASES.get(path.relative_to(ROOT).as_posix())
        if destination:
            return (ROOT / destination).resolve()
    return path


def write(path, data):
    """중간 저장 파일을 교체해 불완전한 JSON이 상태 파일로 남지 않게 한다."""
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(path)


def load_spec(path):
    """조건별 문구와 명시적인 조합을 펼친다. 기존 실험은 원문 일치를 검사한다."""
    spec = json.loads(path.read_text())
    if spec["schema_version"] == 1:
        return spec
    if spec["schema_version"] != 2:
        raise ValueError("Unsupported composition schema")
    definitions = spec["components"]
    order = spec["prompt_order"]
    if len(order) != len(set(order)) or set(order) != set(definitions):
        raise ValueError("Prompt order must contain each component axis exactly once")
    expanded = copy.deepcopy(spec)
    for row in expanded["items"]:
        if "prompt" in row:
            raise ValueError("Use components instead of a duplicated prompt")
        choices = row.pop("components")
        if set(choices) != set(order):
            raise ValueError(f"Missing or extra component axis: {row['id']}")
        selected = [definitions[axis][choices[axis]] for axis in order]
        direction = definitions["direction"][choices["direction"]]
        if direction["reference"] != row["reference"]:
            raise ValueError(f"Direction/reference mismatch: {row['id']}")
        row["prompt"] = " ".join(part["prompt"] for part in selected if part["prompt"])
    for key in ("components", "prompt_order", "provenance"):
        expanded.pop(key, None)
    expanded["schema_version"] = 1
    if "provenance" in spec:
        # 원본 JSON 사본 대신 정규화한 내용의 해시로 과거 생성 조건을 검증한다.
        original = copy.deepcopy({key: value for key, value in expanded.items()
                                  if key not in ("output_dir", "excluded_items")})
        source = spec["provenance"]
        # 향후 학습 지시 수정은 이미지 생성 조건의 변경과 구분한다.
        if "generation_spec_sha256" in source:
            for row in original["items"]:
                row.pop("training_caption", None)
        canonical = json.dumps(original, ensure_ascii=False, sort_keys=True,
                               separators=(",", ":")).encode()
        expected = source.get("generation_spec_sha256", source["expanded_spec_sha256"])
        if hashlib.sha256(canonical).hexdigest() != expected:
            raise ValueError("Composed spec differs from original; use a new independent spec for changed conditions")
        expanded["_original_spec_sha256"] = source["original_spec_sha256"]
    return expanded


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
            "control_image": item.get("training_input"),
            "control_sha256": item.get("training_input_sha256"),
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



def generation_plan(out, spec_path, spec, selection=None):
    """선택·제외·완료 기록을 합쳐 실제 생성 대상만 반환한다."""
    selection = {} if selection is None else selection
    if not isinstance(selection, dict):
        raise ValueError("Selection must be a JSON object")
    ids = {item["id"] for item in spec["items"]}
    if set(selection) - {"include_ids", "exclude_ids"}:
        raise ValueError("Selection accepts only include_ids and exclude_ids")

    def checked_ids(values):
        if not isinstance(values, list) or not all(isinstance(x, str) for x in values):
            raise ValueError("IDs must be a JSON string list")
        if len(values) != len(set(values)) or not set(values) <= ids:
            raise ValueError("Duplicate or unknown selection IDs")
        return set(values)

    included = ids if selection.get("include_ids") is None else checked_ids(selection["include_ids"])
    excluded = checked_ids(selection.get("exclude_ids", []))
    fingerprint = {
        "spec_sha256": spec.get("_original_spec_sha256", sha256(spec_path)),
        "composition_sha256": sha256(spec_path), "code_sha256": sha256(Path(__file__)),
        "helper_sha256": sha256(ASSETS / "sec-02/p7_5_2_qwen_edit_2511_generate_mira_torso.py"),
    }
    # 과거 폐기 결정은 생성 목록 자체에 보존해 실행 옵션을 빼도 적용한다.
    policy_excluded = checked_ids([item["id"] for item in spec.get("excluded_items", [])])
    excluded |= policy_excluded
    # 이관된 완료 묶음은 기존 카탈로그·원본 기록의 해시를 검증하고 그대로 재사용한다.
    catalog_path = out / "candidate-catalog.json"
    if catalog_path.exists():
        saved = json.loads(catalog_path.read_text())
        if saved["fingerprint"]["spec_sha256"] != fingerprint["spec_sha256"]:
            raise ValueError("Completed catalog belongs to a different spec")
        rows = saved["items"]
        if len(rows) == len({row["id"] for row in rows}) and {row["id"] for row in rows} == ids - policy_excluded:
            for row in rows:
                image, record = asset_path(row["image"]), asset_path(row["record"])
                if sha256(image) != row["sha256"] or sha256(record) != row["record_sha256"]:
                    raise ValueError(f"Completed catalog changed: {row['id']}")
                if json.loads(record.read_text())["output"]["sha256"] != row["sha256"]:
                    raise ValueError(f"Completed record mismatch: {row['id']}")
            return {"model_id": MODEL_ID, "fingerprint": fingerprint,
                    "status": "already_generated", "completed": sorted(ids - excluded),
                    "excluded_ids": sorted(excluded), "current": None,
                    "selected_ids": sorted(included), "reuse_catalog": True}, []
    state_path = out / "generation-state.json"
    old = json.loads(state_path.read_text()) if state_path.exists() else {}
    if old and old["fingerprint"] != fingerprint:
        raise ValueError("Changed spec/code: use a new output directory")
    # 실행에서 확정한 제외는 다음 실행에서 옵션을 빼도 유지한다.
    excluded |= checked_ids(old.get("excluded_ids", []))
    completed, pending = [], []
    for item in spec["items"]:
        key = item["id"]
        if key in excluded:
            continue
        png, record = out / (key + ".png"), out / (key + "-result.json")
        if png.exists() or record.exists():
            if not (png.exists() and record.exists()):
                raise ValueError(f"Partial output: {key}; no automatic regeneration")
            data = json.loads(record.read_text())
            if data["fingerprint"] != fingerprint or data["output"]["sha256"] != sha256(png):
                raise ValueError(f"Existing result mismatch: {key}")
            completed.append(key)
        elif key in old.get("completed", []):
            raise ValueError(f"Completed output missing: {key}; mark excluded or restore files")
        elif key in included:
            pending.append(item)
    state = {"model_id": MODEL_ID, "fingerprint": fingerprint, "status": "preflight",
             "completed": completed, "current": None, "excluded_ids": sorted(excluded),
             "selected_ids": sorted(included)}
    return state, pending


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--spec",
        type=Path,
        default=ASSETS / "sec-10/p7-5-10-bfs-input-combinations-v1.json",
    )
    parser.add_argument(
        "--output-dir", type=Path,
        help="JSON의 output_dir을 덮어쓸 저장 경로",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="모델을 로드하지 않고 참조 해시와 생성 순서만 확인",
    )
    parser.add_argument("--limit", type=int, help="이번 실행에서 생성할 미완료 후보 수")
    parser.add_argument("--wait-for-gpu", action="store_true", help="다른 CUDA 작업 종료 후 시작")
    parser.add_argument("--selection", type=Path, help="include_ids·exclude_ids를 지정한 JSON")
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be positive")
    # 얼굴 외형을 다시 정의하지 않고 목록의 변경 대상과 방향별 참조를 사용한다.
    spec = load_spec(args.spec)
    # 실험별 프롬프트·참조·저장 위치는 JSON으로 교체하고 생성기는 공유한다.
    out = (args.output_dir or ROOT / spec.get(
        "output_dir", ".tmp/p7-5-11/supplements-v2"
    )).resolve()
    if not out.is_relative_to(ROOT):
        raise ValueError("Output directory must be inside the repository")
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
    groups = {}
    for item in spec["items"]:
        assert item["reference"] in spec["references"] and item["prompt"].strip()
        reference_keys = item.get("reference_images", [item["reference"]])
        assert reference_keys and reference_keys[0] == item["reference"]
        assert all(key in spec["references"] for key in reference_keys)
        if item.get("training_input"):
            assert sha256(asset_path(item["training_input"])) == item["training_input_sha256"]
        if item.get("training_target"):
            target_hash = item["training_target_sha256"]
            assert sha256(asset_path(item["training_target"])) == target_hash, "Target changed"
            split = item.get("reserved_split")
            assert groups.setdefault(target_hash, split) == split, "Target split leakage"
    selection = json.loads(args.selection.read_text()) if args.selection else None
    if args.dry_run:
        state, pending = generation_plan(out, args.spec, spec, selection)
        print(json.dumps({"model": MODEL_ID, "planned_count": len(ids),
                          "completed_count": len(state["completed"]),
                          "excluded_ids": state["excluded_ids"],
                          "count": len(pending[:args.limit]),
                          "order": [item["id"] for item in pending[:args.limit]],
                          "output_dir": str(out)}, indent=2))
        return
    out.mkdir(parents=True, exist_ok=True)
    with (out / ".lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        run(out, args.spec, spec, args.limit, args.wait_for_gpu, selection)


def run(out, spec_path, spec, limit=None, wait_gpu=False, selection=None):
    """완료 항목은 재사용하고 선택 목록의 미완료 항목만 생성한다."""
    state, pending = generation_plan(out, spec_path, spec, selection)
    if state.get("reuse_catalog"):
        print(json.dumps({"status": "already_generated", "count": len(state["completed"]),
                          "excluded_ids": state["excluded_ids"]}))
        return
    fingerprint = state["fingerprint"]
    state_path = out / "generation-state.json"
    # 제외된 이미지는 학습 후보 카탈로그에서도 제거하되 파일은 삭제하지 않는다.
    spec = dict(spec, items=[item for item in spec["items"]
                            if item["id"] not in state["excluded_ids"]])
    write(state_path, state)
    catalog(out, spec, fingerprint)
    try:
        if not pending:
            state["status"] = ("generated_pending_review"
                               if len(state["completed"]) == len(spec["items"])
                               else "paused_at_selection")
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
            refs = [spec["references"][key] for key in
                    item.get("reference_images", [item["reference"]])]
            images = []
            # Picture 1은 편집할 장면, 추가 참조는 JSON에 명시한 순서로 전달한다.
            for ref in refs:
                with Image.open(asset_path(ref["path"])) as opened:
                    assert opened.width == opened.height
                    images.append(opened.convert("RGB").resize(
                        (size, size), Image.Resampling.LANCZOS
                    ))
            started = time.monotonic()
            # 각 항목의 시드를 고정해 반복 실행의 입력 조건을 추적한다.
            with torch.inference_mode():
                result = pipe(
                    image=images,
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
                    "input": refs[0],
                    "input_images": refs,
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
            else ("paused_at_limit" if limit is not None and len(pending) > limit
                  else "paused_at_selection")
        )
    except Exception as error:
        state["status"] = "failed"
        state["error"] = str(error)
        raise
    finally:
        write(state_path, state)


if __name__ == "__main__":
    main()
