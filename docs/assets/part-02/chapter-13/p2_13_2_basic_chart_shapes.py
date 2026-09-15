"""Recreate the manuscript charts from the repository root.

Use --language to render one language and --output-dir for temporary previews.
Matplotlib and NumPy are required. Localized SVG export requires a CJK font
such as Noto Sans CJK JP; --font-family can select another installed font.
"""
from pathlib import Path
import argparse
import os

REPO_ROOT = Path(__file__).resolve().parents[4]
MPL_CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.text import Text
import numpy as np

OUT_DIR = Path(__file__).resolve().parent
LANGUAGES = ("ko", "en", "zh")
FONT_FAMILY = "Noto Sans CJK JP"

LABELS = {'epoch': ('에폭', '轮次'), 'loss': ('손실', '损失'), 'count': ('개수', '数量'), 'Function shape: y = x^2': ('함수의 모양: y = x²', '函数形状：y = x²'), 'input value': ('입력값', '输入值'), 'observed value': ('관측값', '观测值'), 'Scatter plot: relationship with variation': ('산점도: 관계와 흩어짐', '散点图：关系与离散'), 'value': ('값', '值'), 'Histogram: where values gather': ('히스토그램: 값이 모이는 구간', '直方图：值集中的区间'), 'model': ('모델', '模型'), 'validation loss': ('검증 손실', '验证损失'), 'Model comparison on the same validation set': ('같은 검증 자료에서 모델 비교', '在同一验证集上比较模型'), 'steady decrease': ('꾸준한 감소', '持续下降'), 'unstable': ('진동', '波动'), 'Loss curves can reveal training behavior': ('손실 곡선의 감소와 진동', '损失曲线的下降与波动')}

def save_figure(fig, stem):
    # Keep one data/geometry source; translate visible labels for each export.
    fig.canvas.draw()
    originals = [(text, text.get_text()) for text in fig.findobj(Text)]
    for language in LANGUAGES:
        for text, original in originals:
            translated = LABELS.get(original)
            text.set_text(original if language == "en" or translated is None
                          else translated[0 if language == "ko" else 1])
            text.set_fontfamily(FONT_FAMILY)
        fig.tight_layout()
        path = OUT_DIR / f"{stem}-{language}.svg"
        fig.savefig(path, metadata={"Date": None})
        path.write_text("\n".join(line.rstrip() for line in path.read_text().splitlines()) + "\n")
    plt.close(fig)


def save_basic_line_function_shape():
    x = np.linspace(-3, 3, 121)
    y = x**2

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Function shape: y = x^2")
    save_figure(fig, "basic-line-function-shape")

def save_basic_scatter_relationship():
    rng = np.random.default_rng(42)
    x = np.linspace(1, 10, 24)
    y = 2.5 * x + rng.normal(0, 2.2, size=x.shape)

    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set_xlabel("input value")
    ax.set_ylabel("observed value")
    ax.set_title("Scatter plot: relationship with variation")
    save_figure(fig, "basic-scatter-relationship")

def save_basic_hist_distribution():
    rng = np.random.default_rng(7)
    values = rng.normal(loc=0, scale=1, size=240)

    fig, ax = plt.subplots()
    ax.hist(values, bins=18)
    ax.set_xlabel("value")
    ax.set_ylabel("count")
    ax.set_title("Histogram: where values gather")
    save_figure(fig, "basic-hist-distribution")

def save_basic_bar_model_comparison():
    models = ["A", "B", "C"]
    validation_loss = [0.42, 0.39, 0.47]
    fig, ax = plt.subplots()
    ax.bar(models, validation_loss)
    ax.set_ylim(0, 0.55)
    ax.set_xlabel("model")
    ax.set_ylabel("validation loss")
    ax.set_title("Model comparison on the same validation set")
    save_figure(fig, "basic-bar-model-comparison")

def save_basic_loss_curve_comparison():
    epochs = np.arange(1, 11)
    decreasing_loss = [2.4, 1.8, 1.35, 1.08, 0.91, 0.79, 0.70, 0.64, 0.60, 0.57]
    unstable_loss = [2.4, 1.9, 1.75, 1.82, 1.55, 1.62, 1.45, 1.52, 1.40, 1.46]

    fig, ax = plt.subplots()
    ax.plot(epochs, decreasing_loss, marker="o", label="steady decrease")
    ax.plot(epochs, unstable_loss, marker="o", label="unstable")
    ax.set_xlabel("epoch")
    ax.set_ylabel("loss")
    ax.set_title("Loss curves can reveal training behavior")
    ax.legend()
    save_figure(fig, "basic-loss-curve-comparison")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", choices=["all", "ko", "en", "zh"], default="all")
    parser.add_argument("--output-dir", type=Path, default=OUT_DIR)
    parser.add_argument("--font-family", default=FONT_FAMILY)
    args = parser.parse_args()
    OUT_DIR = args.output_dir
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    LANGUAGES = ("ko", "en", "zh") if args.language == "all" else (args.language,)
    FONT_FAMILY = args.font_family
    plt.rcParams.update({"font.family": FONT_FAMILY, "font.size": 10,
                         "figure.figsize": (6.4, 4), "svg.hashsalt": "p2-13"})
    save_basic_line_function_shape()
    save_basic_scatter_relationship()
    save_basic_hist_distribution()
    save_basic_bar_model_comparison()
    save_basic_loss_curve_comparison()
