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

ROUND_PROGRESS = [
    {"round": 1, "completed_state_count": 1, "next_step": "read_top_documents"},
    {"round": 2, "completed_state_count": 2, "next_step": "summarize_changes"},
    {"round": 3, "completed_state_count": 3, "next_step": "attach_sources"},
    {"round": 4, "completed_state_count": 4, "next_step": "finished"},
]

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
        "outfile": "agent-state-progress-ko.png",
        "xlabel": "라운드",
        "ylabel": "완료된 상태 항목 수",
        "labels": ["검색", "읽기", "요약", "출처"],
        "annotation_prefix": "다음:",
        "next_labels": ["읽기", "요약", "출처", "종료"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "agent-state-progress-en.png",
        "xlabel": "round",
        "ylabel": "completed state checks",
        "labels": ["search", "read", "summarize", "sources"],
        "annotation_prefix": "next:",
        "next_labels": ["read", "summarize", "sources", "done"],
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
    rounds = [item["round"] for item in ROUND_PROGRESS]
    values = [item["completed_state_count"] for item in ROUND_PROGRESS]
    colors = ["#2563eb", "#0f766e", "#f59e0b", "#9333ea"]

    fig, ax = plt.subplots(figsize=(7.0, 3.9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    bars = ax.bar(rounds, values, color=colors, width=0.55)
    ax.plot(rounds, values, color="#172033", marker="o", linewidth=1.5)

    for bar, next_label in zip(bars, text["next_labels"]):
        value = bar.get_height()
        ax.annotate(
            f"{value:g}/4\n{text['annotation_prefix']} {next_label}",
            (bar.get_x() + bar.get_width() / 2, value),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=8.5,
            color="#172033",
        )

    ax.set_xticks(rounds)
    ax.set_xticklabels([f"{idx}\n{label}" for idx, label in zip(rounds, text["labels"])])
    ax.set_xlabel(text["xlabel"])
    ax.set_ylabel(text["ylabel"])
    ax.set_ylim(0, 4.85)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
