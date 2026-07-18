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
        "font_candidates": ["Noto Sans CJK KR", "NanumGothic", "Apple SD Gothic Neo", "AppleGothic", "Arial Unicode MS", "DejaVu Sans"],
        "outfile": "backprop-gradient-direction-ko.svg",
        "direction_outfile": "backprop-gradient-signal-direction-ko.svg",
        "strength_outfile": "backprop-gradient-signal-strength-ko.svg",
        "title": "손실 곡선 위에서 읽는 gradient 방향과 강도",
        "desc": "위험 가중치 축 위의 손실 곡선에서 현재 위치가 목표점 왼쪽이면 가중치를 키우는 방향, 오른쪽이면 줄이는 방향으로 gradient 신호가 생기고, 목표점에서 멀수록 신호가 더 강해진다는 점을 보여 주는 그래프.",
        "direction_title": "손실 곡선 위 gradient 방향",
        "direction_desc": "손실 곡선에서 현재 위치가 목표점 왼쪽이면 가중치를 키우고, 오른쪽이면 줄여야 한다는 방향 신호를 보여 주는 그래프.",
        "strength_title": "손실 곡선 위 gradient 강도",
        "strength_desc": "손실 곡선에서 목표점에 가까운 오차와 먼 오차를 비교해, 더 멀수록 더 강한 gradient 신호가 생긴다는 점을 보여 주는 그래프.",
        "xlabel": "위험 가중치",
        "ylabel": "손실",
        "left": "증가 방향",
        "right": "감소 방향",
        "target": "목표점",
        "near": "가까운 오차",
        "far": "큰 오차",
        "case_labels": ["조금 부족", "많이 부족", "너무 큼"],
        "prediction_ylabel": "예측 차단 점수",
        "loss_ylabel": "손실",
        "gradient_ylabel": "위험 가중치 gradient",
        "case_xlabel": "사례",
        "target_label": "목표",
        "open_label": "문 열림",
        "closed_label": "문 닫힘",
        "forward_node_labels": ["weighted\npressure", "block\nlogit", "block\nactivation", "loss"],
        "backward_node_labels": ["dL/d\nactivation", "dL/d\nlogit", "dL/d\nweighted", "dL/d\nweight", "dL/d\nbias"],
        "forward_ylabel": "forward 값",
        "backward_ylabel": "backward gradient",
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans SC",
            "Microsoft YaHei",
            "PingFang SC",
            "SimHei",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "backprop-gradient-direction-zh.svg",
        "direction_outfile": "backprop-gradient-signal-direction-zh.svg",
        "strength_outfile": "backprop-gradient-signal-strength-zh.svg",
        "title": "在损失曲线上读取梯度方向与强度",
        "desc": "展示在风险权重坐标轴上的损失曲线中，当前位置位于目标点左侧时会出现增大权重的信号，位于右侧时会出现减小权重的信号，而且离目标越远梯度信号越强。",
        "direction_title": "损失曲线上的梯度方向",
        "direction_desc": "展示在损失曲线上，当前位置位于目标点左侧时应增大权重，位于右侧时应减小权重的方向信号。",
        "strength_title": "损失曲线上的梯度强度",
        "strength_desc": "比较靠近目标点与远离目标点的误差，展示越远时会产生更强的梯度信号。",
        "xlabel": "风险权重",
        "ylabel": "损失",
        "left": "增大方向",
        "right": "减小方向",
        "target": "目标点",
        "near": "较近误差",
        "far": "较大误差",
        "case_labels": ["略低", "过低", "过高"],
        "prediction_ylabel": "预测阻断分数",
        "loss_ylabel": "损失",
        "gradient_ylabel": "风险权重梯度",
        "case_xlabel": "案例",
        "target_label": "目标",
        "open_label": "门打开",
        "closed_label": "门关闭",
        "forward_node_labels": ["weighted\npressure", "block\nlogit", "block\nactivation", "loss"],
        "backward_node_labels": ["dL/d\nactivation", "dL/d\nlogit", "dL/d\nweighted", "dL/d\nweight", "dL/d\nbias"],
        "forward_ylabel": "forward 值",
        "backward_ylabel": "backward 梯度",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "backprop-gradient-direction-en.svg",
        "direction_outfile": "backprop-gradient-signal-direction-en.svg",
        "strength_outfile": "backprop-gradient-signal-strength-en.svg",
        "title": "Gradient direction and strength on a loss curve",
        "desc": "A chart showing that on a loss curve over a risk-weight axis, points left of the target produce an increase signal, points right of the target produce a decrease signal, and points farther from the target produce a stronger gradient signal.",
        "direction_title": "Gradient direction on a loss curve",
        "direction_desc": "A chart showing that points left of the target create an increase signal and points right of the target create a decrease signal.",
        "strength_title": "Gradient strength on a loss curve",
        "strength_desc": "A chart showing that points farther from the target create a stronger gradient signal than points closer to the target.",
        "xlabel": "risk weight",
        "ylabel": "loss",
        "left": "increase",
        "right": "decrease",
        "target": "target",
        "near": "small error",
        "far": "large error",
        "case_labels": ["slightly low", "too low", "too high"],
        "prediction_ylabel": "predicted block score",
        "loss_ylabel": "loss",
        "gradient_ylabel": "risk-weight gradient",
        "case_xlabel": "case",
        "target_label": "target",
        "open_label": "gate open",
        "closed_label": "gate closed",
        "forward_node_labels": ["weighted\npressure", "block\nlogit", "block\nactivation", "loss"],
        "backward_node_labels": ["dL/d\nactivation", "dL/d\nlogit", "dL/d\nweighted", "dL/d\nweight", "dL/d\nbias"],
        "forward_ylabel": "forward value",
        "backward_ylabel": "backward gradient",
    },
}

