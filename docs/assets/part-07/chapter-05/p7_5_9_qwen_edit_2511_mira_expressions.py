#!/usr/bin/env python3
"""Compare independent facial-expression edits of the P7-5.2 Mira portrait."""
from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path

from p7_5_2_qwen_edit_2511_generate_mira_torso import (
    ASSETS, CACHE_DIR, DEFAULT_FACE, MODEL_ID, runtime_record, sha256,
)

SPEC_PATH = ASSETS / "p7-5-9-mira-expression-spec.json"


def main() -> None:
    catalog = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    expressions = {item["id"]: item for item in catalog["expressions"]}
    if len(expressions) != len(catalog["expressions"]):
        raise ValueError("Expression IDs must be unique")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_FACE)
    parser.add_argument("--expressions", nargs="+", choices=expressions, default=list(expressions))
    parser.add_argument("--size", type=int, default=1024)
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--cfg", type=float, default=4.0)
    parser.add_argument("--run-label", default="run")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.size < 32 or args.size % 32 or args.steps < 1 or args.cfg < 1:
        parser.error("size must be a positive multiple of 32; steps >= 1; cfg >= 1")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.run_label):
        parser.error("run-label must contain only letters, digits, underscores and hyphens")
    source = args.input.resolve()
    if not source.is_file():
        parser.error(f"Missing input: {source}")
    jobs = []
    for name in dict.fromkeys(args.expressions):
        stem = f"p7-5-9-mira-expression-{name}-{args.run_label}-size-{args.size}-seed-{args.seed}-steps-{args.steps}"
        output = args.output_dir.resolve() / f"{stem}.png"
        record = output.with_name(f"{stem}-result.json")
        prompt = (
            f"Edit only the facial expression of the woman in Picture 1 to show {expressions[name]['movement_prompt']}. "
            "Keep the same person, facial proportions, iris color, hair color and hairstyle. "
            "Keep her head facing straight forward, the same framing, shoulders, background, "
            "lighting and illustration style. Do not add text or objects."
        )
        jobs.append({"expression": name, "design": expressions[name], "prompt": prompt, "output": str(output), "record": str(record)})
    plan = {
        "model": MODEL_ID, "input": {"path": str(source), "sha256": sha256(source)},
        "size": [args.size, args.size], "steps": args.steps, "seed": args.seed,
        "true_cfg_scale": args.cfg, "negative_prompt": " ", "jobs": jobs,
        "independent_from_original": True, "extra_lora": None,
        "expression_spec": {"path": str(SPEC_PATH), "sha256": sha256(SPEC_PATH)},
    }
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return
    for job in jobs:
        if Path(job["output"]).exists() or Path(job["record"]).exists():
            parser.error(f"Output already exists; choose a new run-label: {job['output']}")

    source_code_hash = sha256(Path(__file__))

    import torch
    from PIL import Image
    from diffusers import QwenImageEditPlusPipeline

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU is not available; no model was loaded")
    with Image.open(source) as opened:
        if opened.width != opened.height:
            raise ValueError("Use a square portrait to avoid distorting the face")
        reference = opened.convert("RGB").resize((args.size, args.size), Image.Resampling.LANCZOS)
    started = time.monotonic()
    pipe = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID, torch_dtype=torch.bfloat16, cache_dir=CACHE_DIR, local_files_only=True,
    )
    pipe.enable_sequential_cpu_offload()
    pipe.vae.enable_slicing()
    load_seconds = round(time.monotonic() - started, 2)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    runtime = runtime_record()
    for job in jobs:
        print(f"Generating {job['expression']}", flush=True)
        torch.cuda.reset_peak_memory_stats()
        started = time.monotonic()
        with torch.inference_mode():
            result = pipe(
                image=[reference.copy()], prompt=job["prompt"], negative_prompt=" ",
                width=args.size, height=args.size, num_inference_steps=args.steps,
                true_cfg_scale=args.cfg, guidance_scale=1.0,
                generator=torch.Generator(device="cuda").manual_seed(args.seed),
            ).images[0]
        if result.size != (args.size, args.size):
            raise RuntimeError(f"Unexpected image dimensions: {result.size}")
        result.save(job["output"])
        record = {
            **{key: value for key, value in plan.items() if key != "jobs"},
            "status": "generated", "experiment_id": "p7-5-9-mira-expressions",
            "expression": job["expression"], "design": job["design"], "prompt": job["prompt"], "runtime": runtime,
            "gpu": torch.cuda.get_device_name(), "dtype": "bfloat16",
            "device_placement": "sequential_cpu_offload", "attention_slicing": None,
            "model_load_seconds": load_seconds,
            "elapsed_seconds": round(time.monotonic() - started, 2),
            "peak_allocated_bytes": torch.cuda.max_memory_allocated(),
            "peak_reserved_bytes": torch.cuda.max_memory_reserved(),
            "source_code_sha256": source_code_hash,
            "helper_code_sha256": sha256(ASSETS / "p7_5_2_qwen_edit_2511_generate_mira_torso.py"),
            "output": {"path": job["output"], "sha256": sha256(Path(job["output"]))},
        }
        Path(job["record"]).write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps({"expression": job["expression"], "elapsed_seconds": record["elapsed_seconds"]}), flush=True)


if __name__ == "__main__":
    main()
