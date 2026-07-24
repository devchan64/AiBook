from pathlib import Path
import os
import string

REPO_ROOT = Path(__file__).resolve().parents[4]
MPL_CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))
os.environ.setdefault("XDG_CACHE_HOME", str(MPL_CACHE))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import tiktoken

OUT_DIR = Path(__file__).resolve().parent

CONTEXT_ITEMS = [
    {
        "name": "system instruction",
        "priority": 100,
        "content": "Follow policy and explain the cause clearly.",
    },
    {
        "name": "older chat history",
        "priority": 40,
        "content": "Earlier small talk and unrelated setup questions.",
    },
    {
        "name": "repeated greeting",
        "priority": 5,
        "content": "Hello again thank you hello again.",
    },
    {
        "name": "user question",
        "priority": 95,
        "content": "Why did login fail after the deploy?",
    },
    {
        "name": "current error log",
        "priority": 90,
        "content": "Login failed because session token signature mismatch after deploy.",
    },
    {
        "name": "related function code",
        "priority": 88,
        "content": "verify_session_token compares signature and rejects mismatch.",
    },
]

ENCODING = tiktoken.get_encoding("o200k_base")
for item in CONTEXT_ITEMS:
    item["tokens"] = len(ENCODING.encode(item["content"]))

BUDGET_OPTIONS = [24, 32, 40]
MUST_KEEP = {"system instruction", "user question", "current error log"}
QUERY_KEYWORDS = {"login", "fail", "deploy", "token", "signature", "mismatch"}

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
        "outfile": "context-selection-budget-ko.png",
        "item_labels": {
            "system instruction": "시스템\n지시",
            "older chat history": "오래된\n대화",
            "repeated greeting": "반복\n인사",
            "user question": "현재\n질문",
            "current error log": "현재\n오류",
            "related function code": "관련\n코드",
        },
        "method_labels": {
            "naive": "입력 순서",
            "priority": "우선순위",
        },
        "budget_xlabel": "토큰 예산",
        "coverage_ylabel": "필수 상태 보존 수",
        "relevance_ylabel": "relevance 합계",
        "relevance_label": "relevance 합계",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "context-selection-budget-en.png",
        "item_labels": {
            "system instruction": "system\ninstruction",
            "older chat history": "older\nhistory",
            "repeated greeting": "repeated\ngreeting",
            "user question": "user\nquestion",
            "current error log": "error\nlog",
            "related function code": "related\ncode",
        },
        "method_labels": {
            "naive": "original order",
            "priority": "priority based",
        },
        "budget_xlabel": "token budget",
        "coverage_ylabel": "must-keep items kept",
        "relevance_ylabel": "relevance sum",
        "relevance_label": "relevance sum",
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


def select_in_original_order(items: list[dict[str, object]], budget: int) -> list[dict[str, object]]:
    selected = []
    used = 0
    for item in items:
        if used + item["tokens"] <= budget:
            selected.append(item)
            used += item["tokens"]
    return selected


def select_by_priority(items: list[dict[str, object]], budget: int) -> list[dict[str, object]]:
    ranked = sorted(items, key=lambda item: item["priority"], reverse=True)
    selected = []
    used = 0
    for item in ranked:
        if used + item["tokens"] <= budget:
            selected.append(item)
            used += item["tokens"]
    return selected


def relevance_score(item: dict[str, object]) -> int:
    clean_content = item["content"].lower().translate(str.maketrans("", "", string.punctuation))
    return len(set(clean_content.split()) & QUERY_KEYWORDS)


def summarize_budget(budget: int) -> dict[str, dict[str, int]]:
    methods = {
        "naive": select_in_original_order(CONTEXT_ITEMS, budget),
        "priority": select_by_priority(CONTEXT_ITEMS, budget),
    }
    summary = {}
    for method, selected in methods.items():
        selected_names = {item["name"] for item in selected}
        summary[method] = {
            "must_keep_count": len(selected_names & MUST_KEEP),
            "relevance_sum": sum(relevance_score(item) for item in selected),
        }
    return summary


def summarize_all_budgets() -> dict[int, dict[str, dict[str, int]]]:
    return {budget: summarize_budget(budget) for budget in BUDGET_OPTIONS}


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_chart(text: dict[str, object]) -> None:
    configure_font(text)
    rows = summarize_all_budgets()
    x_positions = list(range(len(BUDGET_OPTIONS)))
    width = 0.34

    fig, (coverage_ax, relevance_ax) = plt.subplots(
        2,
        1,
        figsize=(7.6, 5.2),
        dpi=180,
        gridspec_kw={"height_ratios": [1.0, 1.0], "hspace": 0.36},
    )
    fig.patch.set_facecolor("white")
    for axis in (coverage_ax, relevance_ax):
        axis.set_facecolor("white")
        style_axis(axis)

    method_order = ["naive", "priority"]
    colors = {"naive": "#64748b", "priority": "#0f766e"}
    metric_axes = [
        (coverage_ax, "must_keep_count", text["coverage_ylabel"], 3.8),
        (relevance_ax, "relevance_sum", text["relevance_ylabel"], 11),
    ]
    for axis, metric, ylabel, ymax in metric_axes:
        for index, method in enumerate(method_order):
            values = [rows[budget][method][metric] for budget in BUDGET_OPTIONS]
            positions = [x + (index - 0.5) * width for x in x_positions]
            bars = axis.bar(
                positions,
                values,
                width=width,
                color=colors[method],
                label=text["method_labels"][method],
            )
            for bar, value in zip(bars, values):
                axis.annotate(
                    f"{value:g}",
                    (bar.get_x() + bar.get_width() / 2, value),
                    textcoords="offset points",
                    xytext=(0, 5),
                    ha="center",
                    fontsize=8,
                    color="#172033",
                )
        axis.set_xticks(x_positions, [str(budget) for budget in BUDGET_OPTIONS])
        axis.set_ylabel(ylabel)
        axis.set_ylim(0, ymax)

    coverage_ax.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, 1.01),
        ncol=2,
        frameon=False,
        fontsize=8.5,
    )
    relevance_ax.set_xlabel(text["budget_xlabel"])

    fig.subplots_adjust(left=0.11, right=0.98, top=0.96, bottom=0.12, hspace=0.36)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
