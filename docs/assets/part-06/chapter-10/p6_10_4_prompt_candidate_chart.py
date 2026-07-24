from pathlib import Path
import csv
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
CSV_PATH = OUT_DIR / "p6-10-4-prompt-candidate-eval.csv"
WEIGHTS = {
    "format_ok": 1,
    "key_fact_ok": 3,
    "forbidden_ok": 3,
    "boundary_ok": 2,
}

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
        "outfile": "prompt-candidate-score-ko.png",
        "score_ylabel": "가중 점수",
        "failure_ylabel": "실패 건수",
        "failure_labels": ["형식", "핵심 항목", "금지 조건", "경계 사례"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "prompt-candidate-score-en.png",
        "score_ylabel": "weighted score",
        "failure_ylabel": "failure count",
        "failure_labels": ["format", "key facts", "forbidden rule", "boundary cases"],
    },
}


def choose_font(candidates: list[str]) -> str:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def configure_font(text: dict[str, object]) -> None:
    plt.rcParams["font.family"] = choose_font(text["font_candidates"])
    plt.rcParams["axes.unicode_minus"] = False


def to_bool(value: str) -> bool:
    return value.lower() == "true"


def read_rows() -> list[dict[str, object]]:
    with CSV_PATH.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    for row in rows:
        for column in WEIGHTS:
            row[column] = to_bool(row[column])
        row["response_too_long"] = to_bool(row["response_too_long"])
    return rows


def summarize(rows: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    summary = {}
    for candidate in sorted({row["prompt_candidate"] for row in rows}):
        group = [row for row in rows if row["prompt_candidate"] == candidate]
        score = sum(
            sum(weight for column, weight in WEIGHTS.items() if row[column])
            for row in group
        )
        summary[candidate] = {
            "score": score,
            "format_fail": sum(not row["format_ok"] for row in group),
            "key_fact_fail": sum(not row["key_fact_ok"] for row in group),
            "forbidden_fail": sum(not row["forbidden_ok"] for row in group),
            "boundary_fail": sum(not row["boundary_ok"] for row in group),
        }
    return summary


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_chart(text: dict[str, object]) -> None:
    configure_font(text)
    summary = summarize(read_rows())
    candidates = list(summary)
    scores = [summary[candidate]["score"] for candidate in candidates]

    fig, (score_ax, failure_ax) = plt.subplots(
        2,
        1,
        figsize=(7.2, 5.6),
        dpi=180,
        constrained_layout=True,
        gridspec_kw={"height_ratios": [1.1, 1.4], "hspace": 0.48},
    )
    fig.patch.set_facecolor("white")
    for axis in (score_ax, failure_ax):
        axis.set_facecolor("white")
        style_axis(axis)

    bars = score_ax.bar(candidates, scores, color="#2563eb")
    for bar, value in zip(bars, scores):
        score_ax.annotate(
            f"{value:g}",
            (bar.get_x() + bar.get_width() / 2, value),
            textcoords="offset points",
            xytext=(0, 6),
            ha="center",
            fontsize=8.5,
            color="#172033",
        )
    score_ax.set_ylabel(text["score_ylabel"])
    score_ax.set_ylim(0, max(scores) * 1.18)

    failure_columns = ["format_fail", "key_fact_fail", "forbidden_fail", "boundary_fail"]
    failure_labels = text["failure_labels"]
    x_positions = list(range(len(candidates)))
    bottom = [0] * len(candidates)
    colors = ["#94a3b8", "#f97316", "#dc2626", "#0f766e"]
    for column, label, color in zip(failure_columns, failure_labels, colors):
        values = [summary[candidate][column] for candidate in candidates]
        failure_ax.bar(candidates, values, bottom=bottom, color=color, label=label)
        bottom = [base + value for base, value in zip(bottom, values)]

    failure_ax.set_ylabel(text["failure_ylabel"])
    failure_ax.set_ylim(0, max(bottom) * 1.2)
    failure_ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.01), ncol=4, frameon=False, fontsize=8)
    failure_ax.set_xticks(x_positions, candidates)

    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
