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

SCORES = [40, 45, 48, 50, 52, 55, 58, 60, 62, 90]
LOW_VARIANCE = [4, 5, 6, 7, 8]
HIGH_VARIANCE = [0, 2, 6, 10, 12]

LANG_TEXT = {
    "ko": {
        "font_candidates": ["Apple SD Gothic Neo", "AppleGothic", "Arial Unicode MS", "DejaVu Sans"],
        "value_label": "값",
        "count_label": "개수",
        "mean_label": "평균",
        "spread_label": "퍼짐",
        "outlier_label": "튀는 값",
        "group_label": "데이터 묶음",
        "low_label": "A: 낮은 분산",
        "high_label": "B: 높은 분산",
        "variance_label": "분산",
        "summary_outfile": "distribution-mean-variance-summary-ko.png",
        "variance_outfile": "same-mean-different-variance-ko.png",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "value_label": "value",
        "count_label": "count",
        "mean_label": "mean",
        "spread_label": "spread",
        "outlier_label": "outlier",
        "group_label": "data bundle",
        "low_label": "A: low variance",
        "high_label": "B: high variance",
        "variance_label": "variance",
        "summary_outfile": "distribution-mean-variance-summary-en.png",
        "variance_outfile": "same-mean-different-variance-en.png",
    },
    "zh": {
        "font_candidates": ["Arial Unicode MS", "Heiti TC", "PingFang SC", "DejaVu Sans"],
        "value_label": "值",
        "count_label": "个数",
        "mean_label": "均值",
        "spread_label": "扩散",
        "outlier_label": "离群值",
        "group_label": "数据组",
        "low_label": "A: 低方差",
        "high_label": "B: 高方差",
        "variance_label": "方差",
        "summary_outfile": "distribution-mean-variance-summary-zh.png",
        "variance_outfile": "same-mean-different-variance-zh.png",
    },
}


def choose_font(candidates: list[str]) -> str:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def variance(values: list[float]) -> float:
    center = mean(values)
    return sum((value - center) ** 2 for value in values) / len(values)


def save_distribution_summary(text: dict[str, object]) -> None:
    avg = mean(SCORES)
    low_band = avg - 10
    high_band = avg + 10

    fig, ax = plt.subplots(figsize=(7.4, 3.25), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    bins = [35, 45, 55, 65, 75, 85, 95]
    ax.hist(SCORES, bins=bins, color="#ddf4ff", edgecolor="#0969da", linewidth=1.1)
    ax.axvspan(low_band, high_band, color="#dafbe1", alpha=0.55, zorder=0)
    ax.axvline(avg, color="#cf222e", linestyle=(0, (5, 4)), linewidth=1.5)

    ax.annotate(
        f"{text['mean_label']} {avg:.0f}",
        xy=(avg, 3.0),
        xytext=(avg + 4, 3.35),
        ha="left",
        va="center",
        fontsize=9.2,
        color="#cf222e",
        arrowprops={"arrowstyle": "-|>", "color": "#cf222e", "linewidth": 0.9},
        bbox={"boxstyle": "round,pad=0.2", "facecolor": "white", "edgecolor": "#cf222e", "linewidth": 0.8},
    )
    ax.annotate(
        text["spread_label"],
        xy=(avg, 0.55),
        ha="center",
        va="center",
        fontsize=9.2,
        color="#116329",
        bbox={"boxstyle": "round,pad=0.22", "facecolor": "white", "edgecolor": "#1a7f37", "linewidth": 0.8},
    )
    ax.annotate(
        text["outlier_label"],
        xy=(90, 0.4),
        xytext=(82, 1.15),
        ha="center",
        va="center",
        fontsize=9.2,
        color="#8250df",
        arrowprops={"arrowstyle": "-|>", "color": "#8250df", "linewidth": 0.9},
        bbox={"boxstyle": "round,pad=0.2", "facecolor": "white", "edgecolor": "#8250df", "linewidth": 0.8},
    )

    ax.set_xlabel(text["value_label"])
    ax.set_ylabel(text["count_label"])
    ax.set_xlim(35, 95)
    ax.set_ylim(0, 4.0)
    ax.set_xticks([40, 50, 60, 70, 80, 90])
    ax.set_yticks([0, 1, 2, 3, 4])
    ax.grid(axis="y", color="#d0d7de", linewidth=0.7, alpha=0.75)

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    fig.tight_layout(pad=0.8)
    fig.savefig(OUT_DIR / text["summary_outfile"])
    plt.close(fig)


def save_same_mean_variance(text: dict[str, object]) -> None:
    datasets = [(text["low_label"], LOW_VARIANCE, "#0969da"), (text["high_label"], HIGH_VARIANCE, "#8250df")]

    fig, ax = plt.subplots(figsize=(7.4, 2.95), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    for row, (label, values, color) in enumerate(datasets):
        y = 1 - row
        ax.hlines(y, -0.5, 12.5, color="#d0d7de", linewidth=1.0, zorder=0)
        ax.scatter(values, [y] * len(values), s=70, color=color, edgecolor="white", linewidth=0.8, zorder=2)
        ax.axvline(mean(values), color="#cf222e", linestyle=(0, (5, 4)), linewidth=1.3, zorder=1)
        ax.text(
            12.75,
            y,
            f"{text['variance_label']} {variance(values):.1f}",
            ha="left",
            va="center",
            fontsize=9.2,
            color=color,
            bbox={"boxstyle": "round,pad=0.22", "facecolor": "white", "edgecolor": color, "linewidth": 0.8},
        )

    ax.text(
        6,
        1.34,
        f"{text['mean_label']} 6",
        ha="center",
        va="center",
        fontsize=9.2,
        color="#cf222e",
        bbox={"boxstyle": "round,pad=0.2", "facecolor": "white", "edgecolor": "#cf222e", "linewidth": 0.8},
    )

    ax.set_xlabel(text["value_label"])
    ax.set_ylabel(text["group_label"])
    ax.set_xlim(-0.8, 15.5)
    ax.set_ylim(-0.55, 1.55)
    ax.set_xticks([0, 2, 4, 6, 8, 10, 12])
    ax.set_yticks([1, 0])
    ax.set_yticklabels([datasets[0][0], datasets[1][0]])
    ax.grid(axis="x", color="#d0d7de", linewidth=0.7, alpha=0.65)

    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)

    fig.tight_layout(pad=0.8)
    fig.savefig(OUT_DIR / text["variance_outfile"])
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        plt.rcParams["font.family"] = choose_font(text["font_candidates"])
        plt.rcParams["axes.unicode_minus"] = False
        save_distribution_summary(text)
        save_same_mean_variance(text)


if __name__ == "__main__":
    main()
