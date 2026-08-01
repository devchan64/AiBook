"""绘制 P7-4.1 的中文支持路由学习曲线。"""
from __future__ import annotations

import os
import sys
import xml.etree.ElementTree as ET
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

ASSET_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ASSET_DIR))
from p7_4_training_curves import run_training

FONT_PATH = next((path for path in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"] if Path(path).exists()), None)
CN = FontProperties(fname=FONT_PATH) if FONT_PATH else None
if FONT_PATH:
    font_manager.fontManager.addfont(FONT_PATH)
    plt.rcParams["font.family"] = CN.get_name()
OUT = ASSET_DIR / "p7-4-1-learning-curves-zh.svg"
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

def accessible(path):
    tree = ET.parse(path); root = tree.getroot(); root.set("role", "img"); root.set("aria-labelledby", "title desc")
    title = ET.Element(f"{{{SVG_NS}}}title", {"id": "title"}); title.text = "支持路由学习记录"
    desc = ET.Element(f"{{{SVG_NS}}}desc", {"id": "desc"}); desc.text = "十二个 epoch 中训练和评估损失下降。最终评估准确率为 0.857，高于 0.714 基线。"
    root.insert(0, desc); root.insert(0, title); tree.write(path, encoding="utf-8", xml_declaration=False)

def main():
    logs = run_training(); epochs = [row["epoch"] for row in logs]
    fig, (loss_ax, accuracy_ax) = plt.subplots(1, 2, figsize=(11.8, 4.5), constrained_layout=True)
    loss_ax.plot(epochs, [row["train_loss"] for row in logs], marker="o", linewidth=2.2, color="#0f766e", label="训练损失")
    loss_ax.plot(epochs, [row["eval_loss"] for row in logs], marker="o", linewidth=2.2, color="#ea580c", label="评估损失")
    loss_ax.set(title="损失曲线", xlabel="Epoch", ylabel="损失", xticks=epochs); loss_ax.grid(alpha=.22); loss_ax.legend(frameon=False, prop=CN)
    accuracy_ax.plot(epochs, [row["eval_accuracy"] for row in logs], marker="o", linewidth=2.2, color="#2563eb", label="评估准确率")
    accuracy_ax.plot(epochs, [row["baseline_accuracy"] for row in logs], linestyle="--", linewidth=1.8, color="#64748b", label="基线准确率")
    accuracy_ax.set(title="准确率与基线", xlabel="Epoch", ylabel="准确率", xticks=epochs, ylim=(.68, 1.04)); accuracy_ax.grid(alpha=.22); accuracy_ax.legend(frameon=False, loc="lower right", prop=CN)
    accuracy_ax.annotate("早期预测完美后\n准确率改变", xy=(8, logs[7]["eval_accuracy"]), xytext=(4.4, 1.0), arrowprops={"arrowstyle": "->", "color": "#1f2937"}, fontproperties=CN)
    fig.suptitle(f"支持路由学习记录\n最终评估准确率 {logs[-1]['eval_accuracy']:.3f}；评估损失 {logs[0]['eval_loss']:.3f} → {logs[-1]['eval_loss']:.3f}", fontweight="bold", fontproperties=CN)
    fig.savefig(OUT, format="svg", dpi=160, bbox_inches="tight"); plt.close(fig); accessible(OUT)
    print(f"saved={OUT.relative_to(REPO_ROOT)}")

if __name__ == "__main__": main()
