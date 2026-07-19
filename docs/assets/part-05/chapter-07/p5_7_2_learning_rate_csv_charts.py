from csv import DictReader
from pathlib import Path
import os
from typing import Optional, Union

REPO_ROOT = Path(__file__).resolve().parents[4]
MPL_CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))
os.environ.setdefault("XDG_CACHE_HOME", str(MPL_CACHE))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


OUT_DIR = Path(__file__).resolve().parent
DATA_PATH = OUT_DIR / "optimizer-step-role-log.csv"
RISK_WEIGHT = 1.0
LEARNING_RATES = [0.003, 0.03, 0.12]
RowValue = Union[float, str]


def choose_font() -> str:
    candidates = [
        "Noto Sans CJK KR",
        "NanumGothic",
        "Apple SD Gothic Neo",
        "AppleGothic",
        "Arial Unicode MS",
        "DejaVu Sans",
    ]
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def load_rows() -> list[dict[str, RowValue]]:
    with DATA_PATH.open(newline="", encoding="utf-8") as f:
        return [
            {
                "case_id": row["case_id"],
                "equipment_group": row["equipment_group"],
                "pressure_unrecovered": float(row["pressure_unrecovered"]),
                "target_block_score": float(row["target_block_score"]),
            }
            for row in DictReader(f)
        ]


def predict(row: dict[str, RowValue], risk_weight: float) -> float:
    return float(row["pressure_unrecovered"]) * risk_weight


def mean_loss(rows: list[dict[str, RowValue]], risk_weight: float) -> float:
    losses = [
        (predict(row, risk_weight) - float(row["target_block_score"])) ** 2
        for row in rows
    ]
    return sum(losses) / len(losses)


def mean_gradient(rows: list[dict[str, RowValue]], risk_weight: float) -> float:
    gradients = [
        2
        * (predict(row, risk_weight) - float(row["target_block_score"]))
        * float(row["pressure_unrecovered"])
        for row in rows
    ]
    return sum(gradients) / len(gradients)


def learning_rate_values() -> tuple[list[float], list[float], list[float], float]:
    rows = load_rows()
    gradient = mean_gradient(rows, RISK_WEIGHT)
    weights = []
    scores = []
    losses = []
    for learning_rate in LEARNING_RATES:
        optimizer_delta = -learning_rate * gradient
        updated_weight = RISK_WEIGHT + optimizer_delta
        mean_score = sum(predict(row, updated_weight) for row in rows) / len(rows)
        weights.append(updated_weight)
        scores.append(mean_score)
        losses.append(mean_loss(rows, updated_weight))
    mean_target = sum(float(row["target_block_score"]) for row in rows) / len(rows)
    return weights, scores, losses, mean_target


def style_axis(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, axis="y", linestyle="--", linewidth=0.8, alpha=0.35)
    ax.set_axisbelow(True)


def save_bar(values: list[float], ylabel: str, title: str, filename: str, ylim: tuple[float, float], target: Optional[float] = None) -> None:
    plt.rcParams["font.family"] = choose_font()
    plt.rcParams["axes.unicode_minus"] = False
    colors = ["#2563eb", "#0f766e", "#dc2626"]
    labels = [f"lr={learning_rate:g}" for learning_rate in LEARNING_RATES]

    fig, ax = plt.subplots(figsize=(7.2, 3.8), constrained_layout=True)
    bars = ax.bar(range(len(values)), values, color=colors, width=0.48)
    ax.set_xticks(range(len(values)))
    ax.set_xticklabels(labels)
    ax.set_xlabel("학습률")
    ax.set_ylabel(ylabel)
    ax.set_ylim(*ylim)
    ax.set_title(title, fontsize=11.2)
    style_axis(ax)

    if target is not None:
        ax.axhline(target, color="#0f766e", linewidth=1.4, linestyle=(0, (5, 4)), label=f"평균 목표={target:.2f}")
        ax.legend(frameon=False, loc="upper left")

    for bar, value in zip(bars, values):
        offset = (ylim[1] - ylim[0]) * 0.03
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + offset,
            f"{value:.3g}",
            ha="center",
            fontsize=10,
        )
    fig.savefig(OUT_DIR / filename, dpi=160)
    plt.close(fig)


def main() -> None:
    weights, scores, losses, mean_target = learning_rate_values()
    save_bar(
        weights,
        "업데이트 후 risk_weight",
        "learning rate별 업데이트 후 위험 가중치",
        "learning-rate-batch-updated-weight-ko.png",
        (0, 3.9),
    )
    save_bar(
        scores,
        "업데이트 후 평균 predicted_block_score",
        "learning rate별 업데이트 후 평균 차단 점수",
        "learning-rate-batch-updated-score-ko.png",
        (0, 13.4),
        target=mean_target,
    )
    save_bar(
        losses,
        "업데이트 후 평균 loss",
        "learning rate별 업데이트 후 평균 손실",
        "learning-rate-batch-updated-loss-ko.png",
        (0, 53),
    )


if __name__ == "__main__":
    main()
