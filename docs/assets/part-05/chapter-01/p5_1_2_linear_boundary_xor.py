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

LINEAR_POINTS = {
    "class_0": np.array([[0.16, 0.22], [0.28, 0.34], [0.38, 0.27], [0.48, 0.41]]),
    "class_1": np.array([[0.62, 0.62], [0.74, 0.78], [0.82, 0.66], [0.88, 0.84]]),
}

XOR_POINTS = {
    "class_0": np.array([[0.0, 0.0], [1.0, 1.0]]),
    "class_1": np.array([[0.0, 1.0], [1.0, 0.0]]),
}

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
        "outfile": "linear-boundary-xor-ko.svg",
        "linear_outfile": "linear-boundary-points-ko.svg",
        "xor_outfile": "xor-pattern-ko.svg",
        "title": "선형 경계와 XOR 한계",
        "desc": "왼쪽 패널은 직선 하나로 나눌 수 있는 점 배치를, 오른쪽 패널은 XOR 점 배치를 보여 준다. 퍼셉트론 하나의 직선 경계는 첫 번째 패턴은 분리할 수 있지만 XOR는 깔끔하게 분리하기 어렵다.",
        "linear_title": "직선 하나로 나눌 수 있는 점 배치",
        "linear_desc": "직선 하나로 두 클래스를 깔끔하게 나눌 수 있는 점 배치를 보여 주는 좌표 그래프.",
        "xor_title": "직선 하나로 나누기 어려운 XOR 점 배치",
        "xor_desc": "같은 출력이 대각선에 놓여 있어 직선 하나로는 깔끔하게 나누기 어려운 XOR 점 배치를 보여 주는 좌표 그래프.",
        "panel_left": "선형 분리 가능",
        "panel_right": "XOR 배치",
        "xlabel": "입력 x1",
        "ylabel": "입력 x2",
        "class_0": "분류 0",
        "class_1": "분류 1",
        "line_ok": "직선 하나로 가능",
        "line_fail": "직선 하나로 실패",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "linear-boundary-xor-en.svg",
        "linear_outfile": "linear-boundary-points-en.svg",
        "xor_outfile": "xor-pattern-en.svg",
        "title": "Linear boundary and XOR limitation",
        "desc": "The left panel shows a linearly separable point pattern and the right panel shows the XOR pattern. A single straight boundary can separate the first, but cannot cleanly separate XOR.",
        "linear_title": "Point pattern that one straight line can separate",
        "linear_desc": "A coordinate chart showing a point pattern that can be cleanly separated into two classes with one straight boundary.",
        "xor_title": "XOR point pattern that one straight line cannot separate cleanly",
        "xor_desc": "A coordinate chart showing the XOR point pattern, where same-label points lie on opposite corners and one straight boundary is not enough.",
        "panel_left": "Linearly separable",
        "panel_right": "XOR pattern",
        "xlabel": "input x1",
        "ylabel": "input x2",
        "class_0": "class 0",
        "class_1": "class 1",
        "line_ok": "one line works",
        "line_fail": "one line fails",
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK JP",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "linear-boundary-xor-zh.svg",
        "linear_outfile": "linear-boundary-points-zh.svg",
        "xor_outfile": "xor-pattern-zh.svg",
        "title": "线性边界与 XOR 局限",
        "desc": "左侧面板显示可被一条直线分开的点分布，右侧面板显示 XOR 点分布。单一线性边界可以分开前者，但无法干净地分开 XOR。",
        "linear_title": "可被一条直线分开的点分布",
        "linear_desc": "展示一条直线可以把两类点干净分开的坐标图。",
        "xor_title": "难以用一条直线分开的 XOR 点分布",
        "xor_desc": "展示同类点位于对角位置、难以用一条直线干净分开的 XOR 坐标图。",
        "panel_left": "线性可分",
        "panel_right": "XOR 分布",
        "xlabel": "输入 x1",
        "ylabel": "输入 x2",
        "class_0": "类别 0",
        "class_1": "类别 1",
        "line_ok": "一条直线可分",
        "line_fail": "一条直线失效",
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


