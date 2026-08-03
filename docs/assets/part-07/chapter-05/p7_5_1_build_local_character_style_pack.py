"""Build a reviewable mirror-safe local character-and-style anchor pack."""

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


ASSET_DIR = Path(__file__).parent
PREFIX = "p7-5-1-local-character-style-pack-v1"
SOURCES = {
    "front": ASSET_DIR / f"{PREFIX}-master.png",
    "three_quarter_left": ASSET_DIR / f"{PREFIX}-three-quarter-left.png",
    "profile_left": ASSET_DIR / f"{PREFIX}-profile-left.png",
    "rear_three_quarter_left": ASSET_DIR / f"{PREFIX}-rear-three-quarter-left.png",
}


def save_mirror(source_id: str, target_id: str) -> Path:
    target = ASSET_DIR / f"{PREFIX}-{target_id}.png"
    ImageOps.mirror(Image.open(SOURCES[source_id]).convert("RGB")).save(target)
    return target


def main() -> None:
    missing = [str(path) for path in SOURCES.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError("\n".join(missing))

    mirrored = {
        "three_quarter_right": save_mirror("three_quarter_left", "three-quarter-right-mirrored"),
        "profile_right": save_mirror("profile_left", "profile-right-mirrored"),
        "rear_three_quarter_right": save_mirror("rear_three_quarter_left", "rear-three-quarter-right-mirrored"),
    }
    entries = [
        ("front", SOURCES["front"], "base text-to-image"),
        ("three-quarter-left", SOURCES["three_quarter_left"], "single-reference generation"),
        ("three-quarter-right", mirrored["three_quarter_right"], "deterministic horizontal mirror"),
        ("profile-left", SOURCES["profile_left"], "single-reference generation"),
        ("profile-right", mirrored["profile_right"], "deterministic horizontal mirror"),
        ("rear-three-quarter-left", SOURCES["rear_three_quarter_left"], "single-reference generation"),
        ("rear-three-quarter-right", mirrored["rear_three_quarter_right"], "deterministic horizontal mirror"),
    ]
    thumbnail_size = (384, 576)
    sheet = Image.new("RGB", (thumbnail_size[0] * 4, (thumbnail_size[1] + 28) * 2), "white")
    draw = ImageDraw.Draw(sheet)
    for index, (view_id, image_path, _) in enumerate(entries):
        x = (index % 4) * thumbnail_size[0]
        y = (index // 4) * (thumbnail_size[1] + 28)
        draw.text((x + 6, y + 5), view_id, fill="black")
        thumbnail = Image.open(image_path).convert("RGB").resize(thumbnail_size, Image.Resampling.LANCZOS)
        sheet.paste(thumbnail, (x, y + 28))
    sheet.save(ASSET_DIR / f"{PREFIX}-contact-sheet.png")

    manifest = {
        "status": "approved_limited_scope",
        "scope": "local-only mirror-safe character and style anchor; neutral full-body turnarounds only",
        "excluded_scope": [
            "asymmetric accessories and props",
            "bag, strap, object contact, and hand-object detail",
            "dynamic pose, scene composition, and extreme camera",
            "face close-up preservation",
        ],
        "base_master": {
            "model_id": "black-forest-labs/FLUX.2-klein-base-4B",
            "runtime": "Diffusers Flux2KleinPipeline sequential CPU offload",
            "size": [768, 1152],
            "steps": 50,
            "guidance_scale": 4.0,
            "seed": 410201,
        },
        "view_expansion": {
            "model_id": "black-forest-labs/FLUX.2-klein-4B",
            "runtime": "Diffusers Flux2KleinPipeline sequential CPU offload",
            "size": [768, 1152],
            "steps": 4,
            "guidance_scale": 1.0,
        },
        "style_contract": {
            "line": "thin charcoal outlines",
            "palette": "low-saturation teal, white, charcoal, and warm light skin",
            "shading": "subtle fold shadows without screentones or painterly texture",
            "background": "plain white studio background",
        },
        "character_contract": {
            "hair": "symmetric deep teal-blue jaw-length bob with a soft center part",
            "outfit": "white cropped utility jacket, charcoal crew-neck shirt, teal high-waisted wide-leg trousers, white sneakers",
            "accessories": "none",
        },
        "views": [
            {"view_id": view_id, "image": image_path.name, "method": method}
            for view_id, image_path, method in entries
        ],
        "contact_sheet": f"{PREFIX}-contact-sheet.png",
    }
    (ASSET_DIR / f"{PREFIX}.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
