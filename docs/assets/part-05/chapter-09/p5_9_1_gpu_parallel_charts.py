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

BATCH = np.array(
    [
        [1.0, 0.5, 2.0],
        [0.2, 1.5, 0.3],
        [1.2, 0.1, 0.7],
        [0.0, 2.0, 1.0],
    ]
)
WEIGHTS = np.array([0.4, 0.8, -0.3])

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
        "score_outfile": "gpu-batch-score-comparison-ko.png",
        "multiply_outfile": "gpu-scalar-multiply-scaling-ko.png",
        "line": "라인",
        "score": "위험 점수",
        "one_by_one": "샘플별 반복",
        "batch": "배치 행렬 계산",
        "multiply_count": "scalar multiply count",
        "batch_size": "batch 크기",
        "current_batch": "현재 batch",
        "double_batch": "batch 두 배",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "score_outfile": "gpu-batch-score-comparison-en.png",
        "multiply_outfile": "gpu-scalar-multiply-scaling-en.png",
        "line": "line",
        "score": "risk score",
        "one_by_one": "one-by-one loop",
        "batch": "batch matrix calculation",
        "multiply_count": "scalar multiply count",
        "batch_size": "batch size",
        "current_batch": "current batch",
        "double_batch": "double batch",
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


def style_axis(ax) -> None:
    ax.set_facecolor("white")
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_score_chart(text: dict[str, str]) -> None:
    configure_font(text)
    scores_one_by_one = []
    scalar_multiply_count = 0
    for sample in BATCH:
        score = 0.0
        for x, w in zip(sample, WEIGHTS):
            score += x * w
            scalar_multiply_count += 1
        scores_one_by_one.append(round(score, 3))

    scores_batch = np.round(BATCH @ WEIGHTS, 3)
    x = np.arange(len(scores_batch))
    width = 0.34

    fig, ax = plt.subplots(figsize=(6.3, 3.6), dpi=170)
    fig.patch.set_facecolor("white")
    style_axis(ax)

    ax.bar(x - width / 2, scores_one_by_one, width, label=text["one_by_one"], color="#94a3b8")
    ax.bar(x + width / 2, scores_batch, width, label=text["batch"], color="#2563eb")
    ax.set_xticks(x)
    ax.set_xticklabels([f"{text['line']} {i + 1}" for i in x], fontsize=8.5)
    ax.set_ylabel(text["score"])
    ax.set_ylim(0, 1.55)
    ax.legend(frameon=False, loc="upper left", fontsize=8.2)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["score_outfile"], format="png", bbox_inches="tight")
    plt.close(fig)


def save_multiply_chart(text: dict[str, str]) -> None:
    configure_font(text)
    current_count = BATCH.shape[0] * BATCH.shape[1]
    labels = [text["current_batch"], text["double_batch"]]
    counts = [current_count, current_count * 2]

    fig, ax = plt.subplots(figsize=(5.4, 3.4), dpi=170)
    fig.patch.set_facecolor("white")
    style_axis(ax)

    bars = ax.bar(labels, counts, color=["#2563eb", "#dc2626"], width=0.58)
    for bar, value in zip(bars, counts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.7,
            str(value),
            ha="center",
            va="bottom",
            fontsize=9,
            color="#111827",
        )

    ax.set_ylabel(text["multiply_count"])
    ax.set_xlabel(text["batch_size"])
    ax.set_ylim(0, 28)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["multiply_outfile"], format="png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_score_chart(text)
        save_multiply_chart(text)


if __name__ == "__main__":
    main()
