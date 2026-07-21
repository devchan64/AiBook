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
    "simple": {
        "format_ok_count": 0,
        "slot_ok_count": 0,
        "full_keyword_keep_count": 0,
    },
    "structured": {
        "format_ok_count": 3,
        "slot_ok_count": 3,
        "full_keyword_keep_count": 1,
    },
    "request_count": 3,
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
        "outfile": "prompt-structure-check-ko.png",
        "ylabel": "통과한 요청 카드 수",
        "simple_label": "단순 프롬프트",
        "structured_label": "구조화 프롬프트",
        "labels": ["번호 형식", "필수 슬롯", "핵심 키워드"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "prompt-structure-check-en.png",
        "ylabel": "passed request cards",
        "simple_label": "simple prompt",
        "structured_label": "structured prompt",
        "labels": ["numbered format", "required slots", "key facts"],
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
    simple_values = [
        SUMMARY["simple"]["format_ok_count"],
        SUMMARY["simple"]["slot_ok_count"],
        SUMMARY["simple"]["full_keyword_keep_count"],
    ]
    structured_values = [
        SUMMARY["structured"]["format_ok_count"],
        SUMMARY["structured"]["slot_ok_count"],
        SUMMARY["structured"]["full_keyword_keep_count"],
    ]
    x_positions = list(range(len(labels)))
    bar_width = 0.34

    fig, ax = plt.subplots(figsize=(6.8, 3.9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    simple_bars = ax.bar(
        [x - bar_width / 2 for x in x_positions],
        simple_values,
        width=bar_width,
        color="#64748b",
        label=text["simple_label"],
    )
    structured_bars = ax.bar(
        [x + bar_width / 2 for x in x_positions],
        structured_values,
        width=bar_width,
        color="#2563eb",
        label=text["structured_label"],
    )

    for bars in (simple_bars, structured_bars):
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
    ax.set_ylim(0, SUMMARY["request_count"] * 1.25)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
