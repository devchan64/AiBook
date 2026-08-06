from __future__ import annotations

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
import numpy as np
from matplotlib import font_manager
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


OUT_DIR = Path(__file__).resolve().parent
DATA_PATH = OUT_DIR / "p7-3-surface-patches.csv"
PNG_PATH = OUT_DIR / "p7-3-input-representation-report-ko.png"
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


def configure_font() -> None:
    plt.rcParams["font.family"] = choose_font()
    plt.rcParams["axes.unicode_minus"] = False


def load_rows() -> tuple[list[dict[str, str]], list[dict[str, str]], list[str]]:
    rows = list(csv.DictReader(DATA_PATH.open(encoding="utf-8")))
    pixel_columns = [name for name in rows[0] if name.startswith("pixel_")]
    train_rows = [row for row in rows if row["split"] == "train"]
    test_rows = [row for row in rows if row["split"] == "test"]
    return train_rows, test_rows, pixel_columns


def pixel_matrix(rows: list[dict[str, str]], pixel_columns: list[str]) -> np.ndarray:
    return np.array(
        [[float(row[column]) for column in pixel_columns] for row in rows],
        dtype=float,
    )


def column_profile(matrix: np.ndarray) -> np.ndarray:
    images = matrix.reshape(len(matrix), 8, 8)
    return images.mean(axis=1)


def center_band_profile(matrix: np.ndarray) -> np.ndarray:
    images = matrix.reshape(len(matrix), 8, 8)
    center = images[:, :, 3:5].mean(axis=(1, 2))
    left = images[:, :, :3].mean(axis=(1, 2))
    right = images[:, :, 5:].mean(axis=(1, 2))
    return np.column_stack([center, left, right])


def run_experiments() -> tuple[list[dict[str, object]], list[str]]:
    train_rows, test_rows, pixel_columns = load_rows()
    raw_train = pixel_matrix(train_rows, pixel_columns)
    raw_test = pixel_matrix(test_rows, pixel_columns)
    y_train = np.array([int(row["label"]) for row in train_rows])
    y_test = np.array([int(row["label"]) for row in test_rows])
    sample_names = [row["sample"].replace("평가-", "") for row in test_rows]

    representations = {
        "64픽셀": (raw_train, raw_test),
        "열 평균": (column_profile(raw_train), column_profile(raw_test)),
        "중심 band": (center_band_profile(raw_train), center_band_profile(raw_test)),
    }

    results: list[dict[str, object]] = []
    for name, (x_train, x_test) in representations.items():
        model = LogisticRegression(max_iter=1000, random_state=7)
        model.fit(x_train, y_train)
        predictions = model.predict(x_test)
        probabilities = model.predict_proba(x_test)
        margins = np.abs(probabilities[:, 1] - probabilities[:, 0])
        results.append(
            {
                "name": name,
                "accuracy": float(accuracy_score(y_test, predictions)),
                "error_count": int((predictions != y_test).sum()),
                "low_margin_count": int((margins < 0.25).sum()),
                "margins": margins,
            }
        )

    return results, sample_names


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def draw_report() -> None:
    configure_font()
    results, sample_names = run_experiments()
    names = [str(result["name"]) for result in results]

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.4), dpi=180)
    fig.patch.set_facecolor("white")
    left, right = axes

    x_positions = np.arange(len(names))
    width = 0.32
    errors = [int(result["error_count"]) for result in results]
    low_margin = [int(result["low_margin_count"]) for result in results]

    style_axis(left)
    left.bar(x_positions - width / 2, errors, width, label="오류 수", color="#dc2626")
    left.bar(x_positions + width / 2, low_margin, width, label="낮은 확신 수", color="#0f766e")
    left.set_xticks(x_positions, names)
    left.set_ylim(0, 4.6)
    left.set_ylabel("평가 샘플 수")
    left.set_title("오류와 낮은 확신 샘플 수")
    left.legend(frameon=False, fontsize=8.5, loc="upper left")

    style_axis(right)
    sample_positions = np.arange(len(sample_names))
    colors = ["#2563eb", "#ea580c", "#0f766e"]
    for result, color in zip(results, colors):
        right.plot(
            sample_positions,
            result["margins"],
            marker="o",
            linewidth=2.0,
            label=str(result["name"]),
            color=color,
        )
    right.axhline(0.25, color="#64748b", linestyle="--", linewidth=1.3, label="낮은 확신 기준")
    right.set_xticks(sample_positions, sample_names, rotation=15, ha="right")
    right.set_ylim(0, 0.7)
    right.set_ylabel("확신 차이")
    right.set_title("평가 샘플별 margin")
    right.legend(frameon=False, fontsize=8.3, loc="upper right")

    fig.suptitle(
        "입력 표현별 이미지 분류 리포트\n세 표현의 평가 정확도는 모두 0.75",
        fontsize=15,
        fontweight="bold",
    )
    fig.tight_layout(pad=1.0, rect=(0, 0, 1, 0.91))
    fig.savefig(PNG_PATH, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    draw_report()
    print(f"saved={PNG_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
