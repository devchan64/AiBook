from pathlib import Path
import os
import random
import numpy as np
from sklearn.neighbors import NearestNeighbors

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

QUERY = [0.90, 0.80]
QUERY_ARRAY = np.array([QUERY])
SETTINGS = {
    "wide": 0.20,
    "balanced": 0.08,
    "aggressive": 0.04,
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
        "outfile": "ann-window-tradeoff-ko.png",
        "xlabel": "coarse_window 설정",
        "candidate_ylabel": "실제 비교 후보 수",
        "recall_ylabel": "recall@5",
        "candidate_label": "비교 후보 수",
        "recall_label": "recall@5",
        "setting_labels": {
            "wide": "넓음",
            "balanced": "균형",
            "aggressive": "공격적",
        },
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "ann-window-tradeoff-en.png",
        "xlabel": "coarse_window setting",
        "candidate_ylabel": "candidates compared",
        "recall_ylabel": "recall@5",
        "candidate_label": "candidates",
        "recall_label": "recall@5",
        "setting_labels": {
            "wide": "wide",
            "balanced": "balanced",
            "aggressive": "aggressive",
        },
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK TC",
            "PingFang SC",
            "Songti SC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "ann-window-tradeoff-zh.png",
        "xlabel": "coarse_window 设置",
        "candidate_ylabel": "实际比较候选数",
        "recall_ylabel": "recall@5",
        "candidate_label": "比较候选数",
        "recall_label": "recall@5",
        "setting_labels": {
            "wide": "宽",
            "balanced": "平衡",
            "aggressive": "激进",
        },
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


def build_docs() -> dict[str, list[float]]:
    random.seed(24)
    docs = {
        "refund_policy": [0.88, 0.82],
        "cancel_payment": [0.845, 0.79],
        "refund_exception": [0.83, 0.86],
        "billing_deadline": [0.94, 0.76],
        "payment_receipt": [0.96, 0.83],
        "change_address": [0.30, 0.20],
        "shipping_delay": [0.40, 0.35],
    }
    categories = ["login", "shipping", "coupon", "profile", "notice"]
    for i in range(3000):
        docs[f"{random.choice(categories)}_{i:04d}"] = [
            random.random(),
            random.random() * 0.45,
        ]
    return docs


def rank_with_neighbors(names: list[str], vectors: list[list[float]], k: int = 5) -> list[str]:
    model = NearestNeighbors(n_neighbors=min(k, len(names)), metric="euclidean")
    model.fit(np.array(vectors))
    _, indices = model.kneighbors(QUERY_ARRAY)
    return [names[index] for index in indices[0]]


def summarize_windows(text: dict[str, str]) -> list[dict[str, float]]:
    docs = build_docs()
    full_top5 = rank_with_neighbors(list(docs), list(docs.values()))

    summaries = []
    for label, window in SETTINGS.items():
        coarse_candidates = [
            (name, vec) for name, vec in docs.items() if abs(vec[0] - QUERY[0]) <= window
        ]
        top5 = rank_with_neighbors(
            [name for name, _ in coarse_candidates],
            [vec for _, vec in coarse_candidates],
        )
        recall = len(set(full_top5) & set(top5)) / len(full_top5)
        summaries.append(
            {
                "label": f"{label}\n({window:g})",
                "display_label": f"{text['setting_labels'][label]}\n({window:g})",
                "candidates": len(coarse_candidates),
                "recall": recall,
            }
        )
    return summaries


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)


def save_tradeoff_chart(text: dict[str, str]) -> None:
    configure_font(text)
    summaries = summarize_windows(text)
    labels = [row["display_label"] for row in summaries]
    candidates = [row["candidates"] for row in summaries]
    recalls = [row["recall"] for row in summaries]
    x_positions = range(len(labels))

    fig, ax_candidates = plt.subplots(figsize=(6.6, 3.8), dpi=180)
    fig.patch.set_facecolor("white")
    ax_candidates.set_facecolor("white")
    style_axis(ax_candidates)

    bars = ax_candidates.bar(
        x_positions,
        candidates,
        color="#2563eb",
        width=0.52,
        label=text["candidate_label"],
    )
    for bar, value in zip(bars, candidates):
        ax_candidates.annotate(
            f"{value:g}",
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            textcoords="offset points",
            xytext=(0, -15),
            ha="center",
            va="top",
            fontsize=9,
            color="white",
        )

    ax_candidates.set_xticks(list(x_positions), labels)
    ax_candidates.set_xlabel(text["xlabel"])
    ax_candidates.set_ylabel(text["candidate_ylabel"])
    ax_candidates.set_ylim(0, max(candidates) * 1.22)

    ax_recall = ax_candidates.twinx()
    ax_recall.plot(
        list(x_positions),
        recalls,
        color="#dc2626",
        marker="o",
        linewidth=2.2,
        label=text["recall_label"],
    )
    for x, value in zip(x_positions, recalls):
        ax_recall.annotate(
            f"{value:.1f}",
            (x, value),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=9,
            color="#7f1d1d",
        )
    ax_recall.set_ylabel(text["recall_ylabel"])
    ax_recall.set_ylim(0, 1.12)
    ax_recall.spines["top"].set_visible(False)

    handles_1, labels_1 = ax_candidates.get_legend_handles_labels()
    handles_2, labels_2 = ax_recall.get_legend_handles_labels()
    ax_candidates.legend(
        handles_1 + handles_2,
        labels_1 + labels_2,
        loc="upper right",
        frameon=False,
        fontsize=9,
    )

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_tradeoff_chart(text)


if __name__ == "__main__":
    main()
