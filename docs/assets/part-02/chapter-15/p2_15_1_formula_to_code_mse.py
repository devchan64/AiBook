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


def calculate_with_loop(actual: list[float], predicted: list[float]) -> float:
    squared_errors = []
    for y, y_hat in zip(actual, predicted):
        error = y - y_hat
        squared_errors.append(error**2)
    return sum(squared_errors) / len(squared_errors)


def calculate_with_numpy(actual: np.ndarray, predicted: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    errors = actual - predicted
    squared_errors = errors**2
    mse = float(np.mean(squared_errors))
    return errors, squared_errors, mse


def save_actual_predicted_plot(actual: np.ndarray, predicted: np.ndarray) -> None:
    index = np.arange(len(actual))

    fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=160)
    ax.plot(index, actual, marker="o", color="#2563eb", label="actual")
    ax.plot(index, predicted, marker="o", color="#dc2626", label="predicted")
    ax.vlines(index, predicted, actual, color="#64748b", linewidth=1.4, alpha=0.7)
    ax.set_xlabel("sample index")
    ax.set_ylabel("value")
    ax.set_title("Actual and predicted values")
    ax.grid(True, alpha=0.24)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "actual-predicted-mse.png")
    plt.close(fig)


def main() -> None:
    actual_list = [3.0, 5.0, 7.0]
    predicted_list = [2.5, 5.5, 8.0]

    loop_mse = calculate_with_loop(actual_list, predicted_list)
    print("loop mse:", loop_mse)

    actual = np.array(actual_list)
    predicted = np.array(predicted_list)
    errors, squared_errors, numpy_mse = calculate_with_numpy(actual, predicted)

    print("errors:", errors)
    print("squared errors:", squared_errors)
    print("numpy mse:", numpy_mse)

    save_actual_predicted_plot(actual, predicted)
    print("saved: actual-predicted-mse.png")


if __name__ == "__main__":
    main()
