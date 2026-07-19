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
from matplotlib.colors import LinearSegmentedColormap

OUT_DIR = Path(__file__).resolve().parent

SCORES = [
    [10, 0, 0, 6],
    [1, 9, 3, 3],
    [0, 3, 10, 0],
    [6, 0, 0, 10],
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
        "outfile": "solution-selection-score-map-ko.png",
        "title": "실패 유형별 우선 수단 점수",
        "rows": ["형식 흔들림", "최신 규정 오류", "계산 오류", "문체 불안정"],
        "columns": ["프롬프트", "RAG", "도구 사용", "파인튜닝"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "solution-selection-score-map-en.png",
        "title": "Solution score by failure type",
        "rows": ["format drift", "missing policy", "calculation error", "style drift"],
        "columns": ["prompt", "RAG", "tool use", "fine-tuning"],
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
    cmap = LinearSegmentedColormap.from_list(
        "selection_score",
        ["#f8fafc", "#bfdbfe", "#2563eb"],
    )

    fig, ax = plt.subplots(figsize=(7.0, 4.0), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.imshow(SCORES, cmap=cmap, vmin=0, vmax=10, aspect="auto")

    ax.set_title(text["title"], fontsize=12, pad=14, fontweight="bold")
    ax.set_xticks(range(len(text["columns"])), text["columns"])
    ax.set_yticks(range(len(text["rows"])), text["rows"])
    ax.tick_params(axis="x", labelsize=9, pad=8)
    ax.tick_params(axis="y", labelsize=9)

    ax.set_xticks([index - 0.5 for index in range(1, len(text["columns"]))], minor=True)
    ax.set_yticks([index - 0.5 for index in range(1, len(text["rows"]))], minor=True)
    ax.grid(which="minor", color="white", linewidth=2.0)
    ax.tick_params(which="minor", bottom=False, left=False)

    for row_index, row in enumerate(SCORES):
        row_max = max(row)
        for col_index, value in enumerate(row):
            ax.text(
                col_index,
                row_index,
                str(value),
                ha="center",
                va="center",
                color="white" if value == row_max and value >= 9 else "#172033",
                fontsize=9,
                fontweight="bold" if value == row_max else "normal",
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
