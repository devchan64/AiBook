# P2-13.3 比较并保存多个图形

> Section ID: `P2-13.3`
> Version: `v2026.09.15`

## 并排查看损失与准确率

在这组虚构训练记录中，损失从 2.02 降到 0.60，准确率从 0.55 升到 0.88。准确率是预测正确的比例。两者含义和数值范围不同，因此用各自具有 y 轴的两个图形比较。

```python
import matplotlib.pyplot as plt
import numpy as np

epochs = np.arange(1, 13)
loss = [2.02, 1.68, 1.42, 1.18, 1.03, 0.91, 0.82, 0.75, 0.70, 0.66, 0.63, 0.60]
accuracy = [0.55, 0.61, 0.66, 0.70, 0.74, 0.78, 0.81, 0.83, 0.85, 0.86, 0.87, 0.88]

fig, axes = plt.subplots(1, 2, figsize=(8, 3.8), sharex=True)

axes[0].plot(epochs, loss, marker="o")
axes[0].set_title("Loss over epochs")
axes[0].set_xlabel("epoch")
axes[0].set_ylabel("loss")

axes[1].plot(epochs, accuracy, marker="o")
axes[1].set_title("Accuracy over epochs")
axes[1].set_xlabel("epoch")
axes[1].set_ylabel("accuracy")
axes[1].set_ylim(0, 1)

fig.tight_layout()
plt.show()
```

输出在一个 Figure 中将两个相关问题分开显示。

![分开展示损失与准确率](/AiBook/assets/part-02/chapter-13/subplot-loss-accuracy-zh.svg)

`plt.subplots(1, 2)` 创建一个整体图形和两个坐标区域。`axes[0]` 是左侧损失图，`axes[1]` 是右侧准确率图。两图的 x 轴都表示相同的 12 次迭代。

最后三次迭代中，损失为 `0.66 → 0.63 → 0.60`，准确率为 `0.86 → 0.87 → 0.88`。使用独立坐标轴，可以根据各自刻度读取变化幅度。

## 叠加训练与验证损失

并非总要分开画图。比较相同单位的值时，把两条线放在同一个 Axes 上往往更直接。

训练与验证损失若采用相同损失函数和聚合标准计算，就可以共用 y 轴。这组虚构记录中，训练损失持续下降，验证损失则在第 8 次迭代达到 0.88 后上升。

```python
import matplotlib.pyplot as plt
import numpy as np

epochs = np.arange(1, 16)
train_loss = [1.82, 1.45, 1.19, 1.00, 0.86, 0.76, 0.68, 0.62, 0.57, 0.53, 0.49, 0.46, 0.43, 0.41, 0.39]
validation_loss = [1.88, 1.53, 1.31, 1.14, 1.02, 0.94, 0.90, 0.88, 0.89, 0.92, 0.97, 1.03, 1.10, 1.17, 1.25]

fig, ax = plt.subplots()
ax.plot(epochs, train_loss, marker="o", label="train loss")
ax.plot(epochs, validation_loss, marker="o", label="validation loss")
ax.axvline(8, color="gray", linestyle="--")
ax.text(8.25, 1.38, "minimum validation loss at epoch 8")
ax.set_xlabel("epoch")
ax.set_ylabel("loss")
ax.set_title("Training and validation loss can diverge")
ax.legend()
plt.show()
```

输出在同一坐标区域中比较两条损失曲线。

![训练与验证损失逐渐分离](/AiBook/assets/part-02/chapter-13/train-validation-loss-diverge-zh.svg)

这种模式可能提示过拟合。如果训练损失持续下降而验证损失回升，模型可能更贴合训练数据，却更不适合新数据。

从第 8 次到第 15 次迭代，训练损失从 0.62 降到 0.39，验证损失从 0.88 升到 1.25。同一期间两者方向相反。判断原因还需要检查数据划分与训练条件。

## 保存图像文件

在 Colab 或 Jupyter Notebook 中，可以用 `plt.show()` 直接查看图形。用于书籍、报告或实验记录时，还需要保存成图像文件。

Matplotlib 使用 `savefig()` 保存。

```python
from pathlib import Path

output_dir = Path(".tmp") / "chapter-13-plots"
output_dir.mkdir(parents=True, exist_ok=True)
fig.savefig(output_dir / "train-validation-loss-diverge.png", dpi=160)
fig.savefig(output_dir / "train-validation-loss-diverge.svg")
```

| 代码 | 含义 |
| --- | --- |
| `plt.show()` | 在当前环境显示图形 |
| `fig.savefig(...)` | 将图形保存成文件 |
| `fig.tight_layout()` | 调整间距，减少标题、标签与图形区域重叠 |

相对路径会在当前工作目录下的 `.tmp/chapter-13-plots/` 中生成文件。此保存代码使用刚刚创建的训练与验证损失 Figure。若要保存最初的并排图，应把保存调用放在它的 `plt.show()` 之前。创建多个图形时，变量 `fig` 可能已指向后来的图形，因此要先确认保存对象。

