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
CSV_PATH = OUT_DIR / "p6_16_1_llm_eval_outputs.csv"


def split_terms(value: str) -> list[str]:
    return [term.strip() for term in value.split("|") if term.strip()]


def evaluate_row(row: dict[str, str]) -> dict[str, bool | int]:
    output = row["model_output"]
    source = row["source_excerpt"]
    required_claims = split_terms(row["required_claim_terms"])
    unsupported_claims = split_terms(row["unsupported_claim_terms"])
    safety_risk_terms = split_terms(row.get("safety_risk_terms", ""))
    safety_required_terms = split_terms(row.get("safety_required_terms", ""))
    format_terms = split_terms(row["format_terms"])
    helpful_terms = split_terms(row["helpful_terms"])

    source_backed_claims = [term for term in required_claims if term in source]
    matched_claims = [term for term in source_backed_claims if term in output]
    unsupported_hits = [
        term for term in unsupported_claims if term in output and term not in source
    ]
    safety_risk_hits = [term for term in safety_risk_terms if term in output]
    missing_safety_terms = [
        term for term in safety_required_terms if term not in output
    ]

    correctness = len(matched_claims) >= max(1, len(source_backed_claims) - 1)
    groundedness = not unsupported_hits
    safety = not safety_risk_hits and not missing_safety_terms
    format_compliance = output.endswith(".") and all(term in output for term in format_terms)
    helpfulness = any(term in output for term in helpful_terms)

    return {
        "correctness": correctness,
        "groundedness": groundedness,
        "safety": safety,
        "format_compliance": format_compliance,
        "helpfulness": helpfulness,
        "passes_all": all(
            [correctness, groundedness, safety, format_compliance, helpfulness]
        ),
    }


def build_summary() -> dict[str, int]:
    with CSV_PATH.open(newline="", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))

    reports = [evaluate_row(row) for row in rows]
    return {
        "all_pass_count": sum(report["passes_all"] for report in reports),
        "correct_count": sum(report["correctness"] for report in reports),
        "grounded_count": sum(report["groundedness"] for report in reports),
        "safety_count": sum(report["safety"] for report in reports),
        "format_ok_count": sum(report["format_compliance"] for report in reports),
        "helpful_count": sum(report["helpfulness"] for report in reports),
        "answer_count": len(reports),
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
        "outfile": "llm-eval-axis-check-ko.png",
        "ylabel": "통과한 후보 수",
        "labels": ["전체 통과", "정확성", "근거성", "안전성", "형식", "유용성"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "llm-eval-axis-check-en.png",
        "ylabel": "passed candidates",
        "labels": ["all axes", "correct", "grounded", "safe", "format", "helpful"],
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


def save_chart(text: dict[str, str], summary: dict[str, int]) -> None:
    configure_font(text)
    values = [
        summary["all_pass_count"],
        summary["correct_count"],
        summary["grounded_count"],
        summary["safety_count"],
        summary["format_ok_count"],
        summary["helpful_count"],
    ]
    colors = ["#0f766e", "#dc2626", "#2563eb", "#7c3aed", "#64748b", "#f59e0b"]

    fig, ax = plt.subplots(figsize=(8.4, 3.9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    bars = ax.bar(text["labels"], values, color=colors, width=0.56)
    for bar in bars:
        value = bar.get_height()
        ratio = value / summary["answer_count"]
        ax.annotate(
            f"{value:g}\n({ratio:.0%})",
            (bar.get_x() + bar.get_width() / 2, value),
            textcoords="offset points",
            xytext=(0, 7),
            ha="center",
            fontsize=8.8,
            color="#172033",
        )

    ax.set_ylabel(text["ylabel"])
    ax.set_ylim(0, summary["answer_count"] * 1.24)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    summary = build_summary()
    for text in LANG_TEXT.values():
        save_chart(text, summary)


if __name__ == "__main__":
    main()
