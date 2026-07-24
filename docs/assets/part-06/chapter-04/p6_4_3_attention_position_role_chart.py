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

ROWS = [
    {
        "key": "subject_action",
        "multi_head": 0.92,
        "position": 0.45,
    },
    {
        "key": "object_change",
        "multi_head": 0.88,
        "position": 0.42,
    },
    {
        "key": "recipient_relation",
        "multi_head": 0.82,
        "position": 0.48,
    },
    {
        "key": "order_switch",
        "multi_head": 0.48,
        "position": 0.94,
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
        "outfile": "attention-position-role-split-ko.png",
        "row_labels": {
            "subject_action": "주체-행동\n관계",
            "object_change": "대상-변화\n관계",
            "recipient_relation": "전달 대상\n관계",
            "order_switch": "앞뒤 순서\n뒤집힘",
        },
        "xlabel": "직접 연결 강도",
        "multi_head_label": "multi-head attention",
        "position_label": "위치 표현",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "attention-position-role-split-en.png",
        "row_labels": {
            "subject_action": "subject-action\nrelation",
            "object_change": "object-change\nrelation",
            "recipient_relation": "recipient\nrelation",
            "order_switch": "order\nswitch",
        },
        "xlabel": "direct connection strength",
        "multi_head_label": "multi-head attention",
        "position_label": "positional information",
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK KR",
            "PingFang SC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "attention-position-role-split-zh.png",
        "row_labels": {
            "subject_action": "主体-动作\n关系",
            "object_change": "对象-变化\n关系",
            "recipient_relation": "传递对象\n关系",
            "order_switch": "前后顺序\n反转",
        },
        "xlabel": "直接连接强度",
        "multi_head_label": "multi-head attention",
        "position_label": "位置表示",
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
    ax.grid(True, axis="x", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_chart(text: dict[str, object]) -> None:
    configure_font(text)
    labels = [text["row_labels"][row["key"]] for row in ROWS]
    multi_head_values = [row["multi_head"] for row in ROWS]
    position_values = [row["position"] for row in ROWS]
    y_positions = list(range(len(ROWS)))
    height = 0.34

    fig, ax = plt.subplots(figsize=(7.5, 4.3), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    upper_positions = [y - height / 2 for y in y_positions]
    lower_positions = [y + height / 2 for y in y_positions]
    multi_bars = ax.barh(
        upper_positions,
        multi_head_values,
        height=height,
        color="#0f766e",
        label=text["multi_head_label"],
    )
    position_bars = ax.barh(
        lower_positions,
        position_values,
        height=height,
        color="#2563eb",
        label=text["position_label"],
    )

    for bars in (multi_bars, position_bars):
        for bar in bars:
            value = bar.get_width()
            ax.annotate(
                f"{value:.2f}",
                (value, bar.get_y() + bar.get_height() / 2),
                textcoords="offset points",
                xytext=(5, 0),
                va="center",
                fontsize=8,
                color="#172033",
            )

    ax.set_yticks(y_positions, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 1.08)
    ax.set_xlabel(text["xlabel"])
    ax.legend(loc="upper right", bbox_to_anchor=(1.0, 1.16), ncol=2, frameon=False, fontsize=8.5)

    fig.subplots_adjust(left=0.15, right=0.96, top=0.86, bottom=0.13)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
