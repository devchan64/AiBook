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
from matplotlib.ticker import FuncFormatter


OUT_DIR = Path(__file__).resolve().parent

STAGES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
CANDIDATES = [3**stage for stage in STAGES]
HIGHLIGHT_STAGES = {1, 2, 5, 10}

LANG_TEXT = {
    "ko": {
        "font_candidates": ["Noto Sans CJK KR", "Apple SD Gothic Neo", "AppleGothic", "Arial Unicode MS", "Droid Sans Fallback", "DejaVu Sans"],
        "xlabel": "단계 수",
        "ylabel": "가능한 조합 수",
        "note": "각 단계 선택지 3개",
        "point_suffix": "개",
        "outfile": "search-space-growth-ko.png",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "xlabel": "number of stages",
        "ylabel": "possible combinations",
        "note": "3 choices at each stage",
        "point_suffix": "",
        "outfile": "search-space-growth-en.png",
    },
    "zh": {
        "font_candidates": ["Noto Sans CJK SC", "Noto Sans CJK TC", "Arial Unicode MS", "Heiti TC", "PingFang SC", "Droid Sans Fallback", "DejaVu Sans"],
        "xlabel": "阶段数",
        "ylabel": "可能组合数",
        "note": "每阶段 3 个选择",
        "point_suffix": "种",
        "outfile": "search-space-growth-zh.png",
    },
}


def choose_font(candidates: list[str]) -> str:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def format_count(value: int, suffix: str) -> str:
    return f"{value:,}{suffix}" if suffix else f"{value:,}"


def save_chart(text: dict[str, object]) -> None:
    plt.rcParams["font.family"] = choose_font(text["font_candidates"])
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(7.4, 3.25), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    ax.plot(STAGES, CANDIDATES, color="#0969da", linewidth=1.8, marker="o", markersize=4.5)
    ax.fill_between(STAGES, CANDIDATES, color="#ddf4ff", alpha=0.55)

    for stage, count in zip(STAGES, CANDIDATES):
        if stage not in HIGHLIGHT_STAGES:
            continue
        ax.annotate(
            format_count(count, text["point_suffix"]),
            xy=(stage, count),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.6,
            color="#0969da",
            bbox={"boxstyle": "round,pad=0.18", "facecolor": "white", "edgecolor": "#0969da", "linewidth": 0.75},
        )

    ax.text(
        0.98,
        0.08,
        text["note"],
        transform=ax.transAxes,
        ha="right",
        va="center",
        fontsize=9.2,
        color="#57606a",
        bbox={"boxstyle": "round,pad=0.24", "facecolor": "#f6f8fa", "edgecolor": "#d0d7de", "linewidth": 0.8},
    )

    ax.set_xlabel(text["xlabel"])
    ax.set_ylabel(text["ylabel"])
    ax.set_xlim(0.7, 10.3)
    ax.set_ylim(0, 64000)
    ax.set_xticks(STAGES)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{int(value):,}"))
    ax.grid(axis="y", color="#d0d7de", linewidth=0.7, alpha=0.75)
    ax.grid(axis="x", color="#d0d7de", linewidth=0.5, alpha=0.35)

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    fig.tight_layout(pad=0.8)
    fig.savefig(OUT_DIR / text["outfile"])
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