PNG 是像素图像。图形为 8×3.8 英寸且 `dpi=160` 时，默认画布为 1280×608 像素。SVG 将线条与文字保存为矢量，放大后仍保持轮廓。指定 `bbox_inches="tight"` 会裁剪保存范围，像素尺寸可能随之改变。

通常顺序是创建图形、调整标签和布局、调用 `fig.savefig`，再调用 `plt.show()`。阻塞式 `show()` 结束后，当前图形可能已关闭，此时 `plt.savefig()` 可能保存一张新的空图。上例通过保留的 Figure 对象调用 `fig.savefig()`，但先保存再 show 可以减少执行环境带来的混淆。批量生成文件时，保存后用 `plt.close(fig)` 关闭每张图。

## 复现所需的记录

图像能展示结果，但它本身并不是可复现记录。重新生成相同图形需要：

- 绘图代码
- 数据或数据生成条件
- 库及其版本
- 使用随机值时的随机种子
- 图形所回答的问题

因此，文档项目在可能时应同时保存图像和生成脚本。若一张图需要反复修改，把脚本放在图像附近会更容易复现。

以下脚本将三个语言版本的示例 SVG 保存到资源目录。Matplotlib 默认将缓存放在仓库的 `.tmp` 下。

[p2_13_3_compare_and_save.py](/AiBook/assets/part-02/chapter-13/p2_13_3_compare_and_save.py)

```bash
python docs/assets/part-02/chapter-13/p2_13_3_compare_and_save.py
```

## 比较条件

比较多个图形时，应检查以下事项：

| 检查项 | 原因 |
| --- | --- |
| 不把不同单位强放在同一轴上 | 可能扭曲变化印象 |
| 相同单位可在同一轴上比较 | 例如训练与验证损失可直接比较 |
| 添加图例 | 必须明确每条线的含义 |
| 检查坐标范围 | 小差异可能被放大，大差异可能被隐藏 |
| 使用有说明性的文件名 | 以后仍能辨认图形内容 |

## 案例：记录准确率停滞

把第一个例子中最后三个准确率值改为 `[0.86, 0.86, 0.86]` 后重新运行。损失继续下降，准确率却从第 10 次迭代开始变平。即使损失降低，预测正确的比例也不再提高。

修改第一个准确率列表后，在 `plt.show()` 前加入 `fig.savefig(output_dir / "loss-accuracy-plateau.png", dpi=160)`。`output_dir` 是前面保存示例创建的文件夹。应在创建修改后的图形后立即保存，避免误存后来另一个 `fig`。

准确率只统计最终判断是否正确，损失则可以更细致地反映预测值与目标的接近程度。例如目标为正类、分类阈值为 0.5 时，预测概率从 0.6 变到 0.8 都会判对，但二元交叉熵损失约从 0.511 降到 0.223。因此，准确率停滞与损失下降并不矛盾。

比较此文件与原结果时，应同时保留原始和修改后的准确率列表。文件名不同并不能说明输入改了什么。将“最后三个准确率固定为 0.86，损失列表不变”的修改记录与生成代码一同保存，才能解释两图差异。

## 检查清单

- 能否解释多个区域为何有助于比较相关问题？
- 能否说明 `plt.subplots(1, 2)` 在一个 Figure 中创建两个 Axes？
- 能否解释损失与准确率为何分开显示？
- 能否区分何时共用坐标轴、何时按不同单位分开？
- 能否区分 `plt.show()` 与 `fig.savefig()`？
- 能否说明哪些代码和数据记录能让已保存图像可复现？

## 来源与参考资料

- Matplotlib Developers, [Quick start guide](https://matplotlib.org/stable/users/explain/quick_start.html){: target="_blank" rel="noopener noreferrer" }, Matplotlib documentation, 查阅日期：2026-07-20. 在一个 Figure 中放置多个 Axes。
- Matplotlib Developers, [Introduction to Axes (or Subplots)](https://matplotlib.org/stable/users/explain/axes/axes_intro.html){: target="_blank" rel="noopener noreferrer" }, Matplotlib documentation, 查阅日期：2026-07-20. Axes 作为设置标签、标题与图例的坐标区域。
- Matplotlib Developers, [matplotlib.figure.Figure.savefig](https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html){: target="_blank" rel="noopener noreferrer" }, Matplotlib documentation, 查阅日期：2026-09-15. 用 Figure.savefig 保存图像与矢量图。
- Matplotlib Developers, [pyplot.show](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.show.html){: target="_blank" rel="noopener noreferrer" }, 查阅日期：2026-09-15. show 与保存顺序，以及保留 Figure 引用.
- scikit-learn Developers, [log_loss](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.log_loss.html){: target="_blank" rel="noopener noreferrer" }, 查阅日期：2026-09-15. 正类样本的二元交叉熵计算.
