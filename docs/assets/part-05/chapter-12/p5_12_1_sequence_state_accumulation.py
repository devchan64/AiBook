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
import numpy as np


OUT_DIR = Path(__file__).resolve().parent

SEQUENCES = {
    "gradual_rise": [60, 65, 72, 80],
    "temporary_spike": [80, 60, 60, 80],
}

ALPHA = 0.6
THRESHOLD = 63

LANG_TEXT = {
    "ko": {
        "font_candidates": ["Apple SD Gothic Neo", "AppleGothic", "Arial Unicode MS", "DejaVu Sans"],
        "xlabel": "step",
        "input_ylabel": "입력값",
        "state_ylabel": "누적 상태",
        "threshold": "경보 기준",
        "gradual": "지속 상승",
        "spike": "일시 튐",
        "outfile": "sequence-state-accumulation-ko.png",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "xlabel": "step",
        "input_ylabel": "input value",
        "state_ylabel": "accumulated state",
        "threshold": "alert threshold",
        "gradual": "gradual rise",
        "spike": "temporary spike",
        "outfile": "sequence-state-accumulation-en.png",
    },
}


def choose_font(candidates: list[str]) -> str:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def accumulated_state(sequence: list[int]) -> list[float]:
    state = 0.0
    states = []
    for value in sequence:
        state = ALPHA * state + (1 - ALPHA) * value
        states.append(state)
    return states


def save_chart(lang: str, text: dict[str, object]) -> None:
    plt.rcParams["font.family"] = choose_font(text["font_candidates"])
    plt.rcParams["axes.unicode_minus"] = False

    steps = np.arange(1, 5)
    gradual_input = SEQUENCES["gradual_rise"]
    spike_input = SEQUENCES["temporary_spike"]
    gradual_state = accumulated_state(gradual_input)
    spike_state = accumulated_state(spike_input)

    fig, (ax_input, ax_state) = plt.subplots(2, 1, figsize=(7.4, 5.3), dpi=160, sharex=True)
    fig.patch.set_facecolor("white")
    ax_input.set_facecolor("white")
    ax_state.set_facecolor("white")

    gradual_color = "#0969da"
    spike_color = "#cf222e"
    threshold_color = "#6e7781"

    ax_input.plot(
        steps,
        gradual_input,
        color=gradual_color,
        linestyle=(0, (4, 3)),
        linewidth=1.6,
        marker="o",
        markersize=4.8,
        alpha=0.82,
        label=text["gradual"],
    )
    ax_input.plot(
        steps,
        spike_input,
        color=spike_color,
        linestyle=(0, (4, 3)),
        linewidth=1.6,
        marker="o",
        markersize=4.8,
        alpha=0.82,
        label=text["spike"],
    )
    ax_state.plot(
        steps,
        gradual_state,
        color=gradual_color,
        linewidth=2.4,
        marker="o",
        markersize=5.2,
        label=text["gradual"],
    )
    ax_state.plot(
        steps,
        spike_state,
        color=spike_color,
        linewidth=2.4,
        marker="o",
        markersize=5.2,
        label=text["spike"],
    )
    ax_state.axhline(THRESHOLD, color=threshold_color, linewidth=1.5, linestyle=(0, (5, 4)))
    ax_state.text(3.15, THRESHOLD + 1.1, text["threshold"], color=threshold_color, fontsize=9.5, ha="left", va="bottom")

    ax_state.scatter([4], [gradual_state[-1]], color=gradual_color, s=70, edgecolor="white", linewidth=1.0, zorder=4)
    ax_state.scatter([4], [spike_state[-1]], color=spike_color, s=70, edgecolor="white", linewidth=1.0, zorder=4)

    ax_input.set_xlim(0.85, 4.15)
    ax_input.set_ylim(54, 84)
    ax_state.set_ylim(20, 68)
    ax_state.set_xlabel(text["xlabel"])
    ax_input.set_ylabel(text["input_ylabel"])
    ax_state.set_ylabel(text["state_ylabel"])
    ax_input.set_xticks(steps)
    for ax in (ax_input, ax_state):
        ax.grid(True, axis="both", color="#d0d7de", linewidth=0.8, alpha=0.75)
        ax.set_axisbelow(True)
        ax.legend(loc="upper left", frameon=True, framealpha=0.94, fontsize=8.8, ncol=2)

    fig.tight_layout(pad=0.8)
    fig.savefig(OUT_DIR / text["outfile"])
    plt.close(fig)


def main() -> None:
    for lang, text in LANG_TEXT.items():
        save_chart(lang, text)


if __name__ == "__main__":
    main()
