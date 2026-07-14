from pathlib import Path
import os
import xml.etree.ElementTree as ET

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
        "loss_shapes_out": "loss-shapes-ko.svg",
        "squared_loss_out": "squared-error-loss-ko.svg",
        "cross_entropy_loss_out": "cross-entropy-loss-ko.svg",
        "problem_axes_out": "problem-loss-axes-ko.svg",
        "regression_axis_out": "regression-loss-axis-ko.svg",
        "classification_axis_out": "classification-loss-axis-ko.svg",
        "generation_axis_out": "generation-loss-axis-ko.svg",
        "batch_priority_out": "loss-example-batch-priority-ko.svg",
        "regression_experiment_out": "loss-example-regression-experiment-ko.svg",
        "classification_experiment_out": "loss-example-classification-experiment-ko.svg",
        "generation_experiment_out": "loss-example-generation-experiment-ko.svg",
        "loss_shapes_title": "제곱오차와 cross-entropy 손실 모양",
        "loss_shapes_desc": "회귀에서는 목표값에서 멀어질수록 손실이 커지고, 분류에서는 정답 클래스 확률이 낮을수록 손실이 커지는 모습을 나란히 보여 주는 좌표 그래프.",
        "squared_loss_title": "제곱오차 손실 모양",
        "squared_loss_desc": "목표값에서 멀어질수록 제곱오차 손실이 더 가파르게 커지는 모습을 보여 주는 좌표 그래프.",
        "cross_entropy_loss_title": "cross-entropy 손실 모양",
        "cross_entropy_loss_desc": "정답 클래스에 준 확률이 낮을수록 cross-entropy 손실이 빠르게 커지는 모습을 보여 주는 좌표 그래프.",
        "problem_axes_title": "문제 유형별 손실 읽기 축",
        "problem_axes_desc": "회귀, 분류, 생성이 각각 정답 숫자와의 거리, 정답 클래스 확률, 위치별 정답 토큰 확률이라는 서로 다른 축에서 손실을 읽는다는 점을 비교하는 좌표 그래프.",
        "regression_axis_title": "회귀 손실 읽기 축",
        "regression_axis_desc": "회귀 문제에서 손실이 정답 숫자와의 거리를 중심으로 읽힌다는 점을 보여 주는 좌표 그래프.",
        "classification_axis_title": "분류 손실 읽기 축",
        "classification_axis_desc": "분류 문제에서 손실이 정답 클래스 확률을 중심으로 읽힌다는 점을 보여 주는 좌표 그래프.",
        "generation_axis_title": "생성 손실 읽기 축",
        "generation_axis_desc": "생성 문제에서 손실이 위치별 정답 토큰 확률을 누적해 읽힌다는 점을 보여 주는 막대 그래프.",
        "batch_priority_title": "배치 보정 후보별 평균 손실과 worst case",
        "batch_priority_desc": "현재 상태, restart_delay_batch 보정, night_shift_batch 보정에서 평균 손실과 가장 큰 샘플 손실이 어떻게 달라지는지 비교하는 막대 그래프.",
        "regression_experiment_title": "회귀 예측 보정 전후 손실",
        "regression_experiment_desc": "에너지 사용량 예측을 정답에 가깝게 옮기면 회귀 손실이 줄어드는 모습을 보여 주는 막대 그래프.",
        "classification_experiment_title": "분류 정답 확률 보정 전후 손실",
        "classification_experiment_desc": "정답 클래스 확률을 올리면 분류 손실이 줄어드는 모습을 보여 주는 막대 그래프.",
        "generation_experiment_title": "생성 정답 토큰 확률 보정 전후 손실",
        "generation_experiment_desc": "정답 토큰 확률을 올리면 생성 손실이 줄어드는 모습을 보여 주는 막대 그래프.",
        "regression_panel": "회귀: 제곱오차",
        "classification_panel": "분류: cross-entropy 직관",
        "loss_ylabel": "손실",
        "regression_xlabel": "목표값에서 떨어진 거리",
        "classification_xlabel": "정답 클래스에 준 확률",
        "small_error": "작은 오차",
        "large_error": "큰 오차",
        "low_true_prob": "정답 확률 낮음",
        "high_true_prob": "정답 확률 높음",
        "problem_panels": [
            ("회귀", "정답 숫자와의 거리"),
            ("분류", "정답 클래스 확률"),
            ("생성", "위치별 정답 토큰 확률"),
        ],
        "token_labels": ["t1", "t2", "t3", "t4"],
        "scenario_labels": ["현재", "restart\n보정", "night\n보정"],
        "current_fix_labels": ["현재", "보정 후"],
        "mean_loss_label": "평균 손실",
        "worst_loss_label": "worst 손실",
        "regression_loss_label": "회귀 손실",
        "classification_loss_label": "분류 손실",
        "generation_loss_label": "생성 손실",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "loss_shapes_out": "loss-shapes-en.svg",
        "squared_loss_out": "squared-error-loss-en.svg",
        "cross_entropy_loss_out": "cross-entropy-loss-en.svg",
        "problem_axes_out": "problem-loss-axes-en.svg",
        "regression_axis_out": "regression-loss-axis-en.svg",
        "classification_axis_out": "classification-loss-axis-en.svg",
        "generation_axis_out": "generation-loss-axis-en.svg",
        "batch_priority_out": "loss-example-batch-priority-en.svg",
        "regression_experiment_out": "loss-example-regression-experiment-en.svg",
        "classification_experiment_out": "loss-example-classification-experiment-en.svg",
        "generation_experiment_out": "loss-example-generation-experiment-en.svg",
        "loss_shapes_title": "Squared-error and cross-entropy loss shapes",
        "loss_shapes_desc": "A coordinate chart showing that regression loss grows as predictions move farther from the target, while classification loss grows as the true-class probability gets smaller.",
        "squared_loss_title": "Squared-error loss shape",
        "squared_loss_desc": "A coordinate chart showing that squared-error loss rises more steeply as predictions move farther from the target value.",
        "cross_entropy_loss_title": "Cross-entropy loss shape",
        "cross_entropy_loss_desc": "A coordinate chart showing that cross-entropy loss rises quickly as the probability assigned to the true class gets smaller.",
        "problem_axes_title": "Loss-reading axes by problem type",
        "problem_axes_desc": "A coordinate chart comparing how regression, classification, and generation read loss on different axes: distance from the target value, true-class probability, and per-position true-token probability.",
        "regression_axis_title": "Regression loss-reading axis",
        "regression_axis_desc": "A coordinate chart showing that regression loss is read primarily on the distance from the target value.",
        "classification_axis_title": "Classification loss-reading axis",
        "classification_axis_desc": "A coordinate chart showing that classification loss is read primarily on the probability assigned to the true class.",
        "generation_axis_title": "Generation loss-reading axis",
        "generation_axis_desc": "A bar chart showing that generation loss is read by accumulating true-token probabilities across positions.",
        "batch_priority_title": "Mean loss and worst case by batch-fix candidate",
        "batch_priority_desc": "A bar chart comparing how mean loss and the largest sample loss change in the current state, after fixing restart_delay_batch, and after fixing night_shift_batch.",
        "regression_experiment_title": "Regression loss before and after prediction repair",
        "regression_experiment_desc": "A bar chart showing that regression loss drops when the energy prediction moves closer to the target.",
        "classification_experiment_title": "Classification loss before and after true-class probability repair",
        "classification_experiment_desc": "A bar chart showing that classification loss drops when the probability assigned to the true class increases.",
        "generation_experiment_title": "Generation loss before and after true-token probability repair",
        "generation_experiment_desc": "A bar chart showing that generation loss drops when the probability assigned to the true next token increases.",
        "regression_panel": "Regression: squared error",
        "classification_panel": "Classification: cross-entropy intuition",
        "loss_ylabel": "loss",
        "regression_xlabel": "distance from target value",
        "classification_xlabel": "probability assigned to true class",
        "small_error": "small error",
        "large_error": "large error",
        "low_true_prob": "low true-class probability",
        "high_true_prob": "high true-class probability",
        "problem_panels": [
            ("Regression", "distance from target value"),
            ("Classification", "true-class probability"),
            ("Generation", "per-position true-token probability"),
        ],
        "token_labels": ["t1", "t2", "t3", "t4"],
        "scenario_labels": ["current", "fix\nrestart", "fix\nnight"],
        "current_fix_labels": ["current", "after fix"],
        "mean_loss_label": "mean loss",
        "worst_loss_label": "worst loss",
        "regression_loss_label": "regression loss",
        "classification_loss_label": "classification loss",
        "generation_loss_label": "generation loss",
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


