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

SIGNALS = np.array(
    [
        [1.0, 2.0],
        [2.0, 1.0],
        [0.5, 3.0],
        [3.0, 0.5],
    ]
)
W1 = np.array(
    [
        [0.8, 0.2, 0.5],
        [0.1, 0.7, 0.4],
    ]
)
W2 = np.array(
    [
        [0.5, 0.3],
        [0.2, 0.9],
        [0.6, 0.1],
    ]
)


def relu(x: np.ndarray) -> np.ndarray:
    return np.maximum(0, x)


H1 = relu(SIGNALS @ W1)
H2 = relu(H1 @ W2)
STAGES = ["signals", "h1", "h2"]
PAIR_12 = [np.linalg.norm(SIGNALS[0] - SIGNALS[1]), np.linalg.norm(H1[0] - H1[1]), np.linalg.norm(H2[0] - H2[1])]
PAIR_14 = [np.linalg.norm(SIGNALS[0] - SIGNALS[3]), np.linalg.norm(H1[0] - H1[3]), np.linalg.norm(H2[0] - H2[3])]

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
        "distance_outfile": "hierarchical-representation-distance-trace-ko.png",
        "space_outfile": "hierarchical-representation-h2-space-ko.png",
        "distance_ylabel": "배치 쌍 거리",
        "stage_xlabel": "표현 단계",
        "pair_12": "batch_1 - batch_2",
        "pair_14": "batch_1 - batch_4",
        "axis_1": "h2 축 1",
        "axis_2": "h2 축 2",
        "batch": "batch",
        "closer_pair": "더 가까운 이웃",
        "farther_pair": "더 멀리 남은 쌍",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "distance_outfile": "hierarchical-representation-distance-trace-en.png",
        "space_outfile": "hierarchical-representation-h2-space-en.png",
        "distance_ylabel": "pair distance",
        "stage_xlabel": "representation stage",
        "pair_12": "batch_1 - batch_2",
        "pair_14": "batch_1 - batch_4",
        "axis_1": "h2 axis 1",
        "axis_2": "h2 axis 2",
        "batch": "batch",
        "closer_pair": "closer neighbor",
        "farther_pair": "farther pair",
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
        "distance_outfile": "hierarchical-representation-distance-trace-zh.png",
        "space_outfile": "hierarchical-representation-h2-space-zh.png",
        "distance_ylabel": "batch 对距离",
        "stage_xlabel": "表征阶段",
        "pair_12": "batch_1 - batch_2",
        "pair_14": "batch_1 - batch_4",
        "axis_1": "h2 轴 1",
        "axis_2": "h2 轴 2",
        "batch": "batch",
        "closer_pair": "更近的邻居",
        "farther_pair": "仍较远的 pair",
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


def save_distance_trace(text: dict[str, str]) -> None:
    configure_font(text)
    x = np.arange(len(STAGES))
    pair_12 = np.round(PAIR_12, 3)
    pair_14 = np.round(PAIR_14, 3)

    fig, ax = plt.subplots(figsize=(6.2, 3.7), dpi=170)
    fig.patch.set_facecolor("white")
    style_axis(ax)

    ax.plot(x, pair_12, marker="o", linewidth=2.0, color="#2563eb", label=text["pair_12"])
    ax.plot(x, pair_14, marker="o", linewidth=2.0, color="#dc2626", label=text["pair_14"])
    for values, color in ((pair_12, "#2563eb"), (pair_14, "#dc2626")):
        for x_pos, value in zip(x, values):
            ax.text(x_pos, value + 0.07, f"{value:.3f}".rstrip("0").rstrip("."), ha="center", fontsize=8.3, color=color)

    ax.set_xticks(x)
    ax.set_xticklabels(STAGES)
    ax.set_xlabel(text["stage_xlabel"])
    ax.set_ylabel(text["distance_ylabel"])
    ax.set_ylim(0, 2.8)
    ax.legend(loc="upper right", frameon=False, fontsize=8.5)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["distance_outfile"], format="png", bbox_inches="tight")
    plt.close(fig)


def save_h2_space(text: dict[str, str]) -> None:
    configure_font(text)

    fig, ax = plt.subplots(figsize=(5.8, 4.0), dpi=170)
    fig.patch.set_facecolor("white")
    style_axis(ax)

    colors = ["#2563eb", "#f59e0b", "#94a3b8", "#dc2626"]
    ax.scatter(H2[:, 0], H2[:, 1], s=78, color=colors, zorder=3)
    for index, (x, y) in enumerate(H2, start=1):
        ax.text(x + 0.035, y + 0.035, f"{text['batch']}_{index}", fontsize=8.5, color="#111827")

    ax.plot([H2[0, 0], H2[1, 0]], [H2[0, 1], H2[1, 1]], color="#2563eb", linewidth=1.2, linestyle=(0, (4, 3)))
    ax.plot([H2[0, 0], H2[3, 0]], [H2[0, 1], H2[3, 1]], color="#dc2626", linewidth=1.2, linestyle=(0, (4, 3)))
    ax.annotate(
        text["closer_pair"],
        xy=((H2[0, 0] + H2[1, 0]) / 2, (H2[0, 1] + H2[1, 1]) / 2),
        xytext=(1.42, 1.55),
        fontsize=8.3,
        color="#1e3a8a",
        arrowprops={"arrowstyle": "->", "color": "#1e3a8a", "linewidth": 0.8},
    )
    ax.annotate(
        text["farther_pair"],
        xy=((H2[0, 0] + H2[3, 0]) / 2, (H2[0, 1] + H2[3, 1]) / 2),
        xytext=(2.22, 2.12),
        fontsize=8.3,
        color="#7f1d1d",
        arrowprops={"arrowstyle": "->", "color": "#7f1d1d", "linewidth": 0.8},
    )

    ax.set_xlabel(text["axis_1"])
    ax.set_ylabel(text["axis_2"])
    ax.set_xlim(1.45, 2.55)
    ax.set_ylim(1.50, 2.42)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["space_outfile"], format="png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_distance_trace(text)
        save_h2_space(text)


if __name__ == "__main__":
    main()
