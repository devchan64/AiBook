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
        "ko_prompt": "회의 결과",
        "en_prompt": "meeting result",
        "ko_candidates": [("배포", 0.5), ("우선", 0.5)],
        "en_candidates": [("release", 0.5), ("priority", 0.5)],
    },
    {
        "ko_prompt": "고객 문의 확인 결과",
        "en_prompt": "customer inquiry result",
        "ko_candidates": [("환불", 0.5), ("배송", 0.5)],
        "en_candidates": [("refund", 0.5), ("delivery", 0.5)],
    },
    {
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
        "title": "First Next-Token Candidate Distribution by Prompt",
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


def configure_font(text: dict[str, str]) -> None:
    plt.rcParams["font.family"] = choose_font(text["font_candidates"])
    plt.rcParams["axes.unicode_minus"] = False


def style_axis(ax) -> None:
    ax.grid(True, axis="x", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_branch_chart(text: dict[str, str]) -> None:
    configure_font(text)
    fig, axes = plt.subplots(len(BRANCHES), 1, figsize=(7.0, 4.8), dpi=180, sharex=True)
    fig.patch.set_facecolor("white")

    for ax, branch in zip(axes, BRANCHES):
        candidates = branch[text["candidate_key"]]
        labels = [candidate for candidate, _ in candidates]
        values = [prob for _, prob in candidates]
        bars = ax.barh(labels, values, color=["#2563eb", "#f97316"], height=0.48)
        style_axis(ax)
        ax.set_xlim(0, 0.7)
        ax.set_title(branch[text["prompt_key"]], loc="left", fontsize=10, pad=4)
        ax.tick_params(axis="y", labelsize=9)

        for bar, value in zip(bars, values):
            ax.annotate(
                f"{value:.2f}",
                (value, bar.get_y() + bar.get_height() / 2),
                textcoords="offset points",
                xytext=(6, 0),
                va="center",
                fontsize=9,
                color="#172033",
            )

    axes[-1].set_xlabel(text["xlabel"])
    fig.suptitle(text["title"], fontsize=12, y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.95], pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_branch_chart(text)


if __name__ == "__main__":
    main()
