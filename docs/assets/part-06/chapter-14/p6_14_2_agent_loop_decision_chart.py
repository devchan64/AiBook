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

SCENARIOS = [
    {
        "latest_doc": True,
        "conflict": False,
        "stop": True,
        "decision": "stop",
    },
    {
        "latest_doc": True,
        "conflict": True,
        "stop": True,
        "decision": "human_review",
    },
    {
        "latest_doc": False,
        "conflict": False,
        "stop": False,
        "decision": "continue",
    },
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
        "outfile": "agent-loop-decision-split-ko.png",
        "scenario_labels": ["최신 근거 확보", "충돌 문서 발견", "최신 근거 부족"],
        "condition_labels": ["최신 문서", "충돌", "멈춤"],
        "decision_labels": {
            "continue": "계속 진행",
            "stop": "종료",
            "human_review": "사람\n검토",
        },
        "decision_axis": "결정",
        "yes": "예",
        "no": "아니오",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "agent-loop-decision-split-en.png",
        "scenario_labels": ["latest evidence", "conflicting docs", "missing latest"],
        "condition_labels": ["latest doc", "conflict", "stop"],
        "decision_labels": {
            "continue": "continue",
            "stop": "stop",
            "human_review": "human review",
        },
        "decision_axis": "decision",
        "yes": "yes",
        "no": "no",
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
    ax.grid(True, axis="x", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_chart(text: dict[str, str]) -> None:
    configure_font(text)
    condition_keys = ["latest_doc", "conflict", "stop"]
    decision_colors = {
        "continue": "#2563eb",
        "stop": "#0f766e",
        "human_review": "#dc2626",
    }

    fig, ax = plt.subplots(figsize=(7.4, 3.9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    for row_index, scenario in enumerate(SCENARIOS):
        for col_index, key in enumerate(condition_keys):
            value = scenario[key]
            ax.scatter(
                col_index,
                row_index,
                s=520,
                marker="s",
                color="#0f766e" if value else "#e5e7eb",
                edgecolor="#172033",
                linewidth=0.8,
                zorder=3,
            )
            ax.text(
                col_index,
                row_index,
                text["yes"] if value else text["no"],
                ha="center",
                va="center",
                fontsize=8.5,
                color="white" if value else "#172033",
                zorder=4,
            )

        decision_x = len(condition_keys) + 0.7
        decision = scenario["decision"]
        ax.scatter(
            decision_x,
            row_index,
            s=860,
            marker="o",
            color=decision_colors[decision],
            edgecolor="#172033",
            linewidth=0.8,
            zorder=3,
        )
        ax.text(
            decision_x,
            row_index,
            text["decision_labels"][decision],
            ha="center",
            va="center",
            fontsize=8.0,
            color="white",
            zorder=4,
        )

    ax.axvline(len(condition_keys) - 0.4, color="#94a3b8", linewidth=1.0, linestyle="--")
    ax.set_xticks([0, 1, 2, len(condition_keys) + 0.7])
    ax.set_xticklabels([*text["condition_labels"], text["decision_axis"]])
    ax.set_yticks(range(len(SCENARIOS)))
    ax.set_yticklabels(text["scenario_labels"])
    ax.set_xlim(-0.6, len(condition_keys) + 1.35)
    ax.set_ylim(-0.65, len(SCENARIOS) - 0.35)
    ax.invert_yaxis()
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
