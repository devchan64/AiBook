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
    {"alarm_count": 1.0, "restart_delay_hours": 2.0, "target_block_score": 4.0},
    {"alarm_count": 2.0, "restart_delay_hours": 1.0, "target_block_score": 5.0},
    {"alarm_count": 3.0, "restart_delay_hours": 2.0, "target_block_score": 8.0},
    {"alarm_count": 4.0, "restart_delay_hours": 3.0, "target_block_score": 11.0},
]
INITIAL_PARAMETERS = {"alarm_weight": 0.4, "delay_weight": 0.2, "bias": 0.0}
LEARNING_RATE = 0.03
SERVICE_INPUTS = [
    {"alarm_count": 4.0, "restart_delay_hours": 1.0},
    {"alarm_count": 5.0, "restart_delay_hours": 3.0},
]

LANG_TEXT = {
    "ko": {
        "font_candidates": ["Noto Sans CJK KR", "NanumGothic", "Apple SD Gothic Neo", "AppleGothic", "Arial Unicode MS", "DejaVu Sans"],
        "training_outfile": "learning-weight-update-trace-ko.png",
        "inference_outfile": "inference-fixed-weight-trace-ko.png",
        "step_xlabel": "학습 step",
        "input_xlabel": "서비스 입력 순서",
        "weight_ylabel": "parameter value",
        "prediction_ylabel": "predicted_block_score",
        "alarm_weight": "alarm_weight",
        "delay_weight": "delay_weight",
        "bias": "bias",
        "prediction": "prediction",
        "fixed_parameter": "고정된 parameter",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "training_outfile": "learning-weight-update-trace-en.png",
        "inference_outfile": "inference-fixed-weight-trace-en.png",
        "step_xlabel": "training step",
        "input_xlabel": "service input order",
        "weight_ylabel": "parameter value",
        "prediction_ylabel": "predicted_block_score",
        "alarm_weight": "alarm_weight",
        "delay_weight": "delay_weight",
        "bias": "bias",
        "prediction": "prediction",
        "fixed_parameter": "fixed parameter",
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK KR",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "training_outfile": "learning-weight-update-trace-zh.png",
        "inference_outfile": "inference-fixed-weight-trace-zh.png",
        "step_xlabel": "训练 step",
        "input_xlabel": "服务输入顺序",
        "weight_ylabel": "parameter value",
        "prediction_ylabel": "predicted_block_score",
        "alarm_weight": "alarm_weight",
        "delay_weight": "delay_weight",
        "bias": "bias",
        "prediction": "prediction",
        "fixed_parameter": "固定 parameter",
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


def predict_block_score(alarm_count: float, restart_delay_hours: float, parameters: dict[str, float]) -> float:
    return (
        alarm_count * parameters["alarm_weight"]
        + restart_delay_hours * parameters["delay_weight"]
        + parameters["bias"]
    )


def run_train_step(sample: dict[str, float], parameters: dict[str, float]) -> dict[str, float]:
    prediction = predict_block_score(sample["alarm_count"], sample["restart_delay_hours"], parameters)
    error = prediction - sample["target_block_score"]
    gradients = {
        "alarm_weight": 2 * error * sample["alarm_count"],
        "delay_weight": 2 * error * sample["restart_delay_hours"],
        "bias": 2 * error,
    }
    parameters_after = {
        name: value - LEARNING_RATE * gradients[name]
        for name, value in parameters.items()
    }
    return {
        "prediction": prediction,
        "parameters_before": parameters.copy(),
        "parameters_after": parameters_after,
    }


def build_trace() -> tuple[list[dict[str, float]], list[dict[str, float]]]:
    parameters = INITIAL_PARAMETERS.copy()
    training_trace = []
    for step, sample in enumerate(TRAIN_ALARM_DATA, start=1):
        result = run_train_step(sample, parameters)
        training_trace.append({"step": float(step), **result})
        parameters = result["parameters_after"]

    inference_trace = [
        {
            "input_order": float(index),
            "prediction": predict_block_score(row["alarm_count"], row["restart_delay_hours"], parameters),
            "alarm_weight": parameters["alarm_weight"],
            "delay_weight": parameters["delay_weight"],
            "bias": parameters["bias"],
        }
        for index, row in enumerate(SERVICE_INPUTS, start=1)
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
    colors = {"alarm_weight": "#2563eb", "delay_weight": "#059669", "bias": "#dc2626"}
    for parameter_name, color in colors.items():
        values = [row["parameters_after"][parameter_name] for row in training_trace]
        ax.plot(steps, values, marker="o", linewidth=2.2, color=color, label=text[parameter_name])
        for step, value in zip(steps, values):
            ax.annotate(f"{value:.2f}", (step, value), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8.0, color="#172033")

    ax.set_xticks(steps)
    ax.set_ylim(0, 2.2)
    ax.set_xlabel(text["step_xlabel"])
    ax.set_ylabel(text["weight_ylabel"])
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

    input_orders = [row["input_order"] for row in inference_trace]
    predictions = [row["prediction"] for row in inference_trace]
    ax_prediction.plot(input_orders, predictions, marker="o", linewidth=2.4, color="#059669", label=text["prediction"])
    ax_prediction.set_xlabel(text["input_xlabel"])
    ax_prediction.set_ylabel(text["prediction_ylabel"], color="#059669")
    ax_prediction.tick_params(axis="y", labelcolor="#059669")
    ax_prediction.set_xticks(input_orders)
    ax_prediction.set_ylim(0, 15)
    for input_order, prediction in zip(input_orders, predictions):
        ax_prediction.annotate(f"{prediction:.2f}", (input_order, prediction), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8.5, color="#172033")

    ax_weight = ax_prediction.twinx()
    ax_weight.spines["top"].set_visible(False)
    ax_weight.plot(input_orders, [row["alarm_weight"] for row in inference_trace], marker="s", linewidth=2.0, color="#2563eb", label=text["alarm_weight"])
    ax_weight.plot(input_orders, [row["delay_weight"] for row in inference_trace], marker="s", linewidth=2.0, color="#059669", label=text["delay_weight"])
    ax_weight.plot(input_orders, [row["bias"] for row in inference_trace], marker="s", linewidth=2.0, color="#dc2626", label=text["bias"])
    ax_weight.set_ylabel(text["weight_ylabel"], color="#dc2626")
    ax_weight.tick_params(axis="y", labelcolor="#dc2626")
    ax_weight.set_ylim(0, 15)

    lines, labels = ax_prediction.get_legend_handles_labels()
    lines2, labels2 = ax_weight.get_legend_handles_labels()
    ax_prediction.legend(lines + lines2, labels + labels2, loc="upper left", frameon=False, fontsize=8.5)
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
