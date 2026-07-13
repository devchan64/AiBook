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


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
