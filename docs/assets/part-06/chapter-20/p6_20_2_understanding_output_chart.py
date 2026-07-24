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
LANG_TEXT = {
    "ko": {
        "csv_path": OUT_DIR / "p6-20-understanding-task-cases.csv",
        "font_candidates": [
            "Noto Sans CJK KR",
            "NanumGothic",
            "Apple SD Gothic Neo",
            "AppleGothic",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "understanding-output-types-ko.png",
        "ylabel": "사례 수",
        "task_labels": ["분류", "문장쌍", "검색 랭킹"],
        "output_labels": ["라벨", "점수", "순위"],
        "task_title": "태스크별 입력 사례",
        "output_title": "출력 형식별 등장",
    },
    "en": {
        "csv_path": OUT_DIR / "p6-20-understanding-task-cases-en.csv",
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "understanding-output-types-en.png",
        "ylabel": "cases",
        "task_labels": ["classification", "pair relation", "ranking"],
        "output_labels": ["label", "score", "rank"],
        "task_title": "input cases by task",
        "output_title": "judgment output forms",
    },
    "zh": {
        "csv_path": OUT_DIR / "p6-20-understanding-task-cases-zh.csv",
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK TC",
            "PingFang SC",
            "Heiti SC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "understanding-output-types-zh.png",
        "ylabel": "案例数",
        "task_labels": ["分类", "句子对", "搜索排序"],
        "output_labels": ["标签", "分数", "排名"],
        "task_title": "按任务划分的输入案例",
        "output_title": "判断输出形式",
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


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def read_cases(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def summarize_outputs(csv_path: Path) -> dict[str, list[int]]:
    cases = read_cases(csv_path)
    task_order = ["classification", "pair_relation", "ranking"]
    task_counts = [sum(row["task_type"] == task for row in cases) for task in task_order]

    output_counts = {
        "label": 0,
        "score": 0,
        "rank": 0,
    }
    for row in cases:
        if row["task_type"] == "classification":
            output_counts["label"] += 1
            output_counts["score"] += 1
        elif row["task_type"] == "pair_relation":
            output_counts["label"] += 1
            output_counts["score"] += 1
        elif row["task_type"] == "ranking":
            output_counts["score"] += 1
            output_counts["rank"] += 1

    return {
        "task_counts": task_counts,
        "output_counts": [
            output_counts["label"],
            output_counts["score"],
            output_counts["rank"],
        ],
    }


def annotate_bars(bars) -> None:
    for bar in bars:
        value = bar.get_height()
        if value == 0:
            continue
        bar.axes.annotate(
            f"{value:g}",
            (bar.get_x() + bar.get_width() / 2, value),
            textcoords="offset points",
            xytext=(0, 7),
            ha="center",
            fontsize=8.7,
            color="#172033",
        )


def save_chart(text: dict[str, object]) -> None:
    configure_font(text)
    summary = summarize_outputs(text["csv_path"])

    fig, (task_ax, output_ax) = plt.subplots(
        1,
        2,
        figsize=(9.0, 3.9),
        dpi=180,
        gridspec_kw={"width_ratios": [1.2, 1]},
    )
    fig.patch.set_facecolor("white")

    for ax in (task_ax, output_ax):
        ax.set_facecolor("white")
        style_axis(ax)

    task_bars = task_ax.bar(
        text["task_labels"],
        summary["task_counts"],
        color=["#0f766e", "#2563eb", "#f59e0b"],
        width=0.52,
    )
    annotate_bars(task_bars)
    task_ax.set_title(text["task_title"], fontsize=10, pad=8)
    task_ax.set_ylabel(text["ylabel"])
    task_ax.set_ylim(0, max(summary["task_counts"]) * 1.35)

    output_bars = output_ax.bar(
        text["output_labels"],
        summary["output_counts"],
        color=["#0f766e", "#2563eb", "#f59e0b"],
        width=0.52,
    )
    annotate_bars(output_bars)
    output_ax.set_title(text["output_title"], fontsize=10, pad=8)
    output_ax.set_ylabel(text["ylabel"])
    output_ax.set_ylim(0, max(summary["output_counts"]) * 1.25)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
