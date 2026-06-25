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


def save_function_shape() -> None:
    x = np.linspace(-3, 3, 121)
    y = x**2

    fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=160)
    ax.plot(x, y, color="#2563eb", linewidth=2.4)
    ax.axhline(0, color="#64748b", linewidth=1.0)
    ax.axvline(0, color="#64748b", linewidth=1.0)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Function shape: y = x^2")
    ax.grid(True, alpha=0.28)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "basic-line-function-shape.png")
    plt.close(fig)


def save_relationship_scatter() -> None:
    rng = np.random.default_rng(42)
    x = np.linspace(1, 10, 24)
    y = 2.5 * x + rng.normal(0, 2.2, size=x.shape)

    fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=160)
    ax.scatter(x, y, s=55, color="#0f766e")
    ax.set_xlabel("input value")
    ax.set_ylabel("observed value")
    ax.set_title("Scatter plot: relationship with variation")
    ax.grid(True, alpha=0.28)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "basic-scatter-relationship.png")
    plt.close(fig)


def save_distribution_histogram() -> None:
    rng = np.random.default_rng(7)
    values = rng.normal(loc=0, scale=1, size=240)

    fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=160)
    ax.hist(values, bins=18, color="#64748b", edgecolor="#1f2937")
    ax.set_xlabel("value")
    ax.set_ylabel("count")
    ax.set_title("Histogram: where values gather")
    ax.grid(True, axis="y", alpha=0.28)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "basic-hist-distribution.png")
    plt.close(fig)


def save_loss_curves() -> None:
    epochs = np.arange(1, 11)
    decreasing_loss = [2.4, 1.8, 1.35, 1.08, 0.91, 0.79, 0.70, 0.64, 0.60, 0.57]
    unstable_loss = [2.4, 1.9, 1.75, 1.82, 1.55, 1.62, 1.45, 1.52, 1.40, 1.46]

    fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=160)
    ax.plot(epochs, decreasing_loss, marker="o", color="#2563eb", label="steady decrease")
    ax.plot(epochs, unstable_loss, marker="o", color="#dc2626", label="unstable")
    ax.set_xlabel("epoch")
    ax.set_ylabel("loss")
    ax.set_title("Loss curves can reveal training behavior")
    ax.grid(True, alpha=0.28)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "basic-loss-curve-comparison.png")
    plt.close(fig)


if __name__ == "__main__":
    save_function_shape()
    save_relationship_scatter()
    save_distribution_histogram()
    save_loss_curves()
