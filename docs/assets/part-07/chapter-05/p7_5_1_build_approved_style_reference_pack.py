"""Write the manifest for approved P7-5.1 individual style-reference originals."""

import json
from pathlib import Path

ASSET_DIR = Path(__file__).resolve().parent
PREFIX = "p7-5-1-approved-style-reference-pack"
REFERENCES = []


def main() -> None:
    manifest = {
        "status": "blocked_pending_local_gpu_regeneration",
        "purpose": "P7-5.1 local-GPU style-reference originals awaiting human review",
        "model_input_rule": "No downstream diffusion call may use a reference until a human approves a local-GPU original and adds it to references.",
        "gate_status": "blocked_pending_local_gpu_regeneration",
        "references": REFERENCES,
    }
    manifest_path = ASSET_DIR / f"{PREFIX}.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"references: {len(REFERENCES)}")
    print(f"manifest: {manifest_path.name}")


if __name__ == "__main__":
    main()
