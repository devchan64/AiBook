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

TASK_OUTPUTS = {
    "classification": {"label": 3, "score": 3, "rank": 0},
    "pair_relation": {"label": 2, "score": 2, "rank": 0},
    "ranking": {"label": 0, "score": 3, "rank": 3},
}

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
        "outfile": "understanding-output-types-ko.png",
        "ylabel": "출력 항목 수",
        "tasks": ["분류", "문장쌍", "검색 랭킹"],
        "series": ["라벨", "점수", "순위"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "understanding-output-types-en.png",
        "ylabel": "output items",
        "tasks": ["classification", "pair relation", "ranking"],
        "series": ["label", "score", "rank"],
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


def save_chart(text: dict[str, object]) -> None:
    configure_font(text)
    task_keys = list(TASK_OUTPUTS)
    series_keys = ["label", "score", "rank"]
    x_positions = range(len(task_keys))
    width = 0.24
    colors = ["#0f766e", "#2563eb", "#f59e0b"]

    fig, ax = plt.subplots(figsize=(8.1, 3.9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    for offset_index, series_key in enumerate(series_keys):
        values = [TASK_OUTPUTS[task][series_key] for task in task_keys]
        bars = ax.bar(
            [x + (offset_index - 1) * width for x in x_positions],
            values,
            width=width,
            color=colors[offset_index],
            label=text["series"][offset_index],
        )
        for bar in bars:
            value = bar.get_height()
            if value == 0:
                continue
            ax.annotate(
                f"{value:g}",
                (bar.get_x() + bar.get_width() / 2, value),
                textcoords="offset points",
                xytext=(0, 7),
                ha="center",
                fontsize=8.4,
                color="#172033",
            )

    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(text["tasks"])
    ax.set_ylabel(text["ylabel"])
    ax.set_ylim(0, 3.9)
    ax.legend(frameon=False, fontsize=8.7, ncol=3)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
