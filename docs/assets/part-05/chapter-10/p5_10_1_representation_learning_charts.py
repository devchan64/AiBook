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

DATA = np.array(
    [
        [6.0, 5.0, 1.0],
        [2.0, 3.0, 5.0],
        [1.0, 1.0, 1.0],
        [5.0, 4.0, 5.0],
    ]
)
RISK_SCORE = DATA[:, 0] * 3 + DATA[:, 1] * 4 + DATA[:, 2] * 5


def compute_representation(data: np.ndarray) -> np.ndarray:
    standardized = (data - data.mean(axis=0)) / data.std(axis=0)
    _, _, components = np.linalg.svd(standardized, full_matrices=False)
    axes = components[:2].copy()
    if axes[0, 0] < 0:
        axes[0] *= -1
    if axes[1, 2] < 0:
        axes[1] *= -1
    return standardized @ axes.T


REPRESENTATION = compute_representation(DATA)

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
        "risk_outfile": "representation-risk-score-ko.png",
        "coordinate_outfile": "representation-coordinate-space-ko.png",
        "line": "line",
        "risk_score": "hand-crafted risk score",
        "axis_1": "데이터 기반 표현 축 1",
        "axis_2": "데이터 기반 표현 축 2",
        "close_score": "점수는 같음",
        "far_rep": "표현 좌표는 멀어짐",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "risk_outfile": "representation-risk-score-en.png",
        "coordinate_outfile": "representation-coordinate-space-en.png",
        "line": "line",
        "risk_score": "hand-crafted risk score",
        "axis_1": "data-driven representation axis 1",
        "axis_2": "data-driven representation axis 2",
        "close_score": "same score",
        "far_rep": "farther in representation",
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
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_risk_score_chart(text: dict[str, str]) -> None:
    configure_font(text)
    labels = [f"{text['line']}_{name}" for name in ["A", "B", "C", "D"]]

    fig, ax = plt.subplots(figsize=(6.0, 3.5), dpi=170)
    fig.patch.set_facecolor("white")
    style_axis(ax)

    colors = ["#2563eb", "#2563eb", "#94a3b8", "#dc2626"]
    bars = ax.bar(labels, RISK_SCORE, color=colors, width=0.62)
    for bar, value in zip(bars, RISK_SCORE):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 1.3,
            f"{value:.1f}" if value % 1 else f"{value:.0f}",
            ha="center",
            va="bottom",
            fontsize=8.8,
            color="#111827",
        )

    ax.annotate(
        text["close_score"],
        xy=(0.5, 43.0),
        xytext=(0.5, 51.0),
        ha="center",
        fontsize=8.6,
        color="#1e3a8a",
        arrowprops={"arrowstyle": "<->", "color": "#1e3a8a", "linewidth": 0.9},
    )
    ax.set_ylabel(text["risk_score"])
    ax.set_ylim(0, 63)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["risk_outfile"], format="png", bbox_inches="tight")
    plt.close(fig)


def save_coordinate_chart(text: dict[str, str]) -> None:
    configure_font(text)

    fig, ax = plt.subplots(figsize=(5.8, 4.0), dpi=170)
    fig.patch.set_facecolor("white")
    style_axis(ax)

    colors = ["#2563eb", "#dc2626", "#94a3b8", "#16a34a"]
    ax.scatter(REPRESENTATION[:, 0], REPRESENTATION[:, 1], s=72, color=colors, zorder=3)
    for index, (x, y) in enumerate(REPRESENTATION, start=1):
        line_name = ["A", "B", "C", "D"][index - 1]
        ax.text(x + 0.13, y + 0.08, f"{text['line']}_{line_name}", fontsize=8.6, color="#111827")

    ax.plot(
        [REPRESENTATION[0, 0], REPRESENTATION[1, 0]],
        [REPRESENTATION[0, 1], REPRESENTATION[1, 1]],
        color="#7f1d1d",
        linewidth=1.1,
        linestyle=(0, (4, 3)),
    )
    midpoint = (REPRESENTATION[0] + REPRESENTATION[1]) / 2
    ax.annotate(
        text["far_rep"],
        xy=(midpoint[0], midpoint[1]),
        xytext=(midpoint[0] + 0.9, midpoint[1] + 0.8),
        fontsize=8.4,
        color="#7f1d1d",
        arrowprops={"arrowstyle": "->", "color": "#7f1d1d", "linewidth": 0.8},
    )

    ax.set_xlabel(text["axis_1"])
    ax.set_ylabel(text["axis_2"])
    ax.set_xlim(-2.4, 1.9)
    ax.set_ylim(-1.5, 1.4)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["coordinate_outfile"], format="png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_risk_score_chart(text)
        save_coordinate_chart(text)


if __name__ == "__main__":
    main()
