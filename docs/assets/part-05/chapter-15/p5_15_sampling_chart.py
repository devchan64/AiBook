from pathlib import Path
import os
import random
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
        "weight_outfile": "sampling-candidate-weights-ko.svg",
        "weight_title": "후보 문구별 상대 비중",
        "weight_desc": "샘플링 전 후보 문구별 상대 비중을 막대로 보여 주는 그래프.",
        "count_outfile": "sampling-choice-counts-ko.svg",
        "count_title": "20회 샘플링 선택 빈도",
        "count_desc": "20회 샘플링했을 때 각 후보 문구가 실제로 몇 번 선택됐는지 보여 주는 그래프.",
        "xlabel": "후보 문구",
        "ylabel_left": "상대 비중",
        "ylabel_right": "선택 횟수",
        "labels": ["재확인", "담당자 확인", "10분 뒤 재측정", "정상 유지"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "weight_outfile": "sampling-candidate-weights-en.svg",
        "weight_title": "Candidate weights",
        "weight_desc": "A bar chart showing the relative weight assigned to each candidate before sampling.",
        "count_outfile": "sampling-choice-counts-en.svg",
        "count_title": "Choice counts over 20 samples",
        "count_desc": "A bar chart showing how many times each candidate was selected across twenty sampling draws.",
        "xlabel": "candidate output",
        "ylabel_left": "relative weight",
        "ylabel_right": "number of choices",
        "labels": ["recheck", "operator confirm", "remeasure", "keep normal"],
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK JP",
            "Microsoft YaHei",
            "PingFang SC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "weight_outfile": "sampling-candidate-weights-zh.svg",
        "weight_title": "候选短语相对权重",
        "weight_desc": "展示 sampling 前每个候选短语相对权重的柱状图。",
        "count_outfile": "sampling-choice-counts-zh.svg",
        "count_title": "20 次 sampling 的选择频率",
        "count_desc": "展示进行二十次 sampling 时，各候选短语实际被选中了多少次的柱状图。",
        "xlabel": "候选输出",
        "ylabel_left": "相对权重",
        "ylabel_right": "选择次数",
        "labels": ["重新确认", "主管确认", "重新测量", "保持正常"],
    },
}

RESPONSE_CANDIDATES = [
    "재확인이 필요합니다.",
    "담당자 확인 후 재개합니다.",
    "10분 뒤 재측정합니다.",
    "현재 기준에서는 정상으로 유지합니다.",
]
RESPONSE_WEIGHTS = [0.46, 0.24, 0.18, 0.12]


def sampling_counts() -> np.ndarray:
    random.seed(7)
    sampled_choices = [random.choices(RESPONSE_CANDIDATES, weights=RESPONSE_WEIGHTS, k=1)[0] for _ in range(20)]
    return np.array([sampled_choices.count(candidate) for candidate in RESPONSE_CANDIDATES])


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
        values = np.array(RESPONSE_WEIGHTS)
        outfile = text["weight_outfile"]
        title = text["weight_title"]
        desc = text["weight_desc"]
        ylabel = text["ylabel_left"]
        ylim = (0, 0.56)
        value_offset = 0.015
        formatter = lambda value: f"{value:.2f}"
    else:
        values = sampling_counts()
        outfile = text["count_outfile"]
        title = text["count_title"]
        desc = text["count_desc"]
        ylabel = text["ylabel_right"]
        ylim = (0, max(values) + 2)
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
        save_single_chart(text, kind="weights")
        save_single_chart(text, kind="counts")


if __name__ == "__main__":
    main()
