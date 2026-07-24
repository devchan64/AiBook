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

from p6_17_1_evaluate_service_candidates import load_reports

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
        "outfile": "service-constraint-matrix-ko.png",
        "checks": ["품질", "지연 시간", "비용", "처리량", "운영 후보"],
        "pass": "통과",
        "fail": "탈락",
        "ylabel": "후보 수",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "service-constraint-matrix-en.png",
        "checks": ["quality", "latency", "cost", "throughput", "operational"],
        "pass": "pass",
        "fail": "fail",
        "ylabel": "candidate count",
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
        "outfile": "service-constraint-matrix-zh.png",
        "checks": ["质量", "延迟", "成本", "处理量", "运营候选"],
        "pass": "通过",
        "fail": "未通过",
        "ylabel": "候选数",
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


def count_by_check(reports: list[dict[str, object]]) -> tuple[list[int], list[int]]:
    checks = [
        "quality_ok",
        "latency_ok",
        "cost_ok",
        "throughput_ok",
        "operationally_acceptable",
    ]
    pass_counts = [sum(1 for report in reports if report[check]) for check in checks]
    fail_counts = [len(reports) - count for count in pass_counts]
    return pass_counts, fail_counts


def save_chart(text: dict[str, object]) -> None:
    configure_font(text)
    reports = load_reports()
    pass_counts, fail_counts = count_by_check(reports)
    x_positions = list(range(len(text["checks"])))

    fig, ax = plt.subplots(figsize=(8.9, 4.2), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    pass_color = "#0f766e"
    fail_color = "#d1d5db"
    ax.bar(x_positions, pass_counts, color=pass_color, width=0.58, label=text["pass"])
    ax.bar(
        x_positions,
        fail_counts,
        bottom=pass_counts,
        color=fail_color,
        width=0.58,
        label=text["fail"],
    )

    ax.set_xticks(range(len(text["checks"])))
    ax.set_xticklabels(text["checks"])
    ax.set_ylabel(text["ylabel"])
    ax.set_ylim(0, len(reports) + 4)
    ax.grid(axis="y", color="#cbd5e1", linewidth=0.8, alpha=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize=9, pad=8)
    ax.tick_params(axis="y", labelsize=8.7)
    ax.legend(loc="upper left", frameon=False, ncols=2, bbox_to_anchor=(0, 1.08))

    for index, (pass_count, fail_count) in enumerate(zip(pass_counts, fail_counts)):
        ax.text(
            index,
            pass_count / 2,
            str(pass_count),
            ha="center",
            va="center",
            color="white",
            fontsize=9,
            fontweight="bold",
        )
        if fail_count:
            ax.text(
                index,
                pass_count + fail_count / 2,
                str(fail_count),
                ha="center",
                va="center",
                color="#334155",
                fontsize=9,
                fontweight="bold",
            )

    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
