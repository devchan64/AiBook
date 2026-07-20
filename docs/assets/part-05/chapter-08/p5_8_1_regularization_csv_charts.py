from csv import DictReader
from pathlib import Path
import os

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
CSV_PATH = OUT_DIR / "regularization-training-log.csv"

MODEL_LABELS = {
    "without_regularization": "정규화 없음",
    "with_l2_regularization": "L2 정규화",
}
MODEL_COLORS = {
    "without_regularization": "#dc2626",
    "with_l2_regularization": "#2563eb",
}
MODELS = ["without_regularization", "with_l2_regularization"]


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


def configure_font() -> None:
    plt.rcParams["font.family"] = choose_font()
    plt.rcParams["axes.unicode_minus"] = False


def load_rows():
    rows = []
    with CSV_PATH.open(encoding="utf-8") as file:
        for row in DictReader(file):
            rows.append(
                {
                    "model": row["model"],
                    "epoch": int(row["epoch"]),
                    "train_loss": float(row["train_loss"]),
                    "validation_loss": float(row["validation_loss"]),
                    "weight_size": float(row["weight_size"]),
                    "regularization_strength": float(row["regularization_strength"]),
                }
            )
    return rows


def rows_for_model(rows, model: str):
    return [row for row in rows if row["model"] == model]


def save_loss_chart(rows) -> None:
    fig, ax = plt.subplots(figsize=(7.0, 4.2), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.8)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for model in MODELS:
        model_rows = rows_for_model(rows, model)
        epochs = [int(row["epoch"]) for row in model_rows]
        train_loss = [float(row["train_loss"]) for row in model_rows]
        validation_loss = [float(row["validation_loss"]) for row in model_rows]
        color = MODEL_COLORS[model]
        label = MODEL_LABELS[model]
        best_validation = min(model_rows, key=lambda row: float(row["validation_loss"]))

        ax.plot(epochs, train_loss, color=color, linewidth=2.2, alpha=0.55, linestyle="--", label=f"{label} 훈련 손실")
        ax.plot(epochs, validation_loss, color=color, linewidth=2.6, label=f"{label} 검증 손실")
        ax.scatter(
            [int(best_validation["epoch"])],
            [float(best_validation["validation_loss"])],
            color=color,
            s=32,
            zorder=4,
        )

    ax.set_title("정규화 유무에 따른 훈련 손실과 검증 손실")
    ax.set_xlabel("epoch")
    ax.set_ylabel("loss")
    ax.set_xlim(1, 18)
    ax.legend(frameon=False, fontsize=8.2, ncol=2)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / "regularization-loss-compare-ko.png", bbox_inches="tight")
    plt.close(fig)


def save_weight_chart(rows) -> None:
    fig, ax = plt.subplots(figsize=(6.2, 3.8), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.8)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for model in MODELS:
        model_rows = rows_for_model(rows, model)
        epochs = [int(row["epoch"]) for row in model_rows]
        weight_size = [float(row["weight_size"]) for row in model_rows]
        ax.plot(
            epochs,
            weight_size,
            color=MODEL_COLORS[model],
            linewidth=2.6,
            marker="o",
            markersize=3.2,
            label=MODEL_LABELS[model],
        )

    ax.set_title("정규화 유무에 따른 가중치 크기 증가")
    ax.set_xlabel("epoch")
    ax.set_ylabel("weight size")
    ax.set_xlim(1, 18)
    ax.legend(frameon=False, fontsize=8.8)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / "regularization-weight-growth-ko.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    configure_font()
    rows = load_rows()
    save_loss_chart(rows)
    save_weight_chart(rows)


if __name__ == "__main__":
    main()
