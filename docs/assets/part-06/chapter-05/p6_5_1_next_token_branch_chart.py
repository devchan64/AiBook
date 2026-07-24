from pathlib import Path
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

PATHS = [
    {
        "key": "time",
        "color": "#2563eb",
        "ko_label": "시간 경로",
        "en_label": "time path",
        "zh_label": "时间路径",
        "ko_tokens": ["오후", "세", "시입니다"],
        "en_tokens": ["afternoon", "three", "o'clock"],
        "zh_tokens": ["下午", "三点", "开始"],
        "scores": [0.62, 0.55, 0.58],
        "ko_offsets": [(0, 11), (0, -30), (0, -30)],
        "en_offsets": [(0, 11), (0, -30), (0, -30)],
        "zh_offsets": [(0, 11), (0, -30), (0, -30)],
    },
    {
        "key": "online",
        "color": "#0f766e",
        "ko_label": "온라인 경로",
        "en_label": "online path",
        "zh_label": "线上路径",
        "ko_tokens": ["온라인", "으로", "진행합니다"],
        "en_tokens": ["online", "as", "held"],
        "zh_tokens": ["线上", "进行", "确认"],
        "scores": [0.27, 0.64, 0.67],
        "ko_offsets": [(0, 11), (0, 12), (0, 13)],
        "en_offsets": [(0, 11), (0, 12), (0, 13)],
        "zh_offsets": [(0, 11), (0, 12), (0, 13)],
    },
]

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
        "outfile": "autoregressive-path-split-ko.png",
        "title": "첫 선택 뒤 갈라지는 누적 생성 경로",
        "step_labels": ["step 1", "step 2", "step 3"],
        "ylabel": "선택 토큰 점수",
        "score_label": "누적",
        "label_key": "ko_label",
        "token_key": "ko_tokens",
        "offset_key": "ko_offsets",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "autoregressive-path-split-en.png",
        "title": "Autoregressive paths diverge after the first choice",
        "step_labels": ["step 1", "step 2", "step 3"],
        "ylabel": "chosen token score",
        "score_label": "total",
        "label_key": "en_label",
        "token_key": "en_tokens",
        "offset_key": "en_offsets",
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK KR",
            "PingFang SC",
            "Heiti SC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "autoregressive-path-split-zh.png",
        "title": "第一选择之后分岔的累积生成路径",
        "step_labels": ["step 1", "step 2", "step 3"],
        "ylabel": "所选 token 分数",
        "score_label": "累计",
        "label_key": "zh_label",
        "token_key": "zh_tokens",
        "offset_key": "zh_offsets",
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


def cumulative(values: list[float]) -> list[float]:
    running = 0.0
    totals = []
    for value in values:
        running += value
        totals.append(running)
    return totals


def save_chart(text: dict[str, object]) -> None:
    configure_font(text)
    fig, (ax_scores, ax_totals) = plt.subplots(
        2,
        1,
        figsize=(7.4, 4.8),
        dpi=180,
        sharex=True,
        gridspec_kw={"height_ratios": [1.1, 1.0]},
    )
    fig.patch.set_facecolor("white")
    x_positions = [1, 2, 3]

    for ax in (ax_scores, ax_totals):
        ax.set_facecolor("white")
        ax.grid(axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    for path in PATHS:
        label = path[text["label_key"]]
        tokens = path[text["token_key"]]
        offsets = path[text["offset_key"]]
        scores = path["scores"]
        color = path["color"]
        totals = cumulative(scores)

        ax_scores.plot(
            x_positions,
            scores,
            marker="o",
            linewidth=2.2,
            color=color,
            label=label,
        )
        for x, score, token, offset in zip(x_positions, scores, tokens, offsets):
            ax_scores.annotate(
                f"{token}\n{score:.2f}",
                (x, score),
                textcoords="offset points",
                xytext=offset,
                ha="center",
                fontsize=9,
                color="#172033",
            )

        ax_totals.plot(
            x_positions,
            totals,
            marker="o",
            linewidth=2.2,
            color=color,
            label=label,
        )
        ax_totals.annotate(
            f"{text['score_label']} {totals[-1]:.2f}",
            (x_positions[-1], totals[-1]),
            textcoords="offset points",
            xytext=(9, 0),
            ha="left",
            va="center",
            fontsize=9,
            color="#172033",
        )

    ax_scores.set_title(text["title"], fontsize=13, pad=12, fontweight="bold")
    ax_scores.set_ylabel(text["ylabel"])
    ax_scores.set_ylim(0.15, 0.78)
    ax_scores.legend(loc="lower right", frameon=False, fontsize=9)

    ax_totals.set_ylabel(text["score_label"])
    ax_totals.set_ylim(0, 2.05)
    ax_totals.set_xticks(x_positions, text["step_labels"])
    ax_totals.set_xlim(0.75, 3.35)

    fig.tight_layout(pad=1.0)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
