from pathlib import Path
import math
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

SENTENCES = {
    "pressure_hold_time": 3.0,
    "coolant_flow_limit": 12.0,
    "high_temp_exception": 5.0,
}
SCORES_FOR_RETURN = {
    "pressure_hold_time": 2.5,
    "coolant_flow_limit": 0.9,
    "high_temp_exception": 0.3,
}
SCORES_FOR_FLOW = {
    "pressure_hold_time": 0.8,
    "coolant_flow_limit": 2.4,
    "high_temp_exception": 0.4,
}
ORDERED_NAMES = list(SENTENCES.keys())
VALUES = np.array([SENTENCES[name] for name in ORDERED_NAMES])
BASELINE_CONTEXT = sum((1 / len(VALUES)) * value for value in VALUES)


def attention_weights(score_table: dict[str, float]) -> np.ndarray:
    raw_scores = [score_table[name] for name in ORDERED_NAMES]
    exp_scores = [math.exp(score) for score in raw_scores]
    total = sum(exp_scores)
    return np.array([score / total for score in exp_scores])


RETURN_WEIGHTS = attention_weights(SCORES_FOR_RETURN)
FLOW_WEIGHTS = attention_weights(SCORES_FOR_FLOW)
RETURN_CONTEXT = float(np.sum(RETURN_WEIGHTS * VALUES))
FLOW_CONTEXT = float(np.sum(FLOW_WEIGHTS * VALUES))

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
        "return_weight_outfile": "attention-pressure-question-weights-ko.png",
        "flow_weight_outfile": "attention-flow-question-weights-ko.png",
        "context_outfile": "attention-context-comparison-ko.png",
        "return_question": "압력 해소 유지 시간 질문",
        "flow_question": "냉각수 유량 기준 질문",
        "weight_label": "attention 비중",
        "candidate_label": "문장 후보",
        "context_label": "문맥값",
        "baseline": "baseline 평균",
        "pressure_context": "압력 질문 context",
        "flow_context": "유량 질문 context",
        "names": ["압력 유지 시간", "냉각수 유량", "고온 예외"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "return_weight_outfile": "attention-pressure-question-weights-en.png",
        "flow_weight_outfile": "attention-flow-question-weights-en.png",
        "context_outfile": "attention-context-comparison-en.png",
        "return_question": "pressure-hold-time question",
        "flow_question": "coolant-flow question",
        "weight_label": "attention weight",
        "candidate_label": "sentence candidate",
        "context_label": "context value",
        "baseline": "baseline mean",
        "pressure_context": "pressure question context",
        "flow_context": "flow question context",
        "names": ["pressure hold", "coolant flow", "high-temp exception"],
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
    ax.set_facecolor("white")
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_weight_chart(text: dict[str, str], weights: np.ndarray, outfile: str, focus_index: int) -> None:
    configure_font(text)
    positions = np.arange(len(weights))
    colors = ["#94a3b8"] * len(weights)
    colors[focus_index] = "#2563eb"

    fig, ax = plt.subplots(figsize=(5.9, 3.6), dpi=170)
    fig.patch.set_facecolor("white")
    style_axis(ax)

    bars = ax.bar(positions, weights, color=colors, width=0.6)
    for bar, value in zip(bars, weights):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.025,
            f"{value:.3f}",
            ha="center",
            va="bottom",
            fontsize=8.5,
            color="#111827",
        )

    ax.set_xticks(positions)
    ax.set_xticklabels(text["names"], fontsize=8.3)
    ax.set_xlabel(text["candidate_label"])
    ax.set_ylabel(text["weight_label"])
    ax.set_ylim(0, 0.86)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / outfile, format="png", bbox_inches="tight")
    plt.close(fig)


def save_context_chart(text: dict[str, str]) -> None:
    configure_font(text)
    labels = [text["baseline"], text["pressure_context"], text["flow_context"]]
    contexts = [BASELINE_CONTEXT, RETURN_CONTEXT, FLOW_CONTEXT]
    colors = ["#94a3b8", "#2563eb", "#0f766e"]

    fig, ax = plt.subplots(figsize=(5.8, 3.7), dpi=170)
    fig.patch.set_facecolor("white")
    style_axis(ax)

    bars = ax.bar(labels, contexts, color=colors, width=0.58)
    for bar, value in zip(bars, contexts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.18,
            f"{value:.3f}".rstrip("0").rstrip("."),
            ha="center",
            va="bottom",
            fontsize=8.7,
            color="#111827",
        )

    ax.set_ylabel(text["context_label"])
    ax.set_ylim(0, 11.0)
    ax.tick_params(axis="x", labelsize=8.2)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["context_outfile"], format="png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_weight_chart(text, RETURN_WEIGHTS, text["return_weight_outfile"], 0)
        save_weight_chart(text, FLOW_WEIGHTS, text["flow_weight_outfile"], 1)
        save_context_chart(text)


if __name__ == "__main__":
    main()
