from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CACHE = ROOT / ".tmp" / "matplotlib-cache"
CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(CACHE))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

OUT = Path(__file__).with_name("p7-2-2-normalization-outcome-chart-zh.png")


def chinese_font() -> str:
    for path in font_manager.findSystemFonts():
        candidate = Path(path)
        if "NotoSansCJK" in candidate.name or "Nanum" in candidate.name:
            font_manager.fontManager.addfont(str(candidate))
            return font_manager.FontProperties(fname=str(candidate)).get_name()
    raise RuntimeError("中文图表需要 Noto Sans CJK 或 Nanum 字体。")


def main() -> None:
    plt.rcParams["font.family"] = chinese_font()
    plt.rcParams["axes.unicode_minus"] = False
    labels = ["两者正确", "标准化恢复", "标准化新错", "两者错误"]
    counts = [4, 2, 0, 0]
    colors = ["#2f855a", "#2563eb", "#dc2626", "#64748b"]
    fig, ax = plt.subplots(figsize=(8.2, 4.8), constrained_layout=True)
    bars = ax.bar(labels, counts, color=colors, width=0.62)
    ax.set(title="raw 1-NN 与标准化 1-NN 的评估转换", ylabel="评估样本数", ylim=(0, 4.8))
    ax.grid(axis="y", alpha=0.22)
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, count + 0.12, str(count), ha="center", va="bottom", fontsize=12, fontweight="bold")
    fig.text(0.5, 0.01, "评估-02、评估-04 经标准化后恢复；本次没有新错误。", ha="center")
    fig.savefig(OUT, dpi=170, bbox_inches="tight")


if __name__ == "__main__":
    main()
