"""P7-1.3의 두 채널-일자 기준선 설계가 만드는 변화량과 표본 수를 그린다."""

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
from matplotlib import font_manager

ASSET_DIR = Path(__file__).resolve().parent
DATA_PATH = ASSET_DIR / "p7-1-traffic-log.csv"
OUTPUT_PATH = ASSET_DIR / "p7-1-3-baseline-design-chart-ko.png"
DESIGNS = [
    ("7일 기준선\n기준 7일 / 최근 7일", "2026-06-08"),
    ("최근 4일 집중\n기준 10일 / 최근 4일", "2026-06-11"),
]


def choose_font() -> str:
    candidates = ["Noto Sans CJK KR", "Noto Sans CJK JP", "NanumGothic", "DejaVu Sans"]
    available = {font.name for font in font_manager.fontManager.ttflist}
    return next((font for font in candidates if font in available), "DejaVu Sans")


def read_rows() -> list[dict[str, object]]:
    with DATA_PATH.open(encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    for row in rows:
        row["date"] = datetime.strptime(row["date"], "%Y-%m-%d").date()
        row["visitors"] = int(row["visitors"])
        row["signups"] = int(row["signups"])
        row["errors"] = int(row["errors"])
    return rows


def rate(rows: list[dict[str, object]], column: str) -> float:
    return sum(row[column] for row in rows) / sum(row["visitors"] for row in rows) * 100


def collect_comparisons(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ads_rows = [row for row in rows if row["channel"] == "ads"]
    comparisons = []
    for name, cutoff_text in DESIGNS:
        cutoff = datetime.strptime(cutoff_text, "%Y-%m-%d").date()
        baseline = [row for row in ads_rows if row["date"] < cutoff]
        recent = [row for row in ads_rows if row["date"] >= cutoff]
        # 본문 Python 예제처럼 각 구간 비율을 소수 넷째 자리에서 표시한 뒤 차이를 낸다.
        baseline_conversion = round(rate(baseline, "signups") / 100, 4)
        recent_conversion = round(rate(recent, "signups") / 100, 4)
        baseline_error = round(rate(baseline, "errors") / 100, 4)
        recent_error = round(rate(recent, "errors") / 100, 4)
        comparisons.append(
            {
                "name": name,
                "conversion_delta": (recent_conversion - baseline_conversion) * 100,
                "error_delta": (recent_error - baseline_error) * 100,
                "baseline_count": len(baseline),
                "recent_count": len(recent),
            }
        )
    return comparisons


def add_bar_labels(ax: plt.Axes, bars: object) -> None:
    for bar in bars:
        value = bar.get_height()
        offset = -0.18 if value < 0 else 0.12
        va = "top" if value < 0 else "bottom"
        ax.text(bar.get_x() + bar.get_width() / 2, value + offset, f"{value:+.2f}%p", ha="center", va=va, fontsize=10, weight="bold")


def main() -> None:
    plt.rcParams["font.family"] = choose_font()
    plt.rcParams["axes.unicode_minus"] = False
    comparisons = collect_comparisons(read_rows())
    labels = [item["name"] for item in comparisons]
    positions = range(len(comparisons))

    fig, (conversion_ax, error_ax) = plt.subplots(1, 2, figsize=(10.8, 4.8), dpi=180)
    fig.patch.set_facecolor("white")
    for ax, key, title, color in (
        (conversion_ax, "conversion_delta", "ads 전환율 변화", "#c2410c"),
        (error_ax, "error_delta", "ads 오류율 변화", "#2563eb"),
    ):
        ax.set_facecolor("white")
        bars = ax.bar(positions, [item[key] for item in comparisons], color=color, width=0.58)
        ax.axhline(0, color="#6b7280", linewidth=1.0)
        ax.grid(axis="y", color="#d1d5db", linewidth=0.7, alpha=0.85)
        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_title(title, fontsize=14, pad=12)
        ax.set_ylabel("기준선 대비 변화(%p)")
        ax.set_xticks(list(positions), labels, fontsize=10)
        add_bar_labels(ax, bars)

    conversion_ax.set_ylim(-4.35, 0.8)
    error_ax.set_ylim(-0.25, 1.65)
    for position, item in enumerate(comparisons):
        conversion_ax.text(position, 0.47, f"표본: 기준 {item['baseline_count']}건 / 최근 {item['recent_count']}건", ha="center", fontsize=9, color="#4b5563")

    fig.tight_layout(pad=1.4)
    fig.savefig(OUTPUT_PATH, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
