import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
MPL_CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))
os.environ.setdefault("XDG_CACHE_HOME", str(MPL_CACHE))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

from p6_17_2_evaluate_failure_recovery import load_reports

OUT_DIR = Path(__file__).resolve().parent

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
        "outfile": "failure-recovery-routing-ko.png",
        "title": "같은 실패도 조건에 따라 복구 경로가 갈라짐",
        "headers": ["실패 신호", "조건", "복구 결정"],
        "rows": [
            ("timeout", "재시도 남음", "재시도"),
            ("timeout", "재시도 소진 + 캐시 있음", "대체 경로"),
            ("timeout", "재시도 소진 + 캐시 없음", "중단·상향"),
            ("위험 실행", "검토자 있음", "승인"),
            ("위험 실행", "검토자 없음", "중단·상향"),
            ("환각", "근거 + 검토자 있음", "사람 검토"),
            ("환각", "근거 없음", "중단·상향"),
        ],
        "case_names": [
            "timeout_retry_search",
            "timeout_fallback_search",
            "timeout_stop_search",
            "risky_action_approval_delete",
            "risky_action_stop_no_reviewer",
            "hallucination_review_grounded",
            "hallucination_stop_ungrounded",
        ],
        "decision_labels": {
            "retry": "재시도",
            "fallback": "대체 경로",
            "approval": "승인",
            "human_review": "사람 검토",
            "stop_and_escalate": "중단·상향",
        },
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "failure-recovery-routing-en.png",
        "title": "The same failure can route differently by condition",
        "headers": ["failure signal", "condition", "recovery decision"],
        "rows": [
            ("timeout", "retry budget left", "retry"),
            ("timeout", "retry exhausted + cache", "fallback"),
            ("timeout", "retry exhausted + no cache", "stop/escalate"),
            ("risky action", "reviewer available", "approval"),
            ("risky action", "no reviewer", "stop/escalate"),
            ("hallucination", "grounding + reviewer", "human review"),
            ("hallucination", "no grounding", "stop/escalate"),
        ],
        "case_names": [
            "timeout_retry_search",
            "timeout_fallback_search",
            "timeout_stop_search",
            "risky_action_approval_delete",
            "risky_action_stop_no_reviewer",
            "hallucination_review_grounded",
            "hallucination_stop_ungrounded",
        ],
        "decision_labels": {
            "retry": "retry",
            "fallback": "fallback",
            "approval": "approval",
            "human_review": "human review",
            "stop_and_escalate": "stop/escalate",
        },
    },
}

DECISION_COLORS = {
    "retry": "#0f766e",
    "fallback": "#64748b",
    "approval": "#f59e0b",
    "human_review": "#9333ea",
    "stop_and_escalate": "#dc2626",
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


def save_chart(text: dict[str, object]) -> None:
    configure_font(text)
    reports = {report["case_name"]: report for report in load_reports()}
    rows = text["rows"]

    fig, ax = plt.subplots(figsize=(10.2, 4.8), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, 3)
    ax.set_ylim(0, len(rows) + 1)
    ax.axis("off")

    col_x = [0.05, 1.02, 2.14]
    col_w = [0.86, 1.02, 0.78]
    header_y = len(rows) + 0.18

    for index, header in enumerate(text["headers"]):
        ax.text(
            col_x[index],
            header_y,
            header,
            fontsize=11,
            fontweight="bold",
            color="#172033",
            va="center",
        )

    for row_index, ((signal, condition, _), case_name) in enumerate(
        zip(rows, text["case_names"])
    ):
        report = reports[case_name]
        y = len(rows) - row_index - 0.55
        fill = "#f8fafc" if row_index % 2 == 0 else "#ffffff"
        ax.add_patch(
            plt.Rectangle(
                (0.0, y - 0.35),
                2.95,
                0.7,
                facecolor=fill,
                edgecolor="#e5e7eb",
                linewidth=0.8,
            )
        )
        decision = report["decision"]
        ax.text(col_x[0], y, signal, fontsize=9.2, color="#172033", va="center")
        ax.text(col_x[1], y, condition, fontsize=9.2, color="#172033", va="center")
        ax.add_patch(
            plt.Rectangle(
                (col_x[2] - 0.02, y - 0.22),
                col_w[2],
                0.44,
                facecolor=DECISION_COLORS[decision],
                edgecolor="none",
            )
        )
        ax.text(
            col_x[2] + 0.04,
            y,
            text["decision_labels"][decision],
            fontsize=9.2,
            color="white",
            va="center",
            fontweight="bold",
        )

    ax.set_title(text["title"], fontsize=12, fontweight="bold", pad=12, color="#111827")

    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