def save_loss_shapes(text: dict[str, str]) -> None:
    configure_font(text)
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.2), dpi=160)
    fig.patch.set_facecolor("white")

    distance = np.linspace(-3.2, 3.2, 500)
    squared_error = distance**2
    axes[0].set_facecolor("#f8fafc")
    axes[0].grid(True, color="#d0d7de", linewidth=0.75, alpha=0.82)
    axes[0].set_axisbelow(True)
    axes[0].spines["top"].set_visible(False)
    axes[0].spines["right"].set_visible(False)
    axes[0].plot(distance, squared_error, color="#2563eb", linewidth=2.4)
    axes[0].axvline(0, color="#94a3b8", linewidth=1.0, linestyle=(0, (4, 4)))
    axes[0].set_xlabel(text["regression_xlabel"])
    axes[0].set_ylabel(text["loss_ylabel"])
    axes[0].set_xlim(-3.3, 3.3)
    axes[0].set_ylim(0, 10.4)
    axes[0].scatter([0.6, 2.3], [0.36, 5.29], color=["#0f766e", "#b91c1c"], s=30, zorder=3)
    axes[0].annotate(
        text["small_error"],
        xy=(0.6, 0.36),
        xytext=(1.2, 1.8),
        fontsize=8.7,
        color="#0f766e",
        bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": "none", "alpha": 0.92},
        arrowprops={"arrowstyle": "-", "color": "#0f766e", "lw": 1.0},
    )
    axes[0].annotate(
        text["large_error"],
        xy=(2.3, 5.29),
        xytext=(1.45, 7.7),
        fontsize=8.7,
        color="#b91c1c",
        bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": "none", "alpha": 0.92},
        arrowprops={"arrowstyle": "-", "color": "#b91c1c", "lw": 1.0},
    )

    true_prob = np.linspace(0.02, 0.99, 500)
    cross_entropy = -np.log(true_prob)
    axes[1].set_facecolor("#f8fafc")
    axes[1].grid(True, color="#d0d7de", linewidth=0.75, alpha=0.82)
    axes[1].set_axisbelow(True)
    axes[1].spines["top"].set_visible(False)
    axes[1].spines["right"].set_visible(False)
    axes[1].plot(true_prob, cross_entropy, color="#dc2626", linewidth=2.4)
    axes[1].set_xlabel(text["classification_xlabel"])
    axes[1].set_ylabel(text["loss_ylabel"])
    axes[1].set_xlim(0.0, 1.02)
    axes[1].set_ylim(0, 4.8)
    axes[1].scatter([0.08, 0.9], [-np.log(0.08), -np.log(0.9)], color=["#b91c1c", "#0f766e"], s=30, zorder=3)
    axes[1].annotate(
        text["low_true_prob"],
        xy=(0.08, -np.log(0.08)),
        xytext=(0.22, 3.45),
        fontsize=8.7,
        color="#b91c1c",
        bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": "none", "alpha": 0.92},
        arrowprops={"arrowstyle": "-", "color": "#b91c1c", "lw": 1.0},
    )
    axes[1].annotate(
        text["high_true_prob"],
        xy=(0.9, -np.log(0.9)),
        xytext=(0.54, 0.95),
        fontsize=8.7,
        color="#0f766e",
        bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": "none", "alpha": 0.92},
        arrowprops={"arrowstyle": "-", "color": "#0f766e", "lw": 1.0},
    )

    fig.tight_layout(pad=1.0, w_pad=1.5)
    out_path = OUT_DIR / text["loss_shapes_out"]
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    inject_accessibility(out_path, text["loss_shapes_title"], text["loss_shapes_desc"])


