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


OUT_DIR = Path(__file__).resolve().parent


def save_loss_plot() -> None:
    epochs = [1, 2, 3, 4, 5]
    loss = [2.40, 1.65, 1.12, 0.86, 0.79]

    fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=160)
    ax.plot(epochs, loss, marker="o", linewidth=2.4, color="#2563eb")
    ax.set_xlabel("epoch")
    ax.set_ylabel("loss")
    ax.set_title("Loss decreases over epochs")
    ax.grid(True, alpha=0.28)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "pyplot-loss-line.png")
    plt.close(fig)


def save_study_scatter() -> None:
    study_hours = [2, 4, 6, 8]
    scores = [62, 71, 82, 88]

    fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=160)
    ax.scatter(study_hours, scores, s=90, color="#0f766e")
    ax.set_xlabel("study hours")
    ax.set_ylabel("score")
    ax.set_title("Study hours and score")
    ax.grid(True, alpha=0.28)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "pyplot-study-scatter.png")
    plt.close(fig)


def save_score_hist() -> None:
    scores = [45, 62, 71, 73, 82, 88, 90]

    fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=160)
    ax.hist(scores, bins=5, color="#64748b", edgecolor="#1f2937")
    ax.set_xlabel("score")
    ax.set_ylabel("count")
    ax.set_title("Score distribution")
    ax.grid(True, axis="y", alpha=0.28)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "pyplot-score-hist.png")
    plt.close(fig)


if __name__ == "__main__":
    save_loss_plot()
    save_study_scatter()
    save_score_hist()
