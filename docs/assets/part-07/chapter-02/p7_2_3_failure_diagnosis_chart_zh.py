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

OUT = Path(__file__).with_name("p7-2-3-failure-diagnosis-chart-zh.png")


def pick_font() -> str:
    for path in font_manager.findSystemFonts():
        candidate = Path(path)
        if "NotoSansCJK" in candidate.name or "Nanum" in candidate.name:
            font_manager.fontManager.addfont(str(candidate))
            return font_manager.FontProperties(fname=str(candidate)).get_name()
    raise RuntimeError("中文图表需要 Noto Sans CJK 或 Nanum 字体。")


def main() -> None:
    plt.rcParams["font.family"] = pick_font()
    plt.rcParams["axes.unicode_minus"] = False
    fig, (score_ax, diagnosis_ax) = plt.subplots(1, 2, figsize=(11.2, 4.8), constrained_layout=True)
    variants, scores = ["基线", "原始 1-NN", "部分缩放", "z-score"], [0.361, 0.861, 0.722, 0.833]
    bars = score_ax.bar(variants, scores, color=["#64748b", "#c2410c", "#2563eb", "#2f855a"])
    score_ax.set(title="压力评估集上的设置比较", ylabel="准确率", ylim=(0, 1.0))
    score_ax.grid(axis="y", alpha=0.22)
    for bar, score in zip(bars, scores): score_ax.text(bar.get_x() + bar.get_width()/2, score + .025, f"{score:.3f}", ha="center")
    labels, counts = ["预处理恢复", "仍需调查", "设置敏感", "稳定正确"], [5, 6, 8, 17]
    bars = diagnosis_ax.bar(labels, counts, color=["#2f855a", "#dc2626", "#7c3aed", "#64748b"])
    diagnosis_ax.set(title="样本级失败诊断", ylabel="压力样本数", ylim=(0, 20))
    diagnosis_ax.grid(axis="y", alpha=0.22)
    for bar, count in zip(bars, counts): diagnosis_ax.text(bar.get_x() + bar.get_width()/2, count + .35, str(count), ha="center")
    fig.savefig(OUT, dpi=170, bbox_inches="tight")


if __name__ == "__main__":
    main()
