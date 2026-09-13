#!/usr/bin/env python3
"""Probe real LoRA execution, then render a fixed-seed identity strength sweep."""

import argparse
import fcntl
import json
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sec-02"))
from p7_5_2_qwen_edit_2511_generate_mira_torso import (
    ROOT,
    ASSETS,
    CACHE_DIR,
    MODEL_ID,
    sha256,
    runtime_record,
)
from p7_5_11_generate_supplements import write

CHECKPOINT = (
    ROOT / ".tmp/p7-5-11/lora-v2-run100-retry1/checkpoints/mira_identity.safetensors"
)
CHECKPOINT_SHA = "d76b96198d210ef27a9d97955315e4dfec8f688044d9a832520281a10698d0f3"
PROBE_NAMES = [f"transformer_blocks.{i}.attn.to_q" for i in (0, 30, 59)]


def adapter_state(layers, scale):
    errors = []
    for name, layer in layers:
        if scale == 0:
            ok = layer.disable_adapters
        else:
            ok = (
                not layer.disable_adapters
                and not layer.merged
                and layer.active_adapters == ["mira"]
                and abs(float(layer.scaling["mira"]) - scale) < 1e-8
            )
        if not ok:
            errors.append(name)
    assert not errors, errors
    return {"checked_modules": len(layers), "scale": scale, "state_errors": errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--wait-for", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    from PIL import Image

    spec = json.loads(
        (ASSETS / "sec-11/identity-evaluation/spec.json").read_text()
    )
    case = next(x for x in spec["cases"] if x["id"] == "portrait")
    ref_path = ROOT / case["reference"]["path"]
    assert sha256(CHECKPOINT) == CHECKPOINT_SHA
    assert sha256(ref_path) == case["reference"]["sha256"]
    with Image.open(ref_path) as im:
        assert (
            im.mode == "RGB"
            and im.size == (512, 512)
            and im.getextrema() == ((240, 240),) * 3
        )
        ref = im.copy()
    plan = {
        "checkpoint": str(CHECKPOINT),
        "checkpoint_sha256": CHECKPOINT_SHA,
        "model": MODEL_ID,
        "case": case,
        "size": 512,
        "steps": 20,
        "cfg": 4.0,
        "first_step_only_scales": [0, 1],
        "render_scales": [2, 4],
        "probe_modules": PROBE_NAMES,
        "code_sha256": sha256(Path(__file__)),
        "runtime": runtime_record(),
        "note": "First-step probes keep the 20-step schedule; they are not quality samples.",
    }
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return
    out = args.output_dir.resolve()
    assert not out.exists(), f"Use a new output directory: {out}"
    (out / "images").mkdir(parents=True)
    (out / "results").mkdir()
    write(out / "plan.json", plan)
    state = {"status": "waiting" if args.wait_for else "loading", "completed": []}
    write(out / "state.json", state)
    try:
        if args.wait_for:
            with (args.wait_for / ".lock").open("r") as lock:
                fcntl.flock(lock, fcntl.LOCK_EX)
                prior = json.loads((args.wait_for / "state.json").read_text())
                assert prior["status"] == "generated_pending_visual_review", prior
        state["status"] = "loading"
        write(out / "state.json", state)
        import torch
        from diffusers import QwenImageEditPlusPipeline
        from safetensors import safe_open

        torch.set_num_threads(2)
        assert torch.cuda.is_available()
        pipe = QwenImageEditPlusPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.bfloat16,
            cache_dir=CACHE_DIR,
            local_files_only=True,
        )
        pipe.load_lora_weights(
            str(CHECKPOINT.parent),
            weight_name=CHECKPOINT.name,
            adapter_name="mira",
            local_files_only=True,
        )
        layers = [
            (n, m)
            for n, m in pipe.transformer.named_modules()
            if hasattr(m, "lora_A") and "mira" in m.lora_A
        ]
        assert len(layers) == 840
        loaded = []
        with safe_open(CHECKPOINT, framework="pt") as checkpoint:
            for name, layer in layers:
                original = "lora_unet_" + name.replace(".", "_")
                assert checkpoint.get_tensor(original + ".alpha").item() == 16
                for slot, suffix in [("lora_A", "lora_down"), ("lora_B", "lora_up")]:
                    actual = getattr(layer, slot)["mira"].weight.detach().cpu()
                    expected = checkpoint.get_tensor(
                        original + "." + suffix + ".weight"
                    ).to(actual.dtype)
                    assert torch.equal(actual, expected), (name, slot)
                    loaded.append(name + "." + slot)
        write(
            out / "results/loaded-weights.json",
            {
                "checkpoint_sha256": CHECKPOINT_SHA,
                "exact_loaded_tensors": len(loaded),
                "modules": len(layers),
                "comparison": "Exact equality after casting saved weights to loaded dtype",
            },
        )
        pipe.enable_sequential_cpu_offload()
        pipe.vae.enable_slicing()
        baseline = None
        for scale in [0, 1, 2, 4]:
            key = f"portrait-scale-{scale}"
            state.update(status="probing" if scale < 2 else "generating", current=key)
            write(out / "state.json", state)
            with torch.inference_mode():
                if scale:
                    pipe.enable_lora()
                    pipe.set_adapters("mira", adapter_weights=scale)
                else:
                    pipe.disable_lora()
            observed = {
                "adapter_state": adapter_state(layers, scale),
                "lora_branch_first_call": {},
            }
            handles = []
            for name in PROBE_NAMES:
                layer = pipe.transformer.get_submodule(name)

                def branch_hook(module, inputs, output, name=name):
                    if name not in observed["lora_branch_first_call"]:
                        v = output.detach().float()
                        observed["lora_branch_first_call"][name] = {
                            "unscaled_rms": v.square().mean().sqrt().item(),
                            "unscaled_abs_max": v.abs().max().item(),
                            "finite": bool(torch.isfinite(v).all()),
                        }

                handles.append(layer.lora_B["mira"].register_forward_hook(branch_hook))
            first = []

            def transformer_hook(module, inputs, output):
                if not first:
                    first.append(output[0].detach().float().cpu())

            handles.append(pipe.transformer.register_forward_hook(transformer_hook))

            def callback(pipeline, step, timestep, callback_kwargs):
                nonlocal baseline
                if step == 0:
                    pred = first[0]
                    if scale == 0:
                        baseline = pred.clone()
                        assert not observed["lora_branch_first_call"]
                    else:
                        assert len(observed["lora_branch_first_call"]) == len(
                            PROBE_NAMES
                        )
                        assert all(
                            v["finite"] and v["unscaled_abs_max"] > 0
                            for v in observed["lora_branch_first_call"].values()
                        )
                    delta = pred - baseline
                    observed["first_positive_prediction"] = {
                        "rms": pred.square().mean().sqrt().item(),
                        "delta_rms_vs_scale0": delta.square().mean().sqrt().item(),
                        "relative_l2_vs_scale0": (
                            delta.norm() / baseline.norm()
                        ).item(),
                    }
                    write(out / "results" / (key + "-probe.json"), observed)
                    for handle in handles:
                        handle.remove()
                    if scale < 2:
                        pipeline._interrupt = True
                return callback_kwargs

            start = time.monotonic()
            with torch.inference_mode():
                result = pipe(
                    image=[ref],
                    prompt=case["prompt"],
                    negative_prompt=" ",
                    width=512,
                    height=512,
                    num_inference_steps=20,
                    true_cfg_scale=4.0,
                    guidance_scale=1.0,
                    generator=torch.Generator(device="cuda").manual_seed(case["seed"]),
                    callback_on_step_end=callback,
                    output_type="latent" if scale < 2 else "pil",
                )
            record = {
                "scale": scale,
                "case": case,
                "plan_sha256": sha256(out / "plan.json"),
                "elapsed_seconds": round(time.monotonic() - start, 2),
                "status": (
                    "runtime_probe_complete" if scale < 2 else "pending_visual_review"
                ),
            }
            if scale >= 2:
                png = out / "images" / (key + ".png")
                result.images[0].save(png)
                record["output_sha256"] = sha256(png)
            write(out / "results" / (key + "-result.json"), record)
            state["completed"].append(key)
            write(out / "state.json", state)
        state.update(status="generated_pending_visual_review", current=None)
    except BaseException as exc:
        state.update(status="failed", error=str(exc))
        raise
    finally:
        write(out / "state.json", state)


if __name__ == "__main__":
    main()
