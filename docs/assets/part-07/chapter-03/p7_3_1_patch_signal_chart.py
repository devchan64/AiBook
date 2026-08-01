"""P7-3.1 평가 패치의 중앙 결함 신호와 스크래치 확률을 그린다."""

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
DATA_PATH = ASSET_DIR / "p7-3-surface-patches.csv"
OUTPUT_PATH = ASSET_DIR / "p7-3-1-patch-signal-chart-ko.png"
KOREAN_FONT_PATH = Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")


def choose_font() -> str:
    system_fonts = [Path(path) for path in font_manager.findSystemFonts()]
    candidates = [KOREAN_FONT_PATH] + [
        path for path in system_fonts if "NotoSansCJK" in path.name or "Nanum" in path.name
    ]
    for path in candidates:
        if path.exists():
            font_manager.fontManager.addfont(str(path))
            return font_manager.FontProperties(fname=str(path)).get_name()
    raise RuntimeError("한글 차트에는 Noto Sans CJK 또는 Nanum 계열 폰트가 필요합니다.")


def softmax(values: np.ndarray) -> np.ndarray:
    values = values - values.max(axis=1, keepdims=True)
    exponentials = np.exp(values)
    return exponentials / exponentials.sum(axis=1, keepdims=True)


def read_rows() -> list[dict[str, object]]:
    pixel_columns = [f"pixel_{row}{column}" for row in range(8) for column in range(8)]
    rows = []
    with DATA_PATH.open(encoding="utf-8") as source:
        for raw_row in csv.DictReader(source):
            rows.append(
                {
                    "split": raw_row["split"],
                    "sample": raw_row["sample"],
                    "label": int(raw_row["label"]),
                    "image": np.array([float(raw_row[column]) for column in pixel_columns]).reshape(8, 8),
                }
            )
    return rows


def collect_results() -> list[dict[str, object]]:
    rows = read_rows()
    train_rows = [row for row in rows if row["split"] == "train"]
    test_rows = [row for row in rows if row["split"] == "test"]
    x_train = np.array([row["image"].reshape(-1) for row in train_rows])
    y_train = np.array([row["label"] for row in train_rows])
    x_test = np.array([row["image"].reshape(-1) for row in test_rows])

    weights = np.zeros((64, 2))
    bias = np.zeros(2)
    targets = np.zeros((len(y_train), 2))
    targets[np.arange(len(y_train)), y_train] = 1
    for _ in range(700):
        probabilities = softmax(x_train @ weights + bias)
        weights -= 0.35 * (x_train.T @ (probabilities - targets) / len(x_train))
        bias -= 0.35 * (probabilities - targets).mean(axis=0)

    probabilities = softmax(x_test @ weights + bias)
    results = []
    for row, probability in zip(test_rows, probabilities):
        image = row["image"]
        center_band = float(image[:, 3:5].mean())
        outside_band = float(np.concatenate((image[:, :3], image[:, 5:]), axis=1).mean())
        prediction = int(probability.argmax())
        results.append(
            {
                "sample": row["sample"].replace("평가-", ""),
                "center_band": center_band,
                "outside_band": outside_band,
                "signal_gap": center_band - outside_band,
                "scratch_probability": float(probability[1]),
                "result": "정답" if prediction == row["label"] else "오답",
            }
        )
    return results


def style_axis(axis: plt.Axes) -> None:
    axis.grid(True, axis="y", color="#d1d5db", linewidth=0.75, alpha=0.85)
    axis.set_axisbelow(True)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)


def main() -> None:
    plt.rcParams["font.family"] = choose_font()
    plt.rcParams["axes.unicode_minus"] = False
    results = collect_results()
    labels = [result["sample"] for result in results]
    positions = np.arange(len(labels))
    fig, (signal_ax, probability_ax) = plt.subplots(1, 2, figsize=(11.0, 4.9), dpi=180)
    fig.patch.set_facecolor("white")

    width = 0.34
    center = [result["center_band"] for result in results]
    outside = [result["outside_band"] for result in results]
    signal_ax.bar(positions - width / 2, center, width, label="중앙 2열 평균", color="#c2410c")
    signal_ax.bar(positions + width / 2, outside, width, label="주변 6열 평균", color="#64748b")
    for position, center_value, outside_value, result in zip(positions, center, outside, results):
        signal_ax.text(
            position,
            max(center_value, outside_value) + 0.035,
            f"Δ {result['signal_gap']:+.3f}",
            ha="center",
            fontsize=9.5,
            weight="bold",
            color="#b45309" if result["result"] == "오답" else "#374151",
        )
    signal_ax.set_title("입력 위치별 평균 밝기 (중앙−주변)", fontsize=14, pad=12)
    signal_ax.set_ylabel("grayscale 값")
    signal_ax.set_ylim(0, 0.85)
    signal_ax.set_xticks(positions, labels, rotation=12, ha="right")
    signal_ax.legend(frameon=False, loc="upper left")
    style_axis(signal_ax)

    probabilities = [result["scratch_probability"] for result in results]
    colors = ["#15803d" if result["result"] == "정답" else "#dc2626" for result in results]
    bars = probability_ax.bar(positions, probabilities, color=colors, width=0.62)
    probability_ax.axhline(0.5, color="#6b7280", linestyle="--", linewidth=1.2)
    probability_ax.text(3.35, 0.53, "예측 경계 0.5", ha="right", fontsize=9, color="#4b5563")
    for bar, result in zip(bars, results):
        probability_ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.035, f"{bar.get_height():.3f}", ha="center", fontsize=10, weight="bold")
    probability_ax.set_title("스크래치 경고 확률", fontsize=14, pad=12)
    probability_ax.set_ylabel("클래스 1 확률")
    probability_ax.set_ylim(0, 1.1)
    probability_ax.set_xticks(positions, labels, rotation=12, ha="right")
    probability_ax.legend(
        handles=[Patch(color="#15803d", label="정답"), Patch(color="#dc2626", label="오답")],
        frameon=False,
        loc="upper left",
    )
    style_axis(probability_ax)

    fig.tight_layout(pad=1.3)
    fig.savefig(OUTPUT_PATH, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
