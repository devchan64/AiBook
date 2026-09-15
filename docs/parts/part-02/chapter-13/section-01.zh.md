# P2-13.1 图形能揭示什么？

> Section ID: `P2-13.1`
> Version: `v2026.09.15`

## 损失的变化

这些虚构记录用于说明损失随训练迭代的变化。表格能准确显示第三个值为 1.12；折线图则能显示下降幅度逐渐减小的形状。

| epoch | loss |
| ---: | ---: |
| 1 | 2.40 |
| 2 | 1.65 |
| 3 | 1.12 |
| 4 | 0.86 |
| 5 | 0.79 |

第一次下降为 `2.40 - 1.65 = 0.75`，最后一次为 `0.86 - 0.79 = 0.07`。下面的代码把五个有顺序的值画成点并连接起来。

```python
import matplotlib.pyplot as plt

epochs = [1, 2, 3, 4, 5]
loss = [2.40, 1.65, 1.12, 0.86, 0.79]

fig, ax = plt.subplots()
ax.plot(epochs, loss, marker="o")
ax.set_xlabel("epoch")
ax.set_ylabel("loss")
ax.set_title("Loss decreases over epochs")
plt.show()
```

生成的曲线随轮次增加而下降。

![损失随轮次下降](/AiBook/assets/part-02/chapter-13/pyplot-loss-line-zh.svg)

三个语言版本的图形均由相同数据生成。此脚本重新生成本节的 SVG 资源。正文代码用 `plt.show()` 显示图形，脚本则在保存文件后关闭图形。

[p2_13_1_plot_questions.py](/AiBook/assets/part-02/chapter-13/p2_13_1_plot_questions.py)

```bash
python docs/assets/part-02/chapter-13/p2_13_1_plot_questions.py
```

## 平均值相同，变化不同

动作 A 的区段值为 `[1.0, 2.0, 2.0, 1.0]`，动作 B 为 `[1.5, 1.5, 1.5, 1.5]`。平均值都是 1.5，但 A 在中间升高，B 始终不变。只画平均值会隐藏这一差异，因此要比较各区段的值。

```python
import matplotlib.pyplot as plt

steps = [1, 2, 3, 4]
action_a = [1.0, 2.0, 2.0, 1.0]
action_b = [1.5, 1.5, 1.5, 1.5]

fig, ax = plt.subplots()
ax.plot(steps, action_a, marker="o", label="action A")
ax.plot(steps, action_b, marker="o", label="action B")
ax.set_xlabel("segment")
ax.set_ylabel("signal level")
ax.set_title("Same mean, different pattern")
ax.legend()
plt.show()
```

![平均值相同而模式不同的两个信号](/AiBook/assets/part-02/chapter-13/same-mean-pattern-zh.svg)

## 趋势、关系、分布与异常值

图形能展示数值变化、变量之间的关系、数值集中区间，以及远离其他值的观测。

| 问题 | 图形帮助揭示的内容 | 例子 |
| --- | --- | --- |
| 趋势 | 数值随时间或顺序的变化 | 各训练轮次的损失 |
| 关系 | 两个值是否共同变化 | 学习时间与分数 |
| 分布 | 数值集中在哪里 | 分数或误差分布 |
| 异常值 | 是否存在明显偏离的值 | 远离其他值的传感器读数 |

## 学习时间与分数的关系

来看这四名学生的记录。

| name | study_hours | score |
| --- | ---: | ---: |
| Kim | 2 | 62 |
| Park | 4 | 71 |
| Lee | 6 | 82 |
| Choi | 8 | 88 |

表格适合读取准确值。若要判断学习时间更长的学生是否也往往分数更高，散点图更直观。

```python
import matplotlib.pyplot as plt

study_hours = [2, 4, 6, 8]
scores = [62, 71, 82, 88]

fig, ax = plt.subplots()
ax.scatter(study_hours, scores)
ax.set_xlabel("study hours")
ax.set_ylabel("score")
ax.set_title("Study hours and score")
plt.show()
```

一个点代表一名学生。Kim 位于 `(2, 62)`，Choi 位于 `(8, 88)`。在这四条记录中，学习时间较长的学生分数较高。

![学习时间与分数](/AiBook/assets/part-02/chapter-13/pyplot-study-scatter-zh.svg)

图形不能证明因果关系，但能让两个值共同变化的模式更容易观察。

## Figure 与 Axes

Matplotlib 将绘图描述为在 `Figure` 上画数据。Figure 是整张图，可以包含一个或多个 `Axes`。Axes 是实际绘制数据的坐标区域。

| 术语 | 直观理解 |
| --- | --- |
| `Figure` | 整张画纸 |
| `Axes` | 绘制坐标和数据的区域 |
| `plot`、`scatter`、`hist` | 决定如何在 Axes 上画数据的方法 |

用 `plt.subplots()` 创建图形和坐标区域，再连接 `(1, 2)`、`(2, 4)` 和 `(3, 3)`。

```python
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [2, 4, 3])
plt.show()
```

这里 `plt.subplots()` 返回一个 Figure 和一个 Axes，再通过 `ax.plot(...)` 等方法在 Axes 上绘制数据。

