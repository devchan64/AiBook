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
import numpy as np


OUT_DIR = Path(__file__).resolve().parent

HISTORY = {
    "temperature_alert": {
        "coolant": 14,
        "fan": 9,
        "sensor": 5,
    },
    "seal_edge_alert": {
        "seal_pressure": 13,
        "film_tension": 8,
        "blade_wear": 4,
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
        "ylabel": "확률",
        "xlabel": "후속 조치 후보",
        "cases": {
            "temperature_alert": {
                "outfile": "generative-response-distribution-temperature-ko.png",
                "labels": ["냉각수 유량", "팬 상태", "센서 보정"],
            },
            "seal_edge_alert": {
                "outfile": "generative-response-distribution-seal-ko.png",
                "labels": ["실링 압력", "필름 장력", "칼날 마모"],
            },
        },
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "ylabel": "probability",
        "xlabel": "follow-up candidate",
        "cases": {
            "temperature_alert": {
                "outfile": "generative-response-distribution-temperature-en.png",
                "labels": ["coolant flow", "fan state", "sensor check"],
            },
            "seal_edge_alert": {
                "outfile": "generative-response-distribution-seal-en.png",
                "labels": ["seal pressure", "film tension", "blade wear"],
            },
        },
    },
    "zh": {
        "font_candidates": [
            "Noto Sans CJK SC",
            "Noto Sans CJK JP",
            "Microsoft YaHei",
            "PingFang SC",
            "Arial Unicode MS",
            "DejaVu Sans",
        ],
        "ylabel": "概率",
        "xlabel": "后续候选",
        "cases": {
            "temperature_alert": {
                "outfile": "generative-response-distribution-temperature-zh.png",
                "labels": ["冷却水流量", "风扇状态", "传感器校准"],
            },
            "seal_edge_alert": {
                "outfile": "generative-response-distribution-seal-zh.png",
                "labels": ["封边压力", "膜张力", "刀刃磨损"],
            },
        },
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


def probabilities(case: str) -> np.ndarray:
    counts = np.array(list(HISTORY[case].values()), dtype=float)
    return np.round(counts / counts.sum(), 2)


def save_case_chart(lang: str, text: dict[str, object], case: str) -> None:
    configure_font(text)
    case_text = text["cases"][case]
    labels = case_text["labels"]
    values = probabilities(case)
    positions = np.arange(len(labels))
    colors = ["#2563eb", "#38bdf8", "#38bdf8"]

    fig, axis = plt.subplots(figsize=(4.8, 3.6), dpi=180)
    fig.patch.set_facecolor("white")
    axis.set_facecolor("#f8fafc")
    axis.grid(True, axis="y", color="#d0d7de", linewidth=0.75, alpha=0.85)
    axis.set_axisbelow(True)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)

    axis.bar(positions, values, color=colors, width=0.58)
    axis.set_xticks(positions)
    axis.set_xticklabels(labels, fontsize=8.2)
    axis.set_ylim(0, 0.6)
    axis.set_xlabel(text["xlabel"])
    axis.set_ylabel(text["ylabel"])

    for idx, value in enumerate(values):
        axis.text(idx, value + 0.018, f"{value:.2f}", ha="center", fontsize=8.2, color="#334155")

    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / case_text["outfile"], format="png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for lang, text in LANG_TEXT.items():
        for case in HISTORY:
            save_case_chart(lang, text, case)


if __name__ == "__main__":
    main()
