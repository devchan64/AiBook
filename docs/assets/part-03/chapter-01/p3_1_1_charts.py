"""Rebuild P3-1.1 flow charts from the manuscript's fictional measurements."""
from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR', '/tmp/aibook-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

OUT = Path(__file__).resolve().parent
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_manager.fontManager.addfont(FONT)
plt.rcParams.update({'font.family': font_manager.FontProperties(fname=FONT).get_name(),
                     'font.size': 13, 'axes.unicode_minus': False})
LABELS = {
 'ko': ('동작 시작 후 시간 (초)', '유량 (L/min)', '관측값', '마지막 관측 구간', '평균'),
 'en': ('Time since action start (s)', 'Flow (L/min)', 'Observed value', 'Last observed interval', 'Mean'),
 'zh': ('动作开始后的时间（秒）', '流量 (L/min)', '观测值', '最后观测区间', '均值'),
}

def main():
    for lang, (xlabel, ylabel, observed, last, avg) in LABELS.items():
        fig, axes = plt.subplots(2, 1, figsize=(7, 7), layout='constrained')
        for ax, name, y in zip(axes, ['A-101', 'A-102'], [[24.8,25.1,23.9],[24.7,24.8,24.8]]):
            ax.plot([0,1,2], y, color='#2463a4', lw=1.5, label=observed)
            ax.plot([1,2], y[1:], color='#b74427', lw=3.2, label=last)
            ax.scatter([0,1,2], y, color='#2463a4', s=55, zorder=4)
            m = np.mean(y)
            ax.axhline(m, color='#68717a', ls='--', lw=1.5, label=avg)
            ax.text(2.06, m - .22, f'{avg} {m:.2f}', va='center', fontsize=12)
            for x, v in zip([0,1,2], y):
                ax.annotate(f'{v:.1f}', (x,v), xytext=(0,10), textcoords='offset points', ha='center', fontsize=12)
            ax.set(xlim=(-.15,2.8), ylim=(23.55,25.55), xticks=[0,1,2], yticks=[24,24.5,25], ylabel=ylabel)
            ax.set_title(name, loc='left', weight='bold')
            ax.grid(alpha=.2)
            ax.spines[['top','right']].set_visible(False)
        axes[-1].set_xlabel(xlabel)
        axes[0].legend(loc='lower left', fontsize=10, frameon=False)
        fig.savefig(OUT / f'p3-1-1-flow-mean-{lang}.png', dpi=140, metadata={'Software':'Matplotlib'})
        plt.close(fig)

if __name__ == '__main__':
    main()
