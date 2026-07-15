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
        "xlabel": "선형 점수 z",
        "ylabel": "활성화 출력 a",
        "sigmoid_out": "sigmoid-curve-ko.svg",
        "tanh_out": "tanh-curve-ko.svg",
        "relu_out": "relu-curve-ko.svg",
        "nonlinear_out": "nonlinear-activation-example-ko.svg",
        "case_before_after_out": "activation-case-before-after-ko.svg",
        "experiment_shift_out": "activation-experiment-shift-ko.svg",
        "sigmoid_title": "sigmoid 활성화 함수 곡선",
        "sigmoid_desc": "sigmoid 곡선이 큰 음수에서는 0에, z=0에서는 0.5에, 큰 양수에서는 1에 가까워지는 모습을 보여 주는 좌표 그래프.",
        "tanh_title": "tanh 활성화 함수 곡선",
        "tanh_desc": "tanh 곡선이 큰 음수에서는 -1에, z=0에서는 0에, 큰 양수에서는 1에 가까워지는 모습을 보여 주는 좌표 그래프.",
        "relu_title": "ReLU 활성화 함수 곡선",
        "relu_desc": "ReLU 곡선이 음수 구간에서는 0으로 유지되고, z가 0 이상이면 직선으로 증가하는 모습을 보여 주는 좌표 그래프.",
        "nonlinear_title": "비선형 활성화 변환의 교육용 예시",
        "nonlinear_desc": "입력 점수 z를 그대로 통과시키는 직선과, 구간에 따라 반응이 달라지는 비선형 활성화 예시를 비교하는 좌표 그래프.",
        "case_before_after_title": "활성화 전후 운영 신호 비교",
        "case_before_after_desc": "네 운영 상태에서 활성화 전 선형 점수 z와 활성화 뒤 값 a가 어떻게 달라지는지 비교하는 좌표 그래프.",
        "experiment_shift_title": "입력 조정에 따른 활성화 전후 변화",
        "experiment_shift_desc": "편향, 실패 가중치, 복귀 지연 점수 조정이 활성화 뒤 값 a를 어떻게 바꾸는지 비교하는 좌표 그래프.",
        "linear_pass": "선형 통과 a = z",
        "nonlinear_pass": "비선형 변환 a = f(z)",
        "negative_band": "음수 구간은 더 약해짐",
        "middle_band": "중간 구간은 비교적 직접 전달",
        "high_band": "큰 양수는 증가가 다시 눌림",
        "z_label": "활성화 전 z",
        "a_label": "활성화 뒤 a",
        "before_label": "변경 전 a",
        "after_label": "변경 후 a",
        "threshold_label": "문턱 0",
        "case_labels": ["짧은 경보", "복귀 우세", "경계 신호", "강한 경고"],
        "experiment_labels": ["편향 낮춤", "실패 가중치 증가", "복귀 지연 감소"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "xlabel": "linear score z",
        "ylabel": "activation output a",
        "sigmoid_out": "sigmoid-curve-en.svg",
        "tanh_out": "tanh-curve-en.svg",
        "relu_out": "relu-curve-en.svg",
        "nonlinear_out": "nonlinear-activation-example-en.svg",
        "case_before_after_out": "activation-case-before-after-en.svg",
        "experiment_shift_out": "activation-experiment-shift-en.svg",
        "sigmoid_title": "Sigmoid activation curve",
        "sigmoid_desc": "A coordinate chart showing the sigmoid curve approaching 0 for large negative inputs, 0.5 at z equals 0, and 1 for large positive inputs.",
        "tanh_title": "Tanh activation curve",
        "tanh_desc": "A coordinate chart showing the tanh curve approaching -1 for large negative inputs, 0 at z equals 0, and 1 for large positive inputs.",
        "relu_title": "ReLU activation curve",
        "relu_desc": "A coordinate chart showing the ReLU curve staying at 0 for negative inputs and increasing linearly once z is 0 or larger.",
        "nonlinear_title": "Instructional example of nonlinear activation",
        "nonlinear_desc": "A coordinate chart comparing a straight pass-through line with an instructional nonlinear activation that changes its reaction across different input ranges.",
        "case_before_after_title": "Operational signals before and after activation",
        "case_before_after_desc": "A coordinate chart comparing the pre-activation linear score z and the post-activation value a across four operational states.",
        "experiment_shift_title": "Activation changes after input adjustments",
        "experiment_shift_desc": "A coordinate chart comparing how changes to bias, failure weight, and recovery delay score alter the post-activation value a.",
        "linear_pass": "linear pass a = z",
        "nonlinear_pass": "nonlinear transform a = f(z)",
        "negative_band": "negative range is weakened",
        "middle_band": "middle range passes more directly",
        "high_band": "high positives are compressed again",
        "z_label": "before activation z",
        "a_label": "after activation a",
        "before_label": "before change a",
        "after_label": "after change a",
        "threshold_label": "threshold 0",
        "case_labels": ["brief alarm", "recovery wins", "borderline", "strong warning"],
        "experiment_labels": ["lower bias", "raise failure weight", "lower recovery delay"],
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


def style_single_axes(ax, text: dict[str, str], y_ticks: list[float], xlim=(-4.2, 4.2), ylim=(-1.2, 4.2)) -> None:
    ax.set_facecolor("white")
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.8)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks([-4, -2, 0, 2, 4])
    ax.set_yticks(y_ticks)
    ax.set_xlabel(text["xlabel"])
    ax.set_ylabel(text["ylabel"])


