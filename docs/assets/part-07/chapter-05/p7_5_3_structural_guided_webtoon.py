#!/usr/bin/env python3
"""Render a new webtoon cut from text plus a derived structural guide.

This is text-to-image, not img2img: diffusion starts from seeded noise.  The
structural condition is one or two depth, Canny, lineart, or OpenPose PNGs derived
after a text-only storyboard passed human review.  SDXL-family runs can add
separate approved character and face references through IP-Adapter.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import importlib.util
import json
from pathlib import Path
import sys
import sysconfig
from time import perf_counter
import types

import numpy as np
import torch
from diffusers import (
    ControlNetModel,
    FluxControlNetModel,
    MultiControlNetModel,
    StableDiffusionControlNetPipeline,
    StableDiffusionXLControlNetPipeline,
)
from PIL import Image, ImageDraw, ImageFilter


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
ANIMAGINE_XL_MODEL = Path(
    "/home/cbsim/.cache/huggingface/hub/"
    "models--cagliostrolab--animagine-xl-4.0/"
    "snapshots/2b7c1b397761bf5bd3cc42e5b39ec99314a75a96"
)
# Flux.1-dev와 InstantX ControlNet은 아직 이 저장소의 `.tmp/`에 내려받지 않았다.
# 경로만 선언하며, `--backbone flux1-dev`는 가중치를 준비한 뒤 별도 실행 계약으로 검수한다.
FLUX1_DEV_MODEL = PROJECT_ROOT / ".tmp/p7-5-3-flux1-dev"
DEPTH_CONTROLNET = PROJECT_ROOT / ".tmp/p7-5-3-controlnet-depth"
CANNY_CONTROLNET = PROJECT_ROOT / ".tmp/p7-5-3-controlnet-canny"
LINEART_CONTROLNET = PROJECT_ROOT / ".tmp/p7-5-3-controlnet-lineart"
SDXL_CANNY_CONTROLNET = PROJECT_ROOT / ".tmp/p7-5-3-controlnet-canny-sdxl-small"
SDXL_DEPTH_CONTROLNET = PROJECT_ROOT / ".tmp/p7-5-3-controlnet-depth-sdxl-small"
SDXL_OPENPOSE_CONTROLNET = Path(
    "/home/cbsim/.cache/huggingface/hub/models--xinsir--controlnet-openpose-sdxl-1.0/"
    "snapshots/23f966cd5cfdd3f7729c903e243d87152162d2b7"
)
OPENPOSE_ANNOTATORS = Path(
    "/home/cbsim/.cache/huggingface/hub/models--lllyasviel--Annotators/"
    "snapshots/982e7edaec38759d914a963c48c4726685de7d96"
)
DWPOSE_SOURCE = PROJECT_ROOT / ".tmp/p7-5-3-dwpose-source/ControlNet-v1-1-nightly"
DWPOSE_WEIGHTS = PROJECT_ROOT / ".tmp/p7-5-3-dwpose-weights"
FLUX1_CANNY_CONTROLNET = PROJECT_ROOT / ".tmp/p7-5-3-flux1-dev-controlnet-canny"
FLUX1_DEPTH_CONTROLNET = PROJECT_ROOT / ".tmp/p7-5-3-flux1-dev-controlnet-depth"
QWEN_IMAGE_MODEL = PROJECT_ROOT / ".tmp/p7-5-3-qwen-image"
QWEN_IMAGE_UNION_CONTROLNET = PROJECT_ROOT / ".tmp/p7-5-3-qwen-image-controlnet-union"
ZIMAGE_TURBO_MODEL = PROJECT_ROOT / ".tmp/p7-5-3-z-image-turbo"
# Z-Image Union은 config.json과 가중치를 함께 둔 Diffusers 폴더를 요구한다.
# 현재 내려받은 ComfyUI model-patch safetensors는 이 경로와 호환되지 않는다.
ZIMAGE_UNION_CONTROLNET = PROJECT_ROOT / ".tmp/p7-5-3-z-image-turbo-union"
IP_ADAPTER = Path(
    "/home/cbsim/.cache/huggingface/models--h94--IP-Adapter/"
    "snapshots/018e402774aeeddd60609b4ecdb7e298259dc729"
)
BASE_MODELS = {
    "sd15": SD15_MODEL,
    "sdxl": SDXL_MODEL,
    "animagine-xl": ANIMAGINE_XL_MODEL,
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
        "openpose": SDXL_OPENPOSE_CONTROLNET,
    },
    # Animagine XL은 SDXL ControlNet 가중치와 같은 입력 형태를 사용한다.
    "animagine-xl": {
        "canny": SDXL_CANNY_CONTROLNET,
        "depth": SDXL_DEPTH_CONTROLNET,
        "openpose": SDXL_OPENPOSE_CONTROLNET,
    },
    # Diffusers FluxControlNetPipeline supports InstantX Flux.1-dev Canny and depth.
    "flux1-dev": {"canny": FLUX1_CANNY_CONTROLNET, "depth": FLUX1_DEPTH_CONTROLNET},
    # Qwen Union은 canny, soft-edge(여기서는 lineart), depth를 하나의 ControlNet으로 받는다.
    "qwen-image": {
        "canny": QWEN_IMAGE_UNION_CONTROLNET,
        "depth": QWEN_IMAGE_UNION_CONTROLNET,
        "lineart": QWEN_IMAGE_UNION_CONTROLNET,
    },
    # Z-Image Union은 Canny, HED(여기서는 lineart), depth를 한 Diffusers 폴더로 받는다.
    "z-image-turbo": {
        "canny": ZIMAGE_UNION_CONTROLNET,
        "depth": ZIMAGE_UNION_CONTROLNET,
        "lineart": ZIMAGE_UNION_CONTROLNET,
    },
}
BACKBONE_DEFAULTS = {
    "sd15": {
        # SD 1.5 비교 결과는 사람 형상을 안정적으로 만들지 못해 보류 상태다.
        "guide_kind": "canny", "steps": 24, "scale": 0.80, "second_scale": 0.45,
        "width": 512, "height": 768, "guidance_scale": 7.0,
        "prompt": "full body contemporary dancer, black leotard, opaque black footed tights, rocky canyon",
        "negative_prompt": "extra limbs, malformed feet, cropped body, bare legs, bare feet, shoes",
        "character_reference_scale": 0.20,
    },
    "sdxl": {
        "guide_kind": "canny", "steps": 28, "scale": 0.50, "width": 768, "height": 1152,
        "guidance_scale": 7.0, "second_scale": 0.35,
        "prompt": "full body contemporary dancer, black leotard, opaque black footed tights, rocky canyon, webtoon illustration",
        "negative_prompt": "extra limbs, malformed feet, cropped body, bare legs, bare feet, shoes",
        "character_reference_scale": 0.20,
    },
    # seed=5413에서 Canny 0.80·24 step 및 얼굴 turnaround가 8 GB에서 구조를 보존했다.
    "animagine-xl": {
        "guide_kind": "canny", "steps": 24, "scale": 0.80, "second_scale": 0.35,
        "width": 768, "height": 1152, "guidance_scale": 5.0,
        "prompt": "1girl, solo, full body, dancer, black leotard, black footed tights, rocky canyon, anime webtoon",
        "negative_prompt": "extra limbs, malformed feet, cropped body, bare legs, bare feet, shoes",
        "character_reference_scale": 0.20,
    },
    # 공식 Flux ControlNet Canny 예시의 1024px·28 step·scale 0.5를 정적 후보로 둔다.
    # 이 저장소의 8 GB 환경에서의 실행 성립·VRAM·품질은 아직 검수하지 않았다.
    "flux1-dev": {
        "guide_kind": "canny", "steps": 28, "scale": 0.50, "width": 1024, "height": 1024,
        "guidance_scale": 3.5, "second_scale": 0.50,
        "prompt": "full body contemporary dancer, black leotard, opaque black footed tights, rocky canyon",
        "negative_prompt": "extra limbs, malformed feet, cropped body, bare legs, bare feet, shoes",
        "character_reference_scale": 0.20,
    },
    # Qwen 공식 ControlNet 예시: 30 step, true CFG 4.0, control scale 1.0.
    "qwen-image": {
        "guide_kind": "canny", "steps": 30, "scale": 1.0, "width": 1024, "height": 1024,
        "guidance_scale": 1.0, "true_cfg_scale": 4.0, "second_scale": 1.0,
        "prompt": "full body contemporary dancer, black leotard, opaque black footed tights, rocky canyon",
        "negative_prompt": "extra limbs, malformed feet, cropped body, bare legs, shoes",
        "character_reference_scale": 0.20,
    },
    # Z-Image Turbo ControlNet 예시: 8~9 step, CFG 0, control scale 0.75.
    "z-image-turbo": {
        "guide_kind": "canny", "steps": 9, "scale": 0.75, "width": 1024, "height": 1024,
        "guidance_scale": 0.0, "second_scale": 0.75,
        "prompt": "full body contemporary dancer, black leotard, opaque black footed tights, rocky canyon",
        "negative_prompt": "",
        "character_reference_scale": 0.20,
    },
}
# Flux.2 Klein은 현 Diffusers에서 image=[...] 다중 참조 입력을 받지만 Flux.2 ControlNet
# pipeline은 제공하지 않는다. 그러므로 Canny/depth 전용 BACKBONE_DEFAULTS에는 넣지 않는다.
# The scene and style are text conditions.  No storyboard RGB pixels are used.
# 이 단계에서는 프롬프트의 장면 지시를 줄여 구조 guide 수용도를 관찰한다.
BENCHMARK_PROMPT = "full body dancer"
BENCHMARK_NEGATIVE_PROMPT = "extra limbs, malformed feet, cropped body"
ANIMAGINE_BENCHMARK_PROMPT = "1girl, solo, full body, dancer, black leotard, black footed tights, anime webtoon"
HUMANML3D_CHAINS = (
    (0, 2, 5, 8, 11),
    (0, 1, 4, 7, 10),
    (0, 3, 6, 9, 12, 15),
    (9, 14, 17, 19, 21),
    (9, 13, 16, 18, 20),
)
OPENPOSE_CHAIN_COLORS = ((255, 85, 0), (255, 170, 0), (255, 255, 0), (0, 255, 85), (0, 170, 255))


def build_parser() -> argparse.ArgumentParser:
    """Offer reproducible settings while keeping the prompt and input boundary fixed."""
    parser = argparse.ArgumentParser(
        description="텍스트와 검수된 구조 guide로 새 웹툰 컷을 생성합니다. img2img는 쓰지 않습니다."
    )
    parser.add_argument("--seed", type=int, default=5413, help="재현용 seed (기본값: 5413)")
    parser.add_argument("--steps", type=int, help="backbone 기본 step을 덮어쓸 값")
    parser.add_argument("--scale", type=float, help="backbone 기본 구조 조건 강도를 덮어쓸 값")
    parser.add_argument("--width", type=int, help="backbone 기본 출력 너비를 덮어쓸 값")
    parser.add_argument("--height", type=int, help="backbone 기본 출력 높이를 덮어쓸 값")
    parser.add_argument(
        "--prompt",
        help="guide 수용도 비교용 최소 프롬프트 (생략 시 backbone 계약 기본값)",
    )
    parser.add_argument(
        "--negative-prompt",
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
        default="animagine-xl",
        help="텍스트-웹툰 기반 모델 (기본값: animagine-xl, 8 GB Canny 단일 가이드 계약)",
    )
    parser.add_argument(
        "--guide",
        type=Path,
        help="사람 검수한 depth·Canny·lineart·OpenPose PNG. --extract-openpose-from과 함께면 생략 가능",
    )
    parser.add_argument(
        "--guide-kind",
        choices=("depth", "canny", "lineart", "openpose"),
        help="guide와 짝이 되는 ControlNet 종류 (생략하면 backbone 기본값)",
    )
    parser.add_argument(
        "--second-guide",
        type=Path,
        help="같은 검수 스토리보드에서 얻은 두 번째 구조 guide (선택 사항; 자동 결합하지 않음).",
    )
    parser.add_argument(
        "--second-guide-kind",
        choices=("depth", "canny", "lineart", "openpose"),
        help="두 번째 guide와 짝이 되는 ControlNet 종류",
    )
    parser.add_argument(
        "--second-scale",
        type=float,
        help="두 번째 구조 조건 강도 (기본값: --scale과 같음)",
    )
    parser.add_argument(
        "--extract-openpose-from",
        type=Path,
        help="승인 스토리보드 RGB에서 OpenPose 관절 지도를 추출해 이 실행의 openpose guide로 사용합니다.",
    )
    parser.add_argument(
        "--openpose-output",
        type=Path,
        help="추출 OpenPose PNG 경로. 생략하면 스토리보드 옆에 '-openpose.png'로 저장합니다.",
    )
    parser.add_argument(
        "--extract-dwpose-from",
        type=Path,
        help=(
            "DWPose whole-body detector로 승인 스토리보드에서 관절 지도를 추출합니다. "
            "OpenPose가 빈 지도를 낸 stylized/occluded 포즈의 대안입니다. 다리 연결은 사람이 검수해야 합니다."
        ),
    )
    parser.add_argument(
        "--dwpose-output",
        type=Path,
        help="추출 DWPose PNG 경로. 생략하면 스토리보드 옆에 '-dwpose.png'로 저장합니다.",
    )
    parser.add_argument(
        "--render-3d-joints",
        type=Path,
        help=(
            "T2M-GPT처럼 22개 HumanML3D 관절을 가진 [frame, 22, 3] NPY. "
            "한 프레임을 OpenPose로 렌더링해 storyboard RGB 대신 구조 입력으로 씁니다."
        ),
    )
    parser.add_argument(
        "--render-3d-pose-output-dir",
        type=Path,
        help="3D 관절에서 렌더한 OpenPose·깊이 PNG 저장 폴더",
    )
    parser.add_argument(
        "--pose-frame", type=int,
        help="쓸 모션 프레임. 생략하면 골반보다 가장 높이 올라간 발 프레임을 고릅니다.",
    )
    parser.add_argument(
        "--pose-yaw-degrees", type=float, default=0.0,
        help="3D 관절을 2D로 투영할 때 수직축 기준 카메라 회전 각도 (기본값: 0)",
    )
    parser.add_argument(
        "--use-rendered-skeleton-depth", action="store_true",
        help=(
            "--render-3d-joints와 함께, 관절·뼈대의 z-order 깊이 지도를 두 번째 ControlNet으로 추가합니다. "
            "인체 표면 depth가 아닌 가려짐 보조 힌트입니다."
        ),
    )
    parser.add_argument(
        "--use-rendered-surface-guides", action="store_true",
        help=(
            "--render-3d-joints의 관절을 굵기 있는 capsule 표면으로 z-buffer 렌더한 "
            "silhouette Canny와 surface-depth를 사용합니다. OpenPose+뼈대 depth의 대안입니다."
        ),
    )
    parser.add_argument(
        "--sequential-cpu-offload", action="store_true",
        help=(
            "다중 ControlNet이 8 GB에 동시에 올라가지 않을 때 모듈 단위 CPU 오프로딩을 사용합니다. "
            "생성 시간은 늘어나므로 수용도 검증에만 씁니다."
        ),
    )
    parser.add_argument(
        "--character-reference",
        type=Path,
        action="append",
        help="캐릭터·의상 일관성용 전신/소품 참조 PNG. 여러 번 지정하면 Plus IP-Adapter에 한 그룹으로 전달합니다.",
    )
    parser.add_argument(
        "--face-reference",
        type=Path,
        action="append",
        help="얼굴 일관성용 얼굴 전용 참조 PNG. 지정하면 기본 turnaround 묶음을 이 목록으로 바꿉니다.",
    )
    parser.add_argument(
        "--no-face-reference",
        action="store_true",
        help="기본 얼굴 turnaround 참조를 끄고 구조 guide만 비교합니다.",
    )
    parser.add_argument(
        "--character-reference-scale",
        type=float,
        help="SDXL/Animagine IP-Adapter 참조 강도 (생략 시 backbone 기본값)",
    )
    parser.add_argument(
        "--allow-character-multiguide-probe",
        action="store_true",
        help=(
            "8 GB에서 단일 IP-Adapter와 두 구조 guide를 함께 쓰는 저해상도 검증을 명시적으로 허용합니다. "
            "--sequential-cpu-offload, 한 IP-Adapter 그룹, 최대 512×768을 요구하며 사람 검수용 결과만 만듭니다."
        ),
    )
    parser.add_argument(
        "--lora-path",
        type=Path,
        help="검증할 SDXL/Animagine LoRA 가중치가 든 폴더 또는 safetensors 파일. IP-Adapter와 달리 학습된 캐릭터 토큰을 적용합니다.",
    )
    parser.add_argument(
        "--lora-scale",
        type=float,
        default=0.8,
        help="--lora-path 적용 강도 (기본값: 0.8)",
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


def load_reference_images(reference_paths: list[Path], option_name: str) -> list[Image.Image]:
    """Load one approved multi-view group for its matching IP-Adapter."""
    if not reference_paths:
        return []
    for path in reference_paths:
        if not path.is_file():
            raise FileNotFoundError(f"{option_name} PNG를 찾지 못했습니다: {path}")
    return [Image.open(path).convert("RGB") for path in reference_paths]


def openpose_detector_class():
    """Load the cached OpenPose annotator without importing its optional extras globally."""
    package_root = Path(sysconfig.get_paths()["purelib"]) / "controlnet_aux"
    parent = types.ModuleType("p7_5_3_openpose_aux")
    parent.__path__ = [str(package_root)]
    sys.modules[parent.__name__] = parent
    package = package_root / "open_pose"
    spec = importlib.util.spec_from_file_location(
        "p7_5_3_openpose_aux.open_pose",
        package / "__init__.py",
        submodule_search_locations=[str(package)],
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("로컬 OpenPose annotator 구현을 찾지 못했습니다.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.OpenposeDetector


def extract_openpose(storyboard: Path, output: Path) -> Path:
    """Derive a body-only pose map; no storyboard colours or textures are passed on."""
    if not storyboard.is_file():
        raise FileNotFoundError(f"OpenPose를 추출할 스토리보드를 찾지 못했습니다: {storyboard}")
    if not OPENPOSE_ANNOTATORS.exists():
        raise FileNotFoundError(f"OpenPose annotator 가중치를 찾지 못했습니다: {OPENPOSE_ANNOTATORS}")
    detector = openpose_detector_class().from_pretrained(OPENPOSE_ANNOTATORS)
    pose = detector(Image.open(storyboard).convert("RGB"), hand_and_face=False).convert("RGB")
    if not np.any(np.asarray(pose)):
        raise ValueError(
            "스토리보드에서 OpenPose 신체 관절을 검출하지 못했습니다. "
            "빈 OpenPose map은 LoRA·ControlNet 입력으로 사용하지 않습니다."
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    pose.save(output)
    return output


def extract_dwpose(storyboard: Path, output: Path) -> Path:
    """Derive a DWPose map when OpenPose cannot associate an occluded silhouette."""
    if not storyboard.is_file():
        raise FileNotFoundError(f"DWPose를 추출할 스토리보드를 찾지 못했습니다: {storyboard}")
    required = (
        DWPOSE_SOURCE / "annotator/dwpose/__init__.py",
        DWPOSE_WEIGHTS / "yolox_l.onnx",
        DWPOSE_WEIGHTS / "dw-ll_ucoco_384.onnx",
    )
    missing = [path for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "DWPose 임시 소스 또는 Apache-2.0 ONNX 가중치를 찾지 못했습니다: "
            + ", ".join(str(path) for path in missing)
        )
    source_root = str(DWPOSE_SOURCE)
    if source_root not in sys.path:
        sys.path.insert(0, source_root)
    from annotator.dwpose import DWposeDetector

    source = np.asarray(Image.open(storyboard).convert("RGB"))[:, :, ::-1].copy()
    detector = DWposeDetector()
    pose_bgr = detector(source)
    if not np.any(pose_bgr):
        raise ValueError("스토리보드에서 DWPose 관절을 검출하지 못했습니다.")
    output.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(pose_bgr[:, :, ::-1]).save(output)
    return output


def render_humanml3d_guides(
    joints_path: Path, output_dir: Path, width: int, height: int, frame: int | None, yaw_degrees: float
) -> tuple[Path, Path, int]:
    """Render 3D joints as paired OpenPose and bone z-order maps.

    The second map deliberately encodes only joint/bone ordering, not a body surface.
    It can disambiguate a lifted leg crossing a torso, but cannot solve cloth or body
    silhouette occlusion in the way a mesh/DensePose condition could.
    """
    if not joints_path.is_file():
        raise FileNotFoundError(f"3D 관절 NPY를 찾지 못했습니다: {joints_path}")
    sequence = np.load(joints_path)
    if sequence.ndim != 3 or sequence.shape[1:] != (22, 3):
        raise ValueError("--render-3d-joints는 [frame, 22, 3] HumanML3D float NPY여야 합니다.")
    if frame is None:
        raised_foot = np.maximum(sequence[:, 10, 1], sequence[:, 11, 1]) - sequence[:, 0, 1]
        frame = int(np.argmax(raised_foot))
    if not 0 <= frame < len(sequence):
        raise ValueError(f"--pose-frame은 0..{len(sequence) - 1} 범위여야 합니다.")
    joints = sequence[frame]
    yaw = np.deg2rad(yaw_degrees)
    horizontal = joints[:, 0] * np.cos(yaw) + joints[:, 2] * np.sin(yaw)
    depth = -joints[:, 0] * np.sin(yaw) + joints[:, 2] * np.cos(yaw)
    vertical = joints[:, 1]
    scale = min(
        width * 0.72 / max(float(np.ptp(horizontal)), 0.1),
        height * 0.78 / max(float(np.ptp(vertical)), 0.1),
    )
    points = [
        (int(width / 2 + x * scale), int(height * 0.90 - (y - vertical.min()) * scale))
        for x, y in zip(horizontal, vertical)
    ]
    pose = Image.new("RGB", (width, height), "black")
    depth_map = Image.new("L", (width, height), 0)
    pose_draw = ImageDraw.Draw(pose)
    depth_draw = ImageDraw.Draw(depth_map)
    low, high = np.percentile(depth, (5, 95))
    intensity = np.clip((depth - low) / max(float(high - low), 1e-6) * 190 + 65, 0, 255).astype(np.uint8)
    for chain, color in zip(HUMANML3D_CHAINS, OPENPOSE_CHAIN_COLORS):
        for first, second in zip(chain, chain[1:]):
            pose_draw.line((points[first], points[second]), fill=color, width=10)
            depth_draw.line(
                (points[first], points[second]),
                fill=(int(intensity[first]) + int(intensity[second])) // 2,
                width=18,
            )
    for joint in np.argsort(depth)[::-1]:
        x, y = points[int(joint)]
        pose_draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill="white")
        depth_draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill=int(intensity[joint]))
    output_dir.mkdir(parents=True, exist_ok=True)
    pose_path = output_dir / "3d-joints-openpose.png"
    depth_path = output_dir / "3d-joints-skeleton-depth.png"
    pose.save(pose_path)
    depth_map.convert("RGB").save(depth_path)
    return pose_path, depth_path, frame


def render_humanml3d_surface_guides(
    joints_path: Path, output_dir: Path, width: int, height: int, frame: int, yaw_degrees: float
) -> tuple[Path, Path]:
    """Approximate an occlusion-aware body surface without a restricted SMPL asset.

    Capsules are deliberately a structural proxy, not a character mesh.  A z-buffer
    resolves which limb is visible at crossings before converting the silhouette to
    an edge map, avoiding the ambiguous, coloured stick figure used by OpenPose.
    """
    sequence = np.load(joints_path)
    joints = sequence[frame]
    yaw = np.deg2rad(yaw_degrees)
    horizontal = joints[:, 0] * np.cos(yaw) + joints[:, 2] * np.sin(yaw)
    depth = -joints[:, 0] * np.sin(yaw) + joints[:, 2] * np.cos(yaw)
    vertical = joints[:, 1]
    scale = min(
        width * 0.72 / max(float(np.ptp(horizontal)), 0.1),
        height * 0.78 / max(float(np.ptp(vertical)), 0.1),
    )
    points = np.column_stack((width / 2 + horizontal * scale, height * 0.90 - (vertical - vertical.min()) * scale))
    # pelvis, left/right leg, spine/head, right/left arm; radii are metres in the
    # normalized HumanML3D coordinate system and intentionally do not encode identity.
    radii = np.array([
        .16, .13, .13, .15, .12, .12, .14, .10, .10, .15, .08, .08,
        .10, .11, .10, .09, .10, .09, .08, .07, .07, .06,
    ])
    z_buffer = np.full((height, width), -np.inf, dtype=np.float32)
    for chain in HUMANML3D_CHAINS:
        for start, end in zip(chain, chain[1:]):
            distance = np.linalg.norm(joints[end] - joints[start])
            samples = max(2, int(np.ceil(distance / 0.035)))
            for fraction in np.linspace(0.0, 1.0, samples):
                xy = points[start] * (1 - fraction) + points[end] * fraction
                z = depth[start] * (1 - fraction) + depth[end] * fraction
                radius = (radii[start] * (1 - fraction) + radii[end] * fraction) * scale
                left = max(0, int(np.floor(xy[0] - radius)))
                right = min(width, int(np.ceil(xy[0] + radius + 1)))
                top = max(0, int(np.floor(xy[1] - radius)))
                bottom = min(height, int(np.ceil(xy[1] + radius + 1)))
                yy, xx = np.ogrid[top:bottom, left:right]
                disk = (xx - xy[0]) ** 2 + (yy - xy[1]) ** 2 <= radius ** 2
                local = z_buffer[top:bottom, left:right]
                local[disk] = np.maximum(local[disk], z)
    visible = np.isfinite(z_buffer)
    if not np.any(visible):
        raise ValueError("3D 관절 surface blockout을 렌더하지 못했습니다.")
    low, high = np.percentile(z_buffer[visible], (2, 98))
    depth_map = np.zeros_like(z_buffer, dtype=np.uint8)
    depth_map[visible] = np.clip(
        (z_buffer[visible] - low) / max(float(high - low), 1e-6) * 190 + 65, 0, 255
    ).astype(np.uint8)
    silhouette = Image.fromarray((visible * 255).astype(np.uint8))
    canny_like = silhouette.filter(ImageFilter.FIND_EDGES).convert("RGB")
    output_dir.mkdir(parents=True, exist_ok=True)
    canny_path = output_dir / "3d-surface-silhouette-canny.png"
    depth_path = output_dir / "3d-surface-depth.png"
    canny_like.save(canny_path)
    Image.fromarray(depth_map).convert("RGB").save(depth_path)
    return canny_path, depth_path


def main() -> None:
    """Generate one controlled cut and write a comparable performance/adherence record."""
    args = build_parser().parse_args()
    defaults = BACKBONE_DEFAULTS[args.backbone]
    args.guide_kind = args.guide_kind or defaults["guide_kind"]
    args.prompt = args.prompt or defaults["prompt"]
    args.negative_prompt = (
        args.negative_prompt if args.negative_prompt is not None else defaults["negative_prompt"]
    )
    args.character_reference_scale = (
        args.character_reference_scale
        if args.character_reference_scale is not None
        else defaults["character_reference_scale"]
    )
    args.steps = args.steps or defaults["steps"]
    args.scale = args.scale if args.scale is not None else defaults["scale"]
    args.width = args.width or defaults["width"]
    args.height = args.height or defaults["height"]
    rendered_pose_frame = None
    rendered_depth_path = None
    if args.render_3d_joints:
        if args.guide or args.extract_openpose_from or args.second_guide:
            raise ValueError(
                "--render-3d-joints는 --guide·--extract-openpose-from·--second-guide와 함께 쓰지 않습니다."
            )
        render_dir = args.render_3d_pose_output_dir or (
            ASSET_DIR / "p7-5-3-3d-pose-guides"
        )
        args.guide, rendered_depth_path, rendered_pose_frame = render_humanml3d_guides(
            args.render_3d_joints,
            render_dir,
            args.width,
            args.height,
            args.pose_frame,
            args.pose_yaw_degrees,
        )
        args.guide_kind = "openpose"
        if args.use_rendered_skeleton_depth and args.use_rendered_surface_guides:
            raise ValueError(
                "--use-rendered-skeleton-depth와 --use-rendered-surface-guides 중 하나만 지정하세요."
            )
        if args.use_rendered_surface_guides:
            args.guide, rendered_depth_path = render_humanml3d_surface_guides(
                args.render_3d_joints,
                render_dir,
                args.width,
                args.height,
                rendered_pose_frame,
                args.pose_yaw_degrees,
            )
            args.guide_kind = "canny"
            args.second_guide = rendered_depth_path
            args.second_guide_kind = "depth"
        if args.use_rendered_skeleton_depth:
            args.second_guide = rendered_depth_path
            args.second_guide_kind = "depth"
    if args.extract_openpose_from:
        if args.extract_dwpose_from:
            raise ValueError("--extract-openpose-from과 --extract-dwpose-from 중 하나만 지정하세요.")
        output = args.openpose_output or args.extract_openpose_from.with_name(
            f"{args.extract_openpose_from.stem}-openpose.png"
        )
        args.guide = extract_openpose(args.extract_openpose_from, output)
        args.guide_kind = "openpose"
    if args.extract_dwpose_from:
        output = args.dwpose_output or args.extract_dwpose_from.with_name(
            f"{args.extract_dwpose_from.stem}-dwpose.png"
        )
        args.guide = extract_dwpose(args.extract_dwpose_from, output)
        args.guide_kind = "openpose"
    if not args.guide:
        raise ValueError("--guide 또는 --extract-openpose-from 중 하나가 필요합니다.")
    if bool(args.second_guide) != bool(args.second_guide_kind):
        raise ValueError("--second-guide와 --second-guide-kind는 함께 지정해야 합니다.")
    guide_paths = [args.guide]
    guide_kinds = [args.guide_kind]
    guide_scales = [args.scale]
    if args.second_guide:
        guide_paths.append(args.second_guide)
        guide_kinds.append(args.second_guide_kind)
        guide_scales.append(
            args.second_scale
            if args.second_scale is not None
            else defaults.get("second_scale", args.scale)
        )
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
    if args.lora_path and args.backbone not in {"sdxl", "animagine-xl"}:
        raise ValueError("현재 LoRA 검증 경로는 SDXL/Animagine XL에서만 지원합니다.")
    if args.lora_path and not args.lora_path.exists():
        raise FileNotFoundError(f"LoRA 경로를 찾지 못했습니다: {args.lora_path}")
    reference_paths = args.character_reference or []
    face_reference_paths = (
        []
        if args.no_face_reference
        else args.face_reference
        or []
    )
    has_references = bool(reference_paths or face_reference_paths)
    if has_references and len(guide_paths) > 1 and not args.allow_character_multiguide_probe:
        raise ValueError(
            "8 GB 계약에서는 캐릭터 참조와 Canny+Depth 동시 조건을 지원하지 않습니다. "
            "검증하려면 --allow-character-multiguide-probe를 명시하고 저해상도 CPU offload 계약을 지키세요."
        )
    if reference_paths and face_reference_paths:
        raise ValueError(
            "8 GB에서는 Plus와 Plus-Face IP-Adapter를 동시에 적재할 수 없습니다. "
            "전신·의상 비교에는 --character-reference만, 얼굴 비교에는 --face-reference만 지정하세요."
        )
    if (reference_paths or face_reference_paths) and args.backbone not in {"sdxl", "animagine-xl"}:
        raise ValueError("캐릭터 다중 참조는 현재 SDXL/Animagine XL IP-Adapter 경로에서만 지원합니다.")
    if args.allow_character_multiguide_probe:
        if not (has_references and len(guide_paths) == 2):
            raise ValueError(
                "--allow-character-multiguide-probe는 캐릭터 참조 한 그룹과 구조 guide 두 개를 함께 줄 때만 씁니다."
            )
        if not args.sequential_cpu_offload:
            raise ValueError(
                "캐릭터+다중 guide 검증은 8 GB에서 --sequential-cpu-offload를 반드시 사용합니다."
            )
        if args.width > 512 or args.height > 768:
            raise ValueError(
                "캐릭터+다중 guide 검증은 8 GB에서 최대 512×768만 허용합니다."
            )
    reference_images = load_reference_images(reference_paths, "--character-reference")
    face_reference_images = load_reference_images(face_reference_paths, "--face-reference")
    if (reference_images or face_reference_images) and not IP_ADAPTER.exists():
        raise FileNotFoundError(f"IP-Adapter 가중치를 찾지 못했습니다: {IP_ADAPTER}")
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

            # Z-Image Union은 config.json을 포함한 Diffusers 폴더 가중치 계약이다.
            controlnets.append(
                ZImageControlNetModel.from_pretrained(
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
    # IP-Adapter와 함께 쓸 때도 다중 ControlNet을 명시적 모듈로 감싼다.
    # list를 넘기는 자동 변환은 현 Diffusers 조합에서 adapter attention 입력을 깨뜨릴 수 있다.
    controlnet = controlnets[0] if len(controlnets) == 1 else MultiControlNetModel(controlnets)
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
            "animagine-xl": StableDiffusionXLControlNetPipeline,
        }[args.backbone]
    base_model = BASE_MODELS[args.backbone]
    pipeline = pipeline_class.from_pretrained(
        base_model,
        controlnet=controlnet,
        torch_dtype=torch.bfloat16 if (is_flux or is_qwen or is_zimage) else torch.float16,
        local_files_only=True,
    )
    if args.lora_path:
        if args.lora_path.is_dir():
            pipeline.load_lora_weights(str(args.lora_path))
        else:
            pipeline.load_lora_weights(str(args.lora_path.parent), weight_name=args.lora_path.name)
        pipeline.fuse_lora(lora_scale=args.lora_scale)
    if reference_images or face_reference_images:
        adapter_weights = []
        adapter_scales = []
        if reference_images:
            adapter_weights.append("ip-adapter-plus_sdxl_vit-h.safetensors")
            adapter_scales.append(args.character_reference_scale)
        if face_reference_images:
            adapter_weights.append("ip-adapter-plus-face_sdxl_vit-h.safetensors")
            adapter_scales.append(args.character_reference_scale)
        pipeline.load_ip_adapter(
            str(IP_ADAPTER),
            subfolder="sdxl_models",
            weight_name=adapter_weights,
            image_encoder_folder="models/image_encoder",
            local_files_only=True,
        )
        pipeline.set_ip_adapter_scale(adapter_scales)
    if args.sequential_cpu_offload:
        pipeline.enable_sequential_cpu_offload()
    else:
        pipeline.enable_model_cpu_offload()
    # attention slicing은 IP-Adapter 전용 attention processor를 덮어쓰므로 함께 켜지 않는다.
    if not (is_flux or is_qwen or is_zimage or reference_images or face_reference_images):
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
    if reference_images or face_reference_images:
        # Diffusers expects one image-group per loaded IP-Adapter.  Group 0
        # carries full-body/outfit evidence, group 1 carries cropped faces.
        ip_adapter_groups = []
        if reference_images:
            ip_adapter_groups.append(reference_images)
        if face_reference_images:
            ip_adapter_groups.append(face_reference_images)
        pipeline_inputs["ip_adapter_image"] = ip_adapter_groups
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
        "openpose_source": str(args.extract_openpose_from) if args.extract_openpose_from else None,
        "dwpose_source": str(args.extract_dwpose_from) if args.extract_dwpose_from else None,
        "rendered_3d_joints_source": str(args.render_3d_joints) if args.render_3d_joints else None,
        "rendered_3d_pose_frame": rendered_pose_frame,
        "rendered_skeleton_depth": str(rendered_depth_path) if rendered_depth_path else None,
        "rendered_surface_guides": args.use_rendered_surface_guides,
        "guide_kinds": guide_kinds,
        "guide_scales": guide_scales,
        "character_references": [str(path) for path in reference_paths],
        "face_references": [str(path) for path in face_reference_paths],
        "character_reference_scale": (
            args.character_reference_scale if (reference_paths or face_reference_paths) else None
        ),
        "lora_path": str(args.lora_path) if args.lora_path else None,
        "lora_scale": args.lora_scale if args.lora_path else None,
        "width": args.width,
        "height": args.height,
        "steps": args.steps,
        "guidance_scale": defaults["guidance_scale"],
        "true_cfg_scale": pipeline_inputs.get("true_cfg_scale"),
        "control_window": [args.control_guidance_start, args.control_guidance_end],
        "sequential_cpu_offload": args.sequential_cpu_offload,
        "character_multiguide_probe": args.allow_character_multiguide_probe,
        "elapsed_seconds": round(elapsed_seconds, 3),
        "peak_vram_mib": round(torch.cuda.max_memory_allocated() / 1024**2, 1),
        "output": str(output),
        "guide_adherence": {
            "status": "human-review-required",
            "criterion": (
                "guide의 인물 윤곽·발과 지면의 분리·절벽의 상대 위치와, "
                "앞쪽 다리/몸통의 가려짐 순서가 유지되는지"
            ),
        },
        "character_adherence": {
            "status": "human-review-required" if has_references else "not-conditioned",
            "criterion": (
                "얼굴의 식별 특징, 체형, 검은 타이즈 복장이 참조와 일치하고 "
                "얼굴·양팔·양다리가 모두 판별되는지"
            ),
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
