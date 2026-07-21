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
    "consistent_layer": {
        "success_count": 4,
        "tool_resolution_success_count": 4,
        "resource_resolution_success_count": 4,
    },
    "inconsistent_layer": {
        "success_count": 0,
        "tool_resolution_success_count": 3,
        "resource_resolution_success_count": 3,
    },
    "request_count": 4,
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
        "outfile": "mcp-connection-layer-check-ko.png",
        "ylabel": "통과한 요청 수",
        "consistent_label": "공통 연결 계층",
        "inconsistent_label": "제각각 연결 계층",
        "labels": ["요청 완료", "도구 해석", "자원 해석"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "mcp-connection-layer-check-en.png",
        "ylabel": "passed requests",
        "consistent_label": "consistent layer",
        "inconsistent_label": "inconsistent layer",
        "labels": ["request success", "tool resolved", "resource resolved"],
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
    consistent_values = [
        SUMMARY["consistent_layer"]["success_count"],
        SUMMARY["consistent_layer"]["tool_resolution_success_count"],
        SUMMARY["consistent_layer"]["resource_resolution_success_count"],
    ]
    inconsistent_values = [
        SUMMARY["inconsistent_layer"]["success_count"],
        SUMMARY["inconsistent_layer"]["tool_resolution_success_count"],
        SUMMARY["inconsistent_layer"]["resource_resolution_success_count"],
    ]
    x_positions = list(range(len(labels)))
    bar_width = 0.34

    fig, ax = plt.subplots(figsize=(7.2, 3.9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    consistent_bars = ax.bar(
        [x - bar_width / 2 for x in x_positions],
        consistent_values,
        width=bar_width,
        color="#2563eb",
        label=text["consistent_label"],
    )
    inconsistent_bars = ax.bar(
        [x + bar_width / 2 for x in x_positions],
        inconsistent_values,
        width=bar_width,
        color="#dc2626",
        label=text["inconsistent_label"],
    )

    for bars in (consistent_bars, inconsistent_bars):
        for bar in bars:
            value = bar.get_height()
            ax.annotate(
                f"{value:g}",
                (bar.get_x() + bar.get_width() / 2, value),
                textcoords="offset points",
                xytext=(0, 6),
                ha="center",
                fontsize=9,
                color="#172033",
            )

    ax.set_xticks(x_positions)
    ax.set_xticklabels(labels)
    ax.set_ylabel(text["ylabel"])
    ax.set_ylim(0, SUMMARY["request_count"] * 1.25)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
