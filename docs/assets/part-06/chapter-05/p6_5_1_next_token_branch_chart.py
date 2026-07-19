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

BRANCHES = [
    {
        "key": "meeting",
        "ko_prompt": "회의 결과",
        "en_prompt": "meeting result",
        "ko_candidates": [("배포", 0.5), ("우선", 0.5)],
        "en_candidates": [("release", 0.5), ("priority", 0.5)],
    },
    {
        "key": "customer",
        "ko_prompt": "고객 문의 확인 결과",
        "en_prompt": "customer inquiry result",
        "ko_candidates": [("환불", 0.5), ("배송", 0.5)],
        "en_candidates": [("refund", 0.5), ("delivery", 0.5)],
    },
    {
        "key": "deploy_error",
        "ko_prompt": "배포 오류 확인 결과",
        "en_prompt": "deployment error result",
        "ko_candidates": [("설정", 0.5), ("로그", 0.5)],
        "en_candidates": [("config", 0.5), ("logs", 0.5)],
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
        "outfile": "next-token-first-branch-ko.png",
        "title": "프롬프트별 첫 다음 토큰 후보 분포",
        "xlabel": "첫 다음 토큰 확률",
        "prompt_key": "ko_prompt",
        "candidate_key": "ko_candidates",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "next-token-first-branch-en.png",
        "title": "First next-token distribution by prompt",
        "xlabel": "first next-token probability",
        "prompt_key": "en_prompt",
        "candidate_key": "en_candidates",
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


def save_chart(text: dict[str, object]) -> None:
    configure_font(text)
    fig, ax = plt.subplots(figsize=(7.4, 3.6), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    bar_height = 0.26
    colors = ["#2563eb", "#0f766e"]
    y_ticks = []
    y_labels = []

    for group_index, branch in enumerate(BRANCHES):
        base_y = len(BRANCHES) - group_index
        y_ticks.append(base_y)
        y_labels.append(branch[text["prompt_key"]])
        for candidate_index, (token, probability) in enumerate(branch[text["candidate_key"]]):
            y = base_y + (0.16 if candidate_index == 0 else -0.16)
            ax.barh(
                y,
                probability,
                height=bar_height,
                color=colors[candidate_index],
                edgecolor="none",
            )
            ax.text(
                probability + 0.025,
                y,
                f"{token} {probability:.2f}",
                va="center",
                ha="left",
                fontsize=9,
                color="#172033",
            )

    ax.set_title(text["title"], fontsize=12, pad=14, fontweight="bold")
    ax.set_xlabel(text["xlabel"], labelpad=9)
    ax.set_yticks(y_ticks, y_labels)
    ax.set_xlim(0, 0.72)
    ax.set_ylim(0.45, len(BRANCHES) + 0.55)
    ax.grid(axis="x", color="#e2e8f0", linewidth=0.9)
    ax.tick_params(axis="y", length=0, labelsize=9)

    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#cbd5e1")

    fig.tight_layout(pad=1.0)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
