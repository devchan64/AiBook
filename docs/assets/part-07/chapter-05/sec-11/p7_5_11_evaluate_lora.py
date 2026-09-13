#!/usr/bin/env python3
"""얼굴 없는 동일 입력에서 지정 LoRA 체크포인트의 출력을 비교한다.

조작: --checkpoint와 --checkpoint-sha256으로 학습량을 선택한다.
--case는 장면, --scales 0 1은 미적용·적용 비교를 선택한다.
관찰: PNG의 정체성 특징과 지시 준수를 비교하며 JSON은 실행 조건의 증거다.
--dry-run은 가중치 해시·조건만 확인하며 시각 평가나 GPU 생성을 하지 않는다.
"""

import argparse
import json
import time
import fcntl
import shutil
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
from p7_5_11_generate_supplements import write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume-from", type=Path)
    parser.add_argument(
        "--checkpoint", type=Path, required=True, help="비교할 학습 스텝의 LoRA 파일"
    )
    parser.add_argument(
        "--checkpoint-sha256", required=True, help="선택한 LoRA 파일의 SHA-256"
    )
    parser.add_argument(
        "--case", action="append", choices=["portrait", "cafe", "garden"]
    )
    parser.add_argument("--scales", type=int, nargs="+", choices=[0, 1], default=[0, 1])
    args = parser.parse_args()
    if bool(args.checkpoint) != bool(args.checkpoint_sha256):
        parser.error("--checkpoint and --checkpoint-sha256 must be provided together")
    if len(set(args.scales)) != len(args.scales):
        parser.error("Duplicate scales are not allowed")
    spec = json.loads((ASSETS / "sec-11/identity-evaluation/spec.json").read_text())
    # 특정 과거 실험을 기본값으로 숨기지 않고 비교할 가중치를 명시한다.
    checkpoint = args.checkpoint.resolve()
    expected_sha = args.checkpoint_sha256
    assert sha256(checkpoint) == expected_sha
    assert (
        spec["evaluation_type"] == "identity_from_neutral_canvas"
        and spec["model"] == MODEL_ID
    )
    cases = [case for case in spec["cases"] if not args.case or case["id"] in args.case]
    from PIL import Image

    # 얼굴 참조가 정체성 보존을 대신하지 않도록 평가 입력의 모든 픽셀을 검사한다.
    for case in cases:
        ref = case["reference"]
        assert sha256(ROOT / ref["path"]) == ref["sha256"]
        with Image.open(ROOT / ref["path"]) as im:
            assert (
                im.mode == "RGB"
                and im.size == (512, 512)
                and im.getextrema() == ((240, 240),) * 3
            ), (
                "Identity evaluation requires a neutral canvas without facial information"
            )
    # 장면·시드·추론 설정은 고정하고 체크포인트와 적용 여부만 비교한다.
    plan = {
        "model": MODEL_ID,
        "checkpoint": str(checkpoint),
        "checkpoint_sha256": sha256(checkpoint),
        "size": 512,
        "steps": 20,
        "cfg": 4.0,
        "scales": args.scales,
        "cases": cases,
        "code_sha256": sha256(Path(__file__)),
        "runtime": runtime_record(),
    }
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    with (out / ".lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if (out / "plan.json").exists():
            assert json.loads((out / "plan.json").read_text()) == plan
        if args.resume_from:
            assert args.resume_from.resolve() != out
            prior = json.loads((args.resume_from / "plan.json").read_text())
            for field in (
                "model",
                "checkpoint_sha256",
                "size",
                "steps",
                "cfg",
                "scales",
                "cases",
            ):
                assert prior[field] == plan[field], field
            write(out / "prior-plan.json", prior)
            for record in args.resume_from.glob("*-result.json"):
                data = json.loads(record.read_text())
                png = record.with_name(record.name.replace("-result.json", ".png"))
                assert data["output_sha256"] == sha256(png) and data[
                    "plan_sha256"
                ] == sha256(args.resume_from / "plan.json")
                for source in (record, png):
                    target = out / source.name
                    if target.exists():
                        assert sha256(target) == sha256(source)
                    else:
                        shutil.copy2(source, target)
        write(out / "plan.json", plan)
        state = {"status": "loading", "completed": [], "current": None}
        write(out / "state.json", state)
        try:
            import torch
            from PIL import Image
            from diffusers import QwenImageEditPlusPipeline

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
            for case in cases:
                with Image.open(ROOT / case["reference"]["path"]) as im:
                    ref = im.convert("RGB").resize((512, 512), Image.Resampling.LANCZOS)
                for scale in plan["scales"]:
                    key = case["id"] + ("-base" if scale == 0 else "-lora")
                    png = out / (key + ".png")
                    record = out / (key + "-result.json")
                    if png.exists() or record.exists():
                        assert png.exists() and record.exists()
                        assert json.loads(record.read_text())[
                            "output_sha256"
                        ] == sha256(png)
                        state["completed"].append(key)
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
                    result.save(png)
                    write(
                        record,
                        {
                            "case": case,
                            "scale": scale,
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
