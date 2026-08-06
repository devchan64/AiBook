"""绘制 P7-4.2 的中文词汇覆盖与类别分数图。"""
import csv, os
from pathlib import Path
REPO_ROOT=Path(__file__).resolve().parents[4]; CACHE=REPO_ROOT/".tmp"/"matplotlib-cache"; CACHE.mkdir(parents=True,exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR",str(CACHE)); os.environ.setdefault("XDG_CACHE_HOME",str(CACHE))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Patch
import numpy as np
ASSET=Path(__file__).resolve().parent; DATA=ASSET/"p7-4-support-routing-dataset.csv"; OUT=ASSET/"p7-4-2-coverage-review-chart-zh.png"
FONT=next((p for p in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc","/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"] if Path(p).exists()),None); CN=FontProperties(fname=FONT) if FONT else None
if FONT: font_manager.fontManager.addfont(FONT); plt.rcParams["font.family"]=CN.get_name()
def records():
    rows=list(csv.DictReader(DATA.open(encoding="utf-8"))); train=[r for r in rows if r["split"]=="train"]; vocab={t for r in train for t in r["text"].split()}; profiles={0:{},1:{}}
    for row in train:
        for token in row["text"].split(): profiles[int(row["label"])][token]=profiles[int(row["label"])].get(token,0)+1
    result=[]
    for row in (r for r in rows if r["split"]=="test"):
        tokens=row["text"].split(); known=[t for t in tokens if t in vocab]; scores=[sum(profiles[label].get(t,0) for t in known) for label in (0,1)]
        result.append({"sample":row["sample_id"].replace("평가-","评估-"),"coverage":len(known)/len(tokens),"scores":scores,"correct":int(np.argmax(scores))==int(row["label"])})
    return result
def style(ax): ax.grid(True,axis="y",color="#d1d5db",linewidth=.75); ax.set_axisbelow(True); ax.spines[["top","right"]].set_visible(False)
def main():
    data=records(); pos=np.arange(len(data)); fig,(coverage,score)=plt.subplots(1,2,figsize=(11.8,4.8),dpi=180)
    coverage.bar(pos,[r["coverage"] for r in data],color=["#15803d" if r["correct"] else "#dc2626" for r in data],width=.64); coverage.axhline(.5,color="#64748b",linestyle="--",linewidth=1.3)
    coverage.set(ylim=(0,1.12),ylabel="训练词汇覆盖率"); coverage.set_title("各评估咨询的覆盖率",fontproperties=CN); coverage.set_xticks(pos,[r["sample"] for r in data],rotation=15,ha="right",fontproperties=CN); coverage.legend(handles=[Patch(color="#15803d",label="正确"),Patch(color="#dc2626",label="错误"),plt.Line2D([],[],color="#64748b",linestyle="--",label="低覆盖复核阈值")],frameon=False,loc="upper right",fontsize=8.5,prop=CN); style(coverage)
    focus=[r for r in data if r["sample"] in {"评估-05","评估-07"}]; p=np.arange(len(focus)); width=.30
    score.bar(p-width/2,[r["scores"][0] for r in focus],width,label="退款分数",color="#2563eb"); score.bar(p+width/2,[r["scores"][1] for r in focus],width,label="配送分数",color="#ea580c")
    for position,row in zip(p,focus): score.text(position,max(row["scores"])+.32,"正确" if row["correct"] else "错误",ha="center",weight="bold",fontproperties=CN,color="#15803d" if row["correct"] else "#dc2626")
    score.set(ylim=(0,8.2),ylabel="训练词汇分数"); score.set_title("同样低覆盖，不同类别分数",fontproperties=CN); score.set_xticks(p,["评估-05\n取消 + 追踪","评估-07\n缺陷 + 退款"],fontproperties=CN); score.legend(frameon=False,loc="upper left",prop=CN); style(score)
    fig.suptitle("低覆盖不是一种单一失败",fontsize=15,fontweight="bold",fontproperties=CN); fig.tight_layout(pad=1,rect=(0,0,1,.92)); fig.savefig(OUT,bbox_inches="tight"); plt.close(fig); print(f"saved={OUT.relative_to(REPO_ROOT)}")
if __name__=="__main__": main()
