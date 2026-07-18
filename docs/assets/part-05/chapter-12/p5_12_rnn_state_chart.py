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
        "outfile": "rnn-sequence-state-contrast-ko.svg",
        "gradual_outfile": "rnn-gradual-rise-state-ko.svg",
        "spike_outfile": "rnn-temporary-spike-state-ko.svg",
        "title": "같은 마지막 값에서도 순차 상태가 달라지는 비교",
        "desc": "gradual rise와 temporary spike가 모두 마지막 값 80으로 끝나지만, 직전 추세와 누적 상태가 달라 상태 기반 경보 판정이 달라질 수 있음을 보여 주는 비교 그래프.",
        "gradual_title": "점진 상승 시퀀스 상태",
        "gradual_desc": "마지막 값 80으로 끝나는 gradual rise 시퀀스가 직전까지 상승 흐름을 누적해 상태 기반 경보로 이어질 수 있음을 보여 주는 그래프.",
        "spike_title": "일시 급등 시퀀스 상태",
        "spike_desc": "마지막 값 80으로 끝나는 temporary spike 시퀀스가 중간 급등 뒤 다시 낮아졌다가 끝나, gradual rise와 다른 상태 누적을 남긴다는 점을 보여 주는 그래프.",
        "left": "gradual_rise",
        "right": "temporary_spike",
        "input": "입력값",
        "state": "누적 상태",
        "xlabel": "step",
        "ylabel": "값",
        "threshold": "threshold 63",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "rnn-sequence-state-contrast-en.svg",
        "gradual_outfile": "rnn-gradual-rise-state-en.svg",
        "spike_outfile": "rnn-temporary-spike-state-en.svg",
        "title": "Sequence-state contrast despite the same final value",
        "desc": "A comparison chart showing that gradual rise and temporary spike both end at the final value 80, but their recent trend and accumulated state differ enough to change a state-based alert decision.",
        "gradual_title": "Gradual-rise sequence state",
        "gradual_desc": "A chart showing that a gradual-rise sequence ending at 80 preserves a rising trend into the accumulated state.",
        "spike_title": "Temporary-spike sequence state",
        "spike_desc": "A chart showing that a temporary-spike sequence ending at 80 leaves a different accumulated state because it rose sharply and then dropped before the final value.",
        "left": "gradual_rise",
        "right": "temporary_spike",
        "input": "input value",
        "state": "accumulated state",
        "xlabel": "step",
        "ylabel": "value",
        "threshold": "threshold 63",
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
        "outfile": "rnn-sequence-state-contrast-zh.svg",
        "gradual_outfile": "rnn-gradual-rise-state-zh.svg",
        "spike_outfile": "rnn-temporary-spike-state-zh.svg",
        "title": "即使最终值相同，序列状态也可能不同",
        "desc": "比较图显示 gradual rise 与 temporary spike 虽然都以最终值 80 结束，但最近趋势和累积状态不同，因此基于状态的警报判定也可能不同。",
        "gradual_title": "gradual rise 序列状态",
        "gradual_desc": "该图显示：以 80 结束的 gradual rise 序列，会把持续上升的流向保留进累积状态里。",
        "spike_title": "temporary spike 序列状态",
        "spike_desc": "该图显示：以 80 结束的 temporary spike 序列，因为中间先急升后回落，所以留下了与 gradual rise 不同的累积状态。",
        "left": "gradual_rise",
        "right": "temporary_spike",
        "input": "输入值",
        "state": "累积状态",
        "xlabel": "step",
        "ylabel": "数值",
        "threshold": "阈值 63",
    },
}

LEFT_SEQ = np.array([60, 65, 72, 80])
RIGHT_SEQ = np.array([80, 60, 60, 80])


def accumulated_state(seq: np.ndarray, alpha: float = 0.6) -> np.ndarray:
    state = 0.0
    states = []
    for value in seq:
        state = alpha * state + (1 - alpha) * value
        states.append(state)
    return np.array(states)


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
    x = np.arange(1, 5)
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.9), dpi=160, sharey=True)
    fig.patch.set_facecolor("white")
    for ax, label, seq, color in zip(axes, [text["left"], text["right"]], [LEFT_SEQ, RIGHT_SEQ], ["#2563eb", "#dc2626"]):
        states = accumulated_state(seq)
        ax.set_facecolor("#f8fafc")
        ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.85)
        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.plot(x, seq, color="#64748b", linewidth=1.7, marker="o", markersize=4.2, label=text["input"])
        ax.plot(x, states, color=color, linewidth=2.6, marker="o", markersize=4.8, label=text["state"])
        ax.axhline(63, color="#94a3b8", linewidth=1.0, linestyle=(0, (4, 4)))
        ax.text(1.04, 64.5, text["threshold"], fontsize=8.0, color="#64748b")
        ax.text(0.03, 0.93, label, transform=ax.transAxes, fontsize=10.3, fontweight="bold", color="#172033")
        ax.set_xlabel(text["xlabel"])
        ax.set_xticks(x)
        ax.legend(frameon=False, loc="lower right", fontsize=7.8)
    axes[0].set_ylabel(text["ylabel"])
    axes[0].set_ylim(0, 88)

    fig.tight_layout(pad=0.9, w_pad=1.4)
    out_path = OUT_DIR / text["outfile"]
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    inject_accessibility(out_path, text["title"], text["desc"])


def save_single_chart(text: dict[str, str], seq: np.ndarray, color: str, title: str, outfile: str, svg_title: str, svg_desc: str) -> None:
    configure_font(text)
    x = np.arange(1, 5)
    states = accumulated_state(seq)
    fig, ax = plt.subplots(figsize=(4.0, 3.9), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#f8fafc")
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.plot(x, seq, color="#64748b", linewidth=1.7, marker="o", markersize=4.2, label=text["input"])
    ax.plot(x, states, color=color, linewidth=2.6, marker="o", markersize=4.8, label=text["state"])
    ax.axhline(63, color="#94a3b8", linewidth=1.0, linestyle=(0, (4, 4)))
    ax.text(1.04, 64.5, text["threshold"], fontsize=8.0, color="#64748b")
    ax.set_xlabel(text["xlabel"])
    ax.set_ylabel(text["ylabel"])
    ax.set_xticks(x)
    ax.set_ylim(0, 88)
    ax.legend(frameon=False, loc="lower right", fontsize=8.0)

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
            LEFT_SEQ,
            "#2563eb",
            text["left"],
            text["gradual_outfile"],
            text["gradual_title"],
            text["gradual_desc"],
        )
        save_single_chart(
            text,
            RIGHT_SEQ,
            "#dc2626",
            text["right"],
            text["spike_outfile"],
            text["spike_title"],
            text["spike_desc"],
        )


if __name__ == "__main__":
    main()
