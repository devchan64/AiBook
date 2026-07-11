# P2-13.2 基础图表与公式形状的确认

> Section ID: `P2-13.2`
> Version: `v2026.07.09`

在 P2-13.1，我们把图表（plot）看成确认数字形状的工具。现在开始把几种基础图表直接连起来看。

本节的核心不是“背 Matplotlib 函数名”，而是先确定问题，再建立为这个问题选择合适图表的感觉。

本节说明 `折线图（line plot）`、`散点图（scatter plot）`、`直方图（histogram）`、`损失曲线（loss curve）` 的基本区分。关于 `plot` 本身的角色，以及 `Figure`、`Axes` 的代表性说明，放在 P2-13.1 和[概念词汇表](/AiBook/en/reference/concept-glossary/)中；这里重点讨论：面对什么问题，应该先选哪一种基础图表。

## 用不同问题重新阅读同一个学习场景

本节不为每种图表分别举一个完全不同世界的例子，而是把`检查学习过程的场景`用几个不同问题重新阅读。

| 在同一场景里提出的问题 | 先想到的图表 | 为什么适合这张图 |
| --- | --- | --- |
| epoch 增加时，loss 怎样变化？ | 折线图（line plot） | 因为核心是顺序上的变化。 |
| 输入值变大时，观测值也会一起变大吗？ | 散点图（scatter plot） | 因为要同时看样本之间的关系和分散程度。 |
| 分数或测量值集中在哪些区间？ | 直方图（histogram） | 因为想看分布与集中。 |

即使是在同一个场景里，只要问题改变，图表选择也会改变。抓住这个连接后，留下来的不会只是图表名称，而会是`问题-图表对应`。

## 本节范围

本节只在入门层面处理 Matplotlib 的基础图表。不讨论样式装饰、配色系统、带多坐标区的复杂 Figure，也不讨论交互式可视化。

本节回答以下问题。

- 折线图什么时候使用？
- 散点图会展示什么？
- 直方图会展示什么是仅靠平均值看不到的？
- 用图表确认公式变化或 loss 变化，究竟是什么意思？
- 为什么作图时要加坐标轴、标题和标签？

## 本节目标

- 能区分折线图、散点图、直方图的基本用途。
- 能把公式形状用代码计算出来，并用图表确认。
- 能通过损失曲线（loss curve）对学习流程提出问题。
- 能说明图表为什么需要坐标轴标签和标题。
- 能保持“图表不是结论，而是检查工具”的视角。

## 三个判断标准

| 标准 | 为什么重要 | 本节需要达到的理解程度 |
| --- | --- | --- |
| 折线图什么时候使用？ | 它帮助你区分“有顺序的值”和“有关联的值”各该用什么图。 | 理解它适用于查看顺序或时间上的变化。 |
| 散点图和直方图有什么不同？ | 它帮助你把“关系”和“分布”读成两个不同问题。 | 理解前者看两个值的关系，后者看数值集中在哪里。 |
| 为什么标题和坐标轴标签重要？ | 它明确告诉你，图表解释不只靠图形本身。 | 理解图表解释要和文字一起完成。 |

| 术语 | 本节先抓住的含义 |
| --- | --- |
| 折线图（line plot） | 用线连接顺序或时间上的数值变化的图表。 |
| 散点图（scatter plot） | 用点展示两个变量关系与分散程度的图表。 |
| 直方图（histogram） | 展示各区间内数值集中程度的图表。 |
| 损失曲线（loss curve） | 展示损失随着训练重复而如何变化的折线图。 |
| 坐标轴标签（axis label） | 说明图表中横轴和纵轴各代表什么的文字。 |

## 折线图用来看顺序上的变化

当 x 轴上的顺序有意义时，折线图经常会被使用。像时间、重复次数、训练 epoch、输入值的连续变化这种“从左到右有阅读流程”的情况，都很适合。

确认公式的形状时，折线图也是基础工具。比如 \(y = x^2\) 虽然也能做成数字表，但画成图后，U 形会立刻显现出来。

问题情境：把公式值列成表时，精确数字能看到，但很难马上抓住整体曲线形状。
输入（input）：连续变化的 x 值，以及每个 x 对应的 \(y = x^2\) 计算值。
期望输出（output）：显示 \(y = x^2\) 整体形状的折线图。
要确认的概念：折线图适合确认函数随连续输入变化而形成的形状，而坐标轴标签与标题应明确这张图在回答什么问题。

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 121)
y = x**2

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Function shape: y = x^2")
plt.show()
```

输出结果如下所示。

![函数 y 等于 x 平方的形状折线图](../../../assets/part-02/chapter-13/basic-line-function-shape.png)

这张图展示的不是解题过程，而是形状。

- 在 \(x=0\) 附近最低。
- 随着 \(x\) 向左右两侧远离，\(y\) 会变大。
- 斜率（slope）会随着位置不同而变化。

这种确认会直接连接到 P2-4 中处理过的导数（derivative）、梯度（gradient）、损失函数（loss function）直觉。

## 散点图用来看两个值的关系

散点图会把每个样本（sample）画成一个点。当你把不同的值放在 x 轴和 y 轴上，并想确认这两个值是否一起变化时，它就很有用。

例如，如果你想看“某个输入值增大时，观测值是否也大致增大”，就可以使用散点图。

问题情境：你想用眼睛确认两个值是否一起变大，以及点分散得有多开。
输入（input）：连续的 `x` 值和混入噪声的观测值 `y`。
期望输出（output）：能同时看到关系方向和波动的散点图。
要确认的概念：散点图会同时展示关系候选与由波动、噪声带来的分散。

```python
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(42)
x = np.linspace(1, 10, 24)
y = 2.5 * x + rng.normal(0, 2.2, size=x.shape)

