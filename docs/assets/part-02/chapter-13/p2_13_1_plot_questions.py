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

LABELS = {'epoch': ('에폭', '轮次'), 'loss': ('손실', '损失'), 'score': ('점수', '分数'), 'count': ('개수', '数量'), 'study hours': ('공부 시간', '学习时间'), 'segment': ('구간', '区段'), 'signal level': ('신호값', '信号值'), 'action A': ('동작 A', '动作 A'), 'action B': ('동작 B', '动作 B'), 'attempt': ('시도', '尝试'), 'Loss decreases over epochs': ('에폭에 따른 손실 감소', '损失随轮次下降'), 'Same mean, different pattern': ('같은 평균, 다른 패턴', '平均值相同，模式不同'), 'Study hours and score': ('공부 시간과 점수', '学习时间与分数'), 'Full range: 0 to 100': ('전체 범위: 0~100', '完整范围：0～100'), 'Zoomed range: 79 to 84': ('확대 범위: 79~84', '放大范围：79～84'), 'Score distribution': ('점수 분포', '分数分布')}

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


def save_pyplot_loss_line():
    epochs = [1, 2, 3, 4, 5]
    loss = [2.40, 1.65, 1.12, 0.86, 0.79]

    fig, ax = plt.subplots()
    ax.plot(epochs, loss, marker="o")
    ax.set_xlabel("epoch")
    ax.set_ylabel("loss")
    ax.set_title("Loss decreases over epochs")
    save_figure(fig, "pyplot-loss-line")

def save_same_mean_pattern():
    steps = [1, 2, 3, 4]
    action_a = [1.0, 2.0, 2.0, 1.0]
    action_b = [1.5, 1.5, 1.5, 1.5]

    fig, ax = plt.subplots()
    ax.plot(steps, action_a, marker="o", label="action A")
    ax.plot(steps, action_b, marker="o", label="action B")
    ax.set_xlabel("segment")
    ax.set_ylabel("signal level")
    ax.set_title("Same mean, different pattern")
    ax.legend()
    save_figure(fig, "same-mean-pattern")

def save_pyplot_study_scatter():
    study_hours = [2, 4, 6, 8]
    scores = [62, 71, 82, 88]

    fig, ax = plt.subplots()
    ax.scatter(study_hours, scores)
    ax.set_xlabel("study hours")
    ax.set_ylabel("score")
    ax.set_title("Study hours and score")
    save_figure(fig, "pyplot-study-scatter")

def save_axis_range_comparison():
    attempts = [1, 2, 3, 4]
    scores = [80, 82, 81, 83]
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.6), sharex=True)
    for ax in axes:
        ax.plot(attempts, scores, marker="o")
        ax.set_xlabel("attempt")
        ax.set_ylabel("score")
    axes[0].set_ylim(0, 100)
    axes[0].set_title("Full range: 0 to 100")
    axes[1].set_ylim(79, 84)
    axes[1].set_title("Zoomed range: 79 to 84")
    fig.tight_layout()
    save_figure(fig, "axis-range-comparison")

def save_pyplot_score_hist():
    scores = [45, 62, 71, 73, 82, 88, 90]

    fig, ax = plt.subplots()
    ax.hist(scores, bins=5)
    ax.set_xlabel("score")
    ax.set_ylabel("count")
    ax.set_title("Score distribution")
    save_figure(fig, "pyplot-score-hist")

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
    save_pyplot_loss_line()
    save_same_mean_pattern()
    save_pyplot_study_scatter()
    save_axis_range_comparison()
    save_pyplot_score_hist()
