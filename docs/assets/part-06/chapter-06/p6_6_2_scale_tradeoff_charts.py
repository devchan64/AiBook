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

REQUESTS = [
    {"task": "faq", "input_tokens": 600},
    {"task": "summary", "input_tokens": 2400},
    {"task": "contract_review", "input_tokens": 6200},
    {"task": "code_assistant", "input_tokens": 4100},
]

SCALE_STEPS = [
    {
        "name": "small",
        "data_tokens_b": 80,
        "parameters_b": 1.5,
        "training_compute_units": 120,
        "context_window": 2048,
        "cost_per_1k_tokens": 0.2,
        "latency_per_1k_tokens": 0.7,
        "review_batches": 2,
    },
    {
        "name": "medium",
        "data_tokens_b": 400,
        "parameters_b": 7,
        "training_compute_units": 900,
        "context_window": 4096,
        "cost_per_1k_tokens": 0.55,
        "latency_per_1k_tokens": 1.1,
        "review_batches": 7,
    },
    {
        "name": "large",
        "data_tokens_b": 1800,
        "parameters_b": 30,
        "training_compute_units": 7200,
        "context_window": 8192,
        "cost_per_1k_tokens": 1.2,
        "latency_per_1k_tokens": 1.8,
        "review_batches": 22,
    },
]

LANG_TEXT = {
    "ko": {
        "font_candidates": ["Noto Sans CJK KR", "NanumGothic", "Apple SD Gothic Neo", "AppleGothic", "Arial Unicode MS", "DejaVu Sans"],
        "coverage_outfile": "scale-context-coverage-ko.png",
        "cost_outfile": "scale-inference-cost-ko.png",
        "review_outfile": "scale-data-review-burden-ko.png",
        "step_xlabel": "스케일 단계",
        "coverage_ylabel": "처리 가능한 요청 수",
        "cost_ylabel": "총 추론 비용",
        "review_ylabel": "검증 대기 데이터 묶음",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "coverage_outfile": "scale-context-coverage-en.png",
        "cost_outfile": "scale-inference-cost-en.png",
        "review_outfile": "scale-data-review-burden-en.png",
        "step_xlabel": "scale step",
        "coverage_ylabel": "requests within context",
        "cost_ylabel": "total inference cost",
        "review_ylabel": "data review batches",
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


def summarize_steps() -> list[dict[str, float]]:
    summaries = []
    total_tokens = sum(request["input_tokens"] for request in REQUESTS)
    for step in SCALE_STEPS:
        supported = [
            request["task"]
            for request in REQUESTS
            if request["input_tokens"] <= step["context_window"]
        ]
        summaries.append(
            {
                "name": step["name"],
                "supported_count": len(supported),
                "total_inference_cost": round((total_tokens / 1000) * step["cost_per_1k_tokens"], 2),
                "review_batches": step["review_batches"],
            }
        )
    return summaries


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_bar_chart(text: dict[str, str], outfile_key: str, ylabel_key: str, values_key: str, color: str) -> None:
    configure_font(text)
    summaries = summarize_steps()
    labels = [row["name"] for row in summaries]
    values = [row[values_key] for row in summaries]

    fig, ax = plt.subplots(figsize=(6.2, 3.7), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)
    bars = ax.bar(labels, values, color=color, width=0.56)
    for bar, value in zip(bars, values):
        ax.annotate(
            f"{value:g}",
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            textcoords="offset points",
            xytext=(0, 7),
            ha="center",
            fontsize=9,
            color="#172033",
        )
    ax.set_xlabel(text["step_xlabel"])
    ax.set_ylabel(text[ylabel_key])
    ax.set_ylim(0, max(values) * 1.22)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text[outfile_key], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_bar_chart(text, "coverage_outfile", "coverage_ylabel", "supported_count", "#2563eb")
        save_bar_chart(text, "cost_outfile", "cost_ylabel", "total_inference_cost", "#dc2626")
        save_bar_chart(text, "review_outfile", "review_ylabel", "review_batches", "#d97706")


if __name__ == "__main__":
    main()
