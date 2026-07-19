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

VALIDATION_SESSIONS = [
    {"id": "S01", "clicks_5m": 3, "dwell_seconds": 42, "error_count": 0},
    {"id": "S02", "clicks_5m": 6, "dwell_seconds": 55, "error_count": 1},
    {"id": "S03", "clicks_5m": 2, "dwell_seconds": 28, "error_count": 0},
    {"id": "S04", "clicks_5m": 7, "dwell_seconds": 70, "error_count": 2},
    {"id": "S05", "clicks_5m": 4, "dwell_seconds": 36, "error_count": 0},
    {"id": "S06", "clicks_5m": 5, "dwell_seconds": 48, "error_count": 1},
    {"id": "S07", "clicks_5m": 1, "dwell_seconds": 24, "error_count": 0},
    {"id": "S08", "clicks_5m": 8, "dwell_seconds": 73, "error_count": 2},
    {"id": "S09", "clicks_5m": 4, "dwell_seconds": 52, "error_count": 1},
    {"id": "S10", "clicks_5m": 6, "dwell_seconds": 61, "error_count": 0},
    {"id": "S11", "clicks_5m": 2, "dwell_seconds": 39, "error_count": 1},
    {"id": "S12", "clicks_5m": 7, "dwell_seconds": 58, "error_count": 2},
]
WEIGHTS = {"clicks_5m": 0.18, "dwell_seconds": 0.015, "error_count": 0.32}
BIAS = -0.35
DROP_RATE = 0.4
PASS_COUNT = 30


def make_prior_batch(rows: list[dict], dwell_shift: int, error_shift: int) -> list[dict[str, int]]:
    batch = []
    for row in rows:
        batch.append(
            {
                "clicks_5m": int(row["clicks_5m"]),
                "dwell_seconds": max(12, int(row["dwell_seconds"]) + dwell_shift),
                "error_count": max(0, int(row["error_count"]) + error_shift),
            }
        )
    return batch


PRIOR_SESSION_BATCHES = [
    make_prior_batch(VALIDATION_SESSIONS, dwell_shift=-4, error_shift=0),
    make_prior_batch(VALIDATION_SESSIONS, dwell_shift=2, error_shift=1),
    make_prior_batch(VALIDATION_SESSIONS, dwell_shift=5, error_shift=-1),
]

LANG_TEXT = {
    "ko": {
        "font_candidates": ["Noto Sans CJK KR", "NanumGothic", "Apple SD Gothic Neo", "AppleGothic", "Arial Unicode MS", "DejaVu Sans"],
        "hidden_outfile": "hidden-activation-from-sessions-ko.png",
        "centered_outfile": "mode-centered-output-comparison-ko.png",
        "dropout_outfile": "dropout-mode-output-trace-ko.png",
        "batchnorm_outfile": "batchnorm-mode-reference-trace-ko.png",
        "session_label": "검증 세션",
        "hidden_ylabel": "은닉층 활성값",
        "centered_ylabel": "기준 평균을 뺀 출력",
        "x_label": "forward pass",
        "dropout_ylabel": "dropout 생존 비율",
        "reference_ylabel": "normalization 기준 평균",
        "hidden": "은닉층",
        "train_run_1": "train 1",
        "train_run_2": "train 2",
        "train": "학습 모드",
        "eval": "평가 모드",
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
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK KR",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "hidden_outfile": "hidden-activation-from-sessions-zh.png",
        "centered_outfile": "mode-centered-output-comparison-zh.png",
        "dropout_outfile": "dropout-mode-output-trace-zh.png",
        "batchnorm_outfile": "batchnorm-mode-reference-trace-zh.png",
        "session_label": "会话样本",
        "hidden_ylabel": "隐藏层激活值",
        "centered_ylabel": "减去参考均值后的输出",
        "x_label": "forward pass",
        "dropout_ylabel": "dropout 保留比例",
        "reference_ylabel": "normalization 参考均值",
        "hidden": "隐藏层",
        "train_run_1": "train 1",
        "train_run_2": "train 2",
        "train": "训练模式",
        "eval": "评估模式",
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


def hidden_activation(row: dict) -> float:
    raw = (
        int(row["clicks_5m"]) * WEIGHTS["clicks_5m"]
        + int(row["dwell_seconds"]) * WEIGHTS["dwell_seconds"]
        + int(row["error_count"]) * WEIGHTS["error_count"]
        + BIAS
    )
    return round(max(0.0, raw), 3)


def flatten(rows: list[list[float]]) -> list[float]:
    return [value for row in rows for value in row]


def hidden_batch(batch: list[dict]) -> list[float]:
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
    example_sessions = VALIDATION_SESSIONS
    activations = [hidden_activation(row) for row in example_sessions]
    prior_hidden_batches = [hidden_batch(batch) for batch in PRIOR_SESSION_BATCHES]
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
    activations = [hidden_activation(row) for row in VALIDATION_SESSIONS]
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
    fig, ax = plt.subplots(figsize=(7.2, 3.8), dpi=180)
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
    ax.set_xticklabels(trace["session_ids"], rotation=35, ha="right")
    ax.set_xlabel(text["session_label"])
    ax.set_ylabel(text["hidden_ylabel"])
    ax.set_ylim(0, max(trace["activations"]) * 1.22)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["hidden_outfile"], bbox_inches="tight")
    plt.close(fig)


def save_centered_chart(text: dict[str, str], trace: dict) -> None:
    configure_font(text)
    positions = list(range(len(trace["session_ids"])))
    width = 0.24
    fig, ax = plt.subplots(figsize=(8.2, 4.1), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)
    ax.axhline(0, color="#172033", linewidth=0.8)
    ax.bar([pos - width for pos in positions], trace["train_run_1_centered"], width=width, color="#2563eb", label=text["train_run_1"])
    ax.bar(positions, trace["train_run_2_centered"], width=width, color="#dc2626", label=text["train_run_2"])
    ax.bar([pos + width for pos in positions], trace["eval_centered"], width=width, color="#059669", label=text["eval"])
    ax.set_xticks(positions)
    ax.set_xticklabels(trace["session_ids"], rotation=35, ha="right")
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
