# P2-15.1 把公式翻译成代码的小步骤

> Section ID: `P2-15.1`
> Version: `v2026.07.20`

在 Part 2，我们分别看过公式、Python、NumPy、Pandas、Matplotlib。现在把这条流程重新绑成一个整体。目标不是证明复杂公式，而是拥有一套把简单公式翻译成代码并检查结果的步骤。

学机器学习时，损失函数（loss function）、平均值（mean）、方差（variance）、线性组合（linear combination）这类公式会不断出现。要想在看到公式时不立刻卡住，就需要一种习惯：`把符号变成计算步骤`。

## 重新把前面章节的概念绑在一起的位置

这一节是把 Part 2 中分别学过的概念，通过一个例子重新绑在一起的位置。它不是大量引入新理论，而是展示：当前面章节的代表概念真正一起运作时，应检查什么。

| 从前面章节带来的概念 | 在本节中重新使用的方式 |
| --- | --- |
| 变量（variable）、值（value）、类型（type） | 先决定公式符号分别对应哪个代码变量、哪个值。 |
| 列表（list）、循环（loop） | 把 sigma 求和读成对每个样本重复计算。 |
| NumPy 数组（array）、向量化（vectorization） | 用更短的数组运算再次表达同一计算。 |
| 表格与图表 | 不只看最后一个数字，也一起检查中间值和趋势。 |
| Python 工作流 | 按输入、计算、输出、检查的顺序阅读并验证代码。 |

因此，本节的核心不是`背一个新公式`，而是`把已经见过的工具按步骤连接到同一个问题上`。

## 核心判断标准：把公式翻译成代码的小步骤

- 能先区分公式中的变量和数据组合。
- 能把 sigma 求和翻译成 Python 循环或 NumPy 计算。
- 能用一小段代码计算平均平方误差（mean squared error）。
- 能说明用数字、表格和图表检查代码结果的流程。
- 能获得一个阅读 Part 3 机器学习公式的最小步骤。

## 本节先抓住的连接

- 把公式符号变成代码变量。
- 先看每个样本的重复计算。
- 再把同一计算读成 NumPy 数组表达。
- 把最终数字、中间值和图表一起检查。

## 三个判断标准

| 标准 | 为什么重要 | 本节需要达到的理解程度 |
| --- | --- | --- |
| 把公式翻译成代码时先看什么？ | 它让你先把公式拆成计算步骤，而不是马上跳进语法。 | 理解要先分出输入、计算顺序和输出。 |
| 为什么要同时看循环和 NumPy？ | 它让你区分“理解步骤”和“理解压缩表达”。 | 理解同一个计算可能只是表达方式不同。 |
| 为什么要用多种方式检查结果？ | 它补足最终一个数字可能遗漏的中间含义。 | 理解一个数字本身可能隐藏中间过程和趋势。 |

## 把公式翻译成代码的基本顺序

把公式变成代码时，不要立刻写代码，而要先按下面的顺序阅读。

```mermaid
--8<-- "assets/part-02/chapter-15/formula-to-code-flow-zh.mmd"
```

关键点在于：不要一下子把公式整体变成代码。先决定符号指向什么，再确认这些值是单个数字还是一组数据，最后再计算。

## 用平均平方误差来读一个例子

平均平方误差（mean squared error, MSE）是把预测值和真实值的差平方后，再求平均得到的数值。

\[
\mathrm{MSE} = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2
\]

第一次看时它可能显得复杂，但把符号拆开后就会变成下面这样。

| 符号 | 含义 |
| --- | --- |
| \(n\) | 数据个数 |
| \(y_i\) | 第 i 个真实值 |
| \(\hat{y}_i\) | 第 i 个预测值 |
| \(y_i - \hat{y}_i\) | 第 i 个误差 |
| \((y_i - \hat{y}_i)^2\) | 误差平方 |
| \(\sum\) | 对所有数据相加 |
| \(\frac{1}{n}\) | 用数据个数去除总和，得到平均值 |

这个公式可以读成：“计算每个样本的误差，把误差平方，全部加起来，再除以样本数。”

