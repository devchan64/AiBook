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
import numpy as np

ASSET_DIR = Path(__file__).resolve().parent
DATA_PATH = ASSET_DIR / "p7-2-churn-dataset.csv"
OUTPUT_PATH = ASSET_DIR / "p7-2-1-prediction-outcome-transition-ko.png"
KOREAN_FONT_PATH = Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")

OUTCOME_ORDER = ["둘 다 정답", "1-NN 회수", "1-NN 새 오답", "둘 다 오류"]
OUTCOME_COLORS = {
    "둘 다 정답": "#64748b",
    "1-NN 회수": "#15803d",
    "1-NN 새 오답": "#dc2626",
    "둘 다 오류": "#d97706",
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
        row["unresolved_tickets"] = int(row["unresolved_tickets"])
        row["days_since_login"] = int(row["days_since_login"])
        row["usage_minutes_30d"] = int(row["usage_minutes_30d"])
        row["label"] = int(row["label"])
    return rows


def collect_outcomes(rows: list[dict[str, object]]) -> dict[str, list[str]]:
    train_rows = [row for row in rows if row["split"] == "train"]
    test_rows = [row for row in rows if row["split"] == "test"]
    feature_columns = ["unresolved_tickets", "days_since_login", "usage_minutes_30d"]
    x_train = np.array([[row[column] for column in feature_columns] for row in train_rows], dtype=float)
    y_train = np.array([row["label"] for row in train_rows])
    baseline_class = int(np.bincount(y_train).argmax())
    outcomes = defaultdict(list)

    for row in test_rows:
        point = np.array([row[column] for column in feature_columns], dtype=float)
        nearest_index = int(np.argmin(np.linalg.norm(x_train - point, axis=1)))
        baseline_correct = baseline_class == row["label"]
        knn_correct = int(y_train[nearest_index]) == row["label"]
        if not baseline_correct and knn_correct:
            outcome = "1-NN 회수"
        elif baseline_correct and not knn_correct:
            outcome = "1-NN 새 오답"
        elif baseline_correct:
            outcome = "둘 다 정답"
        else:
            outcome = "둘 다 오류"
        outcomes[outcome].append(row["sample_id"])
    return outcomes


def outcome_summary(outcomes: dict[str, list[str]]) -> str:
    recovered = len(outcomes["1-NN 회수"])
    new_errors = len(outcomes["1-NN 새 오답"])
    net_correct = recovered - new_errors
    if net_correct > 0:
        net_text = f"정답 {net_correct}건 증가"
    elif net_correct < 0:
        net_text = f"정답 {abs(net_correct)}건 감소"
    else:
        net_text = "정답 수 변화 없음"
    return f"회수 {recovered}건 - 새 오답 {new_errors}건 = {net_text}"


def main() -> None:
    plt.rcParams["font.family"] = choose_font()
    plt.rcParams["axes.unicode_minus"] = False

    outcomes = collect_outcomes(read_rows())
    counts = [len(outcomes[outcome]) for outcome in OUTCOME_ORDER]
    sample_labels = [", ".join(outcomes[outcome]) or "없음" for outcome in OUTCOME_ORDER]
    max_count = max(counts)

    fig, ax = plt.subplots(figsize=(8.6, 4.8), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    bars = ax.bar(
        OUTCOME_ORDER,
        counts,
        color=[OUTCOME_COLORS[outcome] for outcome in OUTCOME_ORDER],
        width=0.62,
    )
    for bar, count, samples in zip(bars, counts, sample_labels):
        ax.annotate(
            str(count),
            (bar.get_x() + bar.get_width() / 2, count),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            fontsize=12,
            weight="bold",
            color="#172033",
        )
        ax.annotate(
            samples,
            (bar.get_x() + bar.get_width() / 2, 0),
            xytext=(0, -31),
            textcoords="offset points",
            ha="center",
            va="top",
            fontsize=9,
            color="#374151",
        )

    ax.text(
        1.5,
        max_count + 0.45,
        outcome_summary(outcomes),
        ha="center",
        fontsize=11,
        color="#172033",
        weight="bold",
    )
    ax.set_ylabel("평가 샘플 수")
    ax.set_ylim(0, max_count + 0.75)
    ax.set_yticks(range(max_count + 1))
    ax.grid(True, axis="y", color="#d1d5db", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="x", length=0)

    fig.tight_layout(pad=1.2)
    fig.savefig(OUTPUT_PATH, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
