from pathlib import Path
from collections import Counter, defaultdict
import csv
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
TEMPERATURES = [0.3, 1.0, 1.7]
SEEDS = range(1, 13)

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
        "candidate_file": "p6-6-2-next-token-candidates.csv",
        "xlabel": "temperature",
        "retention_ylabel": "상위 토큰 선택 비율",
        "unique_ylabel": "서로 다른 출력 수",
        "retention_title": "토큰 선택 안정성",
        "unique_title": "출력 다양성",
        "first_token_title": "첫 토큰 분포",
        "first_token_ylabel": "선택 횟수",
        "first_token_labels": {
            "안내": "안내",
            "주문": "주문",
            "확인": "확인",
            "환불": "환불",
        },
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "temperature-unique-reply-count-en.png",
        "candidate_file": "p6-6-2-next-token-candidates-en.csv",
        "xlabel": "temperature",
        "retention_ylabel": "top-token rate",
        "unique_ylabel": "unique outputs",
        "retention_title": "Token-choice stability",
        "unique_title": "Output diversity",
        "first_token_title": "First-token distribution",
        "first_token_ylabel": "selection count",
        "first_token_labels": {
            "안내": "guide",
            "주문": "order",
            "확인": "check",
            "환불": "refund",
        },
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
        "outfile": "temperature-unique-reply-count-zh.png",
        "candidate_file": "p6-6-2-next-token-candidates-zh.csv",
        "xlabel": "temperature",
        "retention_ylabel": "上位 token 选择比例",
        "unique_ylabel": "不同输出数",
        "retention_title": "token 选择稳定性",
        "unique_title": "输出多样性",
        "first_token_title": "第一 token 分布",
        "first_token_ylabel": "选择次数",
        "first_token_labels": {
            "引导": "引导",
            "订单": "订单",
            "确认": "确认",
            "退款": "退款",
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


def load_candidates(candidate_path: Path) -> dict[int, list[dict[str, str]]]:
    by_step: dict[int, list[dict[str, str]]] = defaultdict(list)
    with candidate_path.open(encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            by_step[int(row["step"])].append(row)
    return dict(sorted(by_step.items()))


def apply_temperature(candidates: list[dict[str, str]], temperature: float) -> list[float]:
    adjusted = [
        float(candidate["base_probability"]) ** (1.0 / temperature)
        for candidate in candidates
    ]
    total = sum(adjusted)
    return [value / total for value in adjusted]


def greedy_output(candidates_by_step: dict[int, list[dict[str, str]]], temperature: float) -> str:
    tokens = []
    for candidates in candidates_by_step.values():
        probs = apply_temperature(candidates, temperature)
        top_index = max(range(len(candidates)), key=lambda index: probs[index])
        tokens.append(candidates[top_index]["candidate_token"])
    return "".join(tokens)


def sample_output(
    candidates_by_step: dict[int, list[dict[str, str]]],
    temperature: float,
    seed: int,
) -> tuple[str, int, str]:
    rng = random.Random(seed)
    tokens = []
    top_hits = 0
    first_token = ""
    for step, candidates in candidates_by_step.items():
        probs = apply_temperature(candidates, temperature)
        top_index = max(range(len(candidates)), key=lambda index: probs[index])
        picked_index = rng.choices(range(len(candidates)), weights=probs, k=1)[0]
        if picked_index == top_index:
            top_hits += 1
        picked_token = candidates[picked_index]["candidate_token"]
        if step == 1:
            first_token = picked_token
        tokens.append(picked_token)
    return "".join(tokens), top_hits, first_token


def summarize(candidates_by_step: dict[int, list[dict[str, str]]]) -> tuple[list[float], list[int], dict[float, Counter]]:
    token_count = len(candidates_by_step)
    retention_rates = []
    unique_counts = []
    first_token_counts = {}
    for temperature in TEMPERATURES:
        greedy = greedy_output(candidates_by_step, temperature)
        outputs = []
        top_hits = 0
        first_tokens = []
        for seed in SEEDS:
            output, hits, first_token = sample_output(candidates_by_step, temperature, seed)
            outputs.append(output)
            top_hits += hits
            first_tokens.append(first_token)
        retention_rates.append(top_hits / (len(SEEDS) * token_count))
        unique_counts.append(len(set(outputs)))
        first_token_counts[temperature] = Counter(first_tokens)
    return retention_rates, unique_counts, first_token_counts


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_temperature_chart(text: dict[str, str]) -> None:
    configure_font(text)
    candidates_by_step = load_candidates(OUT_DIR / text["candidate_file"])
    retention_rates, unique_counts, first_token_counts = summarize(candidates_by_step)
    labels = [str(temperature) for temperature in TEMPERATURES]

    fig, axes = plt.subplots(1, 3, figsize=(13.2, 3.9), dpi=180)
    fig.patch.set_facecolor("white")
    for ax in axes:
        ax.set_facecolor("white")
        style_axis(ax)

    retention_bars = axes[0].bar(labels, retention_rates, color="#0f766e", width=0.52)
    for bar, value in zip(retention_bars, retention_rates):
        axes[0].annotate(
            f"{value:.2f}",
            (bar.get_x() + bar.get_width() / 2, value),
            textcoords="offset points",
            xytext=(0, 7),
            ha="center",
            fontsize=9,
            color="#172033",
        )
    axes[0].set_title(text["retention_title"], fontsize=11, pad=10)
    axes[0].set_xlabel(text["xlabel"])
    axes[0].set_ylabel(text["retention_ylabel"])
    axes[0].set_ylim(0, 1.05)

    unique_bars = axes[1].bar(labels, unique_counts, color="#d97706", width=0.52)
    for bar, value in zip(unique_bars, unique_counts):
        axes[1].annotate(
            f"{value:g}",
            (bar.get_x() + bar.get_width() / 2, value),
            textcoords="offset points",
            xytext=(0, 7),
            ha="center",
            fontsize=9,
            color="#172033",
        )
    axes[1].set_title(text["unique_title"], fontsize=11, pad=10)
    axes[1].set_xlabel(text["xlabel"])
    axes[1].set_ylabel(text["unique_ylabel"])
    axes[1].set_ylim(0, max(unique_counts) * 1.3)

    first_tokens = sorted({
        token
        for counts in first_token_counts.values()
        for token in counts
    })
    x_positions = list(range(len(first_tokens)))
    bar_width = 0.24
    colors = ["#64748b", "#0f766e", "#2563eb"]
    for index, temperature in enumerate(TEMPERATURES):
        offsets = [x + (index - 1) * bar_width for x in x_positions]
        values = [first_token_counts[temperature].get(token, 0) for token in first_tokens]
        axes[2].bar(offsets, values, width=bar_width, color=colors[index], label=str(temperature))
    axes[2].set_title(text["first_token_title"], fontsize=11, pad=10)
    axes[2].set_xticks(x_positions)
    axes[2].set_xticklabels([
        text["first_token_labels"].get(token, token)
        for token in first_tokens
    ])
    axes[2].set_xlabel("first token")
    axes[2].set_ylabel(text["first_token_ylabel"])
    axes[2].set_ylim(0, 12.8)
    axes[2].legend(frameon=False, fontsize=8, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.18))

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_temperature_chart(text)


if __name__ == "__main__":
    main()
