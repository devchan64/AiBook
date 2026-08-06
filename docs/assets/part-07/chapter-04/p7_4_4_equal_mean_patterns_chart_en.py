"""Draw the English P7-4.4 equal-mean pattern comparison chart."""

import csv
import os
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
DATA_PATH = ASSET_DIR / "p7-action-unit-pattern-pairs.csv"
OUTPUT_PATH = ASSET_DIR / "p7-4-4-equal-mean-patterns-chart-en.png"
COLORS = {"rising": "#2563eb", "flat": "#64748b", "falling": "#dc2626", "middle_high": "#7c3aed", "edge_high": "#0f766e"}
SHAPES = {"rising": "rising", "flat": "flat", "falling": "falling", "middle_high": "middle-high", "edge_high": "edge-high"}

def read_records() -> list[dict[str, object]]:
    rows = list(csv.DictReader(DATA_PATH.open(encoding="utf-8")))
    return [{"event_id": row["event_id"], "shape": row["expected_shape"], "values": [float(row[f"segment_{index}"]) for index in range(1, 5)]} for row in rows if row["event_id"] in {f"PAT-{index:02d}" for index in range(1, 7)}]

def main() -> None:
    records = read_records()
    fig, axes = plt.subplots(2, 3, figsize=(11.8, 6.5), dpi=180, sharex=True, sharey=True)
    for axis, record in zip(axes.flat, records):
        shape = str(record["shape"])
        axis.plot([1, 2, 3, 4], record["values"], color=COLORS[shape], marker="o", linewidth=2.4)
        axis.axhline(2.5, color="#64748b", linestyle="--", linewidth=1.1, label="mean 2.5")
        axis.set_title(f"{record['event_id']} · {SHAPES[shape]}", fontsize=11.5, pad=8)
        axis.set_xticks([1, 2, 3, 4]); axis.set_ylim(1.5, 3.55)
        axis.grid(True, axis="y", color="#d1d5db", linewidth=0.75)
        axis.spines[["top", "right"]].set_visible(False)
    for axis in axes[:, 0]: axis.set_ylabel("segment value")
    for axis in axes[1, :]: axis.set_xlabel("segment order")
    axes[0, 2].legend(frameon=False, loc="upper right", fontsize=8.5)
    fig.suptitle("Same mean 2.5, different sequence patterns", fontsize=16, fontweight="bold")
    fig.tight_layout(pad=1.2, rect=(0, 0, 1, 0.94))
    fig.savefig(OUTPUT_PATH, bbox_inches="tight")
    plt.close(fig)
    print(f"saved={OUTPUT_PATH.relative_to(REPO_ROOT)}")

if __name__ == "__main__":
    main()
