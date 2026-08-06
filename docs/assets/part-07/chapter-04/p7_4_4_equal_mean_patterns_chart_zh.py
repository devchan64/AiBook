"""绘制 P7-4.4 的中文同均值模式比较图。"""
import csv, os
from pathlib import Path
REPO_ROOT=Path(__file__).resolve().parents[4]; CACHE=REPO_ROOT/".tmp"/"matplotlib-cache"; CACHE.mkdir(parents=True,exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR",str(CACHE)); os.environ.setdefault("XDG_CACHE_HOME",str(CACHE))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
ASSET=Path(__file__).resolve().parent; DATA=ASSET/"p7-action-unit-pattern-pairs.csv"; OUT=ASSET/"p7-4-4-equal-mean-patterns-chart-zh.png"
FONT=next((p for p in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc","/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"] if Path(p).exists()),None); CN=FontProperties(fname=FONT) if FONT else None
if FONT: font_manager.fontManager.addfont(FONT); plt.rcParams["font.family"]=CN.get_name()
COLORS={"rising":"#2563eb","flat":"#64748b","falling":"#dc2626","middle_high":"#7c3aed","edge_high":"#0f766e"}; SHAPES={"rising":"上升","flat":"平坦","falling":"下降","middle_high":"中间高","edge_high":"两端高"}
def main():
 rows=list(csv.DictReader(DATA.open(encoding="utf-8"))); records=[{"id":r["event_id"],"shape":r["expected_shape"],"values":[float(r[f"segment_{i}"]) for i in range(1,5)]} for r in rows if r["event_id"] in {f"PAT-{i:02d}" for i in range(1,7)}]
 fig,axes=plt.subplots(2,3,figsize=(11.8,6.5),dpi=180,sharex=True,sharey=True)
 for axis,record in zip(axes.flat,records):
  shape=record["shape"]; axis.plot([1,2,3,4],record["values"],color=COLORS[shape],marker="o",linewidth=2.4); axis.axhline(2.5,color="#64748b",linestyle="--",linewidth=1.1,label="平均值 2.5"); axis.set_title(f"{record['id']} · {SHAPES[shape]}",fontproperties=CN,fontsize=11.5,pad=8); axis.set_xticks([1,2,3,4]); axis.set_ylim(1.5,3.55); axis.grid(True,axis="y",color="#d1d5db",linewidth=.75); axis.spines[["top","right"]].set_visible(False)
 for axis in axes[:,0]: axis.set_ylabel("分段值")
 for axis in axes[1,:]: axis.set_xlabel("分段顺序")
 axes[0,2].legend(frameon=False,loc="upper right",fontsize=8.5,prop=CN); fig.suptitle("相同均值 2.5，不同序列模式",fontsize=16,fontweight="bold",fontproperties=CN); fig.tight_layout(pad=1.2,rect=(0,0,1,.94)); fig.savefig(OUT,bbox_inches="tight"); plt.close(fig); print(f"saved={OUT.relative_to(REPO_ROOT)}")
if __name__=="__main__": main()
