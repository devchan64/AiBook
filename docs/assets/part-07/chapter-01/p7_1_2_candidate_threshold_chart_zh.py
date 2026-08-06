"""绘制 P7-1.2 的中文候选阈值图。"""
import csv, os
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]; CACHE=ROOT/".tmp"/"matplotlib-cache"; CACHE.mkdir(parents=True,exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR",str(CACHE)); os.environ.setdefault("XDG_CACHE_HOME",str(CACHE))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle
ASSET=Path(__file__).resolve().parent; DATA=ASSET/"p7-1-traffic-log.csv"; OUT=ASSET/"p7-1-2-candidate-threshold-chart-zh.png"; COLORS={"organic":"#2f855a","search":"#2563eb","ads":"#c2410c"}; NAMES={"organic":"自然","search":"搜索","ads":"广告"}
FONT=next((p for p in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc","/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"] if Path(p).exists()),None); CN=FontProperties(fname=FONT) if FONT else None
if FONT: font_manager.fontManager.addfont(FONT); plt.rcParams["font.family"]=CN.get_name()
def main():
 rows=list(csv.DictReader(DATA.open(encoding="utf-8"))); totals=defaultdict(lambda:{"visitors":0,"signups":0,"errors":0})
 for row in rows:
  for key in ("visitors","signups","errors"): row[key]=int(row[key])
  if row["date"]<"2026-06-08":
   for key in ("visitors","signups","errors"): totals[row["channel"]][key]+=row[key]
 points=[]
 for row in rows:
  if row["date"]>="2026-06-08":
   base=totals[row["channel"]]; conversion=(row["signups"]/row["visitors"]-base["signups"]/base["visitors"])*100; error=(row["errors"]/row["visitors"]-base["errors"]/base["visitors"])*100; points.append((row["date"],row["channel"],conversion,error,conversion<=-3.5 and error>=1.2))
 fig,ax=plt.subplots(figsize=(8.8,5.4),dpi=180); ax.add_patch(Rectangle((-5.1,1.2),1.6,1.1,facecolor="#fee2e2",edgecolor="none",alpha=.7)); ax.text(-4.98,2.17,"共同候选区域",color="#991b1b",fontsize=10,weight="bold",fontproperties=CN)
 for channel,color in COLORS.items():
  selected=[p for p in points if p[1]==channel]; ax.scatter([p[2] for p in selected],[p[3] for p in selected],label=NAMES[channel],color=color,s=46,edgecolor="white",linewidth=.7)
 for date,channel,x,y,candidate in points:
  if candidate: ax.annotate(date[5:],(x,y),xytext=(7,6),textcoords="offset points",fontsize=9,color="#7c2d12",weight="bold")
 for x,color in ((-3.5,"#dc2626"),(-2.5,"#2563eb")): ax.axvline(x,color=color,linestyle="--",linewidth=1.4)
 for y,color in ((.9,"#dc2626"),(1.2,"#2563eb")): ax.axhline(y,color=color,linestyle="--",linewidth=1.4)
 ax.set(xlim=(-5.1,1.15),ylim=(-.65,2.3),xlabel="相对基线的转化率变化（百分点）",ylabel="相对基线的错误率变化（百分点）"); ax.grid(True,color="#d1d5db",linewidth=.7); ax.set_axisbelow(True); ax.spines[["top","right"]].set_visible(False); ax.legend(title="渠道",frameon=False,loc="lower right",prop=CN); fig.tight_layout(pad=1.2); fig.savefig(OUT,bbox_inches="tight"); plt.close(fig); print(f"saved={OUT.relative_to(ROOT)}")
if __name__=="__main__": main()
