"""绘制 P7-2.1 的中文预测转变图。"""
import csv, os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]; CACHE=ROOT/".tmp"/"matplotlib-cache"; CACHE.mkdir(parents=True,exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR",str(CACHE)); os.environ.setdefault("XDG_CACHE_HOME",str(CACHE))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
ASSET=Path(__file__).resolve().parent; DATA=ASSET/"p7-2-churn-dataset.csv"; OUT=ASSET/"p7-2-1-prediction-outcome-transition-zh.png"; FEATURES=["unresolved_tickets","days_since_login","usage_minutes_30d"]
FONT=next((p for p in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc","/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"] if Path(p).exists()),None); CN=FontProperties(fname=FONT) if FONT else None
if FONT: font_manager.fontManager.addfont(FONT); plt.rcParams["font.family"]=CN.get_name()
def main():
 rows=list(csv.DictReader(DATA.open(encoding="utf-8")))
 for r in rows:
  for key in FEATURES+["label"]: r[key]=int(r[key])
 train=[r for r in rows if r["split"]=="train"]; test=[r for r in rows if r["split"]=="test"]; raw=[min(train,key=lambda candidate:sum((row[key]-candidate[key])**2 for key in FEATURES))["label"] for row in test]; groups={"均正确":[],"1-NN 恢复":[],"1-NN 新错误":[],"两者都错":[]}
 for row,candidate in zip(test,raw):
  base_ok=0==row["label"]; candidate_ok=candidate==row["label"]; key="均正确" if base_ok and candidate_ok else "1-NN 恢复" if not base_ok and candidate_ok else "1-NN 新错误" if base_ok else "两者都错"; groups[key].append(row["sample_id"].replace("평가-","评估-"))
 names=list(groups); counts=[len(groups[n]) for n in names]; fig,ax=plt.subplots(figsize=(9.5,5),dpi=180); bars=ax.bar(names,counts,color=["#15803d","#2563eb","#dc2626","#64748b"],width=.64)
 for bar,name,count in zip(bars,names,counts): ax.text(bar.get_x()+bar.get_width()/2,count+.08,", ".join(groups[name]) if count else "无",ha="center",va="bottom",fontsize=9,fontproperties=CN)
 ax.set(ylim=(0,max(counts)+.9),ylabel="评估样本数"); ax.set_title("预测转变：仅保留基线与原始 1-NN",fontproperties=CN); ax.set_xticks(range(len(names)),names,fontproperties=CN); ax.grid(True,axis="y",color="#d1d5db",linewidth=.75); ax.set_axisbelow(True); ax.spines[["top","right"]].set_visible(False); fig.tight_layout(); fig.savefig(OUT,bbox_inches="tight"); plt.close(fig); print(f"saved={OUT.relative_to(ROOT)}")
if __name__=="__main__": main()
