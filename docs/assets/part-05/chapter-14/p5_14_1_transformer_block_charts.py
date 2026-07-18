from __future__ import annotations

from pathlib import Path
import os

REPO_ROOT = Path(__file__).resolve().parents[4]
MPL_CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager


OUT_DIR = Path(__file__).resolve().parent

TOKENS = np.array([
    [1.0, 0.2],
    [0.8, 0.5],
    [0.3, 1.0],
])

ATTENTION_CASES = {
    "rollback_confirmed": np.array([
        [0.6, 0.3, 0.1],
        [0.2, 0.5, 0.3],
        [0.1, 0.3, 0.6],
    ]),
    "rollback_not_confirmed": np.array([
        [0.6, 0.3, 0.1],
        [0.3, 0.5, 0.2],
        [0.3, 0.5, 0.2],
    ]),
}

FF_WEIGHTS = np.array([
    [1.1, 0.4],
    [0.2, 1.0],
])

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
        "confirmed": "롤백 확인",
        "not_confirmed": "롤백 미확인",
        "x_label": "긴급/원인 축",
        "y_label": "복구 상태 축",
        "axis_labels": ["긴급/원인 축", "복구 상태 축"],
        "stage_labels": ["입력", "문맥 섞기", "피드포워드", "잔차 후"],
        "stage_outfile": "transformer-block-action-stage-trace-ko.png",
        "residual_outfile": "transformer-block-action-residual-compare-ko.png",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "confirmed": "rollback confirmed",
        "not_confirmed": "rollback not confirmed",
        "x_label": "urgency/cause axis",
        "y_label": "recovery-status axis",
        "axis_labels": ["urgency/cause", "recovery status"],
        "stage_labels": ["input", "contextual", "feed-forward", "after residual"],
        "stage_outfile": "transformer-block-action-stage-trace-en.png",
        "residual_outfile": "transformer-block-action-residual-compare-en.png",
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
        "confirmed": "已确认回滚",
        "not_confirmed": "未确认回滚",
        "x_label": "紧急/原因轴",
        "y_label": "恢复状态轴",
        "axis_labels": ["紧急/原因轴", "恢复状态轴"],
        "stage_labels": ["输入", "上下文混合", "前馈网络", "残差之后"],
        "stage_outfile": "transformer-block-action-stage-trace-zh.png",
        "residual_outfile": "transformer-block-action-residual-compare-zh.png",
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


def block_outputs() -> dict[str, dict[str, np.ndarray]]:
    result = {}
    for name, attention_weights in ATTENTION_CASES.items():
        contextual = attention_weights @ TOKENS
        ff_output = contextual @ FF_WEIGHTS
        residual_added = ff_output + TOKENS
        result[name] = {
            "input": TOKENS,
            "contextual": contextual,
            "feed_forward": ff_output,
            "residual": residual_added,
        }
    return result


def action_points(case_output: dict[str, np.ndarray]) -> np.ndarray:
    return np.vstack([
        case_output["input"][2],
        case_output["contextual"][2],
        case_output["feed_forward"][2],
        case_output["residual"][2],
    ])


def draw_stage_trace(locale: str, data: dict[str, dict[str, np.ndarray]]) -> None:
    text = TEXT[locale]
    configure_font(text)
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.set_xlabel(text["x_label"], fontsize=10)
    ax.set_ylabel(text["y_label"], fontsize=10)
    ax.set_xlim(0.2, 1.4)
    ax.set_ylim(0.45, 2.1)
    ax.grid(True, linestyle="--", alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)

    cases = [
        ("rollback_confirmed", text["confirmed"], "#2563eb"),
        ("rollback_not_confirmed", text["not_confirmed"], "#f97316"),
    ]
    for case_name, label, color in cases:
        points = action_points(data[case_name])
        ax.plot(points[:, 0], points[:, 1], marker="o", linewidth=2.2, color=color, label=label)
        for stage_index, (x_value, y_value) in enumerate(points):
            ax.text(
                x_value + 0.025,
                y_value + 0.025,
                text["stage_labels"][stage_index],
                fontsize=8.1,
                color=color,
            )
    ax.legend(frameon=False, loc="upper left", fontsize=8.5)
    fig.tight_layout()
    fig.savefig(OUT_DIR / text["stage_outfile"], format="png", bbox_inches="tight", dpi=160)
    plt.close(fig)


def draw_residual_compare(locale: str, data: dict[str, dict[str, np.ndarray]]) -> None:
    text = TEXT[locale]
    configure_font(text)
    confirmed = data["rollback_confirmed"]["residual"][2]
    not_confirmed = data["rollback_not_confirmed"]["residual"][2]
    x = np.arange(2)
    width = 0.34

    fig, ax = plt.subplots(figsize=(6.3, 3.8))
    bars_a = ax.bar(x - width / 2, confirmed, width, label=text["confirmed"], color="#2563eb")
    bars_b = ax.bar(x + width / 2, not_confirmed, width, label=text["not_confirmed"], color="#f97316")
    ax.set_xticks(x)
    ax.set_xticklabels(text["axis_labels"], fontsize=9)
    ax.set_ylim(0, 2.15)
    ax.grid(axis="y", linestyle="--", alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, loc="upper left", fontsize=8.5)
    for bars in [bars_a, bars_b]:
        for bar in bars:
            value = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, value + 0.04, f"{value:.3f}", ha="center", fontsize=8.5)
    fig.tight_layout()
    fig.savefig(OUT_DIR / text["residual_outfile"], format="png", bbox_inches="tight", dpi=160)
    plt.close(fig)


def main() -> None:
    data = block_outputs()
    for locale in ["en", "ko", "zh"]:
        draw_stage_trace(locale, data)
        draw_residual_compare(locale, data)


if __name__ == "__main__":
    main()
