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


OUT_DIR = REPO_ROOT / "docs" / "assets" / "part-05" / "chapter-02"

FRAMES = [
    ("needle_dominant_frame", [1.0, 0.2, 0.1]),
    ("beacon_valve_frame", [0.5, 0.9, 0.8]),
    ("combined_stop_frame", [1.1, 1.0, 0.9]),
    ("borderline_watch_frame", [0.7, 0.6, 0.5]),
]

INPUT_LABELS = ["needle_deviation", "beacon_blink", "valve_offset"]
HIDDEN_LABELS = ["pressure_axis", "warning_axis", "coordination_axis"]

HIDDEN_WEIGHTS = np.array(
    [
        [1.0, 0.1, 0.2],
        [0.1, 1.0, 0.6],
        [0.4, 0.5, 0.9],
    ]
)
HIDDEN_BIAS = np.array([-0.4, -0.5, -0.7])
OUTPUT_WEIGHTS = np.array([0.6, 0.5, 0.7])
OUTPUT_BIAS = -0.2

FRAME_NAMES = [name for name, _values in FRAMES]
INPUT_VALUES = np.array([values for _name, values in FRAMES])
PRE_ACTIVATION = INPUT_VALUES @ HIDDEN_WEIGHTS.T + HIDDEN_BIAS
HIDDEN_VALUES = np.maximum(0.0, PRE_ACTIVATION)
SCORES = HIDDEN_VALUES @ OUTPUT_WEIGHTS + OUTPUT_BIAS

COLORS = ["#2563eb", "#d97706", "#16a34a"]


def configure_fonts():
    candidates = [
        "AppleGothic",
        "Noto Sans CJK SC",
        "Noto Sans CJK KR",
        "Noto Sans KR",
        "Malgun Gothic",
        "DejaVu Sans",
    ]
    available = {font.name for font in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False


def locale_text(locale: str):
    is_ko = locale == "ko"
    is_zh = locale == "zh"
    return {
        "frame_labels": (
            ["바늘 중심", "경광등+밸브", "복합 정지", "경계 감시"]
            if is_ko
            else (
                ["指针主导", "警示灯+阀门", "复合停机", "边界监视"]
                if is_zh
                else ["Needle", "Beacon+valve", "Combined stop", "Borderline"]
            )
        ),
        "input_labels": (
            ["바늘 편차", "경광등 점멸", "밸브 이탈"]
            if is_ko
            else (
                ["指针偏差", "警示灯闪烁", "阀门偏移"]
                if is_zh
                else ["Needle deviation", "Beacon blink", "Valve offset"]
            )
        ),
        "hidden_labels": (
            ["압력 축", "경보 축", "조합 축"]
            if is_ko
            else (
                ["压力轴", "警告轴", "组合轴"]
                if is_zh
                else ["Pressure axis", "Warning axis", "Coordination axis"]
            )
        ),
        "input_ylabel": "原始输入值" if is_zh else ("원본 입력값" if is_ko else "Raw input value"),
        "pre_ylabel": "隐藏层前的值" if is_zh else ("은닉층 전 값" if is_ko else "Pre-activation value"),
        "hidden_ylabel": "ReLU 后激活值" if is_zh else ("ReLU 후 활성값" if is_ko else "Post-ReLU activation"),
        "score_ylabel": "最终分数" if is_zh else ("최종 점수" if is_ko else "Final score"),
        "frame_xlabel": "帧" if is_zh else ("프레임" if is_ko else "Frame"),
    }


def style_axis(ax, ylim=None):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, axis="y", linestyle="--", alpha=0.28)
    if ylim is not None:
        ax.set_ylim(*ylim)


def draw_grouped_bars(data, labels, ylabel, output_name, locale, ylim=None, zero_line=False):
    text = locale_text(locale)
    x = np.arange(len(FRAME_NAMES))
    width = 0.22

    fig, ax = plt.subplots(figsize=(10.2, 4.2), constrained_layout=True)
    for idx, (label, color) in enumerate(zip(labels, COLORS)):
        offset = (idx - 1) * width
        bars = ax.bar(
            x + offset,
            data[:, idx],
            width=width,
            label=label,
            color=color,
            alpha=0.92,
        )
        for bar, value in zip(bars, data[:, idx]):
            label_y = value + 0.035 if value >= 0 else value - 0.08
            va = "bottom" if value >= 0 else "top"
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                label_y,
                f"{value:.2f}",
                ha="center",
                va=va,
                fontsize=9,
            )

    if zero_line:
        ax.axhline(0, color="#334155", linewidth=1)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(text["frame_xlabel"])
    ax.set_xticks(x)
    ax.set_xticklabels(text["frame_labels"])
    ax.legend(loc="upper left", ncol=3, frameon=False)
    style_axis(ax, ylim=ylim)
    fig.savefig(OUT_DIR / f"{output_name}-{locale}.png", dpi=160)
    plt.close(fig)


def draw_score(locale: str):
    text = locale_text(locale)
    x = np.arange(len(FRAME_NAMES))
    colors = ["#94a3b8", "#f59e0b", "#dc2626", "#94a3b8"]

    fig, ax = plt.subplots(figsize=(10.2, 4.2), constrained_layout=True)
    bars = ax.bar(x, SCORES, color=colors, width=0.48)
    for bar, value in zip(bars, SCORES):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.06,
            f"{value:.3f}",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    ax.set_ylabel(text["score_ylabel"])
    ax.set_xlabel(text["frame_xlabel"])
    ax.set_xticks(x)
    ax.set_xticklabels(text["frame_labels"])
    style_axis(ax, ylim=(0, 1.9))
    fig.savefig(OUT_DIR / f"hidden-axis-score-{locale}.png", dpi=160)
    plt.close(fig)


def draw(locale: str):
    text = locale_text(locale)
    draw_grouped_bars(
        INPUT_VALUES,
        text["input_labels"],
        text["input_ylabel"],
        "hidden-axis-input",
        locale,
        ylim=(0, 1.25),
    )
    draw_grouped_bars(
        PRE_ACTIVATION,
        text["hidden_labels"],
        text["pre_ylabel"],
        "hidden-axis-preactivation",
        locale,
        ylim=(-0.32, 1.3),
        zero_line=True,
    )
    draw_grouped_bars(
        HIDDEN_VALUES,
        text["hidden_labels"],
        text["hidden_ylabel"],
        "hidden-axis-activation",
        locale,
        ylim=(0, 1.25),
    )
    draw_score(locale)


if __name__ == "__main__":
    configure_fonts()
    draw("ko")
    draw("en")
    draw("zh")
