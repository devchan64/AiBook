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

SUMMARY = {
    "prompt_only": {
        "fully_passed": 0,
        "total_passed_checks": 0,
    },
    "structured": {
        "fully_passed": 3,
        "total_passed_checks": 9,
    },
    "total_tasks": 3,
    "total_checks": 9,
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
        "outfile": "prompt-limit-checks-ko.png",
        "ylabel": "통과 수",
        "prompt_only_label": "강한 프롬프트만",
        "structured_label": "구조 보강",
        "labels": ["전체 통과 작업", "통과한 검사"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "prompt-limit-checks-en.png",
        "ylabel": "passed count",
        "prompt_only_label": "prompt only",
        "structured_label": "structured support",
        "labels": ["fully passed tasks", "passed checks"],
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK TC",
            "PingFang SC",
            "Microsoft YaHei",
            "SimHei",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "prompt-limit-checks-zh.png",
        "ylabel": "通过数",
        "prompt_only_label": "只靠强提示",
        "structured_label": "结构补强",
        "labels": ["完全通过的任务", "通过的检查"],
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


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_chart(text: dict[str, str]) -> None:
    configure_font(text)
    labels = text["labels"]
    prompt_only_values = [
        SUMMARY["prompt_only"]["fully_passed"],
        SUMMARY["prompt_only"]["total_passed_checks"],
    ]
    structured_values = [
        SUMMARY["structured"]["fully_passed"],
        SUMMARY["structured"]["total_passed_checks"],
    ]
    x_positions = list(range(len(labels)))
    bar_width = 0.34

    fig, ax = plt.subplots(figsize=(6.4, 3.8), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    prompt_only_bars = ax.bar(
        [x - bar_width / 2 for x in x_positions],
        prompt_only_values,
        width=bar_width,
        color="#64748b",
        label=text["prompt_only_label"],
    )
    structured_bars = ax.bar(
        [x + bar_width / 2 for x in x_positions],
        structured_values,
        width=bar_width,
        color="#2563eb",
        label=text["structured_label"],
    )

    for bars in (prompt_only_bars, structured_bars):
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

    ax.set_xticks(x_positions)
    ax.set_xticklabels(labels)
    ax.set_ylabel(text["ylabel"])
    ax.set_ylim(0, SUMMARY["total_checks"] * 1.2)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
