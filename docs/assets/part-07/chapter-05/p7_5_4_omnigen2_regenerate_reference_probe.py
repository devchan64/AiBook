#!/usr/bin/env python3
"""OmniGen2로 기존 장면을 다중 참조 기반으로 다시 그리는 소규모 실험.

조절값
------
``--steps``와 ``--image-guidance-scale``을 바꾸어 원본 장면 보존 정도를
비교한다. 첫 실행은 512x768, 20 step, 순차 CPU 오프로딩으로 제한한다.

관찰값
------
원본의 점프 자세·농구 코트·공·골대·구도를 유지하면서, 두 참조 이미지의
얼굴·헤어와 착장을 한 인물에게만 적용하는지 출력 PNG와 ``-result.json``에서
확인한다.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[4]
ASSET_DIR = ROOT / "docs" / "assets" / "part-07" / "chapter-05"
DEFAULT_SOURCE = ASSET_DIR / "p7-5-3-qwen-edit-fullbody-alley-oop-v1-seed-62294-steps-20.png"
DEFAULT_OUTFIT = ASSET_DIR / "p7-5-3-qwen-edit-prompt-style-outfit_stage2_jacket_face-long-trousers-folded-collar-v3-seed-62294-steps-30.png"
DEFAULT_FACE = ASSET_DIR / "p7-5-2-qwen-torso-yaw-front-cfg4-front-1024-v4-seed-62294-steps-8.png"
DEFAULT_OUTPUT = ASSET_DIR / "p7-5-4-omnigen2-regenerate-alley-oop-face-outfit-v1-seed-62294-steps-20.png"
DEFAULT_MODEL = ROOT / ".tmp" / "download" / "model-omnigen2"
DEFAULT_SOURCE_DIR = ROOT / ".tmp" / "omnigen2-source"
MODEL_REF = "model:omnigen2"
MODEL_REVISION = "df5dca8a981d74e6c3af214c145f5c735fe72367"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="장면과 자세를 유지할 원본 이미지")
    parser.add_argument("--outfit", type=Path, default=DEFAULT_OUTFIT, help="착장 참조 이미지")
    parser.add_argument("--face", type=Path, default=DEFAULT_FACE, help="얼굴과 헤어 참조 이미지")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="출력 PNG")
    parser.add_argument("--model-path", type=Path, default=DEFAULT_MODEL, help="OmniGen2 가중치 폴더")
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR, help="OmniGen2 공식 소스 체크아웃")
    parser.add_argument("--width", type=int, default=512, help="출력 너비(16의 배수)")
    parser.add_argument("--height", type=int, default=768, help="출력 높이(16의 배수)")
    parser.add_argument("--steps", type=int, default=20, help="확산 step 수")
    parser.add_argument("--seed", type=int, default=62294, help="재현용 시드")
    parser.add_argument("--text-guidance-scale", type=float, default=5.0, help="텍스트 지시 강도")
    parser.add_argument("--image-guidance-scale", type=float, default=2.0, help="입력 이미지 보존 강도")
    parser.add_argument("--max-reference-edge", type=int, default=512, help="각 참조 입력의 최대 긴 변")
    parser.add_argument("--source-repeats", type=int, default=1, help="장면·포즈 원본을 입력 목록에 반복하는 횟수")
    return parser.parse_args()


def require_file(path: Path, label: str) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"{label} 파일을 찾을 수 없습니다: {path}")


def resize_reference(path: Path, max_edge: int) -> Image.Image:
    """입력 토큰 수를 낮추기 위해 비율을 보존한 RGB 참조 이미지를 만든다."""
    image = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    long_edge = max(image.size)
    if long_edge <= max_edge:
        return image
    scale = max_edge / long_edge
    size = tuple(max(16, round(value * scale / 16) * 16) for value in image.size)
    return image.resize(size, Image.Resampling.LANCZOS)


def result_path(output: Path) -> Path:
    return output.with_name(f"{output.stem}-result.json")


def write_result(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    if args.width % 16 or args.height % 16:
        raise ValueError("출력 너비와 높이는 16의 배수여야 합니다.")
    if args.source_repeats < 1:
        raise ValueError("--source-repeats는 1 이상이어야 합니다.")
    for label, path in (("원본 장면", args.source), ("착장 참조", args.outfit), ("얼굴 참조", args.face)):
        require_file(path, label)
    if not args.model_path.is_dir():
        raise FileNotFoundError(
            f"OmniGen2 가중치 폴더를 찾을 수 없습니다: {args.model_path}\n"
            "모델 인벤토리 등록 뒤 .tmp/download/model-omnigen2/에 공식 가중치를 내려받으세요."
        )
    if not args.source_dir.is_dir():
        raise FileNotFoundError(f"OmniGen2 공식 소스 폴더를 찾을 수 없습니다: {args.source_dir}")

    outfit_index = args.source_repeats + 1
    face_index = args.source_repeats + 2
    source_images = ", ".join(f"image {index}" for index in range(1, args.source_repeats + 1))
    prompt = (
        f"Regenerate the source scene in {source_images}. Preserve its basketball jump, pose, composition, hoop, ball, "
        f"court, background, and shadow. Apply the woman's face and teal wavy bob from image {face_index} "
        f"and the white cropped jacket, gray crop top, teal wide-leg trousers, and white sneakers from image {outfit_index}."
    )
    input_paths = [args.source] * args.source_repeats + [args.outfit, args.face]
    input_roles = ["scene and pose"] * args.source_repeats + ["outfit", "face and hair"]
    output = args.output.resolve()
    record = {
        "schema": "aibook-image-generation-result-v1",
        "status": "running",
        "model": {"bom_ref": MODEL_REF, "revision": MODEL_REVISION, "source": "https://huggingface.co/OmniGen2/OmniGen2"},
        "inputs": [str(path.resolve()) for path in input_paths],
        "input_roles": input_roles,
        "prompt": prompt,
        "negative_prompt": "",
        "output": str(output),
        "width": args.width,
        "height": args.height,
        "steps": args.steps,
        "seed": args.seed,
        "text_guidance_scale": args.text_guidance_scale,
        "image_guidance_scale": args.image_guidance_scale,
        "max_reference_edge": args.max_reference_edge,
        "source_repeats": args.source_repeats,
        "memory_strategy": "sequential CPU offload",
        "started_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    record_file = result_path(output)
    write_result(record_file, record)

    try:
        sys.path.insert(0, str(args.source_dir.resolve()))
        import torch
        from accelerate import Accelerator
        from omnigen2.models.transformers.transformer_omnigen2 import OmniGen2Transformer2DModel
        from omnigen2.pipelines.omnigen2.pipeline_omnigen2 import OmniGen2Pipeline

        accelerator = Accelerator(mixed_precision="bf16")
        pipeline = OmniGen2Pipeline.from_pretrained(args.model_path, torch_dtype=torch.bfloat16, trust_remote_code=True)
        pipeline.transformer = OmniGen2Transformer2DModel.from_pretrained(
            args.model_path, subfolder="transformer", torch_dtype=torch.bfloat16
        )
        pipeline.enable_sequential_cpu_offload()
        inputs = [resize_reference(path, args.max_reference_edge) for path in input_paths]
        generator = torch.Generator(device=accelerator.device).manual_seed(args.seed)
        image = pipeline(
            prompt=prompt,
            input_images=inputs,
            width=args.width,
            height=args.height,
            num_inference_steps=args.steps,
            max_sequence_length=1024,
            text_guidance_scale=args.text_guidance_scale,
            image_guidance_scale=args.image_guidance_scale,
            cfg_range=(0.0, 1.0),
            negative_prompt="",
            generator=generator,
            output_type="pil",
        ).images[0]
        output.parent.mkdir(parents=True, exist_ok=True)
        image.save(output)
        record.update({"status": "completed", "completed_at": dt.datetime.now(dt.timezone.utc).isoformat()})
    except Exception as error:
        record.update({"status": "failed", "failed_at": dt.datetime.now(dt.timezone.utc).isoformat(), "error": repr(error)})
        raise
    finally:
        write_result(record_file, record)

    print(f"image: {output}")
    print(f"result: {record_file}")


if __name__ == "__main__":
    main()
