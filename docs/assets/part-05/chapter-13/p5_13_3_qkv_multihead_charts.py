from __future__ import annotations

from pathlib import Path
import csv
import os

REPO_ROOT = Path(__file__).resolve().parents[4]
MPL_CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager


OUT_DIR = Path(__file__).resolve().parent
DATA_PATH = OUT_DIR / "qkv-multihead-report-scenarios.csv"
FOCUS_REPORT_ID = "ops_pressure_return"
CONTEXT_AXES = [
    ("decision_axis", ["decision_axis"]),
    ("evidence_condition_axis", ["evidence_axis", "condition_axis"]),
]

TEXT = {
    "ko": {
        "font_candidates": [
            "Noto Sans CJK KR",
            "NanumGothic",
            "Apple SD Gothic Neo",
            "AppleGothic",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "scenario_labels": ["균형", "결정/조건 분리", "조건 쏠림"],
        "separation_ylabel": "head_separation",
        "x_label": "결정 축",
        "y_label": "근거/조건 축",
        "single": "싱글 헤드",
        "head1": "헤드 1",
        "head2": "헤드 2",
        "separation_outfile": "qkv-head-separation-ko.png",
        "context_outfile": "qkv-head-context-space-ko.png",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "scenario_labels": ["balanced", "decision/condition", "condition heavy"],
        "separation_ylabel": "head_separation",
        "x_label": "decision axis",
        "y_label": "ground/condition axis",
        "single": "single head",
        "head1": "head 1",
        "head2": "head 2",
        "separation_outfile": "qkv-head-separation-en.png",
        "context_outfile": "qkv-head-context-space-en.png",
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
        "scenario_labels": ["平衡", "决定/条件分离", "条件偏重"],
        "separation_ylabel": "head_separation",
        "x_label": "决定轴",
        "y_label": "依据/条件轴",
        "single": "single head",
        "head1": "head 1",
        "head2": "head 2",
        "separation_outfile": "qkv-head-separation-zh.png",
        "context_outfile": "qkv-head-context-space-zh.png",
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


def load_rows() -> list[dict[str, str]]:
    with DATA_PATH.open(encoding="utf-8", newline="") as f:
        return [
            row
            for row in csv.DictReader(f)
            if row["report_id"] == FOCUS_REPORT_ID
        ]


def scenario_names(rows: list[dict[str, str]]) -> list[str]:
    names = []
    for row in rows:
        if row["scenario"] not in names:
            names.append(row["scenario"])
    return names


def weighted_context(rows: list[dict[str, str]], weight_column: str) -> np.ndarray:
    return np.array(
        [
            sum(
                float(row[weight_column]) * sum(float(row[column]) for column in source_columns)
                for row in rows
            )
            for _, source_columns in CONTEXT_AXES
        ]
    )


def contexts() -> dict[str, dict[str, np.ndarray | float]]:
    rows = load_rows()
    result = {}
    for name in scenario_names(rows):
        scenario_rows = [row for row in rows if row["scenario"] == name]
        single = weighted_context(scenario_rows, "single_weight")
        head1 = weighted_context(scenario_rows, "head1_weight")
        head2 = weighted_context(scenario_rows, "head2_weight")
        result[name] = {
            "single": single,
            "head1": head1,
            "head2": head2,
            "separation": float(np.linalg.norm(head1 - head2)),
        }
    return result


def draw_separation_chart(locale: str, data: dict[str, dict[str, np.ndarray | float]]) -> None:
    text = TEXT[locale]
    configure_font(text)
    labels = text["scenario_labels"]
    values = [scenario["separation"] for scenario in data.values()]
    colors = ["#94a3b8", "#2563eb", "#f97316"]

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    bars = ax.bar(range(len(values)), values, color=colors, width=0.58)
    ax.set_ylabel(text["separation_ylabel"], fontsize=10)
    ax.set_xticks(range(len(values)))
    ax.set_xticklabels(labels, fontsize=8.5)
    ax.set_ylim(0, 1.28)
    ax.grid(axis="y", linestyle="--", alpha=0.28)
    ax.spines[["top", "right"]].set_visible(False)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.035, f"{value:.3f}", ha="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT_DIR / text["separation_outfile"], format="png", bbox_inches="tight", dpi=160)
    plt.close(fig)


def draw_context_chart(locale: str, data: dict[str, dict[str, np.ndarray | float]]) -> None:
    text = TEXT[locale]
    configure_font(text)
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.set_xlabel(text["x_label"], fontsize=10)
    ax.set_ylabel(text["y_label"], fontsize=10)
    ax.set_xlim(0.75, 2.25)
    ax.set_ylim(0.35, 1.35)
    ax.grid(True, linestyle="--", alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)

    marker_by_role = {"single": "o", "head1": "^", "head2": "s"}
    color_by_role = {"single": "#64748b", "head1": "#2563eb", "head2": "#f97316"}
    label_by_role = {"single": text["single"], "head1": text["head1"], "head2": text["head2"]}

    for scenario_index, (name, scenario) in enumerate(data.items()):
        label = text["scenario_labels"][scenario_index]
        for role in ["single", "head1", "head2"]:
            x, y = scenario[role]
            ax.scatter(
                x,
                y,
                marker=marker_by_role[role],
                s=78,
                color=color_by_role[role],
                edgecolor="white",
                linewidth=0.8,
                label=label_by_role[role] if scenario_index == 0 else None,
                zorder=3,
            )
        h1 = scenario["head1"]
        h2 = scenario["head2"]
        ax.plot([h1[0], h2[0]], [h1[1], h2[1]], color="#334155", linewidth=1.1, alpha=0.45)
        midpoint = (h1 + h2) / 2
        ax.text(midpoint[0] + 0.025, midpoint[1] + 0.025, label, fontsize=8.2, color="#334155")

    ax.legend(frameon=False, loc="lower right", fontsize=8.5)
    fig.tight_layout()
    fig.savefig(OUT_DIR / text["context_outfile"], format="png", bbox_inches="tight", dpi=160)
    plt.close(fig)


def main() -> None:
    data = contexts()
    for locale in ["en", "ko", "zh"]:
        draw_separation_chart(locale, data)
        draw_context_chart(locale, data)


if __name__ == "__main__":
    main()
