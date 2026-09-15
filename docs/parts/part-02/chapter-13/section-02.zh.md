# P2-13.2 基本图形与函数形状

> Section ID: `P2-13.2`
> Version: `v2026.09.15`

## 折线图：函数形状

当 x 轴顺序有意义时，折线图通常很适合，例如时间、迭代次数、训练轮次或输入值的连续变化。

对于 \(y=x^2\)，输入 −3、0、3 分别得到 9、0、9。下面的代码在 −3 到 3 之间计算 121 个点，并连接成 U 形曲线。

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

输出如下：

![函数 y = x²](/AiBook/assets/part-02/chapter-13/basic-line-function-shape-zh.svg)

此脚本使用与正文相同的输入条件，保存三个语言版本的 SVG 图形。

[p2_13_2_basic_chart_shapes.py](/AiBook/assets/part-02/chapter-13/p2_13_2_basic_chart_shapes.py)

```bash
python docs/assets/part-02/chapter-13/p2_13_2_basic_chart_shapes.py
```

曲线展示以下特征：

- 在 \(x=0\) 处取得最小值 0。
- \(x\) 向零点两侧远离时，\(y\) 增大。
- 斜率随位置变化。

将 `y = x**2` 改为 `y = (x - 1)**2`，最低点从 `(0, 0)` 移到 `(1, 0)`，公式的变化反映在曲线位置上。

`np.linspace(-3, 3, 121)` 包含两个端点，生成间距为 0.05 的 121 个输入值。图形只是用线段连接已计算的点，并未计算所有实数输入。若将点数减为三个，就只连接 `(-3, 9)`、`(0, 0)`、`(3, 9)`，看起来像 V 形。即使公式相同，计算点过少也可能无法充分呈现曲线形状。

## 散点图：关系与分散

散点图将每个样本画成一个点，在 x 轴和 y 轴放置不同变量，用于观察两者如何共同变化。

这个人工数据集为 24 个输入计算 `2.5 * x`，再加入均值为 0、标准差为 2.2 的正态随机噪声，点便分散在直线周围。

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

输出如下：

![带有分散的关系](/AiBook/assets/part-02/chapter-13/basic-scatter-relationship-zh.svg)

点并不完全落在一条直线上，但向右总体呈上升趋势。

在此人工数据集中：

- 一个点代表一个样本。
- 点总体沿数值增大的方向分布。
- 偏离直线的程度反映加入的噪声。
- 仅凭散点图不能断定因果关系。

## 直方图：按区间计数

直方图把值分入区间，并显示各区间有多少值。下面从均值为 0、标准差为 1 的正态分布中抽取 240 个值，分入 18 个区间。柱高表示各区间的数量。

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

输出如下：

![按区间分组的数值](/AiBook/assets/part-02/chapter-13/basic-hist-distribution-zh.svg)

查看直方图时，可以问：

- 哪个区间的值最多？
- 是否偏向一侧？
- 两端是否有少见的值？
- 只看平均值会漏掉什么形状？

将 `bins=18` 改为 `bins=6`，会把同样的 240 个值放入更宽的区间。柱数和柱高改变，但数量总和仍为 240。

## 区间边界与被排除的值

将分数 `[45, 62, 71, 73, 82, 88, 90]` 按边界 `[40, 60, 80, 100]` 分组，三个柱的高度如下。边界列表的元素数比区间数多一个。

| 区间 | 分数 | 数量 |
| --- | --- | ---: |
| 40 ≤ 分数 < 60 | 45 | 1 |
| 60 ≤ 分数 < 80 | 62, 71, 73 | 3 |
| 80 ≤ 分数 ≤ 100 | 82, 88, 90 | 3 |

Matplotlib 的直方图区间通常包含左边界、不包含右边界，最后一个区间则两端都包含。因此 80 属于最后一个区间，最终边界 100 也被包含。设置 `bins=3, range=(60, 100)` 会排除 45，使数量总和变为六。改变可见坐标范围，与改变参与统计的数值范围不同。

比较两个群体的分布时，应使用相同边界。若分别设置 `bins=5`，两组最小值和最大值不同可能产生不同边界。这里 y 轴表示数量；使用 `density=True` 后，柱高变为概率密度，此时总和为 1 的是柱面积而不是柱高。

## 条形图：比较类别