def save_squared_error_loss(text: dict[str, str]) -> None:
    configure_font(text)
    fig, ax = plt.subplots(figsize=(4.4, 4.2), dpi=160)
    fig.patch.set_facecolor("white")

    distance = np.linspace(-3.2, 3.2, 500)
    squared_error = distance**2
    ax.set_facecolor("#f8fafc")
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.82)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.plot(distance, squared_error, color="#2563eb", linewidth=2.4)
    ax.axvline(0, color="#94a3b8", linewidth=1.0, linestyle=(0, (4, 4)))
    ax.set_xlabel(text["regression_xlabel"])
    ax.set_ylabel(text["loss_ylabel"])
    ax.set_xlim(-3.3, 3.3)
    ax.set_ylim(0, 10.4)
    ax.scatter([0.6, 2.3], [0.36, 5.29], color=["#0f766e", "#b91c1c"], s=30, zorder=3)
    ax.annotate(
        text["small_error"],
        xy=(0.6, 0.36),
        xytext=(1.2, 1.8),
        fontsize=8.7,
        color="#0f766e",
        bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": "none", "alpha": 0.92},
        arrowprops={"arrowstyle": "-", "color": "#0f766e", "lw": 1.0},
    )
    ax.annotate(
        text["large_error"],
        xy=(2.3, 5.29),
        xytext=(1.45, 7.7),
        fontsize=8.7,
        color="#b91c1c",
        bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": "none", "alpha": 0.92},
        arrowprops={"arrowstyle": "-", "color": "#b91c1c", "lw": 1.0},
    )

    fig.tight_layout(pad=1.0)
    out_path = OUT_DIR / text["squared_loss_out"]
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    inject_accessibility(out_path, text["squared_loss_title"], text["squared_loss_desc"])


