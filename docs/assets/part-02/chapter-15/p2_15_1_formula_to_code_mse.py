"""Compare loop/array MSE and reproduce the localized sample-error charts."""
from pathlib import Path
from html import escape
import argparse
import os
import re

REPO_ROOT = Path(__file__).resolve().parents[4]
os.environ.setdefault("MPLCONFIGDIR", str(REPO_ROOT / ".tmp" / "matplotlib-cache"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path(__file__).resolve().parent
LABELS = {
    "ko": ("실제값", "예측값", "샘플 인덱스", "값", "실제값과 예측값"),
    "en": ("actual", "predicted", "sample index", "value", "Actual and predicted values"),
    "zh": ("实际值", "预测值", "样本索引", "值", "实际值与预测值"),
}


def calculate_with_loop(actual: list[float], predicted: list[float]) -> float:
    # Never let zip silently discard an unmatched sample.
    if len(actual) != len(predicted) or not actual:
        raise ValueError("Use equally sized, non-empty lists.")
    if not all(np.isfinite(value) for value in actual + predicted):
        raise ValueError("Use finite values.")
    squared_errors = []
    for y, y_hat in zip(actual, predicted):
        error = y - y_hat
        squared_errors.append(error ** 2)
    return sum(squared_errors) / len(squared_errors)


def calculate_with_numpy(actual: np.ndarray, predicted: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    # Require paired scalar targets, rather than accidental broadcasting.
    if actual.ndim != 1 or actual.shape != predicted.shape or actual.size == 0:
        raise ValueError("Use equally shaped, non-empty 1-D arrays.")
    if not (np.isfinite(actual).all() and np.isfinite(predicted).all()):
        raise ValueError("Use finite values.")
    errors = actual - predicted
    squared_errors = errors ** 2
    return errors, squared_errors, float(np.mean(squared_errors))


def save_actual_predicted_plot(actual, predicted, output_dir, language):
    actual_label, predicted_label, xlabel, ylabel, title = LABELS[language]
    index = np.arange(len(actual))
    # Use an independent figure for each language to keep layout reproducible.
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    ax.scatter(index, actual, marker="o", color="#2563eb", label=actual_label)
    ax.scatter(index, predicted, marker="x", color="#dc2626", label=predicted_label)
    ax.vlines(index, predicted, actual, color="#64748b", linewidth=1.4)
    ax.set_xticks(index)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    path = output_dir / f"actual-predicted-mse-{language}.svg"
    fig.savefig(path, metadata={"Date": None, "Title": title,
                                "Description": f"Paired values: {actual.tolist()} and {predicted.tolist()}"})
    description = f"{actual_label}: {actual.tolist()}; {predicted_label}: {predicted.tolist()}"
    svg = re.sub(r'(<svg\b[^>]*>)',
                 lambda match: match[1] + f"\n <title>{escape(title)}</title>\n <desc>{escape(description)}</desc>",
                 path.read_text(), count=1)
    path.write_text("\n".join(line.rstrip() for line in svg.splitlines()) + "\n")
    plt.close(fig)
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--last-prediction", type=float, default=8.0,
                        help="Change the final prediction to 7 or 9 and compare MSE.")
    parser.add_argument("--output-dir", type=Path, default=OUT_DIR)
    parser.add_argument("--language", choices=["all", *LABELS], default="all")
    parser.add_argument("--font-family", default="Noto Sans CJK JP")
    args = parser.parse_args()
    actual_list = [3.0, 5.0, 7.0]
    predicted_list = [2.5, 5.5, args.last_prediction]
    loop_mse = calculate_with_loop(actual_list, predicted_list)
    actual = np.array(actual_list)
    predicted = np.array(predicted_list)
    errors, squared_errors, numpy_mse = calculate_with_numpy(actual, predicted)
    print("loop mse:", loop_mse)
    print("errors:", errors)
    print("squared errors:", squared_errors)
    print("numpy mse:", numpy_mse)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with plt.rc_context({"font.family": args.font_family, "font.size": 10,
                         "svg.hashsalt": "p2-15-mse"}):
        languages = LABELS if args.language == "all" else [args.language]
        for language in languages:
            print("saved:", save_actual_predicted_plot(actual, predicted, args.output_dir, language))


if __name__ == "__main__":
    main()
