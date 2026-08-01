"""Draw the English P7-2.3 stress-variant and failure-diagnosis chart."""
from collections import Counter
import csv
import os
from pathlib import Path
REPO_ROOT=Path(__file__).resolve().parents[4]; CACHE=REPO_ROOT/".tmp"/"matplotlib-cache"; CACHE.mkdir(parents=True,exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR",str(CACHE)); os.environ.setdefault("XDG_CACHE_HOME",str(CACHE))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
ASSET_DIR=Path(__file__).resolve().parent; TRAIN=ASSET_DIR/"p7-2-churn-dataset.csv"; STRESS=ASSET_DIR/"p7-2-stress-test.csv"; OUT=ASSET_DIR/"p7-2-3-failure-diagnosis-chart-en.png"; FEATURES=["unresolved_tickets","days_since_login","usage_minutes_30d"]
def read(path):
    rows=list(csv.DictReader(path.open(encoding="utf-8")))
    for row in rows:
        for column in FEATURES+["label"]: row[column]=int(row[column])
    return rows
def matrix(rows): return np.array([[row[column] for column in FEATURES] for row in rows],dtype=float)
def one_nn(train_x,train_y,test_x): return np.array([int(train_y[int(np.argmin(np.linalg.norm(train_x-row,axis=1)))]) for row in test_x])
def main():
    train=[row for row in read(TRAIN) if row["split"]=="train"]; stress=read(STRESS); x_train,x_test=matrix(train),matrix(stress); y_train=np.array([row["label"] for row in train]); y_test=np.array([row["label"] for row in stress])
    baseline=np.full(len(y_test),int(np.bincount(y_train).argmax())); raw=one_nn(x_train,y_train,x_test); partial_train,partial_test=x_train.copy(),x_test.copy(); partial_train[:,2]/=60; partial_test[:,2]/=60; partial=one_nn(partial_train,y_train,partial_test); mean,std=x_train.mean(axis=0),x_train.std(axis=0); zscore=one_nn((x_train-mean)/std,y_train,(x_test-mean)/std)
    diagnoses=Counter()
    for before,middle,after,label in zip(raw,partial,zscore,y_test):
        key="fixed by\npreprocessing" if before!=label and after==label else "remaining after\nnormalization" if after!=label else "setting\nsensitive" if len({int(before),int(middle),int(after)})>1 else "stable in\ncomparison"
        diagnoses[key]+=1
    accuracy={"baseline":(baseline==y_test).mean(),"raw 1-NN":(raw==y_test).mean(),"partial scale":(partial==y_test).mean(),"z-score":(zscore==y_test).mean()}; fig,(left,right)=plt.subplots(1,2,figsize=(11,4.9),dpi=180)
    labels=list(accuracy); values=[accuracy[label] for label in labels]; bars=left.bar(labels,values,color=["#64748b","#2563eb","#d97706","#15803d"],width=.62)
    for bar,value in zip(bars,values): left.text(bar.get_x()+bar.get_width()/2,value+.025,f"{value:.3f}",ha="center",weight="bold")
    left.set(title="Stress-evaluation accuracy by variant",ylabel="accuracy",ylim=(0,1.05),yticks=[0,.25,.5,.75,1]); order=["fixed by\npreprocessing","remaining after\nnormalization","setting\nsensitive","stable in\ncomparison"]; vals=[diagnoses[key] for key in order]; bars=right.bar(order,vals,color=["#15803d","#d97706","#dc2626","#64748b"],width=.62)
    for bar,value in zip(bars,vals): right.text(bar.get_x()+bar.get_width()/2,value+.45,str(value),ha="center",weight="bold")
    right.set(title="Failure diagnosis using z-score as reference",ylabel="stress-evaluation samples",ylim=(0,max(vals)+3),yticks=range(0,max(vals)+1,5))
    for axis in (left,right): axis.grid(True,axis="y",color="#d1d5db",linewidth=.75); axis.set_axisbelow(True); axis.spines[["top","right"]].set_visible(False)
    fig.tight_layout(pad=1.3); fig.savefig(OUT,bbox_inches="tight"); plt.close(fig); print(f"saved={OUT.relative_to(REPO_ROOT)}")
if __name__=="__main__": main()
