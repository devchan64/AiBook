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
CSV_PATH = OUT_DIR / "p6-10-3-response-path-log.csv"

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
        "outfile": "response-path-consistency-ko.png",
        "answer_ylabel": "최다 결론 비율",
        "risk_ylabel": "관찰된 점검 신호 수",
        "task_labels": {
            "mixed_refund_label": "복합\n분류",
            "discount_total": "수치\n비교",
            "current_refund_policy": "최신\n정책",
            "security_escalation": "보안\n이관",
        },
        "risk_labels": ["근거 누락", "계산 오류", "현재 정책 누락", "규칙 경고", "소수 결론"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "response-path-consistency-en.png",
        "answer_ylabel": "majority answer ratio",
        "risk_ylabel": "observed review signals",
        "task_labels": {
            "mixed_refund_label": "mixed\nlabel",
            "discount_total": "numeric\ncomparison",
            "current_refund_policy": "current\npolicy",
            "security_escalation": "security\nescalation",
        },
        "risk_labels": [
            "missing evidence",
            "calculation error",
            "stale policy",
            "rule warning",
            "minority answer",
        ],
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
        for column in [
            "evidence_mentioned",
            "calculation_correct",
            "policy_current",
            "rule_warning",
            "minority_answer",
        ]:
            row[column] = to_bool(row[column])
    return rows


def summarize(rows: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    summary = {}
    for task in sorted({row["task_name"] for row in rows}):
        group = [row for row in rows if row["task_name"] == task]
        answer_counts = {}
        for row in group:
            answer_counts[row["final_answer"]] = answer_counts.get(row["final_answer"], 0) + 1
        majority_answer, majority_count = max(answer_counts.items(), key=lambda item: item[1])
        summary[task] = {
            "run_count": len(group),
            "majority_answer": majority_answer,
            "majority_ratio": majority_count / len(group),
            "missing_evidence": sum(not row["evidence_mentioned"] for row in group),
            "calculation_error": sum(not row["calculation_correct"] for row in group),
            "stale_policy": sum(not row["policy_current"] for row in group),
            "rule_warning": sum(row["rule_warning"] for row in group),
            "minority_answer": sum(row["minority_answer"] for row in group),
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
    tasks = list(summary)
    labels = [text["task_labels"][task] for task in tasks]

    fig, (answer_ax, risk_ax) = plt.subplots(
        1,
        2,
        figsize=(9.2, 4.2),
        dpi=180,
        constrained_layout=True,
        gridspec_kw={"width_ratios": [1.0, 1.25]},
    )
    fig.patch.set_facecolor("white")
    for axis in (answer_ax, risk_ax):
        axis.set_facecolor("white")
        style_axis(axis)

    ratios = [summary[task]["majority_ratio"] for task in tasks]
    bars = answer_ax.bar(labels, ratios, color="#2563eb")
    for bar, value in zip(bars, ratios):
        answer_ax.annotate(
            f"{value:.2f}",
            (bar.get_x() + bar.get_width() / 2, value),
            textcoords="offset points",
            xytext=(0, 6),
            ha="center",
            fontsize=8.5,
            color="#172033",
        )
    answer_ax.set_ylabel(text["answer_ylabel"])
    answer_ax.set_ylim(0, 1.08)

    risk_columns = [
        "missing_evidence",
        "calculation_error",
        "stale_policy",
        "rule_warning",
        "minority_answer",
    ]
    colors = ["#f97316", "#dc2626", "#64748b", "#0f766e", "#7c3aed"]
    bottom = [0] * len(tasks)
    for column, label, color in zip(risk_columns, text["risk_labels"], colors):
        values = [summary[task][column] for task in tasks]
        risk_ax.bar(labels, values, bottom=bottom, color=color, label=label)
        bottom = [base + value for base, value in zip(bottom, values)]
    risk_ax.set_ylabel(text["risk_ylabel"])
    risk_ax.set_ylim(0, max(bottom) * 1.25)
    risk_ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, frameon=False, fontsize=8)

    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
