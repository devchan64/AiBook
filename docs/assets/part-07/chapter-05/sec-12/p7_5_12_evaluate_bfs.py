#!/usr/bin/env python3
"""검증 입력만으로 BFS LoRA 미적용·적용 결과를 생성한다.

조작: 체크포인트와 --scales를 바꾸어 같은 입력·시드의 편집 결과를 비교한다.
관찰: Mira 변환과 입력 표정·장면 보존을 목표와 나란히 검수한다.
목표 이미지는 비교용으로만 기록하며 파이프라인에 전달하지 않는다.
--dry-run은 경로·해시·분할을 점검하고 GPU를 사용하지 않는다.
"""

import argparse
import math
import json
import time
import fcntl
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sec-02"))
from p7_5_2_qwen_edit_2511_generate_mira_torso import (
    ROOT,
    ASSETS,
    CACHE_DIR,
    MODEL_ID,
    sha256,
    runtime_record,
)


def write(path, value):
    """완성된 JSON만 남기도록 임시 파일을 원자적으로 교체한다."""
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    temp.replace(path)


def parse_scale(value):
    scale = float(value)
    if not math.isfinite(scale) or not 0 <= scale <= 1:
        raise argparse.ArgumentTypeError("Scale must be finite and between 0 and 1")
    return scale


def output_key(case, scale):
    # 기존 0·1 파일명은 보존하고 소수 강도마다 별도 결과를 남긴다.
    suffix = "-base" if scale == 0 else "-lora" if scale == 1 else "-lora-scale-" + repr(scale)
    return case["id"] + suffix


def select_cases(cases, requested):
    if not requested:
        return cases
    aliases = {alias: c["id"] for c in cases for alias in (c["id"], c["management_code"])}
    unknown = set(requested) - aliases.keys()
    if unknown:
        raise ValueError(f"Unknown cases: {sorted(unknown)}")
    selected = [aliases[x] for x in requested]
    if len(set(selected)) != len(selected):
        raise ValueError("Duplicate case selection")
    return [c for c in cases if c["id"] in selected]


