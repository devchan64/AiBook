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
    "fast": {
        "hit_count": 30,
        "top1_hit_count": 30,
        "version_ok_count": 35,
        "avg_latency_ms": 29.0,
    },
    "balanced": {
        "hit_count": 45,
        "top1_hit_count": 42,
        "version_ok_count": 46,
        "avg_latency_ms": 51.0,
    },
    "strict": {
        "hit_count": 52,
        "top1_hit_count": 48,
        "version_ok_count": 52,
        "avg_latency_ms": 70.0,
    },
    "query_count": 52,
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
        "outfile": "index-quality-latency-ko.png",
        "quality_ylabel": "실패한 질문 수",
        "latency_ylabel": "평균 지연 시간(ms)",
        "fast_label": "빠른 설정",
        "balanced_label": "균형 설정",
        "strict_label": "엄격한 설정",
        "quality_labels": ["목표 문서\n누락", "1위 오류", "버전 오류"],
        "latency_label": "평균 지연",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "index-quality-latency-en.png",
        "quality_ylabel": "failed queries",
        "latency_ylabel": "average latency (ms)",
        "fast_label": "fast setting",
        "balanced_label": "balanced setting",
        "strict_label": "strict setting",
        "quality_labels": ["target missed", "top-1 error", "version error"],
        "latency_label": "avg latency",
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
        "outfile": "index-quality-latency-zh.png",
        "quality_ylabel": "失败问题数",
        "latency_ylabel": "平均延迟时间(ms)",
        "fast_label": "快速设置",
        "balanced_label": "均衡设置",
        "strict_label": "严格设置",
        "quality_labels": ["目标文档\n遗漏", "首位错误", "版本错误"],
        "latency_label": "平均延迟",
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


def annotate_bars(bars, fmt: str = "{:g}") -> None:
    for bar in bars:
        value = bar.get_height()
        bar.axes.annotate(
            fmt.format(value),
            (bar.get_x() + bar.get_width() / 2, value),
            textcoords="offset points",
            xytext=(0, 6),
            ha="center",
            fontsize=9,
            color="#172033",
        )


def save_chart(text: dict[str, str]) -> None:
    configure_font(text)
    quality_labels = text["quality_labels"]
    query_count = SUMMARY["query_count"]
    fast_quality = [
        query_count - SUMMARY["fast"]["hit_count"],
        query_count - SUMMARY["fast"]["top1_hit_count"],
        query_count - SUMMARY["fast"]["version_ok_count"],
    ]
    balanced_quality = [
        query_count - SUMMARY["balanced"]["hit_count"],
        query_count - SUMMARY["balanced"]["top1_hit_count"],
        query_count - SUMMARY["balanced"]["version_ok_count"],
    ]
    strict_quality = [
        query_count - SUMMARY["strict"]["hit_count"],
        query_count - SUMMARY["strict"]["top1_hit_count"],
        query_count - SUMMARY["strict"]["version_ok_count"],
    ]
    positions = list(range(len(quality_labels)))
    bar_width = 0.24

    fig, (quality_ax, latency_ax) = plt.subplots(
        1,
        2,
        figsize=(9.0, 3.9),
        dpi=180,
        gridspec_kw={"width_ratios": [2.3, 1]},
    )
    fig.patch.set_facecolor("white")

    for ax in (quality_ax, latency_ax):
        ax.set_facecolor("white")
        style_axis(ax)

    fast_bars = quality_ax.bar(
        [x - bar_width for x in positions],
        fast_quality,
        width=bar_width,
        color="#64748b",
        label=text["fast_label"],
    )
    balanced_bars = quality_ax.bar(
        positions,
        balanced_quality,
        width=bar_width,
        color="#0f766e",
        label=text["balanced_label"],
    )
    strict_bars = quality_ax.bar(
        [x + bar_width for x in positions],
        strict_quality,
        width=bar_width,
        color="#2563eb",
        label=text["strict_label"],
    )
    annotate_bars(fast_bars)
    annotate_bars(balanced_bars)
    annotate_bars(strict_bars)
    quality_ax.set_xticks(positions)
    quality_ax.set_xticklabels(quality_labels)
    quality_ax.set_ylabel(text["quality_ylabel"])
    max_error = max(fast_quality + balanced_quality + strict_quality)
    quality_ax.set_ylim(0, max(max_error * 1.45, 4))
    quality_ax.legend(
        frameon=False,
        loc="upper left",
        bbox_to_anchor=(0.0, 1.18),
        ncol=3,
        handlelength=1.2,
        columnspacing=1.2,
    )

    latency_bars = latency_ax.bar(
        [text["fast_label"], text["balanced_label"], text["strict_label"]],
        [
            SUMMARY["fast"]["avg_latency_ms"],
            SUMMARY["balanced"]["avg_latency_ms"],
            SUMMARY["strict"]["avg_latency_ms"],
        ],
        color=["#64748b", "#0f766e", "#2563eb"],
        width=0.52,
    )
    annotate_bars(latency_bars, "{:.1f}")
    latency_ax.set_ylabel(text["latency_ylabel"])
    latency_ax.set_ylim(0, SUMMARY["strict"]["avg_latency_ms"] * 1.25)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
