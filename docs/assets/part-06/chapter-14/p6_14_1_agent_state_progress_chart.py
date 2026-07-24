from collections import Counter
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
CSV_PATH = OUT_DIR / "p6-14-1-agent-observation-states.csv"

MODEL_ACTIONS_CAPTURED = {
    "coding-01": "search_or_inspect",
    "coding-02": "refine_search_or_reload",
    "coding-03": "collect_supporting_context",
    "coding-04": "retry_with_changed_step",
    "coding-05": "handoff_for_review",
    "coding-06": "attach_sources",
    "coding-07": "attach_sources",
    "coding-08": "compare_evidence",
    "coding-09": "retry_with_changed_step",
    "coding-10": "handoff_for_review",
    "coding-11": "attach_sources",
    "coding-12": "attach_sources",
    "research-01": "search_or_inspect",
    "research-02": "refine_search_or_reload",
    "research-03": "collect_supporting_context",
    "research-04": "compare_evidence",
    "research-05": "handoff_for_review",
    "research-06": "attach_sources",
    "research-07": "attach_sources",
    "research-08": "search_or_inspect",
    "research-09": "refine_search_or_reload",
    "research-10": "handoff_for_review",
    "research-11": "attach_sources",
    "research-12": "attach_sources",
    "workflow-01": "search_or_inspect",
    "workflow-02": "search_or_inspect",
    "workflow-03": "collect_supporting_context",
    "workflow-04": "retry_with_changed_step",
    "workflow-05": "handoff_for_review",
    "workflow-06": "handoff_for_review",
    "workflow-07": "attach_sources",
    "workflow-08": "attach_sources",
    "workflow-09": "search_or_inspect",
    "workflow-10": "handoff_for_review",
    "workflow-11": "attach_sources",
    "workflow-12": "attach_sources",
}

ACTION_ORDER = [
    "search_or_inspect",
    "refine_search_or_reload",
    "collect_supporting_context",
    "retry_with_changed_step",
    "compare_evidence",
    "handoff_for_review",
    "attach_sources",
    "finish",
]

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
        "outfile": "agent-state-progress-ko.png",
        "xlabel": "사례 수",
        "model_label": "모델 제안",
        "guard_label": "guard 최종 행동",
        "actions": {
            "search_or_inspect": "다시 찾기",
            "refine_search_or_reload": "최신 맥락 재확인",
            "collect_supporting_context": "근거 보강",
            "retry_with_changed_step": "재시도",
            "compare_evidence": "근거 비교",
            "handoff_for_review": "사람 검토",
            "attach_sources": "출처 부착",
            "finish": "종료",
        },
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "agent-state-progress-en.png",
        "xlabel": "cases",
        "model_label": "model proposal",
        "guard_label": "guard final action",
        "actions": {
            "search_or_inspect": "search again",
            "refine_search_or_reload": "refresh context",
            "collect_supporting_context": "add context",
            "retry_with_changed_step": "retry",
            "compare_evidence": "compare evidence",
            "handoff_for_review": "human review",
            "attach_sources": "attach sources",
            "finish": "finish",
        },
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
        "outfile": "agent-state-progress-zh.png",
        "xlabel": "案例数",
        "model_label": "模型建议",
        "guard_label": "guard 最终行动",
        "actions": {
            "search_or_inspect": "重新查找",
            "refine_search_or_reload": "重新确认当前语境",
            "collect_supporting_context": "补充依据",
            "retry_with_changed_step": "改变步骤重试",
            "compare_evidence": "比较证据",
            "handoff_for_review": "交给人工审查",
            "attach_sources": "附上来源",
            "finish": "结束",
        },
    },
}


def as_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def guard_next_action(state: dict[str, bool]) -> str:
    if state["approval_needed"]:
        return "handoff_for_review"
    if state["action_failed"]:
        return "retry_with_changed_step"
    if state["conflict_found"]:
        return "compare_evidence"
    if not state["found_context"]:
        return "search_or_inspect"
    if not state["current_context"]:
        return "refine_search_or_reload"
    if state["detail_missing"]:
        return "collect_supporting_context"
    if not state["sources_attached"]:
        return "attach_sources"
    return "finish"


def load_action_counts() -> tuple[Counter, Counter]:
    model_counts = Counter()
    guard_counts = Counter()
    with CSV_PATH.open(encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            state = {
                "found_context": as_bool(row["found_context"]),
                "current_context": as_bool(row["current_context"]),
                "detail_missing": as_bool(row["detail_missing"]),
                "conflict_found": as_bool(row["conflict_found"]),
                "action_failed": as_bool(row["action_failed"]),
                "approval_needed": as_bool(row["approval_needed"]),
                "sources_attached": as_bool(row["sources_attached"]),
            }
            model_counts[MODEL_ACTIONS_CAPTURED[row["case_id"]]] += 1
            guard_counts[guard_next_action(state)] += 1
    return model_counts, guard_counts


def choose_font(candidates: list[str]) -> str:
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def configure_font(text: dict[str, object]) -> None:
    plt.rcParams["font.family"] = choose_font(text["font_candidates"])
    plt.rcParams["axes.unicode_minus"] = False


def style_axis(ax) -> None:
    ax.grid(True, axis="x", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def annotate_bars(ax, bars) -> None:
    for bar in bars:
        value = bar.get_width()
        if value == 0:
            continue
        ax.annotate(
            f"{value:g}",
            (value, bar.get_y() + bar.get_height() / 2),
            textcoords="offset points",
            xytext=(4, 0),
            ha="left",
            va="center",
            fontsize=8.2,
            color="#172033",
        )


def save_chart(text: dict[str, object], model_counts: Counter, guard_counts: Counter) -> None:
    configure_font(text)

    y_positions = list(range(len(ACTION_ORDER)))
    model_values = [model_counts[action] for action in ACTION_ORDER]
    guard_values = [guard_counts[action] for action in ACTION_ORDER]
    height = 0.36

    fig, ax = plt.subplots(figsize=(8.4, 4.9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    model_bars = ax.barh(
        [pos - height / 2 for pos in y_positions],
        model_values,
        height=height,
        color="#64748b",
        label=text["model_label"],
    )
    guard_bars = ax.barh(
        [pos + height / 2 for pos in y_positions],
        guard_values,
        height=height,
        color="#2563eb",
        label=text["guard_label"],
    )
    annotate_bars(ax, model_bars)
    annotate_bars(ax, guard_bars)

    ax.set_yticks(y_positions)
    ax.set_yticklabels([text["actions"][action] for action in ACTION_ORDER])
    ax.invert_yaxis()
    ax.set_xlabel(text["xlabel"])
    ax.set_xlim(0, max(max(model_values), max(guard_values)) + 2)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.1), ncol=2, frameon=False)
    fig.tight_layout(pad=1.0)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    model_counts, guard_counts = load_action_counts()
    for text in LANG_TEXT.values():
        save_chart(text, model_counts, guard_counts)


if __name__ == "__main__":
    main()
