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
        "outfile": "batch-normalization-scale-ko.svg",
        "title": "batch normalization 전후 출력 스케일",
        "desc": "작은 초기화 출력, 큰 초기화 출력, batch normalization 뒤 출력 위치를 한 축 위에서 비교해, batch normalization이 퍼진 활성값 분포를 다시 중심 근처의 다루기 쉬운 범위로 옮긴다는 점을 보여 주는 좌표 그래프.",
        "xlabel": "활성값",
        "small": "작은 초기화",
        "large": "큰 초기화",
        "bn": "batch normalization 뒤",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "batch-normalization-scale-en.svg",
        "title": "Output scale before and after batch normalization",
        "desc": "A coordinate chart comparing small-initialization outputs, large-initialization outputs, and outputs after batch normalization on one axis to show how batch normalization moves a spread-out activation distribution back toward a manageable central range.",
        "xlabel": "activation value",
        "small": "small init",
        "large": "large init",
        "bn": "after batch norm",
    },
}

SMALL = np.array([-0.22, -0.1, 0.04, 0.18, 0.31])
LARGE = np.array([-2.7, -1.5, 0.4, 1.8, 3.1])
BN = np.array([-1.1, -0.42, 0.05, 0.58, 1.06])


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


def save_chart(text: dict[str, str]) -> None:
    configure_font(text)
    fig, ax = plt.subplots(figsize=(6.2, 3.9), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(True, axis="x", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.axvline(0, color="#cbd5e1", linewidth=1.0, linestyle=(0, (4, 4)))
    rows = [3, 2, 1]
    labels = [text["small"], text["large"], text["bn"]]
    values = [SMALL, LARGE, BN]
    colors = ["#2563eb", "#dc2626", "#059669"]
    for row, label, data, color in zip(rows, labels, values, colors):
        ax.scatter(data, np.full_like(data, row, dtype=float), color=color, s=34)
        ax.hlines(row, data.min(), data.max(), color=color, linewidth=2.0, alpha=0.35)
        ax.text(-3.55, row + 0.14, label, fontsize=9.0, color="#172033", fontweight="bold")
    ax.set_xlim(-3.8, 3.8)
    ax.set_ylim(0.45, 3.55)
    ax.set_yticks([])
    ax.set_xlabel(text["xlabel"])
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