def style_axes(ax, text: dict[str, str]) -> None:
    ax.set_facecolor("#f8fafc")
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xticks([0.0, 0.5, 1.0])
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.grid(True, color="#d0d7de", linewidth=0.8, alpha=0.85)
    ax.set_axisbelow(True)
    ax.set_xlabel(text["xlabel"])
    ax.set_ylabel(text["ylabel"])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def draw_linear_panel(ax, text: dict[str, str]) -> None:
    style_axes(ax, text)

    class_0 = LINEAR_POINTS["class_0"]
    class_1 = LINEAR_POINTS["class_1"]
    ax.scatter(class_0[:, 0], class_0[:, 1], s=74, color="#2563eb", label=text["class_0"], zorder=3)
    ax.scatter(class_1[:, 0], class_1[:, 1], s=74, color="#dc2626", label=text["class_1"], zorder=3)

    x = np.linspace(0.08, 0.95, 300)
    y = 1.08 - 0.82 * x
    ax.plot(x, y, color="#0f766e", linewidth=2.4)
    ax.text(0.54, 0.55, text["line_ok"], color="#0f766e", fontsize=9.5, rotation=-39, ha="center", va="center")

    ax.legend(loc="lower right", frameon=False, fontsize=9)


def draw_xor_panel(ax, text: dict[str, str]) -> None:
    style_axes(ax, text)

    class_0 = XOR_POINTS["class_0"]
    class_1 = XOR_POINTS["class_1"]
    ax.scatter(class_0[:, 0], class_0[:, 1], s=86, color="#2563eb", label=text["class_0"], zorder=3)
    ax.scatter(class_1[:, 0], class_1[:, 1], s=86, color="#dc2626", label=text["class_1"], zorder=3)

    line_x = np.linspace(0.0, 1.0, 300)
    ax.plot(line_x, 0.88 - 0.78 * line_x, color="#64748b", linewidth=2.0, linestyle=(0, (5, 4)))
    ax.plot(line_x, 0.2 + 0.62 * line_x, color="#94a3b8", linewidth=2.0, linestyle=(0, (5, 4)))
    ax.text(0.63, 0.79, text["line_fail"], color="#64748b", fontsize=9.5, ha="center")

    labels = {
        (0.0, 0.0): (0.05, -0.07),
        (0.0, 1.0): (0.05, 0.02),
        (1.0, 0.0): (-0.17, -0.07),
        (1.0, 1.0): (-0.17, 0.02),
    }
    for point in np.vstack([class_0, class_1]):
        dx, dy = labels[(float(point[0]), float(point[1]))]
        ax.text(point[0] + dx, point[1] + dy, f"({int(point[0])}, {int(point[1])})", fontsize=9, color="#334155")

    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.02), ncol=2, frameon=False, fontsize=9)


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


def save_chart(text: dict[str, str]) -> None:
    configure_font(text)
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.85), dpi=160)
    fig.patch.set_facecolor("white")

    draw_linear_panel(axes[0], text)
    draw_xor_panel(axes[1], text)

    fig.tight_layout(pad=0.8, w_pad=1.4)
    out_path = OUT_DIR / text["outfile"]
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    inject_accessibility(out_path, text["title"], text["desc"])


def save_single_panel(text: dict[str, str], mode: str) -> None:
    configure_font(text)
    fig, ax = plt.subplots(figsize=(4.2, 3.85), dpi=160)
    fig.patch.set_facecolor("white")

    if mode == "linear":
        draw_linear_panel(ax, text)
        out_path = OUT_DIR / text["linear_outfile"]
        title = text["linear_title"]
        desc = text["linear_desc"]
    else:
        draw_xor_panel(ax, text)
        out_path = OUT_DIR / text["xor_outfile"]
        title = text["xor_title"]
        desc = text["xor_desc"]

    fig.tight_layout(pad=0.8)
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    inject_accessibility(out_path, title, desc)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)
        save_single_panel(text, "linear")
        save_single_panel(text, "xor")


if __name__ == "__main__":
    main()
