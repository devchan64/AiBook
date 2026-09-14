"""Reproduce the Korean, English and Chinese P2-3.4 coordinate diagrams (Matplotlib required)."""
from pathlib import Path
import os
import math

OUT = Path(__file__).resolve().parent
os.environ.setdefault('MPLCONFIGDIR', str(OUT.parents[3] / '.tmp' / 'matplotlib-cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager


LABELS = {
    'ko': ['거리 1', '차이 1', 'q ↔ a: √2', '커피 구매량', '차 구매량', '길이 1인 원의 일부', '정규화한 첫 번째 성분', '정규화한 두 번째 성분'],
    'en': ['Distance 1', 'Δ = 1', 'q ↔ a: √2', 'Coffee (cups)', 'Tea (cups)', 'Part of the unit circle', 'Normalized first component', 'Normalized second component'],
    'zh': ['距离 1', '差值 1', 'q ↔ a: √2', '咖啡购买量（杯）', '茶购买量（杯）', '单位圆的一部分', '归一化后的第一分量', '归一化后的第二分量'],
}


def setup():
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in ('Noto Sans CJK KR', 'Noto Sans CJK JP', 'NanumGothic'):
        if name in available:
            plt.rcParams['font.family'] = name
            break
    else:
        raise RuntimeError('Install a Korean font such as Noto Sans CJK.')
    plt.rcParams.update({'font.size': 14, 'axes.unicode_minus': False})
    fig, ax = plt.subplots(figsize=(7, 6), layout='constrained')
    ax.set_aspect('equal')
    ax.grid(color='#e2e8f0', linewidth=.8)
    ax.set_axisbelow(True)
    return fig, ax


def arrow(ax, end, color, width=2):
    ax.annotate('', xy=end, xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color=color, lw=width))


def draw(lang):
    labels = LABELS[lang]
    q, a, b = (1, 1), (2, 2), (1, 0)
    fig, ax = setup()
    arrow(ax, a, '#16a34a', 7)
    arrow(ax, q, '#2563eb', 3)
    arrow(ax, b, '#475569')
    for name, point, offset in [('q = [1, 1]', q, (-105, 8)),
                                ('a = [2, 2]', a, (-100, 15)),
                                ('b = [1, 0]', b, (12, 12))]:
        ax.scatter(*point, s=42, color='#334155', zorder=4)
        ax.annotate(name, point, xytext=offset, textcoords='offset points')
    ax.plot([1, 1], [0, 1], '--', color='#dc2626', lw=2)
    ax.plot([1, 2], [1, 1], ':', color='#dc2626', lw=2)
    ax.plot([2, 2], [1, 2], ':', color='#dc2626', lw=2)
    ax.text(1.08, .43, labels[0], color='#b91c1c')
    ax.text(1.43, .85, labels[1], color='#b91c1c')
    ax.text(2.07, 1.43, labels[1], color='#b91c1c')
    # Offset dimension line keeps endpoint distance separate from origin vectors.
    ax.plot([1, .83], [1, 1.17], color='#dc2626', lw=1)
    ax.plot([2, 1.83], [2, 2.17], color='#dc2626', lw=1)
    ax.annotate('', xy=(1.83, 2.17), xytext=(.83, 1.17),
                arrowprops=dict(arrowstyle='<->', color='#dc2626', lw=1.7))
    ax.text(1.19, 1.7, labels[2], rotation=45, ha='center', color='#b91c1c',
            bbox=dict(facecolor='white', edgecolor='none', pad=2))
    ax.set(xlim=(-.15, 2.8), ylim=(-.22, 2.5), xlabel=labels[3], ylabel=labels[4])
    ax.set_xticks([0, 1, 2]); ax.set_yticks([0, 1, 2])
    fig.savefig(OUT / f'vector-distance-{lang}.png', dpi=160)
    plt.close(fig)

    fig, ax = setup()
    r = 1 / math.sqrt(2)
    theta = [i * math.pi / 200 for i in range(101)]
    ax.plot([math.cos(t) for t in theta], [math.sin(t) for t in theta],
            '--', color='#94a3b8', lw=1.5)
    arrow(ax, (r, r), '#2563eb', 3)
    arrow(ax, (1, 0), '#475569', 2)
    ax.scatter([r, 1], [r, 0], color=['#2563eb', '#475569'], zorder=4)
    ax.annotate('q, a, c\n[0.707, 0.707]', (r, r), xytext=(12, 10), textcoords='offset points')
    ax.annotate('b = [1, 0]', (1, 0), xytext=(-70, -30), textcoords='offset points')
    arc = [i * math.pi / 180 for i in range(46)]
    ax.plot([.3*math.cos(t) for t in arc], [.3*math.sin(t) for t in arc], color='#dc2626')
    ax.text(.32, .12, '45°', color='#b91c1c')
    ax.text(.12, 1.02, labels[5], color='#64748b')
    ax.set(xlim=(-.1, 1.4), ylim=(-.18, 1.22), xlabel=labels[6], ylabel=labels[7])
    ax.set_xticks([0, .5, 1]); ax.set_yticks([0, .5, 1])
    fig.savefig(OUT / f'vector-normalization-{lang}.png', dpi=160)
    plt.close(fig)


if __name__ == '__main__':
    for lang in LABELS:
        draw(lang)