`ax.set_xlabel(...)` 设置 x 轴名称，`ax.set_title(...)` 设置区域标题。在一个 Figure 中放入多个 Axes，就能在同一画面上比较不同图形。

## 根据问题选择图形

Matplotlib 提供折线图（`plot`）、散点图（`scatter`）、条形图（`bar`）和直方图（`hist`）等基本形式。

根据需要观察顺序变化还是比较类别，选择表达方式。

| 问题 | 常用图形 |
| --- | --- |
| 想看按顺序的变化？ | 折线图 |
| 想看两个值的关系？ | 散点图 |
| 想比较各类别大小？ | 条形图 |
| 想看值集中在哪里？ | 直方图 |

这张表是起点，不是固定规则。实际选择取决于数据形态、读者的问题和想传达的信息。

## 坐标范围与解读

图形把许多数值压缩到一个画面中。同一份数据也会因坐标范围和表达方式不同而给人不同印象。

例如：

- 改变坐标范围，会让变化看起来更大或更小。
- 把少量点连接起来，可能暗示超出实际观测的连续性。
- 过度使用颜色或面积，会放大不重要的差异。
- 只画平均值，可能隐藏分布或异常值。

阅读图形时，应同时确认：

1. x 轴和 y 轴分别是什么？
2. 一个点或一条线代表什么？
3. 是否有缺失值或被隐藏的范围？
4. 图形展示的是观测还是解释？

## 相同数值，不同坐标范围

分数 `[80, 82, 81, 83]` 的最大值与最小值相差三分。y 轴为 0～100 时变化看起来较小，缩小到 79～84 后，同样的变化会显得很大。

```python
attempts = [1, 2, 3, 4]
scores = [80, 82, 81, 83]
fig, axes = plt.subplots(1, 2, figsize=(8, 3.6), sharex=True)
for ax in axes:
    ax.plot(attempts, scores, marker="o")
    ax.set_xlabel("attempt")
    ax.set_ylabel("score")
axes[0].set_ylim(0, 100)
axes[0].set_title("Full range: 0 to 100")
axes[1].set_ylim(79, 84)
axes[1].set_title("Zoomed range: 79 to 84")
fig.tight_layout()
plt.show()
```

![相同分数在完整与放大坐标范围下的比较](/AiBook/assets/part-02/chapter-13/axis-range-comparison-zh.svg)

右图有助于观察小变化，但若把陡峭的线条理解为分数差很大，就会产生误读。放大坐标后，实际差仍是三分。比较两个实验的变化量时，应采用相同坐标范围，或明确标示范围差异。

## 分数分布

把 `[45, 62, 71, 73, 82, 88, 90]` 分为五个区间并计数。直方图能显示仅凭平均值看不到的集中和分散。

```python
import matplotlib.pyplot as plt

scores = [45, 62, 71, 73, 82, 88, 90]

fig, ax = plt.subplots()
ax.hist(scores, bins=5)
ax.set_xlabel("score")
ax.set_ylabel("count")
ax.set_title("Score distribution")
plt.show()
```

结果显示哪些分数区间集中了更多值。

![分数分布](/AiBook/assets/part-02/chapter-13/pyplot-score-hist-zh.svg)

这段代码不计算平均值，而是查看分数集中在哪里。

## 案例：找出损失突增的区间

把第一个例子的损失列表 `[2.40, 1.65, 1.12, 0.86, 0.79]` 中第三个值改为 `2.10` 后重新绘图。起点和终点不变，但第二点到第三点上升 0.45，随后下降 1.24，第三点会形成峰值。

只记录总体下降量 `2.40 - 0.79 = 1.61`，就会漏掉中间的上升。图形提示需要复查的区间，却不能决定原因是数据批次、训练设置还是记录错误。还需检查该次迭代的输入与设置。

如果这表示训练损失，仅凭下降趋势也无法判断新数据上的表现，还需要单独检查验证损失或评估指标。

## 检查清单

- 能否解释图形如何揭示形状、变化、关系和分布？
- 能否区分表格的准确值读取与图形的模式观察？
- 能否区分 Figure 与 Axes？
- 能否先确定问题，再选择图形类型？
- 能否说明折线图、散点图、条形图和直方图的典型用途？
- 能否检查坐标、点的含义、隐藏范围和过度解读？
- 能否解释图形为何不能自动证明原因或结论？

## 来源与参考资料

- Matplotlib Developers, [Quick start guide](https://matplotlib.org/stable/users/explain/quick_start.html){: target="_blank" rel="noopener noreferrer" }, Matplotlib documentation, 查阅日期：2026-07-20. Figure/Axes 结构与子图。
- Matplotlib Developers, [Plot types](https://matplotlib.org/stable/plot_types/index.html){: target="_blank" rel="noopener noreferrer" }, Matplotlib documentation, 查阅日期：2026-07-20. 根据问题选择基本图形。
- Matplotlib Developers, [matplotlib.pyplot](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.html){: target="_blank" rel="noopener noreferrer" }, Matplotlib documentation, 查阅日期：2026-07-20. 示例使用的 pyplot 接口。