假设虚构模型 A、B、C 在相同验证数据与损失函数下的损失为 `[0.42, 0.39, 0.47]`。模型名称是类别，不是数值区间，因此用 `bar` 比较。

```python
models = ["A", "B", "C"]
validation_loss = [0.42, 0.39, 0.47]
fig, ax = plt.subplots()
ax.bar(models, validation_loss)
ax.set_ylim(0, 0.55)
ax.set_xlabel("model")
ax.set_ylabel("validation loss")
ax.set_title("Model comparison on the same validation set")
plt.show()
```

![同一验证集上的模型损失](/AiBook/assets/part-02/chapter-13/basic-bar-model-comparison-zh.svg)

此记录中 B 的损失最低，比 A 低 0.03。条长用于表达大小，因此 y 轴从 0 开始。把 B 改为 0.49 后，最低的是 A。条形图显示已按类别给出的数值，而直方图将原始观测分入数值区间后计算数量。

## 损失曲线：下降与波动

比较两组虚构训练记录。第一组从 2.4 逐次下降到 0.57。第二组虽从 2.4 降到 1.46，却在第 4、6、8、10 次迭代相对前一次上升。

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

生成的图形可以比较这两种变化。

![下降与波动的损失](/AiBook/assets/part-02/chapter-13/basic-loss-curve-comparison-zh.svg)

这张图不能立即证明模型好坏，但可以帮助提出以下问题：

- 损失总体是否下降？
- 中途是否有明显波动？
- 从哪里开始下降变慢？
- 是否需要分别查看训练与验证损失？

两条曲线是不同的虚构记录，不是一对训练与验证损失。即使训练损失降低，也必须用验证数据另行确认在新数据上的表现。

## 坐标轴与标题

函数图的 x 轴是公式输入，y 轴是计算结果；损失图的 x 轴是迭代次数，y 轴是损失。即使线形相似，坐标含义不同，解释也会不同。用 `set_xlabel`、`set_ylabel`、`set_title` 标明变量和对象，多条线重叠时用 `label` 和 `legend()` 区分。

## 案例：颠倒损失记录的顺序

比较 `[2.4, 1.8, 1.2, 0.6]` 与其逆序 `[0.6, 1.2, 1.8, 2.4]`。两者包含相同值，平均值都为 1.5，但前者下降，后者上升。

使用相同区间边界的直方图完全一致，因为它只统计各值出现的次数，不保留顺序。以迭代编号为 x 轴的折线图则朝相反方向变化。

直方图可以回答损失值的分布问题。若要判断训练期间损失是否下降，就需要保留顺序的折线图。选择图形时，应确认所需信息仍被保留。

## 检查清单

- 能否根据变化、关系或分布来选择图形？
- 能否解释何时适合使用折线图？
- 能否说明散点图中一个点的含义及分散模式？
- 能否解释直方图比平均值多提供哪些分布信息？
- 能否根据损失曲线提出有关训练的问题？
- 能否选择图形来检查函数或分布形状？
- 能否解释坐标、标题和标签为何是解读的一部分？

## 来源与参考资料

- Matplotlib Developers, [Quick start guide](https://matplotlib.org/stable/users/explain/quick_start.html){: target="_blank" rel="noopener noreferrer" }, Matplotlib documentation, 查阅日期：2026-07-20. Axes 方法、标签和标题。
- Matplotlib Developers, [Plot types](https://matplotlib.org/stable/plot_types/index.html){: target="_blank" rel="noopener noreferrer" }, Matplotlib documentation, 查阅日期：2026-07-20. 折线图、散点图、条形图和直方图。
- Matplotlib Developers, [matplotlib.pyplot](https://matplotlib.org/stable/api/pyplot_summary.html){: target="_blank" rel="noopener noreferrer" }, Matplotlib documentation, 查阅日期：2026-07-20. 基本绘图的 pyplot 接口。
- Matplotlib Developers, [Axes.hist](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.hist.html){: target="_blank" rel="noopener noreferrer" }, 查阅日期：2026-09-15. 区间边界、range 与 density 的行为.
- NumPy Developers, [numpy.linspace](https://numpy.org/doc/stable/reference/generated/numpy.linspace.html){: target="_blank" rel="noopener noreferrer" }, 查阅日期：2026-09-15. 包含端点与采样点数.
