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
PREFIX_LENGTHS = [3, 20, 100]
GENERATED_LENGTH = 5

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
        "outfile": "kv-cache-projection-count-ko.png",
        "xlabel": "prefix 길이",
        "ylabel": "K/V projection 대상 토큰 수",
        "without_cache": "cache 없음",
        "with_cache": "KV cache",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "kv-cache-projection-count-en.png",
        "xlabel": "prefix length",
        "ylabel": "tokens projected to K/V",
        "without_cache": "without cache",
        "with_cache": "KV cache",
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


def projection_counts(prefix_length: int, generated_length: int) -> tuple[int, int]:
    without_cache = sum(prefix_length + step for step in range(1, generated_length + 1))
    with_cache = prefix_length + generated_length
    return without_cache, with_cache


def summarize_counts() -> list[dict[str, int]]:
    rows = []
    for prefix_length in PREFIX_LENGTHS:
        without_cache, with_cache = projection_counts(prefix_length, GENERATED_LENGTH)
        rows.append(
            {
                "prefix_length": prefix_length,
                "without_cache": without_cache,
                "with_cache": with_cache,
            }
        )
    return rows


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_projection_chart(text: dict[str, str]) -> None:
    configure_font(text)
    rows = summarize_counts()
    labels = [str(row["prefix_length"]) for row in rows]
    without_cache = [row["without_cache"] for row in rows]
    with_cache = [row["with_cache"] for row in rows]
    x_positions = list(range(len(labels)))
    width = 0.34

    fig, ax = plt.subplots(figsize=(6.4, 3.8), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    left_positions = [x - width / 2 for x in x_positions]
    right_positions = [x + width / 2 for x in x_positions]
    left_bars = ax.bar(left_positions, without_cache, width=width, color="#dc2626", label=text["without_cache"])
    right_bars = ax.bar(right_positions, with_cache, width=width, color="#2563eb", label=text["with_cache"])

    for bars in (left_bars, right_bars):
        for bar in bars:
            value = bar.get_height()
            ax.annotate(
                f"{value:g}",
                (bar.get_x() + bar.get_width() / 2, value),
                textcoords="offset points",
                xytext=(0, 6),
                ha="center",
                fontsize=9,
                color="#172033",
            )

    ax.set_xticks(x_positions, labels)
    ax.set_xlabel(text["xlabel"])
    ax.set_ylabel(text["ylabel"])
    ax.set_ylim(0, max(without_cache) * 1.18)
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_projection_chart(text)


if __name__ == "__main__":
    main()
