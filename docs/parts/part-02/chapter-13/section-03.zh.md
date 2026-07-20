# P2-13.3 比较多个图表并保存

> Section ID: `P2-13.3`
> Version: `v2026.07.20`

在 P2-13.2，我们看过折线图（line plot）、散点图（scatter plot）、直方图（histogram）这些基础图表分别适合回答什么问题。现在再往前走一步，整理“把多个图表放在一起看，并把结果保存成文件”的流程。

在 AI 学习里，往往不会只看一张图就结束。你可能要同时看损失（loss）和准确率（accuracy），或者把训练数据（train data）和验证数据（validation data）的走势并排比较。这时最好更有意识地理解 Matplotlib 的 `Figure` 与 `Axes` 结构。

本节说明比较与保存流程中的基本区分，包括 `savefig`、图例（legend）、准确率（accuracy）。`plot`、`Figure`、`Axes` 的代表性说明放在 P2-13.1，基础图表选择标准放在 P2-13.2 和[概念词汇表](/AiBook/en/reference/concept-glossary/)；这里重点讲“怎样把多个图表一起比较，并把结果留成文件”。

## 核心判断标准：比较多个图表并保存

- 能说明一个 `Figure` 内可以包含多个 `Axes`。
- 能做出并排比较损失（loss）与准确率（accuracy）的图表。
- 能在同一个坐标轴上比较训练损失（train loss）与验证损失（validation loss）。
- 能用 `savefig()` 保存图表，并在文档或学习记录里再次使用。
- 能说明：想让保存下来的图表成为可复现记录，还必须同时保留代码和数据条件。

## 三个判断标准

| 标准 | 为什么重要 | 本节需要达到的理解程度 |
| --- | --- | --- |
| 为什么要一起画多个图？ | 它明确告诉你，重点不是图多，而是比较问题。 | 理解这样做是为了让比较问题更清楚。 |
| 什么情况下要分开坐标轴，什么情况下不用？ | 它帮助你区分哪些值能直接比较，哪些值应该拆开。 | 理解直接比较重要时放在一起，解释会混淆时就分开。 |
| 为什么保存很重要？ | 它帮助你区分屏幕输出与可复用记录。 | 理解保存不是只为了看结果，而是为了留下以后还能再次说明的记录。 |

| 术语 | 本节先抓住的含义 |
| --- | --- |
| `savefig` | 把当前图表保存为图像文件的函数调用。 |
| 图例（legend） | 用来区分各条线或各组点分别表示什么的标识。 |
| 准确率（accuracy） | 表示全部预测中有多少比例是预测正确的基础性能指标。 |
| 比较图（comparison plot） | 为了并排比较两个或以上流程或数值而制作的图表。 |
| 可复现记录（reproducible record） | 以同样代码和条件还能重新做出来的图表结果。 |

## 多个图表会制造比较问题

把多个图表排在一起，并不是为了把画面填满，而是为了把相关问题并排放置。

例如，在学习过程中，你可能想看损失（loss）是否下降、准确率（accuracy）是否上升。因为这两个值的单位不同，与其硬塞在同一个 y 轴上，不如拆成两个小图，通常会更容易读。

问题情境：你想在同一画面里比较学习进行时，损失和准确率分别如何变化。
输入（input）：epoch 编号、损失值列表、准确率值列表。
期望输出（output）：左边是损失曲线、右边是准确率曲线的 1 行 2 列图表。
要确认的概念：当一个 `Figure` 里有多个 `Axes` 时，就能把相关问题并排比较。

```python
# 这个例子在同一个 Figure 中比较多个图表，并保存结果图像。
import matplotlib.pyplot as plt
import numpy as np

epochs = np.arange(1, 13)
loss = [2.02, 1.68, 1.42, 1.18, 1.03, 0.91, 0.82, 0.75, 0.70, 0.66, 0.63, 0.60]
accuracy = [0.55, 0.61, 0.66, 0.70, 0.74, 0.78, 0.81, 0.83, 0.85, 0.86, 0.87, 0.88]

fig, axes = plt.subplots(1, 2)

axes[0].plot(epochs, loss, marker="o")
axes[0].set_title("Loss over epochs")
axes[0].set_xlabel("epoch")
axes[0].set_ylabel("loss")

axes[1].plot(epochs, accuracy, marker="o")
axes[1].set_title("Accuracy over epochs")
axes[1].set_xlabel("epoch")
axes[1].set_ylabel("accuracy")

fig.tight_layout()
plt.show()
```

输出结果会像下面这样，在一个 `Figure` 里分开显示两个相关问题。

![并排比较损失与准确率的两个子图](/AiBook/assets/part-02/chapter-13/subplot-loss-accuracy.png)

这张图会同时提出两个问题。

- 随着重复学习进行，损失是否大体下降？
- 在同一时期内，准确率是否大体上升？

