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

OUT_DIR = Path(__file__).resolve().parent

SEARCH_CASES = [
    {"query": "refund delay", "lexical": 0, "normalized": 1},
    {"query": "cancel order", "lexical": 1, "normalized": 3},
]

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
        "outfile": "history-computation-search-gain-ko.png",
        "ylabel": "관련 토큰 일치 수",
        "labels": ["환불 지연", "주문 취소"],
        "series": ["단어 그대로", "정규화 후"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "history-computation-search-gain-en.png",
        "ylabel": "matched relevant tokens",
        "labels": ["refund delay", "cancel order"],
        "series": ["lexical", "normalized"],
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


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def annotate(ax, bars) -> None:
    for bar in bars:
        value = bar.get_height()
        ax.annotate(
            f"{value:g}",
            (bar.get_x() + bar.get_width() / 2, value),
            textcoords="offset points",
            xytext=(0, 7),
            ha="center",
            fontsize=8.8,
            color="#172033",
        )


def save_chart(text: dict[str, object]) -> None:
    configure_font(text)
    labels = text["labels"]
    lexical = [case["lexical"] for case in SEARCH_CASES]
    normalized = [case["normalized"] for case in SEARCH_CASES]
    x_positions = range(len(labels))
    width = 0.34

    fig, ax = plt.subplots(figsize=(7.5, 3.8), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    left_bars = ax.bar(
        [x - width / 2 for x in x_positions],
        lexical,
        width=width,
        label=text["series"][0],
        color="#64748b",
    )
    right_bars = ax.bar(
        [x + width / 2 for x in x_positions],
        normalized,
        width=width,
        label=text["series"][1],
        color="#0f766e",
    )
    annotate(ax, left_bars)
    annotate(ax, right_bars)

    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(labels)
    ax.set_ylabel(text["ylabel"])
    ax.set_ylim(0, max(normalized) * 1.35)
    ax.legend(frameon=False, fontsize=8.8)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
