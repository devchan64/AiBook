"""绘制 P7-1.3 的中文基线设计比较图。"""
import csv, os
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]; CACHE=ROOT/".tmp"/"matplotlib-cache"; CACHE.mkdir(parents=True,exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR",str(CACHE)); os.environ.setdefault("XDG_CACHE_HOME",str(CACHE))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
ASSET=Path(__file__).resolve().parent; DATA=ASSET/"p7-1-traffic-log.csv"; OUT=ASSET/"p7-1-3-baseline-design-chart-zh.png"; DESIGNS=[("7 天基线\n7 天基线 / 7 天近期","2026-06-08"),("近期 4 天焦点\n10 天基线 / 4 天近期","2026-06-11")]
FONT=next((p for p in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc","/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"] if Path(p).exists()),None); CN=FontProperties(fname=FONT) if FONT else None
if FONT: font_manager.fontManager.addfont(FONT); plt.rcParams["font.family"]=CN.get_name()
def main():
 rows=list(csv.DictReader(DATA.open(encoding="utf-8")))
 for r in rows: r["date"]=datetime.strptime(r["date"],"%Y-%m-%d").date(); [r.__setitem__(c,int(r[c])) for c in ("visitors","signups","errors")]
 ads=[r for r in rows if r["channel"]=="ads"]; data=[]
 for name,cutoff_text in DESIGNS:
  cutoff=datetime.strptime(cutoff_text,"%Y-%m-%d").date(); base=[r for r in ads if r["date"]<cutoff]; recent=[r for r in ads if r["date"]>=cutoff]; rate=lambda items,col:sum(r[col] for r in items)/sum(r["visitors"] for r in items); data.append((name,(rate(recent,"signups")-rate(base,"signups"))*100,(rate(recent,"errors")-rate(base,"errors"))*100,len(base),len(recent)))
 fig,axes=plt.subplots(1,2,figsize=(10.8,4.8),dpi=180)
 for ax,key,title,color in ((axes[0],1,"广告转化率变化","#c2410c"),(axes[1],2,"广告错误率变化","#2563eb")):
  vals=[r[key] for r in data]; bars=ax.bar(range(2),vals,color=color,width=.58); ax.axhline(0,color="#6b7280",linewidth=1); ax.grid(axis="y",color="#d1d5db",linewidth=.7); ax.set_axisbelow(True); ax.spines[["top","right"]].set_visible(False); ax.set_title(title,fontproperties=CN,fontsize=14,pad=12); ax.set_ylabel("相对基线变化（百分点）"); ax.set_xticks(range(2),[r[0] for r in data],fontproperties=CN,fontsize=10)
  for bar in bars: value=bar.get_height(); ax.text(bar.get_x()+bar.get_width()/2,value+(-.18 if value<0 else .12),f"{value:+.2f}pp",ha="center",va="top" if value<0 else "bottom",fontsize=10,weight="bold")
 axes[0].set_ylim(-4.35,.8); axes[1].set_ylim(-.25,1.65)
 for pos,item in enumerate(data): axes[0].text(pos,.47,f"样本：{item[3]} 基线 / {item[4]} 近期",ha="center",fontsize=9,fontproperties=CN,color="#4b5563")
 fig.tight_layout(pad=1.4); fig.savefig(OUT,bbox_inches="tight"); plt.close(fig); print(f"saved={OUT.relative_to(ROOT)}")
if __name__=="__main__": main()
