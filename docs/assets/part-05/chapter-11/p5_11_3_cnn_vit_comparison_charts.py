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

INSPECTION_FRAME = np.array(
    [
        [4, 4, 4, 1, 1, 1],
        [4, 5, 4, 1, 2, 1],
        [4, 4, 4, 1, 1, 1],
        [2, 2, 2, 3, 3, 3],
        [2, 2, 2, 3, 8, 3],
        [2, 2, 2, 3, 3, 3],
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
        "cnn_outfile": "cnn-vit-cnn-local-score-map-ko.png",
        "vit_outfile": "cnn-vit-patch-token-mean-map-ko.png",
        "cnn_x_label": "2x2 국소 창 열 위치",
        "cnn_y_label": "2x2 국소 창 행 위치",
        "vit_x_label": "3x3 패치 열 위치",
        "vit_y_label": "3x3 패치 행 위치",
        "cnn_colorbar": "국소 대비 점수",
        "vit_colorbar": "패치 평균",
        "top_candidate": "상위 후보",
        "code_token": "코드 패치",
        "blank_token": "빈 배경 패치",
        "seal_token": "실링 패치",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "cnn_outfile": "cnn-vit-cnn-local-score-map-en.png",
        "vit_outfile": "cnn-vit-patch-token-mean-map-en.png",
        "cnn_x_label": "2x2 local-window column",
        "cnn_y_label": "2x2 local-window row",
        "vit_x_label": "3x3 patch column",
        "vit_y_label": "3x3 patch row",
        "cnn_colorbar": "local contrast score",
        "vit_colorbar": "patch mean",
        "top_candidate": "top candidate",
        "code_token": "code patch",
        "blank_token": "blank patch",
        "seal_token": "seal patch",
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK JP",
            "Source Han Sans SC",
            "Microsoft YaHei",
            "PingFang SC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "cnn_outfile": "cnn-vit-cnn-local-score-map-zh.png",
        "vit_outfile": "cnn-vit-patch-token-mean-map-zh.png",
        "cnn_x_label": "2x2 局部窗口列位置",
        "cnn_y_label": "2x2 局部窗口行位置",
        "vit_x_label": "3x3 patch 列位置",
        "vit_y_label": "3x3 patch 行位置",
        "cnn_colorbar": "局部对比分数",
        "vit_colorbar": "patch 平均值",
        "top_candidate": "高优先候选",
        "code_token": "代码 patch",
        "blank_token": "空白背景 patch",
        "seal_token": "封口 patch",
    },
}


def cnn_local_score_map(image: np.ndarray, window: int = 2) -> np.ndarray:
    scores = np.zeros((image.shape[0] - window + 1, image.shape[1] - window + 1))
    for i in range(scores.shape[0]):
        for j in range(scores.shape[1]):
            values = image[i : i + window, j : j + window]
            scores[i, j] = np.max(values) - np.min(values)
    return scores


def vit_patch_mean_map(image: np.ndarray, patch_size: int = 3) -> np.ndarray:
    rows = image.shape[0] // patch_size
    cols = image.shape[1] // patch_size
    means = np.zeros((rows, cols))
    for row, i in enumerate(range(0, image.shape[0], patch_size)):
        for col, j in enumerate(range(0, image.shape[1], patch_size)):
            means[row, col] = round(float(np.mean(image[i : i + patch_size, j : j + patch_size])), 2)
    return means


def choose_font(candidates: list[str]) -> str:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def configure_font(text: dict[str, str]) -> None:
    plt.rcParams["font.family"] = choose_font(text["font_candidates"])
    plt.rcParams["axes.unicode_minus"] = False


def save_cnn_score_map(text: dict[str, str]) -> None:
    configure_font(text)
    scores = cnn_local_score_map(INSPECTION_FRAME)
    top_positions = [(3, 3), (3, 4), (4, 3), (4, 4)]

    fig, ax = plt.subplots(figsize=(5.6, 4.8), dpi=180)
    fig.patch.set_facecolor("white")
    image = ax.imshow(scores, cmap="YlOrRd", vmin=0, vmax=5)
    for row in range(scores.shape[0]):
        for col in range(scores.shape[1]):
            ax.text(col, row, f"{scores[row, col]:.0f}", ha="center", va="center", fontsize=8.5, color="#111827")

    for row, col in top_positions:
        ax.scatter([col], [row], marker="s", s=265, facecolors="none", edgecolors="#1d4ed8", linewidths=1.8)
    ax.annotate(
        text["top_candidate"],
        xy=(3.5, 3.5),
        xytext=(1.35, 4.35),
        fontsize=8.4,
        color="#1d4ed8",
        arrowprops={"arrowstyle": "->", "color": "#1d4ed8", "linewidth": 0.8},
    )

    ax.set_xticks(range(scores.shape[1]))
    ax.set_yticks(range(scores.shape[0]))
    ax.set_xlabel(text["cnn_x_label"])
    ax.set_ylabel(text["cnn_y_label"])
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04, label=text["cnn_colorbar"])
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["cnn_outfile"], format="png", bbox_inches="tight")
    plt.close(fig)


def save_vit_token_map(text: dict[str, str]) -> None:
    configure_font(text)
    means = vit_patch_mean_map(INSPECTION_FRAME)

    fig, ax = plt.subplots(figsize=(5.0, 4.2), dpi=180)
    fig.patch.set_facecolor("white")
    image = ax.imshow(means, cmap="YlGnBu", vmin=1, vmax=4.2)
    for row in range(means.shape[0]):
        for col in range(means.shape[1]):
            color = "white" if means[row, col] >= 3.2 else "#111827"
            ax.text(col, row, f"{means[row, col]:.2f}".rstrip("0").rstrip("."), ha="center", va="center", fontsize=9, color=color)

    labels = {
        (0, 1): text["blank_token"],
        (1, 0): text["seal_token"],
        (1, 1): text["code_token"],
    }
    for (row, col), label in labels.items():
        ax.scatter([col], [row], marker="s", s=480, facecolors="none", edgecolors="#0f766e", linewidths=1.8)
        label_color = "white" if means[row, col] >= 3.2 else "#0f766e"
        ax.text(col, row + 0.32, label, ha="center", va="center", fontsize=7.8, color=label_color)

    ax.set_xticks(range(means.shape[1]))
    ax.set_yticks(range(means.shape[0]))
    ax.set_xticklabels(["0", "3"])
    ax.set_yticklabels(["0", "3"])
    ax.set_xlabel(text["vit_x_label"])
    ax.set_ylabel(text["vit_y_label"])
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04, label=text["vit_colorbar"])
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["vit_outfile"], format="png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_cnn_score_map(text)
        save_vit_token_map(text)


if __name__ == "__main__":
    main()
