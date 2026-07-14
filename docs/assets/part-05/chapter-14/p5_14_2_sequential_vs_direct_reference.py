from pathlib import Path
import os


REPO_ROOT = Path(__file__).resolve().parents[4]
MPL_CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


OUT_DIR = Path(__file__).resolve().parent

CONTEXT = {
    "ko": ["규칙", "보정 로그", "자재 로그", "압력 상태", "일정 로그", "요청"],
    "en": ["Rule", "Calibration", "Restock", "Pressure state", "Schedule", "Request"],
}

STATE_HISTORY = {
    "pressure_risk": [1.0, 0.55, 0.303, 1.166, 0.642, 0.353],
    "restart": [1.0, 0.55, 0.303, 0.166, 0.092, 1.05],
    "block": [1.0, 0.55, 0.303, 0.166, 0.092, 0.05],
}

DIRECT_MATCHES = {
    "ko": {
        "규칙 줄": 4,
        "압력 상태 줄": 2,
        "기타 로그": 0,
    },
    "en": {
        "Rule line": 4,
        "Pressure state": 2,
        "Other logs": 0,
    },
}


def configure_fonts():
    candidates = [
        "AppleGothic",
        "Noto Sans CJK KR",
        "Noto Sans KR",
        "Malgun Gothic",
        "DejaVu Sans",
    ]
    available = {font.name for font in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False


def draw_state_decay(locale: str):
    is_ko = locale == "ko"
    title = (
        "순차 상태: 앞 단서가 중간 로그를 지나며 약해짐"
        if is_ko
        else "Sequential state: earlier clues fade through intervening logs"
    )
    x_label = "문맥 진행 위치" if is_ko else "Context position"
    y_label = "상태 강도" if is_ko else "State strength"
    final_note = "마지막 요청에서 금지 근거는 0.05만 남음" if is_ko else "At the final request, block clue remains only 0.05"

    context_labels = CONTEXT[locale]
    x = list(range(1, len(context_labels) + 1))
    fig, ax = plt.subplots(figsize=(8.2, 4.8))

    colors = {
        "pressure_risk": "#d97706",
        "restart": "#2563eb",
        "block": "#dc2626",
    }
    labels = {
        "pressure_risk": "압력 위험" if is_ko else "pressure risk",
        "restart": "재기동 요청" if is_ko else "restart",
        "block": "금지 근거" if is_ko else "block clue",
    }
    for key, values in STATE_HISTORY.items():
        ax.plot(
            x,
            values,
            marker="o",
            linewidth=2.8,
            color=colors[key],
            label=labels[key],
        )
    ax.axvline(6, color="#111827", linestyle="--", linewidth=1.1, alpha=0.55)
    ax.annotate(
        final_note,
        xy=(6, STATE_HISTORY["block"][-1]),
        xytext=(3.55, 1.2),
        arrowprops={"arrowstyle": "->", "color": "#111827", "lw": 1.2},
        fontsize=9.5,
        color="#111827",
    )
    ax.set_title(title, fontsize=13, loc="left", fontweight="bold", color="#172033")
    ax.set_xticks(x)
    ax.set_xticklabels(context_labels, rotation=18, ha="right")
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_ylim(0, 1.35)
    ax.grid(True, axis="y", linestyle="--", alpha=0.35)
    ax.legend(loc="upper right", frameon=False, fontsize=8.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    suffix = "ko" if is_ko else "en"
    fig.tight_layout()
    fig.savefig(OUT_DIR / f"sequential-state-decay-{suffix}.png", dpi=160)
    plt.close(fig)


def draw_direct_reference(locale: str):
    is_ko = locale == "ko"
    title = (
        "직접 재참조: 요청 시점에 관련 줄을 다시 끌어옴"
        if is_ko
        else "Direct re-reference: relevant lines are retrieved at request time"
    )
    bar_label = "키워드 일치 점수" if is_ko else "Keyword match score"
    direct_matches = DIRECT_MATCHES[locale]
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    bar_names = list(direct_matches.keys())
    bar_values = list(direct_matches.values())
    bar_colors = ["#dc2626", "#d97706", "#9ca3af"]
    ax.bar(bar_names, bar_values, color=bar_colors, width=0.58)
    ax.set_title(title, fontsize=13, loc="left", fontweight="bold", color="#172033")
    ax.set_ylabel(bar_label)
    ax.set_ylim(0, 4.6)
    ax.grid(True, axis="y", linestyle="--", alpha=0.3)
    for idx, value in enumerate(bar_values):
        ax.text(idx, value + 0.12, str(value), ha="center", va="bottom", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    suffix = "ko" if is_ko else "en"
    fig.tight_layout()
    fig.savefig(OUT_DIR / f"direct-reference-match-scores-{suffix}.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    configure_fonts()
    for locale in ["ko", "en"]:
        draw_state_decay(locale)
        draw_direct_reference(locale)
