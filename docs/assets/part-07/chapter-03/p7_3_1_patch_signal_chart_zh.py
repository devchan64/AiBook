"""绘制 P7-3.1 的中文补丁位置信号与划痕概率图。"""
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
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Patch
import numpy as np

ASSET_DIR = Path(__file__).resolve().parent
DATA = ASSET_DIR / "p7-3-surface-patches.csv"
OUT = ASSET_DIR / "p7-3-1-patch-signal-chart-zh.png"
FONT = next((path for path in [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
] if Path(path).exists()), None)
CN = FontProperties(fname=FONT) if FONT else None


def softmax(values):
    values = values - values.max(axis=1, keepdims=True)
    exponentials = np.exp(values)
    return exponentials / exponentials.sum(axis=1, keepdims=True)


def main():
    columns = [f"pixel_{row}{col}" for row in range(8) for col in range(8)]
    rows = []
    for raw in csv.DictReader(DATA.open(encoding="utf-8")):
        rows.append({"split": raw["split"], "sample": raw["sample"], "label": int(raw["label"]),
                     "image": np.array([float(raw[column]) for column in columns]).reshape(8, 8)})
    train = [row for row in rows if row["split"] == "train"]
    test = [row for row in rows if row["split"] == "test"]
    x_train = np.array([row["image"].reshape(-1) for row in train])
    y_train = np.array([row["label"] for row in train])
    x_test = np.array([row["image"].reshape(-1) for row in test])
    weights, bias = np.zeros((64, 2)), np.zeros(2)
    targets = np.eye(2)[y_train]
    for _ in range(700):
        probabilities = softmax(x_train @ weights + bias)
        weights -= .35 * x_train.T @ (probabilities - targets) / len(x_train)
        bias -= .35 * (probabilities - targets).mean(axis=0)
    probabilities = softmax(x_test @ weights + bias)
    names = {"평가-정상-안정": "稳定\n正常", "평가-결함-명확": "明确\n划痕",
             "평가-결함-약함": "弱\n划痕", "평가-정상-그림자": "阴影\n正常"}
    results = []
    for row, probability in zip(test, probabilities):
        image = row["image"]
        center = float(image[:, 3:5].mean())
        outer = float(np.concatenate((image[:, :3], image[:, 5:]), axis=1).mean())
        correct = int(probability.argmax()) == row["label"]
        results.append((names[row["sample"]], center, outer, center - outer, float(probability[1]), correct))
    positions = np.arange(len(results))
    fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4.9), dpi=180)
    width = .34
    left.bar(positions - width / 2, [row[1] for row in results], width, label="中央两列平均亮度", color="#c2410c")
    left.bar(positions + width / 2, [row[2] for row in results], width, label="外围六列平均亮度", color="#64748b")
    for position, row in zip(positions, results):
        left.text(position, max(row[1], row[2]) + .035, f"差 {row[3]:+.3f}", ha="center", fontsize=9.5, weight="bold", fontproperties=CN, color="#b45309" if not row[5] else "#374151")
    left.set_title("输入位置的平均亮度（中央 − 周围）", fontproperties=CN)
    left.set_ylabel("灰度值", fontproperties=CN)
    left.set_ylim(0, .85)
    left.set_xticks(positions, [row[0] for row in results], fontproperties=CN)
    left.legend(frameon=False, loc="upper left", prop=CN)
    bars = right.bar(positions, [row[4] for row in results], color=["#15803d" if row[5] else "#dc2626" for row in results], width=.62)
    right.axhline(.5, color="#6b7280", linestyle="--", linewidth=1.2)
    right.text(3.35, .53, "决策边界 0.5", ha="right", fontsize=9, color="#4b5563", fontproperties=CN)
    for bar, row in zip(bars, results):
        right.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + .035, f"{row[4]:.3f}", ha="center", fontsize=10, weight="bold")
    right.set_title("划痕警告概率", fontproperties=CN)
    right.set_ylabel("类别 1 概率", fontproperties=CN)
    right.set_ylim(0, 1.1)
    right.set_xticks(positions, [row[0] for row in results], fontproperties=CN)
    right.legend(handles=[Patch(color="#15803d", label="正确"), Patch(color="#dc2626", label="错误")], frameon=False, loc="upper left", prop=CN)
    for axis in (left, right):
        axis.grid(True, axis="y", color="#d1d5db", linewidth=.75)
        axis.set_axisbelow(True)
        axis.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(pad=1.3)
    fig.savefig(OUT, bbox_inches="tight")
    plt.close(fig)
    print(f"saved={OUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
