from __future__ import annotations

import csv
from collections import Counter, defaultdict
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
CSV_PATH = OUT_DIR / "p6-14-2-agent-loop-observations.csv"

DECISION_ORDER = [
    "continue_refine",
    "stop_ready",
    "human_review",
]

DECISION_COLORS = {
    "continue_refine": "#2563eb",
    "stop_ready": "#0f766e",
    "human_review": "#dc2626",
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
        "outfile": "agent-loop-decision-split-ko.png",
        "decision_labels": {
            "continue_refine": "계속·재계획",
            "stop_ready": "멈춤",
            "human_review": "사람 검토",
        },
        "xlabel": "라운드",
        "ylabel": "결정 수",
        "title": "라운드가 진행되며 갈라지는 루프 결정",
        "final_title": "사례별 마지막 결정",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "agent-loop-decision-split-en.png",
        "decision_labels": {
            "continue_refine": "continue/refine",
            "stop_ready": "stop",
            "human_review": "human review",
        },
        "xlabel": "round",
        "ylabel": "decision count",
        "title": "Loop decisions change across rounds",
        "final_title": "Final decision by case",
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK",
            "PingFang SC",
            "Heiti SC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "agent-loop-decision-split-zh.png",
        "decision_labels": {
            "continue_refine": "继续·重规划",
            "stop_ready": "停止",
            "human_review": "人工审查",
        },
        "xlabel": "轮次",
        "ylabel": "决策数",
        "title": "轮次推进时分裂的循环决策",
        "final_title": "各案例最后决策",
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


def as_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def decide(row: dict[str, str]) -> str:
    retry_count = int(row["retry_count"])
    retry_limit = int(row["retry_limit"])
    if as_bool(row["approval_needed"]) or as_bool(row["conflict_found"]):
        return "human_review"
    if as_bool(row["action_failed"]) and retry_count >= retry_limit:
        return "human_review"
    if as_bool(row["evidence_sufficient"]) and not as_bool(row["action_failed"]):
        return "stop_ready"
    return "continue_refine"


def load_rows() -> list[dict[str, str]]:
    with CSV_PATH.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    for row in rows:
        row["decision"] = decide(row)
    return rows


def final_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_case: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_case[row["case_id"]].append(row)
    return [sorted(case_rows, key=lambda item: int(item["round"]))[-1] for case_rows in by_case.values()]


def save_chart(text: dict[str, str]) -> None:
    configure_font(text)
    rows = load_rows()
    rounds = sorted({int(row["round"]) for row in rows})
    round_counts = {
        round_number: Counter(row["decision"] for row in rows if int(row["round"]) == round_number)
        for round_number in rounds
    }
    final_counts = Counter(row["decision"] for row in final_rows(rows))

    fig, (ax1, ax2) = plt.subplots(
        1,
        2,
        figsize=(9.4, 4.2),
        dpi=180,
        gridspec_kw={"width_ratios": [1.45, 1.0]},
    )
    fig.patch.set_facecolor("white")

    bottom = [0] * len(rounds)
    for decision in DECISION_ORDER:
        values = [round_counts[round_number][decision] for round_number in rounds]
        ax1.bar(
            rounds,
            values,
            bottom=bottom,
            width=0.62,
            color=DECISION_COLORS[decision],
            label=text["decision_labels"][decision],
        )
        bottom = [prev + value for prev, value in zip(bottom, values)]

    ax1.set_title(text["title"], fontsize=11)
    ax1.set_xlabel(text["xlabel"])
    ax1.set_ylabel(text["ylabel"])
    ax1.set_xticks(rounds)
    ax1.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax1.set_axisbelow(True)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.legend(loc="upper right", frameon=False, fontsize=8)

    labels = [text["decision_labels"][decision] for decision in DECISION_ORDER]
    values = [final_counts[decision] for decision in DECISION_ORDER]
    colors = [DECISION_COLORS[decision] for decision in DECISION_ORDER]
    ax2.barh(labels, values, color=colors, height=0.55)
    ax2.set_title(text["final_title"], fontsize=11)
    ax2.set_xlabel(text["ylabel"])
    ax2.grid(True, axis="x", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax2.set_axisbelow(True)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    for index, value in enumerate(values):
        ax2.text(value + 0.08, index, str(value), va="center", fontsize=8.5)
    ax2.set_xlim(0, max(values) + 1.2)

    fig.tight_layout(pad=1.0)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
