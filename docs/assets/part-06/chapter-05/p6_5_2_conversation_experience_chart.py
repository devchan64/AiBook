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
from matplotlib import colors, font_manager

OUT_DIR = Path(__file__).resolve().parent

EXPERIENCE_RESULTS = {
    "autocomplete": {
        "format_followed": False,
        "role_followed": False,
        "safety_ok": False,
        "structured_response": False,
    },
    "instruction": {
        "format_followed": True,
        "role_followed": True,
        "safety_ok": True,
        "structured_response": True,
    },
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
        "outfile": "conversation-experience-criteria-ko.png",
        "row_labels": ["자동완성형", "지시 응답형"],
        "column_labels": ["형식 준수", "역할 반영", "안전 조건", "구조화"],
        "met": "충족",
        "not_met": "미충족",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "conversation-experience-criteria-en.png",
        "row_labels": ["autocomplete", "instruction response"],
        "column_labels": ["format", "role", "safety", "structure"],
        "met": "met",
        "not_met": "not met",
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK KR",
            "PingFang SC",
            "Heiti SC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "conversation-experience-criteria-zh.png",
        "row_labels": ["自动补全型", "指令回应型"],
        "column_labels": ["格式遵守", "角色反映", "安全条件", "结构化"],
        "met": "满足",
        "not_met": "未满足",
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


def matrix_values() -> list[list[int]]:
    keys = ["format_followed", "role_followed", "safety_ok", "structured_response"]
    return [
        [int(EXPERIENCE_RESULTS["autocomplete"][key]) for key in keys],
        [int(EXPERIENCE_RESULTS["instruction"][key]) for key in keys],
    ]


def save_experience_chart(text: dict[str, str]) -> None:
    configure_font(text)
    values = matrix_values()
    cmap = colors.ListedColormap(["#f3f4f6", "#2563eb"])
    norm = colors.BoundaryNorm([-0.5, 0.5, 1.5], cmap.N)

    fig, ax = plt.subplots(figsize=(6.4, 2.7), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.imshow(values, cmap=cmap, norm=norm, aspect="auto")

    ax.set_xticks(range(len(text["column_labels"])), text["column_labels"])
    ax.set_yticks(range(len(text["row_labels"])), text["row_labels"])
    ax.tick_params(axis="both", length=0)
    ax.set_xticks([x - 0.5 for x in range(1, len(text["column_labels"]))], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, len(text["row_labels"]))], minor=True)
    ax.grid(which="minor", color="white", linewidth=3)

    for row_index, row in enumerate(values):
        for col_index, value in enumerate(row):
            ax.text(
                col_index,
                row_index,
                text["met"] if value else text["not_met"],
                ha="center",
                va="center",
                color="white" if value else "#172033",
                fontsize=10,
            )

    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.tight_layout(pad=0.8)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_experience_chart(text)


if __name__ == "__main__":
    main()