## 先把它翻译成一个小 Python 循环

这里不先用 NumPy 把它缩成一行，而是先用循环确认计算流程。

问题情境：

- 即使读懂了公式，也可能没法马上把每个符号对应到代码里的循环和变量

输入（input）：

- 真实值列表 `actual`
- 预测值列表 `predicted`

期望输出（output）：

- 每个样本的平方误差列表
- 平均平方误差（MSE）数值

要确认的概念：

- sigma 求和可以翻译成循环，也可以翻译成数组计算
- 把公式翻译成代码时，最好先把每个样本的计算和最后的平均步骤分开看
- 循环版本会比压缩后的 NumPy 表达更先显露计算含义

```python
# 这个例子计算真实值和预测值之间的误差，并把损失公式翻译成代码。
actual = [3.0, 5.0, 7.0]
predicted = [2.5, 5.5, 8.0]

squared_errors = []

for y, y_hat in zip(actual, predicted):
    error = y - y_hat
    squared_errors.append(error ** 2)

mse = sum(squared_errors) / len(squared_errors)
print(mse)
```

这段代码几乎直接跟着公式的每个部分走。

| 公式中的部分 | 代码中的部分 |
| --- | --- |
| \(y_i\), \(\hat{y}_i\) | `y`, `y_hat` |
| \(y_i - \hat{y}_i\) | `error = y - y_hat` |
| \((y_i - \hat{y}_i)^2\) | `error ** 2` |
| \(\sum\) | `sum(squared_errors)` |
| \(\frac{1}{n}\) | `/ len(squared_errors)` |

这一步虽然短，也很简单，但很重要。它让你用手去确认：这个公式到底代表怎样的计算过程。

## 然后再用 NumPy 缩短同样的计算

在理解了计算流程之后，就可以借助 NumPy 数组（array）把它写得更短。

问题情境：

- 在用循环理解了含义之后，还应该能把同一个公式重新表达成更短的数组计算

输入（input）：

- 真实值数组 `actual`
- 预测值数组 `predicted`

期望输出（output）：

- 误差数组 `errors`
- 平方误差数组 `squared_errors`
- 平均平方误差 `mse`

要确认的概念：

- NumPy 数组运算会把 sigma 计算缩成向量化表达
- 即使代码更短，计算步骤的含义仍与循环版本相同

```python
# 这个例子计算真实值和预测值之间的误差，并把损失公式翻译成代码。
import numpy as np

actual = np.array([3.0, 5.0, 7.0])
predicted = np.array([2.5, 5.5, 8.0])

errors = actual - predicted
squared_errors = errors ** 2
mse = np.mean(squared_errors)

print(mse)
```

在 NumPy 中，两个数组相减时，会按对应位置计算。这直接连接到 Part 2 Chapter 11 中学过的向量化（vectorization）。

不过，NumPy 代码更短，并不代表一开始就更容易理解。在本节里，公式与代码的连接顺序是：`先用循环确认含义，再用 NumPy 缩短表达`。

## 不要只看最后一个数字

MSE 最后会变成一个数字。但在检查计算过程时，最好连中间值也一起看。

问题情境：

- 如果只看最终 MSE 数值，就很难马上读出到底哪个样本的误差更大

输入（input）：

- 上面算出的 `errors`
- `squared_errors`
- `mse`

输出（output）：

- 中间误差数组与最终平均平方误差

要确认的概念：

- 把中间值一起打印出来，可以检查公式每一步到底生成了什么数字
- 可以直接比较误差的符号和平方后的数值差别

```python
# 这个例子计算真实值和预测值之间的误差，并把损失公式翻译成代码。
print(errors)
print(squared_errors)
print(mse)
```

如果输出看起来和下面相似，就可以确认每一步的含义。

```text
[ 0.5 -0.5 -1. ]
[0.25 0.25 1.  ]
0.5
```

误差（error）有方向。预测值比真实值小还是大，会改变符号。但平方误差（squared error）不会变成负数。因此，MSE 成为一个用来平均衡量误差大小的指标。

