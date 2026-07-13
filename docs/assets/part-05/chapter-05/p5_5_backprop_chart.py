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
        "left": "increase",
        "right": "decrease",
        "target": "목표점",
        "near": "가까운 오차",
        "far": "큰 오차",
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


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)
        save_direction_chart(text)
        save_strength_chart(text)


if __name__ == "__main__":
    main()
