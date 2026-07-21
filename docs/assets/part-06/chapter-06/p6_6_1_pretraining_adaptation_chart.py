from collections import Counter, defaultdict
from pathlib import Path
from typing import Tuple, Union
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

GENERAL_CORPUS = [
    "문의 내용을 확인 합니다",
    "요청 내용을 확인 합니다",
    "문서 내용을 정리 합니다",
    "결과 내용을 설명 합니다",
    "안내 메일을 전달 합니다",
]

CUSTOMER_SUPPORT_CORPUS = [
    "환불 문의 내용을 확인 합니다",
    "배송 문의 내용을 확인 합니다",
    "계정 문의 내용을 확인 합니다",
    "환불 요청 내용을 확인 합니다",
]

LINKS = [
    ("문의 -> 내용을", "문의", "내용을"),
    ("환불 -> 문의/요청", "환불", ("문의", "요청")),
    ("내용을 -> 확인", "내용을", "확인"),
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
        "outfile": "pretraining-adaptation-counts-ko.png",
        "xlabel": "후보 연결",
        "ylabel": "다음 토큰 관측 횟수",
        "general_label": "일반 코퍼스",
        "adapted_label": "도메인 문장 추가 후",
        "labels": ["문의 -> 내용을", "환불 -> 문의/요청", "내용을 -> 확인"],
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "pretraining-adaptation-counts-en.png",
        "xlabel": "candidate link",
        "ylabel": "next-token count",
        "general_label": "general corpus",
        "adapted_label": "after domain data",
        "labels": ["inquiry -> content", "refund -> inquiry/request", "content -> check"],
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


def build_bigram_counts(sentences: list[str]) -> dict[str, Counter]:
    counts = defaultdict(Counter)
    for sentence in sentences:
        tokens = sentence.split()
        for left, right in zip(tokens, tokens[1:]):
            counts[left][right] += 1
    return counts


def link_count(counts: dict[str, Counter], left: str, rights: Union[str, Tuple[str, ...]]) -> int:
    if isinstance(rights, str):
        rights = (rights,)
    return sum(counts[left][right] for right in rights)


def collect_rows() -> list[dict[str, int]]:
    general_counts = build_bigram_counts(GENERAL_CORPUS)
    adapted_counts = build_bigram_counts(GENERAL_CORPUS + CUSTOMER_SUPPORT_CORPUS)

    rows = []
    for _, left, rights in LINKS:
        rows.append(
            {
                "general": link_count(general_counts, left, rights),
                "adapted": link_count(adapted_counts, left, rights),
            }
        )
    return rows


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_chart(text: dict[str, str]) -> None:
    configure_font(text)
    rows = collect_rows()
    labels = text["labels"]
    general_values = [row["general"] for row in rows]
    adapted_values = [row["adapted"] for row in rows]
    x_positions = list(range(len(labels)))
    bar_width = 0.34

    fig, ax = plt.subplots(figsize=(7.0, 3.9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    general_bars = ax.bar(
        [x - bar_width / 2 for x in x_positions],
        general_values,
        width=bar_width,
        color="#64748b",
        label=text["general_label"],
    )
    adapted_bars = ax.bar(
        [x + bar_width / 2 for x in x_positions],
        adapted_values,
        width=bar_width,
        color="#16a34a",
        label=text["adapted_label"],
    )

    for bars in (general_bars, adapted_bars):
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
    ax.set_xlabel(text["xlabel"])
    ax.set_ylabel(text["ylabel"])
    ax.set_ylim(0, max(adapted_values) * 1.25)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
