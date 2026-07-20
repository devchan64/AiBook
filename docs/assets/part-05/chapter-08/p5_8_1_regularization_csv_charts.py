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

LANGUAGE_CONFIGS = {
    "ko": {
        "font_candidates": [
            "Noto Sans CJK KR",
            "NanumGothic",
            "Apple SD Gothic Neo",
            "AppleGothic",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "model_labels": {
            "without_regularization": "정규화 없음",
            "with_l2_regularization": "L2 정규화",
        },
        "loss_title": "정규화 유무에 따른 훈련 손실과 검증 손실",
        "weight_title": "정규화 유무에 따른 가중치 크기 증가",
        "train_loss": "훈련 손실",
        "validation_loss": "검증 손실",
        "weight_size": "weight size",
    },
    "en": {
        "font_candidates": [
            "DejaVu Sans",
            "Arial",
            "Arial Unicode MS",
        ],
        "model_labels": {
            "without_regularization": "without regularization",
            "with_l2_regularization": "L2 regularization",
        },
        "loss_title": "Training And Validation Loss With And Without Regularization",
        "weight_title": "Weight Size Growth With And Without Regularization",
        "train_loss": "training loss",
        "validation_loss": "validation loss",
        "weight_size": "weight size",
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Source Han Sans SC",
            "PingFang SC",
            "Songti SC",
            "Hiragino Sans GB",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "model_labels": {
            "without_regularization": "无正则化",
            "with_l2_regularization": "L2 正则化",
        },
        "loss_title": "有无正则化时的训练损失与验证损失",
        "weight_title": "有无正则化时的权重大小增长",
        "train_loss": "训练损失",
        "validation_loss": "验证损失",
        "weight_size": "权重大小",
    },
}
MODEL_COLORS = {
    "without_regularization": "#dc2626",
    "with_l2_regularization": "#2563eb",
}
MODELS = ["without_regularization", "with_l2_regularization"]


def choose_font(candidates) -> str:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def configure_font(config: dict) -> None:
    plt.rcParams["font.family"] = choose_font(config["font_candidates"])
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


def save_loss_chart(rows, lang: str, config: dict) -> None:
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
        label = config["model_labels"][model]
        best_validation = min(model_rows, key=lambda row: float(row["validation_loss"]))

        ax.plot(
            epochs,
            train_loss,
            color=color,
            linewidth=2.2,
            alpha=0.55,
            linestyle="--",
            label=f"{label} {config['train_loss']}",
        )
        ax.plot(epochs, validation_loss, color=color, linewidth=2.6, label=f"{label} {config['validation_loss']}")
        ax.scatter(
            [int(best_validation["epoch"])],
            [float(best_validation["validation_loss"])],
            color=color,
            s=32,
            zorder=4,
        )

    ax.set_title(config["loss_title"])
    ax.set_xlabel("epoch")
    ax.set_ylabel("loss")
    ax.set_xlim(1, 18)
    ax.legend(frameon=False, fontsize=8.2, ncol=2)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / f"regularization-loss-compare-{lang}.png", bbox_inches="tight")
    plt.close(fig)


def save_weight_chart(rows, lang: str, config: dict) -> None:
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
            label=config["model_labels"][model],
        )

    ax.set_title(config["weight_title"])
    ax.set_xlabel("epoch")
    ax.set_ylabel(config["weight_size"])
    ax.set_xlim(1, 18)
    ax.legend(frameon=False, fontsize=8.8)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / f"regularization-weight-growth-{lang}.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    rows = load_rows()
    for lang, config in LANGUAGE_CONFIGS.items():
        configure_font(config)
        save_loss_chart(rows, lang, config)
        save_weight_chart(rows, lang, config)


if __name__ == "__main__":
    main()
