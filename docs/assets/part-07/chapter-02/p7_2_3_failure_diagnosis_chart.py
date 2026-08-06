"""P7-2.3의 설정별 정확도와 샘플 실패 진단 분포를 그린다."""

from collections import Counter
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
TRAIN_PATH = ASSET_DIR / "p7-2-churn-dataset.csv"
STRESS_PATH = ASSET_DIR / "p7-2-stress-test.csv"
OUTPUT_PATH = ASSET_DIR / "p7-2-3-failure-diagnosis-chart-ko.png"
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


def read_rows(path: Path) -> list[dict[str, object]]:
    with path.open(encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    for row in rows:
        for column in ("unresolved_tickets", "days_since_login", "usage_minutes_30d", "label"):
            row[column] = int(row[column])
    return rows


def to_matrix(rows: list[dict[str, object]]) -> np.ndarray:
    return np.array([
        [row["unresolved_tickets"], row["days_since_login"], row["usage_minutes_30d"]]
        for row in rows
    ], dtype=float)


def predict_1nn(train_x: np.ndarray, train_y: np.ndarray, test_x: np.ndarray) -> np.ndarray:
    predictions = []
    for point in test_x:
        predictions.append(int(train_y[int(np.argmin(np.linalg.norm(train_x - point, axis=1)))]))
    return np.array(predictions)


def collect_results() -> tuple[dict[str, float], Counter[str]]:
    train_rows = [row for row in read_rows(TRAIN_PATH) if row["split"] == "train"]
    stress_rows = read_rows(STRESS_PATH)
    x_train = to_matrix(train_rows)
    x_test = to_matrix(stress_rows)
    y_train = np.array([row["label"] for row in train_rows])
    y_test = np.array([row["label"] for row in stress_rows])

    baseline = np.full(len(y_test), int(np.bincount(y_train).argmax()), dtype=int)
    raw = predict_1nn(x_train, y_train, x_test)
    scaled_train, scaled_test = x_train.copy(), x_test.copy()
    scaled_train[:, 2] /= 60.0
    scaled_test[:, 2] /= 60.0
    scaled = predict_1nn(scaled_train, y_train, scaled_test)
    mean, std = x_train.mean(axis=0), x_train.std(axis=0)
    zscore = predict_1nn((x_train - mean) / std, y_train, (x_test - mean) / std)

    diagnoses = Counter()
    for raw_value, scaled_value, z_value, label in zip(raw, scaled, zscore, y_test):
        if raw_value != label and z_value == label:
            diagnoses["전처리로 해결됨"] += 1
        elif z_value != label:
            diagnoses["정규화 후에도 남음"] += 1
        elif len({int(raw_value), int(scaled_value), int(z_value)}) > 1:
            diagnoses["설정에 따라 갈림"] += 1
        else:
            diagnoses["현재는 안정적"] += 1

    accuracy = {
        "baseline": float((baseline == y_test).mean()),
        "raw 1-NN": float((raw == y_test).mean()),
        "부분 스케일": float((scaled == y_test).mean()),
        "z-score": float((zscore == y_test).mean()),
    }
    return accuracy, diagnoses


def main() -> None:
    plt.rcParams["font.family"] = choose_font()
    plt.rcParams["axes.unicode_minus"] = False
    accuracy, diagnoses = collect_results()
    fig, (accuracy_ax, diagnosis_ax) = plt.subplots(1, 2, figsize=(11.0, 4.9), dpi=180)
    fig.patch.set_facecolor("white")

    accuracy_labels = list(accuracy)
    accuracy_values = [accuracy[label] for label in accuracy_labels]
    accuracy_bars = accuracy_ax.bar(accuracy_labels, accuracy_values, color=["#64748b", "#2563eb", "#d97706", "#15803d"], width=0.62)
    for bar, value in zip(accuracy_bars, accuracy_values):
        accuracy_ax.text(bar.get_x() + bar.get_width() / 2, value + 0.025, f"{value:.3f}", ha="center", fontsize=10, weight="bold")
    accuracy_ax.set_title("설정별 스트레스 평가 정확도", fontsize=14, pad=12)
    accuracy_ax.set_ylabel("정확도")
    accuracy_ax.set_ylim(0, 1.05)
    accuracy_ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])

    diagnosis_order = ["전처리로 해결됨", "정규화 후에도 남음", "설정에 따라 갈림", "현재는 안정적"]
    diagnosis_values = [diagnoses[label] for label in diagnosis_order]
    diagnosis_bars = diagnosis_ax.bar(diagnosis_order, diagnosis_values, color=["#15803d", "#d97706", "#dc2626", "#64748b"], width=0.62)
    for bar, value in zip(diagnosis_bars, diagnosis_values):
        diagnosis_ax.text(bar.get_x() + bar.get_width() / 2, value + 0.45, str(value), ha="center", fontsize=11, weight="bold")
    diagnosis_ax.set_title("z-score 기준 샘플 실패 진단", fontsize=14, pad=12)
    diagnosis_ax.set_ylabel("스트레스 평가 샘플 수")
    diagnosis_ax.set_ylim(0, max(diagnosis_values) + 3)
    diagnosis_ax.set_yticks(range(0, max(diagnosis_values) + 1, 5))

    for ax in (accuracy_ax, diagnosis_ax):
        ax.set_facecolor("white")
        ax.grid(True, axis="y", color="#d1d5db", linewidth=0.75, alpha=0.85)
        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(axis="x", labelrotation=0)
    fig.tight_layout(pad=1.3)
    fig.savefig(OUTPUT_PATH, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
