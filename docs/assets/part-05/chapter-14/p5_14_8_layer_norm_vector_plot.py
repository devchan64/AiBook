from pathlib import Path
import os


REPO_ROOT = Path(__file__).resolve().parents[4]
MPL_CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
import numpy as np


OUT_DIR = Path(__file__).resolve().parent

REPRESENTATIONS = {
    "risk_axis_spike": np.array([0.6, 8.0, 0.4, 0.5]),
    "too_narrow": np.array([0.48, 0.51, 0.49, 0.50]),
    "mixed_after_residual": np.array([2.0, 4.5, 1.0, 3.5]),
}

TEXT = {
    "ko": {
        "raw": "정규화 전",
        "norm": "정규화 후",
        "x": "1번 축",
        "y": "2번 축",
        "note": "앞 두 축만 2D로 투영",
    },
    "en": {
        "raw": "before normalization",
        "norm": "after normalization",
        "x": "axis 1",
        "y": "axis 2",
        "note": "2D projection of first two axes",
    },
    "zh": {
        "raw": "normalization 前",
        "norm": "normalization 后",
        "x": "第 1 轴",
        "y": "第 2 轴",
        "note": "只投影前两个轴",
    },
}

COLORS = {
    "risk_axis_spike": "#e03131",
    "too_narrow": "#2f9e44",
    "mixed_after_residual": "#1971c2",
}


def configure_fonts(locale: str):
    candidates_by_locale = {
        "ko": [
            "Apple SD Gothic Neo",
            "AppleGothic",
            "Noto Sans CJK KR",
            "Noto Sans KR",
            "Malgun Gothic",
            "DejaVu Sans",
        ],
        "en": ["DejaVu Sans"],
        "zh": [
            "Hiragino Sans GB",
            "Heiti TC",
            "Songti SC",
            "Noto Sans CJK SC",
            "Microsoft YaHei",
            "PingFang SC",
            "DejaVu Sans",
        ],
    }
    available = {font.name for font in font_manager.fontManager.ttflist}
    for name in candidates_by_locale[locale]:
        if name in available:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False


def layer_norm(x: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    return (x - x.mean()) / (x.std() + eps)


def draw(locale: str):
    text = TEXT[locale]
    fig, ax = plt.subplots(figsize=(7.2, 5.2))

    ax.axhline(0, color="#adb5bd", linewidth=1)
    ax.axvline(0, color="#adb5bd", linewidth=1)
    ax.grid(True, color="#dee2e6", linewidth=0.8)

    for name, raw in REPRESENTATIONS.items():
        normalized = layer_norm(raw)
        raw_xy = raw[:2]
        norm_xy = normalized[:2]
        color = COLORS[name]

        ax.scatter(raw_xy[0], raw_xy[1], s=72, color=color, marker="o")
        ax.scatter(norm_xy[0], norm_xy[1], s=72, color=color, marker="s")
        ax.annotate(
            "",
            xy=norm_xy,
            xytext=raw_xy,
            arrowprops={"arrowstyle": "->", "color": color, "lw": 1.8, "shrinkA": 5, "shrinkB": 5},
        )
        ax.text(raw_xy[0] + 0.08, raw_xy[1] + 0.08, name, fontsize=9, color=color)

    ax.set_xlabel(text["x"])
    ax.set_ylabel(text["y"])
    ax.set_xlim(-1.8, 2.4)
    ax.set_ylim(-0.9, 8.6)
    ax.text(0.02, 0.98, text["note"], transform=ax.transAxes, va="top", fontsize=10, color="#495057")

    legend_handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor="#495057", markersize=8, label=text["raw"]),
        Line2D([0], [0], marker="s", color="none", markerfacecolor="#495057", markersize=8, label=text["norm"]),
        Line2D([0], [0], color="#495057", lw=1.8, label="shift"),
    ]
    ax.legend(handles=legend_handles, loc="upper right", fontsize=9, frameon=True)

    fig.tight_layout()
    fig.savefig(OUT_DIR / f"layer-normalization-vector-shift-{locale}.png", dpi=160)
    plt.close(fig)


def main():
    for locale in ("ko", "en", "zh"):
        configure_fonts(locale)
        draw(locale)


if __name__ == "__main__":
    main()
