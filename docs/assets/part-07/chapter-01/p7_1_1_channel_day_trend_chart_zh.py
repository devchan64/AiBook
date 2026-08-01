"""绘制 P7-1.1 的中文渠道日趋势图。"""
import csv, os
from collections import defaultdict
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]; CACHE=ROOT/".tmp"/"matplotlib-cache"; CACHE.mkdir(parents=True,exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR",str(CACHE)); os.environ.setdefault("XDG_CACHE_HOME",str(CACHE))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
ASSET=Path(__file__).resolve().parent; DATA=ASSET/"p7-1-traffic-log.csv"; OUT=ASSET/"p7-1-1-channel-day-trend-chart-zh.png"; CUTOFF=datetime.strptime("2026-06-08","%Y-%m-%d").date(); COLORS={"organic":"#2f855a","search":"#2563eb","ads":"#c2410c"}; NAMES={"organic":"自然","search":"搜索","ads":"广告"}
FONT=next((p for p in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc","/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"] if Path(p).exists()),None); CN=FontProperties(fname=FONT) if FONT else None
if FONT: font_manager.fontManager.addfont(FONT); plt.rcParams["font.family"]=CN.get_name()
def rate(rows,col): return sum(r[col] for r in rows)/sum(r["visitors"] for r in rows)*100
def main():
 rows=list(csv.DictReader(DATA.open(encoding="utf-8"))); groups=defaultdict(list)
 for row in rows:
  row["date"]=datetime.strptime(row["date"],"%Y-%m-%d").date()
  for key in ("visitors","signups","errors"): row[key]=int(row[key])
  groups[row["channel"]].append(row)
 fig,(top,bottom)=plt.subplots(2,1,figsize=(10.5,7),dpi=180,sharex=True)
 for ax in (top,bottom): ax.axvspan(CUTOFF,max(r["date"] for r in rows),color="#fef3c7",alpha=.62); ax.axvline(CUTOFF,color="#6b7280",linestyle="--",linewidth=1.2); ax.grid(True,color="#d1d5db",linewidth=.7); ax.set_axisbelow(True); ax.spines[["top","right"]].set_visible(False)
 for channel,items in sorted(groups.items()):
  items.sort(key=lambda r:r["date"]); dates=[r["date"] for r in items]; color=COLORS[channel]; top.plot(dates,[r["signups"]/r["visitors"]*100 for r in items],marker="o",markersize=3.7,linewidth=2,color=color,label=NAMES[channel]); bottom.plot(dates,[r["errors"]/r["visitors"]*100 for r in items],marker="o",markersize=3.7,linewidth=2,color=color,label=NAMES[channel]); base=[r for r in items if r["date"]<CUTOFF]; top.hlines(rate(base,"signups"),min(dates),CUTOFF,color=color,linestyle=":",linewidth=1.6); bottom.hlines(rate(base,"errors"),min(dates),CUTOFF,color=color,linestyle=":",linewidth=1.6)
 top.text(CUTOFF,12.7,"近期区间开始",color="#4b5563",fontsize=10,ha="left",va="bottom",fontproperties=CN); top.set_ylabel("转化率（%）"); bottom.set_ylabel("错误率（%）"); bottom.set_xlabel("日期"); top.legend(title="渠道",frameon=False,loc="lower left",ncol=3,prop=CN); bottom.xaxis.set_major_locator(mdates.DayLocator(interval=1)); bottom.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d")); fig.autofmt_xdate(rotation=0); fig.tight_layout(pad=1.3); fig.savefig(OUT,bbox_inches="tight"); plt.close(fig); print(f"saved={OUT.relative_to(ROOT)}")
if __name__=="__main__": main()
