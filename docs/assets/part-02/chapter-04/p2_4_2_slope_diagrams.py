"""Reproduce the P2-4.2 diagrams in three languages using function values."""
from pathlib import Path
import os
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent
CACHE = OUT.parents[3] / '.tmp' / 'p2-4-2-diagrams'
CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR', str(CACHE / 'matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

TEXT = {
    'ko': ('입력 x', '출력 y', '구간', '평균 변화율', '직선의 일정한 기울기', '곡선의 구간별 평균 변화율'),
    'en': ('Input x', 'Output y', 'Interval', 'Average rate', 'Constant slope of a line', 'Average rates over curve intervals'),
    'zh': ('输入 x', '输出 y', '区间', '平均变化率', '直线的恒定斜率', '曲线各区间的平均变化率'),
}


def draw(lang, curved):
    available = {f.name for f in font_manager.fontManager.ttflist}
    font = next((n for n in ('Noto Sans CJK KR', 'Noto Sans CJK JP', 'DejaVu Sans') if n in available))
    plt.rcParams.update({'font.family': font, 'font.size': 13, 'axes.unicode_minus': False,
                         'svg.hashsalt': 'p2-4-2'})
    xlabel, ylabel, interval, rate, line_title, curve_title = TEXT[lang]
    f = (lambda x: x*x) if curved else (lambda x: 2*x+1)
    xs = [i / 100 for i in range(321)]
    fig, ax = plt.subplots(figsize=(7.6, 5.4), layout='constrained')
    ax.plot(xs, [f(x) for x in xs], color='#2563eb', lw=2.5,
            label='y = x²' if curved else 'y = 2x + 1')
    for a, b, color in [(0, 1, '#15803d'), (2, 3, '#b91c1c')]:
        slope = (f(b)-f(a))/(b-a)
        ax.plot([a,b], [f(a),f(b)], '--', color=color, lw=2,
                label=f'{interval} [{a}, {b}]: {rate} {slope:g}')
        ax.plot([a,b,b], [f(a),f(a),f(b)], ':', color=color, lw=1.5)
        ax.text((a+b)/2, f(a)-.48, 'Δx = 1', ha='center', color=color)
        ax.text(b+.1, (f(a)+f(b))/2, f'Δy = {f(b)-f(a):g}', color=color,
                bbox=dict(facecolor='white', edgecolor='none', pad=1))
    for x in range(4):
        ax.scatter(x, f(x), s=30, color='#1f2937', zorder=5)
    ax.set(xlim=(-.3,3.9), ylim=(-1,11), xlabel=xlabel, ylabel=ylabel)
    ax.set_xticks(range(4)); ax.set_yticks(range(0,11))
    ax.grid(color='#e2e8f0'); ax.set_axisbelow(True)
    ax.legend(loc='upper left', fontsize=11)
    name=('curve-slope-changing' if curved else 'linear-slope-constant')+'-'+lang
    path=OUT/(name+'.svg')
    fig.savefig(path, metadata={'Date': None})
    fig.savefig(CACHE/(name+'.png'), dpi=120)
    plt.close(fig)
    # Add accessible descriptions without changing the rendered geometry.
    ns='http://www.w3.org/2000/svg'
    ET.register_namespace('', ns)
    tree=ET.parse(path); root=tree.getroot()
    root.set('role','img'); root.set('aria-labelledby','title desc')
    title=ET.Element('{'+ns+'}title',id='title')
    title.text=curve_title if curved else line_title
    desc=ET.Element('{'+ns+'}desc',id='desc')
    desc.text=f'{"y=x²" if curved else "y=2x+1"}; {interval} [0,1], [2,3]; {rate} {1 if curved else 2}, {5 if curved else 2}.'
    root.insert(0,title); root.insert(1,desc)
    tree.write(path,encoding='utf-8',xml_declaration=True)
    path.write_text('\n'.join(line.rstrip() for line in path.read_text(encoding='utf-8').splitlines()) + '\n', encoding='utf-8')


if __name__ == '__main__':
    for language in TEXT:
        for curved in (False, True):
            draw(language, curved)
