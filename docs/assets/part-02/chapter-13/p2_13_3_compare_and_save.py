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
import numpy as np


OUT_DIR = Path(__file__).resolve().parent


def save_subplot_comparison() -> None:
    epochs = np.arange(1, 13)
    loss = [2.02, 1.68, 1.42, 1.18, 1.03, 0.91, 0.82, 0.75, 0.70, 0.66, 0.63, 0.60]
    accuracy = [0.55, 0.61, 0.66, 0.70, 0.74, 0.78, 0.81, 0.83, 0.85, 0.86, 0.87, 0.88]

    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.8), dpi=160)

    axes[0].plot(epochs, loss, marker="o", color="#2563eb")
    axes[0].set_title("Loss over epochs")
    axes[0].set_xlabel("epoch")
    axes[0].set_ylabel("loss")
    axes[0].grid(True, alpha=0.28)

    axes[1].plot(epochs, accuracy, marker="o", color="#0f766e")
    axes[1].set_title("Accuracy over epochs")
    axes[1].set_xlabel("epoch")
    axes[1].set_ylabel("accuracy")
    axes[1].set_ylim(0.45, 1.0)
    axes[1].grid(True, alpha=0.28)

    fig.suptitle("One figure can hold related views")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "subplot-loss-accuracy.png")
    plt.close(fig)


def save_train_validation_loss() -> None:
    epochs = np.arange(1, 16)
    train_loss = [1.82, 1.45, 1.19, 1.00, 0.86, 0.76, 0.68, 0.62, 0.57, 0.53, 0.49, 0.46, 0.43, 0.41, 0.39]
    validation_loss = [1.88, 1.53, 1.31, 1.14, 1.02, 0.94, 0.90, 0.88, 0.89, 0.92, 0.97, 1.03, 1.10, 1.17, 1.25]

    fig, ax = plt.subplots(figsize=(6.8, 4.0), dpi=160)
    ax.plot(epochs, train_loss, marker="o", color="#2563eb", label="train loss")
    ax.plot(epochs, validation_loss, marker="o", color="#dc2626", label="validation loss")
    ax.axvline(8, color="#64748b", linestyle="--", linewidth=1.2)
    ax.text(8.25, 1.38, "validation starts rising", color="#475569", fontsize=10)
    ax.set_title("Training and validation loss can diverge")
    ax.set_xlabel("epoch")
    ax.set_ylabel("loss")
    ax.grid(True, alpha=0.28)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "train-validation-loss-diverge.png")
    plt.close(fig)


if __name__ == "__main__":
    save_subplot_comparison()
    save_train_validation_loss()
