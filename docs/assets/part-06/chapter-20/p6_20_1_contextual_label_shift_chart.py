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
from matplotlib.colors import ListedColormap

OUT_DIR = Path(__file__).resolve().parent

CASES = [
    {"key": "bank_money", "surface_ok": True, "context_ok": True, "label_shift": False},
    {"key": "ginkgo_tree", "surface_ok": False, "context_ok": True, "label_shift": True},
    {"key": "password_reset", "surface_ok": True, "context_ok": True, "label_shift": False},
    {"key": "order_payment", "surface_ok": True, "context_ok": True, "label_shift": False},
]

CHECK_KEYS = ["surface_ok", "context_ok", "label_shift"]

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
        "outfile": "contextual-label-shift-ko.png",
        "rows": ["은행+돈", "은행나무", "비밀번호", "주문+결제"],
        "cols": ["표면 라벨 적합", "문맥 해석 가능", "라벨 전환 발생"],
        "yes": "예",
        "no": "아니오",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "contextual-label-shift-en.png",
        "rows": ["bank+money", "ginkgo tree", "password", "order+payment"],
        "cols": ["surface label fits", "context read works", "label shift"],
        "yes": "yes",
        "no": "no",
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK TC",
            "PingFang SC",
            "Heiti SC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "outfile": "contextual-label-shift-zh.png",
        "rows": ["银行+钱", "河岸", "密码", "订单+付款"],
        "cols": ["表面标签适合", "可读出上下文", "发生标签转换"],
        "yes": "是",
        "no": "否",
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


def save_chart(text: dict[str, object]) -> None:
    configure_font(text)
    matrix = [[1 if case[key] else 0 for key in CHECK_KEYS] for case in CASES]
    cmap = ListedColormap(["#e2e8f0", "#0f766e"])

    fig, ax = plt.subplots(figsize=(8.8, 3.9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.imshow(matrix, cmap=cmap, vmin=0, vmax=1, aspect="auto")

    ax.set_xticks(range(len(text["cols"])))
    ax.set_xticklabels(text["cols"])
    ax.set_yticks(range(len(text["rows"])))
    ax.set_yticklabels(text["rows"])
    ax.tick_params(axis="x", labelsize=8.7, pad=8)
    ax.tick_params(axis="y", labelsize=8.8)

    ax.set_xticks([index - 0.5 for index in range(1, len(CHECK_KEYS))], minor=True)
    ax.set_yticks([index - 0.5 for index in range(1, len(CASES))], minor=True)
    ax.grid(which="minor", color="white", linewidth=2.2)
    ax.tick_params(which="minor", bottom=False, left=False)

    for row_index, row in enumerate(matrix):
        for col_index, value in enumerate(row):
            ax.text(
                col_index,
                row_index,
                text["yes"] if value else text["no"],
                ha="center",
                va="center",
                color="white" if value else "#334155",
                fontsize=8.2,
                fontweight="bold" if value else "normal",
            )

    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
