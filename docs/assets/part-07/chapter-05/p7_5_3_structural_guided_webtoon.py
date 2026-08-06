#!/usr/bin/env python3
"""Render a new webtoon cut from text plus a derived structural guide.

This is text-to-image, not img2img: diffusion starts from seeded noise.  The
only visual condition is one or two depth, Canny, or lineart PNGs derived
after a text-only storyboard passed human review.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import torch
from diffusers import (
    ControlNetModel,
    FluxControlNetModel,
    FluxControlNetPipeline,
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
FLUX1_CANNY_CONTROLNET = PROJECT_ROOT / ".tmp/p7-5-3-flux1-dev-controlnet-canny"
FLUX1_DEPTH_CONTROLNET = PROJECT_ROOT / ".tmp/p7-5-3-flux1-dev-controlnet-depth"
BASE_MODELS = {
    "sd15": SD15_MODEL,
    "sdxl": SDXL_MODEL,
    "flux1-dev": FLUX1_DEV_MODEL,
}
CONTROLNET_MODELS = {
    "sd15": {
        "depth": DEPTH_CONTROLNET,
        "canny": CANNY_CONTROLNET,
        "lineart": LINEART_CONTROLNET,
    },
    "sdxl": {"canny": SDXL_CANNY_CONTROLNET},
    # Diffusers FluxControlNetPipeline supports InstantX Flux.1-dev Canny and depth.
    "flux1-dev": {"canny": FLUX1_CANNY_CONTROLNET, "depth": FLUX1_DEPTH_CONTROLNET},
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
}
# Flux.2 Klein은 현 Diffusers에서 image=[...] 다중 참조 입력을 받지만 Flux.2 ControlNet
# pipeline은 제공하지 않는다. 그러므로 Canny/depth 전용 BACKBONE_DEFAULTS에는 넣지 않는다.
# The scene and style are text conditions.  No storyboard RGB pixels are used.
WEBTOON_PROMPT = (
    "one contemporary dancer, full body, balanced dance silhouette, raised leg, "
    "black sleeveless leotard, black footed opaque tights, supporting leg planted on flat ground, "
    "fully visible supporting foot and sole, "
    "foot outline separate from nearby rocks, one arm up, one arm out, exactly two arms and two legs, "
    "wide shot, dancer on level canyon floor, empty ground around dancer, distant cliffs in background, "
    "teal and leaf green, frame-free webtoon cut"
)
NEGATIVE_PROMPT = (
    "grayscale, monochrome, panel border, text, logo, crowd, duplicate person, "
    "extra limbs, cropped body, blurred, neon, opaque airbrush, floating, hidden feet, "
    "cropped feet, foot fused with ground, shoe merged with rocks, terrain overlapping foot, "
    "standing on rock, pedestal, boulder, malformed feet, twisted ankles, skirt, dress, flowing fabric, oversized clothes, bare legs"
)


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
    """Generate one new image from noise, text, and a derived structure condition."""
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
    require_cuda_and_assets(guide_paths, guide_kinds, args.backbone)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # This guide is a ControlNet condition, not an initial image for img2img.
    guides = [
        Image.open(path).convert("RGB").resize((args.width, args.height))
        for path in guide_paths
    ]
    torch.cuda.reset_peak_memory_stats()
    is_flux = args.backbone == "flux1-dev"
    controlnet_options = {
        "torch_dtype": torch.bfloat16 if is_flux else torch.float16,
        "local_files_only": True,
        "use_safetensors": True,
    }
    # The lineart checkpoint was deliberately downloaded as FP16 safetensors.
    controlnets = []
    for guide_kind in guide_kinds:
        options = controlnet_options.copy()
        if guide_kind == "lineart":
            options["variant"] = "fp16"
        controlnet_class = FluxControlNetModel if is_flux else ControlNetModel
        controlnets.append(
            controlnet_class.from_pretrained(
                CONTROLNET_MODELS[args.backbone][guide_kind], **options
            )
        )
    controlnet = controlnets[0] if len(controlnets) == 1 else controlnets
    pipeline_class = {
        "sd15": StableDiffusionControlNetPipeline,
        "sdxl": StableDiffusionXLControlNetPipeline,
        "flux1-dev": FluxControlNetPipeline,
    }[args.backbone]
    base_model = BASE_MODELS[args.backbone]
    pipeline = pipeline_class.from_pretrained(
        base_model,
        controlnet=controlnet,
        torch_dtype=torch.bfloat16 if is_flux else torch.float16,
        local_files_only=True,
    )
    pipeline.enable_model_cpu_offload()
    if not is_flux:
        pipeline.enable_attention_slicing()
    pipeline.set_progress_bar_config(disable=True)
    pipeline_inputs = {
        "prompt": WEBTOON_PROMPT,
        "negative_prompt": NEGATIVE_PROMPT,
        "width": args.width,
        "height": args.height,
        "num_inference_steps": args.steps,
        "guidance_scale": defaults["guidance_scale"],
        "controlnet_conditioning_scale": guide_scales[0] if len(guide_scales) == 1 else guide_scales,
        "generator": torch.Generator(device="cuda").manual_seed(args.seed),
    }
    # Flux names the structural condition `control_image`; SD pipelines use `image`.
    pipeline_inputs["control_image" if is_flux else "image"] = (
        guides[0] if len(guides) == 1 else guides
    )
    image = pipeline(
        **pipeline_inputs,
    ).images[0]
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    guide_label = "+".join(guide_kinds)
    scale_label = "+".join(f"{scale:.2f}" for scale in guide_scales)
    output = args.output_dir / (
        f"{timestamp}-{args.backbone}-seed-{args.seed}-{guide_label}-{scale_label}.png"
    )
    image.save(output)
    print(f"[검수 대상] {output}")
    print(f"[VRAM peak] {torch.cuda.max_memory_allocated() / 1024**2:.1f} MiB")


if __name__ == "__main__":
    main()
