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

INPUTS = [
    [1.0, 2.0],
    [2.0, 1.0],
    [0.5, 3.0],
]
WEIGHT_CASES = {
    "small_init": [0.2, -0.1],
    "medium_init": [1.0, -0.7],
    "large_init": [3.0, -2.0],
}

LANG_TEXT = {
    "ko": {
        "font_candidates": ["Noto Sans CJK KR", "NanumGothic", "Apple SD Gothic Neo", "AppleGothic", "Arial Unicode MS", "DejaVu Sans"],
        "raw_outfile": "initialization-raw-output-scale-ko.png",
        "variance_outfile": "initialization-raw-variance-ko.png",
        "normalized_outfile": "batchnorm-normalized-output-scale-ko.png",
        "sample_label": "입력 샘플",
        "case_label": "초기화 케이스",
        "raw_ylabel": "선형 출력",
        "variance_ylabel": "raw variance",
        "normalized_ylabel": "batch normalization 뒤 출력",
        "sample_prefix": "샘플",
        "small_init": "small init",
        "medium_init": "medium init",
        "large_init": "large init",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "raw_outfile": "initialization-raw-output-scale-en.png",
        "variance_outfile": "initialization-raw-variance-en.png",
        "normalized_outfile": "batchnorm-normalized-output-scale-en.png",
        "sample_label": "input sample",
        "case_label": "initialization case",
        "raw_ylabel": "linear output",
        "variance_ylabel": "raw variance",
        "normalized_ylabel": "output after batch normalization",
        "sample_prefix": "sample",
        "small_init": "small init",
        "medium_init": "medium init",
        "large_init": "large init",
    },
}


def choose_font(candidates: list[str]) -> str:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def configure_font(text: dict[str, str]) -> None:
    plt.rcParams["font.family"] = choose_font(text["font_candidates"])
    plt.rcParams["axes.unicode_minus"] = False


def linear(batch: list[list[float]], weights: list[float]) -> list[float]:
    return [x1 * weights[0] + x2 * weights[1] for x1, x2 in batch]


def batch_norm(values: list[float], eps: float = 1e-5) -> tuple[float, float, list[float]]:
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    normalized = [(value - mean) / ((variance + eps) ** 0.5) for value in values]
    return mean, variance, normalized


def build_trace() -> dict:
    traces = {}
    for case_name, weights in WEIGHT_CASES.items():
        raw_outputs = linear(INPUTS, weights)
        raw_mean, raw_variance, normalized_outputs = batch_norm(raw_outputs)
        traces[case_name] = {
            "raw_outputs": [round(value, 3) for value in raw_outputs],
            "raw_mean": round(raw_mean, 3),
            "raw_variance": round(raw_variance, 3),
            "normalized_outputs": [round(value, 3) for value in normalized_outputs],
        }
    return traces


def style_axis(ax) -> None:
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_raw_output_chart(text: dict[str, str], trace: dict) -> None:
    configure_font(text)
    sample_positions = list(range(len(INPUTS)))
    width = 0.24
    colors = ["#2563eb", "#f59e0b", "#dc2626"]
    fig, ax = plt.subplots(figsize=(6.8, 3.8), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)
    ax.axhline(0, color="#172033", linewidth=0.8)
    for offset, (case_name, color) in enumerate(zip(WEIGHT_CASES.keys(), colors)):
        positions = [position + (offset - 1) * width for position in sample_positions]
        ax.bar(positions, trace[case_name]["raw_outputs"], width=width, color=color, label=text[case_name])
    ax.set_xticks(sample_positions)
    ax.set_xticklabels([f"{text['sample_prefix']} {index + 1}" for index in sample_positions])
    ax.set_xlabel(text["sample_label"])
    ax.set_ylabel(text["raw_ylabel"])
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["raw_outfile"], bbox_inches="tight")
    plt.close(fig)


def save_variance_chart(text: dict[str, str], trace: dict) -> None:
    configure_font(text)
    case_names = list(WEIGHT_CASES.keys())
    values = [trace[case_name]["raw_variance"] for case_name in case_names]
    colors = ["#2563eb", "#f59e0b", "#dc2626"]
    fig, ax = plt.subplots(figsize=(5.8, 3.6), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)
    bars = ax.bar([text[case_name] for case_name in case_names], values, color=colors, width=0.55)
    for bar, value in zip(bars, values):
        ax.annotate(
            f"{value:.3f}".rstrip("0").rstrip("."),
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            textcoords="offset points",
            xytext=(0, 6),
            ha="center",
            fontsize=8.5,
            color="#172033",
        )
    ax.set_xlabel(text["case_label"])
    ax.set_ylabel(text["variance_ylabel"])
    ax.set_ylim(0, max(values) * 1.2)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["variance_outfile"], bbox_inches="tight")
    plt.close(fig)


def save_normalized_chart(text: dict[str, str], trace: dict) -> None:
    configure_font(text)
    sample_positions = list(range(len(INPUTS)))
    width = 0.24
    colors = ["#2563eb", "#f59e0b", "#dc2626"]
    fig, ax = plt.subplots(figsize=(6.8, 3.8), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)
    ax.axhline(0, color="#172033", linewidth=0.8)
    for offset, (case_name, color) in enumerate(zip(WEIGHT_CASES.keys(), colors)):
        positions = [position + (offset - 1) * width for position in sample_positions]
        ax.bar(positions, trace[case_name]["normalized_outputs"], width=width, color=color, label=text[case_name])
    ax.set_xticks(sample_positions)
    ax.set_xticklabels([f"{text['sample_prefix']} {index + 1}" for index in sample_positions])
    ax.set_xlabel(text["sample_label"])
    ax.set_ylabel(text["normalized_ylabel"])
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["normalized_outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    trace = build_trace()
    for text in LANG_TEXT.values():
        save_raw_output_chart(text, trace)
        save_variance_chart(text, trace)
        save_normalized_chart(text, trace)


if __name__ == "__main__":
    main()
