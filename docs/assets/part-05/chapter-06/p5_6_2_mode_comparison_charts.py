from pathlib import Path
import os
from random import Random

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

SESSIONS = [
    {"id": "A", "clicks": 3, "seconds": 42},
    {"id": "B", "clicks": 6, "seconds": 55},
    {"id": "C", "clicks": 2, "seconds": 28},
    {"id": "D", "clicks": 7, "seconds": 70},
    {"id": "E", "clicks": 4, "seconds": 36},
    {"id": "F", "clicks": 5, "seconds": 48},
    {"id": "G", "clicks": 1, "seconds": 24},
    {"id": "H", "clicks": 8, "seconds": 73},
    {"id": "I", "clicks": 4, "seconds": 52},
    {"id": "J", "clicks": 6, "seconds": 61},
    {"id": "K", "clicks": 2, "seconds": 33},
    {"id": "L", "clicks": 7, "seconds": 58},
    {"id": "M", "clicks": 5, "seconds": 44},
    {"id": "N", "clicks": 3, "seconds": 31},
    {"id": "O", "clicks": 9, "seconds": 80},
    {"id": "P", "clicks": 4, "seconds": 47},
    {"id": "Q", "clicks": 6, "seconds": 66},
    {"id": "R", "clicks": 2, "seconds": 39},
    {"id": "S", "clicks": 8, "seconds": 64},
    {"id": "T", "clicks": 5, "seconds": 59},
]
WEIGHTS = {"clicks": 0.18, "seconds": 0.015}
BIAS = -0.35
PRIOR_SESSION_BATCHES = [
    [{"clicks": row["clicks"], "seconds": max(12, row["seconds"] - 4)} for row in SESSIONS],
    [{"clicks": row["clicks"], "seconds": row["seconds"] + 2} for row in SESSIONS],
    [{"clicks": row["clicks"], "seconds": row["seconds"] + (3 if index % 2 == 0 else -2)} for index, row in enumerate(SESSIONS)],
]
DROP_RATE = 0.4
PASS_COUNT = 30

