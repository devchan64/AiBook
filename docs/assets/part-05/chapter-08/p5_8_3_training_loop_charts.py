from pathlib import Path
import os
from typing import Optional

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

BATCHES = [
    [
        {"alarm_count": 1.0, "target_block_score": 2.0},
        {"alarm_count": 2.0, "target_block_score": 4.0},
    ],
    [
        {"alarm_count": 3.0, "target_block_score": 6.0},
        {"alarm_count": 4.0, "target_block_score": 8.0},
    ],
]
INITIAL_RISK_WEIGHT = 0.5
LEARNING_RATE = 0.1

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
        "prediction_outfile": "training-loop-predictions-ko.png",
        "loss_outfile": "training-loop-batch-loss-ko.png",
        "gradient_outfile": "training-loop-batch-gradient-ko.png",
        "weight_outfile": "training-loop-risk-weight-update-ko.png",
        "batch": "batch",
        "sample": "sample",
        "prediction": "예측 차단 점수",
        "target": "목표 차단 점수",
        "loss": "평균 loss",
        "gradient": "평균 gradient",
        "risk_weight": "risk_weight",
        "start": "시작",
        "after_batch": "batch 뒤",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "prediction_outfile": "training-loop-predictions-en.png",
        "loss_outfile": "training-loop-batch-loss-en.png",
        "gradient_outfile": "training-loop-batch-gradient-en.png",
        "weight_outfile": "training-loop-risk-weight-update-en.png",
        "batch": "batch",
        "sample": "sample",
        "prediction": "predicted block score",
        "target": "target block score",
        "loss": "mean loss",
        "gradient": "mean gradient",
        "risk_weight": "risk_weight",
        "start": "start",
        "after_batch": "after batch",
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


def compute_trace() -> dict[str, list]:
    risk_weight = INITIAL_RISK_WEIGHT
    trace = {
        "predictions": [],
        "targets": [],
        "losses": [],
        "gradients": [],
        "weights": [risk_weight],
    }

    for batch in BATCHES:
        predictions = []
        targets = []
        losses = []
        gradients = []

        for sample in batch:
            alarm_count = sample["alarm_count"]
            target_block_score = sample["target_block_score"]

            prediction = risk_weight * alarm_count
            loss = (prediction - target_block_score) ** 2
            gradient_risk_weight = 2 * (prediction - target_block_score) * alarm_count

            predictions.append(prediction)
            targets.append(target_block_score)
            losses.append(loss)
            gradients.append(gradient_risk_weight)

        batch_gradient = sum(gradients) / len(gradients)
        risk_weight = risk_weight - LEARNING_RATE * batch_gradient

        trace["predictions"].append(predictions)
        trace["targets"].append(targets)
        trace["losses"].append(sum(losses) / len(losses))
        trace["gradients"].append(batch_gradient)
        trace["weights"].append(risk_weight)

    return trace


def style_axis(ax) -> None:
    ax.set_facecolor("white")
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def format_value(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".")


def save_predictions(text: dict[str, str], trace: dict[str, list]) -> None:
    configure_font(text)
    labels = []
    predictions = []
    targets = []
    for batch_index, (batch_predictions, batch_targets) in enumerate(
        zip(trace["predictions"], trace["targets"]), start=1
    ):
        for sample_index, (prediction, target) in enumerate(zip(batch_predictions, batch_targets), start=1):
            labels.append(f"{text['batch']} {batch_index}\n{text['sample']} {sample_index}")
            predictions.append(prediction)
            targets.append(target)

    x = np.arange(len(labels))
    width = 0.34

    fig, ax = plt.subplots(figsize=(6.4, 3.7), dpi=170)
    fig.patch.set_facecolor("white")
    style_axis(ax)

    ax.bar(x - width / 2, predictions, width, label=text["prediction"], color="#2563eb")
    ax.bar(x + width / 2, targets, width, label=text["target"], color="#94a3b8")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8.5)
    ax.set_ylabel(text["prediction"])
    ax.set_ylim(0, 8.8)
    ax.legend(frameon=False, loc="upper left", fontsize=8.2)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["prediction_outfile"], format="png", bbox_inches="tight")
    plt.close(fig)


def save_single_series(
    text: dict[str, str],
    values: list[float],
    outfile_key: str,
    ylabel_key: str,
    color: str,
    ylim: Optional[tuple[float, float]] = None,
) -> None:
    configure_font(text)
    labels = [f"{text['batch']} {i}" for i in range(1, len(values) + 1)]

    fig, ax = plt.subplots(figsize=(5.4, 3.4), dpi=170)
    fig.patch.set_facecolor("white")
    style_axis(ax)

    bars = ax.bar(labels, values, color=color, width=0.58)
    for bar, value in zip(bars, values):
        offset = 0.18 if value >= 0 else -0.8
        va = "bottom" if value >= 0 else "top"
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + offset,
            format_value(value),
            ha="center",
            va=va,
            fontsize=9,
            color="#111827",
        )

    ax.axhline(0, color="#111827", linewidth=0.8)
    ax.set_ylabel(text[ylabel_key])
    if ylim is not None:
        ax.set_ylim(*ylim)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text[outfile_key], format="png", bbox_inches="tight")
    plt.close(fig)


def save_weight_trace(text: dict[str, str], trace: dict[str, list]) -> None:
    configure_font(text)
    weights = trace["weights"]
    labels = [text["start"]] + [f"{text['after_batch']} {i}" for i in range(1, len(weights))]
    x = np.arange(len(weights))

    fig, ax = plt.subplots(figsize=(5.8, 3.4), dpi=170)
    fig.patch.set_facecolor("white")
    style_axis(ax)

    ax.plot(x, weights, color="#16a34a", linewidth=2.4, marker="o", markersize=5.2)
    for index, value in enumerate(weights):
        ax.text(index, value + 0.12, format_value(value), ha="center", va="bottom", fontsize=9, color="#14532d")

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8.5)
    ax.set_ylabel(text["risk_weight"])
    ax.set_ylim(0, 3.6)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["weight_outfile"], format="png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    trace = compute_trace()
    for text in LANG_TEXT.values():
        save_predictions(text, trace)
        save_single_series(text, trace["losses"], "loss_outfile", "loss", "#f97316", (0, 8.2))
        save_single_series(text, trace["gradients"], "gradient_outfile", "gradient", "#dc2626", (-22, 2))
        save_weight_trace(text, trace)


if __name__ == "__main__":
    main()
