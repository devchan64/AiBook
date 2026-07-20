from csv import DictReader
from pathlib import Path
import os
from typing import Union

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
DATA_PATH = OUT_DIR / "optimizer-gradient-history.csv"
LEARNING_RATE = 0.05
BETA1 = 0.8
BETA2 = 0.9
EPSILON = 1e-8
PARAMETER_ORDER = ["risk_weight", "recovery_weight", "noise_weight"]
PARAMETER_LABELS = {
    "risk_weight": "큰 gradient",
    "recovery_weight": "작은 gradient",
    "noise_weight": "흔들리는 gradient",
}
COLORS = {
    "risk_weight": "#dc2626",
    "recovery_weight": "#0f766e",
    "noise_weight": "#2563eb",
}
RowValue = Union[float, int, str]


def choose_font() -> str:
    candidates = [
        "Noto Sans CJK KR",
        "NanumGothic",
        "Apple SD Gothic Neo",
        "AppleGothic",
        "Arial Unicode MS",
        "DejaVu Sans",
    ]
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def load_rows() -> list[dict[str, RowValue]]:
    with DATA_PATH.open(newline="", encoding="utf-8") as f:
        return [
            {
                "step": int(row["step"]),
                "parameter_name": row["parameter_name"],
                "signal_group": row["signal_group"],
                "gradient": float(row["gradient"]),
            }
            for row in DictReader(f)
        ]


def group_by_parameter(rows: list[dict[str, RowValue]]) -> dict[str, list[dict[str, RowValue]]]:
    grouped = {parameter_name: [] for parameter_name in PARAMETER_ORDER}
    for row in sorted(rows, key=lambda item: (str(item["parameter_name"]), int(item["step"]))):
        grouped[str(row["parameter_name"])].append(row)
    return grouped


def simulate(rows: list[dict[str, RowValue]]) -> list[dict[str, RowValue]]:
    result = []
    state = {
        parameter_name: {"direct_weight": 1.0, "adam_like_weight": 1.0, "m": 0.0, "v": 0.0}
        for parameter_name in PARAMETER_ORDER
    }
    parameter_index = {parameter_name: index for index, parameter_name in enumerate(PARAMETER_ORDER)}
    for row in sorted(rows, key=lambda item: (int(item["step"]), parameter_index[str(item["parameter_name"])])):
        parameter_name = str(row["parameter_name"])
        gradient = float(row["gradient"])
        parameter_state = state[parameter_name]
        direct_delta = -LEARNING_RATE * gradient
        parameter_state["direct_weight"] += direct_delta
        parameter_state["m"] = BETA1 * parameter_state["m"] + (1 - BETA1) * gradient
        parameter_state["v"] = BETA2 * parameter_state["v"] + (1 - BETA2) * gradient * gradient
        adam_like_delta = -LEARNING_RATE * parameter_state["m"] / (parameter_state["v"] ** 0.5 + EPSILON)
        parameter_state["adam_like_weight"] += adam_like_delta
        result.append(
            {
                "step": int(row["step"]),
                "parameter_name": parameter_name,
                "gradient": gradient,
                "direct_delta": direct_delta,
                "adam_like_delta": adam_like_delta,
                "direct_weight": parameter_state["direct_weight"],
                "adam_like_weight": parameter_state["adam_like_weight"],
            }
        )
    return result


def style_axis(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, linestyle="--", linewidth=0.8, alpha=0.35)
    ax.set_axisbelow(True)


def configure_plot() -> None:
    plt.rcParams["font.family"] = choose_font()
    plt.rcParams["axes.unicode_minus"] = False


def save_gradient_history(grouped: dict[str, list[dict[str, RowValue]]]) -> None:
    configure_plot()
    fig, ax = plt.subplots(figsize=(7.2, 3.8), constrained_layout=True)
    for parameter_name in PARAMETER_ORDER:
        rows = grouped[parameter_name]
        steps = [int(row["step"]) for row in rows]
        gradients = [float(row["gradient"]) for row in rows]
        ax.plot(steps, gradients, marker="o", linewidth=2.2, color=COLORS[parameter_name], label=PARAMETER_LABELS[parameter_name])
    ax.axhline(0, color="#111827", linewidth=1.0)
    ax.set_xlabel("학습 step")
    ax.set_ylabel("gradient")
    ax.set_title("파라미터별 gradient 흐름")
    ax.legend(frameon=False, loc="lower right")
    style_axis(ax)
    fig.savefig(OUT_DIR / "adaptive-gradient-history-ko.png", dpi=160)
    plt.close(fig)


def save_delta_scale(simulated: list[dict[str, RowValue]]) -> None:
    configure_plot()
    direct_means = []
    adam_means = []
    for parameter_name in PARAMETER_ORDER:
        rows = [row for row in simulated if row["parameter_name"] == parameter_name]
        direct_means.append(sum(abs(float(row["direct_delta"])) for row in rows) / len(rows))
        adam_means.append(sum(abs(float(row["adam_like_delta"])) for row in rows) / len(rows))
    x_values = list(range(len(PARAMETER_ORDER)))
    width = 0.34
    fig, ax = plt.subplots(figsize=(7.2, 3.8), constrained_layout=True)
    direct_bars = ax.bar([value - width / 2 for value in x_values], direct_means, width=width, color="#2563eb", label="직접 update")
    adam_bars = ax.bar([value + width / 2 for value in x_values], adam_means, width=width, color="#0f766e", label="Adam-like")
    ax.set_xticks(x_values)
    ax.set_xticklabels([PARAMETER_LABELS[name] for name in PARAMETER_ORDER])
    ax.set_ylabel("평균 |delta|")
    ax.set_title("좌표별 평균 update 크기")
    ax.legend(frameon=False, loc="upper right")
    style_axis(ax)
    for bars in [direct_bars, adam_bars]:
        for bar in bars:
            value = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, value + 0.01, f"{value:.3g}", ha="center", fontsize=9)
    fig.savefig(OUT_DIR / "adaptive-delta-scale-ko.png", dpi=160)
    plt.close(fig)


def save_weight_trajectory(simulated: list[dict[str, RowValue]]) -> None:
    configure_plot()
    fig, axes = plt.subplots(1, 3, figsize=(10.2, 3.5), constrained_layout=True, sharey=False)
    for ax, parameter_name in zip(axes, PARAMETER_ORDER):
        rows = [row for row in simulated if row["parameter_name"] == parameter_name]
        steps = [int(row["step"]) for row in rows]
        direct_weights = [float(row["direct_weight"]) for row in rows]
        adam_weights = [float(row["adam_like_weight"]) for row in rows]
        ax.plot(steps, direct_weights, color="#2563eb", marker="o", linewidth=2.0, label="직접 update")
        ax.plot(steps, adam_weights, color="#0f766e", marker="o", linewidth=2.0, label="Adam-like")
        ax.set_title(PARAMETER_LABELS[parameter_name], fontsize=10.5)
        ax.set_xlabel("step")
        style_axis(ax)
    axes[0].set_ylabel("weight")
    axes[0].legend(frameon=False, loc="upper left")
    fig.suptitle("update 규칙별 파라미터 이동 경로", fontsize=12)
    fig.savefig(OUT_DIR / "adaptive-weight-trajectory-ko.png", dpi=160)
    plt.close(fig)


def main() -> None:
    rows = load_rows()
    grouped = group_by_parameter(rows)
    simulated = simulate(rows)
    save_gradient_history(grouped)
    save_delta_scale(simulated)
    save_weight_trajectory(simulated)


if __name__ == "__main__":
    main()
