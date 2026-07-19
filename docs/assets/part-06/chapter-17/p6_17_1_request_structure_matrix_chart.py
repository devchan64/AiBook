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

REQUESTS = [
    {
        "key": "polish_notice",
        "structure": {"prompt": True, "retrieval": False, "tool": False, "human_review": False},
    },
    {
        "key": "parental_leave",
        "structure": {"prompt": True, "retrieval": True, "tool": False, "human_review": False},
    },
    {
        "key": "vacation_balance",
        "structure": {"prompt": True, "retrieval": False, "tool": True, "human_review": False},
    },
    {
        "key": "benefit_points",
        "structure": {"prompt": True, "retrieval": True, "tool": False, "human_review": True},
    },
]

STRUCTURE_KEYS = ["prompt", "retrieval", "tool", "human_review"]

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
        "outfile": "request-structure-matrix-ko.png",
        "request_labels": ["문장 다듬기", "육아휴직 순서", "잔여 휴가", "복지포인트"],
        "structure_labels": ["prompt", "retrieval", "tool use", "사람 검토"],
        "needed": "필요",
        "not_needed": "불필요",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "request-structure-matrix-en.png",
        "request_labels": ["polish notice", "leave policy", "vacation balance", "benefit points"],
        "structure_labels": ["prompt", "retrieval", "tool use", "human review"],
        "needed": "needed",
        "not_needed": "skip",
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
    matrix = [
        [1 if request["structure"][key] else 0 for key in STRUCTURE_KEYS]
        for request in REQUESTS
    ]
    cmap = ListedColormap(["#e2e8f0", "#0f766e"])

    fig, ax = plt.subplots(figsize=(8.8, 3.9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.imshow(matrix, cmap=cmap, vmin=0, vmax=1, aspect="auto")

    ax.set_xticks(range(len(text["structure_labels"])))
    ax.set_xticklabels(text["structure_labels"])
    ax.set_yticks(range(len(text["request_labels"])))
    ax.set_yticklabels(text["request_labels"])
    ax.tick_params(axis="x", labelsize=9, pad=8)
    ax.tick_params(axis="y", labelsize=8.8)

    ax.set_xticks([index - 0.5 for index in range(1, len(STRUCTURE_KEYS))], minor=True)
    ax.set_yticks([index - 0.5 for index in range(1, len(REQUESTS))], minor=True)
    ax.grid(which="minor", color="white", linewidth=2.2)
    ax.tick_params(which="minor", bottom=False, left=False)

    for row_index, row in enumerate(matrix):
        for col_index, required in enumerate(row):
            ax.text(
                col_index,
                row_index,
                text["needed"] if required else text["not_needed"],
                ha="center",
                va="center",
                color="white" if required else "#334155",
                fontsize=8.2,
                fontweight="bold" if required else "normal",
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
