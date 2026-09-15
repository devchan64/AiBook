"""Recreate the manuscript charts from the repository root.

Use --language to render one language and --output-dir for temporary previews.
Matplotlib and NumPy are required. Localized SVG export requires a CJK font
such as Noto Sans CJK JP; --font-family can select another installed font.
"""
from pathlib import Path
import argparse
import os

REPO_ROOT = Path(__file__).resolve().parents[4]
MPL_CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.text import Text
import numpy as np

OUT_DIR = Path(__file__).resolve().parent
LANGUAGES = ("ko", "en", "zh")
FONT_FAMILY = "Noto Sans CJK JP"

LABELS = {'epoch': ('에폭', '轮次'), 'loss': ('손실', '损失'), 'validation loss': ('검증 손실', '验证损失'), 'Loss over epochs': ('에폭별 손실', '各轮次损失'), 'Accuracy over epochs': ('에폭별 정확도', '各轮次准确率'), 'accuracy': ('정확도', '准确率'), 'train loss': ('학습 손실', '训练损失'), 'minimum validation loss at epoch 8': ('8번째 에폭의 검증 손실 최솟값', '第 8 轮验证损失最低'), 'Training and validation loss can diverge': ('학습·검증 손실의 차이', '训练损失与验证损失的差异')}

def save_figure(fig, stem):
    # Keep one data/geometry source; translate visible labels for each export.
    fig.canvas.draw()
    originals = [(text, text.get_text()) for text in fig.findobj(Text)]
    for language in LANGUAGES:
        for text, original in originals:
            translated = LABELS.get(original)
            text.set_text(original if language == "en" or translated is None
                          else translated[0 if language == "ko" else 1])
            text.set_fontfamily(FONT_FAMILY)
        fig.tight_layout()
        path = OUT_DIR / f"{stem}-{language}.svg"
        fig.savefig(path, metadata={"Date": None})
        path.write_text("\n".join(line.rstrip() for line in path.read_text().splitlines()) + "\n")
    plt.close(fig)


def save_subplot_loss_accuracy():
    epochs = np.arange(1, 13)
    loss = [2.02, 1.68, 1.42, 1.18, 1.03, 0.91, 0.82, 0.75, 0.70, 0.66, 0.63, 0.60]
    accuracy = [0.55, 0.61, 0.66, 0.70, 0.74, 0.78, 0.81, 0.83, 0.85, 0.86, 0.87, 0.88]

    fig, axes = plt.subplots(1, 2, figsize=(8, 3.8), sharex=True)

    axes[0].plot(epochs, loss, marker="o")
    axes[0].set_title("Loss over epochs")
    axes[0].set_xlabel("epoch")
    axes[0].set_ylabel("loss")

    axes[1].plot(epochs, accuracy, marker="o")
    axes[1].set_title("Accuracy over epochs")
    axes[1].set_xlabel("epoch")
    axes[1].set_ylabel("accuracy")
    axes[1].set_ylim(0, 1)

    fig.tight_layout()
    save_figure(fig, "subplot-loss-accuracy")

def save_train_validation_loss_diverge():
    epochs = np.arange(1, 16)
    train_loss = [1.82, 1.45, 1.19, 1.00, 0.86, 0.76, 0.68, 0.62, 0.57, 0.53, 0.49, 0.46, 0.43, 0.41, 0.39]
    validation_loss = [1.88, 1.53, 1.31, 1.14, 1.02, 0.94, 0.90, 0.88, 0.89, 0.92, 0.97, 1.03, 1.10, 1.17, 1.25]

    fig, ax = plt.subplots()
    ax.plot(epochs, train_loss, marker="o", label="train loss")
    ax.plot(epochs, validation_loss, marker="o", label="validation loss")
    ax.axvline(8, color="gray", linestyle="--")
    ax.text(8.25, 1.38, "minimum validation loss at epoch 8")
    ax.set_xlabel("epoch")
    ax.set_ylabel("loss")
    ax.set_title("Training and validation loss can diverge")
    ax.legend()
    save_figure(fig, "train-validation-loss-diverge")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", choices=["all", "ko", "en", "zh"], default="all")
    parser.add_argument("--output-dir", type=Path, default=OUT_DIR)
    parser.add_argument("--font-family", default=FONT_FAMILY)
    args = parser.parse_args()
    OUT_DIR = args.output_dir
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    LANGUAGES = ("ko", "en", "zh") if args.language == "all" else (args.language,)
    FONT_FAMILY = args.font_family
    plt.rcParams.update({"font.family": FONT_FAMILY, "font.size": 10,
                         "figure.figsize": (6.4, 4), "svg.hashsalt": "p2-13"})
    save_subplot_loss_accuracy()
    save_train_validation_loss_diverge()
