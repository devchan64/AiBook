"""Run the Part 7 local-LLM comparison and write a reproducible CSV snapshot."""

import argparse
import csv
import gc
import os
import subprocess
import sys
import time
from pathlib import Path

import psutil
import torch
from huggingface_hub import snapshot_download
from transformers import AutoModelForCausalLM, AutoTokenizer


MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
HF_HUB_CACHE = Path(__file__).resolve().parents[3] / ".tmp" / "download" / "huggingface" / "hub"
INPUT_PATH = Path("docs/assets/part-07/chapter-06/p7-6-1-prompts.csv")
OUTPUT_PATH = Path("docs/assets/part-07/chapter-06/p7-6-1-local-llm-results.csv")
MAX_NEW_TOKENS = 16

FACTS = {
    "baseline_owner": "Baseline owner: Mina.",
    "fixed_seed": "Fixed seed: 42.",
    "next_action": "Next action: inspect the error sample.",
}


def build_context(fact_key, context_condition):
    fact = FACTS[fact_key]
    if context_condition == "short":
        return f"Project record. {fact}"

    filler = " ".join(
        [
            "This note preserves scope, input, baseline, and review fields."
            for _ in range(24)
        ]
    )
    return f"Project record. {fact} {filler} Keep the recorded facts unchanged."


def load_model(model_path, quantization_mode):
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        local_files_only=True,
        dtype=torch.float32,
    )
    model.eval()
    if quantization_mode == "dynamic-int8-linear":
        model = torch.ao.quantization.quantize_dynamic(
            model,
            {torch.nn.Linear},
            dtype=torch.qint8,
        )
    return model


def answer_for(model, tokenizer, row):
    messages = [
        {
            "role": "system",
            "content": "Answer only with the requested recorded fact. Do not explain.",
        },
        {
            "role": "user",
            "content": f"{build_context(row['fact_key'], row['context_condition'])} {row['user_request']}",
        },
    ]
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )
    inputs = tokenizer([prompt], return_tensors="pt")
    started = time.perf_counter()
    with torch.inference_mode():
        output = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    elapsed_ms = round((time.perf_counter() - started) * 1000, 1)
    answer = tokenizer.batch_decode(
        output[:, inputs.input_ids.shape[1] :],
        skip_special_tokens=True,
    )[0].strip()
    return inputs.input_ids.shape[1], elapsed_ms, answer


def run_one_mode(quantization_mode, output_path):
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    torch.set_num_threads(4)
    model_path = Path(snapshot_download(MODEL_ID, cache_dir=HF_HUB_CACHE, local_files_only=True))
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    cases = list(csv.DictReader(INPUT_PATH.open(encoding="utf-8")))
    process = psutil.Process()
    rows = []

    gc.collect()
    model = load_model(model_path, quantization_mode)
    memory_after_load_mb = round(process.memory_info().rss / 1024**2, 1)

    for case in cases:
        input_tokens, elapsed_ms, answer = answer_for(model, tokenizer, case)
        expected_answer = case["expected_answer"]
        rows.append(
            {
                "run_id": f"p7-6-1-{quantization_mode}-{case['case_id']}",
                "run_date": "2026-08-01",
                "log_source": "actual_cpu_run",
                "model_name": MODEL_ID,
                "quantization_mode": quantization_mode,
                "device": "cpu",
                "torch_version": torch.__version__,
                "context_condition": case["context_condition"],
                "case_id": case["case_id"],
                "input_tokens": input_tokens,
                "max_new_tokens": MAX_NEW_TOKENS,
                "elapsed_ms": elapsed_ms,
                "memory_after_load_mb": memory_after_load_mb,
                "expected_answer": expected_answer,
                "answer": answer,
                "expected_answer_seen": str(expected_answer.lower() in answer.lower()).lower(),
            }
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    success_count = sum(row["expected_answer_seen"] == "true" for row in rows)
    mean_elapsed = sum(float(row["elapsed_ms"]) for row in rows) / len(rows)
    print(f"{quantization_mode}: expected fact {success_count}/{len(rows)}, mean {mean_elapsed:.1f} ms")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("all", "fp32", "dynamic-int8-linear"),
        default="all",
    )
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()

    if args.mode != "all":
        run_one_mode(args.mode, args.output)
        return

    partial_paths = []
    for mode in ("fp32", "dynamic-int8-linear"):
        partial_path = args.output.with_suffix(f".{mode}.csv")
        subprocess.run(
            [
                sys.executable,
                __file__,
                "--mode",
                mode,
                "--output",
                str(partial_path),
            ],
            check=True,
            env={**os.environ, "HF_HUB_OFFLINE": "1"},
        )
        partial_paths.append(partial_path)

    rows = []
    for partial_path in partial_paths:
        rows.extend(csv.DictReader(partial_path.open(encoding="utf-8")))
        partial_path.unlink()

    with args.output.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} actual model runs to {args.output}")


if __name__ == "__main__":
    main()
