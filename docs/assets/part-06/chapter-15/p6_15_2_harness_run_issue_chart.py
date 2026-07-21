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
    "healthy_run_count": 1,
    "stale_reference_count": 1,
    "approval_gap_count": 1,
    "replay_gap_count": 0,
    "replay_ready_count": 2,
    "approval_completed_count": 2,
    "run_count": 3,
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
        "outfile": "harness-run-issue-split-ko.png",
        "ylabel": "해당 실행 수",
        "labels": ["정상 실행", "오래된 근거", "승인 누락", "재현 누락", "replay 준비", "승인 완료"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "harness-run-issue-split-en.png",
        "ylabel": "matching runs",
        "labels": ["healthy", "stale source", "approval gap", "replay gap", "replay ready", "approved"],
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
    values = [
        SUMMARY["healthy_run_count"],
        SUMMARY["stale_reference_count"],
        SUMMARY["approval_gap_count"],
        SUMMARY["replay_gap_count"],
        SUMMARY["replay_ready_count"],
        SUMMARY["approval_completed_count"],
    ]
    colors = ["#0f766e", "#f59e0b", "#dc2626", "#9333ea", "#2563eb", "#64748b"]

    fig, ax = plt.subplots(figsize=(8.4, 3.9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    bars = ax.bar(text["labels"], values, color=colors, width=0.56)
    for bar in bars:
        value = bar.get_height()
        ratio = value / SUMMARY["run_count"]
        ax.annotate(
            f"{value:g}\n({ratio:.0%})",
            (bar.get_x() + bar.get_width() / 2, value),
            textcoords="offset points",
            xytext=(0, 7),
            ha="center",
            fontsize=8.5,
            color="#172033",
        )

    ax.set_ylabel(text["ylabel"])
    ax.set_ylim(0, SUMMARY["run_count"] * 1.32)
    ax.tick_params(axis="x", labelsize=9)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
