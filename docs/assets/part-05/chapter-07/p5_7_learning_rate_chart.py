from pathlib import Path
import os
import xml.etree.ElementTree as ET
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
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

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
        "outfile": "learning-rate-step-size-ko.svg",
        "title": "학습률과 손실 곡선 위 보폭",
        "desc": "같은 기울기 방향을 얻어도 학습률이 너무 작으면 천천히 움직이고, 적절하면 낮은 손실 지점 근처로 가며, 너무 크면 목표를 지나쳐 손실이 다시 커질 수 있음을 보여 주는 좌표 그래프.",
        "xlabel": "파라미터",
        "ylabel": "손실",
        "origin": "현재 위치",
        "small": "너무 작음",
        "good": "비교적 적절",
        "large": "너무 큼",
        "valley": "손실이 낮은 근처",
        "lr_labels": ["lr=0.01", "lr=0.1", "lr=0.5"],
        "weight_ylabel": "업데이트 후 위험 가중치",
        "score_ylabel": "업데이트 후 차단 점수",
        "loss_ylabel": "업데이트 후 손실",
        "lr_xlabel": "학습률",
        "target_label": "목표",
        "step_labels": ["1단계", "2단계", "3단계"],
        "gradient_title": "입력 gradient 흐름",
        "gradient_ylabel": "gradient_risk_weight",
        "delta_title": "변환 후 step별 이동량",
        "delta_ylabel": "delta",
        "weight_title": "출력 risk_weight 이동 경로",
        "weight_ylabel_trace": "risk_weight",
        "step_xlabel": "학습 step",
        "sgd_label": "SGD",
        "adam_label": "Adam-like",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "learning-rate-step-size-en.svg",
        "title": "Learning rate and step size on a loss curve",
        "desc": "A coordinate chart showing that the same gradient direction can lead to slow movement with a very small learning rate, a useful move with an appropriate rate, or overshooting with a rate that is too large.",
        "xlabel": "parameter",
        "ylabel": "loss",
        "origin": "current position",
        "small": "too small",
        "good": "reasonable",
        "large": "too large",
        "valley": "low-loss region",
        "lr_labels": ["lr=0.01", "lr=0.1", "lr=0.5"],
        "weight_ylabel": "updated risk weight",
        "score_ylabel": "updated block score",
        "loss_ylabel": "updated loss",
        "lr_xlabel": "learning rate",
        "target_label": "target",
        "step_labels": ["step 1", "step 2", "step 3"],
        "gradient_title": "Input gradient sequence",
        "gradient_ylabel": "gradient_risk_weight",
        "delta_title": "Transformed per-step movement",
        "delta_ylabel": "delta",
        "weight_title": "Output risk_weight trajectory",
        "weight_ylabel_trace": "risk_weight",
        "step_xlabel": "training step",
        "sgd_label": "SGD",
        "adam_label": "Adam-like",
    },
}

PRESSURE_UNRECOVERED = 2.0
TARGET_BLOCK_SCORE = 6.0
RISK_WEIGHT = 1.0
LEARNING_RATES = np.array([0.01, 0.1, 0.5])
GRADIENT_HISTORY = np.array([-4.0, -2.0, -1.0])
TRACE_LEARNING_RATE = 0.1
TRACE_BETA = 0.9


def exercise_values() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    prediction = PRESSURE_UNRECOVERED * RISK_WEIGHT
    gradient_risk_weight = 2 * (prediction - TARGET_BLOCK_SCORE) * PRESSURE_UNRECOVERED
    updated_weights = RISK_WEIGHT - LEARNING_RATES * gradient_risk_weight
    updated_scores = PRESSURE_UNRECOVERED * updated_weights
    updated_losses = (updated_scores - TARGET_BLOCK_SCORE) ** 2
    return updated_weights, updated_scores, updated_losses


def choose_font(candidates: list[str]) -> str:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def configure_font(text: dict[str, str]) -> None:
    plt.rcParams["font.family"] = choose_font(text["font_candidates"])
    plt.rcParams["axes.unicode_minus"] = False


def inject_accessibility(svg_path: Path, title: str, desc: str) -> None:
    tree = ET.parse(svg_path)
    root = tree.getroot()
    root.set("role", "img")
    root.set("aria-labelledby", "title desc")

    for tag in ["title", "desc"]:
        existing = root.find(f"{{{SVG_NS}}}{tag}")
        if existing is not None:
            root.remove(existing)

    title_el = ET.Element(f"{{{SVG_NS}}}title", {"id": "title"})
    title_el.text = title
    desc_el = ET.Element(f"{{{SVG_NS}}}desc", {"id": "desc"})
    desc_el.text = desc
    root.insert(0, desc_el)
    root.insert(0, title_el)
    tree.write(svg_path, encoding="utf-8", xml_declaration=False)


def loss_curve(x: np.ndarray) -> np.ndarray:
    return 0.18 * (x - 2.2) ** 2 + 0.55 + 0.06 * np.sin(1.25 * x)


