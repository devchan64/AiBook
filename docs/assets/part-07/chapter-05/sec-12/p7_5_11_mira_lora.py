#!/usr/bin/env python3
"""검수 목록을 학습 쌍으로 준비하고 고정 Musubi 버전으로 LoRA를 학습한다.

읽는 순서: validate → prepare → commands → run.
조작: JSON의 steps·save_every 또는 참조 구성을 바꾸어 새 패키지를 만든다.
관찰: train/validation 분할, 명령 계획, 체크포인트와 별도 평가 이미지를 본다.
run은 기본적으로 계획만 출력한다. --execute를 지정해야 캐시·학습을 실행한다.
가중치 다운로드는 tool/model_weight_manager.py에서 별도로 수행한다.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
from p7_5_12_asset_paths import asset_path
import time

ROOT = Path(__file__).resolve().parents[5]
PIN = "e0cbd8f3dfe38365b10f8bc790b980f8894e8ba1"
MODEL = "Qwen/Qwen-Image-Edit-2511"
CONFIG = Path(__file__).parent / "p7-5-12-bfs-lora-config.json"


def sha(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, value):
    Path(path).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local(path):
    return asset_path(path)


def weight_path(path):
    # 확장자가 없는 HF blob으로 바꾸지 않고 파일명으로 가중치 형식을 확인한다.
    p = Path(path)
    return ROOT / p if not p.is_absolute() else p


def inventory(output):
    """현재 원고에 실린 이미지에서 후보를 수집하며 학습 채택은 자동 결정하지 않는다."""
    require(not output.exists(), f"Output already exists: {output}")
    rows, seen = [], set()
    for section in (2, 9):
        manuscript = ROOT / f"docs/parts/part-07/chapter-05/section-{section:02}.md"
        for label, url in re.findall(
            r"!\[([^\]]*)\]\(([^)]+)\)", manuscript.read_text()
        ):
            image = (manuscript.parent / url).resolve()
            require(
                image.is_relative_to(ROOT / "docs/assets"), f"Not a local asset: {url}"
            )
            digest = sha(image)
            if digest in seen:
                continue
            seen.add(digest)
            record = image.with_name(image.stem + "-result.json")
            require(record.is_file(), f"Missing generation record: {record}")
            data = read(record)
            design = data.get("design", {})
            # 그룹과 캡션은 검수자가 확정한다. 후보 수집은 학습 승인 단계가 아니다.
            group = design.get("family") or (
                "camera" if "yaw-" in image.name else "reference"
            )
            rows.append(
                {
                    "id": image.stem,
                    "source_section": f"P7-5.{section}",
                    "image": str(image.relative_to(ROOT)),
                    "sha256": digest,
                    "record": str(record.relative_to(ROOT)),
                    "record_sha256": sha(record),
                    "label": label,
                    "group": group,
                    "split": "pending",
                    "caption": "",
                    "review_note": "",
                }
            )
    output.parent.mkdir(parents=True, exist_ok=True)
    write(
        output,
        {
            "schema_version": 1,
            "model_id": MODEL,
            "trigger": "mira_person",
            "items": rows,
        },
    )
    return {
        "status": "candidate_inventory",
        "count": len(rows),
        "manifest": str(output),
    }


def diagnostic_control(manifest):
    """단색 참조에 외형 정보가 없는지 해시와 픽셀로 확인한다."""
    from PIL import Image

    ref = manifest["neutral_control"]
    path = local(ref["path"])
    require(
        path.is_relative_to(ROOT / "docs/assets"), "Diagnostic control outside assets"
    )
    require(sha(path) == ref["sha256"], "Diagnostic control hash mismatch")
    with Image.open(path) as image:
        require(
            image.mode == "RGB"
            and image.size == (512, 512)
            and image.getextrema() == ((240, 240),) * 3,
            "Diagnostic control must be uniform RGB 240 without identity information",
        )
    return path


def validate(manifest):
    """분할 누수·중복·해시 변경을 검사하며 인물 유사도는 판정하지 않는다."""
    require(manifest.get("model_id") == MODEL, "Expected Edit-2511 manifest")
    require(manifest.get("schema_version") == 1, "Unsupported manifest schema")
    trigger = manifest.get("trigger", "")
    require(trigger and isinstance(trigger, str), "Missing trigger")
    paired = manifest.get("purpose") == "paired_edit_training"
    ids, hashes, groups, target_splits = set(), set(), {}, {}
    selected = {"train": [], "validation": []}
    for item in manifest["items"]:
        key = item["id"]
        require(re.fullmatch(r"[A-Za-z0-9_-]+", key), f"Unsafe id: {key}")
        require(key not in ids, f"Duplicate id: {key}")
        ids.add(key)
        split = item["split"]
        require(
            split in ("pending", "exclude", "train", "validation"),
            f"Invalid split: {key}",
        )
        if split not in selected:
            continue
        require(item.get("review_note", "").strip(), f"Review note required: {key}")
        caption = item.get("caption", "").strip()
        require(
            trigger in caption and "\n" not in caption,
            f"Single-line caption with trigger required: {key}",
        )
        require(item.get("group", "").strip(), f"Group required: {key}")
        group = item["group"]
        require(groups.setdefault(group, split) == split, f"Group leakage: {group}")
        image, record = local(item["image"]), local(item["record"])
        require(
            image.is_relative_to(ROOT / "docs/assets"), f"Image outside assets: {key}"
        )
        require(
            record.is_relative_to(ROOT / "docs/assets"), f"Record outside assets: {key}"
        )
        require(sha(image) == item["sha256"], f"Image changed: {key}")
        require(
            sha(record) == item["record_sha256"], f"Generation record changed: {key}"
        )
        # 편집 쌍의 생성 기록은 Mira 목표가 아니라 생성된 입력을 가리킨다.
        content_hash = item["control_sha256"] if paired else item["sha256"]
        if paired:
            control = local(item["control_image"])
            require(
                control.is_relative_to(ROOT / "docs/assets"),
                f"Input outside assets: {key}",
            )
            require(sha(control) == content_hash, f"Input changed: {key}")
            require(
                content_hash != item["sha256"], f"Identical input and target: {key}"
            )
            require(
                target_splits.setdefault(item["sha256"], split) == split,
                f"Target leakage: {key}",
            )
        require(
            read(record).get("output", {}).get("sha256") == content_hash,
            f"Record/image mismatch: {key}",
        )
        require(content_hash not in hashes, f"Duplicate image content: {key}")
        hashes.add(content_hash)
        selected[split].append(item)
    purpose = manifest.get("purpose", "identity_training")
    require(
        purpose
        in (
            "identity_training",
            "single_image_memorization",
            "neutral_control_ablation",
            "paired_edit_training",
        ),
        "Unknown experiment purpose",
    )
    if purpose == "single_image_memorization":
        require(
            len(selected["train"]) == 1 and not selected["validation"],
            "Diagnostic requires exactly one train image and no held-out validation",
        )
        diagnostic_control(manifest)
    else:
        require(
            len(selected["train"]) >= 2, "Select at least two reviewed train images"
        )
        require(selected["validation"], "Select at least one held-out validation image")
        if purpose == "neutral_control_ablation":
            diagnostic_control(manifest)
    return selected


def settings(config):
    """실행 가능한 설정인지 검사한다. 이 값이 최적 학습량이라는 뜻은 아니다."""
    require(
        config["model_id"] == MODEL and config["trainer_commit"] == PIN,
        "Model or trainer pin mismatch",
    )
    t = config["training"]
    for key in ("save_state", "save_state_on_train_end"):
        require(type(t.get(key, False)) is bool, f"Boolean required: {key}")
    for key in (
        "resolution",
        "control_resolution",
        "rank",
        "alpha",
        "steps",
        "save_every",
    ):
        require(type(t[key]) is int and t[key] > 0, f"Positive integer required: {key}")
    require(
        t["resolution"] % 32 == 0 and t["control_resolution"] % 32 == 0,
        "Resolutions must be multiples of 32",
    )
    require(
        type(t["blocks_to_swap"]) is int and 0 <= t["blocks_to_swap"] <= 59,
        "blocks_to_swap must be 0..59",
    )
    require(
        math.isfinite(t["learning_rate"]) and t["learning_rate"] > 0,
        "Invalid learning rate",
    )
    require(type(t["seed"]) is int and t["seed"] >= 0, "Invalid seed")
    for key in ("fp8_base", "fp8_scaled", "fp8_vl"):
        require(type(t[key]) is bool, f"Boolean required: {key}")
    require(not t["fp8_scaled"] or t["fp8_base"], "fp8_scaled requires fp8_base")
    require(
        t.get("text_encoder_device", "cuda") in ("cpu", "cuda"),
        "Invalid text encoder device",
    )
    require(
        t.get("text_encoder_device", "cuda") != "cpu" or not t["fp8_vl"],
        "CPU text caching requires BF16, not fp8_vl",
    )
    return t


def state_files(state):
    """단일 프로세스 재개 상태의 누락을 검사하고 파일 해시를 고정한다."""
    require(state.is_dir(), f"Missing training state directory: {state}")
    names = {p.name for p in state.iterdir() if p.is_file()}
    require(
        {"optimizer.bin", "scheduler.bin", "random_states_0.pkl"} <= names
        and bool({"model.safetensors", "pytorch_model.bin"} & names),
        f"Incomplete training state: {state}",
    )
    return {
        str(p.relative_to(state)): sha(p)
        for p in sorted(state.rglob("*"))
        if p.is_file()
    }


def prepare_resume(source, state, additional_steps, output):
    """원래 자료·설정을 계승하고 추가 스텝만 바꾼 별도 패키지를 만든다."""
    check_package(source)
    require(
        type(additional_steps) is int and additional_steps > 0,
        "Positive additional steps required",
    )
    config = read(source / "config.json")
    require(
        state.parent == source / "checkpoints",
        "State must belong to source package checkpoints",
    )
    match = re.fullmatch(r"mira_(?:bfs|identity)-step(\d+)-state", state.name)
    if match:
        completed = int(match[1])
        require(0 < completed <= config["training"]["steps"], "Invalid saved step")
    else:
        require(
            state.name in ("mira_bfs-state", "mira_identity-state"),
            "Unknown state name",
        )
        require(
            read(source / "run-result.json")["status"] == "trained_not_evaluated",
            "Final state requires completed training",
        )
        completed = config["training"]["steps"]
    files = state_files(state)
    cumulative = config.get("resume", {}).get("previous_steps", 0) + completed
    config["resume"] = {
        "state": str(state),
        "files": files,
        "source_package": str(source),
        "source_package_sha256": sha(source / "package.json"),
        "previous_steps": cumulative,
    }
    config["training"].update(
        steps=additional_steps, save_state=True, save_state_on_train_end=True
    )
    # 元パッケージは変更せず、キャッシュ・出力も新しい場所に作る。
    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp) / "config.json"
        write(path, config)
        result = prepare(source / "manifest.json", path, output)
    return {
        **result,
        "previous_steps": cumulative,
        "additional_steps": additional_steps,
        "planned_total_steps": cumulative + additional_steps,
    }


def prepare(manifest_path, config_path, output):
    """선정 목록과 설정을 고정한 새 학습 패키지를 만든다."""
    manifest, config = read(manifest_path), read(config_path)
    selected, t = validate(manifest), settings(config)
    require(not output.exists(), f"Output already exists: {output}")
    paired = manifest.get("purpose") == "paired_edit_training"
    aliases = {}
    if paired:
        # 학습기는 목표 파일명으로 캐시를 구분하므로 쌍마다 별도 이름을 부여한다.
        (output / "paired-targets").mkdir(parents=True)
    train = sorted(selected["train"], key=lambda x: x["id"])
    # A는 다른 Mira 이미지, B·1장 진단은 외형 정보가 없는 단색을 조건으로 삼는다.
    neutral = (
        diagnostic_control(manifest)
        if manifest.get("purpose")
        in ("single_image_memorization", "neutral_control_ablation")
        else None
    )
    pairs = {"train": [], "validation": []}
    for split in pairs:
        for i, target in enumerate(sorted(selected[split], key=lambda x: x["id"])):
            # 검증 목표가 학습 참조로 유입되지 않도록 참조는 학습 분할에서만 고른다.
            choices = [x for x in train if x["sha256"] != target["sha256"]]
            image_path = local(target["image"])
            if paired:
                control_path = local(target["control_image"])
                name = f"paired-targets/{target['id']}{image_path.suffix}"
                (output / name).symlink_to(image_path)
                image_path = output / name
                aliases[name] = target["sha256"]
            else:
                control_path = (
                    neutral if neutral else local(choices[i % len(choices)]["image"])
                )
            pairs[split].append(
                {
                    "image_path": str(image_path),
                    "control_path": str(control_path),
                    "caption": target["caption"],
                }
            )
    output.mkdir(parents=True, exist_ok=paired)
    for split, rows in pairs.items():
        (output / f"{split}.jsonl").write_text(
            "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows)
        )
    # 검증 이미지는 품질 비교용이며 실제 학습 TOML에는 train.jsonl만 연결한다.
    toml = (
        "[general]\n" + f"resolution = [{t['resolution']}, {t['resolution']}]\n"
        "batch_size = 1\nenable_bucket = true\nbucket_no_upscale = true\n\n[[datasets]]\n"
        f"image_jsonl_file = {json.dumps(str(output / 'train.jsonl'))}\n"
        f"cache_directory = {json.dumps(str(output / 'cache'))}\n"
        f"control_resolution = [{t['control_resolution']}, {t['control_resolution']}]\nnum_repeats = 1\n"
    )
    (output / "dataset.toml").write_text(toml)
    write(output / "manifest.json", manifest)
    write(output / "config.json", config)
    lock = {
        "status": "prepared_not_trained",
        "trainer_commit": PIN,
        "counts": {k: len(v) for k, v in pairs.items()},
        "files": {
            n: sha(output / n)
            for n in (
                "train.jsonl",
                "validation.jsonl",
                "dataset.toml",
                "manifest.json",
                "config.json",
            )
        },
    }
    lock["files"].update(aliases)
    write(output / "package.json", lock)
    return lock


def commands(package, trainer, python):
    """잠재표현 캐시 → 조건 임베딩 캐시 → 학습의 실행 명령을 구성한다."""
    c = read(package / "config.json")
    t = settings(c)
    model_paths = {
        k: str(weight_path(v["path"])) if v["path"] else f"<{k.upper()}_SAFETENSORS>"
        for k, v in c["weights"].items()
    }
    common = [
        "--dataset_config",
        str(package / "dataset.toml"),
        "--model_version",
        "edit-2511",
    ]
    script = lambda n: str(trainer / "src/musubi_tuner" / n)
    latent = [
        str(python),
        script("qwen_image_cache_latents.py"),
        *common,
        "--vae",
        model_paths["vae"],
        "--batch_size",
        "1",
        "--num_workers",
        "1",
    ]
    text = [
        str(python),
        script("qwen_image_cache_text_encoder_outputs.py"),
        *common,
        "--text_encoder",
        model_paths["text_encoder"],
        "--batch_size",
        "1",
        "--num_workers",
        "1",
    ]
    text.extend(["--device", t.get("text_encoder_device", "cuda")])
    if t["fp8_vl"]:
        text.append("--fp8_vl")
    train = [
        str(python),
        "-m",
        "accelerate.commands.launch",
        "--num_processes",
        "1",
        "--num_machines",
        "1",
        "--mixed_precision",
        "bf16",
        "--num_cpu_threads_per_process",
        "1",
        script("qwen_image_train_network.py"),
        *common,
        "--dit",
        model_paths["dit"],
        "--vae",
        model_paths["vae"],
        "--text_encoder",
        model_paths["text_encoder"],
        "--sdpa",
        "--mixed_precision",
        "bf16",
        "--timestep_sampling",
        "shift",
        "--discrete_flow_shift",
        "2.2",
        "--weighting_scheme",
        "none",
        "--optimizer_type",
        "adamw8bit",
        "--learning_rate",
        str(t["learning_rate"]),
        "--gradient_checkpointing",
        "--max_data_loader_n_workers",
        "0",
        "--network_module",
        "networks.lora_qwen_image",
        "--network_dim",
        str(t["rank"]),
        "--network_alpha",
        str(t["alpha"]),
        "--max_train_steps",
        str(t["steps"]),
        "--save_every_n_steps",
        str(min(t["save_every"], t["steps"])),
        "--seed",
        str(t["seed"]),
        "--blocks_to_swap",
        str(t["blocks_to_swap"]),
        "--output_dir",
        str(package / "checkpoints"),
        "--output_name",
        "mira_bfs"
        if read(package / "manifest.json").get("purpose") == "paired_edit_training"
        else "mira_identity",
    ]
    for key in ("fp8_base", "fp8_scaled", "fp8_vl"):
        if t[key]:
            train.append("--" + key)
    for key in ("save_state", "save_state_on_train_end"):
        if t.get(key, False):
            train.append("--" + key)
    if c.get("resume"):
        train.extend(["--resume", c["resume"]["state"]])
    return [("cache_latents", latent), ("cache_text", text), ("train", train)]


def check_package(package):
    lock = read(package / "package.json")
    for name, digest in lock["files"].items():
        require(
            sha(package / name) == digest,
            f"Prepared file changed: {name}; create a new package",
        )
    validate(read(package / "manifest.json"))
    require(lock["trainer_commit"] == PIN, "Package trainer mismatch")
    resume = read(package / "config.json").get("resume")
    if resume:
        require(
            sha(Path(resume["source_package"]) / "package.json")
            == resume["source_package_sha256"],
            "Source package changed",
        )
        require(
            state_files(Path(resume["state"])) == resume["files"],
            "Training state changed",
        )


def run(package, trainer, python, execute):
    """계획을 확인한 뒤 명시적으로 요청한 경우에만 GPU 학습을 실행한다."""
    check_package(package)
    plan = commands(package, trainer, python)
    if not execute:
        return {
            "status": "plan_only",
            "commands": {k: shlex.join(v) for k, v in plan},
            "note": "No model or GPU loaded; local weights/environment still require preflight.",
        }
    require(python.is_file(), f"Missing trainer Python: {python}")
    revision = subprocess.check_output(
        ["git", "-C", str(trainer), "rev-parse", "HEAD"], text=True
    ).strip()
    require(revision == PIN, f"Expected Musubi commit {PIN}, got {revision}")
    require(
        not subprocess.check_output(
            [
                "git",
                "-C",
                str(trainer),
                "status",
                "--porcelain",
                "--untracked-files=no",
            ],
            text=True,
        ).strip(),
        "Trainer tracked files are modified",
    )
    config = read(package / "config.json")
    for role in ("dit", "vae", "text_encoder"):
        w = config["weights"][role]
        require(
            w["path"] and w["sha256"] and w["repo_id"] and w["revision"],
            f"Configure path/hash/source revision for {role}",
        )
        path = weight_path(w["path"])
        require(
            path.suffix == ".safetensors" and path.is_file(),
            f"Expected local safetensors file: {path}",
        )
        require(
            not re.search(r"-\d+-of-\d+", path.name),
            "Use a complete single-file checkpoint, not one shard",
        )
        require(sha(path) == w["sha256"], f"Weight checksum mismatch: {role}")
    # 가중치·토크나이저는 .tmp/download에 사전 준비하고 학습 중 다운로드하지 않는다.
    env = os.environ.copy()
    env.update(
        {
            "HF_HUB_OFFLINE": "1",
            "TRANSFORMERS_OFFLINE": "1",
            "HF_HOME": str(ROOT / ".tmp/download/huggingface"),
            "HF_HUB_CACHE": str(ROOT / ".tmp/download/huggingface/hub"),
            "PYTHONUNBUFFERED": "1",
            "PYTHONPATH": str(trainer / "src"),
            "TOKENIZERS_PARALLELISM": "false",
        }
    )
    for name in ("cache", "checkpoints", "logs", "run-result.json"):
        require(
            not (package / name).exists(),
            f"Existing run artifact: {name}; prepare a new package",
        )
    subprocess.run(
        [
            str(python),
            "-c",
            'import torch, accelerate, bitsandbytes; assert torch.cuda.is_available(), "CUDA required"; assert torch.cuda.is_bf16_supported(), "BF16 required"',
        ],
        check=True,
        env=env,
        cwd=trainer,
    )
    subprocess.run(
        [
            str(python),
            "-c",
            "from transformers import Qwen2Tokenizer, Qwen2VLProcessor; "
            'Qwen2Tokenizer.from_pretrained("Qwen/Qwen-Image", subfolder="tokenizer", local_files_only=True); '
            'Qwen2VLProcessor.from_pretrained("Qwen/Qwen-Image-Edit", subfolder="processor", local_files_only=True)',
        ],
        check=True,
        env=env,
        cwd=trainer,
    )
    # 고정한 학습기의 옵션 지원을 모델 로드 전에 확인한다.
    for _, cmd in plan:
        entry = next(x for x in cmd if x.endswith(".py"))
        help_text = subprocess.check_output(
            [str(python), entry, "--help"], text=True, env=env, cwd=trainer
        )
        for flag in cmd[cmd.index(entry) + 1 :]:
            if flag.startswith("--"):
                require(flag in help_text, f"Unsupported option: {flag}")
    (package / "logs").mkdir()
    result = {
        "status": "running",
        "trainer_commit": revision,
        "wrapper_sha256": sha(__file__),
        "package_sha256": sha(package / "package.json"),
        "steps": [],
        "previous_training_steps": config.get("resume", {}).get("previous_steps", 0),
        "requested_training_steps": config["training"]["steps"],
    }
    write(package / "run-result.json", result)
    try:
        for stage, cmd in plan:
            started = time.time()
            print(
                f"Running {stage}; log: {package / 'logs' / (stage + '.log')}",
                flush=True,
            )
            with (package / "logs" / (stage + ".log")).open("w") as log:
                proc = subprocess.run(
                    cmd, cwd=trainer, env=env, stdout=log, stderr=subprocess.STDOUT
                )
            result["steps"].append(
                {
                    "stage": stage,
                    "command": cmd,
                    "returncode": proc.returncode,
                    "elapsed_seconds": round(time.time() - started, 2),
                }
            )
            write(package / "run-result.json", result)
            require(proc.returncode == 0, f"{stage} failed: inspect its log")
        checkpoints = sorted((package / "checkpoints").glob("*.safetensors"))
        require(checkpoints, "Trainer exited without a LoRA checkpoint")
        if config["training"].get("save_state") or config["training"].get(
            "save_state_on_train_end"
        ):
            output_name = (
                "mira_bfs"
                if read(package / "manifest.json").get("purpose")
                == "paired_edit_training"
                else "mira_identity"
            )
            final_state = package / "checkpoints" / f"{output_name}-state"
            result["final_training_state"] = {
                "path": str(final_state),
                "files": state_files(final_state),
            }
        result.update(
            status="trained_not_evaluated",
            checkpoints=[{"path": str(p), "sha256": sha(p)} for p in checkpoints],
            cumulative_training_steps=result["previous_training_steps"]
            + config["training"]["steps"],
        )
    except BaseException as error:
        result.update(status="failed", error=str(error))
        raise
    finally:
        write(package / "run-result.json", result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    p = sub.add_parser("inventory")
    p.add_argument(
        "--output", type=Path, default=ROOT / ".tmp/p7-5-11/mira-candidates.json"
    )
    p = sub.add_parser("prepare")
    p.add_argument(
        "--manifest",
        type=Path,
        required=True,
        help="split·caption·참조 구성이 검수된 JSON 목록",
    )
    p.add_argument(
        "--config",
        type=Path,
        default=CONFIG,
        help="steps·save_every·학습률·가중치 경로를 담은 JSON",
    )
    p.add_argument("--output", type=Path, required=True)
    p = sub.add_parser("prepare-resume", help="저장 상태를 이어 학습할 새 패키지 준비")
    p.add_argument("--source-package", type=Path, required=True)
    p.add_argument("--state", type=Path, required=True)
    p.add_argument("--additional-steps", type=int, required=True)
    p.add_argument("--output", type=Path, required=True)
    p = sub.add_parser("run")
    p.add_argument("--package", type=Path, required=True)
    p.add_argument("--trainer", type=Path, required=True)
    p.add_argument(
        "--python",
        type=Path,
        required=True,
        help="Python executable in the separate Musubi environment",
    )
    p.add_argument(
        "--execute",
        action="store_true",
        help="Run GPU caching and training; default prints plan only",
    )
    args = parser.parse_args()
    try:
        if args.action == "inventory":
            result = inventory(args.output.resolve())
        elif args.action == "prepare":
            result = prepare(args.manifest, args.config, args.output.resolve())
        elif args.action == "prepare-resume":
            result = prepare_resume(
                args.source_package.resolve(),
                args.state.resolve(),
                args.additional_steps,
                args.output.resolve(),
            )
        else:
            result = run(
                args.package.resolve(),
                args.trainer.resolve(),
                args.python.absolute(),
                args.execute,
            )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        parser.exit(2, f"Error: {error}\n")


if __name__ == "__main__":
    main()
