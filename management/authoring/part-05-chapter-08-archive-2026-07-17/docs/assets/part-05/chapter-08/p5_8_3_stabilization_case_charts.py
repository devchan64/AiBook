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

LANG_TEXT = {
    "ko": {
        "font_candidates": ["Noto Sans CJK KR", "NanumGothic", "Apple SD Gothic Neo", "AppleGothic", "Arial Unicode MS", "DejaVu Sans"],
        "paths_outfile": "stabilization-neuron-paths-ko.png",
        "range_outfile": "stabilization-layer-range-ko.png",
        "batch_outfile": "stabilization-batch-spread-ko.png",
        "step_label": "업데이트 단계",
        "weight_label": "뉴런 가중치",
        "layer_label": "층",
        "range_label": "활성값 범위 폭",
        "batch_label": "배치 장면",
        "activation_label": "중간 활성값 범위",
        "unstable_a": "흔들림 뉴런 A",
        "unstable_b": "흔들림 뉴런 B",
        "stable_a": "안정화 뉴런 A",
        "stable_b": "안정화 뉴런 B",
        "unstable_range": "흔들림 범위",
        "stable_range": "안정화 범위",
        "unstable_batch_1": "흔들림 배치 1",
        "unstable_batch_2": "흔들림 배치 2",
        "stable_batch_1": "안정화 배치 1",
        "stable_batch_2": "안정화 배치 2",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "paths_outfile": "stabilization-neuron-paths-en.png",
        "range_outfile": "stabilization-layer-range-en.png",
        "batch_outfile": "stabilization-batch-spread-en.png",
        "step_label": "update step",
        "weight_label": "neuron weight",
        "layer_label": "layer",
        "range_label": "activation range width",
        "batch_label": "batch scene",
        "activation_label": "mid activation range",
        "unstable_a": "unstable neuron A",
        "unstable_b": "unstable neuron B",
        "stable_a": "stabilized neuron A",
        "stable_b": "stabilized neuron B",
        "unstable_range": "unstable range",
        "stable_range": "stabilized range",
        "unstable_batch_1": "unstable batch 1",
        "unstable_batch_2": "unstable batch 2",
        "stable_batch_1": "stabilized batch 1",
        "stable_batch_2": "stabilized batch 2",
    },
}

WEIGHT_PATHS = {
    "unstable_a": [0.0, 0.3, 0.6],
    "unstable_b": [0.0, 0.3, 0.6],
    "stable_a": [0.10, 0.28, 0.46],
    "stable_b": [0.24, 0.38, 0.56],
}

LAYER_RANGES = {
    "unstable_range": [0.6, 1.8, 5.4],
    "stable_range": [0.6, 0.9, 1.1],
}

BATCH_RANGES = {
    "unstable_batch_1": (0.5, 1.0),
    "unstable_batch_2": (15.0, 24.0),
    "stable_batch_1": (-0.9, 1.1),
    "stable_batch_2": (-1.1, 1.0),
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


def style_axis(ax) -> None:
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_neuron_paths(text: dict[str, str]) -> None:
    configure_font(text)
    steps = [0, 1, 2]
    fig, ax = plt.subplots(figsize=(4.4, 3.2), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)
    series_specs = [
        ("unstable_a", "#dc2626", "o", "--"),
        ("unstable_b", "#f97316", "s", "--"),
        ("stable_a", "#2563eb", "o", "-"),
        ("stable_b", "#0f766e", "s", "-"),
    ]
    for key, color, marker, linestyle in series_specs:
        ax.plot(
            steps,
            WEIGHT_PATHS[key],
            marker=marker,
            linestyle=linestyle,
            linewidth=2.0,
            color=color,
            label=text[key],
        )
    ax.set_xticks(steps)
    ax.set_xlabel(text["step_label"])
    ax.set_ylabel(text["weight_label"])
    ax.set_ylim(-0.05, 0.7)
    ax.legend(loc="upper left", frameon=False, fontsize=7.6)
    fig.tight_layout(pad=0.8)
    fig.savefig(OUT_DIR / text["paths_outfile"], bbox_inches="tight")
    plt.close(fig)


def save_layer_range(text: dict[str, str]) -> None:
    configure_font(text)
    layers = [1, 2, 3]
    fig, ax = plt.subplots(figsize=(4.4, 3.2), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)
    ax.plot(layers, LAYER_RANGES["unstable_range"], marker="o", linewidth=2.2, linestyle="--", color="#dc2626", label=text["unstable_range"])
    ax.plot(layers, LAYER_RANGES["stable_range"], marker="o", linewidth=2.2, linestyle="-", color="#2563eb", label=text["stable_range"])
    ax.set_xticks(layers)
    ax.set_xlabel(text["layer_label"])
    ax.set_ylabel(text["range_label"])
    ax.set_ylim(0.0, 6.0)
    ax.legend(loc="upper left", frameon=False, fontsize=8)
    fig.tight_layout(pad=0.8)
    fig.savefig(OUT_DIR / text["range_outfile"], bbox_inches="tight")
    plt.close(fig)


def save_batch_spread(text: dict[str, str]) -> None:
    configure_font(text)
    entries = [
        ("unstable_batch_1", 1, "#dc2626"),
        ("unstable_batch_2", 2, "#f97316"),
        ("stable_batch_1", 3, "#2563eb"),
        ("stable_batch_2", 4, "#0f766e"),
    ]
    fig, ax = plt.subplots(figsize=(5.2, 3.2), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)
    for key, x_pos, color in entries:
        low, high = BATCH_RANGES[key]
        ax.vlines(x_pos, low, high, color=color, linewidth=6, alpha=0.95)
        ax.scatter([x_pos, x_pos], [low, high], color=color, s=18, zorder=3, label=text[key])
    ax.set_xticks([1, 2, 3, 4], ["U1", "U2", "S1", "S2"])
    ax.set_xlabel(text["batch_label"])
    ax.set_ylabel(text["activation_label"])
    ax.set_ylim(-1.5, 25.5)
    ax.legend(loc="upper left", frameon=False, fontsize=7.4, ncol=2)
    fig.tight_layout(pad=0.8)
    fig.savefig(OUT_DIR / text["batch_outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_neuron_paths(text)
        save_layer_range(text)
        save_batch_spread(text)


if __name__ == "__main__":
    main()
