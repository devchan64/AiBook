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
        "outfile": "train-validation-overfit-ko.svg",
        "title": "훈련 손실과 검증 손실이 갈라지는 과적합 장면",
        "desc": "훈련 손실은 계속 내려가지만 검증 손실은 어느 지점 이후 다시 올라가며, 정규화가 훈련 손실 하나가 아니라 검증 곡선과 간극을 함께 보게 만든다는 점을 보여 주는 좌표 그래프.",
        "xlabel": "학습 step",
        "ylabel": "손실",
        "train": "훈련 손실",
        "validation": "검증 손실",
        "turn": "검증 손실 전환",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "train-validation-overfit-en.svg",
        "title": "Overfitting scene where training and validation loss diverge",
        "desc": "A coordinate chart showing training loss continuing downward while validation loss turns upward after a point, reinforcing that regularization watches the validation gap instead of the training minimum alone.",
        "xlabel": "training step",
        "ylabel": "loss",
        "train": "training loss",
        "validation": "validation loss",
        "turn": "validation turn",
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
        "outfile": "train-validation-overfit-zh.svg",
        "title": "训练损失与验证损失分叉的过拟合场景",
        "desc": "一张坐标图，显示训练损失持续下降，而验证损失在某个时点之后重新上升，用来强调正则化关注的不只是训练最小值，还包括验证间隙。",
        "xlabel": "训练 step",
        "ylabel": "损失",
        "train": "训练损失",
        "validation": "验证损失",
        "turn": "验证损失转折点",
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


def save_chart(text: dict[str, str]) -> None:
    configure_font(text)
    x = np.linspace(1, 18, 250)
    train = 1.25 * np.exp(-0.15 * x) + 0.15
    validation = 1.05 * np.exp(-0.11 * x) + 0.22 + 0.015 * np.maximum(x - 8, 0) ** 1.55
    turn_x = 8.0
    turn_y = np.interp(turn_x, x, validation)

    fig, ax = plt.subplots(figsize=(6.2, 3.9), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.plot(x, train, color="#2563eb", linewidth=2.6, label=text["train"])
    ax.plot(x, validation, color="#dc2626", linewidth=2.6, label=text["validation"])
    ax.axvline(turn_x, color="#64748b", linewidth=1.0, linestyle=(0, (4, 4)))
    ax.scatter([turn_x], [turn_y], color="#dc2626", s=30, zorder=4)
    ax.annotate(text["turn"], xy=(turn_x, turn_y), xytext=(8.7, turn_y + 0.18), fontsize=8.7, color="#991b1b")
    ax.set_xlabel(text["xlabel"])
    ax.set_ylabel(text["ylabel"])
    ax.legend(frameon=False, loc="upper right", fontsize=8.4)

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
