"""P7-4.2의 OOV·coverage 실패 분해 기록을 PNG 차트로 만든다."""

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
from matplotlib.patches import Patch
import numpy as np

ASSET_DIR = Path(__file__).resolve().parent
DATA_PATH = ASSET_DIR / "p7-4-support-routing-dataset.csv"
OUTPUT_PATH = ASSET_DIR / "p7-4-2-coverage-review-chart-ko.png"
KOREAN_FONT_PATH = Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")


def choose_font() -> str:
    system_fonts = [Path(path) for path in font_manager.findSystemFonts()]
    candidates = [KOREAN_FONT_PATH] + [
        path
        for path in system_fonts
        if "NotoSansCJK" in path.name or "Nanum" in path.name
    ]
    for candidate in candidates:
        if candidate.exists():
            font_manager.fontManager.addfont(str(candidate))
            return font_manager.FontProperties(fname=str(candidate)).get_name()
    raise RuntimeError("한글 차트에는 Noto Sans CJK 또는 Nanum 계열 폰트가 필요합니다.")


def tokenize(text: str) -> list[str]:
    return text.split()


def collect_records() -> list[dict[str, object]]:
    rows = list(csv.DictReader(DATA_PATH.open(encoding="utf-8")))
    train_rows = [row for row in rows if row["split"] == "train"]
    test_rows = [row for row in rows if row["split"] == "test"]
    vocabulary = {token for row in train_rows for token in tokenize(row["text"])}
    class_profiles = {0: {}, 1: {}}

    for row in train_rows:
        profile = class_profiles[int(row["label"])]
        for token in tokenize(row["text"]):
            profile[token] = profile.get(token, 0) + 1

    records = []
    for row in test_rows:
        tokens = tokenize(row["text"])
        known = [token for token in tokens if token in vocabulary]
        scores = [sum(class_profiles[label].get(token, 0) for token in known) for label in (0, 1)]
        prediction = int(np.argmax(scores))
        actual = int(row["label"])
        records.append(
            {
                "sample": row["sample_id"].replace("평가-", ""),
                "coverage": len(known) / len(tokens),
                "scores": scores,
                "correct": prediction == actual,
            }
        )
    return records


def style_axis(axis) -> None:
    axis.grid(True, axis="y", color="#d1d5db", linewidth=0.75, alpha=0.9)
    axis.set_axisbelow(True)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)


def main() -> None:
    plt.rcParams["font.family"] = choose_font()
    plt.rcParams["axes.unicode_minus"] = False
    records = collect_records()
    labels = [str(record["sample"]) for record in records]
    positions = np.arange(len(records))
    fig, (coverage_ax, score_ax) = plt.subplots(1, 2, figsize=(11.8, 4.8), dpi=180)
    fig.patch.set_facecolor("white")

    colors = ["#15803d" if record["correct"] else "#dc2626" for record in records]
    coverage_ax.bar(positions, [record["coverage"] for record in records], color=colors, width=0.64)
    coverage_ax.axhline(0.5, color="#64748b", linestyle="--", linewidth=1.3, label="낮은 coverage 기준")
    coverage_ax.set_ylim(0, 1.12)
    coverage_ax.set_xticks(positions, labels, rotation=15, ha="right")
    coverage_ax.set_ylabel("기존 어휘 포함 비율")
    coverage_ax.set_title("평가 문장별 coverage")
    coverage_ax.legend(
        handles=[
            Patch(color="#15803d", label="정답"),
            Patch(color="#dc2626", label="오답"),
            plt.Line2D([], [], color="#64748b", linestyle="--", label="낮은 coverage 기준"),
        ],
        frameon=False,
        loc="upper right",
        fontsize=8.5,
    )
    style_axis(coverage_ax)

    focus_records = [record for record in records if record["sample"] in {"05", "07"}]
    focus_positions = np.arange(len(focus_records))
    width = 0.30
    refund_scores = [int(record["scores"][0]) for record in focus_records]
    delivery_scores = [int(record["scores"][1]) for record in focus_records]
    score_ax.bar(focus_positions - width / 2, refund_scores, width, label="환불팀 점수", color="#2563eb")
    score_ax.bar(focus_positions + width / 2, delivery_scores, width, label="배송팀 점수", color="#ea580c")
    for position, record in zip(focus_positions, focus_records):
        result = "정답" if record["correct"] else "오답"
        score_ax.text(position, max(record["scores"]) + 0.32, result, ha="center", weight="bold", color="#15803d" if record["correct"] else "#dc2626")
    score_ax.set_ylim(0, 8.2)
    score_ax.set_xticks(focus_positions, ["평가-05\n캔슬·송장", "평가-07\n하자·환불"])
    score_ax.set_ylabel("학습 어휘 점수")
    score_ax.set_title("같은 낮은 coverage, 다른 팀 점수")
    score_ax.legend(frameon=False, loc="upper left")
    style_axis(score_ax)

    fig.suptitle("낮은 coverage는 같은 실패가 아니다", fontsize=15, fontweight="bold")
    fig.tight_layout(pad=1.0, rect=(0, 0, 1, 0.92))
    fig.savefig(OUTPUT_PATH, bbox_inches="tight")
    plt.close(fig)
    print(f"saved={OUTPUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
