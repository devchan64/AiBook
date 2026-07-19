from csv import DictReader
from pathlib import Path
import os
from typing import Union

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
RISK_WEIGHT_BEFORE = 1.0
LEARNING_RATE = 0.03


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


RowValue = Union[float, str]


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


def batch_step_values() -> tuple[list[float], list[float], list[float]]:
    rows = load_rows()
    gradient = mean_gradient(rows, RISK_WEIGHT_BEFORE)
    optimizer_delta = -LEARNING_RATE * gradient
    risk_weight_after = RISK_WEIGHT_BEFORE + optimizer_delta
    mean_score_before = sum(predict(row, RISK_WEIGHT_BEFORE) for row in rows) / len(rows)
    mean_score_after = sum(predict(row, risk_weight_after) for row in rows) / len(rows)
    return (
        [RISK_WEIGHT_BEFORE, risk_weight_after],
        [mean_score_before, mean_score_after],
        [mean_loss(rows, RISK_WEIGHT_BEFORE), mean_loss(rows, risk_weight_after)],
    )


def style_axis(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, axis="y", linestyle="--", linewidth=0.8, alpha=0.35)
    ax.set_axisbelow(True)


def save_before_after(values: list[float], ylabel: str, title: str, filename: str, ylim: tuple[float, float]) -> None:
    plt.rcParams["font.family"] = choose_font()
    plt.rcParams["axes.unicode_minus"] = False
    fig, ax = plt.subplots(figsize=(6.8, 3.7), constrained_layout=True)
    bars = ax.bar([0, 1], values, color=["#94a3b8", "#0f766e"], width=0.5)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["optimizer step 전", "optimizer step 후"])
    ax.set_ylabel(ylabel)
    ax.set_ylim(*ylim)
    ax.set_title(title, fontsize=11.2)
    style_axis(ax)
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
    weights, scores, losses = batch_step_values()
    save_before_after(
        weights,
        "risk_weight",
        "CSV batch update 전후 위험 가중치",
        "optimizer-step-batch-before-after-weight-ko.png",
        (0, 1.9),
    )
    save_before_after(
        scores,
        "평균 predicted_block_score",
        "CSV batch update 전후 평균 차단 점수",
        "optimizer-step-batch-before-after-score-ko.png",
        (0, 6.4),
    )
    save_before_after(
        losses,
        "평균 loss",
        "CSV batch update 전후 평균 손실",
        "optimizer-step-batch-before-after-loss-ko.png",
        (0, 8.1),
    )


if __name__ == "__main__":
    main()
