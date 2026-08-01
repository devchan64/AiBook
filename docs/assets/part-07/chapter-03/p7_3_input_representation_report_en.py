"""Draw the English P7-3.3 input-representation report."""
import csv
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
MPL_CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CACHE)); os.environ.setdefault("XDG_CACHE_HOME", str(MPL_CACHE))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

ASSET_DIR = Path(__file__).resolve().parent
DATA_PATH = ASSET_DIR / "p7-3-surface-patches.csv"
OUTPUT_PATH = ASSET_DIR / "p7-3-input-representation-report-en.png"

def profile_column(matrix): return matrix.reshape(len(matrix), 8, 8).mean(axis=1)
def profile_center(matrix):
    images = matrix.reshape(len(matrix), 8, 8)
    return np.column_stack([images[:, :, 3:5].mean(axis=(1, 2)), images[:, :, :3].mean(axis=(1, 2)), images[:, :, 5:].mean(axis=(1, 2))])
def style(axis):
    axis.grid(True, axis="y", color="#d0d7de", linewidth=.75); axis.set_axisbelow(True); axis.spines[["top", "right"]].set_visible(False)
def main():
    rows = list(csv.DictReader(DATA_PATH.open(encoding="utf-8"))); columns = [n for n in rows[0] if n.startswith("pixel_")]
    train, test = [r for r in rows if r["split"] == "train"], [r for r in rows if r["split"] == "test"]
    matrix = lambda selected: np.array([[float(row[column]) for column in columns] for row in selected])
    raw_train, raw_test = matrix(train), matrix(test); y_train = np.array([int(r["label"]) for r in train]); y_test = np.array([int(r["label"]) for r in test])
    variants = {"64 raw pixels": (raw_train, raw_test), "8 column averages": (profile_column(raw_train), profile_column(raw_test)), "3 center-band values": (profile_center(raw_train), profile_center(raw_test))}; results=[]
    for name, (x_train, x_test) in variants.items():
        model=LogisticRegression(max_iter=1000,random_state=7).fit(x_train,y_train); pred=model.predict(x_test); margins=np.abs(model.predict_proba(x_test)[:,1]-model.predict_proba(x_test)[:,0])
        results.append({"name":name,"accuracy":accuracy_score(y_test,pred),"errors":int((pred != y_test).sum()),"low":int((margins < .25).sum()),"margins":margins})
    fig,(left,right)=plt.subplots(1,2,figsize=(11.8,4.4),dpi=180); names=[r["name"] for r in results]; x=np.arange(len(names)); width=.32
    left.bar(x-width/2,[r["errors"] for r in results],width,label="errors",color="#dc2626"); left.bar(x+width/2,[r["low"] for r in results],width,label="low-margin samples",color="#0f766e"); left.set(ylim=(0,4.6),ylabel="evaluation samples",title="Errors and low-margin samples"); left.set_xticks(x,names,rotation=10,ha="right"); left.legend(frameon=False,fontsize=8.5,loc="upper left"); style(left)
    positions=np.arange(len(test)); colors=["#2563eb","#ea580c","#0f766e"]
    for result,color in zip(results,colors): right.plot(positions,result["margins"],marker="o",linewidth=2,label=result["name"],color=color)
    labels = {"평가-정상-안정": "stable\nnormal", "평가-결함-명확": "clear\nscratch", "평가-결함-약함": "weak\nscratch", "평가-정상-그림자": "shadow\nnormal"}
    right.axhline(.25,color="#64748b",linestyle="--",linewidth=1.3,label="low-margin threshold"); right.set(ylim=(0,.7),ylabel="margin",title="Margin by evaluation patch"); right.set_xticks(positions,[labels[r["sample"]] for r in test],rotation=0,ha="center"); right.legend(frameon=False,fontsize=8.3,loc="upper right"); style(right)
    fig.suptitle("Image-classification report by input representation\nAll three test accuracies are 0.75",fontsize=15,fontweight="bold"); fig.tight_layout(pad=1,rect=(0,0,1,.91)); fig.savefig(OUTPUT_PATH,bbox_inches="tight"); plt.close(fig); print(f"saved={OUTPUT_PATH.relative_to(REPO_ROOT)}")
if __name__ == "__main__": main()
