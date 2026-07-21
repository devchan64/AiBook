from pathlib import Path
import os
import random

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
TEMPERATURES = [0.5, 1.0, 1.5]

REPLY_SLOTS = {
    "opening": {
        "불편을 드려 죄송합니다.": 0.50,
        "문의 주셔서 감사합니다.": 0.30,
        "확인 도와드리겠습니다.": 0.20,
    },
    "policy": {
        "환불은 배송 완료 후 7일 이내 가능합니다.": 0.55,
        "배송 완료 후 7일 안에 환불을 접수할 수 있습니다.": 0.25,
        "주문 상태를 확인한 뒤 환불 가능 여부를 안내해 드립니다.": 0.20,
    },
    "next_step": {
        "주문번호를 보내 주시면 바로 확인하겠습니다.": 0.60,
        "주문번호와 수령일을 함께 알려 주세요.": 0.25,
        "필요한 정보를 남겨 주시면 순서대로 도와드리겠습니다.": 0.15,
    },
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
        "outfile": "temperature-unique-reply-count-ko.png",
        "xlabel": "temperature",
        "ylabel": "서로 다른 답변 조합 수",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "temperature-unique-reply-count-en.png",
        "xlabel": "temperature",
        "ylabel": "unique reply combinations",
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


def apply_temperature(prob_dict: dict[str, float], temperature: float) -> dict[str, float]:
    adjusted = {token: prob ** (1.0 / temperature) for token, prob in prob_dict.items()}
    total = sum(adjusted.values())
    return {token: adjusted[token] / total for token in adjusted}


def sample_many(
    slots: dict[str, dict[str, float]],
    temperature: float,
    trials: int = 12,
    seed: int = 7,
) -> int:
    random.seed(seed)
    replies = []
    for _ in range(trials):
        parts = []
        for _, prob_dict in slots.items():
            adjusted = apply_temperature(prob_dict, temperature)
            tokens = list(adjusted.keys())
            weights = list(adjusted.values())
            parts.append(random.choices(tokens, weights=weights, k=1)[0])
        replies.append(" ".join(parts))
    return len(set(replies))


def unique_counts() -> list[int]:
    return [sample_many(REPLY_SLOTS, temperature, trials=12, seed=7) for temperature in TEMPERATURES]


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_temperature_chart(text: dict[str, str]) -> None:
    configure_font(text)
    values = unique_counts()
    labels = [str(temperature) for temperature in TEMPERATURES]

    fig, ax = plt.subplots(figsize=(6.2, 3.6), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)
    bars = ax.bar(labels, values, color="#2563eb", width=0.52)

    for bar, value in zip(bars, values):
        ax.annotate(
            f"{value:g}",
            (bar.get_x() + bar.get_width() / 2, value),
            textcoords="offset points",
            xytext=(0, 7),
            ha="center",
            fontsize=9,
            color="#172033",
        )

    ax.set_xlabel(text["xlabel"])
    ax.set_ylabel(text["ylabel"])
    ax.set_ylim(0, max(values) * 1.28)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_temperature_chart(text)


if __name__ == "__main__":
    main()