EXERCISE_CASES = [
    ("slightly_under_block_signal", 2.0, 5.0, 2.3),
    ("too_weak_block_signal", 2.0, 5.0, 1.5),
    ("too_strong_block_signal", 2.0, 5.0, 3.2),
]

COMPUTATION_GRAPH_CASES = [
    ("block_gate_open", 2.0, 1.5, -0.5, 4.0),
    ("block_gate_closed", 2.0, 0.1, -0.5, 4.0),
]


def exercise_values() -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    predictions = []
    losses = []
    gradients = []
    target = EXERCISE_CASES[0][2]
    for _name, pressure_unrecovered, target_block_score, risk_weight in EXERCISE_CASES:
        prediction = risk_weight * pressure_unrecovered
        loss = (prediction - target_block_score) ** 2
        gradient = 2 * (prediction - target_block_score) * pressure_unrecovered
        predictions.append(prediction)
        losses.append(loss)
        gradients.append(gradient)
    return np.array(predictions), np.array(losses), np.array(gradients), target


def computation_graph_case_values(
    pressure_signal: float,
    risk_weight: float,
    base_block_bias: float,
    target_block_score: float,
) -> tuple[list[float], list[float]]:
    weighted_pressure = risk_weight * pressure_signal
    block_logit = weighted_pressure + base_block_bias
    block_activation = max(0.0, block_logit)
    loss = (block_activation - target_block_score) ** 2

    d_loss_d_activation = 2 * (block_activation - target_block_score)
    d_activation_d_logit = 1.0 if block_logit > 0 else 0.0
    d_loss_d_logit = d_loss_d_activation * d_activation_d_logit
    d_loss_d_weighted_pressure = d_loss_d_logit
    d_loss_d_weight = d_loss_d_logit * pressure_signal
    d_loss_d_bias = d_loss_d_logit

    return (
        [weighted_pressure, block_logit, block_activation, loss],
        [d_loss_d_activation, d_loss_d_logit, d_loss_d_weighted_pressure, d_loss_d_weight, d_loss_d_bias],
    )


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
    return 0.27 * (x - 2.7) ** 2 + 0.48