## 也可以用图表来检查

如果只看数字，可能不容易一眼看出哪个样本的误差更大。用 Matplotlib 把真实值和预测值并排画出来，就更容易看出误差在哪些位置变大。

问题情境：

- 只看数值输出时，可能难以一眼把握每个样本差异的位置和大小

输入（input）：

- 真实值数组 `actual`
- 预测值数组 `predicted`
- 样本索引 `index`

输出（output）：

- 比较真实值与预测值的折线图

要确认的概念：

- 图表不会替代损失计算，但会成为解释误差分布的辅助工具
- 即使数字结果相同，可视化也能更快读出差异在哪些区间较大

```python
# 这个例子计算真实值和预测值之间的误差，并把损失公式翻译成代码。
import matplotlib.pyplot as plt

index = np.arange(len(actual))

fig, ax = plt.subplots()
ax.plot(index, actual, marker="o", label="actual")
ax.plot(index, predicted, marker="o", label="predicted")
ax.set_xlabel("sample index")
ax.set_ylabel("value")
ax.set_title("Actual and predicted values")
ax.legend()
plt.show()
```

这张图不会替你计算 MSE，而是帮助你用眼睛检查那些在压缩成一个数字之前的差异。

## 用案例来看

### 案例 1. 为什么看到损失公式后，还是不能马上写代码

假设一个学习者第一次看到平均平方误差公式，就卡在“这个怎么翻译成 Python？”这个问题上。人可能读得出公式的形状，但不一定能立刻连接上：`哪个值是单个数字`、`哪个值是一组样本`、`sigma 在代码里到底会变成什么样的重复`。

如果这时直接跳进一行 NumPy 代码，虽然可能拿到结果，却容易丢掉步骤。先把 `actual` 和 `predicted` 放成小列表，再用循环去求每个样本的误差、平方、总和、平均，那么公式的结构就会被转换成计算步骤。

然后再用 NumPy 数组把同样的计算缩短，就能把 `压缩表达` 和 `计算含义` 分开来读。换句话说，循环是解释公式的脚手架，而 NumPy 是把同样计算写得更简洁的表达。

这个案例会直接延续到 Part 3 之后的公式阅读。首先重要的不是快速写代码，而是先拥有把符号转换成“输入、重复、输出”步骤的感觉。

## 检查清单

- 能说明 MSE 公式里的 \(y_i\)、\(\hat{y}_i\)、\(n\)、\(\sum\) 各是什么意思吗？
- 能把同一个计算分别写成 Python 循环和 NumPy 数组计算吗？
- 能说明 `errors`、`squared_errors`、`mse` 之间的区别吗？
- 能说明为什么不能只看最终结果，而要检查中间值吗？
- 能说明图表是在帮助解释，而不是取代计算吗？
- 能在把公式翻译成代码时，先分开符号、数据形状和计算步骤吗？

## 来源与参考资料

- Python Software Foundation, `An Informal Introduction to Python`, Python documentation, 确认日期：2026-07-20. [https://docs.python.org/3/tutorial/introduction.html](https://docs.python.org/3/tutorial/introduction.html){: target="_blank" rel="noopener noreferrer" } 这是公式转代码示例中数字、列表和基础计算表达的依据。
- NumPy Developers, `NumPy: the absolute basics for beginners`, NumPy documentation, 确认日期：2026-07-20. [https://numpy.org/doc/stable/user/absolute_beginners.html](https://numpy.org/doc/stable/user/absolute_beginners.html){: target="_blank" rel="noopener noreferrer" } 这是数组创建、数组运算和用 `np.mean` 进行向量化计算说明的依据。
- Matplotlib Developers, `Quick start guide`, Matplotlib documentation, 确认日期：2026-07-20. [https://matplotlib.org/stable/users/explain/quick_start.html](https://matplotlib.org/stable/users/explain/quick_start.html){: target="_blank" rel="noopener noreferrer" } 这是用 `Figure`、`Axes`、`plot`、标签和图例检查计算结果图形的依据。
