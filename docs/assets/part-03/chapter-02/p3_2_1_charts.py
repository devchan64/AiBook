"""Rebuild P3-2.1 observed-interval charts; lines join measurements only."""
from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR', '/tmp/aibook-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

OUT = Path(__file__).resolve().parent
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_manager.fontManager.addfont(FONT)
plt.rcParams.update({'font.family': font_manager.FontProperties(fname=FONT).get_name(),
                     'font.size':13, 'axes.unicode_minus':False})
LABELS = {
 'ko': ('동작 시작 후 시간 (초)', '유량 (L/min)', '관측점', '마지막 관측 구간', '이후 기록 없음', '기존 시각', '변경 시각', '점 수', '기울기'),
 'en': ('Time since action start (s)', 'Flow (L/min)', 'Observations', 'Last observed interval', 'No later records', 'Original times', 'Changed times', 'Points', 'Slope'),
 'zh': ('动作开始后的时间（秒）', '流量 (L/min)', '观测点', '最后观测区间', '无后续记录', '原始时刻', '修改后的时刻', '点数', '斜率'),
}

def style(ax, xlabel, ylabel, xmax):
    ax.set(xlim=(-.12,xmax), ylim=(.4,1.65), yticks=[.5,1,1.5], ylabel=ylabel)
    ax.grid(alpha=.2)
    ax.spines[['top','right']].set_visible(False)

def main():
    for lang, (xlabel,ylabel,obs,last,missing,original,changed,points,slope) in LABELS.items():
        fig, axes = plt.subplots(3,1,figsize=(7,8.8),layout='constrained')
        for ax, name, x, y in zip(axes, ['A','B','C'], [[0,1,2],[0,1,2],[0,1]], [[.8,1.4,1.2],[.7,1.1,.6],[.9,1.0]]):
            ax.plot(x,y,color='#2463a4',lw=1.5)
            ax.plot(x[-2:],y[-2:],color='#b74427',lw=3.5,label=last)
            ax.scatter(x,y,color='#2463a4',s=55,zorder=4,label=obs)
            for t,v in zip(x,y):
                ax.annotate(f'{v:.1f}',(t,v),xytext=(0,10),textcoords='offset points',ha='center',fontsize=12)
            ax.set_title(f'{name} · {points}: {len(x)}',loc='left',weight='bold')
            ax.text(.98,.88,f'{x[-2]}–{x[-1]} s',transform=ax.transAxes,ha='right',color='#b74427')
            style(ax,xlabel,ylabel,2.35)
            ax.set_xticks([0,1,2])
            if name=='C':
                ax.axvspan(1.03,2.35,color='#eeeeee',zorder=0)
                ax.text(1.7,.65,missing,ha='center',fontsize=12,color='#535b63')
        axes[-1].set_xlabel(xlabel)
        axes[0].legend(loc='lower left',frameon=False,fontsize=10)
        fig.savefig(OUT / f'p3-2-1-observed-intervals-{lang}.png',dpi=140,metadata={'Software':'Matplotlib'})
        plt.close(fig)
        fig, axes = plt.subplots(2,1,figsize=(7,7),layout='constrained')
        for ax, x, title in zip(axes, [[0,1,2],[0,1,4]], [original,changed]):
            y=[.8,1.4,1.2]
            ax.plot(x,y,color='#2463a4',lw=1.5)
            ax.plot(x[-2:],y[-2:],color='#b74427',lw=3.5)
            ax.scatter(x,y,color='#2463a4',s=55,zorder=4)
            for t,v in zip(x,y):
                ax.annotate(f'{v:.1f}',(t,v),xytext=(0,10),textcoords='offset points',ha='center',fontsize=12)
            dt=x[-1]-x[-2]; rate=(y[-1]-y[-2])/dt
            ax.annotate('',(x[-1],.65),(x[-2],.65),arrowprops={'arrowstyle':'<->','color':'#b74427'})
            ax.text((x[-1]+x[-2])/2,.49,f'Δt = {dt} s',ha='center',color='#b74427')
            ax.text(.98,.89,f'{slope}: {rate:.3f} L/min/s',transform=ax.transAxes,ha='right',fontsize=12)
            ax.set_title(f'A · {title}',loc='left',weight='bold')
            style(ax,xlabel,ylabel,4.35)
            ax.set_xticks([0,1,2,3,4])
        axes[-1].set_xlabel(xlabel)
        fig.savefig(OUT / f'p3-2-1-time-spacing-{lang}.png',dpi=140,metadata={'Software':'Matplotlib'})
        plt.close(fig)

if __name__=='__main__':
    main()
