"""Plot three fictional segment summaries; connecting lines are visual guides."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

BASE = Path(__file__).resolve().parent
FONT = FontProperties(fname="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
LABELS = {
    "en": (["Early", "Middle", "Late"], "Segment mean flow (L/min)"),
    "ko": (["초반", "중반", "후반"], "구간 평균 유량 (L/min)"),
    "zh": (["前段", "中段", "后段"], "区段平均流量 (L/min)"),
}

def main():
    with (BASE / "p3_5_2_segment_patterns.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))[:3]
    for lang, (ticks, ylabel) in LABELS.items():
        fig, ax = plt.subplots(figsize=(8, 4.4), constrained_layout=True)
        for row, color, marker, style in zip(rows, ["#1764ab", "#36853b", "#c44d32"], ["o", "s", "^"], ["-", "--", "-."]):
            values = [float(row[f"{s}_flow_mean"]) for s in ["early", "mid", "late"]]
            ax.plot(range(3), values, label=row["event_id"], color=color, marker=marker, linestyle=style, linewidth=2, markersize=8)
        ax.set_xticks(range(3), ticks, fontproperties=FONT, fontsize=13)
        ax.set_ylabel(ylabel, fontproperties=FONT, fontsize=13)
        ax.set_ylim(1.5, 3.15)
        ax.set_yticks([1.5, 1.8, 2.1, 2.4, 2.7, 3.0])
        ax.grid(axis="y", alpha=.25)
        ax.legend(loc="lower center", ncol=3, fontsize=12)
        ax.spines[["top", "right"]].set_visible(False)
        fig.savefig(BASE / f"p3-5-2-patterns-{lang}.png", dpi=150)
        plt.close(fig)

if __name__ == "__main__":
    main()
