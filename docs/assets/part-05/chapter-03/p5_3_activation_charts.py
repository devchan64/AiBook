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
        "compare_out": "activation-function-curves-ko.svg",
        "nonlinear_out": "nonlinear-activation-example-ko.svg",
        "sigmoid_title": "sigmoid 활성화 함수 곡선",
        "sigmoid_desc": "sigmoid 곡선이 큰 음수에서는 0에, z=0에서는 0.5에, 큰 양수에서는 1에 가까워지는 모습을 보여 주는 좌표 그래프.",
        "tanh_title": "tanh 활성화 함수 곡선",
        "tanh_desc": "tanh 곡선이 큰 음수에서는 -1에, z=0에서는 0에, 큰 양수에서는 1에 가까워지는 모습을 보여 주는 좌표 그래프.",
        "relu_title": "ReLU 활성화 함수 곡선",
        "relu_desc": "ReLU 곡선이 음수 구간에서는 0으로 유지되고, z가 0 이상이면 직선으로 증가하는 모습을 보여 주는 좌표 그래프.",
        "compare_title": "sigmoid, tanh, ReLU의 함수 곡선 비교",
        "compare_desc": "sigmoid, tanh, ReLU의 곡선을 세 패널에 나란히 놓아 출력 범위와 음수 처리 방식의 차이를 비교하는 좌표 그래프.",
        "nonlinear_title": "비선형 활성화 변환의 교육용 예시",
        "nonlinear_desc": "입력 점수 z를 그대로 통과시키는 직선과, 구간에 따라 반응이 달라지는 비선형 활성화 예시를 비교하는 좌표 그래프.",
        "sigmoid_panel": "0과 1로 압축",
        "tanh_panel": "-1과 1로 압축",
        "relu_panel": "음수 차단, 양수 통과",
        "linear_pass": "선형 통과 a = z",
        "nonlinear_pass": "비선형 변환 a = f(z)",
        "negative_band": "음수 구간은 더 약해짐",
        "middle_band": "중간 구간은 비교적 직접 전달",
        "high_band": "큰 양수는 증가가 다시 눌림",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "xlabel": "linear score z",
        "ylabel": "activation output a",
        "sigmoid_out": "sigmoid-curve-en.svg",
        "tanh_out": "tanh-curve-en.svg",
        "relu_out": "relu-curve-en.svg",
        "compare_out": "activation-function-curves-en.svg",
        "nonlinear_out": "nonlinear-activation-example-en.svg",
        "sigmoid_title": "Sigmoid activation curve",
        "sigmoid_desc": "A coordinate chart showing the sigmoid curve approaching 0 for large negative inputs, 0.5 at z equals 0, and 1 for large positive inputs.",
        "tanh_title": "Tanh activation curve",
        "tanh_desc": "A coordinate chart showing the tanh curve approaching -1 for large negative inputs, 0 at z equals 0, and 1 for large positive inputs.",
        "relu_title": "ReLU activation curve",
        "relu_desc": "A coordinate chart showing the ReLU curve staying at 0 for negative inputs and increasing linearly once z is 0 or larger.",
        "compare_title": "Sigmoid, tanh, and ReLU curve comparison",
        "compare_desc": "A three-panel coordinate chart comparing sigmoid, tanh, and ReLU so their output ranges and negative-input behavior can be read side by side.",
        "nonlinear_title": "Instructional example of nonlinear activation",
        "nonlinear_desc": "A coordinate chart comparing a straight pass-through line with an instructional nonlinear activation that changes its reaction across different input ranges.",
        "sigmoid_panel": "squash into 0 to 1",
        "tanh_panel": "squash into -1 to 1",
        "relu_panel": "cut negatives, pass positives",
        "linear_pass": "linear pass a = z",
        "nonlinear_pass": "nonlinear transform a = f(z)",
        "negative_band": "negative range is weakened",
        "middle_band": "middle range passes more directly",
        "high_band": "high positives are compressed again",
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


def save_compare_chart(text: dict[str, str]) -> None:
    configure_font(text)
    z = np.linspace(-4.2, 4.2, 500)
    curves = [
        ("Sigmoid", 1 / (1 + np.exp(-z)), "#2563eb", text["sigmoid_panel"], (0, 1), [0, 0.5, 1]),
        ("Tanh", np.tanh(z), "#059669", text["tanh_panel"], (-1, 1), [-1, 0, 1]),
        ("ReLU", np.maximum(0, z), "#dc2626", text["relu_panel"], (-0.2, 4.2), [0, 2, 4]),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(9.3, 3.5), dpi=160)
    fig.patch.set_facecolor("white")
    for ax, (title, values, color, subtitle, ylim, y_ticks) in zip(axes, curves):
        ax.set_facecolor("white")
        ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.8)
        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_xlim(-4.2, 4.2)
        ax.set_ylim(*ylim)
        ax.set_xticks([-4, -2, 0, 2, 4])
        ax.set_yticks(y_ticks)
        ax.plot(z, values, color=color, linewidth=2.2)
        ax.axvline(0, color="#94a3b8", linewidth=1.0, linestyle=(0, (4, 4)))
        if title != "ReLU":
            ax.axhline(0 if title == "Tanh" else 0.5, color="#cbd5e1", linewidth=0.9, linestyle=(0, (4, 4)))
        ax.set_title(title, fontsize=11.5, fontweight="bold", color="#172033", loc="left")
        ax.text(0.03, 0.92, subtitle, transform=ax.transAxes, fontsize=8.8, color="#475569", va="top")
        ax.set_xlabel("z")
        if ax is axes[0]:
            ax.set_ylabel("a")

    out = OUT_DIR / text["compare_out"]
    fig.tight_layout(pad=0.9, w_pad=1.1)
    fig.savefig(out, format="svg")
    plt.close(fig)
    inject_accessibility(out, text["compare_title"], text["compare_desc"])


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


def main() -> None:
    for text in LANG_TEXT.values():
        save_sigmoid_chart(text)
        save_tanh_chart(text)
        save_relu_chart(text)
        save_compare_chart(text)
        save_nonlinear_example_chart(text)


if __name__ == "__main__":
    main()
