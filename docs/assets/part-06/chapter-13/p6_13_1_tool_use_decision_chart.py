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
    "no_tool_count": 3,
    "lookup_count": 5,
    "lookup_compute_count": 2,
    "compute_count": 2,
    "approval_pending_count": 3,
    "missing_info_count": 3,
    "tool_executed_count": 9,
    "skipped_tool_count": 3,
    "guard_changed_model_route_count": 4,
    "request_count": 18,
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
        "outfile": "tool-use-decision-check-ko.png",
        "route_ylabel": "최종 route 수",
        "outcome_ylabel": "해당 요청 수",
        "route_labels": ["설명만\n필요", "조회\n필요", "조회+계산", "계산\n필요", "승인\n대기", "정보\n부족"],
        "outcome_labels": ["도구\n실행", "설명으로\n종료", "승인\n대기", "정보\n부족", "guard\n보정"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "tool-use-decision-check-en.png",
        "route_ylabel": "final routes",
        "outcome_ylabel": "matching requests",
        "route_labels": ["no tool", "lookup", "lookup+\ncompute", "compute", "approval\npending", "missing\ninfo"],
        "outcome_labels": ["tool\nexecuted", "no tool\nanswer", "approval\npending", "missing\ninfo", "guard\ncorrected"],
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
    route_values = [
        SUMMARY["no_tool_count"],
        SUMMARY["lookup_count"],
        SUMMARY["lookup_compute_count"],
        SUMMARY["compute_count"],
        SUMMARY["approval_pending_count"],
        SUMMARY["missing_info_count"],
    ]
    outcome_values = [
        SUMMARY["tool_executed_count"],
        SUMMARY["skipped_tool_count"],
        SUMMARY["approval_pending_count"],
        SUMMARY["missing_info_count"],
        SUMMARY["guard_changed_model_route_count"],
    ]
    route_colors = ["#64748b", "#2563eb", "#0f766e", "#9333ea", "#f59e0b", "#dc2626"]
    outcome_colors = ["#0f766e", "#64748b", "#f59e0b", "#dc2626", "#7c3aed"]

    fig, (route_ax, outcome_ax) = plt.subplots(
        1,
        2,
        figsize=(10.8, 4.0),
        dpi=180,
        gridspec_kw={"width_ratios": [1.25, 1]},
    )
    fig.patch.set_facecolor("white")
    for ax in (route_ax, outcome_ax):
        ax.set_facecolor("white")
        style_axis(ax)

    for ax, labels, values, colors in [
        (route_ax, text["route_labels"], route_values, route_colors),
        (outcome_ax, text["outcome_labels"], outcome_values, outcome_colors),
    ]:
        bars = ax.bar(labels, values, color=colors, width=0.58)
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

    route_ax.set_ylabel(text["route_ylabel"])
    outcome_ax.set_ylabel(text["outcome_ylabel"])
    route_ax.set_ylim(0, max(max(route_values) * 1.45, 6))
    outcome_ax.set_ylim(0, max(max(outcome_values) * 1.32, 10))
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
