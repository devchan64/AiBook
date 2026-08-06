"""Draw the English P7-3.1 patch-signal and scratch-probability chart."""
import csv, os
from pathlib import Path
REPO_ROOT=Path(__file__).resolve().parents[4]; CACHE=REPO_ROOT/".tmp"/"matplotlib-cache"; CACHE.mkdir(parents=True,exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR",str(CACHE)); os.environ.setdefault("XDG_CACHE_HOME",str(CACHE))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
ASSET_DIR=Path(__file__).resolve().parent; DATA=ASSET_DIR/"p7-3-surface-patches.csv"; OUT=ASSET_DIR/"p7-3-1-patch-signal-chart-en.png"
def softmax(values): values=values-values.max(axis=1,keepdims=True); ex=np.exp(values); return ex/ex.sum(axis=1,keepdims=True)
def main():
    cols=[f"pixel_{r}{c}" for r in range(8) for c in range(8)]; rows=[]
    for raw in csv.DictReader(DATA.open(encoding="utf-8")): rows.append({"split":raw["split"],"sample":raw["sample"],"label":int(raw["label"]),"image":np.array([float(raw[c]) for c in cols]).reshape(8,8)})
    train=[r for r in rows if r["split"]=="train"]; test=[r for r in rows if r["split"]=="test"]; x=np.array([r["image"].reshape(-1) for r in train]); y=np.array([r["label"] for r in train]); xt=np.array([r["image"].reshape(-1) for r in test]); W=np.zeros((64,2)); b=np.zeros(2); targets=np.eye(2)[y]
    for _ in range(700): p=softmax(x@W+b); W-=.35*x.T@(p-targets)/len(x); b-=.35*(p-targets).mean(axis=0)
    probabilities=softmax(xt@W+b); labels={"평가-정상-안정":"stable\nnormal","평가-결함-명확":"clear\nscratch","평가-결함-약함":"weak\nscratch","평가-정상-그림자":"shadow\nnormal"}; results=[]
    for row,probability in zip(test,probabilities):
        image=row["image"]; center=float(image[:,3:5].mean()); outside=float(np.concatenate((image[:,:3],image[:,5:]),axis=1).mean()); prediction=int(probability.argmax()); results.append((labels[row["sample"]],center,outside,center-outside,float(probability[1]),prediction==row["label"]))
    names=[r[0] for r in results]; pos=np.arange(len(names)); fig,(left,right)=plt.subplots(1,2,figsize=(11,4.9),dpi=180); width=.34
    left.bar(pos-width/2,[r[1] for r in results],width,label="mean of center two columns",color="#c2410c"); left.bar(pos+width/2,[r[2] for r in results],width,label="mean of outer six columns",color="#64748b")
    for p,r in zip(pos,results): left.text(p,max(r[1],r[2])+.035,f"Δ {r[3]:+.3f}",ha="center",fontsize=9.5,weight="bold",color="#b45309" if not r[5] else "#374151")
    left.set(title="Mean brightness by input location (center − surrounding)",ylabel="grayscale value",ylim=(0,.85)); left.set_xticks(pos,names); left.legend(frameon=False,loc="upper left")
    bars=right.bar(pos,[r[4] for r in results],color=["#15803d" if r[5] else "#dc2626" for r in results],width=.62); right.axhline(.5,color="#6b7280",linestyle="--",linewidth=1.2); right.text(3.35,.53,"decision boundary 0.5",ha="right",fontsize=9,color="#4b5563")
    for bar,r in zip(bars,results): right.text(bar.get_x()+bar.get_width()/2,bar.get_height()+.035,f"{r[4]:.3f}",ha="center",fontsize=10,weight="bold")
    right.set(title="Scratch-warning probability",ylabel="class-1 probability",ylim=(0,1.1)); right.set_xticks(pos,names); right.legend(handles=[Patch(color="#15803d",label="correct"),Patch(color="#dc2626",label="incorrect")],frameon=False,loc="upper left")
    for axis in (left,right): axis.grid(True,axis="y",color="#d1d5db",linewidth=.75); axis.set_axisbelow(True); axis.spines[["top","right"]].set_visible(False)
    fig.tight_layout(pad=1.3); fig.savefig(OUT,bbox_inches="tight"); plt.close(fig); print(f"saved={OUT.relative_to(REPO_ROOT)}")
if __name__=="__main__": main()
