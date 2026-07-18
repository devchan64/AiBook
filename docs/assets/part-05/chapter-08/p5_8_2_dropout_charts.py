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

ACTIVATIONS = np.array([0.9, 1.3, 0.4, 1.1, 0.7])
TRAIN_MASK = np.array([1, 1, 1, 0, 1])
TRAIN_VALUES = ACTIVATIONS * TRAIN_MASK
EVAL_VALUES = ACTIVATIONS.copy()

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


def save_activation_chart(text: dict[str, str]) -> None:
    configure_font(text)
    x = np.arange(len(ACTIVATIONS))
    width = 0.24

    fig, ax = plt.subplots(figsize=(6.6, 3.8), dpi=170)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.bar(x - width, ACTIVATIONS, width, label=text["before"], color="#94a3b8")
    ax.bar(x, TRAIN_VALUES, width, label=text["train"], color="#dc2626")
    ax.bar(x + width, EVAL_VALUES, width, label=text["eval"], color="#2563eb")

    dropped_index = int(np.where(TRAIN_MASK == 0)[0][0])
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


def save_sum_chart(text: dict[str, str]) -> None:
    configure_font(text)
    labels = [text["before"], text["train"], text["eval"]]
    sums = [ACTIVATIONS.sum(), TRAIN_VALUES.sum(), EVAL_VALUES.sum()]
    colors = ["#94a3b8", "#dc2626", "#2563eb"]

    fig, ax = plt.subplots(figsize=(5.6, 3.5), dpi=170)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    bars = ax.bar(labels, sums, color=colors, width=0.58)
    for bar, value in zip(bars, sums):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.08,
            f"{value:.1f}",
            ha="center",
            va="bottom",
            fontsize=9,
            color="#111827",
        )

    ax.set_ylabel(text["sum_label"])
    ax.set_ylim(0, 5.0)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["sum_outfile"], format="png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_activation_chart(text)
        save_sum_chart(text)


if __name__ == "__main__":
    main()
