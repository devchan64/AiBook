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
CSV_PATH = OUT_DIR / "p6-19-lineage-items.csv"

LINEAGE_RULES = {
    "direct_domains": {"language"},
    "direct_targets": {
        "next_token",
        "representation",
        "sequence_alignment",
        "sequence_modeling",
    },
    "requires_transformer_connection": True,
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
        "outfile": "lineage-rule-check-matrix-ko.png",
        "ylabel": "항목 수",
        "criterion_labels": ["언어 도메인", "LLM 목표", "Transformer 연결"],
        "group_labels": ["직접 계보", "주변 근거"],
        "criterion_title": "기준별 통과 수",
        "group_title": "최종 분류 수",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "lineage-rule-check-matrix-en.png",
        "ylabel": "items",
        "criterion_labels": ["language domain", "LLM target", "Transformer link"],
        "group_labels": ["direct lineage", "surrounding evidence"],
        "criterion_title": "passed criteria",
        "group_title": "final classes",
    },
}


def read_items() -> list[dict[str, object]]:
    items = []
    with CSV_PATH.open(encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            items.append(
                {
                    "name": row["name"],
                    "domain": row["domain"],
                    "target": row["target"],
                    "connects_to_transformer_llm": (
                        row["connects_to_transformer_llm"].lower() == "true"
                    ),
                }
            )
    return items


def classify(item: dict[str, object]) -> tuple[str, dict[str, bool]]:
    domain_ok = item["domain"] in LINEAGE_RULES["direct_domains"]
    target_ok = item["target"] in LINEAGE_RULES["direct_targets"]
    connection_ok = (
        item["connects_to_transformer_llm"]
        if LINEAGE_RULES["requires_transformer_connection"]
        else True
    )
    checks = {
        "domain_ok": domain_ok,
        "target_ok": target_ok,
        "connection_ok": connection_ok,
    }
    label = "direct_lineage" if all(checks.values()) else "surrounding_evidence"
    return label, checks


def summarize() -> dict[str, object]:
    items = read_items()
    labels = []
    checks = []
    for item in items:
        label, item_checks = classify(item)
        labels.append(label)
        checks.append(item_checks)
    return {
        "item_count": len(items),
        "criterion_counts": [
            sum(item["domain_ok"] for item in checks),
            sum(item["target_ok"] for item in checks),
            sum(item["connection_ok"] for item in checks),
        ],
        "group_counts": [
            labels.count("direct_lineage"),
            labels.count("surrounding_evidence"),
        ],
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


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def annotate_bars(bars) -> None:
    for bar in bars:
        value = bar.get_height()
        bar.axes.annotate(
            f"{value:g}",
            (bar.get_x() + bar.get_width() / 2, value),
            textcoords="offset points",
            xytext=(0, 6),
            ha="center",
            fontsize=9,
            color="#172033",
        )


def save_chart(text: dict[str, object]) -> None:
    configure_font(text)
    summary = summarize()
    fig, (criteria_ax, group_ax) = plt.subplots(
        1,
        2,
        figsize=(9.0, 3.9),
        dpi=180,
        gridspec_kw={"width_ratios": [1.6, 1]},
    )
    fig.patch.set_facecolor("white")

    for ax in (criteria_ax, group_ax):
        ax.set_facecolor("white")
        style_axis(ax)

    criterion_bars = criteria_ax.bar(
        text["criterion_labels"],
        summary["criterion_counts"],
        color=["#0f766e", "#2563eb", "#9333ea"],
        width=0.54,
    )
    annotate_bars(criterion_bars)
    criteria_ax.set_title(text["criterion_title"], fontsize=10, pad=8)
    criteria_ax.set_ylabel(text["ylabel"])
    criteria_ax.set_ylim(0, max(summary["criterion_counts"]) * 1.28)

    group_bars = group_ax.bar(
        text["group_labels"],
        summary["group_counts"],
        color=["#0f766e", "#64748b"],
        width=0.52,
    )
    annotate_bars(group_bars)
    group_ax.set_title(text["group_title"], fontsize=10, pad=8)
    group_ax.set_ylabel(text["ylabel"])
    group_ax.set_ylim(0, max(summary["group_counts"]) * 1.28)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
