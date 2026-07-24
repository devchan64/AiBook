from pathlib import Path
import json
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
        "font_candidates": [
            "Noto Sans CJK KR",
            "NanumGothic",
            "Apple SD Gothic Neo",
            "AppleGothic",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "harness-run-issue-split-ko.png",
        "ylabel": "기록된 항목 수",
        "labels": ["최종 답", "관측 기록", "모델 판단", "도구 계약", "승인 gate", "replay 비교"],
        "legend": ["답변만 저장", "로컬 모델 실행 기록"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "harness-run-issue-split-en.png",
        "ylabel": "retained record items",
        "labels": ["answer", "observations", "model decision", "tool contracts", "approval gate", "replay compare"],
        "legend": ["answer only", "local model run record"],
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK",
            "PingFang SC",
            "Heiti SC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "harness-run-issue-split-zh.png",
        "ylabel": "保留记录项数",
        "labels": ["最终回答", "观察记录", "模型判断", "工具契约", "批准 gate", "replay 比较"],
        "legend": ["只保存回答", "本地模型执行记录"],
    },
}

ARTIFACT_DIR = REPO_ROOT / ".tmp" / "p6-15-2-harness-runs"
FALLBACK_WITHOUT_HARNESS = [1, 0, 0, 0, 0, 0]
FALLBACK_WITH_HARNESS = [1, 8, 1, 2, 1, 1]


def load_run_artifact(run_id: str) -> dict | None:
    path = ARTIFACT_DIR / f"{run_id}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def chart_values() -> tuple[list[int], list[int]]:
    try:
        first_run = load_run_artifact("refund-support-run-001")
        second_run = load_run_artifact("refund-support-run-002")
        if first_run is None:
            return FALLBACK_WITHOUT_HARNESS, FALLBACK_WITH_HARNESS

        observations = first_run["observations"]
        tool_contract_event = next(event for event in observations if event["event"] == "tool_contracts")
        local_model_run = [
            1,
            first_run["run_report"]["observation_count"],
            sum(event["event"] == "model_decision" for event in observations),
            len(tool_contract_event["value"]),
            sum(event["event"] == "approval_gate" for event in observations),
            1 if second_run is not None else 0,
        ]
        return FALLBACK_WITHOUT_HARNESS, local_model_run
    except (KeyError, StopIteration, TypeError):
        return FALLBACK_WITHOUT_HARNESS, FALLBACK_WITH_HARNESS


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


def save_chart(text: dict[str, object]) -> None:
    configure_font(text)
    labels = text["labels"]
    without_harness, with_harness = chart_values()
    x_positions = list(range(len(labels)))
    width = 0.34

    fig, ax = plt.subplots(figsize=(8.6, 3.8), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    left_positions = [x - width / 2 for x in x_positions]
    right_positions = [x + width / 2 for x in x_positions]
    bars_without = ax.bar(left_positions, without_harness, width, label=text["legend"][0], color="#64748b")
    bars_with = ax.bar(right_positions, with_harness, width, label=text["legend"][1], color="#0f766e")

    for bars in [bars_without, bars_with]:
        for bar in bars:
            value = bar.get_height()
            ax.annotate(
                f"{value:g}",
                (bar.get_x() + bar.get_width() / 2, value),
                textcoords="offset points",
                xytext=(0, 6),
                ha="center",
                fontsize=8.5,
                color="#172033",
            )

    ax.set_ylabel(text["ylabel"])
    ax.set_xticks(x_positions, labels)
    ax.set_ylim(0, max(with_harness) * 1.35)
    ax.tick_params(axis="x", labelsize=8.8)
    ax.legend(frameon=False, ncols=2, loc="upper left", bbox_to_anchor=(0, 1.12), fontsize=8.6)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
