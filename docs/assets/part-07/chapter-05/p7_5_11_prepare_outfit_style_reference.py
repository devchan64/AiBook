"""Make one role-separated Qwen reference for outfit and approved rendering style."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[4]
OUTFIT = ROOT / "docs/assets/part-07/chapter-05/p7-5-2-fullbody-front-refined-reference.png"
STYLE = ROOT / "docs/assets/part-07/chapter-05/p7-5-1-style-atrium-dawn-high-angle-qwen-image-qwen30-v3-scene01-code-7a21c8-seed-420713-steps-30.png"
OUTPUT = ROOT / "docs/assets/part-07/chapter-05/p7-5-11-outfit-and-watercolor-reference.png"


def main() -> None:
    outfit = Image.open(OUTFIT).convert("RGB")
    style = Image.open(STYLE).convert("RGB")
    canvas = Image.new("RGB", (outfit.width + style.width, outfit.height), "#f7f5ef")
    canvas.paste(outfit, (0, 0))
    canvas.paste(style, (outfit.width, 0))
    divider = ImageDraw.Draw(canvas)
    divider.line((outfit.width, 0, outfit.width, canvas.height), fill="#535a59", width=8)
    canvas.save(OUTPUT)
    OUTPUT.with_suffix(".json").write_text(
        json.dumps(
            {
                "purpose": "Qwen image 3: one reference with separately visible outfit and rendering-style regions",
                "left_region": {"source": str(OUTFIT), "role": "complete character outfit"},
                "right_region": {"source": str(STYLE), "role": "approved P7-5.1 watercolor rendering"},
                "layout": "equal-width vertical panels; no character or scene from the style panel is a content reference",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()
