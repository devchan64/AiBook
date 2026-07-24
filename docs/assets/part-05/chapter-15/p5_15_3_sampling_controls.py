from pathlib import Path
import os
import random

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

CANDIDATES = [
    "재확인이 필요합니다.",
    "담당자 확인 후 재개합니다.",
    "10분 뒤 재측정합니다.",
    "현재 기준에서는 정상으로 유지합니다.",
    "즉시 재기동합니다.",
]
LOGITS = np.array([3.2, 2.4, 1.7, 0.6, -0.4])
EXPERIMENTS = [
    ("argmax", 0.0, None),
    ("temperature_0.7", 0.7, None),
    ("temperature_1.4", 1.4, None),
    ("top_k_3_temperature_1.0", 1.0, 3),
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
        "labels": ["재확인", "담당자 확인", "10분 뒤", "정상 유지", "즉시 재기동"],
        "prob_title": "sampling 설정별 후보 확률",
        "prob_ylabel": "확률",
        "count_title": "sampling 설정별 40회 선택 빈도",
        "count_ylabel": "선택 횟수",
        "outfile_prob": "sampling-control-probabilities-ko.png",
        "outfile_count": "sampling-control-counts-ko.png",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "labels": ["recheck", "confirm", "10 min", "normal", "restart now"],
        "prob_title": "Candidate probabilities by sampling setting",
        "prob_ylabel": "probability",
        "count_title": "Choice counts over 40 draws",
        "count_ylabel": "choice count",
        "outfile_prob": "sampling-control-probabilities-en.png",
        "outfile_count": "sampling-control-counts-en.png",
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK JP",
            "Microsoft YaHei",
            "PingFang SC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "labels": ["重新确认", "主管确认", "10 分钟后", "保持正常", "立即重启"],
        "prob_title": "不同 sampling 设置下的候选概率",
        "prob_ylabel": "概率",
        "count_title": "40 次 sampling 的选择频率",
        "count_ylabel": "选择次数",
        "outfile_prob": "sampling-control-probabilities-zh.png",
        "outfile_count": "sampling-control-counts-zh.png",
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


def softmax(logits: np.ndarray, temperature: float) -> np.ndarray:
    scaled = logits / temperature
    shifted = scaled - np.max(scaled)
    exp_scores = np.exp(shifted)
    return exp_scores / exp_scores.sum()


def apply_top_k(probabilities: np.ndarray, k: int | None) -> np.ndarray:
    if k is None:
        return probabilities
    cutoff_indices = np.argsort(probabilities)[-k:]
    filtered = np.zeros_like(probabilities)
    filtered[cutoff_indices] = probabilities[cutoff_indices]
    return filtered / filtered.sum()


def probabilities_for(temperature: float, top_k: int | None) -> np.ndarray:
    if temperature == 0.0:
        probabilities = np.zeros_like(LOGITS, dtype=float)
        probabilities[int(np.argmax(LOGITS))] = 1.0
        return probabilities
    return apply_top_k(softmax(LOGITS, temperature), top_k)


def entropy_bits(probabilities: np.ndarray) -> float:
    non_zero = probabilities[probabilities > 0]
    if len(non_zero) <= 1:
        return 0.0
    return -float(np.sum(non_zero * np.log2(non_zero)))


def draw_counts(probabilities: np.ndarray, draws: int = 40) -> np.ndarray:
    random.seed(15)
    choices = random.choices(range(len(CANDIDATES)), weights=probabilities, k=draws)
    return np.array([choices.count(index) for index in range(len(CANDIDATES))])


def style_axis(axis) -> None:
    axis.set_facecolor("#f8fafc")
    axis.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    axis.set_axisbelow(True)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)


def plot_grouped_bars(values_by_case: list[np.ndarray], text: dict[str, object], *, kind: str) -> None:
    configure_font(text)
    labels = text["labels"]
    x = np.arange(len(labels))
    width = 0.19
    colors = ["#1d4ed8", "#0f766e", "#d97706", "#7c3aed"]

    fig, axis = plt.subplots(figsize=(8.2, 4.6), dpi=160)
    fig.patch.set_facecolor("white")
    style_axis(axis)

    for idx, (case, values) in enumerate(zip(EXPERIMENTS, values_by_case)):
        offset = (idx - 1.5) * width
        axis.bar(x + offset, values, width=width, label=case[0], color=colors[idx])

    axis.set_xticks(x)
    axis.set_xticklabels(labels, fontsize=8.5)
    axis.set_ylabel(text["prob_ylabel"] if kind == "prob" else text["count_ylabel"])
    axis.set_title(text["prob_title"] if kind == "prob" else text["count_title"], fontsize=12.5)
    axis.legend(fontsize=7.5, ncol=2, frameon=False)
    if kind == "prob":
        axis.set_ylim(0, 1.05)
    else:
        axis.set_ylim(0, max(max(values) for values in values_by_case) + 4)

    fig.tight_layout(pad=1.1)
    outfile = text["outfile_prob"] if kind == "prob" else text["outfile_count"]
    fig.savefig(OUT_DIR / outfile, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    probability_rows = [probabilities_for(temperature, top_k) for _, temperature, top_k in EXPERIMENTS]
    count_rows = [draw_counts(probabilities) for probabilities in probability_rows]
    for text in LANG_TEXT.values():
        plot_grouped_bars(probability_rows, text, kind="prob")
        plot_grouped_bars(count_rows, text, kind="count")


if __name__ == "__main__":
    main()
