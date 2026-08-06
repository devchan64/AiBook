from __future__ import annotations

import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
MPL_CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))
os.environ.setdefault("XDG_CACHE_HOME", str(MPL_CACHE))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT_DIR))
from p7_4_training_curves import run_training  # noqa: E402

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
OUT_PATH = OUT_DIR / "p7-4-1-learning-curves-en.svg"


def add_accessible_text(path: Path) -> None:
    tree = ET.parse(path)
    root = tree.getroot()
    root.set("role", "img")
    root.set("aria-labelledby", "title desc")
    title = ET.Element(f"{{{SVG_NS}}}title", {"id": "title"})
    title.text = "Support-routing learning record"
    desc = ET.Element(f"{{{SVG_NS}}}desc", {"id": "desc"})
    desc.text = "Training and evaluation loss fall across twelve epochs. Evaluation accuracy stays at 0.857 above the 0.714 baseline."
    root.insert(0, desc)
    root.insert(0, title)
    tree.write(path, encoding="utf-8", xml_declaration=False)


def main() -> None:
    logs = run_training()
    epochs = [row["epoch"] for row in logs]
    fig, (loss_ax, accuracy_ax) = plt.subplots(1, 2, figsize=(11.8, 4.5), constrained_layout=True)
    loss_ax.plot(epochs, [row["train_loss"] for row in logs], marker="o", linewidth=2.2, color="#0f766e", label="Training loss")
    loss_ax.plot(epochs, [row["eval_loss"] for row in logs], marker="o", linewidth=2.2, color="#ea580c", label="Evaluation loss")
    loss_ax.set(title="Loss curves", xlabel="Epoch", ylabel="Loss", xticks=epochs)
    loss_ax.grid(alpha=0.22)
    loss_ax.legend(frameon=False)
    accuracy_ax.plot(epochs, [row["eval_accuracy"] for row in logs], marker="o", linewidth=2.2, color="#2563eb", label="Evaluation accuracy")
    accuracy_ax.plot(epochs, [row["baseline_accuracy"] for row in logs], linestyle="--", linewidth=1.8, color="#64748b", label="Baseline accuracy")
    accuracy_ax.set(title="Accuracy and baseline", xlabel="Epoch", ylabel="Accuracy", xticks=epochs, ylim=(0.68, 1.04))
    accuracy_ax.grid(alpha=0.22)
    accuracy_ax.legend(frameon=False, loc="lower right")
    accuracy_ax.annotate("Accuracy changes after\nearly perfect predictions", xy=(8, logs[7]["eval_accuracy"]), xytext=(4.4, 1.0), arrowprops={"arrowstyle": "->", "color": "#1f2937"})
    fig.suptitle(f"Support-routing learning record\nFinal evaluation accuracy {logs[-1]['eval_accuracy']:.3f}; evaluation loss {logs[0]['eval_loss']:.3f} → {logs[-1]['eval_loss']:.3f}", fontweight="bold")
    fig.savefig(OUT_PATH, format="svg", dpi=160, bbox_inches="tight")
    plt.close(fig)
    add_accessible_text(OUT_PATH)


if __name__ == "__main__":
    main()
