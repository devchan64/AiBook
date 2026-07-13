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

POINTS = np.array([0.0, 0.9, 1.2, 1.25, 0.85, -0.05])
TOKENS = ["UP2", "UP1", "FLAT", "DOWN1", "DOWN2"]

LANG_TEXT = {
    "ko": {
        "font_candidates": ["Apple SD Gothic Neo", "AppleGothic", "Arial Unicode MS", "DejaVu Sans"],
        "xlabel": "시간",
        "ylabel": "값",
        "segment_labels": ["큰 상승", "완만한 상승", "거의 평평", "하강", "큰 하강"],
        "outfile": "segment-tokenization-curve-ko.png",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "xlabel": "time",
        "ylabel": "value",
        "segment_labels": ["strong rise", "gentle rise", "almost flat", "decline", "large decline"],
        "outfile": "segment-tokenization-curve-en.png",
    },
    "zh": {
        "font_candidates": ["Arial Unicode MS", "Heiti TC", "PingFang SC", "DejaVu Sans"],
        "xlabel": "时间",
        "ylabel": "值",
        "segment_labels": ["大幅上升", "缓慢上升", "几乎平", "下降", "大幅下降"],
        "outfile": "segment-tokenization-curve-zh.png",
    },
}


def choose_font(candidates: list[str]) -> str:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def save_chart(lang: str, text: dict[str, object]) -> None:
    plt.rcParams["font.family"] = choose_font(text["font_candidates"])
    plt.rcParams["axes.unicode_minus"] = False

    x = np.arange(len(POINTS))
    fig, ax = plt.subplots(figsize=(7.2, 3.35), dpi=160)

    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.plot(x, POINTS, marker="o", markersize=5.5, linewidth=2.0, color="#0969da")
    ax.set_xlim(-0.1, 5.1)
    ax.set_ylim(-0.35, 1.55)
    ax.set_xlabel(text["xlabel"])
    ax.set_ylabel(text["ylabel"])
    ax.grid(True, color="#d0d7de", linewidth=0.8, alpha=0.75)

    for boundary in range(1, 5):
        ax.axvline(boundary, color="#8c959f", linestyle=(0, (4, 4)), linewidth=1.0)

    label_y = [1.34, 1.38, 1.30, 0.82, 0.2]
    for idx, label in enumerate(text["segment_labels"]):
        midpoint = idx + 0.5
        ax.text(midpoint, label_y[idx], label, ha="center", va="center", fontsize=9.5, color="#57606a")

    for idx, token in enumerate(TOKENS):
        midpoint = idx + 0.5
        color = "#0969da" if token.startswith("UP") else "#cf222e" if token.startswith("DOWN") else "#57606a"
        face = "#ddf4ff" if token.startswith("UP") else "#ffebe9" if token.startswith("DOWN") else "#f6f8fa"
        edge = color if token != "FLAT" else "#8c959f"
        ax.text(
            midpoint,
            -0.23,
            token,
            ha="center",
            va="center",
            fontsize=9.5,
            fontweight="bold",
            color=color,
            bbox={"boxstyle": "round,pad=0.36", "facecolor": face, "edgecolor": edge, "linewidth": 1.0},
        )

    ax.set_xticks(np.arange(6))
    ax.set_xticklabels(["0", "1", "2", "3", "4", "5"])
    ax.set_yticks([-0.25, 0.25, 0.75, 1.25])

    fig.tight_layout(pad=0.8)
    fig.savefig(OUT_DIR / text["outfile"])
    plt.close(fig)


def main() -> None:
    for lang, text in LANG_TEXT.items():
        save_chart(lang, text)


if __name__ == "__main__":
    main()
