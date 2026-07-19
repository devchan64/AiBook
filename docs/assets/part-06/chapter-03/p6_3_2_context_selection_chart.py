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

OUT_DIR = Path(__file__).resolve().parent

CONTEXT_ITEMS = [
    {
        "name": "system instruction",
        "tokens": 18,
        "priority": 100,
        "content": "Follow policy and explain the cause clearly.",
    },
    {
        "name": "older chat history",
        "tokens": 30,
        "priority": 40,
        "content": "Earlier small talk and unrelated setup questions.",
    },
    {
        "name": "repeated greeting",
        "tokens": 8,
        "priority": 5,
        "content": "Hello again thank you hello again.",
    },
    {
        "name": "user question",
        "tokens": 12,
        "priority": 95,
        "content": "Why did login fail after the deploy?",
    },
    {
        "name": "current error log",
        "tokens": 22,
        "priority": 90,
        "content": "Login failed because session token signature mismatch after deploy.",
    },
    {
        "name": "related function code",
        "tokens": 20,
        "priority": 88,
        "content": "verify_session_token compares signature and rejects mismatch.",
    },
]

TOKEN_BUDGET = 60
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
        "selected_tokens_ylabel": "선택된 토큰 수",
        "summary_ylabel": "보존/관련도 점수",
        "must_keep_label": "필수 상태 보존",
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
        "selected_tokens_ylabel": "selected tokens",
        "summary_ylabel": "coverage / relevance score",
        "must_keep_label": "must-keep coverage",
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


def summarize() -> dict[str, dict[str, object]]:
    methods = {
        "naive": select_in_original_order(CONTEXT_ITEMS, TOKEN_BUDGET),
        "priority": select_by_priority(CONTEXT_ITEMS, TOKEN_BUDGET),
    }
    summary = {}
    for method, selected in methods.items():
        selected_names = {item["name"] for item in selected}
        summary[method] = {
            "selected_tokens": {
                item["name"]: item["tokens"] if item["name"] in selected_names else 0
                for item in CONTEXT_ITEMS
            },
            "must_keep_count": len(selected_names & MUST_KEEP),
            "relevance_sum": sum(relevance_score(item) for item in selected),
        }
    return summary


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_chart(text: dict[str, object]) -> None:
    configure_font(text)
    rows = summarize()
    item_names = [item["name"] for item in CONTEXT_ITEMS]
    item_labels = [text["item_labels"][name] for name in item_names]
    x_positions = list(range(len(item_names)))
    width = 0.34

    fig, (selection_ax, summary_ax) = plt.subplots(
        2,
        1,
        figsize=(7.6, 5.6),
        dpi=180,
        gridspec_kw={"height_ratios": [2.1, 1.0], "hspace": 0.42},
    )
    fig.patch.set_facecolor("white")
    for axis in (selection_ax, summary_ax):
        axis.set_facecolor("white")
        style_axis(axis)

    method_order = ["naive", "priority"]
    colors = {"naive": "#64748b", "priority": "#0f766e"}
    for index, method in enumerate(method_order):
        values = [rows[method]["selected_tokens"][name] for name in item_names]
        positions = [x + (index - 0.5) * width for x in x_positions]
        bars = selection_ax.bar(
            positions,
            values,
            width=width,
            color=colors[method],
            label=text["method_labels"][method],
        )
        for bar, value in zip(bars, values):
            if value == 0:
                continue
            selection_ax.annotate(
                f"{value:g}",
                (bar.get_x() + bar.get_width() / 2, value),
                textcoords="offset points",
                xytext=(0, 5),
                ha="center",
                fontsize=7.8,
                color="#172033",
            )

    selection_ax.axhline(TOKEN_BUDGET, color="#dc2626", linewidth=1.0, linestyle="--", alpha=0.8)
    selection_ax.set_xticks(x_positions, item_labels)
    selection_ax.set_ylabel(text["selected_tokens_ylabel"])
    selection_ax.set_ylim(0, 34)
    selection_ax.legend(loc="upper right", frameon=False, fontsize=8.5)

    summary_labels = [text["must_keep_label"], text["relevance_label"]]
    summary_x = [0, 1]
    for index, method in enumerate(method_order):
        values = [rows[method]["must_keep_count"], rows[method]["relevance_sum"]]
        positions = [x + (index - 0.5) * width for x in summary_x]
        bars = summary_ax.bar(positions, values, width=width, color=colors[method])
        for bar, value in zip(bars, values):
            summary_ax.annotate(
                f"{value:g}",
                (bar.get_x() + bar.get_width() / 2, value),
                textcoords="offset points",
                xytext=(0, 5),
                ha="center",
                fontsize=8,
                color="#172033",
            )
    summary_ax.set_xticks(summary_x, summary_labels)
    summary_ax.set_ylabel(text["summary_ylabel"])
    summary_ax.set_ylim(0, 9)

    fig.subplots_adjust(left=0.11, right=0.98, top=0.96, bottom=0.11, hspace=0.42)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
