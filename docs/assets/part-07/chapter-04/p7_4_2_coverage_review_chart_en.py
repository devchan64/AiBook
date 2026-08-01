"""Draw the English P7-4.2 coverage and score chart."""
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
from matplotlib.patches import Patch
import numpy as np

ASSET_DIR = Path(__file__).resolve().parent
DATA_PATH = ASSET_DIR / "p7-4-support-routing-dataset.csv"
OUTPUT_PATH = ASSET_DIR / "p7-4-2-coverage-review-chart-en.png"

def records():
    rows = list(csv.DictReader(DATA_PATH.open(encoding="utf-8"))); train = [r for r in rows if r["split"] == "train"]
    vocab = {t for r in train for t in r["text"].split()}; profiles = {0: {}, 1: {}}
    for row in train:
        for token in row["text"].split(): profiles[int(row["label"])][token] = profiles[int(row["label"])].get(token, 0) + 1
    result = []
    for row in (r for r in rows if r["split"] == "test"):
        tokens = row["text"].split(); known = [t for t in tokens if t in vocab]; scores = [sum(profiles[label].get(t, 0) for t in known) for label in (0, 1)]
        result.append({"sample": row["sample_id"].replace("평가-", "test-"), "coverage": len(known)/len(tokens), "scores": scores, "correct": int(np.argmax(scores)) == int(row["label"])})
    return result

def style(axis):
    axis.grid(True, axis="y", color="#d1d5db", linewidth=.75); axis.set_axisbelow(True); axis.spines[["top", "right"]].set_visible(False)

def main():
    data = records(); positions = np.arange(len(data)); fig, (coverage, score) = plt.subplots(1, 2, figsize=(11.8, 4.8), dpi=180)
    coverage.bar(positions, [r["coverage"] for r in data], color=["#15803d" if r["correct"] else "#dc2626" for r in data], width=.64); coverage.axhline(.5, color="#64748b", linestyle="--", linewidth=1.3)
    coverage.set(ylim=(0,1.12), ylabel="training-vocabulary coverage", title="Coverage by evaluation sentence"); coverage.set_xticks(positions, [r["sample"] for r in data], rotation=15, ha="right")
    coverage.legend(handles=[Patch(color="#15803d",label="correct"),Patch(color="#dc2626",label="incorrect"),plt.Line2D([],[],color="#64748b",linestyle="--",label="low-coverage threshold")],frameon=False,loc="upper right",fontsize=8.5); style(coverage)
    focus = [r for r in data if r["sample"] in {"test-05","test-07"}]; p=np.arange(len(focus)); width=.30
    score.bar(p-width/2,[r["scores"][0] for r in focus],width,label="refund score",color="#2563eb"); score.bar(p+width/2,[r["scores"][1] for r in focus],width,label="delivery score",color="#ea580c")
    for pos,row in zip(p,focus): score.text(pos,max(row["scores"])+.32,"correct" if row["correct"] else "incorrect",ha="center",weight="bold",color="#15803d" if row["correct"] else "#dc2626")
    score.set(ylim=(0,8.2),ylabel="training-vocabulary score",title="Same low coverage, different class scores"); score.set_xticks(p,["test-05\ncancel + tracking","test-07\ndefect + refund"]); score.legend(frameon=False,loc="upper left"); style(score)
    fig.suptitle("Low coverage is not one kind of failure",fontsize=15,fontweight="bold"); fig.tight_layout(pad=1,rect=(0,0,1,.92)); fig.savefig(OUTPUT_PATH,bbox_inches="tight"); plt.close(fig); print(f"saved={OUTPUT_PATH.relative_to(REPO_ROOT)}")

if __name__ == "__main__": main()
