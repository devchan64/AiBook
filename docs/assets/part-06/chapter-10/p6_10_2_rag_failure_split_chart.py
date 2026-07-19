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
    "retrieval_failure_count": 1,
    "generation_failure_count": 1,
    "irrelevant_leak_count": 1,
    "overclaim_count": 1,
    "payload_count": 3,
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
        "outfile": "rag-failure-split-ko.png",
        "ylabel": "감지된 실험 수",
        "labels": ["검색 실패", "생성 실패", "무관 내용\n누출", "과장 표현"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "rag-failure-split-en.png",
        "ylabel": "detected payloads",
        "labels": ["retrieval\nfailure", "generation\nfailure", "irrelevant\nleak", "overclaim"],
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
    values = [
        SUMMARY["retrieval_failure_count"],
        SUMMARY["generation_failure_count"],
        SUMMARY["irrelevant_leak_count"],
        SUMMARY["overclaim_count"],
    ]
    colors = ["#dc2626", "#2563eb", "#f59e0b", "#9333ea"]

    fig, ax = plt.subplots(figsize=(6.8, 3.9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    bars = ax.bar(text["labels"], values, color=colors, width=0.54)
    for bar in bars:
        value = bar.get_height()
        ax.annotate(
            f"{value:g}",
            (bar.get_x() + bar.get_width() / 2, value),
            textcoords="offset points",
            xytext=(0, 7),
            ha="center",
            fontsize=9,
            color="#172033",
        )

    ax.set_ylabel(text["ylabel"])
    ax.set_ylim(0, SUMMARY["payload_count"] * 1.25)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
