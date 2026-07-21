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
from matplotlib.colors import ListedColormap

OUT_DIR = Path(__file__).resolve().parent

ROWS = [
    {
        "key": "too_many_comparisons",
        "compute": 2,
        "retention": 0,
    },
    {
        "key": "early_clue_fades",
        "compute": 0,
        "retention": 2,
    },
    {
        "key": "large_window_weak_clue",
        "compute": 1,
        "retention": 2,
    },
    {
        "key": "both_bottlenecks",
        "compute": 2,
        "retention": 2,
    },
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
        "outfile": "long-context-failure-axis-ko.png",
        "row_labels": {
            "too_many_comparisons": "입력이 길어져\n응답이 버벅임",
            "early_clue_fades": "앞쪽 정의나 예외가\n뒤 판단에서 약해짐",
            "large_window_weak_clue": "window는 커졌지만\n핵심 단서가 흐려짐",
            "both_bottlenecks": "비교도 줄이고\n먼 단서도 살려야 함",
        },
        "columns": ["계산 부담", "단서 유지"],
        "levels": ["낮음", "중간", "높음"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "long-context-failure-axis-en.png",
        "row_labels": {
            "too_many_comparisons": "long input\nslows response",
            "early_clue_fades": "early definition or\nexception fades later",
            "large_window_weak_clue": "larger window but\nkey clue weakens",
            "both_bottlenecks": "reduce comparisons\nand keep distant clues",
        },
        "columns": ["compute burden", "clue retention"],
        "levels": ["low", "medium", "high"],
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


def save_chart(text: dict[str, object]) -> None:
    configure_font(text)
    matrix = [[row["compute"], row["retention"]] for row in ROWS]
    row_labels = [text["row_labels"][row["key"]] for row in ROWS]
    cmap = ListedColormap(["#e2e8f0", "#f59e0b", "#0f766e"])

    fig, ax = plt.subplots(figsize=(7.4, 4.4), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.imshow(matrix, cmap=cmap, vmin=0, vmax=2, aspect="auto")

    ax.set_xticks(range(2), text["columns"])
    ax.set_yticks(range(len(row_labels)), row_labels)
    ax.tick_params(axis="x", labelsize=10, pad=8)
    ax.tick_params(axis="y", labelsize=9)

    ax.set_xticks([0.5], minor=True)
    ax.set_yticks([index - 0.5 for index in range(1, len(row_labels))], minor=True)
    ax.grid(which="minor", color="white", linewidth=2.2)
    ax.tick_params(which="minor", bottom=False, left=False)

    levels = text["levels"]
    for row_index, row in enumerate(matrix):
        for col_index, value in enumerate(row):
            ax.text(
                col_index,
                row_index,
                levels[value],
                ha="center",
                va="center",
                color="white" if value == 2 else "#172033",
                fontsize=9,
                fontweight="bold",
            )

    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
