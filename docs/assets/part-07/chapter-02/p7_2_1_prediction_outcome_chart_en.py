"""Draw the English P7-2.1 prediction-transition chart."""
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
ASSET_DIR = Path(__file__).resolve().parent
DATA_PATH = ASSET_DIR / "p7-2-churn-dataset.csv"
OUTPUT_PATH = ASSET_DIR / "p7-2-1-prediction-outcome-transition-en.png"
FEATURES = ["unresolved_tickets", "days_since_login", "usage_minutes_30d"]
def main():
    rows=list(csv.DictReader(DATA_PATH.open(encoding="utf-8")))
    for row in rows:
        for key in FEATURES+["label"]: row[key]=int(row[key])
    train=[r for r in rows if r["split"]=="train"]; test=[r for r in rows if r["split"]=="test"]
    raw=[min(train,key=lambda candidate:sum((row[key]-candidate[key])**2 for key in FEATURES))["label"] for row in test]
    groups={"both correct":[],"recovered\nby 1-NN":[],"newly wrong\nunder 1-NN":[],"wrong\nunder both":[]}
    for row,candidate in zip(test,raw):
        base_ok=0==row["label"]; candidate_ok=candidate==row["label"]
        key="both correct" if base_ok and candidate_ok else "recovered\nby 1-NN" if not base_ok and candidate_ok else "newly wrong\nunder 1-NN" if base_ok else "wrong\nunder both"
        groups[key].append(row["sample_id"].replace("평가-","test-"))
    names=list(groups); counts=[len(groups[name]) for name in names]; fig,axis=plt.subplots(figsize=(9.5,5),dpi=180); bars=axis.bar(names,counts,color=["#15803d","#2563eb","#dc2626","#64748b"],width=.64)
    for bar,name,count in zip(bars,names,counts): axis.text(bar.get_x()+bar.get_width()/2,count+.08,", ".join(groups[name]) if count else "none",ha="center",va="bottom",fontsize=9)
    axis.set(ylim=(0,max(counts)+.9),ylabel="evaluation samples",title="Prediction transitions: retained-only baseline vs raw 1-NN"); axis.grid(True,axis="y",color="#d1d5db",linewidth=.75); axis.set_axisbelow(True); axis.spines[["top","right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(OUTPUT_PATH,bbox_inches="tight"); plt.close(fig); print(f"saved={OUTPUT_PATH.relative_to(REPO_ROOT)}")
if __name__ == "__main__": main()
