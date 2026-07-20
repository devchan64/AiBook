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
EXAMPLE_STEP = 1

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
        "activation_outfile": "dropout-activation-values-ko.png",
        "sum_outfile": "dropout-sum-comparison-ko.png",
        "node_label": "은닉 노드",
        "value_label": "활성값",
        "sum_label": "활성값 합",
        "before": "dropout 전",
        "train": "학습 모드",
        "eval": "평가 모드",
        "dropped": "꺼진 노드",
        "step_label": "학습 step",
        "train_sum": "학습 모드 합",
        "eval_sum": "평가 모드 합",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "activation_outfile": "dropout-activation-values-en.png",
        "sum_outfile": "dropout-sum-comparison-en.png",
        "node_label": "hidden unit",
        "value_label": "activation",
        "sum_label": "sum of activations",
        "before": "before dropout",
        "train": "training mode",
        "eval": "evaluation mode",
        "dropped": "dropped unit",
        "step_label": "training step",
        "train_sum": "training-mode sum",
        "eval_sum": "evaluation-mode sum",
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK JP",
            "Microsoft YaHei",
            "PingFang SC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "activation_outfile": "dropout-activation-values-zh.png",
        "sum_outfile": "dropout-sum-comparison-zh.png",
        "node_label": "隐藏单元",
        "value_label": "激活值",
        "sum_label": "激活值总和",
        "before": "dropout 前",
        "train": "训练模式",
        "eval": "评估模式",
        "dropped": "被关闭的节点",
        "step_label": "训练 step",
        "train_sum": "训练模式总和",
        "eval_sum": "评估模式总和",
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


def load_rows():
    rows = []
    with CSV_PATH.open(encoding="utf-8") as file:
        for row in DictReader(file):
            rows.append(
                {
                    "step": int(row["step"]),
                    "node": row["node"],
                    "activation": float(row["activation"]),
                    "train_mask": int(row["train_mask"]),
                    "train_value": float(row["train_value"]),
                    "eval_value": float(row["eval_value"]),
                }
            )
    return rows


def node_number(row) -> int:
    return int(row["node"].split("_")[1])


def rows_for_step(rows, step: int):
    return sorted([row for row in rows if row["step"] == step], key=node_number)


def save_activation_chart(text: dict[str, str], rows) -> None:
    configure_font(text)
    step_rows = rows_for_step(rows, EXAMPLE_STEP)
    activations = np.array([row["activation"] for row in step_rows])
    train_mask = np.array([row["train_mask"] for row in step_rows])
    train_values = np.array([row["train_value"] for row in step_rows])
    eval_values = np.array([row["eval_value"] for row in step_rows])
    x = np.arange(len(activations))
    width = 0.24

    fig, ax = plt.subplots(figsize=(6.6, 3.8), dpi=170)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.bar(x - width, activations, width, label=text["before"], color="#94a3b8")
    ax.bar(x, train_values, width, label=text["train"], color="#dc2626")
    ax.bar(x + width, eval_values, width, label=text["eval"], color="#2563eb")

    dropped_index = int(np.where(train_mask == 0)[0][0])
    ax.scatter([dropped_index], [0.04], color="#7f1d1d", marker="x", s=52, zorder=4)
    ax.annotate(
        text["dropped"],
        xy=(dropped_index, 0.04),
        xytext=(dropped_index + 0.28, 0.34),
        fontsize=8.5,
        color="#7f1d1d",
        arrowprops={"arrowstyle": "->", "color": "#7f1d1d", "linewidth": 0.8},
    )

    ax.set_xticks(x)
    ax.set_xticklabels([f"{text['node_label']} {i + 1}" for i in x], fontsize=8.4)
    ax.set_ylabel(text["value_label"])
    ax.set_ylim(0, 1.55)
    ax.legend(frameon=False, loc="upper right", fontsize=8.2)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["activation_outfile"], format="png", bbox_inches="tight")
    plt.close(fig)


def save_sum_chart(text: dict[str, str], rows) -> None:
    configure_font(text)
    steps = sorted({row["step"] for row in rows})
    train_sums = []
    eval_sums = []
    for step in steps:
        step_rows = rows_for_step(rows, step)
        train_sums.append(sum(row["train_value"] for row in step_rows))
        eval_sums.append(sum(row["eval_value"] for row in step_rows))

    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=170)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.plot(steps, train_sums, color="#dc2626", linewidth=2.4, marker="o", markersize=3.8, label=text["train_sum"])
    ax.plot(steps, eval_sums, color="#2563eb", linewidth=2.0, linestyle="--", label=text["eval_sum"])
    ax.set_xlabel(text["step_label"])
    ax.set_ylabel(text["sum_label"])
    ax.set_xlim(min(steps), max(steps))
    ax.set_ylim(0, 5.0)
    ax.legend(frameon=False, loc="lower right", fontsize=8.4)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["sum_outfile"], format="png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    rows = load_rows()
    for text in LANG_TEXT.values():
        save_activation_chart(text, rows)
        save_sum_chart(text, rows)


if __name__ == "__main__":
    main()
