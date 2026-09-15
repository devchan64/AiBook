"""Generate localized loss contours and unit direction vectors for P2-4.3."""
from pathlib import Path
import os
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent
CACHE = OUT.parents[3] / '.tmp' / 'p2-4-3-diagrams'
CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR', str(CACHE / 'mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

LABELS = {
    'ko': ('손실 등고선과 방향', '현재 위치', '증가', '감소', '모든 화살표 길이 = 1'),
    'en': ('Loss contours and directions', 'Current position', 'Increase', 'Decrease', 'All arrow lengths = 1'),
    'zh': ('损失等高线与方向', '当前位置', '增加', '减少', '所有箭头长度 = 1'),
}


def draw(lang):
    title, current, increase, decrease, note = LABELS[lang]
    available = {f.name for f in font_manager.fontManager.ttflist}
    font = next(n for n in ('Noto Sans CJK KR', 'Noto Sans CJK JP', 'DejaVu Sans') if n in available)
    plt.rcParams.update({'font.family': font,
                         'font.size': 14, 'axes.unicode_minus': False,
                         'svg.hashsalt': 'p2-4-3'})
    fig, ax = plt.subplots(figsize=(8, 6.8), layout='constrained')
    x = np.linspace(0, 6, 501)
    xx, yy = np.meshgrid(x, x)
    contours = ax.contour(xx, yy, xx**2 + yy**2, levels=[9, 16, 25, 36, 49],
                          colors=['#2563eb'], linewidths=1.3)
    ax.clabel(contours, inline=True, fontsize=13, fmt=lambda z: f'L={z:g}',
              manual=[(2.8, 1), (3.9, .9), (4.9, 1), (5.6, 2.1), (5.5, 4.3)])
    start = np.array([3., 4.])
    for direction, color, style in [([1, 0], '#64748b', '--'),
                                     ([0, 1], '#64748b', '--'),
                                     ([.6, .8], '#b91c1c', '-'),
                                     ([-.6, -.8], '#15803d', '-')]:
        end = start + direction
        ax.annotate('', xy=end, xytext=start,
                    arrowprops=dict(arrowstyle='->', color=color, lw=2.4,
                                    linestyle=style, shrinkA=0, shrinkB=0))
    box = dict(facecolor='white', edgecolor='none', alpha=.95, pad=2)
    ax.text(4.05, 3.85, '[1, 0]', color='#475569', bbox=box)
    ax.text(2.85, 5.2, '[0, 1]', color='#475569', ha='center', bbox=box)
    ax.text(3.8, 4.85, increase+'\n[0.6, 0.8]', color='#b91c1c', bbox=box)
    ax.text(1.35, 2.75, decrease+'\n[-0.6, -0.8]', color='#15803d', bbox=box)
    ax.scatter(*start, s=45, color='#111827', zorder=6)
    ax.annotate(current+' [3, 4]', xy=start, xytext=(.25, 4.35), fontsize=13,
                arrowprops=dict(arrowstyle='-', color='#475569'), bbox=box)
    ax.text(.2, .2, note, fontsize=13, bbox=box)
    ax.set(xlim=(0, 6), ylim=(0, 6), xlabel=r'$w_1$', ylabel=r'$w_2$', aspect='equal')
    ax.set_xticks(range(7)); ax.set_yticks(range(7))
    ax.grid(color='#e2e8f0', alpha=.65); ax.set_axisbelow(True)
    path = OUT / f'gradient-directions-{lang}.svg'
    fig.savefig(path, metadata={'Date': None})
    fig.savefig(CACHE / f'gradient-directions-{lang}.png', dpi=110)
    plt.close(fig)
    ns = 'http://www.w3.org/2000/svg'
    ET.register_namespace('', ns)
    tree = ET.parse(path)
    root = tree.getroot()
    root.set('role', 'img'); root.set('aria-labelledby', 'title desc')
    for tag, text in [('title', title), ('desc', f'L=w₁²+w₂²; {current}: [3,4]; {note}.')]:
        node = ET.Element('{'+ns+'}'+tag, id=tag)
        node.text = text
        root.insert(0, node)
    tree.write(path, encoding='utf-8', xml_declaration=True)
    path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')


if __name__ == '__main__':
    for language in LABELS:
        draw(language)