def save_chart(text: dict[str, str]) -> None:
    configure_font(text)
    x = np.linspace(0.0, 5.4, 500)
    y = loss_curve(x)
    target_x = 2.7
    left_x = 1.55
    right_x = 4.05

    fig, ax = plt.subplots(figsize=(6.8, 4.2), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.plot(x, y, color="#0f766e", linewidth=2.8)
    ax.set_xlabel(text["xlabel"])
    ax.set_ylabel(text["ylabel"])
    ax.set_xlim(0.0, 5.45)
    ax.set_ylim(0.35, 3.05)

    target_y = loss_curve(np.array([target_x]))[0]
    ax.axvline(target_x, color="#cbd5e1", linewidth=1.0, linestyle=(0, (4, 4)))
    ax.scatter([target_x], [target_y], color="#0f766e", s=30, zorder=4)
    ax.text(
        target_x + 0.08,
        target_y + 0.12,
        text["target"],
        fontsize=8.6,
        color="#475569",
        bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": "none", "alpha": 0.9},
    )

    left_y = loss_curve(np.array([left_x]))[0]
    right_y = loss_curve(np.array([right_x]))[0]
    ax.scatter([left_x, right_x], [left_y, right_y], color=["#2563eb", "#dc2626"], s=30, zorder=4)
    ax.annotate("", xy=(left_x + 0.42, left_y - 0.03), xytext=(left_x, left_y), arrowprops={"arrowstyle": "->", "color": "#2563eb", "lw": 2.0})
    ax.annotate("", xy=(right_x - 0.42, right_y - 0.03), xytext=(right_x, right_y), arrowprops={"arrowstyle": "->", "color": "#dc2626", "lw": 2.0})
    ax.text(
        left_x - 0.72,
        left_y + 0.34,
        text["left"],
        fontsize=8.4,
        color="#1d4ed8",
        bbox={"boxstyle": "round,pad=0.22", "fc": "white", "ec": "#bfdbfe", "alpha": 0.96},
    )
    ax.text(
        right_x - 0.15,
        right_y + 0.34,
        text["right"],
        fontsize=8.4,
        color="#991b1b",
        bbox={"boxstyle": "round,pad=0.22", "fc": "white", "ec": "#fecaca", "alpha": 0.96},
    )

    ax.scatter([2.15, 0.95], loss_curve(np.array([2.15, 0.95])), color=["#38bdf8", "#1d4ed8"], s=22, zorder=4)
    ax.text(
        2.02,
        loss_curve(np.array([2.15]))[0] + 0.22,
        text["near"],
        fontsize=8.2,
        color="#0369a1",
        bbox={"boxstyle": "round,pad=0.18", "fc": "white", "ec": "none", "alpha": 0.9},
    )
    ax.text(
        0.58,
        loss_curve(np.array([0.95]))[0] + 0.24,
        text["far"],
        fontsize=8.2,
        color="#1d4ed8",
        bbox={"boxstyle": "round,pad=0.18", "fc": "white", "ec": "none", "alpha": 0.9},
    )

    fig.tight_layout(pad=1.0)
    out_path = OUT_DIR / text["outfile"]
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    inject_accessibility(out_path, text["title"], text["desc"])


def save_direction_chart(text: dict[str, str]) -> None:
    configure_font(text)
    x = np.linspace(0.0, 5.4, 500)
    y = loss_curve(x)
    target_x = 2.7
    left_x = 1.55
    right_x = 4.05

    fig, ax = plt.subplots(figsize=(6.0, 4.2), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.plot(x, y, color="#0f766e", linewidth=2.8)
    ax.set_xlabel(text["xlabel"])
    ax.set_ylabel(text["ylabel"])
    ax.set_xlim(0.0, 5.45)
    ax.set_ylim(0.35, 3.05)

    target_y = loss_curve(np.array([target_x]))[0]
    left_y = loss_curve(np.array([left_x]))[0]
    right_y = loss_curve(np.array([right_x]))[0]
    ax.axvline(target_x, color="#cbd5e1", linewidth=1.0, linestyle=(0, (4, 4)))
    ax.scatter([target_x], [target_y], color="#0f766e", s=30, zorder=4)
    ax.scatter([left_x, right_x], [left_y, right_y], color=["#2563eb", "#dc2626"], s=30, zorder=4)
    ax.text(
        target_x + 0.08,
        target_y + 0.12,
        text["target"],
        fontsize=8.6,
        color="#475569",
        bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": "none", "alpha": 0.9},
    )
    ax.annotate("", xy=(left_x + 0.42, left_y - 0.03), xytext=(left_x, left_y), arrowprops={"arrowstyle": "->", "color": "#2563eb", "lw": 2.0})
    ax.annotate("", xy=(right_x - 0.42, right_y - 0.03), xytext=(right_x, right_y), arrowprops={"arrowstyle": "->", "color": "#dc2626", "lw": 2.0})
    ax.text(
        left_x - 0.72,
        left_y + 0.34,
        text["left"],
        fontsize=8.4,
        color="#1d4ed8",
        bbox={"boxstyle": "round,pad=0.22", "fc": "white", "ec": "#bfdbfe", "alpha": 0.96},
    )
    ax.text(
        right_x - 0.15,
        right_y + 0.34,
        text["right"],
        fontsize=8.4,
        color="#991b1b",
        bbox={"boxstyle": "round,pad=0.22", "fc": "white", "ec": "#fecaca", "alpha": 0.96},
    )

    fig.tight_layout(pad=1.0)
    out_path = OUT_DIR / text["direction_outfile"]
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    inject_accessibility(out_path, text["direction_title"], text["direction_desc"])


def save_strength_chart(text: dict[str, str]) -> None:
    configure_font(text)
    x = np.linspace(0.0, 5.4, 500)
    y = loss_curve(x)
    target_x = 2.7
    near_x = 2.15
    far_x = 0.95

    fig, ax = plt.subplots(figsize=(6.0, 4.2), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.plot(x, y, color="#0f766e", linewidth=2.8)
    ax.set_xlabel(text["xlabel"])
    ax.set_ylabel(text["ylabel"])
    ax.set_xlim(0.0, 5.45)
    ax.set_ylim(0.35, 3.05)

    target_y = loss_curve(np.array([target_x]))[0]
    near_y = loss_curve(np.array([near_x]))[0]
    far_y = loss_curve(np.array([far_x]))[0]
    ax.axvline(target_x, color="#cbd5e1", linewidth=1.0, linestyle=(0, (4, 4)))
    ax.scatter([target_x], [target_y], color="#0f766e", s=30, zorder=4)
    ax.text(
        target_x + 0.08,
        target_y + 0.12,
        text["target"],
        fontsize=8.6,
        color="#475569",
        bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": "none", "alpha": 0.9},
    )
    ax.scatter([near_x, far_x], [near_y, far_y], color=["#38bdf8", "#1d4ed8"], s=22, zorder=4)
    ax.text(
        near_x - 0.13,
        near_y + 0.22,
        text["near"],
        fontsize=8.2,
        color="#0369a1",
        bbox={"boxstyle": "round,pad=0.18", "fc": "white", "ec": "none", "alpha": 0.9},
    )
    ax.text(
        far_x - 0.37,
        far_y + 0.24,
        text["far"],
        fontsize=8.2,
        color="#1d4ed8",
        bbox={"boxstyle": "round,pad=0.18", "fc": "white", "ec": "none", "alpha": 0.9},
    )

    fig.tight_layout(pad=1.0)
    out_path = OUT_DIR / text["strength_outfile"]
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    inject_accessibility(out_path, text["strength_title"], text["strength_desc"])


def style_case_axis(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, axis="y", linestyle="--", linewidth=0.8, alpha=0.35)
    ax.set_axisbelow(True)


def save_prediction_trace(text: dict[str, str], locale: str) -> None:
    configure_font(text)
    predictions, _losses, _gradients, target = exercise_values()
    x = np.arange(len(predictions))
    colors = ["#f59e0b", "#dc2626", "#2563eb"]

    fig, ax = plt.subplots(figsize=(7.2, 3.8), constrained_layout=True)
    bars = ax.bar(x, predictions, color=colors, width=0.48)
    for bar, value in zip(bars, predictions):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.13, f"{value:.1f}", ha="center", fontsize=10)
    ax.axhline(target, color="#0f766e", linewidth=1.4, linestyle=(0, (5, 4)), label=f"{text['target_label']}={target:.1f}")
    ax.set_xticks(x)
    ax.set_xticklabels(text["case_labels"])
    ax.set_xlabel(text["case_xlabel"])
    ax.set_ylabel(text["prediction_ylabel"])
    ax.set_ylim(0, 7.4)
    ax.legend(loc="upper left", frameon=False)
    style_case_axis(ax)
    fig.savefig(OUT_DIR / f"backprop-example-prediction-{locale}.png", dpi=160)
    plt.close(fig)


def save_loss_trace(text: dict[str, str], locale: str) -> None:
    configure_font(text)
    _predictions, losses, _gradients, _target = exercise_values()
    x = np.arange(len(losses))
    colors = ["#f59e0b", "#dc2626", "#2563eb"]

    fig, ax = plt.subplots(figsize=(7.2, 3.8), constrained_layout=True)
    bars = ax.bar(x, losses, color=colors, width=0.48)
    for bar, value in zip(bars, losses):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.18, f"{value:.2f}", ha="center", fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(text["case_labels"])
    ax.set_xlabel(text["case_xlabel"])
    ax.set_ylabel(text["loss_ylabel"])
    ax.set_ylim(0, 4.8)
    style_case_axis(ax)
    fig.savefig(OUT_DIR / f"backprop-example-loss-{locale}.png", dpi=160)
    plt.close(fig)


def save_gradient_trace(text: dict[str, str], locale: str) -> None:
    configure_font(text)
    _predictions, _losses, gradients, _target = exercise_values()
    x = np.arange(len(gradients))
    colors = ["#f59e0b", "#dc2626", "#2563eb"]

    fig, ax = plt.subplots(figsize=(7.2, 3.8), constrained_layout=True)
    bars = ax.bar(x, gradients, color=colors, width=0.48)
    for bar, value in zip(bars, gradients):
        label_y = value - 0.55 if value < 0 else value + 0.3
        va = "top" if value < 0 else "bottom"
        ax.text(bar.get_x() + bar.get_width() / 2, label_y, f"{value:.1f}", ha="center", va=va, fontsize=10)
    ax.axhline(0, color="#334155", linewidth=1.2)
    ax.set_xticks(x)
    ax.set_xticklabels(text["case_labels"])
    ax.set_xlabel(text["case_xlabel"])
    ax.set_ylabel(text["gradient_ylabel"])
    ax.set_ylim(-9.5, 6.8)
    style_case_axis(ax)
    fig.savefig(OUT_DIR / f"backprop-example-gradient-{locale}.png", dpi=160)
    plt.close(fig)


def computation_graph_example_values() -> tuple[np.ndarray, np.ndarray]:
    traces = [
        computation_graph_case_values(
            pressure_signal,
            risk_weight,
            base_block_bias,
            target_block_score,
        )
        for _name, pressure_signal, risk_weight, base_block_bias, target_block_score in COMPUTATION_GRAPH_CASES
    ]
    forward_values = np.array([forward for forward, _backward in traces])
    backward_values = np.array([backward for _forward, backward in traces])
    return forward_values, backward_values


def save_computation_forward_trace(text: dict[str, str], locale: str) -> None:
    configure_font(text)
    forward_values, _backward_values = computation_graph_example_values()
    x = np.arange(forward_values.shape[1])
    width = 0.34

    fig, ax = plt.subplots(figsize=(7.4, 4.0), constrained_layout=True)
    bars_open = ax.bar(x - width / 2, forward_values[0], width=width, color="#2563eb", label=text["open_label"])
    bars_closed = ax.bar(x + width / 2, forward_values[1], width=width, color="#dc2626", label=text["closed_label"])
    for bars in (bars_open, bars_closed):
        for bar in bars:
            value = bar.get_height()
            label_y = value + 0.35 if value >= 0 else value - 0.55
            va = "bottom" if value >= 0 else "top"
            ax.text(bar.get_x() + bar.get_width() / 2, label_y, f"{value:.3g}", ha="center", va=va, fontsize=9)
    ax.axhline(0, color="#334155", linewidth=1.1)
    ax.set_xticks(x)
    ax.set_xticklabels(text["forward_node_labels"])
    ax.set_ylabel(text["forward_ylabel"])
    ax.set_ylim(-1.4, 18.0)
    ax.legend(frameon=False, loc="upper left")
    style_case_axis(ax)
    fig.savefig(OUT_DIR / f"computation-graph-forward-trace-{locale}.png", dpi=160)
    plt.close(fig)


def save_computation_backward_trace(text: dict[str, str], locale: str) -> None:
    configure_font(text)
    _forward_values, backward_values = computation_graph_example_values()
    x = np.arange(backward_values.shape[1])
    width = 0.34

    fig, ax = plt.subplots(figsize=(7.4, 4.0), constrained_layout=True)
    bars_open = ax.bar(x - width / 2, backward_values[0], width=width, color="#2563eb", label=text["open_label"])
    bars_closed = ax.bar(x + width / 2, backward_values[1], width=width, color="#dc2626", label=text["closed_label"])
    for bars in (bars_open, bars_closed):
        for bar in bars:
            value = bar.get_height()
            label_y = value - 0.35 if value < 0 else value + 0.25
            va = "top" if value < 0 else "bottom"
            ax.text(bar.get_x() + bar.get_width() / 2, label_y, f"{value:.1f}", ha="center", va=va, fontsize=9)
    ax.axhline(0, color="#334155", linewidth=1.1)
    ax.set_xticks(x)
    ax.set_xticklabels(text["backward_node_labels"])
    ax.set_ylabel(text["backward_ylabel"])
    ax.set_ylim(-9.5, 1.3)
    ax.legend(frameon=False, loc="lower left")
    style_case_axis(ax)
    fig.savefig(OUT_DIR / f"computation-graph-backward-trace-{locale}.png", dpi=160)
    plt.close(fig)


def main() -> None:
    for locale, text in LANG_TEXT.items():
        save_chart(text)
        save_direction_chart(text)
        save_strength_chart(text)
        save_prediction_trace(text, locale)
        save_loss_trace(text, locale)
        save_gradient_trace(text, locale)
        save_computation_forward_trace(text, locale)
        save_computation_backward_trace(text, locale)


if __name__ == "__main__":
    main()
