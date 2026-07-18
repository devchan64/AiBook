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

INPUT_PATCH = np.array(
    [
        [3, 3, 1, 1],
        [3, 3, 1, 1],
        [3, 3, 1, 1],
        [3, 3, 1, 1],
    ]
)
FILTER = np.array(
    [
        [1, -1],
        [1, -1],
    ]
)


TEXT = {
    "ko": {
        "font_candidates": [
            "Noto Sans CJK KR",
            "NanumGothic",
            "Apple SD Gothic Neo",
            "AppleGothic",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "input_note": "높은 열분포와 낮은 열분포가 만나는 경계",
        "feature_note": "좌우 차이가 큰 위치에서 반응 4",
        "pool_note": "가장 강한 경계 반응만 남김",
        "row": "행",
        "col": "열",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "input_note": "Boundary between high and low heat columns",
        "feature_note": "Response 4 where left-right contrast is strong",
        "pool_note": "Keep only the strongest boundary response",
        "row": "row",
        "col": "col",
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
        "input_note": "高列分布与低列分布相遇的边界",
        "feature_note": "左右差异明显的位置出现响应 4",
        "pool_note": "只保留最强的边界响应",
        "row": "行",
        "col": "列",
    },
}


def convolve_valid(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    out_rows = image.shape[0] - kernel.shape[0] + 1
    out_cols = image.shape[1] - kernel.shape[1] + 1
    result = np.zeros((out_rows, out_cols), dtype=float)
    for row in range(out_rows):
        for col in range(out_cols):
            window = image[row : row + kernel.shape[0], col : col + kernel.shape[1]]
            result[row, col] = np.sum(window * kernel)
    return result


def max_pool_2x2(values: np.ndarray) -> np.ndarray:
    return np.array([[np.max(values[:2, :2])]])


def choose_font(candidates: list[str]) -> str:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def configure_font(text: dict[str, str]) -> None:
    plt.rcParams["font.family"] = choose_font(text["font_candidates"])
    plt.rcParams["axes.unicode_minus"] = False


def draw_matrix(values: np.ndarray, note: str, filename: str, locale: str, text: dict[str, str], cmap: str, vmax: float) -> None:
    configure_font(text)
    fig, ax = plt.subplots(figsize=(4.8, 4.0), constrained_layout=True)
    image = ax.imshow(values, cmap=cmap, vmin=0, vmax=vmax)
    ax.set_xticks(np.arange(values.shape[1]))
    ax.set_yticks(np.arange(values.shape[0]))
    ax.set_xlabel(text["col"])
    ax.set_ylabel(text["row"])
    ax.set_xticklabels([str(i + 1) for i in range(values.shape[1])])
    ax.set_yticklabels([str(i + 1) for i in range(values.shape[0])])

    for row in range(values.shape[0]):
        for col in range(values.shape[1]):
            color = "white" if values[row, col] >= vmax * 0.58 else "#111827"
            ax.text(col, row, f"{values[row, col]:.0f}", ha="center", va="center", fontsize=13, color=color)

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks(np.arange(-0.5, values.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, values.shape[0], 1), minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=2)
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.text(
        0.5,
        -0.16,
        note,
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=9.5,
        color="#334155",
    )
    fig.colorbar(image, ax=ax, shrink=0.78, fraction=0.05, pad=0.04)
    fig.savefig(OUT_DIR / f"{filename}-{locale}.png", dpi=160)
    plt.close(fig)


def main() -> None:
    feature_map = convolve_valid(INPUT_PATCH, FILTER)
    pooled = max_pool_2x2(feature_map)

    for locale, text in TEXT.items():
        draw_matrix(
            INPUT_PATCH,
            text["input_note"],
            "convolution-pooling-input",
            locale,
            text,
            "YlOrBr",
            4,
        )
        draw_matrix(
            feature_map,
            text["feature_note"],
            "convolution-pooling-feature-map",
            locale,
            text,
            "Blues",
            4,
        )
        draw_matrix(
            pooled,
            text["pool_note"],
            "convolution-pooling-max-pool",
            locale,
            text,
            "Greens",
            4,
        )


if __name__ == "__main__":
    main()
