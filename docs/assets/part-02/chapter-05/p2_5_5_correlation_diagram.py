"""Compare Pearson correlation for the manuscript's linear and curved examples."""
from pathlib import Path
import os

OUT = Path(__file__).resolve().parent
PREVIEW = OUT.parents[3] / '.tmp' / 'p2-5-5-correlation'
PREVIEW.mkdir(parents=True, exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR', str(PREVIEW / 'mpl-cache'))
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt, font_manager
import numpy as np

LABELS = {
    'ko': ('직선 관계', '곡선 관계', '관측값 3개', '주어진 관계식'),
    'en': ('Linear relationship', 'Curved relationship', 'Three observations', 'Given relationship'),
    'zh': ('线性关系', '曲线关系', '三个观测值', '给定关系式'),
}


def main():
    x = np.array([-1., 0., 1.])
    grid = np.linspace(-1, 1, 201)
    fonts = {font.name for font in font_manager.fontManager.ttflist}
    for lang, labels in LABELS.items():
        candidates = ['DejaVu Sans'] if lang == 'en' else ['Noto Sans CJK KR' if lang == 'ko' else 'Noto Sans CJK SC', 'Noto Sans CJK JP', 'Arial Unicode MS']
        font = next((f for f in candidates if f in fonts), 'DejaVu Sans')
        plt.rcParams.update({'font.family': font, 'svg.fonttype': 'none', 'svg.hashsalt': 'p2-5-5-correlation'})
        fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.9), layout='constrained')
        for i, (ax, y, curve, formula) in enumerate(zip(axes, [2*x+4, x*x], [2*grid+4, grid*grid], ['$y=2x+4$', '$y=x^2$'])):
            r = np.corrcoef(x, y)[0, 1]
            ax.plot(grid, curve, '--', color='#64748b', label=labels[3])
            ax.scatter(x, y, s=65, color='#2563eb', zorder=3, label=labels[2])
            ax.set_title(f'{labels[i]}\n{formula},  r = {r:.0f}', fontsize=13)
            ax.set(xlabel='x', ylabel='y', xlim=(-1.3, 1.3))
            ax.set_xticks([-1, 0, 1])
            ax.set_ylim((1, 7) if i == 0 else (-.2, 1.4))
            ax.set_yticks([2, 4, 6] if i == 0 else [0, .5, 1])
            ax.grid(alpha=.2)
            ax.legend(loc='upper left', fontsize=9)
        path = OUT / f'linear-vs-curved-correlation-{lang}.svg'
        fig.savefig(path, metadata={'Date': None})
        path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
        fig.savefig(PREVIEW / f'{lang}.png', dpi=130)
        plt.close(fig)


if __name__ == '__main__':
    main()
