from pathlib import Path
import csv
import os
from collections import Counter, defaultdict
from typing import Optional

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
CSV_PATH = OUT_DIR / "p6-13-2-function-call-requests.csv"

FUNCTION_SCHEMAS = {
    "create_calendar_event": ["title", "date", "time", "timezone", "attendees"],
    "lookup_exchange_rate": ["base_currency", "quote_currency", "amount"],
    "apply_file_patch": ["file_path", "change_summary"],
    "send_email_draft": ["recipient", "subject", "body"],
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
        "outfile": "function-call-validation-ko.png",
        "status_ylabel": "함수별 호출 수",
        "missing_ylabel": "누락 발생 수",
        "status_labels": ["실행 준비", "되물음 필요", "승인 필요"],
        "function_labels": {
            "create_calendar_event": "일정 생성",
            "lookup_exchange_rate": "환율 조회",
            "apply_file_patch": "파일 패치",
            "send_email_draft": "메일 초안",
        },
        "missing_labels": {
            "attendees": "attendees",
            "timezone": "timezone",
            "time": "time",
            "quote_currency": "quote_currency",
            "base_currency": "base_currency",
            "file_path": "file_path",
            "change_summary": "change_summary",
            "recipient": "recipient",
            "body": "body",
        },
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "function-call-validation-en.png",
        "status_ylabel": "calls by function",
        "missing_ylabel": "missing field count",
        "status_labels": ["ready", "needs clarification", "needs approval"],
        "function_labels": {
            "create_calendar_event": "calendar",
            "lookup_exchange_rate": "exchange",
            "apply_file_patch": "file patch",
            "send_email_draft": "email draft",
        },
        "missing_labels": {
            "attendees": "attendees",
            "timezone": "timezone",
            "time": "time",
            "quote_currency": "quote_currency",
            "base_currency": "base_currency",
            "file_path": "file_path",
            "change_summary": "change_summary",
            "recipient": "recipient",
            "body": "body",
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


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def load_rows() -> list[dict[str, str]]:
    with CSV_PATH.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def is_blank(value: Optional[str]) -> bool:
    return value is None or value.strip() == ""


def validate_row(row: dict[str, str]) -> dict[str, object]:
    required_fields = FUNCTION_SCHEMAS[row["function_name"]]
    missing_fields = [field for field in required_fields if is_blank(row.get(field))]
    approval_required = row["approval_required"].strip().lower() == "true"
    if missing_fields:
        status = "needs_clarification"
    elif approval_required:
        status = "needs_approval"
    else:
        status = "ready"
    return {
        "function_name": row["function_name"],
        "missing_fields": missing_fields,
        "approval_required": approval_required,
        "status": status,
    }


def summarize(rows: list[dict[str, str]]) -> tuple[dict[str, Counter], Counter]:
    status_by_function = defaultdict(Counter)
    missing_counts = Counter()
    for row in rows:
        validation = validate_row(row)
        status_by_function[validation["function_name"]][validation["status"]] += 1
        missing_counts.update(validation["missing_fields"])
    return status_by_function, missing_counts


def save_chart(text: dict[str, str]) -> None:
    configure_font(text)
    rows = load_rows()
    status_by_function, missing_counts = summarize(rows)
    function_names = list(FUNCTION_SCHEMAS.keys())
    status_keys = ["ready", "needs_clarification", "needs_approval"]
    status_colors = ["#0f766e", "#dc2626", "#f59e0b"]
    missing_items = missing_counts.most_common()

    fig, (status_ax, missing_ax) = plt.subplots(
        1,
        2,
        figsize=(11.2, 4.4),
        dpi=180,
        gridspec_kw={"width_ratios": [1.35, 1]},
    )
    fig.patch.set_facecolor("white")
    for ax in (status_ax, missing_ax):
        ax.set_facecolor("white")
        style_axis(ax)

    x_positions = range(len(function_names))
    bottoms = [0] * len(function_names)
    for status_key, label, color in zip(status_keys, text["status_labels"], status_colors):
        values = [status_by_function[name][status_key] for name in function_names]
        bars = status_ax.bar(x_positions, values, bottom=bottoms, label=label, color=color, width=0.58)
        for index, bar in enumerate(bars):
            value = values[index]
            if value == 0:
                continue
            status_ax.annotate(
                f"{value:g}",
                (bar.get_x() + bar.get_width() / 2, bottoms[index] + value / 2),
                ha="center",
                va="center",
                fontsize=8.5,
                color="white" if color != "#f59e0b" else "#172033",
            )
        bottoms = [bottom + value for bottom, value in zip(bottoms, values)]

    status_ax.set_xticks(list(x_positions))
    status_ax.set_xticklabels([text["function_labels"][name] for name in function_names])
    status_ax.set_ylabel(text["status_ylabel"])
    status_ax.set_ylim(0, max(bottoms) + 1.5)
    status_ax.legend(loc="upper left", frameon=False, ncols=1)

    missing_labels = [text["missing_labels"].get(field, field) for field, _ in missing_items]
    missing_values = [value for _, value in missing_items]
    bars = missing_ax.barh(missing_labels, missing_values, color="#2563eb", height=0.56)
    for bar, value in zip(bars, missing_values):
        missing_ax.annotate(
            f"{value:g}",
            (bar.get_width(), bar.get_y() + bar.get_height() / 2),
            textcoords="offset points",
            xytext=(6, 0),
            ha="left",
            va="center",
            fontsize=9,
            color="#172033",
        )
    missing_ax.set_xlabel(text["missing_ylabel"])
    missing_ax.set_xlim(0, max(missing_values) + 1 if missing_values else 1)
    missing_ax.invert_yaxis()
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
