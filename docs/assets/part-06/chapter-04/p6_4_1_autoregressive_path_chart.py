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

PATHS = {
    "time_flow": {
        "scores": [0.62, 0.55, 0.58],
        "color": "#2563eb",
    },
    "online_flow": {
        "scores": [0.27, 0.64, 0.67],
        "color": "#0f766e",
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
        "outfile": "autoregressive-path-split-ko.png",
        "title": "첫 토큰 선택 뒤 갈라지는 누적 생성 경로",
        "xlabel": "생성 step",
        "ylabel": "선택 점수 누적합",
        "xticklabels": ["step 1\n첫 선택", "step 2\n다음 후보", "step 3\n최종 흐름"],
        "labels": {
            "time_flow": "시간 안내 경로",
            "online_flow": "온라인 진행 경로",
        },
        "tokens": {
            "time_flow": ["오후", "세", "시입니다"],
            "online_flow": ["온라인", "으로", "진행합니다"],
        },
        "split_label": "첫 선택 분기",
        "token_prefix": "선택",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "outfile": "autoregressive-path-split-en.png",
        "title": "Autoregressive paths split after the first token",
        "xlabel": "generation step",
        "ylabel": "cumulative chosen score",
        "xticklabels": ["step 1\nfirst choice", "step 2\nnext candidates", "step 3\nfinal flow"],
        "labels": {
            "time_flow": "time notice path",
            "online_flow": "online meeting path",
        },
        "tokens": {
            "time_flow": ["afternoon", "three", "time"],
            "online_flow": ["online", "as", "proceeds"],
        },
        "split_label": "first-choice split",
        "token_prefix": "chosen",
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


def cumulative_scores(scores: list[float]) -> list[float]:
    total = 0.0
    values = []
    for score in scores:
        total += score
        values.append(round(total, 2))
    return values


def save_chart(text: dict[str, object]) -> None:
    configure_font(text)
    fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    x_values = [1, 2, 3]
    for key, path in PATHS.items():
        y_values = cumulative_scores(path["scores"])
        ax.plot(
            x_values,
            y_values,
            marker="o",
            linewidth=2.6,
            markersize=6,
            color=path["color"],
            label=text["labels"][key],
        )
        for x, y, token in zip(x_values, y_values, text["tokens"][key]):
            if key == "online_flow" and x == 1:
                xytext = (42, 2)
                ha = "left"
                va = "center"
            else:
                xytext = (0, 14) if key == "time_flow" else (0, -30)
                ha = "center"
                va = "bottom" if key == "time_flow" else "top"
            ax.annotate(
                f"{text['token_prefix']}: {token}\n{y:.2f}",
                xy=(x, y),
                xytext=xytext,
                textcoords="offset points",
                ha=ha,
                va=va,
                fontsize=8.5,
                color="#172033",
            )

    ax.axvline(1, color="#94a3b8", linewidth=1.2, linestyle="--")
    ax.text(
        1.03,
        0.06,
        text["split_label"],
        fontsize=8.5,
        color="#64748b",
        ha="left",
        va="bottom",
    )

    ax.set_title(text["title"], fontsize=12, pad=14, fontweight="bold")
    ax.set_xlabel(text["xlabel"], labelpad=10)
    ax.set_ylabel(text["ylabel"], labelpad=10)
    ax.set_xticks(x_values, text["xticklabels"])
    ax.set_xlim(0.72, 3.28)
    ax.set_ylim(0, 2.12)
    ax.grid(axis="y", color="#e2e8f0", linewidth=0.9)
    ax.legend(loc="lower right", frameon=False, fontsize=9)

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#cbd5e1")
    ax.spines["bottom"].set_color("#cbd5e1")

    fig.tight_layout(pad=1.0)
    fig.savefig(OUT_DIR / text["outfile"], bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for text in LANG_TEXT.values():
        save_chart(text)


if __name__ == "__main__":
    main()
