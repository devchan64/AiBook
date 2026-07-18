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
import numpy as np


OUT_DIR = Path(__file__).resolve().parent
GAPS = np.array([1, 3, 6])


def sequential_state(instruction_document: list[str], decay: float = 0.72) -> tuple[dict[str, float], float, str]:
    state = {"restart": 0.0, "blocked": 0.0, "pressure": 0.0}
    for line in instruction_document:
        lowered = line.lower()
        for key in state:
            state[key] *= decay
        if "restart" in lowered:
            state["restart"] += 1.0
        if "blocked" in lowered:
            state["blocked"] += 1.0
        if "pressure" in lowered or "vented" in lowered:
            state["pressure"] += 1.0
    support = round(min(state.values()), 3)
    decision = "keeps block" if support >= 0.45 else "loses block"
    return {key: round(value, 3) for key, value in state.items()}, support, decision


def direct_reference(instruction_document: list[str]) -> tuple[tuple[int, int, str], str]:
    matches = []
    for idx, line in enumerate(instruction_document[:-1], start=1):
        lowered = line.lower()
        score = 0
        for keyword in ["restart", "blocked", "pressure"]:
            if keyword in lowered:
                score += 1
        matches.append((score, idx, line))
    best = max(matches)
    decision = "keeps block" if best[0] == 3 else "loses block"
    return best, decision


def build_outputs() -> tuple[np.ndarray, np.ndarray, list[str], list[str]]:
    restart_block_rule = "Rule: restart stays blocked until vessel pressure is fully vented."
    restart_question = "Question: can the line restart now?"
    state_supports = []
    direct_scores = []
    state_decisions = []
    direct_decisions = []

    for gap in GAPS:
        filler = [f"Detail line {i}: general maintenance note only." for i in range(1, int(gap) + 1)]
        instruction_document = [restart_block_rule] + filler + [restart_question]
        _, state_support, state_decision = sequential_state(instruction_document)
        best_match, direct_decision = direct_reference(instruction_document)
        state_supports.append(state_support)
        direct_scores.append(best_match[0])
        state_decisions.append(state_decision)
        direct_decisions.append(direct_decision)

    return np.array(state_supports), np.array(direct_scores), state_decisions, direct_decisions


STATE_SUPPORTS, DIRECT_SCORES, STATE_DECISIONS, DIRECT_DECISIONS = build_outputs()

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
        "support_outfile": "long-dependency-state-support-ko.png",
        "decision_outfile": "long-dependency-decision-comparison-ko.png",
        "gap_label": "중간 설명 줄 수(gap)",
        "support_label": "상태 기반 핵심 단서 최소값",
        "direct_label": "직접 참조 match score",
        "threshold_label": "차단 유지 기준",
        "state": "상태 기반",
        "direct": "직접 참조",
        "keeps": "차단 유지",
        "loses": "차단 상실",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "support_outfile": "long-dependency-state-support-en.png",
        "decision_outfile": "long-dependency-decision-comparison-en.png",
        "gap_label": "number of filler lines (gap)",
        "support_label": "state-based minimum cue support",
        "direct_label": "direct match score",
        "threshold_label": "keep-block threshold",
        "state": "state-based",
        "direct": "direct reference",
        "keeps": "keeps block",
        "loses": "loses block",
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK JP",
            "Source Han Sans SC",
            "Microsoft YaHei",
            "PingFang SC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "support_outfile": "long-dependency-state-support-zh.png",
        "decision_outfile": "long-dependency-decision-comparison-zh.png",
        "gap_label": "中间说明行数（gap）",
        "support_label": "状态型核心线索最小值",
        "direct_label": "直接匹配分数",
        "threshold_label": "维持阻断阈值",
        "state": "状态型",
        "direct": "直接引用",
        "keeps": "维持阻断",
        "loses": "失去阻断",
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
    ax.set_facecolor("white")
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_state_support_chart(text: dict[str, str]) -> None:
    configure_font(text)
    fig, ax = plt.subplots(figsize=(6.2, 3.7), dpi=170)
    fig.patch.set_facecolor("white")
    style_axis(ax)

    ax.plot(GAPS, STATE_SUPPORTS, marker="o", linewidth=2.2, color="#dc2626", label=text["support_label"])
    ax.axhline(0.45, color="#475569", linewidth=1.2, linestyle=(0, (4, 3)), label=text["threshold_label"])
    for gap, value in zip(GAPS, STATE_SUPPORTS):
        ax.text(gap, value + 0.035, f"{value:.3f}".rstrip("0").rstrip("."), ha="center", fontsize=8.5, color="#7f1d1d")

    ax.set_xticks(GAPS)
    ax.set_xlabel(text["gap_label"])
    ax.set_ylabel(text["support_label"])
    ax.set_ylim(0, 0.62)
    ax.legend(frameon=False, loc="upper right", fontsize=8.3)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["support_outfile"], format="png", bbox_inches="tight")
    plt.close(fig)


def save_decision_chart(text: dict[str, str]) -> None:
    configure_font(text)
    x = np.arange(len(GAPS))
    width = 0.34
    state_values = np.array([1 if decision == "keeps block" else 0 for decision in STATE_DECISIONS])
    direct_values = np.array([1 if decision == "keeps block" else 0 for decision in DIRECT_DECISIONS])

    fig, ax = plt.subplots(figsize=(6.2, 3.6), dpi=170)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    bars_state = ax.bar(x - width / 2, state_values, width, color="#dc2626", label=text["state"])
    bars_direct = ax.bar(x + width / 2, direct_values, width, color="#2563eb", label=text["direct"])
    for bars, decisions in ((bars_state, STATE_DECISIONS), (bars_direct, DIRECT_DECISIONS)):
        for bar, decision in zip(bars, decisions):
            label = text["keeps"] if decision == "keeps block" else text["loses"]
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.05,
                label,
                ha="center",
                va="bottom",
                fontsize=8.2,
                color="#111827",
            )

    ax.set_xticks(x)
    ax.set_xticklabels([f"gap={gap}" for gap in GAPS])
    ax.set_ylim(0, 1.25)
    ax.set_yticks([0, 1])
    ax.set_yticklabels([text["loses"], text["keeps"]])
    ax.legend(frameon=False, loc="upper right", fontsize=8.4)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["decision_outfile"], format="png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_state_support_chart(text)
        save_decision_chart(text)


if __name__ == "__main__":
    main()
