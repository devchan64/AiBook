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

TOKENS = ["배터리팩", "분리", "절연캡", "씌우지", "그것"]
RAW_SCORES_BY_TARGET = {
    "그것": {
        "배터리팩": 0.2,
        "분리": 0.6,
        "절연캡": 2.1,
        "씌우지": 1.2,
        "그것": 0.7,
    },
    "씌우지": {
        "배터리팩": 0.1,
        "분리": 1.4,
        "절연캡": 1.8,
        "씌우지": 0.9,
        "그것": 0.2,
    },
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
        "outfile": "self-attention-weights-ko.svg",
        "it_outfile": "self-attention-weight-it-ko.svg",
        "cover_outfile": "self-attention-weight-cover-ko.svg",
        "title": "현재 토큰별 self-attention 비중",
        "desc": "현재 토큰이 '그것'일 때와 '씌우지'일 때 문장 안 토큰별 attention 비중이 어떻게 달라지는지 두 막대 그래프로 비교해, 같은 문장이라도 현재 토큰마다 다시 참고하는 분포가 달라진다는 점을 보여 준다.",
        "it_title": "현재 토큰 '그것'의 self-attention 비중",
        "it_desc": "현재 토큰이 '그것'일 때 문장 안 어떤 토큰을 더 크게 다시 참고하는지 보여 주는 막대 그래프.",
        "cover_title": "현재 토큰 '씌우지'의 self-attention 비중",
        "cover_desc": "현재 토큰이 '씌우지'일 때 문장 안 어떤 토큰을 더 크게 다시 참고하는지 보여 주는 막대 그래프.",
        "panel_left": "현재 토큰: 그것",
        "panel_right": "현재 토큰: 씌우지",
        "xlabel": "다시 참고하는 토큰",
        "ylabel": "attention 비중",
        "tokens": ["배터리팩", "분리", "절연캡", "씌우지", "그것"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "self-attention-weights-en.svg",
        "it_outfile": "self-attention-weight-it-en.svg",
        "cover_outfile": "self-attention-weight-cover-en.svg",
        "title": "Self-attention weights by current token",
        "desc": "A two-panel bar chart comparing how the token-level attention distribution changes when the current token is 'it' versus 'cover', showing that the same sentence can be reread differently for each current token.",
        "it_title": "Self-attention weights for current token 'it'",
        "it_desc": "A bar chart showing which tokens are revisited more strongly when the current token is 'it'.",
        "cover_title": "Self-attention weights for current token 'cover'",
        "cover_desc": "A bar chart showing which tokens are revisited more strongly when the current token is 'cover'.",
        "panel_left": "current token: it",
        "panel_right": "current token: cover",
        "xlabel": "revisited token",
        "ylabel": "attention weight",
        "tokens": ["battery", "remove", "cap", "cover", "it"],
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK JP",
            "Source Han Sans SC",
            "Microsoft YaHei",
            "PingFang SC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "self-attention-weights-zh.svg",
        "it_outfile": "self-attention-weight-it-zh.svg",
        "cover_outfile": "self-attention-weight-cover-zh.svg",
        "title": "按当前 token 区分的 self-attention 权重",
        "desc": "两栏柱状图比较当前 token 为“它”和“套上”时，token 级 attention 分布会怎样变化，用来展示同一句子也会因为当前 token 不同而被重新阅读。",
        "it_title": "当前 token“它”的 self-attention 权重",
        "it_desc": "展示当前 token 为“它”时，句子里哪些 token 会被更强地重新参考的柱状图。",
        "cover_title": "当前 token“套上”的 self-attention 权重",
        "cover_desc": "展示当前 token 为“套上”时，句子里哪些 token 会被更强地重新参考的柱状图。",
        "panel_left": "当前 token：它",
        "panel_right": "当前 token：套上",
        "xlabel": "重新参考的 token",
        "ylabel": "attention 权重",
        "tokens": ["电池包", "拆下", "绝缘帽", "套上", "它"],
    },
}


def softmax_weights(score_table: dict[str, float]) -> np.ndarray:
    raw_scores = np.array([score_table[token] for token in TOKENS])
    exp_scores = np.exp(raw_scores)
    return exp_scores / exp_scores.sum()


LEFT_VALUES = softmax_weights(RAW_SCORES_BY_TARGET["그것"])
RIGHT_VALUES = softmax_weights(RAW_SCORES_BY_TARGET["씌우지"])


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


def draw_panel(
    ax,
    values: np.ndarray,
    title: str,
    tokens: list[str],
    ylabel: str,
    xlabel: str,
    current_token: str,
) -> None:
    colors = ["#38bdf8"] * len(tokens)
    top_index = int(np.argmax(values))
    colors[top_index] = "#2563eb"
    if current_token in tokens:
        current_index = tokens.index(current_token)
        if current_index != top_index:
            colors[current_index] = "#0f766e"
    positions = np.arange(len(tokens))
    ax.set_facecolor("#f8fafc")
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.bar(positions, values, color=colors, width=0.62)
    ax.set_xticks(positions)
    ax.set_xticklabels(tokens, fontsize=8.0)
    ax.set_ylim(0, 0.58)
    ax.text(0.03, 0.93, title, transform=ax.transAxes, fontsize=10.3, fontweight="bold", color="#172033")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    for idx, value in enumerate(values):
        ax.text(idx, value + 0.015, f"{value:.3f}", ha="center", fontsize=7.8, color="#334155")


def save_chart(text: dict[str, str]) -> None:
    configure_font(text)
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 4.0), dpi=160)
    fig.patch.set_facecolor("white")

    draw_panel(axes[0], LEFT_VALUES, text["panel_left"], text["tokens"], text["ylabel"], text["xlabel"], text["tokens"][-1])
    draw_panel(axes[1], RIGHT_VALUES, text["panel_right"], text["tokens"], text["ylabel"], text["xlabel"], text["tokens"][3])

    fig.tight_layout(pad=0.9, w_pad=1.2)
    out_path = OUT_DIR / text["outfile"]
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    inject_accessibility(out_path, text["title"], text["desc"])


def save_single_chart(
    text: dict[str, str],
    values: np.ndarray,
    panel_title: str,
    outfile: str,
    svg_title: str,
    svg_desc: str,
) -> None:
    configure_font(text)
    fig, ax = plt.subplots(figsize=(4.1, 4.0), dpi=160)
    fig.patch.set_facecolor("white")
    current_token = text["tokens"][-1] if values is LEFT_VALUES else text["tokens"][3]
    draw_panel(ax, values, panel_title, text["tokens"], text["ylabel"], text["xlabel"], current_token)

    fig.tight_layout(pad=0.9)
    out_path = OUT_DIR / outfile
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    inject_accessibility(out_path, svg_title, svg_desc)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)
        save_single_chart(
            text,
            LEFT_VALUES,
            text["panel_left"],
            text["it_outfile"],
            text["it_title"],
            text["it_desc"],
        )
        save_single_chart(
            text,
            RIGHT_VALUES,
            text["panel_right"],
            text["cover_outfile"],
            text["cover_title"],
            text["cover_desc"],
        )


if __name__ == "__main__":
    main()
