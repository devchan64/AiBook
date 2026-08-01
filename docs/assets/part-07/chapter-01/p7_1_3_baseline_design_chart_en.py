"""Draw the English P7-1.3 baseline-design comparison chart."""

import csv
import os
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
MPL_CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))
os.environ.setdefault("XDG_CACHE_HOME", str(MPL_CACHE))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ASSET_DIR = Path(__file__).resolve().parent
DATA_PATH = ASSET_DIR / "p7-1-traffic-log.csv"
OUTPUT_PATH = ASSET_DIR / "p7-1-3-baseline-design-chart-en.png"
DESIGNS = [("7-day baseline\n7 baseline / 7 recent", "2026-06-08"), ("Recent 4-day focus\n10 baseline / 4 recent", "2026-06-11")]


def comparisons() -> list[dict[str, object]]:
    with DATA_PATH.open(encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    for row in rows:
        row["date"] = datetime.strptime(row["date"], "%Y-%m-%d").date()
        for column in ("visitors", "signups", "errors"):
            row[column] = int(row[column])
    ads = [row for row in rows if row["channel"] == "ads"]
    collected = []
    for name, cutoff_text in DESIGNS:
        cutoff = datetime.strptime(cutoff_text, "%Y-%m-%d").date()
        baseline, recent = [row for row in ads if row["date"] < cutoff], [row for row in ads if row["date"] >= cutoff]
        rate = lambda records, column: round(sum(row[column] for row in records) / sum(row["visitors"] for row in records), 4)
        collected.append({"name": name, "conversion_delta": (rate(recent, "signups") - rate(baseline, "signups")) * 100, "error_delta": (rate(recent, "errors") - rate(baseline, "errors")) * 100, "baseline_count": len(baseline), "recent_count": len(recent)})
    return collected


def main() -> None:
    data = comparisons()
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.8), dpi=180)
    fig.patch.set_facecolor("white")
    for ax, key, title, color in ((axes[0], "conversion_delta", "Ads conversion-rate change", "#c2410c"), (axes[1], "error_delta", "Ads error-rate change", "#2563eb")):
        values = [item[key] for item in data]
        bars = ax.bar(range(len(data)), values, color=color, width=.58)
        ax.axhline(0, color="#6b7280", linewidth=1)
        ax.grid(axis="y", color="#d1d5db", linewidth=.7, alpha=.85)
        ax.set_axisbelow(True); ax.spines[["top", "right"]].set_visible(False)
        ax.set_title(title, fontsize=14, pad=12); ax.set_ylabel("Change from baseline (%p)")
        ax.set_xticks(range(len(data)), [item["name"] for item in data], fontsize=10)
        for bar in bars:
            value = bar.get_height(); ax.text(bar.get_x()+bar.get_width()/2, value+(-.18 if value < 0 else .12), f"{value:+.2f}%p", ha="center", va="top" if value < 0 else "bottom", fontsize=10, weight="bold")
    axes[0].set_ylim(-4.35, .8); axes[1].set_ylim(-.25, 1.65)
    for position, item in enumerate(data):
        axes[0].text(position, .47, f"Samples: {item['baseline_count']} baseline / {item['recent_count']} recent", ha="center", fontsize=9, color="#4b5563")
    fig.tight_layout(pad=1.4); fig.savefig(OUTPUT_PATH, bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    main()