def save_sigmoid_chart(text: dict[str, str]) -> None:
    configure_font(text)
    z = np.linspace(-4.2, 4.2, 500)
    y = 1 / (1 + np.exp(-z))

    fig, ax = plt.subplots(figsize=(5.4, 3.5), dpi=160)
    fig.patch.set_facecolor("white")
    style_single_axes(ax, text, [0, 0.25, 0.5, 0.75, 1], ylim=(-0.05, 1.05))
    ax.plot(z, y, color="#2563eb", linewidth=2.4)
    ax.axvline(0, color="#94a3b8", linewidth=1.0, linestyle=(0, (4, 4)))
    ax.axhline(0.5, color="#94a3b8", linewidth=1.0, linestyle=(0, (4, 4)))
    ax.scatter([0], [0.5], color="#dc2626", s=28, zorder=4)
    out = OUT_DIR / text["sigmoid_out"]
    fig.tight_layout(pad=0.8)
    fig.savefig(out, format="svg")
    plt.close(fig)
    inject_accessibility(out, text["sigmoid_title"], text["sigmoid_desc"])


def save_tanh_chart(text: dict[str, str]) -> None:
    configure_font(text)
    z = np.linspace(-4.2, 4.2, 500)
    y = np.tanh(z)

    fig, ax = plt.subplots(figsize=(5.4, 3.5), dpi=160)
    fig.patch.set_facecolor("white")
    style_single_axes(ax, text, [-1, -0.5, 0, 0.5, 1], ylim=(-1.05, 1.05))
    ax.plot(z, y, color="#059669", linewidth=2.4)
    ax.axvline(0, color="#94a3b8", linewidth=1.0, linestyle=(0, (4, 4)))
    ax.axhline(0, color="#94a3b8", linewidth=1.0, linestyle=(0, (4, 4)))
    out = OUT_DIR / text["tanh_out"]
    fig.tight_layout(pad=0.8)
    fig.savefig(out, format="svg")
    plt.close(fig)
    inject_accessibility(out, text["tanh_title"], text["tanh_desc"])


def save_relu_chart(text: dict[str, str]) -> None:
    configure_font(text)
    z = np.linspace(-4.2, 4.2, 500)
    y = np.maximum(0, z)

    fig, ax = plt.subplots(figsize=(5.4, 3.5), dpi=160)
    fig.patch.set_facecolor("white")
    style_single_axes(ax, text, [0, 1, 2, 3, 4], ylim=(-0.2, 4.2))
    ax.plot(z, y, color="#dc2626", linewidth=2.4)
    ax.axvline(0, color="#94a3b8", linewidth=1.0, linestyle=(0, (4, 4)))
    ax.axhline(0, color="#94a3b8", linewidth=1.0, linestyle=(0, (4, 4)))
    out = OUT_DIR / text["relu_out"]
    fig.tight_layout(pad=0.8)
    fig.savefig(out, format="svg")
    plt.close(fig)
    inject_accessibility(out, text["relu_title"], text["relu_desc"])


def save_nonlinear_example_chart(text: dict[str, str]) -> None:
    configure_font(text)
    z = np.linspace(-3.5, 4.0, 500)
    linear = z
    nonlinear = np.piecewise(
        z,
        [z < 0, (z >= 0) & (z <= 1.5), z > 1.5],
        [lambda x: 0.2 * x, lambda x: x, lambda x: 1.5 + 0.25 * (x - 1.5)],
    )

    fig, ax = plt.subplots(figsize=(6.1, 3.9), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.8)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlim(-3.5, 4.0)
    ax.set_ylim(-1.2, 2.4)
    ax.set_xticks([-3, -1.5, 0, 1.5, 3])
    ax.set_yticks([-1, 0, 1, 2])
    ax.set_xlabel(text["xlabel"])
    ax.set_ylabel(text["ylabel"])
    ax.plot(z, linear, color="#94a3b8", linewidth=2.0, linestyle=(0, (5, 4)), label=text["linear_pass"])
    ax.plot(z, nonlinear, color="#2563eb", linewidth=2.5, label=text["nonlinear_pass"])
    ax.axvline(0, color="#cbd5e1", linewidth=0.9)
    ax.axvline(1.5, color="#cbd5e1", linewidth=0.9)
    ax.text(-2.8, -0.92, text["negative_band"], fontsize=8.8, color="#334155")
    ax.text(0.08, 1.18, text["middle_band"], fontsize=8.8, color="#334155")
    ax.text(1.95, 1.92, text["high_band"], fontsize=8.8, color="#334155")
    ax.legend(frameon=False, loc="upper left", fontsize=8.8)

    out = OUT_DIR / text["nonlinear_out"]
    fig.tight_layout(pad=0.8)
    fig.savefig(out, format="svg")
    plt.close(fig)
    inject_accessibility(out, text["nonlinear_title"], text["nonlinear_desc"])


