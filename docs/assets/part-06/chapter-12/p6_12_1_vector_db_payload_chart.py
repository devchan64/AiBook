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

SIMILARITY = {
    "refund_question": {"top1": 0.9978, "runner_up": 0.2845},
    "settings_question": {"top1": 0.9988, "runner_up": 0.3181},
    "api_limit_question": {"top1": 0.9994, "runner_up": 0.3342},
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
        "outfile": "vector-db-payload-check-ko.png",
        "ylabel": "코사인 유사도",
        "top1_label": "1위 후보",
        "runner_up_label": "다음 후보",
        "labels": ["환불 질문", "설정 질문", "API 제한 질문"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "vector-db-payload-check-en.png",
        "ylabel": "cosine similarity",
        "top1_label": "top-1 match",
        "runner_up_label": "runner-up",
        "labels": ["refund query", "settings query", "API limit query"],
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
    top1_values = [item["top1"] for item in SIMILARITY.values()]
    runner_up_values = [item["runner_up"] for item in SIMILARITY.values()]
    positions = list(range(len(labels)))
    bar_width = 0.34

    fig, ax = plt.subplots(figsize=(7.2, 3.9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    top1_bars = ax.bar(
        [x - bar_width / 2 for x in positions],
        top1_values,
        width=bar_width,
        color="#2563eb",
        label=text["top1_label"],
    )
    runner_up_bars = ax.bar(
        [x + bar_width / 2 for x in positions],
        runner_up_values,
        width=bar_width,
        color="#64748b",
        label=text["runner_up_label"],
    )
    for bars in (top1_bars, runner_up_bars):
        for bar in bars:
            value = bar.get_height()
            ax.annotate(
                f"{value:.2f}",
                (bar.get_x() + bar.get_width() / 2, value),
                textcoords="offset points",
                xytext=(0, 7),
                ha="center",
                fontsize=9,
                color="#172033",
            )

    ax.set_xticks(positions)
    ax.set_xticklabels(labels)
    ax.set_ylabel(text["ylabel"])
    ax.set_ylim(0, 1.18)
    ax.legend(frameon=False, loc="upper center", ncol=2, bbox_to_anchor=(0.5, -0.14))
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
