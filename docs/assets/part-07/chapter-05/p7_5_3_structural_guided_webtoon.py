#!/usr/bin/env python3
"""Render a new webtoon cut from text plus a derived structural guide.

This is text-to-image, not img2img: diffusion starts from seeded noise.  The
only visual condition is one or two depth, Canny, or lineart PNGs derived
after a text-only storyboard passed human review.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
from time import perf_counter

import torch
from diffusers import (
    ControlNetModel,
    FluxControlNetModel,
    StableDiffusionControlNetPipeline,
    StableDiffusionXLControlNetPipeline,
)
from PIL import Image


ASSET_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ASSET_DIR.parents[3]
SD15_MODEL = Path(
    "/home/cbsim/.cache/huggingface/hub/"
    "models--stable-diffusion-v1-5--stable-diffusion-v1-5/"
    "snapshots/451f4fe16113bff5a5d2269ed5ad43b0592e9a14"
)
SDXL_MODEL = Path(
    "/home/cbsim/.cache/huggingface/hub/"
    "models--stabilityai--stable-diffusion-xl-base-1.0/"
    "snapshots/462165984030d82259a11f4367a4eed129e94a7b"
)
# Flux.1-dev와 InstantX ControlNet은 아직 이 저장소의 `.tmp/`에 내려받지 않았다.
# 경로만 선언하며, `--backbone flux1-dev`는 가중치를 준비한 뒤 별도 실행 계약으로 검수한다.
FLUX1_DEV_MODEL = PROJECT_ROOT / ".tmp/p7-5-3-flux1-dev"
DEPTH_CONTROLNET = PROJECT_ROOT / ".tmp/p7-5-3-controlnet-depth"
CANNY_CONTROLNET = PROJECT_ROOT / ".tmp/p7-5-3-controlnet-canny"
LINEART_CONTROLNET = PROJECT_ROOT / ".tmp/p7-5-3-controlnet-lineart"
SDXL_CANNY_CONTROLNET = PROJECT_ROOT / ".tmp/p7-5-3-controlnet-canny-sdxl-small"
SDXL_DEPTH_CONTROLNET = PROJECT_ROOT / ".tmp/p7-5-3-controlnet-depth-sdxl-small"
FLUX1_CANNY_CONTROLNET = PROJECT_ROOT / ".tmp/p7-5-3-flux1-dev-controlnet-canny"
FLUX1_DEPTH_CONTROLNET = PROJECT_ROOT / ".tmp/p7-5-3-flux1-dev-controlnet-depth"
QWEN_IMAGE_MODEL = PROJECT_ROOT / ".tmp/p7-5-3-qwen-image"
QWEN_IMAGE_UNION_CONTROLNET = PROJECT_ROOT / ".tmp/p7-5-3-qwen-image-controlnet-union"
ZIMAGE_TURBO_MODEL = PROJECT_ROOT / ".tmp/p7-5-3-z-image-turbo"
# Z-Image Union은 Diffusers의 from_single_file 입력 계약을 사용한다.
ZIMAGE_UNION_CONTROLNET = PROJECT_ROOT / ".tmp/p7-5-3-z-image-turbo-union.safetensors"
BASE_MODELS = {
    "sd15": SD15_MODEL,
    "sdxl": SDXL_MODEL,
    "flux1-dev": FLUX1_DEV_MODEL,
    "qwen-image": QWEN_IMAGE_MODEL,
    "z-image-turbo": ZIMAGE_TURBO_MODEL,
}
CONTROLNET_MODELS = {
    "sd15": {
        "depth": DEPTH_CONTROLNET,
        "canny": CANNY_CONTROLNET,
        "lineart": LINEART_CONTROLNET,
    },
    "sdxl": {
        "canny": SDXL_CANNY_CONTROLNET,
        "depth": SDXL_DEPTH_CONTROLNET,
    },
    # Diffusers FluxControlNetPipeline supports InstantX Flux.1-dev Canny and depth.
    "flux1-dev": {"canny": FLUX1_CANNY_CONTROLNET, "depth": FLUX1_DEPTH_CONTROLNET},
    # Qwen Union은 canny, soft-edge(여기서는 lineart), depth를 하나의 ControlNet으로 받는다.
    "qwen-image": {
        "canny": QWEN_IMAGE_UNION_CONTROLNET,
        "depth": QWEN_IMAGE_UNION_CONTROLNET,
        "lineart": QWEN_IMAGE_UNION_CONTROLNET,
    },
    # Z-Image Union은 Canny, HED(여기서는 lineart), depth를 하나의 safetensors로 받는다.
    "z-image-turbo": {
        "canny": ZIMAGE_UNION_CONTROLNET,
        "depth": ZIMAGE_UNION_CONTROLNET,
        "lineart": ZIMAGE_UNION_CONTROLNET,
    },
}
BACKBONE_DEFAULTS = {
    "sd15": {
        "guide_kind": "depth", "steps": 24, "scale": 0.65, "width": 512, "height": 768,
        "guidance_scale": 7.0,
    },
    "sdxl": {
        "guide_kind": "canny", "steps": 28, "scale": 0.50, "width": 768, "height": 1152,
        "guidance_scale": 7.0,
    },
    # 공식 Flux ControlNet Canny 예시의 1024px·28 step·scale 0.5를 정적 후보로 둔다.
    # 이 저장소의 8 GB 환경에서의 실행 성립·VRAM·품질은 아직 검수하지 않았다.
    "flux1-dev": {
        "guide_kind": "canny", "steps": 28, "scale": 0.50, "width": 1024, "height": 1024,
        "guidance_scale": 3.5,
    },
    # Qwen 공식 ControlNet 예시: 30 step, true CFG 4.0, control scale 1.0.
    "qwen-image": {
        "guide_kind": "canny", "steps": 30, "scale": 1.0, "width": 1024, "height": 1024,
        "guidance_scale": 1.0, "true_cfg_scale": 4.0,
    },
    # Z-Image Turbo ControlNet 예시: 8~9 step, CFG 0, control scale 0.75.
    "z-image-turbo": {
        "guide_kind": "canny", "steps": 9, "scale": 0.75, "width": 1024, "height": 1024,
        "guidance_scale": 0.0,
    },
}
# Flux.2 Klein은 현 Diffusers에서 image=[...] 다중 참조 입력을 받지만 Flux.2 ControlNet
# pipeline은 제공하지 않는다. 그러므로 Canny/depth 전용 BACKBONE_DEFAULTS에는 넣지 않는다.
# The scene and style are text conditions.  No storyboard RGB pixels are used.
# 이 단계에서는 프롬프트의 장면 지시를 줄여 구조 guide 수용도를 관찰한다.
BENCHMARK_PROMPT = "full body dancer"
BENCHMARK_NEGATIVE_PROMPT = "extra limbs, malformed feet, cropped body"


def build_parser() -> argparse.ArgumentParser:
    """Offer reproducible settings while keeping the prompt and input boundary fixed."""
    parser = argparse.ArgumentParser(
        description="텍스트와 검수된 구조 guide로 새 웹툰 컷을 생성합니다. img2img는 쓰지 않습니다."
    )
    parser.add_argument("--seed", type=int, default=5401, help="재현용 seed (기본값: 5401)")
    parser.add_argument("--steps", type=int, help="backbone 기본 step을 덮어쓸 값")
    parser.add_argument("--scale", type=float, help="backbone 기본 구조 조건 강도를 덮어쓸 값")
    parser.add_argument("--width", type=int, help="backbone 기본 출력 너비를 덮어쓸 값")
    parser.add_argument("--height", type=int, help="backbone 기본 출력 높이를 덮어쓸 값")
    parser.add_argument(
        "--prompt", default=BENCHMARK_PROMPT,
        help="guide 수용도 비교용 최소 프롬프트 (기본값: 'full body dancer')",
    )
    parser.add_argument(
        "--negative-prompt", default=BENCHMARK_NEGATIVE_PROMPT,
        help="모델이 음성 프롬프트를 받는 경우만 쓰는 최소 억제 조건",
    )
    parser.add_argument(
        "--true-cfg-scale", type=float,
        help="Qwen-Image의 전통 CFG. 생략하면 백본 계약 기본값을 사용합니다.",
    )
    parser.add_argument(
        "--control-guidance-start", type=float, default=0.0,
        help="ControlNet 적용 시작 비율 (기본값: 0.0)",
    )
    parser.add_argument(
        "--control-guidance-end", type=float, default=1.0,
        help="ControlNet 적용 종료 비율 (기본값: 1.0)",
    )
    parser.add_argument(
        "--backbone",
        choices=tuple(CONTROLNET_MODELS),
        default="sdxl",
        help="텍스트-웹툰 기반 모델 (기본값: sdxl)",
    )
    parser.add_argument(
        "--guide",
        type=Path,
        required=True,
        help="텍스트 스토리보드에서 추출하고 사람 검수한 depth·Canny·lineart PNG",
    )
    parser.add_argument(
        "--guide-kind",
        choices=("depth", "canny", "lineart"),
        help="guide와 짝이 되는 ControlNet 종류 (생략하면 backbone 기본값)",
    )
    parser.add_argument(
        "--second-guide",
        type=Path,
        help="같은 검수 스토리보드에서 얻은 두 번째 구조 guide (선택 사항)",
    )
    parser.add_argument(
        "--second-guide-kind",
        choices=("depth", "canny", "lineart"),
        help="두 번째 guide와 짝이 되는 ControlNet 종류",
    )
    parser.add_argument(
        "--second-scale",
        type=float,
        help="두 번째 구조 조건 강도 (기본값: --scale과 같음)",
    )
    parser.add_argument(
        "--allow-restricted-license", action="store_true",
        help="비상업 Flux.1-dev를 비교 실행할 때 명시적으로 지정합니다.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ASSET_DIR / "p7-5-3-guided-webtoon",
        help="타임스탬프 PNG 저장 폴더",
    )
    return parser


def require_cuda_and_assets(
    guides: list[Path], guide_kinds: list[str], backbone: str
) -> None:
    """Reject a missing guide or unavailable local-GPU run before model loading."""
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU를 사용할 수 없습니다.")
    supported = CONTROLNET_MODELS[backbone]
    unsupported = [kind for kind in guide_kinds if kind not in supported]
    if unsupported:
        names = ", ".join(unsupported)
        raise ValueError(f"{backbone}에는 다음 guide가 없습니다: {names}")
    base_model = BASE_MODELS[backbone]
    paths = [base_model, *guides, *(supported[kind] for kind in guide_kinds)]
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"필수 로컬 자산을 찾지 못했습니다: {path}")


def main() -> None:
    """Generate one controlled cut and write a comparable performance/adherence record."""
    args = build_parser().parse_args()
    defaults = BACKBONE_DEFAULTS[args.backbone]
    args.guide_kind = args.guide_kind or defaults["guide_kind"]
    args.steps = args.steps or defaults["steps"]
    args.scale = args.scale if args.scale is not None else defaults["scale"]
    args.width = args.width or defaults["width"]
    args.height = args.height or defaults["height"]
    if bool(args.second_guide) != bool(args.second_guide_kind):
        raise ValueError("--second-guide와 --second-guide-kind는 함께 지정해야 합니다.")
    guide_paths = [args.guide]
    guide_kinds = [args.guide_kind]
    guide_scales = [args.scale]
    if args.second_guide:
        guide_paths.append(args.second_guide)
        guide_kinds.append(args.second_guide_kind)
        guide_scales.append(args.second_scale if args.second_scale is not None else args.scale)
    if args.backbone in {"qwen-image", "z-image-turbo"} and len(guide_paths) > 1:
        raise ValueError(
            f"{args.backbone} Union ControlNet 벤치마크는 한 번에 guide 하나만 받습니다. "
            "가이드별 결과를 별도 실행해 수용도를 비교하세요."
        )
    if args.backbone == "flux1-dev" and not args.allow_restricted_license:
        raise PermissionError(
            "Flux.1-dev는 비상업 라이선스 비교 후보입니다. "
            "조건을 확인한 뒤 --allow-restricted-license를 지정하세요."
        )
    require_cuda_and_assets(guide_paths, guide_kinds, args.backbone)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # This guide is a ControlNet condition, not an initial image for img2img.
    guides = [
        Image.open(path).convert("RGB").resize((args.width, args.height))
        for path in guide_paths
    ]
    torch.cuda.reset_peak_memory_stats()
    is_flux = args.backbone == "flux1-dev"
    is_qwen = args.backbone == "qwen-image"
    is_zimage = args.backbone == "z-image-turbo"
    controlnet_options = {
        "torch_dtype": torch.bfloat16 if (is_flux or is_qwen or is_zimage) else torch.float16,
        "local_files_only": True,
        "use_safetensors": True,
    }
    # The lineart checkpoint was deliberately downloaded as FP16 safetensors.
    controlnets = []
    for guide_kind in guide_kinds:
        options = controlnet_options.copy()
        if guide_kind == "lineart":
            options["variant"] = "fp16"
        if is_qwen:
            from diffusers import QwenImageControlNetModel

            controlnet_class = QwenImageControlNetModel
        elif is_zimage:
            from diffusers import ZImageControlNetModel

            # Z-Image Union은 Diffusers 폴더가 아니라 단일 safetensors 가중치 계약이다.
            controlnets.append(
                ZImageControlNetModel.from_single_file(
                    CONTROLNET_MODELS[args.backbone][guide_kind],
                    torch_dtype=torch.bfloat16,
                    local_files_only=True,
                )
            )
            continue
        else:
            controlnet_class = FluxControlNetModel if is_flux else ControlNetModel
        controlnets.append(
            controlnet_class.from_pretrained(
                CONTROLNET_MODELS[args.backbone][guide_kind], **options
            )
        )
    controlnet = controlnets[0] if len(controlnets) == 1 else controlnets
    if is_flux:
        from diffusers import FluxControlNetPipeline

        pipeline_class = FluxControlNetPipeline
    elif is_qwen:
        from diffusers import QwenImageControlNetPipeline

        pipeline_class = QwenImageControlNetPipeline
    elif is_zimage:
        from diffusers import ZImageControlNetPipeline

        pipeline_class = ZImageControlNetPipeline
    else:
        pipeline_class = {
            "sd15": StableDiffusionControlNetPipeline,
            "sdxl": StableDiffusionXLControlNetPipeline,
        }[args.backbone]
    base_model = BASE_MODELS[args.backbone]
    pipeline = pipeline_class.from_pretrained(
        base_model,
        controlnet=controlnet,
        torch_dtype=torch.bfloat16 if (is_flux or is_qwen or is_zimage) else torch.float16,
        local_files_only=True,
    )
    pipeline.enable_model_cpu_offload()
    if not (is_flux or is_qwen or is_zimage):
        pipeline.enable_attention_slicing()
    pipeline.set_progress_bar_config(disable=True)
    pipeline_inputs = {
        "prompt": args.prompt,
        "width": args.width,
        "height": args.height,
        "num_inference_steps": args.steps,
        "guidance_scale": defaults["guidance_scale"],
        "controlnet_conditioning_scale": guide_scales[0] if len(guide_scales) == 1 else guide_scales,
        "generator": torch.Generator(device="cuda").manual_seed(args.seed),
    }
    # Flux, Qwen, Z-Image name the structural condition `control_image`; SD uses `image`.
    pipeline_inputs["control_image" if (is_flux or is_qwen or is_zimage) else "image"] = (
        guides[0] if len(guides) == 1 else guides
    )
    if is_qwen:
        pipeline_inputs["negative_prompt"] = args.negative_prompt
        pipeline_inputs["true_cfg_scale"] = args.true_cfg_scale or defaults["true_cfg_scale"]
        pipeline_inputs["control_guidance_start"] = args.control_guidance_start
        pipeline_inputs["control_guidance_end"] = args.control_guidance_end
    elif not is_zimage:
        pipeline_inputs["negative_prompt"] = args.negative_prompt
        pipeline_inputs["control_guidance_start"] = args.control_guidance_start
        pipeline_inputs["control_guidance_end"] = args.control_guidance_end
    started = perf_counter()
    image = pipeline(
        **pipeline_inputs,
    ).images[0]
    elapsed_seconds = perf_counter() - started
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    guide_label = "+".join(guide_kinds)
    scale_label = "+".join(f"{scale:.2f}" for scale in guide_scales)
    output = args.output_dir / (
        f"{timestamp}-{args.backbone}-seed-{args.seed}-{guide_label}-{scale_label}.png"
    )
    image.save(output)
    # 구조 수용도의 최종 판정은 사람이 한다. 이 JSON은 같은 입력 계약에서
    # 생성 시간·VRAM·가이드 종류를 나란히 비교하기 위한 관찰 기록이다.
    record = {
        "run_id": timestamp,
        "backbone": args.backbone,
        "license_status": "restricted-comparison" if is_flux else "open-weight-candidate",
        "prompt": args.prompt,
        "negative_prompt": args.negative_prompt if not is_zimage else None,
        "seed": args.seed,
        "guide_paths": [str(path) for path in guide_paths],
        "guide_kinds": guide_kinds,
        "guide_scales": guide_scales,
        "width": args.width,
        "height": args.height,
        "steps": args.steps,
        "guidance_scale": defaults["guidance_scale"],
        "true_cfg_scale": pipeline_inputs.get("true_cfg_scale"),
        "control_window": [args.control_guidance_start, args.control_guidance_end],
        "elapsed_seconds": round(elapsed_seconds, 3),
        "peak_vram_mib": round(torch.cuda.max_memory_allocated() / 1024**2, 1),
        "output": str(output),
        "guide_adherence": {
            "status": "human-review-required",
            "criterion": "guide의 인물 윤곽·발과 지면의 분리·절벽의 상대 위치가 유지되는지",
        },
    }
    record_path = output.with_suffix(".json")
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    print(f"[검수 대상] {output}")
    print(f"[검수 기록] {record_path}")
    print(f"[소요 시간] {elapsed_seconds:.1f} s")
    print(f"[VRAM peak] {record['peak_vram_mib']:.1f} MiB")


if __name__ == "__main__":
    main()