def completed_outputs(out, plan):
    """모델 로드 전에 계획·기존 결과를 확인하며 손상 기록은 재생성하지 않는다."""
    plan_path = out / "plan.json"
    if plan_path.exists() and json.loads(plan_path.read_text()) != plan:
        raise ValueError("Existing plan differs; use a new output directory")
    completed = []
    for case in plan["cases"]:
        for scale in plan["scales"]:
            key = output_key(case, scale)
            png, record = out / (key + ".png"), out / (key + "-result.json")
            if not (png.exists() or record.exists()):
                continue
            if not (png.exists() and record.exists() and plan_path.exists()):
                raise ValueError(f"Incomplete existing output: {key}")
            data = json.loads(record.read_text())
            if (data["output_sha256"] != sha256(png)
                    or data["plan_sha256"] != sha256(plan_path)
                    or data["checkpoint_sha256"] != plan["checkpoint_sha256"]
                    or data["case"] != case or data["scale"] != scale):
                raise ValueError(f"Existing output fingerprint mismatch: {key}")
            completed.append(key)
    return completed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--input-manifest", type=Path, help="학습 외 새 입력의 생성 목록 JSON")
    parser.add_argument(
        "--checkpoint", type=Path, required=True, help="비교할 학습 스텝의 LoRA 파일"
    )
    parser.add_argument(
        "--checkpoint-sha256", required=True, help="선택한 LoRA 파일의 SHA-256"
    )
    parser.add_argument(
        "--case", action="append", help="입력 ID 또는 관리번호 선택; 생략하면 목록 전체"
    )
    parser.add_argument("--scales", type=parse_scale, nargs="+", default=[0, 1])
    args = parser.parse_args()
    if bool(args.checkpoint) != bool(args.checkpoint_sha256):
        parser.error("--checkpoint and --checkpoint-sha256 must be provided together")
    if len(set(args.scales)) != len(args.scales):
        parser.error("Duplicate scales are not allowed")
    dataset_path = ASSETS / "sec-10/p7-5-10-paired-dataset.json"
    dataset = json.loads(dataset_path.read_text())
    checkpoint = args.checkpoint.resolve()
    assert sha256(checkpoint) == args.checkpoint_sha256
    assert (
        dataset["purpose"] == "paired_edit_training" and dataset["model_id"] == MODEL_ID
    )
    cases = []
    if args.input_manifest:
        from PIL import Image

        input_manifest = args.input_manifest.resolve()
        inputs = json.loads(input_manifest.read_text())["jobs"]
        assert len({item["id"] for item in inputs}) == len(inputs)
        assert all(item["status"] == "generated" for item in inputs)
        training_hashes = {item["control_sha256"] for item in dataset["items"]}
        caption = dataset["items"][0]["caption"].replace("the woman", "the person")
        for index, item in enumerate(inputs, 1):
            image = input_manifest.parent / item["image"]
            assert image.resolve().is_relative_to(ROOT)
            assert sha256(image) == item["sha256"]
            assert item["sha256"] not in training_hashes
            with Image.open(image) as source:
                assert source.size == (512, 512)
            cases.append({
                "id": item["id"], "management_code": f"P712-CAM-{index:03d}",
                "reference": {"path": str(image.relative_to(ROOT)), "sha256": item["sha256"]},
                "subject": item["subject"], "vertical": item["vertical"], "yaw": item["yaw"],
                "prompt": caption, "seed": 62294,
            })
    else:
        rows = [x for x in dataset["items"] if x["split"] == "validation"]
        assert len(rows) == 19
        cases = []
        for item in rows:
            assert sha256(ROOT / item["control_image"]) == item["control_sha256"]
            assert sha256(ROOT / item["image"]) == item["sha256"]
            cases.append(
                {
                    "id": item["id"],
                    "management_code": item["management_code"],
                    "reference": {
                        "path": item["control_image"],
                        "sha256": item["control_sha256"],
                    },
                    "comparison_target": {"path": item["image"], "sha256": item["sha256"]},
                    "prompt": item["caption"],
                    "seed": 62294,
                }
            )

    cases = select_cases(cases, args.case)
    # 입력·지시·시드를 고정하고 어댑터 적용 여부만 바꾼다.
    plan = {
        "model": MODEL_ID,
        "dataset_sha256": sha256(dataset_path),
        "evaluation_type": "new_synthetic_inputs" if args.input_manifest else "held_out_paired_edit",
        "input_manifest_sha256": sha256(args.input_manifest) if args.input_manifest else None,
        "checkpoint": str(checkpoint),
        "checkpoint_sha256": sha256(checkpoint),
        "size": 512,
        "vae_reference_size": 512,
        "vl_reference_size": 384,
        "preprocessing": "match_training_control_512_no_crop",
        "steps": 20,
        "cfg": 4.0,
        "scales": args.scales,
        "cases": cases,
        "code_sha256": sha256(Path(__file__)),
        "runtime": runtime_record(),
    }
    if args.dry_run:
        completed = completed_outputs(args.output_dir.resolve(), plan)
        total = len(cases) * len(args.scales)
        print(json.dumps({"selected_cases": len(cases), "total": total,
                          "reused": len(completed), "new": total - len(completed)}), file=sys.stderr)
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    with (out / ".lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        completed = completed_outputs(out, plan)
        write(out / "plan.json", plan)
        state = {"status": "loading", "completed": completed, "current": None,
                 "total": len(cases) * len(args.scales)}
        if len(completed) == state["total"]:
            state["status"] = "generated_pending_visual_review"
            write(out / "state.json", state)
            return
        write(out / "state.json", state)
        try:
            import torch
            from PIL import Image
            from diffusers import QwenImageEditPlusPipeline
            from diffusers.pipelines.qwenimage import (
                pipeline_qwenimage_edit_plus as pipeline_module,
            )

            # 설치 파일은 수정하지 않고 이 평가 프로세스의 참조 VAE 크기를 학습에 맞춘다.
            pipeline_module.VAE_IMAGE_SIZE = plan["vae_reference_size"] ** 2
            assert (
                pipeline_module.CONDITION_IMAGE_SIZE == plan["vl_reference_size"] ** 2
            )
            assert pipeline_module.calculate_dimensions(
                pipeline_module.VAE_IMAGE_SIZE, 1.0
            ) == (512, 512)

            assert torch.cuda.is_available()
            pipe = QwenImageEditPlusPipeline.from_pretrained(
                MODEL_ID,
                torch_dtype=torch.bfloat16,
                cache_dir=CACHE_DIR,
                local_files_only=True,
            )
            # 기반 모델에 어댑터를 로드한다. 별도 모델로 실행하거나 병합하지 않는다.
            pipe.load_lora_weights(
                str(checkpoint.parent),
                weight_name=checkpoint.name,
                adapter_name="mira",
                local_files_only=True,
            )
            assert "mira" in pipe.get_active_adapters()
            pipe.enable_sequential_cpu_offload()
            pipe.vae.enable_slicing()
            original_preprocess = pipe.image_processor.preprocess
            observed_sizes = []

            def checked_preprocess(*values, **options):
                tensor = original_preprocess(*values, **options)
                size = list(tensor.shape[-2:])
                assert size == [512, 512], f"Unexpected VAE input size: {size}"
                observed_sizes.append(size)
                return tensor

            pipe.image_processor.preprocess = checked_preprocess
            for case in cases:
                with Image.open(ROOT / case["reference"]["path"]) as im:
                    ref = im.convert("RGB").resize((512, 512), Image.Resampling.LANCZOS)
                for scale in plan["scales"]:
                    key = output_key(case, scale)
                    png = out / (key + ".png")
                    record = out / (key + "-result.json")
                    if key in completed:
                        continue
                    state.update(status="generating", current=key)
                    write(out / "state.json", state)
                    print(key, flush=True)
                    # 같은 파이프라인에서 어댑터만 켜거나 꺼 기반 모델의 차이를 배제한다.
                    with torch.inference_mode():
                        if scale:
                            pipe.enable_lora()
                            pipe.set_adapters("mira", adapter_weights=scale)
                        else:
                            pipe.disable_lora()
                    observed_sizes.clear()
                    start = time.monotonic()
                    with torch.inference_mode():
                        result = pipe(
                            image=[ref],
                            prompt=case["prompt"],
                            negative_prompt=" ",
                            width=512,
                            height=512,
                            num_inference_steps=20,
                            true_cfg_scale=4.0,
                            guidance_scale=1.0,
                            generator=torch.Generator(device="cuda").manual_seed(
                                case["seed"]
                            ),
                        ).images[0]
                    assert observed_sizes == [[512, 512]], observed_sizes
                    result.save(png)
                    write(
                        record,
                        {
                            "case": case,
                            "scale": scale,
                            "observed_vae_input_sizes": observed_sizes.copy(),
                            "checkpoint_sha256": plan["checkpoint_sha256"],
                            "plan_sha256": sha256(out / "plan.json"),
                            "output_sha256": sha256(png),
                            "elapsed_seconds": round(time.monotonic() - start, 2),
                            "status": "pending_visual_review",
                        },
                    )
                    state["completed"].append(key)
                    write(out / "state.json", state)
            state.update(status="generated_pending_visual_review", current=None)
        except BaseException as e:
            state.update(status="failed", error=str(e))
            raise
        finally:
            write(out / "state.json", state)


if __name__ == "__main__":
    main()
