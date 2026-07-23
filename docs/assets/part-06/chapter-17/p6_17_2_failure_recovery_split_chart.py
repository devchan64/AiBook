import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
MPL_CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))
os.environ.setdefault("XDG_CACHE_HOME", str(MPL_CACHE))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

from p6_17_2_evaluate_failure_recovery import load_reports, summarize_reports

OUT_DIR = Path(__file__).resolve().parent

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
        "outfile": "failure-recovery-routing-ko.png",
        "left_title": "실패 계열",
        "right_title": "복구 결정",
        "family_labels": ["시스템 실패", "모델 실패"],
        "decision_labels": ["재시도", "대체 경로", "승인", "사람 검토", "중단·상향", "모델 수정"],
        "xlabel": "사례 수",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "failure-recovery-routing-en.png",
        "left_title": "Failure family",
        "right_title": "Recovery decision",
        "family_labels": ["system failure", "model failure"],
        "decision_labels": ["retry", "fallback", "approval", "human review", "stop/escalate", "model fix"],
        "xlabel": "cases",
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


def style_axis(ax) -> None:
    ax.grid(True, axis="x", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def annotate_bars(ax, bars, total: int) -> None:
    for bar in bars:
        value = bar.get_width()
        ax.annotate(
            f"{value:g} ({value / total:.0%})",
            (value, bar.get_y() + bar.get_height() / 2),
            textcoords="offset points",
            xytext=(7, 0),
            va="center",
            fontsize=8.4,
            color="#172033",
        )


def save_chart(text: dict[str, object]) -> None:
    configure_font(text)
    summary = summarize_reports(load_reports())

    family_values = [
        summary["system_failure_count"],
        summary["model_failure_count"],
    ]
    decision_values = [
        summary["retry_count"],
        summary["fallback_count"],
        summary["approval_count"],
        summary["human_review_count"],
        summary["stop_and_escalate_count"],
        summary["model_fix_count"],
    ]

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(9.4, 4.1),
        dpi=180,
        gridspec_kw={"width_ratios": [0.86, 1.34], "wspace": 0.42},
        constrained_layout=True,
    )
    fig.patch.set_facecolor("white")

    family_colors = ["#2563eb", "#f59e0b"]
    decision_colors = ["#0f766e", "#64748b", "#f59e0b", "#9333ea", "#dc2626", "#2563eb"]

    for ax in axes:
        ax.set_facecolor("white")
        style_axis(ax)
        ax.set_xlabel(text["xlabel"])
        ax.set_xlim(0, summary["case_count"] * 0.62)

    family_bars = axes[0].barh(text["family_labels"], family_values, color=family_colors, height=0.48)
    axes[0].invert_yaxis()
    axes[0].set_title(text["left_title"], fontsize=11, pad=8)
    annotate_bars(axes[0], family_bars, summary["case_count"])

    decision_bars = axes[1].barh(text["decision_labels"], decision_values, color=decision_colors, height=0.48)
    axes[1].invert_yaxis()
    axes[1].set_title(text["right_title"], fontsize=11, pad=8)
    annotate_bars(axes[1], decision_bars, summary["case_count"])

    for ax in axes:
        ax.tick_params(axis="y", labelsize=8.6)

    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