def style_comparison_axes(ax, text: dict[str, str], ylim=(-1.6, 5.2)) -> None:
    ax.set_facecolor("white")
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.8)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(*ylim)
    ax.set_ylabel(text["ylabel"])
    ax.axhline(0, color="#64748b", linewidth=1.0, linestyle=(0, (4, 4)))
    ax.text(-0.45, 0.12, text["threshold_label"], fontsize=8.5, color="#475569")


def save_case_before_after_chart(text: dict[str, str]) -> None:
    configure_font(text)
    z_values = np.array([-0.8, -1.3, 0.42, 4.1])
    a_values = np.maximum(0, z_values)
    x = np.arange(len(z_values))
    width = 0.34

    fig, ax = plt.subplots(figsize=(6.8, 3.9), dpi=160)
    fig.patch.set_facecolor("white")
    style_comparison_axes(ax, text)
    ax.bar(x - width / 2, z_values, width=width, color="#94a3b8", label=text["z_label"])
    ax.bar(x + width / 2, a_values, width=width, color="#2563eb", label=text["a_label"])
    for i, (z, a) in enumerate(zip(z_values, a_values)):
        ax.plot([i - width / 2, i + width / 2], [z, a], color="#334155", linewidth=1.2, alpha=0.75)
        ax.text(i - width / 2, z + (0.16 if z >= 0 else -0.28), f"{z:g}", ha="center", fontsize=8.2, color="#334155")
        ax.text(i + width / 2, a + 0.16, f"{a:g}", ha="center", fontsize=8.2, color="#1d4ed8")
    ax.set_xticks(x)
    ax.set_xticklabels(text["case_labels"], fontsize=8.6)
    ax.legend(frameon=False, loc="upper left", fontsize=8.8)

    out = OUT_DIR / text["case_before_after_out"]
    fig.tight_layout(pad=0.8)
    fig.savefig(out, format="svg")
    plt.close(fig)
    inject_accessibility(out, text["case_before_after_title"], text["case_before_after_desc"])


def save_experiment_shift_chart(text: dict[str, str]) -> None:
    configure_font(text)
    before = np.array([0.42, 4.1, 0.42])
    after = np.array([0.0, 4.9, 0.0])
    x = np.arange(len(before))
    width = 0.34

    fig, ax = plt.subplots(figsize=(6.4, 3.7), dpi=160)
    fig.patch.set_facecolor("white")
    style_comparison_axes(ax, text, ylim=(-0.35, 5.3))
    ax.bar(x - width / 2, before, width=width, color="#94a3b8", label=text["before_label"])
    ax.bar(x + width / 2, after, width=width, color="#f97316", label=text["after_label"])
    for i, (old, new) in enumerate(zip(before, after)):
        ax.annotate(
            "",
            xy=(i + width / 2, new),
            xytext=(i - width / 2, old),
            arrowprops={"arrowstyle": "->", "color": "#334155", "lw": 1.2},
        )
        ax.text(i - width / 2, old + 0.14, f"{old:g}", ha="center", fontsize=8.2, color="#334155")
        ax.text(i + width / 2, new + 0.14, f"{new:g}", ha="center", fontsize=8.2, color="#c2410c")
    ax.set_xticks(x)
    ax.set_xticklabels(text["experiment_labels"], fontsize=8.6)
    ax.legend(frameon=False, loc="upper left", fontsize=8.8)

    out = OUT_DIR / text["experiment_shift_out"]
    fig.tight_layout(pad=0.8)
    fig.savefig(out, format="svg")
    plt.close(fig)
    inject_accessibility(out, text["experiment_shift_title"], text["experiment_shift_desc"])


def main() -> None:
    for text in LANG_TEXT.values():
        save_sigmoid_chart(text)
        save_tanh_chart(text)
        save_relu_chart(text)
        save_nonlinear_example_chart(text)
        save_case_before_after_chart(text)
        save_experiment_shift_chart(text)


if __name__ == "__main__":
    main()
