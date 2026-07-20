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
import numpy as np

OUT_DIR = Path(__file__).resolve().parent
CSV_PATH = OUT_DIR / "long-dependency-instruction-log.csv"
DECAY = 0.72
SUPPORT_THRESHOLD = 0.45

LANG_LABELS = {
    "ko": {
        "support_label": "상태 기반 핵심 단서 최소값",
        "threshold_label": "차단 유지 기준",
        "xlabel": "중간 설명 줄 수(gap)",
        "ylabel": "상태 기반 핵심 단서 최소값",
        "state_label": "상태 기반",
        "direct_label": "직접 참조",
        "keeps": "차단 유지",
        "loses": "차단 상실",
        "state_support_file": "long-dependency-csv-state-support-ko.png",
        "decision_file": "long-dependency-csv-decision-comparison-ko.png",
    },
    "en": {
        "support_label": "minimum key-cue value in state",
        "threshold_label": "block-retention threshold",
        "xlabel": "middle explanation lines (gap)",
        "ylabel": "minimum key-cue value in state",
        "state_label": "state-based",
        "direct_label": "direct reference",
        "keeps": "keeps block",
        "loses": "loses block",
        "state_support_file": "long-dependency-csv-state-support-en.png",
        "decision_file": "long-dependency-csv-decision-comparison-en.png",
    },
    "zh": {
        "support_label": "状态中的关键线索最小值",
        "threshold_label": "维持阻断阈值",
        "xlabel": "中间说明行数（gap）",
        "ylabel": "状态中的关键线索最小值",
        "state_label": "基于状态",
        "direct_label": "直接引用",
        "keeps": "维持阻断",
        "loses": "失去阻断",
        "state_support_file": "long-dependency-csv-state-support-zh.png",
        "decision_file": "long-dependency-csv-decision-comparison-zh.png",
    },
}


def choose_font() -> str:
    candidates = [
        "Noto Sans CJK KR",
        "NanumGothic",
        "Arial Unicode MS",
        "Songti SC",
        "Heiti TC",
        "Apple SD Gothic Neo",
        "AppleGothic",
        "DejaVu Sans",
    ]
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def load_documents() -> dict[str, list[dict[str, str]]]:
    documents: dict[str, list[dict[str, str]]] = {}
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            documents.setdefault(row["document_id"], []).append(row)
    for rows in documents.values():
        rows.sort(key=lambda row: int(row["line_no"]))
    return dict(sorted(documents.items(), key=lambda item: int(item[1][0]["gap"])))


def sequential_state(rows: list[dict[str, str]], decay: float = DECAY) -> tuple[dict[str, float], float, str]:
    state = {"restart": 0.0, "blocked": 0.0, "pressure": 0.0}
    for row in rows:
        lowered = row["text"].lower()
        for key in state:
            state[key] *= decay
        if "restart" in lowered:
            state["restart"] += 1.0
        if "blocked" in lowered:
            state["blocked"] += 1.0
        if "pressure" in lowered or "vented" in lowered:
            state["pressure"] += 1.0
    support = round(min(state.values()), 3)
    decision = "keeps block" if support >= SUPPORT_THRESHOLD else "loses block"
    return {key: round(value, 3) for key, value in state.items()}, support, decision


def direct_reference(rows: list[dict[str, str]]) -> tuple[int, str]:
    best_score = 0
    for row in rows:
        if row["role"] == "question":
            continue
        lowered = row["text"].lower()
        score = sum(1 for keyword in ["restart", "blocked", "pressure"] if keyword in lowered)
        best_score = max(best_score, score)
    decision = "keeps block" if best_score == 3 else "loses block"
    return best_score, decision


def build_outputs() -> tuple[np.ndarray, np.ndarray, list[str], list[str]]:
    documents = load_documents()
    gaps = []
    supports = []
    state_decisions = []
    direct_decisions = []
    for rows in documents.values():
        gaps.append(int(rows[0]["gap"]))
        _, support, state_decision = sequential_state(rows)
        _, direct_decision = direct_reference(rows)
        supports.append(support)
        state_decisions.append(state_decision)
        direct_decisions.append(direct_decision)
    return np.array(gaps), np.array(supports), state_decisions, direct_decisions


def configure_font() -> None:
    plt.rcParams["font.family"] = choose_font()
    plt.rcParams["axes.unicode_minus"] = False


def style_axis(ax) -> None:
    ax.set_facecolor("white")
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_state_support_chart(gaps: np.ndarray, supports: np.ndarray, labels: dict[str, str]) -> None:
    configure_font()
    fig, ax = plt.subplots(figsize=(6.4, 3.8), dpi=170)
    fig.patch.set_facecolor("white")
    style_axis(ax)

    ax.plot(gaps, supports, marker="o", linewidth=2.2, color="#dc2626", label=labels["support_label"])
    ax.axhline(SUPPORT_THRESHOLD, color="#475569", linewidth=1.2, linestyle=(0, (4, 3)), label=labels["threshold_label"])
    for gap, value in zip(gaps, supports):
        ax.text(gap, value + 0.035, f"{value:.3f}".rstrip("0").rstrip("."), ha="center", fontsize=8.5, color="#7f1d1d")

    ax.set_xticks(gaps)
    ax.set_xlabel(labels["xlabel"])
    ax.set_ylabel(labels["ylabel"])
    ax.set_ylim(0, 0.62)
    ax.legend(frameon=False, loc="upper right", fontsize=8.3)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / labels["state_support_file"], format="png", bbox_inches="tight")
    plt.close(fig)


def save_decision_chart(gaps: np.ndarray, state_decisions: list[str], direct_decisions: list[str], labels: dict[str, str]) -> None:
    configure_font()
    x = np.arange(len(gaps))
    width = 0.34
    state_values = np.array([1 if decision == "keeps block" else 0 for decision in state_decisions])
    direct_values = np.array([1 if decision == "keeps block" else 0 for decision in direct_decisions])

    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=170)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    bars_state = ax.bar(x - width / 2, state_values, width, color="#dc2626", label=labels["state_label"])
    bars_direct = ax.bar(x + width / 2, direct_values, width, color="#2563eb", label=labels["direct_label"])
    for bars, decisions, y_offset in ((bars_state, state_decisions, 0.05), (bars_direct, direct_decisions, 0.13)):
        for bar, decision in zip(bars, decisions):
            label = labels["keeps"] if decision == "keeps block" else labels["loses"]
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + y_offset, label, ha="center", va="bottom", fontsize=8.0, color="#111827")

    ax.set_xticks(x)
    ax.set_xticklabels([f"gap={gap}" for gap in gaps])
    ax.set_ylim(0, 1.35)
    ax.set_yticks([0, 1])
    ax.set_yticklabels([labels["loses"], labels["keeps"]])
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, fontsize=8.4)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / labels["decision_file"], format="png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    gaps, supports, state_decisions, direct_decisions = build_outputs()
    for labels in LANG_LABELS.values():
        save_state_support_chart(gaps, supports, labels)
        save_decision_chart(gaps, state_decisions, direct_decisions, labels)


if __name__ == "__main__":
    main()
