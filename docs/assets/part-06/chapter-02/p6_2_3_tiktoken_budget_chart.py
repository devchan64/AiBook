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
import tiktoken


BASE_DIR = Path(__file__).resolve().parent

TEXT = {
    "ko": {
        "outfile": "tiktoken-budget-ko.png",
        "font_candidates": [
            "Noto Sans CJK KR",
            "NanumGothic",
            "Apple SD Gothic Neo",
            "AppleGothic",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "labels": ["짧은 공지", "혼합 일정", "예외 정책", "긴 출력 요청"],
        "input_label": "입력 토큰",
        "output_label": "예상 출력 토큰",
        "budget_label": "토큰 예산",
        "ylabel": "토큰 수",
    },
    "en": {
        "outfile": "tiktoken-budget-en.png",
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "labels": ["plain notice", "mixed schedule", "policy exception", "verbose output"],
        "input_label": "input tokens",
        "output_label": "expected output tokens",
        "budget_label": "token budget",
        "ylabel": "tokens",
    },
}


def count_tokens(encoding, text):
    return len(encoding.encode(text))


def choose_font(candidates):
    available = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def configure_font(text):
    plt.rcParams["font.family"] = choose_font(text["font_candidates"])
    plt.rcParams["axes.unicode_minus"] = False


def main():
    encoding = tiktoken.get_encoding("o200k_base")
    samples = [
        {
            "case": "plain_notice",
            "text": "회의는 내일 열립니다.",
            "expected_output_tokens": 40,
            "token_budget": 120,
            "chunk_size": 80,
        },
        {
            "case": "mixed_schedule",
            "text": "회의는 내일 10:00 AM에 열립니다. Zoom 링크는 mail@example.com으로 보냈어요.",
            "expected_output_tokens": 55,
            "token_budget": 120,
            "chunk_size": 80,
        },
        {
            "case": "policy_with_exception",
            "text": "연차는 3일 전 신청합니다. 단, 긴급 병가는 사후 보고가 가능하며 증빙을 첨부해야 합니다.",
            "expected_output_tokens": 70,
            "token_budget": 120,
            "chunk_size": 30,
        },
        {
            "case": "verbose_output_request",
            "text": "배송 지연 사유를 표로 정리하고, 주의사항 목록과 환불 제한 조건을 마지막에 덧붙여 주세요.",
            "expected_output_tokens": 95,
            "token_budget": 120,
            "chunk_size": 80,
        },
    ]

    rows = []
    for sample in samples:
        input_tokens = count_tokens(encoding, sample["text"])
        total_tokens = input_tokens + sample["expected_output_tokens"]
        rows.append(
            {
                **sample,
                "input_tokens": input_tokens,
                "total_tokens": total_tokens,
                "remaining_tokens": sample["token_budget"] - total_tokens,
                "chunk_margin": sample["chunk_size"] - input_tokens,
            }
        )

    input_values = [row["input_tokens"] for row in rows]
    output_values = [row["expected_output_tokens"] for row in rows]

    for text in TEXT.values():
        configure_font(text)
        labels = text["labels"]
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.bar(labels, input_values, label=text["input_label"], color="#2563eb")
        ax.bar(
            labels,
            output_values,
            bottom=input_values,
            label=text["output_label"],
            color="#f97316",
        )
        ax.axhline(120, color="#111827", linewidth=1.2, linestyle="--", label=text["budget_label"])
        ax.set_ylabel(text["ylabel"])
        ax.set_ylim(0, 135)
        ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=3, frameon=False)
        ax.tick_params(axis="x", rotation=10)
        fig.tight_layout()
        fig.savefig(BASE_DIR / text["outfile"], dpi=180)
        plt.close(fig)

    for row in rows:
        print(
            row["case"],
            "input_tokens=", row["input_tokens"],
            "expected_output_tokens=", row["expected_output_tokens"],
            "total_tokens=", row["total_tokens"],
            "remaining_tokens=", row["remaining_tokens"],
            "chunk_margin=", row["chunk_margin"],
        )


if __name__ == "__main__":
    main()
