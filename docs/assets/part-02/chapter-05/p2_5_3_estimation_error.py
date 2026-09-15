"""Draw signed estimation errors on one shared numerical scale."""
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[4]
PREVIEW = ROOT / '.tmp' / 'p2-5-3-review'
PREVIEW.mkdir(parents=True, exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR', str(PREVIEW / 'mpl-cache'))
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt, font_manager

OUT = Path(__file__).resolve().parent
TEXT = {
    'ko': ('추정값 A: 47', '참값: 50', '추정값 B: 53', '평균 사용 시간(분)', '오차 = 추정값 − 참값'),
    'en': ('Estimate A: 47', 'True value: 50', 'Estimate B: 53', 'Mean usage time (minutes)', 'Error = estimate − true value'),
    'zh': ('估计值 A：47', '真值：50', '估计值 B：53', '平均使用时长（分钟）', '误差 = 估计值 − 真值'),
}


def main():
    available = {font.name for font in font_manager.fontManager.ttflist}
    for lang, labels in TEXT.items():
        candidates = ['DejaVu Sans'] if lang == 'en' else ['Noto Sans CJK KR' if lang == 'ko' else 'Noto Sans CJK SC', 'Noto Sans CJK JP', 'Arial Unicode MS']
        plt.rcParams['font.family'] = next((font for font in candidates if font in available), 'DejaVu Sans')
        plt.rcParams['svg.fonttype'] = 'none'
        fig, ax = plt.subplots(figsize=(8, 3.4), dpi=160)
        for value, label, color in zip([47, 50, 53], labels[:3], ['#2563eb', '#047857', '#2563eb']):
            ax.plot([value, value], [0, .45], color=color, linewidth=2)
            ax.scatter([value], [0], color=color, s=55, zorder=3)
            ax.text(value, .52, label, ha='center', va='bottom', color=color, fontsize=11)
        for estimate, y in [(47, -.43), (53, -.84)]:
            ax.annotate('', xy=(estimate, y), xytext=(50, y), arrowprops=dict(arrowstyle='->', lw=2, color='#b91c1c'))
            ax.text((estimate+50)/2, y+.08, f'{estimate} − 50 = {estimate-50:+d}'.replace('-3', '−3'), ha='center', color='#b91c1c', fontsize=11)
        ax.set_xlim(45.5,54.5)
        ax.set_ylim(-1.1,.95)
        ax.spines['bottom'].set_position(('data',0))
        for side in ['left','right','top']:
            ax.spines[side].set_visible(False)
        ax.set_xticks(range(46,55))
        ax.set_yticks([])
        ax.set_xlabel(labels[3])
        ax.xaxis.set_label_coords(.5,-.06)
        ax.set_title(labels[4],fontsize=13,pad=10)
        fig.tight_layout()
        fig.subplots_adjust(bottom=.18)
        stem=f'estimate-error-gap-{lang}'
        svg = OUT / f'{stem}.svg'
        fig.savefig(svg)
        svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines()) + '\n')
        fig.savefig(PREVIEW / f'{stem}.png')
        plt.close(fig)


if __name__ == '__main__':
    main()
