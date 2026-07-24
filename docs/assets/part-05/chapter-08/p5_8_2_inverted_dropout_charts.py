from csv import DictReader
from pathlib import Path
import os

REPO_ROOT = Path(__file__).resolve().parents[4]
MPL_CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))
os.environ.setdefault("XDG_CACHE_HOME", str(MPL_CACHE))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np


OUT_DIR = Path(__file__).resolve().parent
CSV_PATH = OUT_DIR / "dropout-training-path-log.csv"
KEEP_PROBABILITY = 0.8

LANG_TEXT = {
    "ko": {
        "font_candidates": [
            "Noto Sans CJK KR",
            "NanumGothic",
            "Apple SD Gothic Neo",
            "AppleGothic",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "dropout-inverted-scaling-sum-ko.png",
        "title": "inverted dropout scaling 전후 활성값 합",
        "step_label": "학습 step",
        "sum_label": "활성값 합",
        "raw_train": "스케일 전 train 합",
        "scaled_train": "inverted scaling 후 train 합",
        "eval": "eval 합",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "dropout-inverted-scaling-sum-en.png",
        "title": "Activation sums before and after inverted dropout scaling",
        "step_label": "training step",
        "sum_label": "sum of activations",
        "raw_train": "raw training sum",
        "scaled_train": "after inverted scaling",
        "eval": "evaluation sum",
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK JP",
            "Microsoft YaHei",
            "PingFang SC",
            "Songti SC",
            "Hiragino Sans GB",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "dropout-inverted-scaling-sum-zh.png",
        "title": "inverted dropout scaling 前后的 activation 总和",
        "step_label": "训练 step",
        "sum_label": "activation 总和",
        "raw_train": "缩放前 train 总和",
        "scaled_train": "inverted scaling 后 train 总和",
        "eval": "eval 总和",
    },
}


def choose_font(candidates: list[str]) -> str:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def configure_font(text: dict[str, str]) -> None:
    plt.rcParams["font.family"] = choose_font(text["font_candidates"])
    plt.rcParams["axes.unicode_minus"] = False


def load_rows() -> list[dict[str, object]]:
    rows = []
    with CSV_PATH.open(encoding="utf-8") as file:
        for row in DictReader(file):
            rows.append(
                {
                    "step": int(row["step"]),
                    "activation": float(row["activation"]),
                    "train_mask": int(row["train_mask"]),
                    "train_value": float(row["train_value"]),
                    "eval_value": float(row["eval_value"]),
                }
            )
    return rows


def summarize(rows: list[dict[str, object]]) -> tuple[list[int], list[float], list[float], list[float]]:
    steps = sorted({row["step"] for row in rows})
    raw_train_sums = []
    scaled_train_sums = []
    eval_sums = []
    for step in steps:
        step_rows = [row for row in rows if row["step"] == step]
        raw_train_sums.append(sum(float(row["train_value"]) for row in step_rows))
        scaled_train_sums.append(
            sum(float(row["activation"]) * int(row["train_mask"]) / KEEP_PROBABILITY for row in step_rows)
        )
        eval_sums.append(sum(float(row["eval_value"]) for row in step_rows))
    return steps, raw_train_sums, scaled_train_sums, eval_sums


def save_chart(text: dict[str, str], rows: list[dict[str, object]]) -> None:
    configure_font(text)
    steps, raw_train_sums, scaled_train_sums, eval_sums = summarize(rows)

    fig, ax = plt.subplots(figsize=(7.2, 4.1), dpi=170)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.plot(steps, raw_train_sums, color="#dc2626", linewidth=2.1, marker="o", markersize=3.4, label=text["raw_train"])
    ax.plot(
        steps,
        scaled_train_sums,
        color="#0f766e",
        linewidth=2.2,
        marker="s",
        markersize=3.4,
        label=text["scaled_train"],
    )
    ax.plot(steps, eval_sums, color="#2563eb", linewidth=2.0, linestyle="--", label=text["eval"])

    ax.set_title(text["title"], fontsize=12.5)
    ax.set_xlabel(text["step_label"])
    ax.set_ylabel(text["sum_label"])
    ax.set_xlim(min(steps), max(steps))
    ax.set_ylim(0, max(scaled_train_sums) + 0.8)
    ax.legend(frameon=False, fontsize=8.3, loc="lower right")

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    rows = load_rows()
    for text in LANG_TEXT.values():
        save_chart(text, rows)


if __name__ == "__main__":
    main()
