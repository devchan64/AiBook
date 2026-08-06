from collections import defaultdict
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
from matplotlib import font_manager
from matplotlib.patches import Rectangle

ASSET_DIR = Path(__file__).resolve().parent
DATA_PATH = ASSET_DIR / "p7-1-traffic-log.csv"
OUTPUT_PATH = ASSET_DIR / "p7-1-2-candidate-threshold-chart-ko.png"
CUTOFF = "2026-06-08"
KOREAN_FONT_PATH = Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")

CHANNEL_COLORS = {
    "organic": "#2f855a",
    "search": "#2563eb",
    "ads": "#c2410c",
}


def choose_font() -> str:
    system_fonts = [Path(path) for path in font_manager.findSystemFonts()]
    candidates = [KOREAN_FONT_PATH] + [
        path
        for path in system_fonts
        if "NotoSansCJK" in path.name or "Nanum" in path.name
    ]
    for path in candidates:
        if path.exists():
            font_manager.fontManager.addfont(str(path))
            return font_manager.FontProperties(fname=str(path)).get_name()
    raise RuntimeError("한글 차트에는 Noto Sans CJK 또는 Nanum 계열 폰트가 필요합니다.")


def read_rows() -> list[dict[str, object]]:
    with DATA_PATH.open(encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    for row in rows:
        row["visitors"] = int(row["visitors"])
        row["signups"] = int(row["signups"])
        row["errors"] = int(row["errors"])
    return rows


def collect_points(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    baseline_rows = [row for row in rows if row["date"] < CUTOFF]
    recent_rows = [row for row in rows if row["date"] >= CUTOFF]
    totals = defaultdict(lambda: {"visitors": 0, "signups": 0, "errors": 0})
    for row in baseline_rows:
        channel_totals = totals[row["channel"]]
        channel_totals["visitors"] += row["visitors"]
        channel_totals["signups"] += row["signups"]
        channel_totals["errors"] += row["errors"]

    points = []
    for row in recent_rows:
        baseline = totals[row["channel"]]
        baseline_conversion = baseline["signups"] / baseline["visitors"]
        baseline_error = baseline["errors"] / baseline["visitors"]
        conversion_delta = row["signups"] / row["visitors"] - baseline_conversion
        error_delta = row["errors"] / row["visitors"] - baseline_error
        points.append(
            {
                "date": row["date"],
                "channel": row["channel"],
                "conversion_delta_pp": conversion_delta * 100,
                "error_delta_pp": error_delta * 100,
                "common_candidate": conversion_delta <= -0.035 and error_delta >= 0.012,
            }
        )
    return points


def main() -> None:
    plt.rcParams["font.family"] = choose_font()
    plt.rcParams["axes.unicode_minus"] = False

    points = collect_points(read_rows())
    fig, ax = plt.subplots(figsize=(8.8, 5.4), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#ffffff")

    # The upper-left area is where both review rules select the same row.
    ax.add_patch(
        Rectangle(
            (-5.1, 1.2),
            1.6,
            1.1,
            facecolor="#fee2e2",
            edgecolor="none",
            alpha=0.7,
            zorder=0,
        )
    )
    ax.text(-4.98, 2.17, "공통 후보 영역", color="#991b1b", fontsize=10, weight="bold")

    for channel, color in CHANNEL_COLORS.items():
        channel_points = [point for point in points if point["channel"] == channel]
        ax.scatter(
            [point["conversion_delta_pp"] for point in channel_points],
            [point["error_delta_pp"] for point in channel_points],
            label=channel,
            color=color,
            s=46,
            alpha=0.9,
            edgecolor="white",
            linewidth=0.7,
            zorder=3,
        )

    label_offsets = {
        "2026-06-11": (7, 13),
        "2026-06-12": (7, -15),
        "2026-06-14": (7, 1),
    }
    for point in points:
        if point["common_candidate"]:
            ax.annotate(
                point["date"][5:],
                (point["conversion_delta_pp"], point["error_delta_pp"]),
                xytext=label_offsets[point["date"]],
                textcoords="offset points",
                fontsize=9,
                color="#7c2d12",
                weight="bold",
            )

    ax.axvline(-3.5, color="#dc2626", linestyle="--", linewidth=1.4)
    ax.axvline(-2.5, color="#2563eb", linestyle="--", linewidth=1.4)
    ax.axhline(0.9, color="#dc2626", linestyle="--", linewidth=1.4)
    ax.axhline(1.2, color="#2563eb", linestyle="--", linewidth=1.4)
    ax.text(-3.5, -0.37, "전환율 중심 -3.5%p", color="#b91c1c", fontsize=9, ha="right")
    ax.text(-2.5, -0.57, "오류율 중심 -2.5%p", color="#1d4ed8", fontsize=9, ha="right")
    ax.text(0.9, 0.93, "전환율 중심 +0.9%p", color="#b91c1c", fontsize=9, va="bottom")
    ax.text(0.9, 1.23, "오류율 중심 +1.2%p", color="#1d4ed8", fontsize=9, va="bottom")

    ax.set_xlim(-5.1, 1.15)
    ax.set_ylim(-0.65, 2.3)
    ax.set_xlabel("전환율 변화(%p, 기준선 대비)")
    ax.set_ylabel("오류율 변화(%p, 기준선 대비)")
    ax.grid(True, color="#d1d5db", linewidth=0.7, alpha=0.8)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(title="채널", frameon=False, loc="lower right")

    fig.tight_layout(pad=1.2)
    fig.savefig(OUTPUT_PATH, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