LANG_TEXT = {
    "ko": {
        "font_candidates": ["Noto Sans CJK KR", "NanumGothic", "Apple SD Gothic Neo", "AppleGothic", "Arial Unicode MS", "DejaVu Sans"],
        "hidden_outfile": "hidden-activation-from-sessions-ko.png",
        "centered_outfile": "mode-centered-output-comparison-ko.png",
        "dropout_outfile": "dropout-mode-output-trace-ko.png",
        "batchnorm_outfile": "batchnorm-mode-reference-trace-ko.png",
        "session_label": "세션 샘플",
        "hidden_ylabel": "은닉층 활성값",
        "centered_ylabel": "기준 평균을 뺀 출력",
        "x_label": "forward pass",
        "dropout_ylabel": "dropout 생존 비율",
        "reference_ylabel": "normalization 기준 평균",
        "hidden": "은닉층",
        "train_run_1": "train 1",
        "train_run_2": "train 2",
        "train": "training mode",
        "eval": "evaluation mode",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "hidden_outfile": "hidden-activation-from-sessions-en.png",
        "centered_outfile": "mode-centered-output-comparison-en.png",
        "dropout_outfile": "dropout-mode-output-trace-en.png",
        "batchnorm_outfile": "batchnorm-mode-reference-trace-en.png",
        "session_label": "session sample",
        "hidden_ylabel": "hidden-layer activation",
        "centered_ylabel": "output after subtracting reference mean",
        "x_label": "forward pass",
        "dropout_ylabel": "dropout survival ratio",
        "reference_ylabel": "normalization reference mean",
        "hidden": "hidden",
        "train_run_1": "train 1",
        "train_run_2": "train 2",
        "train": "training mode",
        "eval": "evaluation mode",
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


def hidden_activation(row: dict[str, int]) -> float:
    raw = row["clicks"] * WEIGHTS["clicks"] + row["seconds"] * WEIGHTS["seconds"] + BIAS
    return round(max(0.0, raw), 3)


def flatten(rows: list[list[float]]) -> list[float]:
    return [value for row in rows for value in row]


def hidden_batch(batch: list[dict[str, int]]) -> list[float]:
    return [hidden_activation(row) for row in batch]


def make_dropout_mask(count: int, seed: int) -> list[int]:
    rng = Random(seed)
    return [1 if rng.random() >= DROP_RATE else 0 for _ in range(count)]


def apply_dropout(values: list[float], mask: list[int]) -> list[float]:
    scale = 1 / (1 - DROP_RATE)
    return [0.0 if keep == 0 else round(value * scale, 3) for value, keep in zip(values, mask)]


def mean(values: list[float]) -> float:
    return round(sum(values) / len(values), 3)


def center_by_mean(values: list[float], reference_mean: float) -> list[float]:
    return [round(value - reference_mean, 3) for value in values]


def build_example_trace() -> dict:
    example_sessions = SESSIONS[:5]
    activations = [hidden_activation(row) for row in example_sessions]
    prior_session_batches = [
        [
            {"clicks": 3, "seconds": 42},
            {"clicks": 6, "seconds": 57},
            {"clicks": 2, "seconds": 27},
            {"clicks": 7, "seconds": 67},
            {"clicks": 4, "seconds": 40},
        ],
        [
            {"clicks": 3, "seconds": 38},
            {"clicks": 6, "seconds": 51},
            {"clicks": 2, "seconds": 25},
            {"clicks": 7, "seconds": 63},
            {"clicks": 4, "seconds": 45},
        ],
        [
            {"clicks": 3, "seconds": 46},
            {"clicks": 6, "seconds": 54},
            {"clicks": 2, "seconds": 29},
            {"clicks": 7, "seconds": 69},
            {"clicks": 4, "seconds": 37},
        ],
    ]
    prior_hidden_batches = [hidden_batch(batch) for batch in prior_session_batches]
    running_mean = mean(flatten(prior_hidden_batches))
    train_1 = apply_dropout(activations, make_dropout_mask(len(activations), seed=17))
    train_2 = apply_dropout(activations, make_dropout_mask(len(activations), seed=29))
    train_1_mean = mean(train_1)
    train_2_mean = mean(train_2)
    return {
        "session_ids": [row["id"] for row in example_sessions],
        "activations": activations,
        "train_run_1_centered": center_by_mean(train_1, train_1_mean),
        "train_run_2_centered": center_by_mean(train_2, train_2_mean),
        "eval_centered": center_by_mean(activations, running_mean),
    }


def build_trace() -> dict:
    activations = [hidden_activation(row) for row in SESSIONS]
    prior_hidden_batches = [hidden_batch(batch) for batch in PRIOR_SESSION_BATCHES]
    running_mean = mean(flatten(prior_hidden_batches))
    training_passes = []
    for pass_index in range(1, PASS_COUNT + 1):
        mask = make_dropout_mask(len(activations), seed=pass_index)
        after_dropout = apply_dropout(activations, mask)
        training_passes.append(
            {
                "pass": pass_index,
                "survival_ratio": sum(mask) / len(mask),
                "reference_mean": mean(after_dropout),
            }
        )
    return {
        "passes": [item["pass"] for item in training_passes],
        "survival_ratios": [item["survival_ratio"] for item in training_passes],
        "reference_means": [item["reference_mean"] for item in training_passes],
        "eval_survival_ratio": 1.0,
        "eval_reference_mean": running_mean,
    }


def style_axis(ax) -> None:
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_hidden_chart(text: dict[str, str], trace: dict) -> None:
    configure_font(text)
    positions = list(range(len(trace["session_ids"])))
    fig, ax = plt.subplots(figsize=(6.2, 3.5), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)
    bars = ax.bar(positions, trace["activations"], color="#2563eb", width=0.58, label=text["hidden"])
    for bar, value in zip(bars, trace["activations"]):
        ax.annotate(
            f"{value:.3f}".rstrip("0").rstrip("."),
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            textcoords="offset points",
            xytext=(0, 6),
            ha="center",
            fontsize=8.5,
            color="#172033",
        )
    ax.set_xticks(positions)
    ax.set_xticklabels(trace["session_ids"])
    ax.set_xlabel(text["session_label"])
    ax.set_ylabel(text["hidden_ylabel"])
    ax.set_ylim(0, max(trace["activations"]) * 1.22)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["hidden_outfile"], bbox_inches="tight")
    plt.close(fig)


def save_centered_chart(text: dict[str, str], trace: dict) -> None:
    configure_font(text)
    positions = list(range(len(trace["session_ids"])))
    width = 0.25
    fig, ax = plt.subplots(figsize=(6.8, 3.8), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)
    ax.axhline(0, color="#172033", linewidth=0.8)
    ax.bar([pos - width for pos in positions], trace["train_run_1_centered"], width=width, color="#2563eb", label=text["train_run_1"])
    ax.bar(positions, trace["train_run_2_centered"], width=width, color="#dc2626", label=text["train_run_2"])
    ax.bar([pos + width for pos in positions], trace["eval_centered"], width=width, color="#059669", label=text["eval"])
    ax.set_xticks(positions)
    ax.set_xticklabels(trace["session_ids"])
    ax.set_xlabel(text["session_label"])
    ax.set_ylabel(text["centered_ylabel"])
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["centered_outfile"], bbox_inches="tight")
    plt.close(fig)


def save_dropout_chart(text: dict[str, str], trace: dict) -> None:
    configure_font(text)
    fig, ax = plt.subplots(figsize=(6.5, 3.8), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)
    ax.plot(trace["passes"], trace["survival_ratios"], marker="o", linewidth=1.7, color="#2563eb", label=text["train"])
    ax.axhline(trace["eval_survival_ratio"], color="#059669", linewidth=2.0, linestyle=(0, (4, 3)), label=text["eval"])
    ax.set_xlabel(text["x_label"])
    ax.set_ylabel(text["dropout_ylabel"])
    ax.set_ylim(-0.05, 1.08)
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["dropout_outfile"], bbox_inches="tight")
    plt.close(fig)


def save_batchnorm_chart(text: dict[str, str], trace: dict) -> None:
    configure_font(text)
    fig, ax = plt.subplots(figsize=(6.0, 3.6), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)
    ax.plot(trace["passes"], trace["reference_means"], marker="o", linewidth=1.7, color="#2563eb", label=text["train"])
    ax.axhline(trace["eval_reference_mean"], color="#059669", linewidth=2.0, linestyle=(0, (4, 3)), label=text["eval"])
    ax.set_xlabel(text["x_label"])
    ax.set_ylabel(text["reference_ylabel"])
    ax.set_ylim(0, max(trace["reference_means"] + [trace["eval_reference_mean"]]) * 1.2)
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["batchnorm_outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    example_trace = build_example_trace()
    trace = build_trace()
    for text in LANG_TEXT.values():
        save_hidden_chart(text, example_trace)
        save_centered_chart(text, example_trace)
        save_dropout_chart(text, trace)
        save_batchnorm_chart(text, trace)


if __name__ == "__main__":
    main()
