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
CSV_PATH = OUT_DIR / "p6-8-2-adaptation-portfolio.csv"

BASE_MODEL_PARAMS = 7_000_000_000
FULL_FINETUNING_TRAINABLE_PER_TASK = 7_000_000_000
LORA_TRAINABLE_PER_TASK = 8_000_000
BYTES_PER_PARAM = 2

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
        "outfile": "lora-storage-growth-ko.png",
        "full_title": "전체 파인튜닝",
        "lora_title": "LoRA 조정본",
        "xlabel": "월간 추가 저장 크기(GB)",
        "full_label": "전체 파인튜닝",
        "lora_label": "LoRA 조정본",
        "total_prefix": "월간 합계",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "lora-storage-growth-en.png",
        "full_title": "full fine-tuning",
        "lora_title": "LoRA adapters",
        "xlabel": "monthly extra storage (GB)",
        "full_label": "full fine-tuning",
        "lora_label": "LoRA adapters",
        "total_prefix": "monthly total",
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK",
            "PingFang SC",
            "Songti SC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "lora-storage-growth-zh.png",
        "full_title": "全量微调",
        "lora_title": "LoRA 调整件",
        "xlabel": "月度额外存储大小(GB)",
        "full_label": "全量微调",
        "lora_label": "LoRA 调整件",
        "total_prefix": "月度合计",
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


def to_gb(param_count: int) -> float:
    return param_count * BYTES_PER_PARAM / (1024**3)


def collect_rows() -> list[dict[str, object]]:
    team_summary: dict[str, dict[str, int]] = {}
    with CSV_PATH.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            team = row["team"]
            monthly_experiments = int(row["monthly_experiments"])
            summary = team_summary.setdefault(team, {"task_count": 0, "monthly_runs": 0})
            summary["task_count"] += 1
            summary["monthly_runs"] += monthly_experiments

    rows: list[dict[str, float | int | str]] = []
    for team, summary in team_summary.items():
        monthly_runs = summary["monthly_runs"]
        rows.append(
            {
                "team": team,
                "task_count": summary["task_count"],
                "monthly_runs": monthly_runs,
                "full_storage_gb": to_gb(
                    FULL_FINETUNING_TRAINABLE_PER_TASK * monthly_runs
                ),
                "lora_storage_gb": to_gb(LORA_TRAINABLE_PER_TASK * monthly_runs),
            }
        )
    return sorted(rows, key=lambda row: row["monthly_runs"], reverse=True)


def style_axis(ax) -> None:
    ax.grid(True, axis="x", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_chart(text: dict[str, str]) -> None:
    configure_font(text)
    rows = collect_rows()
    teams = [str(row["team"]) for row in rows]
    full_values = [float(row["full_storage_gb"]) for row in rows]
    lora_values = [float(row["lora_storage_gb"]) for row in rows]
    monthly_runs = [int(row["monthly_runs"]) for row in rows]
    y_values = list(range(len(rows)))

    fig, (full_ax, lora_ax) = plt.subplots(
        ncols=2,
        sharey=True,
        figsize=(9.2, 4.8),
        dpi=180,
        gridspec_kw={"width_ratios": [3.2, 1.45], "wspace": 0.08},
    )
    fig.patch.set_facecolor("white")
    for ax in (full_ax, lora_ax):
        ax.set_facecolor("white")
        style_axis(ax)

    full_ax.barh(
        y_values,
        full_values,
        height=0.62,
        color="#dc2626",
        alpha=0.88,
    )
    lora_ax.barh(
        y_values,
        lora_values,
        height=0.62,
        color="#16a34a",
        alpha=0.88,
    )

    full_ax.set_yticks(y_values)
    full_ax.set_yticklabels(
        [f"{team} ({runs})" for team, runs in zip(teams, monthly_runs)]
    )
    full_ax.invert_yaxis()
    full_ax.set_title(text["full_title"], fontsize=12, pad=8)
    lora_ax.set_title(text["lora_title"], fontsize=12, pad=8)
    full_ax.set_xlabel(text["xlabel"])
    lora_ax.set_xlabel(text["xlabel"])
    full_ax.set_xlim(0, max(full_values) * 1.18)
    lora_ax.set_xlim(0, max(lora_values) * 1.45)

    for y, value in zip(y_values, full_values):
        full_ax.text(
            value + max(full_values) * 0.018,
            y,
            f"{value:.1f}",
            va="center",
            ha="left",
            fontsize=8.5,
            color="#172033",
        )
    for y, value in zip(y_values, lora_values):
        lora_ax.text(
            value + max(lora_values) * 0.045,
            y,
            f"{value:.2f}",
            va="center",
            ha="left",
            fontsize=8.5,
            color="#172033",
        )

    total_full = sum(full_values)
    total_lora = sum(lora_values)
    fig.text(
        0.5,
        0.018,
        f"{text['total_prefix']}: full {total_full:.1f} GB / LoRA {total_lora:.2f} GB",
        ha="center",
        fontsize=10,
        color="#172033",
    )
    fig.subplots_adjust(left=0.18, right=0.985, bottom=0.17, top=0.88, wspace=0.08)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    _ = BASE_MODEL_PARAMS
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
