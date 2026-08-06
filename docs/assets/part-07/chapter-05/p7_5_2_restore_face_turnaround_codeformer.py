"""Create high-fidelity CodeFormer candidates from a 2×2 face turnaround.

This is a facial-feature restoration step, not a style-transfer step.  It
processes each visible 512px face separately with CodeFormer's highest input
fidelity setting (``w=1.0``), then performs a deterministic 2× Lanczos resize.
The rear view has no face, so it is enlarged without CodeFormer.

Install CodeFormer in a separate environment or checkout, then pass its root
and ``codeformer.pth`` explicitly.  The generated files require human review;
in particular, reject a candidate if its nose line, eye shape, lip contour, or
jaw silhouette changes.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import cv2
import numpy as np
import torch
from PIL import Image, ImageOps


ASSET_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = ASSET_DIR / "p7-5-2-face-turnaround-reference.png"
PANEL_NAMES = ("front", "front-quarter", "profile", "rear")
VISIBLE_FACE_PANELS = frozenset(PANEL_NAMES[:-1])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--codeformer-root", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True, help="CodeFormer codeformer.pth path")
    parser.add_argument("--output-dir", type=Path, default=ASSET_DIR)
    parser.add_argument("--prefix", default="p7-5-2-face-turnaround-codeformer")
    parser.add_argument("--device", choices=("auto", "cuda", "cpu"), default="auto")
    return parser.parse_args()


def select_device(requested: str) -> torch.device:
    if requested == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested, but is unavailable.")
    if requested == "cpu" or not torch.cuda.is_available():
        return torch.device("cpu")
    return torch.device("cuda")


def load_codeformer(root: Path, model_path: Path, device: torch.device):
    """Load the official 512px CodeFormer architecture and EMA checkpoint."""
    if not root.is_dir():
        raise FileNotFoundError(f"CodeFormer checkout not found: {root}")
    if not model_path.is_file():
        raise FileNotFoundError(f"CodeFormer checkpoint not found: {model_path}")
    sys.path.insert(0, str(root))
    from basicsr.utils.registry import ARCH_REGISTRY  # pylint: disable=import-outside-toplevel

    network = ARCH_REGISTRY.get("CodeFormer")(
        dim_embd=512,
        codebook_size=1024,
        n_head=8,
        n_layers=9,
        connect_list=["32", "64", "128", "256"],
    ).to(device)
    checkpoint = torch.load(model_path, map_location=device, weights_only=False)["params_ema"]
    network.load_state_dict(checkpoint)
    network.eval()
    return network


def restore_aligned_face(panel: Image.Image, network, device: torch.device) -> Image.Image:
    """Run the official aligned-face path with maximum fidelity (w=1.0)."""
    from basicsr.utils import img2tensor, tensor2img  # pylint: disable=import-outside-toplevel
    from torchvision.transforms.functional import normalize  # pylint: disable=import-outside-toplevel

    bgr = cv2.cvtColor(np.asarray(panel.convert("RGB")), cv2.COLOR_RGB2BGR)
    bgr = cv2.resize(bgr, (512, 512), interpolation=cv2.INTER_LINEAR)
    tensor = img2tensor(bgr / 255.0, bgr2rgb=True, float32=True)
    normalize(tensor, (0.5, 0.5, 0.5), (0.5, 0.5, 0.5), inplace=True)
    tensor = tensor.unsqueeze(0).to(device)
    with torch.no_grad():
        # w=1.0 gives CodeFormer its highest input-fidelity preference.
        output = network(tensor, w=1.0, adain=True)[0]
        restored_bgr = tensor2img(output, rgb2bgr=True, min_max=(-1, 1)).astype("uint8")
    if device.type == "cuda":
        torch.cuda.empty_cache()
    return Image.fromarray(cv2.cvtColor(restored_bgr, cv2.COLOR_BGR2RGB))


def main() -> None:
    args = parse_args()
    image = ImageOps.exif_transpose(Image.open(args.input)).convert("RGB")
    if image.width % 2 or image.height % 2:
        raise ValueError(f"Expected an even-width 2×2 turnaround sheet, got {image.size}.")
    device = select_device(args.device)
    network = load_codeformer(args.codeformer_root, args.model, device)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    half_width, half_height = image.width // 2, image.height // 2
    outputs: list[dict[str, object]] = []
    for index, name in enumerate(PANEL_NAMES):
        column, row = index % 2, index // 2
        box = (column * half_width, row * half_height, (column + 1) * half_width, (row + 1) * half_height)
        panel = image.crop(box)
        restored = name in VISIBLE_FACE_PANELS
        candidate = restore_aligned_face(panel, network, device) if restored else panel
        enlarged = candidate.resize((panel.width * 2, panel.height * 2), Image.Resampling.LANCZOS)
        output_path = args.output_dir / f"{args.prefix}-{name}-2x.png"
        enlarged.save(output_path)
        outputs.append({
            "panel": name,
            "source_crop": list(box),
            "face_restoration": "CodeFormer w=1.0" if restored else "not_applicable_rear_view",
            "enlargement": "Lanczos 2x",
            "output": output_path.name,
            "review_status": "human_review_required",
        })

    record_path = args.output_dir / f"{args.prefix}-review.json"
    record_path.write_text(json.dumps({
        "input": args.input.name,
        "model": args.model.name,
        "device": str(device),
        "panel_layout": "2x2: front, front-quarter, profile, rear",
        "outputs": outputs,
        "inspection_criteria": [
            "eye shape, iris color, and eye spacing are preserved",
            "nose bridge, tip, and profile projection are preserved",
            "lip contour and mouth width are preserved",
            "face width, jawline, and chin silhouette are preserved",
            "the restored face remains the same identity at the stated view direction",
        ],
        "approval": "Human review is required. Style evaluation belongs to a later stage.",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(outputs)} review candidates and {record_path.name}")


if __name__ == "__main__":
    main()
