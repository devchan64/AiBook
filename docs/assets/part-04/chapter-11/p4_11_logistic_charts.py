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

LANG_TEXT = {
    "ko": {
        "font_candidates": ["Noto Sans CJK KR", "Apple SD Gothic Neo", "AppleGothic", "Arial Unicode MS", "DejaVu Sans"],
        "sigmoid_outfile": "p4-11-1-sigmoid-score-map-ko.png",
        "threshold_outfile": "p4-11-2-threshold-shift-ko.png",
        "z_label": "선형 점수 z",
        "p_label": "sigmoid 출력 p",
        "z0": "z = 0",
        "p05": "p = 0.5",
        "class0": "class 0 쪽",
        "class1": "class 1 쪽",
        "threshold": "threshold",
        "stricter": "더 엄격한 기준",
        "region0": "class 0 영역",
        "region1": "class 1 영역",
        "score": "점수",
        "panel_05": "threshold = 0.5",
        "panel_07": "threshold = 0.7",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "sigmoid_outfile": "p4-11-1-sigmoid-score-map-en.png",
        "threshold_outfile": "p4-11-2-threshold-shift-en.png",
        "z_label": "linear score z",
        "p_label": "sigmoid output p",
        "z0": "z = 0",
        "p05": "p = 0.5",
        "class0": "class 0 side",
        "class1": "class 1 side",
        "threshold": "threshold",
        "stricter": "stricter cutoff",
        "region0": "class 0 region",
        "region1": "class 1 region",
        "score": "score",
        "panel_05": "threshold = 0.5",
        "panel_07": "threshold = 0.7",
    },
    "zh": {
        "font_candidates": ["Noto Sans CJK SC", "Arial Unicode MS", "Heiti TC", "PingFang SC", "DejaVu Sans"],
        "sigmoid_outfile": "p4-11-1-sigmoid-score-map-zh.png",
        "threshold_outfile": "p4-11-2-threshold-shift-zh.png",
        "z_label": "线性分数 z",
        "p_label": "sigmoid 输出 p",
        "z0": "z = 0",
        "p05": "p = 0.5",
        "class0": "0 类一侧",
        "class1": "1 类一侧",
        "threshold": "阈值",
        "stricter": "更严格的线",
        "region0": "0 类区域",
        "region1": "1 类区域",
        "score": "分数",
        "panel_05": "threshold = 0.5",
        "panel_07": "threshold = 0.7",
    },
}


def choose_font(candidates: list[str]) -> str:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def configure_font(text: dict[str, object]) -> None:
    plt.rcParams["font.family"] = choose_font(text["font_candidates"])
    plt.rcParams["axes.unicode_minus"] = False


def save_sigmoid_chart(text: dict[str, object]) -> None:
    configure_font(text)
    z = np.linspace(-6, 6, 500)
    p = 1 / (1 + np.exp(-z))

    fig, ax = plt.subplots(figsize=(7.2, 3.6), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    ax.plot(z, p, color="#0969da", linewidth=1.8)
    ax.axvline(0, color="#cf222e", linewidth=1.1, linestyle=(0, (4, 4)))
    ax.axhline(0.5, color="#cf222e", linewidth=1.1, linestyle=(0, (4, 4)))
    ax.scatter([0], [0.5], s=36, color="#cf222e", zorder=4)

    ax.text(-4.8, 0.18, text["class0"], color="#57606a", fontsize=9.5)
    ax.text(2.2, 0.82, text["class1"], color="#57606a", fontsize=9.5)
    ax.text(0.15, 0.08, text["z0"], color="#cf222e", fontsize=9.5)
    ax.text(-5.7, 0.53, text["p05"], color="#cf222e", fontsize=9.5)

    ax.set_xlim(-6, 6)
    ax.set_ylim(-0.04, 1.04)
    ax.set_xlabel(text["z_label"])
    ax.set_ylabel(text["p_label"])
    ax.set_xticks([-6, -3, 0, 3, 6])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.75)

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    fig.tight_layout(pad=0.8)
    fig.savefig(OUT_DIR / text["sigmoid_outfile"])
    plt.close(fig)


def draw_threshold_panel(ax, threshold: float, text: dict[str, object], panel_label: str, strict: bool) -> None:
    scores = [0.42, 0.58, 0.73]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xticks([0, threshold, 1])
    ax.set_xticklabels(["0", f"{threshold:.1f}", "1"])
    ax.set_xlabel(text["score"])

    ax.axvspan(0, threshold, ymin=0.34, ymax=0.76, color="#ddf4ff", alpha=0.8)
    ax.axvspan(threshold, 1, ymin=0.34, ymax=0.76, color="#ffebe9", alpha=0.8)
    ax.axvline(threshold, ymin=0.24, ymax=0.86, color="#cf222e", linewidth=1.2, linestyle=(0, (4, 4)))
    ax.hlines(0.5, 0, 1, color="#57606a", linewidth=1.1)

    dot_color = "#0969da" if not strict else "#1a7f37"
    ax.scatter(scores, [0.5] * len(scores), s=38, color=dot_color, zorder=5)
    for score in scores:
        ax.text(score, 0.37, f"{score:.2f}", ha="center", va="center", fontsize=8.5, color="#57606a")

    ax.text(0.03, 0.72, text["region0"], fontsize=9.0, color="#57606a")
    ax.text(min(threshold + 0.05, 0.82), 0.72, text["region1"], fontsize=9.0, color="#57606a")
    ax.text(threshold, 0.88, text["stricter"] if strict else text["threshold"], ha="center", fontsize=9.0, color="#cf222e")
    ax.set_title(panel_label, loc="left", fontsize=10.5, fontweight="bold", color="#24292f")

    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)


def save_threshold_chart(text: dict[str, object]) -> None:
    configure_font(text)
    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.25), dpi=160, sharey=True)
    fig.patch.set_facecolor("white")

    draw_threshold_panel(axes[0], 0.5, text, text["panel_05"], strict=False)
    draw_threshold_panel(axes[1], 0.7, text, text["panel_07"], strict=True)

    fig.tight_layout(pad=0.9, w_pad=1.2)
    fig.savefig(OUT_DIR / text["threshold_outfile"])
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_sigmoid_chart(text)
        save_threshold_chart(text)


if __name__ == "__main__":
    main()
