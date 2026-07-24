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
LOG_PATH = OUT_DIR / "p6-10-1-prompt-response-log.csv"

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
        "outfile": "prompt-structure-check-ko.png",
        "ylabel_template": "통과한 응답 로그 수({run_count}회 중)",
        "simple_label": "단순 프롬프트",
        "instruction_context_label": "지시+맥락",
        "instruction_context_example_label": "지시+맥락+예시",
        "instruction_context_example_check_label": "지시+맥락+예시+점검",
        "labels": ["번호 형식", "필수 슬롯", "핵심 키워드"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "prompt-structure-check-en.png",
        "ylabel_template": "passed response logs(out of {run_count})",
        "simple_label": "simple prompt",
        "instruction_context_label": "instruction+context",
        "instruction_context_example_label": "instruction+context+example",
        "instruction_context_example_check_label": "instruction+context+example+check",
        "labels": ["numbered format", "required slots", "key facts"],
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK TC",
            "PingFang SC",
            "Microsoft YaHei",
            "SimHei",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "prompt-structure-check-zh.png",
        "ylabel_template": "通过的响应日志数(共 {run_count} 次)",
        "simple_label": "简单提示",
        "instruction_context_label": "指令+上下文",
        "instruction_context_example_label": "指令+上下文+示例",
        "instruction_context_example_check_label": "指令+上下文+示例+检查",
        "labels": ["编号格式", "必需槽位", "关键事实"],
    },
}

PROMPT_ORDER = [
    "simple",
    "instruction_context",
    "instruction_context_example",
    "instruction_context_example_check",
]


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
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def to_bool(value: str) -> bool:
    return value.lower() == "true"


def read_logs() -> list[dict[str, object]]:
    with LOG_PATH.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    for row in rows:
        row["line_count"] = int(row["line_count"])
        row["slot_count"] = int(row["slot_count"])
        row["keyword_hits"] = int(row["keyword_hits"])
        row["keyword_total"] = int(row["keyword_total"])
        row["numbered_lines"] = to_bool(row["numbered_lines"])
    return rows


def summarize(rows: list[dict[str, object]]) -> dict[str, dict[str, int]]:
    summary = {}
    for prompt_type in sorted({row["prompt_type"] for row in rows}):
        group = [row for row in rows if row["prompt_type"] == prompt_type]
        summary[prompt_type] = {
            "run_count": len(group),
            "format_ok_count": sum(
                row["numbered_lines"] and row["line_count"] == 3
                for row in group
            ),
            "slot_ok_count": sum(row["slot_count"] == 3 for row in group),
            "full_keyword_keep_count": sum(
                row["keyword_hits"] == row["keyword_total"]
                for row in group
            ),
        }
    return summary


def save_chart(text: dict[str, str]) -> None:
    configure_font(text)
    rows = read_logs()
    summary = summarize(rows)
    present_prompt_order = [
        prompt_type for prompt_type in PROMPT_ORDER
        if prompt_type in summary
    ]
    labels = text["labels"]
    values_by_prompt = {
        prompt_type: [
            summary[prompt_type]["format_ok_count"],
            summary[prompt_type]["slot_ok_count"],
            summary[prompt_type]["full_keyword_keep_count"],
        ]
        for prompt_type in present_prompt_order
    }
    max_run_count = max(values["run_count"] for values in summary.values())
    x_positions = list(range(len(labels)))
    bar_width = min(0.18, 0.75 / len(present_prompt_order))

    fig, ax = plt.subplots(figsize=(6.8, 3.9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    bars_list = []
    colors = {
        "simple": "#64748b",
        "instruction_context": "#0f766e",
        "instruction_context_example": "#2563eb",
        "instruction_context_example_check": "#9333ea",
    }
    center_offset = (len(present_prompt_order) - 1) / 2
    offsets = {
        prompt_type: (index - center_offset) * bar_width
        for index, prompt_type in enumerate(present_prompt_order)
    }
    for prompt_type in present_prompt_order:
        bars = ax.bar(
            [x + offsets[prompt_type] for x in x_positions],
            values_by_prompt[prompt_type],
            width=bar_width,
            color=colors[prompt_type],
            label=text[f"{prompt_type}_label"],
        )
        bars_list.append(bars)

    for bars in bars_list:
        for bar in bars:
            value = bar.get_height()
            ax.annotate(
                f"{value:g}",
                (bar.get_x() + bar.get_width() / 2, value),
                textcoords="offset points",
                xytext=(0, 6),
                ha="center",
                fontsize=9,
                color="#172033",
            )

    ax.set_xticks(x_positions)
    ax.set_xticklabels(labels)
    ax.set_ylabel(text["ylabel_template"].format(run_count=max_run_count))
    ax.set_ylim(0, max_run_count * 1.2)
    ax.legend(
        frameon=False,
        loc="lower left",
        bbox_to_anchor=(0, 1.02),
        ncol=3,
        borderaxespad=0,
    )
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
