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
    "auto_pass_count": 2,
    "auto_fail_count": 2,
    "needs_human_judgment_count": 1,
    "approved_count": 1,
    "revise_count": 1,
    "reject_count": 2,
    "answer_count": 4,
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
        "outfile": "auto-human-eval-routing-ko.png",
        "ylabel": "해당 후보 수",
        "labels": ["자동 통과", "자동 탈락", "사람 판단", "승인", "수정 후 검토", "탈락"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "auto-human-eval-routing-en.png",
        "ylabel": "matching candidates",
        "labels": ["auto pass", "auto fail", "human judgment", "approve", "revise", "reject"],
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
        SUMMARY["auto_pass_count"],
        SUMMARY["auto_fail_count"],
        SUMMARY["needs_human_judgment_count"],
        SUMMARY["approved_count"],
        SUMMARY["revise_count"],
        SUMMARY["reject_count"],
    ]
    colors = ["#2563eb", "#dc2626", "#9333ea", "#0f766e", "#f59e0b", "#64748b"]

    fig, ax = plt.subplots(figsize=(8.6, 3.9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    bars = ax.bar(text["labels"], values, color=colors, width=0.56)
    for bar in bars:
        value = bar.get_height()
        ratio = value / SUMMARY["answer_count"]
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
    ax.set_ylim(0, SUMMARY["answer_count"] * 1.28)
    ax.tick_params(axis="x", labelsize=9)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