def save_cross_entropy_loss(text: dict[str, str]) -> None:
    configure_font(text)
    fig, ax = plt.subplots(figsize=(4.4, 4.2), dpi=160)
    fig.patch.set_facecolor("white")

    true_prob = np.linspace(0.02, 0.99, 500)
    cross_entropy = -np.log(true_prob)
    ax.set_facecolor("#f8fafc")
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.82)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.plot(true_prob, cross_entropy, color="#dc2626", linewidth=2.4)
    ax.set_xlabel(text["classification_xlabel"])
    ax.set_ylabel(text["loss_ylabel"])
    ax.set_xlim(0.0, 1.02)
    ax.set_ylim(0, 4.8)
    ax.scatter([0.08, 0.9], [-np.log(0.08), -np.log(0.9)], color=["#b91c1c", "#0f766e"], s=30, zorder=3)
    ax.annotate(
        text["low_true_prob"],
        xy=(0.08, -np.log(0.08)),
        xytext=(0.22, 3.45),
        fontsize=8.7,
        color="#b91c1c",
        bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": "none", "alpha": 0.92},
        arrowprops={"arrowstyle": "-", "color": "#b91c1c", "lw": 1.0},
    )
    ax.annotate(
        text["high_true_prob"],
        xy=(0.9, -np.log(0.9)),
        xytext=(0.54, 0.95),
        fontsize=8.7,
        color="#0f766e",
        bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": "none", "alpha": 0.92},
        arrowprops={"arrowstyle": "-", "color": "#0f766e", "lw": 1.0},
    )

    fig.tight_layout(pad=1.0)
    out_path = OUT_DIR / text["cross_entropy_loss_out"]
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    inject_accessibility(out_path, text["cross_entropy_loss_title"], text["cross_entropy_loss_desc"])


