from csv import DictReader
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
from matplotlib.ticker import FuncFormatter

OUT_DIR = Path(__file__).resolve().parent
CSV_PATH = OUT_DIR / "deep-scale-activation-log.csv"
CASE_ORDER = ["small_init", "medium_init", "large_init", "very_large_init"]
LAYER_ORDER = [1, 2, 3]

LANG_TEXT = {
    "ko": {
        "font_candidates": ["Noto Sans CJK KR", "NanumGothic", "Apple SD Gothic Neo", "AppleGothic", "Arial Unicode MS", "DejaVu Sans"],
        "raw_range_outfile": "deep-scale-raw-range-ko.png",
        "raw_variance_outfile": "deep-scale-raw-variance-ko.png",
        "bn_range_outfile": "deep-scale-bn-range-ko.png",
        "layer_label": "층",
        "raw_range_ylabel": "원시 활성값 범위 폭",
        "raw_variance_ylabel": "원시 분산",
        "bn_range_ylabel": "BN 뒤 활성값 범위 폭",
        "small_init": "작은 초기화",
        "medium_init": "중간 초기화",
        "large_init": "큰 초기화",
        "very_large_init": "매우 큰 초기화",
    },
    "en": {
        "font_candidates": ["DejaVu Sans", "Arial Unicode MS"],
        "raw_range_outfile": "deep-scale-raw-range-en.png",
        "raw_variance_outfile": "deep-scale-raw-variance-en.png",
        "bn_range_outfile": "deep-scale-bn-range-en.png",
        "layer_label": "layer",
        "raw_range_ylabel": "raw activation range width",
        "raw_variance_ylabel": "raw variance",
        "bn_range_ylabel": "activation range width after BN",
        "small_init": "small init",
        "medium_init": "medium init",
        "large_init": "large init",
        "very_large_init": "very large init",
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
        "raw_range_outfile": "deep-scale-raw-range-zh.png",
        "raw_variance_outfile": "deep-scale-raw-variance-zh.png",
        "bn_range_outfile": "deep-scale-bn-range-zh.png",
        "layer_label": "层",
        "raw_range_ylabel": "raw activation range 宽度",
        "raw_variance_ylabel": "raw variance",
        "bn_range_ylabel": "BN 后 activation range 宽度",
        "small_init": "小初始化",
        "medium_init": "中等初始化",
        "large_init": "大初始化",
        "very_large_init": "很大的初始化",
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


def batch_norm(values: list[float], eps: float = 1e-5) -> tuple[float, float, list[float]]:
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    normalized = [(value - mean) / ((variance + eps) ** 0.5) for value in values]
    return mean, variance, normalized


def load_rows():
    rows = []
    with CSV_PATH.open(encoding="utf-8") as file:
        for row in DictReader(file):
            rows.append(
                {
                    "case_name": row["case_name"],
                    "weight_scale": float(row["weight_scale"]),
                    "layer": int(row["layer"]),
                    "sample": row["sample"],
                    "raw_activation": float(row["raw_activation"]),
                }
            )
    return rows


def build_trace() -> dict[str, list[dict[str, float]]]:
    rows = load_rows()
    traces = {}
    for case_name in CASE_ORDER:
        case_rows = [row for row in rows if row["case_name"] == case_name]
        layer_trace = []
        for layer in LAYER_ORDER:
            layer_rows = [row for row in case_rows if row["layer"] == layer]
            raw_values = [row["raw_activation"] for row in layer_rows]
            _, raw_variance, bn_values = batch_norm(raw_values)

            layer_trace.append(
                {
                    "layer": layer,
                    "raw_range_width": max(raw_values) - min(raw_values),
                    "raw_variance": raw_variance,
                    "bn_range_width": max(bn_values) - min(bn_values),
                }
            )
        traces[case_name] = layer_trace
    return traces


def style_axis(ax) -> None:
    ax.grid(True, color="#d0d7de", linewidth=0.75, alpha=0.85)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_line_chart(text: dict[str, str], trace: dict, metric: str, ylabel: str, outfile: str, log_scale: bool = False) -> None:
    configure_font(text)
    colors = {
        "small_init": "#2563eb",
        "medium_init": "#f59e0b",
        "large_init": "#dc2626",
        "very_large_init": "#7c3aed",
    }
    x_offsets = {
        "small_init": -0.09,
        "medium_init": -0.03,
        "large_init": 0.03,
        "very_large_init": 0.09,
    }
    fig, ax = plt.subplots(figsize=(6.8, 3.8), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    style_axis(ax)
    for case_name, rows in trace.items():
        layers = [row["layer"] for row in rows]
        if metric == "bn_range_width":
            layers = [layer + x_offsets[case_name] for layer in layers]
        values = [row[metric] for row in rows]
        ax.plot(layers, values, marker="o", linewidth=2.2, color=colors[case_name], label=text[case_name])
    ax.set_xticks([1, 2, 3])
    ax.set_xlabel(text["layer_label"])
    ax.set_ylabel(ylabel)
    if log_scale:
        ax.set_yscale("log")
        ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:g}"))
    if metric == "bn_range_width":
        ax.set_ylim(0, 3.2)
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    fig.tight_layout(pad=0.9)
    fig.savefig(OUT_DIR / outfile, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    trace = build_trace()
    for text in LANG_TEXT.values():
        save_line_chart(text, trace, "raw_range_width", text["raw_range_ylabel"], text["raw_range_outfile"], log_scale=True)
        save_line_chart(text, trace, "raw_variance", text["raw_variance_ylabel"], text["raw_variance_outfile"], log_scale=True)
        save_line_chart(text, trace, "bn_range_width", text["bn_range_ylabel"], text["bn_range_outfile"])


if __name__ == "__main__":
    main()
