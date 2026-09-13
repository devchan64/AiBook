#!/usr/bin/env python3
"""Generate and collect a matched A/B by checkpoint-step comparison."""

import argparse
import fcntl
import json
import shutil
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sec-02"))
from p7_5_2_qwen_edit_2511_generate_mira_torso import ROOT, ASSETS, sha256
from p7_5_11_generate_supplements import write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--plan",
        type=Path,
        default=ASSETS / "sec-11/p7-5-11-checkpoint-matrix-plan.json",
    )
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text())
    if not args.execute:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return
    run = ROOT / ".tmp/p7-5-11/checkpoint-matrix"
    published = ASSETS / "sec-11/checkpoint-matrix-evaluation"
    for folder in ("images", "results"):
        (published / folder).mkdir(parents=True, exist_ok=True)
    entries = []
    state = {"status": "preflight", "completed_images": 0, "expected_images": 18}

    def copy_checked(src, dst):
        if dst.exists():
            assert sha256(src) == sha256(dst), f"Conflicting published artifact: {dst}"
        else:
            shutil.copy2(src, dst)

    def collect(job, name, source, origin):
        p = json.loads((source / "plan.json").read_text())
        for key in ("model", "size", "steps", "cfg", "scales"):
            assert p[key] == plan["conditions"][key], key
        assert p["checkpoint_sha256"] == job["checkpoint_sha256"]
        case = next(c for c in plan["conditions"]["cases"] if c["id"] == name)
        assert case in p["cases"]
        record = source / f"{name}-lora-result.json"
        data = json.loads(record.read_text())
        png = source / f"{name}-lora.png"
        assert data["case"] == case and data["scale"] == 1
        assert data["checkpoint_sha256"] == job["checkpoint_sha256"]
        assert data["plan_sha256"] == sha256(source / "plan.json")
        assert data["output_sha256"] == sha256(png)
        key = f"{job['arm']}-{job['training_steps']}-{name}"
        assert not any(e["id"] == key for e in entries)
        copy_checked(png, published / "images" / f"{key}.png")
        copy_checked(record, published / "results" / f"{key}-result.json")
        copy_checked(source / "plan.json", published / "results" / f"{key}-plan.json")
        entries.append(
            {
                "id": key,
                "arm": job["arm"],
                "training_steps": job["training_steps"],
                "case": name,
                "origin": origin,
                "source_directory": str(source),
                "image": f"images/{key}.png",
                "output_sha256": data["output_sha256"],
                "checkpoint_sha256": job["checkpoint_sha256"],
                "review": "pending",
            }
        )
        state["completed_images"] = len(entries)
        write(
            published / "results/index.json",
            {"status": "pending_visual_review", "items": entries},
        )
        write(run / "state.json", state)

    with (run / ".lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            copy_checked(args.plan, published / "results/matrix-plan.json")
            copy_checked(Path(__file__), published / "results/runner-source.py.txt")
            for job in plan["jobs"]:
                assert sha256(Path(job["checkpoint"])) == job["checkpoint_sha256"]
                for reuse in job["reuse"]:
                    collect(job, reuse["case"], Path(reuse["directory"]), "reused")
            for job in plan["jobs"]:
                if not job["generate_cases"]:
                    continue
                command = [
                    sys.executable,
                    str(ASSETS / "sec-11/p7_5_11_evaluate_lora.py"),
                    "--output-dir",
                    job["output"],
                    "--checkpoint",
                    job["checkpoint"],
                    "--checkpoint-sha256",
                    job["checkpoint_sha256"],
                    "--scales",
                    "1",
                ]
                for name in job["generate_cases"]:
                    command += ["--case", name]
                actual = json.loads(
                    subprocess.check_output(
                        command + ["--dry-run"], cwd=ROOT, text=True
                    )
                )
                for key in ("model", "size", "steps", "cfg", "scales"):
                    assert actual[key] == plan["conditions"][key], key
                assert actual["cases"] == [
                    c
                    for c in plan["conditions"]["cases"]
                    if c["id"] in job["generate_cases"]
                ]
                state.update(
                    status="generating",
                    arm=job["arm"],
                    training_steps=job["training_steps"],
                    current_output=job["output"],
                    command=command,
                )
                write(run / "state.json", state)
                with (run / f"{job['arm']}-{job['training_steps']}.log").open(
                    "a"
                ) as log:
                    subprocess.run(
                        command,
                        cwd=ROOT,
                        stdout=log,
                        stderr=subprocess.STDOUT,
                        check=True,
                    )
                for name in job["generate_cases"]:
                    collect(job, name, Path(job["output"]), "generated")
            assert len(entries) == plan["expected_images"] == 18
            state.update(status="generated_pending_visual_review", current_output=None)
        except BaseException as error:
            state.update(status="failed", error=repr(error))
            raise
        finally:
            write(run / "state.json", state)


if __name__ == "__main__":
    main()
