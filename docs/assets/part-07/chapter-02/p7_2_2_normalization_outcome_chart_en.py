"""Draw the English P7-2.2 raw-versus-scaled 1-NN transition chart."""
from collections import defaultdict
import csv
import os
from pathlib import Path
REPO_ROOT=Path(__file__).resolve().parents[4]; MPL_CACHE=REPO_ROOT/".tmp"/"matplotlib-cache"; MPL_CACHE.mkdir(parents=True,exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR",str(MPL_CACHE)); os.environ.setdefault("XDG_CACHE_HOME",str(MPL_CACHE))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
ASSET_DIR=Path(__file__).resolve().parent; DATA_PATH=ASSET_DIR/"p7-2-churn-dataset.csv"; OUTPUT_PATH=ASSET_DIR/"p7-2-2-normalization-outcome-chart-en.png"
FEATURES=["unresolved_tickets","days_since_login","usage_minutes_30d"]
ORDER=["both correct","recovered\nby scaling","newly wrong\nafter scaling","wrong\nunder both"]
COLORS=["#64748b","#15803d","#dc2626","#d97706"]
def main():
    rows=list(csv.DictReader(DATA_PATH.open(encoding="utf-8")))
    for row in rows:
        for column in FEATURES+["label"]: row[column]=int(row[column])
    train=[r for r in rows if r["split"]=="train"]; test=[r for r in rows if r["split"]=="test"]
    matrix=lambda selected:np.array([[row[column] for column in FEATURES] for row in selected],dtype=float)
    x_train,x_test=matrix(train),matrix(test); y_train=np.array([r["label"] for r in train]); y_test=np.array([r["label"] for r in test])
    raw=KNeighborsClassifier(n_neighbors=1).fit(x_train,y_train).predict(x_test); scaled=Pipeline([("scaler",StandardScaler()),("knn",KNeighborsClassifier(n_neighbors=1))]).fit(x_train,y_train).predict(x_test)
    outcomes=defaultdict(list)
    for row,before,after,actual in zip(test,raw,scaled,y_test):
        key="recovered\nby scaling" if before!=actual and after==actual else "newly wrong\nafter scaling" if before==actual and after!=actual else "both correct" if before==actual else "wrong\nunder both"
        outcomes[key].append(row["sample_id"].replace("평가-","test-"))
    counts=[len(outcomes[key]) for key in ORDER]; fig,axis=plt.subplots(figsize=(8.8,4.8),dpi=180); bars=axis.bar(ORDER,counts,color=COLORS,width=.62)
    for bar,count,key in zip(bars,counts,ORDER):
        axis.annotate(str(count),(bar.get_x()+bar.get_width()/2,count),xytext=(0,6),textcoords="offset points",ha="center",fontsize=12,weight="bold")
        axis.annotate(", ".join(outcomes[key]) or "none",(bar.get_x()+bar.get_width()/2,0),xytext=(0,-31),textcoords="offset points",ha="center",va="top",fontsize=9,color="#374151")
    axis.text(1.5,4.45,"2 recoveries − 0 new errors = 2 additional correct rows",ha="center",fontsize=11,weight="bold")
    axis.set(ylabel="evaluation samples",ylim=(0,4.8),yticks=[0,1,2,3,4]); axis.grid(True,axis="y",color="#d1d5db",linewidth=.75); axis.set_axisbelow(True); axis.spines[["top","right","bottom"]].set_visible(False); axis.tick_params(axis="x",length=0)
    fig.tight_layout(pad=1.2); fig.savefig(OUTPUT_PATH,bbox_inches="tight"); plt.close(fig); print(f"saved={OUTPUT_PATH.relative_to(REPO_ROOT)}")
if __name__=="__main__": main()
