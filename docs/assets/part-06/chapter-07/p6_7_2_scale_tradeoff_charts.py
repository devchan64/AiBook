from csv import DictReader
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
REQUESTS_PATH = OUT_DIR / "p6-7-scale-requests.csv"
STEPS_PATH = OUT_DIR / "p6-7-scale-steps.csv"

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
        "coverage_outfile": "scale-context-coverage-ko.png",
        "cost_outfile": "scale-inference-cost-ko.png",
        "review_outfile": "scale-data-review-burden-ko.png",
        "step_xlabel": "스케일 단계",
        "coverage_ylabel": "문맥 안 처리 요청 수",
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


def load_requests() -> list[dict[str, object]]:
    with REQUESTS_PATH.open(newline="", encoding="utf-8") as f:
        return [
            {
                "request_id": row["request_id"],
                "request_type": row["request_type"],
                "input_tokens": int(row["input_tokens"]),
                "priority": row["priority"],
            }
            for row in DictReader(f)
        ]


def load_steps() -> list[dict[str, object]]:
    with STEPS_PATH.open(newline="", encoding="utf-8") as f:
        return [
            {
                "scale": row["scale"],
                "rank": int(row["rank"]),
                "data_tokens_b": float(row["data_tokens_b"]),
                "parameters_b": float(row["parameters_b"]),
                "training_compute_units": float(row["training_compute_units"]),
                "context_window": int(row["context_window"]),
                "cost_per_1k_tokens": float(row["cost_per_1k_tokens"]),
                "latency_per_1k_tokens": float(row["latency_per_1k_tokens"]),
                "review_batches": int(row["review_batches"]),
            }
            for row in DictReader(f)
        ]


def summarize_scale_step(step: dict[str, object], requests: list[dict[str, object]]) -> dict[str, object]:
    supported = [
        request
        for request in requests
        if int(request["input_tokens"]) <= int(step["context_window"])
    ]
    over_limit = [
        request
        for request in requests
        if int(request["input_tokens"]) > int(step["context_window"])
    ]
    total_tokens = sum(int(request["input_tokens"]) for request in requests)
    total_cost = (total_tokens / 1000) * float(step["cost_per_1k_tokens"])
    total_latency = (total_tokens / 1000) * float(step["latency_per_1k_tokens"])
    high_priority_over_limit = [
        str(request["request_id"])
        for request in over_limit
        if request["priority"] == "high"
    ]
    over_limit_types = sorted({str(request["request_type"]) for request in over_limit})

    return {
        "scale": step["scale"],
        "context_window": step["context_window"],
        "supported_requests": len(supported),
        "over_limit_requests": len(over_limit),
        "over_limit_types": over_limit_types,
        "high_priority_over_limit": len(high_priority_over_limit),
        "total_inference_cost": round(total_cost, 2),
        "total_latency": round(total_latency, 2),
        "review_batches": step["review_batches"],
    }


def summarize_steps() -> list[dict[str, object]]:
    requests = load_requests()
    steps = sorted(load_steps(), key=lambda step: int(step["rank"]))
    return [summarize_scale_step(step, requests) for step in steps]


def print_summary() -> None:
    requests = load_requests()
    steps = sorted(load_steps(), key=lambda step: int(step["rank"]))
    print(f"request_rows = {len(requests)}")
    print(f"scale_steps = {len(steps)}")
    for row in [summarize_scale_step(step, requests) for step in steps]:
        print(row)


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_bar_chart(
    text: dict[str, str],
    outfile_key: str,
    ylabel_key: str,
    values_key: str,
    color: str,
) -> None:
    configure_font(text)
    summaries = summarize_steps()
    labels = [str(row["scale"]) for row in summaries]
    values = [float(row[values_key]) for row in summaries]

    fig, ax = plt.subplots(figsize=(6.6, 3.8), dpi=180)
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
    print_summary()
    for text in LANG_TEXT.values():
        save_bar_chart(text, "coverage_outfile", "coverage_ylabel", "supported_requests", "#2563eb")
        save_bar_chart(text, "cost_outfile", "cost_ylabel", "total_inference_cost", "#dc2626")
        save_bar_chart(text, "review_outfile", "review_ylabel", "review_batches", "#d97706")


if __name__ == "__main__":
    main()
