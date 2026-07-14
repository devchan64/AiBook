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
import numpy as np


OUT_DIR = Path(__file__).resolve().parent

NORMAL_PANEL = np.array(
    [
        [5, 5, 5, 5, 5],
        [5, 6, 6, 6, 5],
        [5, 6, 6, 6, 5],
        [5, 6, 6, 6, 5],
        [5, 5, 5, 5, 5],
    ],
    dtype=float,
)
SCRATCH_PANEL = np.array(
    [
        [5, 5, 5, 5, 5],
        [5, 6, 6, 9, 9],
        [5, 6, 6, 9, 8],
        [5, 6, 6, 8, 7],
        [5, 5, 5, 5, 5],
    ],
    dtype=float,
)

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
        "normal_outfile": "cnn-local-response-normal-ko.png",
        "scratch_outfile": "cnn-local-response-scratch-ko.png",
        "x_label": "2x2 패치 열 위치",
        "y_label": "2x2 패치 행 위치",
        "best_label": "최고 반응",
        "colorbar": "지역 반응 점수",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "normal_outfile": "cnn-local-response-normal-en.png",
        "scratch_outfile": "cnn-local-response-scratch-en.png",
        "x_label": "2x2 patch column",
        "y_label": "2x2 patch row",
        "best_label": "best response",
        "colorbar": "local response score",
    },
}


def local_response(patch: np.ndarray) -> float:
    return float(np.max(patch) - np.min(patch))


def response_map(panel: np.ndarray) -> np.ndarray:
    scores = np.zeros((panel.shape[0] - 1, panel.shape[1] - 1))
    for i in range(panel.shape[0] - 1):
        for j in range(panel.shape[1] - 1):
            scores[i, j] = local_response(panel[i : i + 2, j : j + 2])
    return scores


def choose_font(candidates: list[str]) -> str:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def configure_font(text: dict[str, str]) -> None:
    plt.rcParams["font.family"] = choose_font(text["font_candidates"])
    plt.rcParams["axes.unicode_minus"] = False


def save_response_map(text: dict[str, str], scores: np.ndarray, outfile: str) -> None:
    configure_font(text)
    best_row, best_col = np.unravel_index(np.argmax(scores), scores.shape)

    fig, ax = plt.subplots(figsize=(4.8, 4.1), dpi=180)
    fig.patch.set_facecolor("white")
    image = ax.imshow(scores, cmap="YlOrRd", vmin=0, vmax=4)

    for row in range(scores.shape[0]):
        for col in range(scores.shape[1]):
            ax.text(col, row, f"{scores[row, col]:.0f}", ha="center", va="center", fontsize=9, color="#111827")

    ax.scatter([best_col], [best_row], marker="s", s=420, facecolors="none", edgecolors="#1d4ed8", linewidths=2.0)
    ax.annotate(
        text["best_label"],
        xy=(best_col, best_row),
        xytext=(best_col + 0.45, best_row - 0.55),
        fontsize=8.5,
        color="#1d4ed8",
        arrowprops={"arrowstyle": "->", "color": "#1d4ed8", "linewidth": 0.8},
    )

    ax.set_xticks(range(scores.shape[1]))
    ax.set_yticks(range(scores.shape[0]))
    ax.set_xlabel(text["x_label"])
    ax.set_ylabel(text["y_label"])
    ax.set_xlim(-0.5, scores.shape[1] - 0.5)
    ax.set_ylim(scores.shape[0] - 0.5, -0.5)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04, label=text["colorbar"])
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / outfile, format="png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    normal_scores = response_map(NORMAL_PANEL)
    scratch_scores = response_map(SCRATCH_PANEL)
    for text in LANG_TEXT.values():
        save_response_map(text, normal_scores, text["normal_outfile"])
        save_response_map(text, scratch_scores, text["scratch_outfile"])


if __name__ == "__main__":
    main()
