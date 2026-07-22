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
from matplotlib.colors import LinearSegmentedColormap

OUT_DIR = Path(__file__).resolve().parent

CASES = [
    {
        "issue": "format drift",
        "signals": {"format": 3, "evidence": 0, "execution": 0, "persistent_style": 1},
    },
    {
        "issue": "missing latest policy",
        "signals": {"format": 0, "evidence": 3, "execution": 0, "persistent_style": 1},
    },
    {
        "issue": "needs calculator",
        "signals": {"format": 0, "evidence": 1, "execution": 3, "persistent_style": 0},
    },
    {
        "issue": "persistent domain style",
        "signals": {"format": 1, "evidence": 0, "execution": 0, "persistent_style": 3},
    },
    {
        "issue": "mixed format and policy evidence",
        "signals": {"format": 2, "evidence": 3, "execution": 0, "persistent_style": 1},
    },
]

WEIGHTS = {
    "prompt revision": {"format": 3, "evidence": 0, "execution": 0, "persistent_style": 1},
    "RAG": {"format": 0, "evidence": 3, "execution": 0, "persistent_style": 0},
    "tool use": {"format": 0, "evidence": 1, "execution": 3, "persistent_style": 0},
    "fine-tuning": {"format": 1, "evidence": 0, "execution": 0, "persistent_style": 3},
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
        "outfile": "solution-selection-score-map-ko.png",
        "title": "부족 신호별 보강 경로 점수",
        "rows": ["형식 흔들림", "최신 규정 오류", "계산 오류", "문체 불안정", "형식+근거 복합"],
        "columns": ["프롬프트", "RAG", "도구 사용", "파인튜닝"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "solution-selection-score-map-en.png",
        "title": "Support-path score by missing signal",
        "rows": ["format drift", "missing policy", "calculation error", "style drift", "format + evidence"],
        "columns": ["prompt", "RAG", "tool use", "fine-tuning"],
    },
}


def score_action(signals: dict[str, int], action_name: str) -> int:
    action_weights = WEIGHTS[action_name]
    return sum(signals[key] * action_weights[key] for key in signals)


def calculate_scores() -> list[list[int]]:
    return [
        [score_action(case["signals"], action_name) for action_name in WEIGHTS]
        for case in CASES
    ]


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
    scores = calculate_scores()
    cmap = LinearSegmentedColormap.from_list(
        "selection_score",
        ["#f8fafc", "#bfdbfe", "#2563eb"],
    )

    fig, ax = plt.subplots(figsize=(7.3, 4.5), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.imshow(scores, cmap=cmap, vmin=0, vmax=10, aspect="auto")

    ax.set_title(text["title"], fontsize=12, pad=14, fontweight="bold")
    ax.set_xticks(range(len(text["columns"])), text["columns"])
    ax.set_yticks(range(len(text["rows"])), text["rows"])
    ax.tick_params(axis="x", labelsize=9, pad=8)
    ax.tick_params(axis="y", labelsize=9)

    ax.set_xticks([index - 0.5 for index in range(1, len(text["columns"]))], minor=True)
    ax.set_yticks([index - 0.5 for index in range(1, len(text["rows"]))], minor=True)
    ax.grid(which="minor", color="white", linewidth=2.0)
    ax.tick_params(which="minor", bottom=False, left=False)

    for row_index, row in enumerate(scores):
        row_max = max(row)
        row_sorted = sorted(row, reverse=True)
        second_value = row_sorted[1]
        for col_index, value in enumerate(row):
            is_first = value == row_max
            is_second = value == second_value and value != row_max and value > 0
            ax.text(
                col_index,
                row_index,
                str(value),
                ha="center",
                va="center",
                color="white" if is_first and value >= 9 else "#172033",
                fontsize=9,
                fontweight="bold" if is_first or is_second else "normal",
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
