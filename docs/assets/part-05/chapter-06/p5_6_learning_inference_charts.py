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

TRAIN_ALARM_DATA = [
    {"alarm_count": 1.0, "target_block_score": 3.0},
    {"alarm_count": 2.0, "target_block_score": 6.0},
    {"alarm_count": 3.0, "target_block_score": 9.0},
]
INITIAL_RISK_WEIGHT = 0.5
LEARNING_RATE = 0.1
SERVICE_ALARM_COUNTS = [4.0, 5.0]

LANG_TEXT = {
    "ko": {
        "font_candidates": ["Noto Sans CJK KR", "NanumGothic", "Apple SD Gothic Neo", "AppleGothic", "Arial Unicode MS", "DejaVu Sans"],
        "training_outfile": "learning-weight-update-trace-ko.png",
        "inference_outfile": "inference-fixed-weight-trace-ko.png",
        "training_title": "학습 절차: update가 붙으면 risk_weight가 바뀐다",
        "inference_title": "모델 실행 절차: 입력과 출력은 달라도 risk_weight는 고정된다",
        "step_xlabel": "학습 step",
        "input_xlabel": "서비스 입력 alarm_count",
        "weight_ylabel": "risk_weight",
        "prediction_ylabel": "predicted_block_score",
        "weight_before": "update 전 risk_weight",
        "weight_after": "update 후 risk_weight",
        "prediction": "prediction",
        "fixed_weight": "고정된 risk_weight",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "training_outfile": "learning-weight-update-trace-en.png",
        "inference_outfile": "inference-fixed-weight-trace-en.png",
        "training_title": "Learning path: risk_weight changes when update is attached",
        "inference_title": "Inference path: predictions change while risk_weight stays fixed",
        "step_xlabel": "training step",
        "input_xlabel": "service input alarm_count",
        "weight_ylabel": "risk_weight",
        "prediction_ylabel": "predicted_block_score",
        "weight_before": "risk_weight before update",
        "weight_after": "risk_weight after update",
        "prediction": "prediction",
        "fixed_weight": "fixed risk_weight",
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


def predict_block_score(alarm_count: float, risk_weight: float) -> float:
    return alarm_count * risk_weight


def run_train_step(alarm_count: float, target_block_score: float, risk_weight: float) -> dict[str, float]:
    prediction = predict_block_score(alarm_count, risk_weight)
    gradient_risk_weight = 2 * (prediction - target_block_score) * alarm_count
    risk_weight_after = risk_weight - LEARNING_RATE * gradient_risk_weight
    return {
        "prediction": prediction,
        "risk_weight_before": risk_weight,
        "risk_weight_after": risk_weight_after,
    }


def build_trace() -> tuple[list[dict[str, float]], list[dict[str, float]]]:
    risk_weight = INITIAL_RISK_WEIGHT
    training_trace = []
    for step, sample in enumerate(TRAIN_ALARM_DATA, start=1):
        result = run_train_step(sample["alarm_count"], sample["target_block_score"], risk_weight)
        training_trace.append({"step": float(step), **result})
        risk_weight = result["risk_weight_after"]

    inference_trace = [
        {
            "alarm_count": alarm_count,
            "prediction": predict_block_score(alarm_count, risk_weight),
            "risk_weight": risk_weight,
        }
        for alarm_count in SERVICE_ALARM_COUNTS
    ]
    return training_trace, inference_trace


def style_axis(ax) -> None:
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_training_chart(text: dict[str, str], training_trace: list[dict[str, float]]) -> None:
    configure_font(text)
    fig, ax = plt.subplots(figsize=(6.4, 3.8), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    steps = [row["step"] for row in training_trace]
    weights_before = [row["risk_weight_before"] for row in training_trace]
    weights_after = [row["risk_weight_after"] for row in training_trace]
    ax.plot(steps, weights_before, marker="o", linewidth=2.0, color="#64748b", label=text["weight_before"])
    ax.plot(steps, weights_after, marker="o", linewidth=2.4, color="#2563eb", label=text["weight_after"])
    for step, after in zip(steps, weights_after):
        ax.annotate(f"{after:.2f}", (step, after), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8.5, color="#172033")

    ax.set_xticks(steps)
    ax.set_ylim(0, 3.7)
    ax.set_xlabel(text["step_xlabel"])
    ax.set_ylabel(text["weight_ylabel"])
    ax.set_title(text["training_title"], fontsize=11, fontweight="bold", pad=10)
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["training_outfile"], bbox_inches="tight")
    plt.close(fig)


def save_inference_chart(text: dict[str, str], inference_trace: list[dict[str, float]]) -> None:
    configure_font(text)
    fig, ax_prediction = plt.subplots(figsize=(6.4, 3.8), dpi=180)
    fig.patch.set_facecolor("white")
    ax_prediction.set_facecolor("white")
    style_axis(ax_prediction)

    alarm_counts = [row["alarm_count"] for row in inference_trace]
    predictions = [row["prediction"] for row in inference_trace]
    weights = [row["risk_weight"] for row in inference_trace]
    ax_prediction.plot(alarm_counts, predictions, marker="o", linewidth=2.4, color="#059669", label=text["prediction"])
    ax_prediction.set_xlabel(text["input_xlabel"])
    ax_prediction.set_ylabel(text["prediction_ylabel"], color="#059669")
    ax_prediction.tick_params(axis="y", labelcolor="#059669")
    ax_prediction.set_xticks(alarm_counts)
    ax_prediction.set_ylim(0, 18)
    for alarm_count, prediction in zip(alarm_counts, predictions):
        ax_prediction.annotate(f"{prediction:.2f}", (alarm_count, prediction), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8.5, color="#172033")

    ax_weight = ax_prediction.twinx()
    ax_weight.spines["top"].set_visible(False)
    ax_weight.plot(alarm_counts, weights, marker="s", linewidth=2.0, color="#dc2626", label=text["fixed_weight"])
    ax_weight.set_ylabel(text["weight_ylabel"], color="#dc2626")
    ax_weight.tick_params(axis="y", labelcolor="#dc2626")
    ax_weight.set_ylim(0, 18)

    lines, labels = ax_prediction.get_legend_handles_labels()
    lines2, labels2 = ax_weight.get_legend_handles_labels()
    ax_prediction.legend(lines + lines2, labels + labels2, loc="upper left", frameon=False, fontsize=8.5)
    ax_prediction.set_title(text["inference_title"], fontsize=11, fontweight="bold", pad=10)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["inference_outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    training_trace, inference_trace = build_trace()
    for text in LANG_TEXT.values():
        save_training_chart(text, training_trace)
        save_inference_chart(text, inference_trace)


if __name__ == "__main__":
    main()
