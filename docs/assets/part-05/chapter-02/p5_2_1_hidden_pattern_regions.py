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

BATCHES = {
    "batch_1": (1.0, 0.2),
    "batch_2": (0.3, 1.0),
    "batch_3": (1.1, 1.0),
    "batch_4": (0.1, 0.2),
}

FOLLOW_UPS = {
    "batch_2_x1": ((0.3, 1.0), (0.9, 1.0)),
    "batch_1_x2": ((1.0, 0.2), (1.0, 1.0)),
}

LANG_TEXT = {
    "ko": {
        "font_candidates": ["Apple SD Gothic Neo", "AppleGothic", "Arial Unicode MS", "DejaVu Sans"],
        "xlabel": "입력 x1",
        "ylabel": "입력 x2",
        "h1": "h1 켜짐 경계",
        "h2": "h2 켜짐 경계",
        "region": "h1과 h2가 함께 켜지는 영역",
        "arrow_1": "batch_2의 x1 증가",
        "arrow_2": "batch_1의 x2 증가",
        "outfile": "hidden-pattern-regions-ko.png",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "xlabel": "input x1",
        "ylabel": "input x2",
        "h1": "h1-on boundary",
        "h2": "h2-on boundary",
        "region": "region where h1 and h2 are both on",
        "arrow_1": "raise batch_2 x1",
        "arrow_2": "raise batch_1 x2",
        "outfile": "hidden-pattern-regions-en.png",
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK JP",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "xlabel": "输入 x1",
        "ylabel": "输入 x2",
        "h1": "h1 激活边界",
        "h2": "h2 激活边界",
        "region": "h1 与 h2 同时激活的区域",
        "arrow_1": "提高 batch_2 的 x1",
        "arrow_2": "提高 batch_1 的 x2",
        "outfile": "hidden-pattern-regions-zh.png",
    },
}


def choose_font(candidates: list[str]) -> str:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def step(z):
    return (z > 0).astype(int) if isinstance(z, np.ndarray) else int(z > 0)


def hidden_pattern(x1: np.ndarray, x2: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    h1 = step(x1 * 0.9 + x2 * -0.3 - 0.2)
    h2 = step(x1 * -0.5 + x2 * 1.0 - 0.4)
    return h1, h2


def save_chart(lang: str, text: dict[str, object]) -> None:
    plt.rcParams["font.family"] = choose_font(text["font_candidates"])
    plt.rcParams["axes.unicode_minus"] = False

    x = np.linspace(0.0, 1.3, 360)
    y = np.linspace(0.0, 1.2, 360)
    xx, yy = np.meshgrid(x, y)
    h1, h2 = hidden_pattern(xx, yy)
    both_on = (h1 + h2 == 2).astype(int)

    fig, ax = plt.subplots(figsize=(7.4, 4.5), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    ax.contourf(xx, yy, both_on, levels=[-0.5, 0.5, 1.5], colors=["#ffffff", "#d1fae5"], alpha=0.95)

    h1_line = 3.0 * x - (2.0 / 3.0)
    h2_line = 0.5 * x + 0.4
    h1_mask = (h1_line >= 0.0) & (h1_line <= 1.2)
    h2_mask = (h2_line >= 0.0) & (h2_line <= 1.2)
    ax.plot(x[h1_mask], h1_line[h1_mask], color="#2563eb", linewidth=2.2)
    ax.plot(x[h2_mask], h2_line[h2_mask], color="#dc2626", linewidth=2.2)

    ax.text(0.44, 0.88, text["h1"], color="#2563eb", fontsize=9.5, rotation=56, ha="center", va="center")
    ax.text(0.86, 0.86, text["h2"], color="#dc2626", fontsize=9.5, rotation=22, ha="center", va="center")
    ax.text(0.78, 1.12, text["region"], color="#047857", fontsize=10.2, ha="center", va="center")

    batch_styles = {
        "batch_1": {"color": "#2563eb", "offset": (0.035, -0.055)},
        "batch_2": {"color": "#dc2626", "offset": (-0.16, 0.035)},
        "batch_3": {"color": "#047857", "offset": (0.035, 0.03)},
        "batch_4": {"color": "#64748b", "offset": (0.035, 0.035)},
    }
    for name, (x1, x2) in BATCHES.items():
        style = batch_styles[name]
        ax.scatter([x1], [x2], s=72, color=style["color"], edgecolor="white", linewidth=1.1, zorder=4)
        dx, dy = style["offset"]
        ax.text(x1 + dx, x2 + dy, name, fontsize=9.3, color="#334155", ha="left", va="center")

    for arrow_key, label_key in [("batch_2_x1", "arrow_1"), ("batch_1_x2", "arrow_2")]:
        (x0, y0), (x1, y1) = FOLLOW_UPS[arrow_key]
        ax.annotate(
            "",
            xy=(x1, y1),
            xytext=(x0, y0),
            arrowprops={"arrowstyle": "->", "color": "#7c3aed", "linewidth": 2.0, "shrinkA": 8, "shrinkB": 8},
        )
        ax.text((x0 + x1) / 2.0, (y0 + y1) / 2.0 + 0.055, text[label_key], color="#6d28d9", fontsize=9.2, ha="center")

    ax.set_xlim(0.0, 1.3)
    ax.set_ylim(0.0, 1.2)
    ax.set_xlabel(text["xlabel"])
    ax.set_ylabel(text["ylabel"])
    ax.set_xticks(np.arange(0.0, 1.31, 0.2))
    ax.set_yticks(np.arange(0.0, 1.21, 0.2))
    ax.grid(True, color="#d0d7de", linewidth=0.7, alpha=0.75)
    ax.set_axisbelow(True)
    fig.tight_layout(pad=0.8)
    fig.savefig(OUT_DIR / text["outfile"])
    plt.close(fig)


def main() -> None:
    for lang, text in LANG_TEXT.items():
        save_chart(lang, text)


if __name__ == "__main__":
    main()
