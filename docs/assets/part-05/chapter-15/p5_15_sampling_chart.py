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
        "outfile": "sampling-distribution-choice-ko.svg",
        "title": "후보 분포와 샘플링 선택 결과",
        "desc": "왼쪽에는 후보 문구별 상대 비중을, 오른쪽에는 20번 샘플링했을 때 실제 선택 빈도를 막대로 보여 주며, 샘플링이 높은 후보를 더 자주 고르되 낮은 후보도 일부 남길 수 있음을 설명하는 그래프.",
        "weight_outfile": "sampling-candidate-weights-ko.svg",
        "weight_title": "후보 문구별 상대 비중",
        "weight_desc": "샘플링 전 후보 문구별 상대 비중을 막대로 보여 주는 그래프.",
        "count_outfile": "sampling-choice-counts-ko.svg",
        "count_title": "20회 샘플링 선택 빈도",
        "count_desc": "20회 샘플링했을 때 각 후보 문구가 실제로 몇 번 선택됐는지 보여 주는 그래프.",
        "panel_left": "후보 비중",
        "panel_right": "20회 샘플링 빈도",
        "xlabel": "후보 문구",
        "ylabel_left": "상대 비중",
        "ylabel_right": "선택 횟수",
        "labels": ["후보 A", "후보 B", "후보 C", "후보 D"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "sampling-distribution-choice-en.svg",
        "title": "Candidate distribution and sampled choice results",
        "desc": "A two-panel bar chart showing candidate weights on the left and the observed choice counts after twenty sampling draws on the right, emphasizing that sampling favors stronger candidates without removing weaker ones completely.",
        "weight_outfile": "sampling-candidate-weights-en.svg",
        "weight_title": "Candidate weights",
        "weight_desc": "A bar chart showing the relative weight assigned to each candidate before sampling.",
        "count_outfile": "sampling-choice-counts-en.svg",
        "count_title": "Choice counts over 20 samples",
        "count_desc": "A bar chart showing how many times each candidate was selected across twenty sampling draws.",
        "panel_left": "candidate weights",
        "panel_right": "choice counts over 20 samples",
        "xlabel": "candidate output",
        "ylabel_left": "relative weight",
        "ylabel_right": "number of choices",
        "labels": ["cand A", "cand B", "cand C", "cand D"],
    },
}

WEIGHTS = np.array([0.46, 0.24, 0.18, 0.12])
COUNTS = np.array([9, 5, 4, 2])


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
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 4.0), dpi=160)
    fig.patch.set_facecolor("white")
    colors = ["#2563eb", "#38bdf8", "#38bdf8", "#38bdf8"]
    positions = np.arange(len(text["labels"]))

    axes[0].set_facecolor("#f8fafc")
    axes[0].grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    axes[0].set_axisbelow(True)
    axes[0].spines["top"].set_visible(False)
    axes[0].spines["right"].set_visible(False)
    axes[0].bar(positions, WEIGHTS, color=colors, width=0.62)
    axes[0].set_xticks(positions)
    axes[0].set_xticklabels(text["labels"], fontsize=8.0)
    axes[0].set_ylim(0, 0.56)
    axes[0].set_title(text["panel_left"], loc="left", fontsize=11.4, fontweight="bold", color="#172033")
    axes[0].set_xlabel(text["xlabel"])
    axes[0].set_ylabel(text["ylabel_left"])
    for idx, value in enumerate(WEIGHTS):
        axes[0].text(idx, value + 0.015, f"{value:.2f}", ha="center", fontsize=7.8, color="#334155")

    axes[1].set_facecolor("#f8fafc")
    axes[1].grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    axes[1].set_axisbelow(True)
    axes[1].spines["top"].set_visible(False)
    axes[1].spines["right"].set_visible(False)
    axes[1].bar(positions, COUNTS, color=colors, width=0.62)
    axes[1].set_xticks(positions)
    axes[1].set_xticklabels(text["labels"], fontsize=8.0)
    axes[1].set_ylim(0, 11)
    axes[1].set_title(text["panel_right"], loc="left", fontsize=11.4, fontweight="bold", color="#172033")
    axes[1].set_xlabel(text["xlabel"])
    axes[1].set_ylabel(text["ylabel_right"])
    for idx, value in enumerate(COUNTS):
        axes[1].text(idx, value + 0.2, str(value), ha="center", fontsize=7.8, color="#334155")

    fig.tight_layout(pad=0.9, w_pad=1.2)
    out_path = OUT_DIR / text["outfile"]
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    inject_accessibility(out_path, text["title"], text["desc"])


def style_axis(axis) -> None:
    axis.set_facecolor("#f8fafc")
    axis.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    axis.set_axisbelow(True)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)


def save_single_chart(text: dict[str, str], *, kind: str) -> None:
    configure_font(text)
    fig, axis = plt.subplots(figsize=(4.3, 4.0), dpi=160)
    fig.patch.set_facecolor("white")
    positions = np.arange(len(text["labels"]))
    colors = ["#2563eb", "#38bdf8", "#38bdf8", "#38bdf8"]
    style_axis(axis)

    if kind == "weights":
        values = WEIGHTS
        outfile = text["weight_outfile"]
        title = text["weight_title"]
        desc = text["weight_desc"]
        ylabel = text["ylabel_left"]
        ylim = (0, 0.56)
        value_offset = 0.015
        formatter = lambda value: f"{value:.2f}"
    else:
        values = COUNTS
        outfile = text["count_outfile"]
        title = text["count_title"]
        desc = text["count_desc"]
        ylabel = text["ylabel_right"]
        ylim = (0, 11)
        value_offset = 0.2
        formatter = lambda value: str(int(value))

    axis.bar(positions, values, color=colors, width=0.62)
    axis.set_xticks(positions)
    axis.set_xticklabels(text["labels"], fontsize=8.0)
    axis.set_ylim(*ylim)
    axis.set_xlabel(text["xlabel"])
    axis.set_ylabel(ylabel)

    for idx, value in enumerate(values):
        axis.text(idx, value + value_offset, formatter(value), ha="center", fontsize=7.8, color="#334155")

    fig.tight_layout(pad=0.9)
    out_path = OUT_DIR / outfile
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    inject_accessibility(out_path, title, desc)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)
        save_single_chart(text, kind="weights")
        save_single_chart(text, kind="counts")


if __name__ == "__main__":
    main()