把两张图并排后，你还可以继续提出“一个在变好，另一个是否停滞了？”这类问题。

这种比较方式不只用于学习曲线。比如，一边的 `Axes` 可以画两条动作记录的原始曲线，另一边的 `Axes` 可以画把这些动作按区段平均值或最终值总结后的比较小图。这样左边看的是`形状本身的差异`，右边看的是`总结值里留下来的差异`。

也就是说，把多个图表放在一起，不是为了增加图的数量，而是为了更明确地表达：`用什么问题把原始形状和总结结果一起读`。

## 重新读取 Figure 与 Axes

在 P2-13.1，我们把 `Figure` 看成整张图，把 `Axes` 看成绘制数据的坐标区域。画多个图时，这个区分会更重要。

问题情境：制作分成多个面板的图表时，你需要先抓住 `fig` 和 `axes` 分别指向什么。
输入（input）：一行 `plt.subplots(1, 2)` 调用。
期望输出（output）：一个指向整张图和其中两个图面板的变量结构。
要确认的概念：`Figure` 是整张图，`Axes` 是实际绘制数据的各个坐标区域。

```python
# 这个例子在同一个 Figure 中比较多个图表，并保存结果图像。
fig, axes = plt.subplots(1, 2)
```

这段代码会在一个 `Figure` 里左右创建两个 `Axes`。

这里可以这样理解。

| 代码 | 直观理解 |
| --- | --- |
| `fig` | 整张图 |
| `axes[0]` | 左侧图面板 |
| `axes[1]` | 右侧图面板 |
| `plt.subplots(1, 2)` | 创建 1 行 2 列的图面板 |

一旦有了多个 `Axes`，写法就会从单个 `ax.plot(...)` 变成 `axes[0].plot(...)`、`axes[1].plot(...)` 这种“指定画在哪一格”的方式。

## 有时也应该在同一个坐标轴上比较

并不是所有情况都应该把图拆开。当你比较单位相同的值时，把两条线放到同一个 `Axes` 上会更直接。

典型例子就是比较训练损失（train loss）和验证损失（validation loss）。这两个值本来都是损失（loss），因此可以放在同一个 y 轴上比较。

问题情境：训练损失和验证损失单位相同，所以你想在一个坐标轴上直接比较。
输入（input）：epoch 编号，以及 `train_loss`、`validation_loss` 列表。
期望输出（output）：两条损失曲线画在同一坐标轴上的折线图。
要确认的概念：单位相同的值应该放在同一个 `Axes` 上，这样两个流程之间的分离和交叉更容易直接读出来。

```python
# 这个例子在同一个 Figure 中比较多个图表，并保存结果图像。
import matplotlib.pyplot as plt
import numpy as np

epochs = np.arange(1, 16)
train_loss = [1.82, 1.45, 1.19, 1.00, 0.86, 0.76, 0.68, 0.62, 0.57, 0.53, 0.49, 0.46, 0.43, 0.41, 0.39]
validation_loss = [1.88, 1.53, 1.31, 1.14, 1.02, 0.94, 0.90, 0.88, 0.89, 0.92, 0.97, 1.03, 1.10, 1.17, 1.25]

fig, ax = plt.subplots()
ax.plot(epochs, train_loss, marker="o", label="train loss")
ax.plot(epochs, validation_loss, marker="o", label="validation loss")
ax.axvline(8, color="gray", linestyle="--")
ax.text(8.25, 1.38, "validation starts rising")
ax.set_xlabel("epoch")
ax.set_ylabel("loss")
ax.set_title("Training and validation loss can diverge")
ax.legend()
plt.show()
```

输出结果会像下面这样，让你在同一坐标轴上比较两条损失曲线。

![展示训练损失与验证损失分离的比较图](/AiBook/assets/part-02/chapter-13/train-validation-loss-diverge.png)

这个例子会连接到 Part 3 里还会再见到的过拟合（overfitting）直觉。如果训练损失持续下降，而验证损失又重新上升，就可以怀疑：模型对训练数据拟合得更好，却对新数据拟合得更差。

不过，这里不应把结论说死。这张图的意思不是“已经确认过拟合”，而是“需要更仔细检查验证数据上的性能走势”。

## 保存图表，意味着留下记录

在 Colab 或 Jupyter Notebook 里，可以用 `plt.show()` 直接看到图表。但如果你想把它放进书、报告或实验记录，就需要把它保存成图像文件。

在 Matplotlib 里，用的是 `savefig()`。

问题情境：你需要把屏幕上看到的图表保存成文件，以便在文档和记录里再次使用。
输入（input）：已经创建好的 `fig` 对象，以及要保存的文件名。
期望输出（output）：当前图表被保存成 PNG 等图像文件。
要确认的概念：`plt.show()` 是屏幕显示，`savefig()` 是保存可复用的结果文件。

