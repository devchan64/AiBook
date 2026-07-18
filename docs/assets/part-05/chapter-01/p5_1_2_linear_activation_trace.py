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

STABILITY_SCORE = 1.0
STABILITY_WEIGHT = 0.8
ALARM_WEIGHT = -0.6
ALARM_RISKS = np.array([0.2, 0.5, 0.8])
BIASES = np.array([-0.1, -0.4])
THRESHOLDS = np.array([0.0, 0.2])

STABILITY_TERM = STABILITY_SCORE * STABILITY_WEIGHT
ALARM_TERMS = ALARM_RISKS * ALARM_WEIGHT
Z_VALUES = {
    bias: STABILITY_TERM + ALARM_TERMS + bias
    for bias in BIASES
}
OUTPUT_ROWS = [
    (bias, threshold, (Z_VALUES[bias] > threshold).astype(int))
    for bias in BIASES
    for threshold in THRESHOLDS
]


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
        "risk_label": "경보 위험",
        "input_ylabel": "입력값",
        "score_ylabel": "선형 결합 점수 z",
        "output_label": "최종 출력",
        "x_label": "alarm_risk",
        "bias_label": "편향",
        "threshold_label": "임계값",
        "bias_short": "b",
        "threshold_short": "기준",
        "pass_label": "통과",
        "hold_label": "보류",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "risk_label": "alarm risk",
        "input_ylabel": "input value",
        "score_ylabel": "linear score z",
        "output_label": "final output",
        "x_label": "alarm_risk",
        "bias_label": "bias",
        "threshold_label": "threshold",
        "bias_short": "b",
        "threshold_short": "t",
        "pass_label": "pass",
        "hold_label": "hold",
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK JP",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "risk_label": "报警风险",
        "input_ylabel": "输入值",
        "score_ylabel": "线性组合分数 z",
        "output_label": "最终输出",
        "x_label": "alarm_risk",
        "bias_label": "偏置",
        "threshold_label": "阈值",
        "bias_short": "b",
        "threshold_short": "阈",
        "pass_label": "通过",
        "hold_label": "保留",
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
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, axis="y", linestyle="--", linewidth=0.8, alpha=0.35)


def draw_input(locale: str) -> None:
    text = TEXT[locale]
    configure_font(text)

    fig, ax = plt.subplots(figsize=(7.2, 3.8), constrained_layout=True)
    bars = ax.bar([str(v) for v in ALARM_RISKS], ALARM_RISKS, color="#d97706", width=0.48)
    for bar, value in zip(bars, ALARM_RISKS):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.03, f"{value:.1f}", ha="center", fontsize=10)
    ax.set_xlabel(text["x_label"])
    ax.set_ylabel(text["input_ylabel"])
    ax.set_ylim(0, 1.0)
    style_axis(ax)
    fig.savefig(OUT_DIR / f"linear-activation-input-{locale}.png", dpi=160)
    plt.close(fig)


def draw_score(locale: str) -> None:
    text = TEXT[locale]
    configure_font(text)

    fig, ax = plt.subplots(figsize=(7.2, 3.8), constrained_layout=True)
    for bias, color in zip(BIASES, ["#2563eb", "#dc2626"]):
        values = Z_VALUES[bias]
        ax.plot(ALARM_RISKS, values, marker="o", linewidth=2.4, color=color, label=f"{text['bias_label']}={bias:.1f}")
        for x_value, z_value in zip(ALARM_RISKS, values):
            ax.text(x_value, z_value + 0.035, f"{z_value:.2f}", ha="center", fontsize=9)
    ax.axhline(0.0, color="#64748b", linewidth=1.2, linestyle=(0, (5, 4)), label=f"{text['threshold_label']}=0.0")
    ax.axhline(0.2, color="#94a3b8", linewidth=1.2, linestyle=(0, (2, 4)), label=f"{text['threshold_label']}=0.2")
    ax.set_xlabel(text["x_label"])
    ax.set_ylabel(text["score_ylabel"])
    ax.set_xticks(ALARM_RISKS)
    ax.set_ylim(-0.18, 0.68)
    ax.legend(loc="upper right", frameon=False, ncol=2, fontsize=9)
    style_axis(ax)
    fig.savefig(OUT_DIR / f"linear-activation-score-{locale}.png", dpi=160)
    plt.close(fig)


def draw_output(locale: str) -> None:
    text = TEXT[locale]
    configure_font(text)

    data = np.array([row[2] for row in OUTPUT_ROWS])
    row_labels = [
        f"{text['bias_short']}={bias:.1f}, {text['threshold_short']}={threshold:.1f}"
        for bias, threshold, _outputs in OUTPUT_ROWS
    ]

    fig, ax = plt.subplots(figsize=(7.2, 4.2), constrained_layout=True)
    ax.imshow(data, cmap=matplotlib.colors.ListedColormap(["#cbd5e1", "#16a34a"]), vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(np.arange(len(ALARM_RISKS)))
    ax.set_xticklabels([f"{value:.1f}" for value in ALARM_RISKS])
    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_yticklabels(row_labels)
    ax.set_xlabel(text["x_label"])
    ax.set_ylabel(f"{text['bias_label']}, {text['threshold_label']}")
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            label = text["pass_label"] if data[i, j] == 1 else text["hold_label"]
            color = "white" if data[i, j] == 1 else "#0f172a"
            ax.text(j, i, label, ha="center", va="center", color=color, fontsize=10)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks(np.arange(-0.5, len(ALARM_RISKS), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(row_labels), 1), minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=2)
    ax.tick_params(which="minor", bottom=False, left=False)
    fig.savefig(OUT_DIR / f"linear-activation-output-{locale}.png", dpi=160)
    plt.close(fig)


def main() -> None:
    for locale in ("ko", "en", "zh"):
        draw_input(locale)
        draw_score(locale)
        draw_output(locale)


if __name__ == "__main__":
    main()
