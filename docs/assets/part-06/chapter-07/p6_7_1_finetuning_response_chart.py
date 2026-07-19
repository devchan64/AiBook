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
    "base_label_match_count": 3,
    "tuned_label_match_count": 4,
    "base_format_ok_count": 0,
    "tuned_format_ok_count": 4,
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
        "outfile": "finetuning-response-check-ko.png",
        "xlabel": "점검 항목",
        "ylabel": "통과한 문의 수",
        "base_label": "일반 설명형",
        "tuned_label": "업무 형식 응답",
        "labels": ["라벨 일치", "형식 통과"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "finetuning-response-check-en.png",
        "xlabel": "check item",
        "ylabel": "passed queries",
        "base_label": "general response",
        "tuned_label": "task-form response",
        "labels": ["label match", "format pass"],
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
    base_values = [SUMMARY["base_label_match_count"], SUMMARY["base_format_ok_count"]]
    tuned_values = [SUMMARY["tuned_label_match_count"], SUMMARY["tuned_format_ok_count"]]
    x_positions = list(range(len(labels)))
    bar_width = 0.34

    fig, ax = plt.subplots(figsize=(6.4, 3.8), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    base_bars = ax.bar(
        [x - bar_width / 2 for x in x_positions],
        base_values,
        width=bar_width,
        color="#64748b",
        label=text["base_label"],
    )
    tuned_bars = ax.bar(
        [x + bar_width / 2 for x in x_positions],
        tuned_values,
        width=bar_width,
        color="#2563eb",
        label=text["tuned_label"],
    )

    for bars in (base_bars, tuned_bars):
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
    ax.set_xlabel(text["xlabel"])
    ax.set_ylabel(text["ylabel"])
    ax.set_ylim(0, 4.8)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
