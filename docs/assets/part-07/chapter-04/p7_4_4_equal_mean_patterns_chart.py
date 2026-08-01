"""P7-4.4의 같은 평균·다른 shape token 사례를 작은 선 그래프로 그린다."""

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

ASSET_DIR = Path(__file__).resolve().parent
DATA_PATH = ASSET_DIR / "p7-action-unit-pattern-pairs.csv"
OUTPUT_PATH = ASSET_DIR / "p7-4-4-equal-mean-patterns-chart-ko.png"
KOREAN_FONT_PATH = Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
COLORS = {
    "rising": "#2563eb",
    "flat": "#64748b",
    "falling": "#dc2626",
    "middle_high": "#7c3aed",
    "edge_high": "#0f766e",
}
KOREAN_SHAPES = {
    "rising": "상승형",
    "flat": "평탄형",
    "falling": "하강형",
    "middle_high": "중간 집중형",
    "edge_high": "양끝 집중형",
}


def choose_font() -> str:
    system_fonts = [Path(path) for path in font_manager.findSystemFonts()]
    candidates = [KOREAN_FONT_PATH] + [
        path for path in system_fonts if "NotoSansCJK" in path.name or "Nanum" in path.name
    ]
    for candidate in candidates:
        if candidate.exists():
            font_manager.fontManager.addfont(str(candidate))
            return font_manager.FontProperties(fname=str(candidate)).get_name()
    raise RuntimeError("한글 차트에는 Noto Sans CJK 또는 Nanum 계열 폰트가 필요합니다.")


def read_records() -> list[dict[str, object]]:
    rows = list(csv.DictReader(DATA_PATH.open(encoding="utf-8")))
    records = []
    for row in rows:
        if row["event_id"] not in {f"PAT-{index:02d}" for index in range(1, 7)}:
            continue
        values = [float(row[f"segment_{index}"]) for index in range(1, 5)]
        records.append({"event_id": row["event_id"], "shape": row["expected_shape"], "values": values})
    return records


def main() -> None:
    plt.rcParams["font.family"] = choose_font()
    plt.rcParams["axes.unicode_minus"] = False
    records = read_records()
    fig, axes = plt.subplots(2, 3, figsize=(11.8, 6.5), dpi=180, sharex=True, sharey=True)
    segments = [1, 2, 3, 4]

    for axis, record in zip(axes.flat, records):
        shape = str(record["shape"])
        values = list(record["values"])
        axis.plot(segments, values, color=COLORS[shape], marker="o", linewidth=2.4)
        axis.axhline(2.5, color="#64748b", linestyle="--", linewidth=1.1, label="평균 2.5")
        axis.set_title(f"{record['event_id']} · {KOREAN_SHAPES[shape]}", fontsize=11.5, pad=8)
        axis.set_xticks(segments, ["1", "2", "3", "4"])
        axis.set_ylim(1.5, 3.55)
        axis.grid(True, axis="y", color="#d1d5db", linewidth=0.75)
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)

    for axis in axes[:, 0]:
        axis.set_ylabel("구간 값")
    for axis in axes[1, :]:
        axis.set_xlabel("구간 순서")
    axes[0, 2].legend(frameon=False, loc="upper right", fontsize=8.5)
    fig.suptitle("같은 평균 2.5, 다른 순서 패턴", fontsize=16, fontweight="bold")
    fig.tight_layout(pad=1.2, rect=(0, 0, 1, 0.94))
    fig.savefig(OUTPUT_PATH, bbox_inches="tight")
    plt.close(fig)
    print(f"saved={OUTPUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