def save_problem_axes(text: dict[str, str]) -> None:
    configure_font(text)
    fig, axes = plt.subplots(1, 3, figsize=(9.9, 4.4), dpi=160)
    fig.patch.set_facecolor("white")

    z = np.linspace(-3.1, 3.1, 500)
    regression_curve = z**2
    classification_prob = np.linspace(0.02, 0.99, 500)
    classification_curve = -np.log(classification_prob)
    token_positions = np.array([1, 2, 3, 4])
    token_confidence = np.array([0.08, 0.22, 0.12, 0.71])
    token_loss = -np.log(token_confidence)

    for ax in axes:
        ax.set_facecolor("#f8fafc")
        ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.82)
        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_ylabel(text["loss_ylabel"])

    title, xlabel = text["problem_panels"][0]
    axes[0].plot(z, regression_curve, color="#2563eb", linewidth=2.4)
    axes[0].axvline(0, color="#94a3b8", linewidth=1.0, linestyle=(0, (4, 4)))
    axes[0].set_xlabel(xlabel)
    axes[0].set_ylim(0, 10.2)

    title, xlabel = text["problem_panels"][1]
    axes[1].plot(classification_prob, classification_curve, color="#dc2626", linewidth=2.4)
    axes[1].set_xlabel(xlabel)
    axes[1].set_ylim(0, 4.8)

    title, xlabel = text["problem_panels"][2]
    axes[2].bar(token_positions, token_loss, color=["#dc2626", "#f97316", "#dc2626", "#0f766e"], width=0.56)
    axes[2].set_xlabel(xlabel)
    axes[2].set_xticks(token_positions)
    axes[2].set_xticklabels(text["token_labels"])
    axes[2].set_ylim(0, 3.0)
    for idx, value in enumerate(token_loss):
        axes[2].text(
            token_positions[idx],
            value + 0.08,
            f"{value:.2f}",
            ha="center",
            fontsize=8.0,
            color="#334155",
            bbox={"boxstyle": "round,pad=0.16", "fc": "white", "ec": "none", "alpha": 0.92},
        )

    fig.tight_layout(pad=1.0, w_pad=1.2)
    out_path = OUT_DIR / text["problem_axes_out"]
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    inject_accessibility(out_path, text["problem_axes_title"], text["problem_axes_desc"])


def save_regression_loss_axis(text: dict[str, str]) -> None:
    configure_font(text)
    fig, ax = plt.subplots(figsize=(4.4, 4.2), dpi=160)
    fig.patch.set_facecolor("white")

    z = np.linspace(-3.1, 3.1, 500)
    regression_curve = z**2
    title, xlabel = text["problem_panels"][0]
    ax.set_facecolor("#f8fafc")
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.82)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylabel(text["loss_ylabel"])
    ax.plot(z, regression_curve, color="#2563eb", linewidth=2.4)
    ax.axvline(0, color="#94a3b8", linewidth=1.0, linestyle=(0, (4, 4)))
    ax.set_xlabel(xlabel)
    ax.set_ylim(0, 10.2)

    fig.tight_layout(pad=1.0)
    out_path = OUT_DIR / text["regression_axis_out"]
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    inject_accessibility(out_path, text["regression_axis_title"], text["regression_axis_desc"])


def save_classification_loss_axis(text: dict[str, str]) -> None:
    configure_font(text)
    fig, ax = plt.subplots(figsize=(4.4, 4.2), dpi=160)
    fig.patch.set_facecolor("white")

    classification_prob = np.linspace(0.02, 0.99, 500)
    classification_curve = -np.log(classification_prob)
    title, xlabel = text["problem_panels"][1]
    ax.set_facecolor("#f8fafc")
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.82)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylabel(text["loss_ylabel"])
    ax.plot(classification_prob, classification_curve, color="#dc2626", linewidth=2.4)
    ax.set_xlabel(xlabel)
    ax.set_ylim(0, 4.8)

    fig.tight_layout(pad=1.0)
    out_path = OUT_DIR / text["classification_axis_out"]
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    inject_accessibility(out_path, text["classification_axis_title"], text["classification_axis_desc"])


def save_generation_loss_axis(text: dict[str, str]) -> None:
    configure_font(text)
    fig, ax = plt.subplots(figsize=(4.4, 4.2), dpi=160)
    fig.patch.set_facecolor("white")

    token_positions = np.array([1, 2, 3, 4])
    token_confidence = np.array([0.08, 0.22, 0.12, 0.71])
    token_loss = -np.log(token_confidence)
    title, xlabel = text["problem_panels"][2]
    ax.set_facecolor("#f8fafc")
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.82)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylabel(text["loss_ylabel"])
    ax.bar(token_positions, token_loss, color=["#dc2626", "#f97316", "#dc2626", "#0f766e"], width=0.56)
    ax.set_xlabel(xlabel)
    ax.set_xticks(token_positions)
    ax.set_xticklabels(text["token_labels"])
    ax.set_ylim(0, 3.0)
    for idx, value in enumerate(token_loss):
        ax.text(
            token_positions[idx],
            value + 0.08,
            f"{value:.2f}",
            ha="center",
            fontsize=8.0,
            color="#334155",
            bbox={"boxstyle": "round,pad=0.16", "fc": "white", "ec": "none", "alpha": 0.92},
        )

    fig.tight_layout(pad=1.0)
    out_path = OUT_DIR / text["generation_axis_out"]
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    inject_accessibility(out_path, text["generation_axis_title"], text["generation_axis_desc"])


