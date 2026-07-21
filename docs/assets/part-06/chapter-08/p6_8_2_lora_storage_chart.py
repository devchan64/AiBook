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

BASE_MODEL_PARAMS = 7_000_000_000
TASK_COUNT_OPTIONS = [1, 3, 10]
FULL_FINETUNING_TRAINABLE_PER_TASK = 7_000_000_000
LORA_TRAINABLE_PER_TASK = 8_000_000
BYTES_PER_PARAM = 2

LANG_TEXT = {
    "ko": {
        "font_candidates": [
            "Noto Sans CJK KR",
            "NanumGothic",
            "Apple SD Gothic Neo",
            "AppleGothic",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "lora-storage-growth-ko.png",
        "xlabel": "업무 수",
        "ylabel": "추가 저장 크기(GB)",
        "full_label": "전체 파인튜닝",
        "lora_label": "LoRA 조정본",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "lora-storage-growth-en.png",
        "xlabel": "task count",
        "ylabel": "extra storage (GB)",
        "full_label": "full fine-tuning",
        "lora_label": "LoRA adapters",
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


def to_gb(param_count: int) -> float:
    return round(param_count * BYTES_PER_PARAM / (1024**3), 2)


def collect_rows() -> list[dict[str, float]]:
    rows = []
    for task_count in TASK_COUNT_OPTIONS:
        rows.append(
            {
                "task_count": task_count,
                "full_storage_gb": to_gb(FULL_FINETUNING_TRAINABLE_PER_TASK * task_count),
                "lora_storage_gb": to_gb(LORA_TRAINABLE_PER_TASK * task_count),
            }
        )
    return rows


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_chart(text: dict[str, str]) -> None:
    configure_font(text)
    rows = collect_rows()
    x_values = [row["task_count"] for row in rows]
    full_values = [row["full_storage_gb"] for row in rows]
    lora_values = [row["lora_storage_gb"] for row in rows]

    fig, ax = plt.subplots(figsize=(6.6, 3.9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    ax.plot(
        x_values,
        full_values,
        marker="o",
        linewidth=2.2,
        color="#dc2626",
        label=text["full_label"],
    )
    ax.plot(
        x_values,
        lora_values,
        marker="o",
        linewidth=2.2,
        color="#16a34a",
        label=text["lora_label"],
    )

    for x, value in zip(x_values, full_values):
        ax.annotate(
            f"{value:g}",
            (x, value),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=9,
            color="#172033",
        )
    for x, value in zip(x_values, lora_values):
        ax.annotate(
            f"{value:g}",
            (x, value),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=9,
            color="#172033",
        )

    ax.set_xticks(x_values)
    ax.set_xlabel(text["xlabel"])
    ax.set_ylabel(text["ylabel"])
    ax.set_ylim(0, max(full_values) * 1.16)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    _ = BASE_MODEL_PARAMS
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