def save_chart(text: dict[str, str]) -> None:
    configure_font(text)
    x = np.linspace(0.0, 5.2, 500)
    y = loss_curve(x)
    start_x = 1.0
    step_targets = {
        text["small"]: 1.38,
        text["good"]: 2.15,
        text["large"]: 3.45,
    }
    colors = {
        text["small"]: "#2563eb",
        text["good"]: "#059669",
        text["large"]: "#dc2626",
    }
    label_offsets = {
        text["small"]: (-0.22, 0.16),
        text["good"]: (0.08, -0.12),
        text["large"]: (0.12, 0.12),
    }
    label_align = {
        text["small"]: "right",
        text["good"]: "left",
        text["large"]: "left",
    }

    fig, ax = plt.subplots(figsize=(6.5, 4.1), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.plot(x, y, color="#0f766e", linewidth=2.8)
    ax.set_xlabel(text["xlabel"])
    ax.set_ylabel(text["ylabel"])
    ax.set_xlim(0.0, 5.1)
    ax.set_ylim(y.min() - 0.28, y.max() + 0.12)

    start_y = loss_curve(np.array([start_x]))[0]
    ax.scatter([start_x], [start_y], color="#1d4ed8", s=35, zorder=4)
    ax.annotate(
        text["origin"],
        xy=(start_x, start_y),
        xytext=(0.28, start_y + 0.28),
        fontsize=8.7,
        color="#1d4ed8",
        bbox={"boxstyle": "round,pad=0.2", "facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    valley_x = x[np.argmin(y)]
    ax.axvline(valley_x, color="#cbd5e1", linewidth=1.0, linestyle=(0, (4, 4)))
    ax.text(
        valley_x - 0.18,
        y.min() - 0.2,
        text["valley"],
        fontsize=8.4,
        color="#475569",
        bbox={"boxstyle": "round,pad=0.16", "facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    for label, target_x in step_targets.items():
        target_y = loss_curve(np.array([target_x]))[0]
        ax.annotate(
            "",
            xy=(target_x, target_y),
            xytext=(start_x, start_y),
            arrowprops={"arrowstyle": "->", "color": colors[label], "lw": 2.0},
        )
        ax.scatter([target_x], [target_y], color=colors[label], s=28, zorder=4)
        dx, dy = label_offsets[label]
        ax.text(
            target_x + dx,
            target_y + dy,
            label,
            fontsize=8.5,
            color=colors[label],
            ha=label_align[label],
            bbox={"boxstyle": "round,pad=0.16", "facecolor": "white", "edgecolor": "none", "alpha": 0.92},
        )

    fig.tight_layout(pad=0.9)
    out_path = OUT_DIR / text["outfile"]
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    inject_accessibility(out_path, text["title"], text["desc"])


def style_trace_axis(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, axis="y", linestyle="--", linewidth=0.8, alpha=0.35)
    ax.set_axisbelow(True)


def save_bar_trace(values: np.ndarray, ylabel: str, filename: str, text: dict[str, str], locale: str, ylim: tuple[float, float], target: Optional[float] = None) -> None:
    configure_font(text)
    x = np.arange(len(values))
    colors = ["#2563eb", "#059669", "#dc2626"]

    fig, ax = plt.subplots(figsize=(7.2, 3.8), constrained_layout=True)
    bars = ax.bar(x, values, color=colors, width=0.48)
    if target is not None:
        ax.axhline(target, color="#0f766e", linewidth=1.4, linestyle=(0, (5, 4)), label=f"{text['target_label']}={target:.1f}")
        ax.legend(loc="upper left", frameon=False)
    for bar, value in zip(bars, values):
        offset = (ylim[1] - ylim[0]) * 0.025
        if target is not None and abs(value - target) <= offset * 2.2:
            offset = (ylim[1] - ylim[0]) * 0.006
        ax.text(bar.get_x() + bar.get_width() / 2, value + offset, f"{value:.3g}", ha="center", fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(text["lr_labels"])
    ax.set_xlabel(text["lr_xlabel"])
    ax.set_ylabel(ylabel)
    ax.set_ylim(*ylim)
    style_trace_axis(ax)
    fig.savefig(OUT_DIR / f"{filename}-{locale}.png", dpi=160)
    plt.close(fig)


def save_exercise_traces(text: dict[str, str], locale: str) -> None:
    updated_weights, updated_scores, updated_losses = exercise_values()
    save_bar_trace(
        updated_weights,
        text["weight_ylabel"],
        "optimizer-example-updated-weight",
        text,
        locale,
        (0, 9.8),
    )
    save_bar_trace(
        updated_scores,
        text["score_ylabel"],
        "optimizer-example-updated-score",
        text,
        locale,
        (0, 19.5),
        target=TARGET_BLOCK_SCORE,
    )
    save_bar_trace(
        updated_losses,
        text["loss_ylabel"],
        "optimizer-example-updated-loss",
        text,
        locale,
        (0, 154),
    )


def optimizer_trace_values() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    sgd_weight = 1.0
    adam_weight = 1.0
    moving_avg = 0.0
    sgd_deltas = []
    adam_deltas = []
    sgd_weights = []
    adam_weights = []

    for gradient in GRADIENT_HISTORY:
        sgd_delta = -TRACE_LEARNING_RATE * gradient
        sgd_weight += sgd_delta
        moving_avg = TRACE_BETA * moving_avg + (1 - TRACE_BETA) * gradient
        adam_delta = -TRACE_LEARNING_RATE * moving_avg
        adam_weight += adam_delta
        sgd_deltas.append(sgd_delta)
        adam_deltas.append(adam_delta)
        sgd_weights.append(sgd_weight)
        adam_weights.append(adam_weight)

    return (
        np.array(sgd_deltas),
        np.array(adam_deltas),
        np.array(sgd_weights),
        np.array(adam_weights),
    )


def save_gradient_history(text: dict[str, str], locale: str) -> None:
    configure_font(text)
    x = np.arange(len(GRADIENT_HISTORY))
    fig, ax = plt.subplots(figsize=(7.2, 3.8), constrained_layout=True)
    bars = ax.bar(x, GRADIENT_HISTORY, color="#475569", width=0.48)
    ax.axhline(0, color="#111827", linewidth=1.0)
    for bar, value in zip(bars, GRADIENT_HISTORY):
        ax.text(bar.get_x() + bar.get_width() / 2, value - 0.18, f"{value:.1f}", ha="center", va="top", fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(text["step_labels"])
    ax.set_xlabel(text["step_xlabel"])
    ax.set_ylabel(text["gradient_ylabel"])
    ax.set_ylim(-4.8, 0.8)
    style_trace_axis(ax)
    fig.savefig(OUT_DIR / f"sgd-adam-gradient-history-{locale}.png", dpi=160)
    plt.close(fig)


def save_delta_comparison(text: dict[str, str], locale: str) -> None:
    configure_font(text)
    sgd_deltas, adam_deltas, _sgd_weights, _adam_weights = optimizer_trace_values()
    x = np.arange(len(GRADIENT_HISTORY))
    width = 0.34
    fig, ax = plt.subplots(figsize=(7.2, 3.8), constrained_layout=True)
    ax.bar(x - width / 2, sgd_deltas, width=width, color="#2563eb", label=text["sgd_label"])
    ax.bar(x + width / 2, adam_deltas, width=width, color="#059669", label=text["adam_label"])
    for xpos, value in zip(x - width / 2, sgd_deltas):
        ax.text(xpos, value + 0.015, f"{value:.3g}", ha="center", fontsize=9)
    for xpos, value in zip(x + width / 2, adam_deltas):
        ax.text(xpos, value + 0.015, f"{value:.3g}", ha="center", fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(text["step_labels"])
    ax.set_xlabel(text["step_xlabel"])
    ax.set_ylabel(text["delta_ylabel"])
    ax.set_ylim(0, 0.46)
    ax.legend(frameon=False, loc="upper right")
    style_trace_axis(ax)
    fig.savefig(OUT_DIR / f"sgd-adam-delta-comparison-{locale}.png", dpi=160)
    plt.close(fig)


def save_weight_trajectory(text: dict[str, str], locale: str) -> None:
    configure_font(text)
    _sgd_deltas, _adam_deltas, sgd_weights, adam_weights = optimizer_trace_values()
    x = np.arange(1, len(GRADIENT_HISTORY) + 1)
    fig, ax = plt.subplots(figsize=(7.2, 3.8), constrained_layout=True)
    ax.plot(x, sgd_weights, marker="o", linewidth=2.3, color="#2563eb", label=text["sgd_label"])
    ax.plot(x, adam_weights, marker="o", linewidth=2.3, color="#059669", label=text["adam_label"])
    for xpos, value in zip(x, sgd_weights):
        ax.text(xpos, value + 0.025, f"{value:.3g}", ha="center", fontsize=9, color="#1d4ed8")
    for xpos, value in zip(x, adam_weights):
        ax.text(xpos, value - 0.055, f"{value:.3g}", ha="center", va="top", fontsize=9, color="#047857")
    ax.set_xticks(x)
    ax.set_xticklabels(text["step_labels"])
    ax.set_xlabel(text["step_xlabel"])
    ax.set_ylabel(text["weight_ylabel_trace"])
    ax.set_ylim(0.95, 1.78)
    ax.legend(frameon=False, loc="upper left")
    style_trace_axis(ax)
    fig.savefig(OUT_DIR / f"sgd-adam-risk-weight-trajectory-{locale}.png", dpi=160)
    plt.close(fig)


def save_optimizer_comparison_traces(text: dict[str, str], locale: str) -> None:
    save_gradient_history(text, locale)
    save_delta_comparison(text, locale)
    save_weight_trajectory(text, locale)


def main() -> None:
    for locale, text in LANG_TEXT.items():
        save_chart(text)
        save_exercise_traces(text, locale)
        save_optimizer_comparison_traces(text, locale)


if __name__ == "__main__":
    main()
