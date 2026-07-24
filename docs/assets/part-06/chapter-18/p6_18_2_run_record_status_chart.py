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

from p6_18_2_generate_run_records import (
    load_run_records as load_run_records_ko,
    summarize_records as summarize_records_ko,
)
from p6_18_2_generate_run_records_en import (
    load_run_records as load_run_records_en,
    summarize_records as summarize_records_en,
)
from p6_18_2_generate_run_records_zh import (
    load_run_records as load_run_records_zh,
    summarize_records as summarize_records_zh,
)

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
        "outfile": "run-record-status-summary-ko.png",
        "ylabel": "요청 수",
        "status_title": "실행 상태",
        "review_title": "사람 검토",
        "status_labels": ["다중 근거", "근거 부족", "문서 미회수"],
        "review_labels": ["검토 필요", "자동 초안"],
        "load_run_records": load_run_records_ko,
        "summarize_records": summarize_records_ko,
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "run-record-status-summary-en.png",
        "ylabel": "requests",
        "status_title": "Run status",
        "review_title": "Human review",
        "status_labels": ["multi evidence", "single evidence", "retrieval failed"],
        "review_labels": ["needs review", "auto draft"],
        "load_run_records": load_run_records_en,
        "summarize_records": summarize_records_en,
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK",
            "PingFang SC",
            "Heiti SC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "run-record-status-summary-zh.png",
        "ylabel": "请求数",
        "status_title": "执行状态",
        "review_title": "人工审查",
        "status_labels": ["多重依据", "单一依据", "检索失败"],
        "review_labels": ["需要审查", "自动草稿"],
        "load_run_records": load_run_records_zh,
        "summarize_records": summarize_records_zh,
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
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_chart(text: dict[str, object]) -> None:
    configure_font(text)
    summary = text["summarize_records"](text["load_run_records"]())
    status_values = [
        summary["multi_evidence_count"],
        summary["single_evidence_count"],
        summary["retrieval_failed_count"],
    ]
    review_values = [
        summary["needs_human_review_count"],
        summary["run_count"] - summary["needs_human_review_count"],
    ]
    status_colors = ["#0f766e", "#f59e0b", "#dc2626"]
    review_colors = ["#9333ea", "#64748b"]

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(9.2, 3.8),
        dpi=180,
        gridspec_kw={"width_ratios": [1.35, 1]},
        constrained_layout=True,
    )
    fig.patch.set_facecolor("white")

    for ax in axes:
        ax.set_facecolor("white")
        style_axis(ax)
        ax.set_ylabel(text["ylabel"])
        ax.set_ylim(0, summary["run_count"] * 1.08)
        ax.tick_params(axis="x", labelsize=8.7)

    status_bars = axes[0].bar(
        text["status_labels"], status_values, color=status_colors, width=0.56
    )
    review_bars = axes[1].bar(
        text["review_labels"], review_values, color=review_colors, width=0.56
    )
    axes[0].set_title(text["status_title"], fontsize=10, pad=8)
    axes[1].set_title(text["review_title"], fontsize=10, pad=8)

    for bars in (status_bars, review_bars):
        for bar in bars:
            value = bar.get_height()
            bar.axes.annotate(
                f"{value:g}\n({value / summary['run_count']:.0%})",
                (bar.get_x() + bar.get_width() / 2, value),
                textcoords="offset points",
                xytext=(0, 7),
                ha="center",
                fontsize=8.7,
                color="#172033",
            )

    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
