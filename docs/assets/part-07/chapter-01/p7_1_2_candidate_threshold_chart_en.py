"""Draw the English P7-1.2 candidate-threshold chart from the practice CSV."""

import csv
import os
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
MPL_CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))
os.environ.setdefault("XDG_CACHE_HOME", str(MPL_CACHE))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ASSET_DIR = Path(__file__).resolve().parent
DATA_PATH = ASSET_DIR / "p7-1-traffic-log.csv"
OUTPUT_PATH = ASSET_DIR / "p7-1-2-candidate-threshold-chart-en.png"
CUTOFF = "2026-06-08"
CHANNEL_COLORS = {"organic": "#2f855a", "search": "#2563eb", "ads": "#c2410c"}


def collect_points() -> list[dict[str, object]]:
    with DATA_PATH.open(encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    for row in rows:
        for column in ("visitors", "signups", "errors"):
            row[column] = int(row[column])
    totals = defaultdict(lambda: {"visitors": 0, "signups": 0, "errors": 0})
    for row in rows:
        if row["date"] < CUTOFF:
            total = totals[row["channel"]]
            for column in ("visitors", "signups", "errors"):
                total[column] += row[column]
    points = []
    for row in rows:
        if row["date"] < CUTOFF:
            continue
        baseline = totals[row["channel"]]
        conversion_delta = row["signups"] / row["visitors"] - baseline["signups"] / baseline["visitors"]
        error_delta = row["errors"] / row["visitors"] - baseline["errors"] / baseline["visitors"]
        points.append({"date": row["date"], "channel": row["channel"], "conversion_delta_pp": conversion_delta * 100, "error_delta_pp": error_delta * 100, "common_candidate": conversion_delta <= -0.035 and error_delta >= 0.012})
    return points


def main() -> None:
    points = collect_points()
    fig, ax = plt.subplots(figsize=(8.8, 5.4), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.add_patch(Rectangle((-5.1, 1.2), 1.6, 1.1, facecolor="#fee2e2", edgecolor="none", alpha=0.7, zorder=0))
    ax.text(-4.98, 2.17, "Common-candidate region", color="#991b1b", fontsize=10, weight="bold")
    for channel, color in CHANNEL_COLORS.items():
        channel_points = [point for point in points if point["channel"] == channel]
        ax.scatter([point["conversion_delta_pp"] for point in channel_points], [point["error_delta_pp"] for point in channel_points], label=channel, color=color, s=46, alpha=0.9, edgecolor="white", linewidth=0.7, zorder=3)
    label_offsets = {"2026-06-11": (7, 13), "2026-06-12": (7, -15), "2026-06-14": (7, 1)}
    for point in points:
        if point["common_candidate"]:
            ax.annotate(point["date"][5:], (point["conversion_delta_pp"], point["error_delta_pp"]), xytext=label_offsets[point["date"]], textcoords="offset points", fontsize=9, color="#7c2d12", weight="bold")
    for x, color in ((-3.5, "#dc2626"), (-2.5, "#2563eb")):
        ax.axvline(x, color=color, linestyle="--", linewidth=1.4)
    for y, color in ((0.9, "#dc2626"), (1.2, "#2563eb")):
        ax.axhline(y, color=color, linestyle="--", linewidth=1.4)
    ax.text(-3.5, -0.37, "conversion-focused −3.5%p", color="#b91c1c", fontsize=9, ha="right")
    ax.text(-2.5, -0.57, "error-focused −2.5%p", color="#1d4ed8", fontsize=9, ha="right")
    ax.text(0.9, 0.93, "conversion-focused +0.9%p", color="#b91c1c", fontsize=9, va="bottom")
    ax.text(0.9, 1.23, "error-focused +1.2%p", color="#1d4ed8", fontsize=9, va="bottom")
    ax.set(xlim=(-5.1, 1.15), ylim=(-0.65, 2.3), xlabel="Conversion-rate change (%p from baseline)", ylabel="Error-rate change (%p from baseline)")
    ax.grid(True, color="#d1d5db", linewidth=0.7, alpha=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(title="Channel", frameon=False, loc="lower right")
    fig.tight_layout(pad=1.2)
    fig.savefig(OUTPUT_PATH, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
