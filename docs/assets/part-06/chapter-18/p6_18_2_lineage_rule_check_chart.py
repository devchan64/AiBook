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

ITEMS = [
    {"name": "language modeling", "checks": [True, True, True]},
    {"name": "embeddings", "checks": [True, True, True]},
    {"name": "attention", "checks": [True, True, True]},
    {"name": "Transformer", "checks": [True, True, True]},
    {"name": "YOLO", "checks": [False, False, False]},
    {"name": "Deep Voice", "checks": [False, False, False]},
    {"name": "GPU scaling", "checks": [False, False, False]},
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
        "outfile": "lineage-rule-check-matrix-ko.png",
        "checks": ["언어 도메인", "LLM 목표", "Transformer 연결"],
        "pass": "통과",
        "fail": "미통과",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "lineage-rule-check-matrix-en.png",
        "checks": ["language domain", "LLM target", "Transformer link"],
        "pass": "pass",
        "fail": "fail",
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
    matrix = [[1 if ok else 0 for ok in item["checks"]] for item in ITEMS]
    item_names = [item["name"] for item in ITEMS]
    cmap = ListedColormap(["#dc2626", "#0f766e"])

    fig, ax = plt.subplots(figsize=(8.6, 4.7), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.imshow(matrix, cmap=cmap, vmin=0, vmax=1, aspect="auto")

    ax.set_xticks(range(len(text["checks"])))
    ax.set_xticklabels(text["checks"])
    ax.set_yticks(range(len(item_names)))
    ax.set_yticklabels(item_names)
    ax.tick_params(axis="x", labelsize=8.8, pad=8)
    ax.tick_params(axis="y", labelsize=8.4)

    ax.set_xticks([index - 0.5 for index in range(1, len(text["checks"]))], minor=True)
    ax.set_yticks([index - 0.5 for index in range(1, len(item_names))], minor=True)
    ax.grid(which="minor", color="white", linewidth=2.2)
    ax.tick_params(which="minor", bottom=False, left=False)

    for row_index, row in enumerate(matrix):
        for col_index, ok in enumerate(row):
            ax.text(
                col_index,
                row_index,
                text["pass"] if ok else text["fail"],
                ha="center",
                va="center",
                color="white",
                fontsize=8,
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
