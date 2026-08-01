"""绘制 P7-3.3 的中文输入表示比较报告。"""
import csv
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
CACHE = REPO_ROOT / ".tmp" / "matplotlib-cache"
CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(CACHE))
os.environ.setdefault("XDG_CACHE_HOME", str(CACHE))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

ASSET_DIR = Path(__file__).resolve().parent
DATA = ASSET_DIR / "p7-3-surface-patches.csv"
OUT = ASSET_DIR / "p7-3-input-representation-report-zh.png"
FONT_PATH = next((path for path in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"] if Path(path).exists()), None)
CN = FontProperties(fname=FONT_PATH) if FONT_PATH else None
if FONT_PATH:
    font_manager.fontManager.addfont(FONT_PATH)
    plt.rcParams["font.family"] = CN.get_name()

def column_profile(matrix): return matrix.reshape(len(matrix), 8, 8).mean(axis=1)
def center_profile(matrix):
    images = matrix.reshape(len(matrix), 8, 8)
    return np.column_stack([images[:, :, 3:5].mean(axis=(1, 2)), images[:, :, :3].mean(axis=(1, 2)), images[:, :, 5:].mean(axis=(1, 2))])
def style(axis):
    axis.grid(True, axis="y", color="#d0d7de", linewidth=.75)
    axis.set_axisbelow(True)
    axis.spines[["top", "right"]].set_visible(False)

def main():
    rows = list(csv.DictReader(DATA.open(encoding="utf-8")))
    columns = [name for name in rows[0] if name.startswith("pixel_")]
    train, test = [row for row in rows if row["split"] == "train"], [row for row in rows if row["split"] == "test"]
    matrix = lambda selected: np.array([[float(row[column]) for column in columns] for row in selected])
    raw_train, raw_test = matrix(train), matrix(test)
    y_train, y_test = np.array([int(row["label"]) for row in train]), np.array([int(row["label"]) for row in test])
    variants = {"完整 64 像素": (raw_train, raw_test), "8 个列平均": (column_profile(raw_train), column_profile(raw_test)), "3 个中心带值": (center_profile(raw_train), center_profile(raw_test))}
    results = []
    for name, (x_train, x_test) in variants.items():
        model = LogisticRegression(max_iter=1000, random_state=7).fit(x_train, y_train)
        prediction = model.predict(x_test)
        margin = np.abs(model.predict_proba(x_test)[:, 1] - model.predict_proba(x_test)[:, 0])
        results.append({"name": name, "accuracy": accuracy_score(y_test, prediction), "errors": int((prediction != y_test).sum()), "low": int((margin < .25).sum()), "margins": margin})
    fig, (left, right) = plt.subplots(1, 2, figsize=(11.8, 4.4), dpi=180)
    names, positions, width = [row["name"] for row in results], np.arange(len(results)), .32
    left.bar(positions - width / 2, [row["errors"] for row in results], width, label="错误数", color="#dc2626")
    left.bar(positions + width / 2, [row["low"] for row in results], width, label="低置信度样本数", color="#0f766e")
    left.set(ylim=(0, 4.6), ylabel="评估样本数")
    left.set_title("错误与低置信度样本", fontproperties=CN)
    left.set_xticks(positions, names, rotation=10, ha="right", fontproperties=CN)
    left.legend(frameon=False, fontsize=8.5, loc="upper left", prop=CN); style(left)
    sample_positions, colors = np.arange(len(test)), ["#2563eb", "#ea580c", "#0f766e"]
    for result, color in zip(results, colors): right.plot(sample_positions, result["margins"], marker="o", linewidth=2, label=result["name"], color=color)
    labels = {"평가-정상-안정": "稳定\n正常", "평가-결함-명확": "明确\n划痕", "평가-결함-약함": "弱\n划痕", "평가-정상-그림자": "阴影\n正常"}
    right.axhline(.25, color="#64748b", linestyle="--", linewidth=1.3, label="低置信度阈值")
    right.set(ylim=(0, .7), ylabel="置信差")
    right.set_title("各评估补丁的置信差", fontproperties=CN)
    right.set_xticks(sample_positions, [labels[row["sample"]] for row in test], fontproperties=CN)
    right.legend(frameon=False, fontsize=8.3, loc="upper right", prop=CN); style(right)
    fig.suptitle("按输入表示比较图像分类\n三种表示的评估准确率均为 0.75", fontsize=15, fontweight="bold", fontproperties=CN)
    fig.tight_layout(pad=1, rect=(0, 0, 1, .91)); fig.savefig(OUT, bbox_inches="tight"); plt.close(fig)
    print(f"saved={OUT.relative_to(REPO_ROOT)}")

if __name__ == "__main__": main()
