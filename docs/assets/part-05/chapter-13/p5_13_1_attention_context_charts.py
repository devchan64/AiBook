from __future__ import annotations

from pathlib import Path
import csv
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
DATA_PATH = OUT_DIR / "attention-operating-manual-candidates.csv"
QUESTIONS = {
    "pressure": {
        "score_column": "score_pressure_hold",
        "ko": "압력 해소 유지 시간 질문",
        "en": "pressure-hold-time question",
        "zh": "压力释放保持时间问题",
    },
    "flow": {
        "score_column": "score_flow_limit",
        "ko": "냉각수 유량 기준 질문",
        "en": "coolant-flow question",
        "zh": "冷却水流量标准问题",
    },
    "restart": {
        "score_column": "score_restart_permission",
        "ko": "재기동 승인 조건 질문",
        "en": "restart-approval question",
        "zh": "重启批准条件问题",
    },
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
        "pressure_weight_outfile": "attention-pressure-question-weights-ko.png",
        "flow_weight_outfile": "attention-flow-question-weights-ko.png",
        "context_outfile": "attention-context-comparison-ko.png",
        "weight_label": "attention 비중",
        "candidate_label": "상위 후보 줄",
        "context_label": "문맥값",
        "baseline": "baseline 평균",
        "pressure_context": "압력 질문 context",
        "flow_context": "유량 질문 context",
        "restart_context": "재기동 질문 context",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "pressure_weight_outfile": "attention-pressure-question-weights-en.png",
        "flow_weight_outfile": "attention-flow-question-weights-en.png",
        "context_outfile": "attention-context-comparison-en.png",
        "weight_label": "attention weight",
        "candidate_label": "top candidate line",
        "context_label": "context value",
        "baseline": "baseline mean",
        "pressure_context": "pressure context",
        "flow_context": "flow context",
        "restart_context": "restart context",
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK JP",
            "Source Han Sans SC",
            "Microsoft YaHei",
            "PingFang SC",
            "Songti SC",
            "Heiti SC",
            "Heiti TC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "pressure_weight_outfile": "attention-pressure-question-weights-zh.png",
        "flow_weight_outfile": "attention-flow-question-weights-zh.png",
        "context_outfile": "attention-context-comparison-zh.png",
        "weight_label": "attention 权重",
        "candidate_label": "最高候选行",
        "context_label": "上下文值",
        "baseline": "baseline 平均",
        "pressure_context": "压力问题 context",
        "flow_context": "流量问题 context",
        "restart_context": "重启问题 context",
    },
}


def load_rows() -> list[dict[str, str]]:
    with DATA_PATH.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def softmax(scores: list[float]) -> np.ndarray:
    max_score = max(scores)
    shifted = [math.exp(score - max_score) for score in scores]
    total = sum(shifted)
    return np.array([score / total for score in shifted])


ROWS = load_rows()
VALUES = np.array([float(row["evidence_signal"]) for row in ROWS])
BASELINE_CONTEXT = float(np.mean(VALUES))
QUESTION_WEIGHTS = {
    name: softmax([float(row[config["score_column"]]) for row in ROWS])
    for name, config in QUESTIONS.items()
}
QUESTION_CONTEXTS = {
    name: float(np.sum(weights * VALUES))
    for name, weights in QUESTION_WEIGHTS.items()
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
    ax.grid(True, axis="x", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_weight_chart(text: dict[str, str], question_name: str, outfile: str) -> None:
    configure_font(text)
    weights = QUESTION_WEIGHTS[question_name]
    top_indexes = sorted(range(len(weights)), key=lambda index: (-weights[index], index))[:8]
    labels = [ROWS[index]["line_id"] for index in top_indexes]
    top_weights = [weights[index] for index in top_indexes]
    colors = ["#2563eb" if i == 0 else "#94a3b8" for i in range(len(top_indexes))]

    fig, ax = plt.subplots(figsize=(6.2, 3.9), dpi=170)
    fig.patch.set_facecolor("white")
    style_axis(ax)

    positions = np.arange(len(top_indexes))
    bars = ax.barh(positions, top_weights, color=colors, height=0.62)
    for bar, value in zip(bars, top_weights):
        ax.text(
            value + 0.004,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.3f}",
            ha="left",
            va="center",
            fontsize=8.5,
            color="#111827",
        )

    ax.set_yticks(positions)
    ax.set_yticklabels(labels, fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlabel(text["weight_label"])
    ax.set_ylabel(text["candidate_label"])
    ax.set_xlim(0, max(top_weights) * 1.24)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / outfile, format="png", bbox_inches="tight")
    plt.close(fig)


def save_context_chart(text: dict[str, str]) -> None:
    configure_font(text)
    labels = [
        text["baseline"],
        text["pressure_context"],
        text["flow_context"],
        text["restart_context"],
    ]
    contexts = [
        BASELINE_CONTEXT,
        QUESTION_CONTEXTS["pressure"],
        QUESTION_CONTEXTS["flow"],
        QUESTION_CONTEXTS["restart"],
    ]
    colors = ["#94a3b8", "#2563eb", "#0f766e", "#7c3aed"]

    fig, ax = plt.subplots(figsize=(6.1, 3.7), dpi=170)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    bars = ax.bar(labels, contexts, color=colors, width=0.58)
    for bar, value in zip(bars, contexts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.16,
            f"{value:.3f}".rstrip("0").rstrip("."),
            ha="center",
            va="bottom",
            fontsize=8.7,
            color="#111827",
        )

    ax.set_ylabel(text["context_label"])
    ax.set_ylim(0, max(contexts) * 1.18)
    ax.tick_params(axis="x", labelsize=8.0)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["context_outfile"], format="png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_weight_chart(text, "pressure", text["pressure_weight_outfile"])
        save_weight_chart(text, "flow", text["flow_weight_outfile"])
        save_context_chart(text)


if __name__ == "__main__":
    main()