```python
# 这个例子在同一个 Figure 中比较多个图表，并保存结果图像。
fig.savefig("train-validation-loss-diverge.png")
```

这里可以这样理解。

| 代码 | 含义 |
| --- | --- |
| `plt.show()` | 在当前执行画面中查看图表 |
| `fig.savefig(...)` | 把图表保存成图像文件 |
| `fig.tight_layout()` | 调整留白，避免标题、坐标轴标签和绘图区彼此重叠 |

在文档项目中，经常就是这样生成输出图像：运行代码生成图片，再把图片链接进 Markdown 文档。

## 只有保存的图像还不够可复现

图表文件能展示结果，但它本身还不是可复现记录。想再次做出同一张图，还需要下面这些信息。

- 生成图表的代码
- 使用的数据，或生成数据的条件
- 使用的库与版本
- 如果包含随机值，还需要随机种子（random seed）
- 图表想回答的问题

因此，在文档项目里，不应只留下图像文件。只要可能，也应保留生成这张图的 Python 脚本。比如一张图需要多次修改时，把生成脚本放在离图片较近的位置，会更容易重新生成结果。

这种方式更接近“这张图还能再做出来”，而不只是“这张图被贴上去了”。

## 制作比较图时的注意点

比较多个图表时，要注意下面这些点。

| 注意点 | 原因 |
| --- | --- |
| 不要把不同单位的值硬塞到同一个坐标轴上 | 变化看起来可能会被扭曲 |
| 单位相同的值可以放在同一个坐标轴上比较 | 像 train loss 和 validation loss 这样可以直接比较 |
| 加上图例（legend） | 需要知道每条线代表什么 |
| 检查坐标轴范围 | 小差异可能被夸大，大差异也可能被隐藏 |
| 保存时用说明性的文件名 | 以后需要知道这到底是哪张图 |

图表不会代替结论，但好的图表会帮助你把下一个问题问得更准确。

## 用案例来看

### 案例 1. 当你必须把损失和准确率留在同一张图里时

假设一位学习者想整理模型训练结果，并把它放进团队文档里。只看损失图可以知道学习是否稳定，但如果和准确率一起看，就更容易提出“损失在下降，但准确率是否停滞？”这样的比较问题。

人一开始可能会想，“一张图还不够吗？” 但在实际实验记录中，如果把相关值并排放置，或者把同类单位的值放在同一坐标轴上比较，解释会更容易。因此，多 `Axes` 的结构、图例和坐标轴标签就会变得重要。

另外，如果只是在屏幕上看一次就结束，之后会很难再次说明。你应当用 `savefig()` 把图表保存下来，并把生成这张图的代码和数据条件一起保留，这样同样的结果才能再次做出来。

可检查的结果会体现在“保存下来的文件”和“能否重新运行生成”上。如果比较 `train loss`、`validation loss`、`accuracy` 的图已经作为文件留下，并且还能用同一脚本重新生成，那么这张图就不只是简单截图，而是在充当实验记录。

## 检查清单

- 能说明 `plt.subplots(1, 2)` 会在一个 Figure 里创建两个 Axes 吗？
- 能说明为什么应该把损失和准确率并排比较吗？
- 能说明为什么 train loss 和 validation loss 可以在同一个坐标轴上比较吗？
- 能说明 `plt.show()` 和 `fig.savefig()` 的区别吗？
- 能说明为什么只有图表文件还不足以支撑可复现性吗？
- 当你需要把多个图表并排放在一个画面上做比较时，能先想到 Figure 和 Axes 的排布吗？

## 来源与参考资料

- Matplotlib Developers, `Quick start guide`, Matplotlib documentation, 确认日期：2026-07-20. [https://matplotlib.org/stable/users/explain/quick_start.html](https://matplotlib.org/stable/users/explain/quick_start.html){: target="_blank" rel="noopener noreferrer" } 这是确认一个 `Figure` 可以包含多个 `Axes`，以及 `plt.subplots()` 示例的资料。
- Matplotlib Developers, `Introduction to Axes (or Subplots)`, Matplotlib documentation, 确认日期：2026-07-20. [https://matplotlib.org/stable/users/explain/axes/axes_intro.html](https://matplotlib.org/stable/users/explain/axes/axes_intro.html){: target="_blank" rel="noopener noreferrer" } 这是把 `Axes` 说明为数据坐标、标签、标题和图例设置中心对象的依据。
- Matplotlib Developers, `matplotlib.figure.Figure.savefig`, Matplotlib API reference, 确认日期：2026-07-20. [https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html](https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html){: target="_blank" rel="noopener noreferrer" } 这是说明 `Figure.savefig()` 会把图保存为图像或矢量图文件的直接参考资料。
