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

CANDIDATE_AVERAGES = {
    "direct_but_risky": {"helpfulness": 2.0, "safety": 0.67, "factuality": 0.0},
    "safe_but_thin": {"helpfulness": 1.33, "safety": 2.0, "factuality": 1.0},
    "balanced": {"helpfulness": 3.0, "safety": 3.0, "factuality": 2.0},
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
        "outfile": "alignment-axis-average-ko.png",
        "title": "후보 유형별 평균 평가 축",
        "ylabel": "평균 점수",
        "candidate_labels": {
            "direct_but_risky": "직접적이지만 위험",
            "safe_but_thin": "안전하지만 빈약",
            "balanced": "균형 잡힌 답",
        },
        "axis_labels": {
            "helpfulness": "유용성",
            "safety": "안전성",
            "factuality": "사실성",
        },
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "alignment-axis-average-en.png",
        "title": "Average alignment axes by candidate type",
        "ylabel": "average score",
        "candidate_labels": {
            "direct_but_risky": "direct but risky",
            "safe_but_thin": "safe but thin",
            "balanced": "balanced",
        },
        "axis_labels": {
            "helpfulness": "helpfulness",
            "safety": "safety",
            "factuality": "factuality",
        },
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
    candidate_keys = list(CANDIDATE_AVERAGES.keys())
    axis_keys = ["helpfulness", "safety", "factuality"]
    colors = {
        "helpfulness": "#2563eb",
        "safety": "#16a34a",
        "factuality": "#f59e0b",
    }

    fig, ax = plt.subplots(figsize=(7.2, 4.0), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    x_positions = list(range(len(candidate_keys)))
    bar_width = 0.23
    offsets = [-bar_width, 0, bar_width]

    for axis_key, offset in zip(axis_keys, offsets):
        values = [CANDIDATE_AVERAGES[candidate][axis_key] for candidate in candidate_keys]
        bars = ax.bar(
            [x + offset for x in x_positions],
            values,
            width=bar_width,
            color=colors[axis_key],
            label=text["axis_labels"][axis_key],
        )
        for bar, value in zip(bars, values):
            ax.annotate(
                f"{value:.2f}".rstrip("0").rstrip("."),
                (bar.get_x() + bar.get_width() / 2, value),
                textcoords="offset points",
                xytext=(0, 5),
                ha="center",
                fontsize=8.5,
                color="#172033",
            )

    ax.set_title(text["title"], fontsize=12, pad=14, fontweight="bold")
    ax.set_ylabel(text["ylabel"])
    ax.set_xticks(x_positions, [text["candidate_labels"][key] for key in candidate_keys])
    ax.set_ylim(0, 3.45)
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=False, loc="upper left", ncol=3)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
