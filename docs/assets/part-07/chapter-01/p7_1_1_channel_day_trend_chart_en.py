"""Redraw P7-1.1 channel-day conversion and error trends in English."""

import csv
import os
from collections import defaultdict
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
from matplotlib import dates as mdates

ASSET_DIR = Path(__file__).resolve().parent
DATA_PATH = ASSET_DIR / "p7-1-traffic-log.csv"
OUTPUT_PATH = ASSET_DIR / "p7-1-1-channel-day-trend-chart-en.png"
CUTOFF = datetime.strptime("2026-06-08", "%Y-%m-%d").date()

CHANNEL_COLORS = {"organic": "#2f855a", "search": "#2563eb", "ads": "#c2410c"}


def read_rows() -> list[dict[str, object]]:
    with DATA_PATH.open(encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    for row in rows:
        row["date"] = datetime.strptime(row["date"], "%Y-%m-%d").date()
        row["visitors"] = int(row["visitors"])
        row["signups"] = int(row["signups"])
        row["errors"] = int(row["errors"])
    return rows


def weighted_rate(rows: list[dict[str, object]], column: str) -> float:
    return sum(row[column] for row in rows) / sum(row["visitors"] for row in rows) * 100


def main() -> None:
    rows = read_rows()
    rows_by_channel = defaultdict(list)
    for row in rows:
        rows_by_channel[row["channel"]].append(row)

    fig, (conversion_ax, error_ax) = plt.subplots(2, 1, figsize=(10.5, 7.0), dpi=180, sharex=True)
    fig.patch.set_facecolor("white")
    for ax in (conversion_ax, error_ax):
        ax.set_facecolor("white")
        ax.axvspan(CUTOFF, max(row["date"] for row in rows), color="#fef3c7", alpha=0.62, zorder=0)
        ax.axvline(CUTOFF, color="#6b7280", linestyle="--", linewidth=1.2, zorder=1)
        ax.grid(True, color="#d1d5db", linewidth=0.7, alpha=0.85)
        ax.set_axisbelow(True)
        ax.spines[["top", "right"]].set_visible(False)

    for channel, channel_rows in sorted(rows_by_channel.items()):
        channel_rows.sort(key=lambda row: row["date"])
        dates = [row["date"] for row in channel_rows]
        conversion_rates = [row["signups"] / row["visitors"] * 100 for row in channel_rows]
        error_rates = [row["errors"] / row["visitors"] * 100 for row in channel_rows]
        color = CHANNEL_COLORS[channel]
        conversion_ax.plot(dates, conversion_rates, marker="o", markersize=3.7, linewidth=2.0, color=color, label=channel)
        error_ax.plot(dates, error_rates, marker="o", markersize=3.7, linewidth=2.0, color=color, label=channel)
        baseline_rows = [row for row in channel_rows if row["date"] < CUTOFF]
        conversion_ax.hlines(weighted_rate(baseline_rows, "signups"), min(dates), CUTOFF, color=color, linestyle=":", linewidth=1.6, alpha=0.9)
        error_ax.hlines(weighted_rate(baseline_rows, "errors"), min(dates), CUTOFF, color=color, linestyle=":", linewidth=1.6, alpha=0.9)

    conversion_ax.text(CUTOFF, 12.7, "Recent period begins", color="#4b5563", fontsize=10, ha="left", va="bottom")
    conversion_ax.set_ylabel("Conversion rate (%)")
    error_ax.set_ylabel("Error rate (%)")
    error_ax.set_xlabel("Date")
    conversion_ax.legend(title="Channel", frameon=False, loc="lower left", ncol=3)
    error_ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    error_ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    fig.autofmt_xdate(rotation=0)
    fig.tight_layout(pad=1.3)
    fig.savefig(OUTPUT_PATH, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
