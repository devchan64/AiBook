"""Reproduce the four-student example's full-batch gradient descent loss."""
from pathlib import Path
import os

OUT = Path(__file__).resolve().parent
PREVIEW = OUT.parents[3] / '.tmp' / 'p2-6-3-review'
PREVIEW.mkdir(parents=True, exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR', str(PREVIEW / 'mpl-cache'))

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt, font_manager
import numpy as np

LABELS = {
    'ko': ('갱신 횟수', '평균 제곱 오차 (MSE)', '전체 배치 경사하강법의 손실 기록'),
    'en': ('Number of updates', 'Mean squared error (MSE)', 'Loss history of full-batch gradient descent'),
    'zh': ('更新次数', '均方误差 (MSE)', '全批量梯度下降的损失记录'),
}


def loss_history(steps=20, learning_rate=0.01):
    x = np.array([1., 2., 3., 4.])
    y = np.array([55., 65., 80., 90.])
    parameters = np.array([8., 45.])
    losses = []
    for step in range(steps + 1):
        residual = parameters[0] * x + parameters[1] - y
        losses.append(np.mean(residual ** 2))
        if step < steps:
            gradient = np.array([2 * np.mean(residual * x), 2 * np.mean(residual)])
            parameters -= learning_rate * gradient
    return np.array(losses)


def main():
    losses = loss_history()
    fonts = {f.name for f in font_manager.fontManager.ttflist}
    for lang, (xlabel, ylabel, title) in LABELS.items():
        preferred = {'ko': 'Noto Sans CJK KR', 'en': 'DejaVu Sans', 'zh': 'Noto Sans CJK SC'}[lang]
        font = next((f for f in [preferred, 'Noto Sans CJK JP', 'DejaVu Sans'] if f in fonts))
        plt.rcParams.update({'font.family': font, 'svg.fonttype': 'none', 'svg.hashsalt': 'p2-6-3-loss'})
        fig, ax = plt.subplots(figsize=(7.2, 4.3), layout='constrained')
        ax.plot(np.arange(len(losses)), losses, 'o-', color='#2563eb', markersize=4)
        for step in [0, 1, 2]:
            ax.annotate(f'{losses[step]:.3f}', (step, losses[step]), xytext=(10, 5), textcoords='offset points', fontsize=11)
        ax.set(xlabel=xlabel, ylabel=ylabel, xlim=(-.6, 20.6), ylim=(0, 88))
        ax.set_xticks([0, 1, 2, 5, 10, 15, 20])
        ax.grid(alpha=.2)
        path = OUT / f'gradient-descent-training-loss-{lang}.svg'
        fig.savefig(path, metadata={'Date': None, 'Title': title, 'Description': 'a=8, b=45; learning rate=0.01; n=4; 20 updates.'})
        svg = path.read_text()
        svg = svg.replace('<defs>', f'<title>{title}</title><desc>{xlabel}; {ylabel}. a=8, b=45; η=0.01; n=4.</desc>\n <defs>', 1)
        path.write_text('\n'.join(line.rstrip() for line in svg.splitlines()) + '\n')
        fig.savefig(PREVIEW / f'training-loss-{lang}.png', dpi=120)
        plt.close(fig)


if __name__ == '__main__':
    main()
