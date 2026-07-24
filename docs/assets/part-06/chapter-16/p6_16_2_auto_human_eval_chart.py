from pathlib import Path
import os
import sys

REPO_ROOT = Path(__file__).resolve().parents[4]
MPL_CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))
os.environ.setdefault("XDG_CACHE_HOME", str(MPL_CACHE))

OUT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT_DIR))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib import font_manager

from p6_16_2_eval_routing_cases import load_reports, summarize_reports

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
        "outfile": "auto-human-eval-routing-ko.png",
        "ylabel": "해당 후보 수",
        "gate_label": "자동 채점기",
        "route_label": "검토 준비",
        "legend": ["채점기 통과", "자동 수정 필요", "사람 검토 큐"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "auto-human-eval-routing-en.png",
        "ylabel": "matching candidates",
        "gate_label": "automatic grader",
        "route_label": "review prep",
        "legend": ["grader pass", "auto fix needed", "human review queue"],
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
    ax.grid(True, axis="x", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_chart(text: dict[str, str], summary: dict[str, object]) -> None:
    configure_font(text)
    gate_values = [
        int(summary["auto_pass_count"]),
        int(summary["auto_fail_count"]),
        0,
    ]
    route_values = [
        0,
        int(summary["automatic_fix_first_count"]),
        int(summary["human_review_queue_count"]),
    ]
    answer_count = int(summary["case_count"])
    colors = ["#2563eb", "#64748b", "#9333ea"]

    fig, ax = plt.subplots(figsize=(8.6, 3.9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    y_positions = [1, 0]
    for row_index, values in enumerate([gate_values, route_values]):
        left = 0
        for value, color, label in zip(values, colors, text["legend"]):
            if value == 0:
                continue
            ax.barh(y_positions[row_index], value, left=left, color=color, height=0.46)
            ax.annotate(
                f"{value:g}\n({value / answer_count:.0%})",
                (left + value / 2, y_positions[row_index]),
                ha="center",
                va="center",
                fontsize=8.5,
                color="white",
            )
            left += value

    ax.set_yticks(y_positions, [text["gate_label"], text["route_label"]])
    ax.set_xlabel(text["ylabel"])
    ax.set_xlim(0, answer_count)
    ax.tick_params(axis="y", labelsize=10)
    legend_handles = [
        Patch(facecolor=color, label=label)
        for color, label in zip(colors, text["legend"])
    ]
    ax.legend(
        handles=legend_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.16),
        ncol=4,
        frameon=False,
    )
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    summary = summarize_reports(load_reports())
    for text in LANG_TEXT.values():
        save_chart(text, summary)


if __name__ == "__main__":
    main()