fig, ax = plt.subplots()
ax.scatter(x, y)
ax.set_xlabel("input value")
ax.set_ylabel("observed value")
ax.set_title("Scatter plot: relationship with variation")
plt.show()
```

输出结果如下所示。

![展示带有分散关系的散点图](../../../assets/part-02/chapter-13/basic-scatter-relationship.png)

在这张图中，点并不落在一条完美直线上，但整体仍然呈现出“往右走时大致往上”的趋势。

这里可以这样读取。

- 一个点代表一个样本。
- 点群的方向显示一种关系候选。
- 点的分散程度显示波动（variation）或噪声（noise）。
- 不能只凭散点图就断定原因。

## 直方图用来看值集中在哪里

直方图（histogram）会把数值分成若干区间（bin），并展示每个区间里有多少个值。如果只看一个平均值（mean），就可能错过数据真正集中在哪里。

问题情境：只看平均值时，很难知道样本值实际集中在哪些位置。
输入（input）：从正态分布中抽取的 `values` 样本列表。
期望输出（output）：展示各数值区间计数的直方图。
要确认的概念：直方图能帮助你确认数值的集中、偏斜与稀少区间。

```python
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(7)
values = rng.normal(loc=0, scale=1, size=240)

fig, ax = plt.subplots()
ax.hist(values, bins=18)
ax.set_xlabel("value")
ax.set_ylabel("count")
ax.set_title("Histogram: where values gather")
plt.show()
```

输出结果如下所示。

![显示数值集中区间的直方图](../../../assets/part-02/chapter-13/basic-hist-distribution.png)

看直方图时，可以问下面这些问题。

- 数值最集中在哪个区间？
- 是否向某一侧偏斜？
- 两端是否存在稀少值？
- 是否存在只看平均值会漏掉的形状？

这些问题会直接连接到 P2-5 中处理过的分布（distribution）、平均值（mean）、方差（variance）。

## 损失曲线用于检查学习流程

在 AI 学习中，我们经常确认损失（loss）在重复过程中是怎样变化的。此时，折线图不只是把公式画得更漂亮，而是变成了检查学习是否按预期方向进行的工具。

问题情境：你想把稳定下降的损失和中途摇摆的损失放在一起比较学习流程。
输入（input）：epoch 编号，以及两组损失列表 `decreasing_loss`、`unstable_loss`。
期望输出（output）：把两条损失曲线一起画出的比较折线图。
要确认的概念：损失曲线能让你快速检查学习是否稳定、是否在中间摇摆。

```python
import matplotlib.pyplot as plt
import numpy as np

epochs = np.arange(1, 11)
decreasing_loss = [2.4, 1.8, 1.35, 1.08, 0.91, 0.79, 0.70, 0.64, 0.60, 0.57]
unstable_loss = [2.4, 1.9, 1.75, 1.82, 1.55, 1.62, 1.45, 1.52, 1.40, 1.46]

