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

HIDDEN_SIZE = 4096
RANKS = [4, 8, 16, 32]

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
        "outfile": "lora-rank-ratio-ko.png",
        "xlabel": "rank",
        "ylabel": "전체 행렬 대비 조정분 비율",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "lora-rank-ratio-en.png",
        "xlabel": "rank",
        "ylabel": "update ratio vs full matrix",
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


def collect_rows() -> list[dict[str, float]]:
    full_matrix_params = HIDDEN_SIZE * HIDDEN_SIZE
    rows = []
    for rank in RANKS:
        lora_update_params = HIDDEN_SIZE * rank + rank * HIDDEN_SIZE
        rows.append({"rank": rank, "ratio": lora_update_params / full_matrix_params})
    return rows


def style_axis(ax) -> None:
    ax.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_chart(text: dict[str, str]) -> None:
    configure_font(text)
    rows = collect_rows()
    ranks = [row["rank"] for row in rows]
    ratios = [row["ratio"] for row in rows]

    fig, ax = plt.subplots(figsize=(6.2, 3.8), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)

    ax.plot(ranks, ratios, marker="o", linewidth=2.2, color="#7c3aed")
    for rank, ratio in zip(ranks, ratios):
        ax.annotate(
            f"{ratio:.4f}",
            (rank, ratio),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=9,
            color="#172033",
        )

    ax.set_xticks(ranks)
    ax.set_xlabel(text["xlabel"])
    ax.set_ylabel(text["ylabel"])
    ax.set_ylim(0, max(ratios) * 1.22)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
