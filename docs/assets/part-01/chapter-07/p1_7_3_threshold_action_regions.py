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

POINTS = [
    ("delivery", 0.82, 0.58, "#0969da"),
    ("payment", 0.44, 0.0, "#8250df"),
    ("refund", 0.31, -0.58, "#57606a"),
]

LANG_TEXT = {
    "ko": {
        "font_candidates": ["Apple SD Gothic Neo", "AppleGothic", "Arial Unicode MS", "DejaVu Sans"],
        "xlabel": "모델 출력값 또는 점수",
        "regions": [
            (0.0, 0.60, "추가 질문"),
            (0.60, 0.90, "후보 제안"),
            (0.90, 1.0, "자동 응답"),
        ],
        "threshold_labels": [("0.60", "제안 기준"), ("0.90", "자동 처리 기준")],
        "point_labels": {
            "delivery": "배송 0.82",
            "payment": "결제 0.44",
            "refund": "환불 0.31",
        },
        "outfile": "threshold-action-regions-ko.png",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "xlabel": "model output or score",
        "regions": [
            (0.0, 0.60, "ask more"),
            (0.60, 0.90, "suggest candidate"),
            (0.90, 1.0, "automatic reply"),
        ],
        "threshold_labels": [("0.60", "suggestion threshold"), ("0.90", "automation threshold")],
        "point_labels": {
            "delivery": "delivery 0.82",
            "payment": "payment 0.44",
            "refund": "refund 0.31",
        },
        "outfile": "threshold-action-regions-en.png",
    },
    "zh": {
        "font_candidates": ["Arial Unicode MS", "Heiti TC", "PingFang SC", "DejaVu Sans"],
        "xlabel": "模型输出值或分数",
        "regions": [
            (0.0, 0.60, "追问"),
            (0.60, 0.90, "显示候选"),
            (0.90, 1.0, "自动回复"),
        ],
        "threshold_labels": [("0.60", "建议阈值"), ("0.90", "自动处理阈值")],
        "point_labels": {
            "delivery": "配送 0.82",
            "payment": "支付 0.44",
            "refund": "退款 0.31",
        },
        "outfile": "threshold-action-regions-zh.png",
    },
}


def choose_font(candidates: list[str]) -> str:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def save_chart(text: dict[str, object]) -> None:
    plt.rcParams["font.family"] = choose_font(text["font_candidates"])
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(7.4, 2.85), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    region_colors = ["#f6f8fa", "#ddf4ff", "#dafbe1"]
    for idx, (start, end, label) in enumerate(text["regions"]):
        ax.axvspan(start, end, color=region_colors[idx], alpha=0.95, zorder=0)
        ax.text((start + end) / 2, 0.94, label, ha="center", va="center", fontsize=9.5, color="#24292f")

    for x, label in [(0.60, text["threshold_labels"][0]), (0.90, text["threshold_labels"][1])]:
        value, name = label
        ax.axvline(x, color="#57606a", linestyle=(0, (4, 4)), linewidth=1.0, zorder=1)
        ax.text(
            x,
            -0.77,
            f"{value}\n{name}",
            ha="center",
            va="center",
            fontsize=8.5,
            color="#57606a",
            bbox={"boxstyle": "round,pad=0.18", "facecolor": "white", "edgecolor": "none", "alpha": 0.85},
        )

    ax.axhline(0, color="#8c959f", linewidth=1.0, zorder=1)
    for key, score, y, color in POINTS:
        ax.scatter(score, y, s=58, color=color, zorder=3)
        ax.text(
            score + 0.018,
            y,
            text["point_labels"][key],
            ha="left",
            va="center",
            fontsize=9.5,
            color=color,
            bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": color, "linewidth": 0.9},
        )

    ax.set_xlim(0, 1.0)
    ax.set_ylim(-1.05, 1.08)
    ax.set_xlabel(text["xlabel"])
    ax.set_yticks([])
    ax.set_xticks([0.0, 0.3, 0.6, 0.82, 0.9, 1.0])
    ax.set_xticklabels(["0", "0.30", "0.60", "0.82", "0.90", "1.00"])
    ax.grid(axis="x", color="#d0d7de", linewidth=0.7, alpha=0.75)

    for spine in ["left", "right", "top"]:
        ax.spines[spine].set_visible(False)

    fig.tight_layout(pad=0.8)
    fig.savefig(OUT_DIR / text["outfile"])
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
