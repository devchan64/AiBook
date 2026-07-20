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


def choose_font() -> str:
    candidates = ["Noto Sans CJK KR", "NanumGothic", "Apple SD Gothic Neo", "AppleGothic", "Arial Unicode MS", "DejaVu Sans"]
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


def save_state_support_chart(gaps: np.ndarray, supports: np.ndarray) -> None:
    configure_font()
    fig, ax = plt.subplots(figsize=(6.4, 3.8), dpi=170)
    fig.patch.set_facecolor("white")
    style_axis(ax)

    ax.plot(gaps, supports, marker="o", linewidth=2.2, color="#dc2626", label="상태 기반 핵심 단서 최소값")
    ax.axhline(SUPPORT_THRESHOLD, color="#475569", linewidth=1.2, linestyle=(0, (4, 3)), label="차단 유지 기준")
    for gap, value in zip(gaps, supports):
        ax.text(gap, value + 0.035, f"{value:.3f}".rstrip("0").rstrip("."), ha="center", fontsize=8.5, color="#7f1d1d")

    ax.set_xticks(gaps)
    ax.set_xlabel("중간 설명 줄 수(gap)")
    ax.set_ylabel("상태 기반 핵심 단서 최소값")
    ax.set_ylim(0, 0.62)
    ax.legend(frameon=False, loc="upper right", fontsize=8.3)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / "long-dependency-csv-state-support-ko.png", format="png", bbox_inches="tight")
    plt.close(fig)


def save_decision_chart(gaps: np.ndarray, state_decisions: list[str], direct_decisions: list[str]) -> None:
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

    bars_state = ax.bar(x - width / 2, state_values, width, color="#dc2626", label="상태 기반")
    bars_direct = ax.bar(x + width / 2, direct_values, width, color="#2563eb", label="직접 참조")
    for bars, decisions in ((bars_state, state_decisions), (bars_direct, direct_decisions)):
        for bar, decision in zip(bars, decisions):
            label = "차단 유지" if decision == "keeps block" else "차단 상실"
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05, label, ha="center", va="bottom", fontsize=8.0, color="#111827")

    ax.set_xticks(x)
    ax.set_xticklabels([f"gap={gap}" for gap in gaps])
    ax.set_ylim(0, 1.25)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["차단 상실", "차단 유지"])
    ax.legend(frameon=False, loc="upper right", fontsize=8.4)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / "long-dependency-csv-decision-comparison-ko.png", format="png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    gaps, supports, state_decisions, direct_decisions = build_outputs()
    save_state_support_chart(gaps, supports)
    save_decision_chart(gaps, state_decisions, direct_decisions)


if __name__ == "__main__":
    main()