fig, ax = plt.subplots()
ax.plot(epochs, decreasing_loss, marker="o", label="steady decrease")
ax.plot(epochs, unstable_loss, marker="o", label="unstable")
ax.set_xlabel("epoch")
ax.set_ylabel("loss")
ax.set_title("Loss curves can reveal training behavior")
ax.legend()
plt.show()
```

输出结果会像下面这样，让你比较两种流程。

![比较稳定下降损失与摇摆损失的折线图](../../../assets/part-02/chapter-13/basic-loss-curve-comparison.png)

看这张图时，不应立刻下结论说“这是好模型”。但你可以继续提出下面这些问题。

- 损失是否大体在下降？
- 中间是否出现明显摇摆？
- 从哪一点开始，下降速度变慢了？
- 是否需要把 train loss 和 validation loss 分开看？

最后一个问题会通向 Part 3 的过拟合（overfitting）、验证（validation）、泛化（generalization）。

## 坐标轴、标题、标签都是解释的一部分

在图表中，坐标轴（axis）、标题（title）、标签（label）不是附加装饰，而是读者判断“自己正在看什么”的标准。

糟糕的图表虽然画出了数字，却把问题藏起来了。

问题情境：没有坐标轴和标题时，很难立刻知道图表在展示什么。
输入（input）：只有 `ax.plot(x, y)` 一行的最小代码。
期望输出（output）：能看到线条，但看不出问题是什么的不完整图表代码。
要确认的概念：图表代码不能只停留在“把数据画出来”，还需要解释信息。

```python
ax.plot(x, y)
```

相反，如果像下面这样加上坐标轴和标题，就会更清楚地知道这张图回答什么问题。

问题情境：你想给同一张图加上坐标轴名称和标题，使问题更明确。
输入（input）：在 `ax.plot(x, y)` 上追加 x 轴、y 轴、标题设置的代码。
期望输出（output）：能读出“画了什么”的更具说明性的图表代码。
要确认的概念：坐标轴标签和标题本身就是图表解释的一部分。

```python
ax.plot(x, y)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Function shape: y = x^2")
```

这里至少要养成加上下面三项的习惯。

| 元素 | 作用 |
| --- | --- |
| x 轴标签 | 说明横向数值代表什么 |
| y 轴标签 | 说明纵向数值代表什么 |
| 标题 | 概括这张图要回答的问题 |

## 用一句话整理基础图表选择

基础图表可以像下面这样选。

| 想看的东西 | 先想到的图表 |
| --- | --- |
| 顺序上的变化 | 折线图（line plot） |
| 两个值的关系 | 散点图（scatter plot） |
| 数值的集中与分散 | 直方图（histogram） |
| 学习过程中的变化 | 损失曲线（loss curve） |

这张表不是要背的公式，而是用来确认“你正在向数据提出什么问题”的出发点。

## 本节记住的视角

| 本章给出的抓手 | 下一章进一步看的内容 | 在 Part 3 中再次使用的位置 |
| --- | --- | --- |
| 按照想看“变化、关系、分布”中的哪一种来选择图表的标准 | 如何把这种解释变化和图表选择作为记录留在 Git 里 | 在查看损失曲线、变量关系、误差分布后，调整下一次实验或说明时 |

- 折线图适合确认顺序或连续变化的形状。
- 散点图适合看两个值的关系和分散程度。
- 直方图适合看数值集中在哪里。
- 损失曲线用于检查学习朝着什么方向移动。
- 坐标轴、标题和标签都是图表解释的一部分。

## 用案例来看

### 案例 1. 因为不知道该用什么图，所以随便画一个图的时候

假设一位学习者手上同时有训练日志和分数数据。loss 按 epoch 记录，学习时间和分数按样本成对出现，考试分数则一次性汇总了很多学生的数据。换句话说，这是把前面提到的`同一个学习场景`重新读成三个问题的情况。

人一开始很容易想，“反正要画一张图，那就先随便画一个。” 但问题不同，图表也必须不同。损失变化更自然地适合折线图，两个值一起变化更自然地适合散点图，数值集中在哪里则更自然地适合直方图。

这就是为什么本节让你先看`我到底在问什么问题`，而不是先看图表名称。即使是同一份数据，只要想看的是变化、关系还是分布，图表选择就会不同。

一旦换图表，可检查的结果就会显现出来。把按 epoch 记录的 loss 画成折线图时，流程会更清楚；把同样的数据画成直方图时，问题反而变模糊。相反，分数分布在直方图中会更清楚地显现。

## 简短检查

- 能用折线图确认 \(y = x^2\) 的形状吗？
- 能说明散点图里一个点代表什么吗？
- 能说明直方图展示的是与平均值不同的信息吗？
- 能通过损失曲线提出关于学习流程的问题吗？
- 能说明为什么作图时要加 x 轴、y 轴和标题吗？

## 什么时候应先想起这个视角

- 当你需要区分折线图、散点图、直方图等基础图表各自在回答什么问题时，先想起本节。
- 当你需要把公式形状、单个点的意义、分布的样子用实际图形确认出来时，回到这些基础图表示例。
- 当你想解释为什么图表要加坐标轴标签与标题，或者想读出像损失曲线这样的学习流程时，再次检查本节。

## 来源与参考资料

- Matplotlib Developers, `Quick start guide`, Matplotlib documentation, 确认日期：2026-06-25. [https://matplotlib.org/stable/users/explain/quick_start.html](https://matplotlib.org/stable/users/explain/quick_start.html){: target="_blank" rel="noopener noreferrer" }
- Matplotlib Developers, `Plot types`, Matplotlib documentation, 确认日期：2026-06-25. [https://matplotlib.org/stable/plot_types/index.html](https://matplotlib.org/stable/plot_types/index.html){: target="_blank" rel="noopener noreferrer" }
- Matplotlib Developers, `matplotlib.pyplot`, Matplotlib API reference, 确认日期：2026-06-25. [https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.html](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.html){: target="_blank" rel="noopener noreferrer" }