def save_batch_priority_experiment(text: dict[str, str]) -> None:
    configure_font(text)
    fig, ax = plt.subplots(figsize=(5.4, 4.2), dpi=160)
    fig.patch.set_facecolor("white")

    scenarios = np.arange(3)
    mean_loss = np.array([0.350, 0.167, 0.267])
    worst_loss = np.array([0.640, 0.250, 0.640])
    width = 0.34

    ax.set_facecolor("#f8fafc")
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.82)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.bar(scenarios - width / 2, mean_loss, width=width, color="#2563eb", label=text["mean_loss_label"])
    ax.bar(scenarios + width / 2, worst_loss, width=width, color="#dc2626", label=text["worst_loss_label"])
    ax.set_xticks(scenarios)
    ax.set_xticklabels(text["scenario_labels"])
    ax.set_ylabel(text["loss_ylabel"])
    ax.set_ylim(0, 0.78)
    ax.legend(frameon=False, loc="upper right")

    for xpos, value in zip(scenarios - width / 2, mean_loss):
        ax.text(xpos, value + 0.025, f"{value:.3f}", ha="center", fontsize=8.0, color="#334155")
    for xpos, value in zip(scenarios + width / 2, worst_loss):
        ax.text(xpos, value + 0.025, f"{value:.3f}", ha="center", fontsize=8.0, color="#334155")

    fig.tight_layout(pad=1.0)
    out_path = OUT_DIR / text["batch_priority_out"]
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    inject_accessibility(out_path, text["batch_priority_title"], text["batch_priority_desc"])


def save_two_bar_experiment(
    text: dict[str, str],
    out_key: str,
    title_key: str,
    desc_key: str,
    ylabel_key: str,
    values: tuple[float, float],
    color: str,
) -> None:
    configure_font(text)
    fig, ax = plt.subplots(figsize=(4.4, 4.2), dpi=160)
    fig.patch.set_facecolor("white")

    x = np.arange(2)
    ax.set_facecolor("#f8fafc")
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.82)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    bars = ax.bar(x, values, color=["#94a3b8", color], width=0.56)
    ax.set_xticks(x)
    ax.set_xticklabels(text["current_fix_labels"])
    ax.set_ylabel(text[ylabel_key])
    ax.set_ylim(0, max(values) * 1.28)

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + max(values) * 0.035,
            f"{value:.3f}",
            ha="center",
            fontsize=8.5,
            color="#334155",
        )

    fig.tight_layout(pad=1.0)
    out_path = OUT_DIR / text[out_key]
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    inject_accessibility(out_path, text[title_key], text[desc_key])


def main() -> None:
    for text in LANG_TEXT.values():
        save_loss_shapes(text)
        save_squared_error_loss(text)
        save_cross_entropy_loss(text)
        save_problem_axes(text)
        save_regression_loss_axis(text)
        save_classification_loss_axis(text)
        save_generation_loss_axis(text)
        save_batch_priority_experiment(text)
        save_two_bar_experiment(
            text,
            "regression_experiment_out",
            "regression_experiment_title",
            "regression_experiment_desc",
            "regression_loss_label",
            (1.440, 0.090),
            "#2563eb",
        )
        save_two_bar_experiment(
            text,
            "classification_experiment_out",
            "classification_experiment_title",
            "classification_experiment_desc",
            "classification_loss_label",
            (1.050, 0.223),
            "#dc2626",
        )
        save_two_bar_experiment(
            text,
            "generation_experiment_out",
            "generation_experiment_title",
            "generation_experiment_desc",
            "generation_loss_label",
            (1.204, 0.288),
            "#0f766e",
        )


if __name__ == "__main__":
    main()
