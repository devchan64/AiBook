from pathlib import Path
import os
import csv

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
EVAL_PATH = OUT_DIR / "p6_9_1_instruction_following_eval.csv"

def to_bool(value: str) -> bool:
    return value.lower() == "true"


def check_case(row: dict[str, str], prefix: str) -> bool:
    request_type = row["request_type"]
    lines = int(row[f"{prefix}_lines"])
    numbered_steps = int(row[f"{prefix}_numbered_steps"])
    table_rows = int(row[f"{prefix}_table_rows"])
    uncertainty_marker = to_bool(row[f"{prefix}_uncertainty_marker"])
    bullets = int(row[f"{prefix}_bullets"])

    if request_type == "three_line_summary":
        return lines == 3
    if request_type == "three_steps":
        return lines == 3 and numbered_steps == 3
    if request_type == "table":
        return table_rows >= 4
    if request_type == "limitations":
        return uncertainty_marker and bullets >= 2
    return False


def summarize_eval(path: Path) -> dict[str, int]:
    with path.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    return {
        "request_count": len(rows),
        "base_meets_request_count": sum(check_case(row, "base") for row in rows),
        "tuned_meets_request_count": sum(check_case(row, "tuned") for row in rows),
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
        "outfile": "instruction-tuning-request-match-ko.png",
        "ylabel": "평가 사례 수",
        "labels": ["일반 응답", "지시 튜닝 응답"],
        "met_label": "충족",
        "missed_label": "미충족",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "instruction-tuning-request-match-en.png",
        "ylabel": "evaluation cases",
        "labels": ["base response", "instruction-tuned"],
        "met_label": "met",
        "missed_label": "missed",
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


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_chart(text: dict[str, str]) -> None:
    configure_font(text)
    summary = summarize_eval(EVAL_PATH)
    met_values = [
        summary["base_meets_request_count"],
        summary["tuned_meets_request_count"],
    ]
    missed_values = [summary["request_count"] - value for value in met_values]

    fig, ax = plt.subplots(figsize=(6.1, 3.9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    met_bars = ax.bar(text["labels"], met_values, color="#2563eb", width=0.52, label=text["met_label"])
    missed_bars = ax.bar(
        text["labels"],
        missed_values,
        bottom=met_values,
        color="#cbd5e1",
        width=0.52,
        label=text["missed_label"],
    )
    for bar, value in zip(met_bars, met_values):
        if value > 4:
            label_y = value / 2
            label_offset = (0, 0)
            label_color = "white"
        else:
            label_y = value
            label_offset = (0, 6)
            label_color = "#172033"
        ax.annotate(
            f"{value:g}",
            (bar.get_x() + bar.get_width() / 2, label_y),
            textcoords="offset points",
            xytext=label_offset,
            ha="center",
            fontsize=9,
            color=label_color,
        )
    for bar, bottom, value in zip(missed_bars, met_values, missed_values):
        if value == 0:
            continue
        ax.annotate(
            f"{value:g}",
            (bar.get_x() + bar.get_width() / 2, bottom + value / 2),
            textcoords="offset points",
            xytext=(0, 0),
            ha="center",
            fontsize=9,
            color="#172033",
        )

    ax.set_ylabel(text["ylabel"])
    ax.set_ylim(0, summary["request_count"] * 1.18)
    ax.legend(frameon=False, loc="upper left", ncols=2)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
