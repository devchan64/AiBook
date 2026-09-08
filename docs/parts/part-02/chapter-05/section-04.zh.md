# P2-5.4 用小数据确认概率与统计

> Section ID: `P2-5.4`
> Version: `v2026.09.08`

用八个分数计算均值和方差，在包含极端值的数据中比较均值与中位数，再计算不同样本的均值，观察样本构成带来的差异。

![在小数据上区分原始数据、中心、扩散与样本估计的流程](/AiBook/assets/part-02/chapter-05/small-data-statistics-check-zh.svg)

## 中心与离散程度的计算

| 标准 | 为什么重要 |
| --- | --- |
| 代码会通过数字和输出把概念显示出来 | 只有看到均值、方差、样本均值在实际计算里怎样出现，概念和输出才会真正连起来。 |
| 均值和中位数要一起看 | 它们都在谈中心，但碰到极端值时反应不同。 |
| 方差会补上扩散信息 | 只看中心，无法把数据的性格讲完整。 |

## 执行环境

本节代码使用 NumPy。

笔记本代码单元与终端的区别参见[命令的执行位置](../chapter-03/section-05.zh.md#_2)。按从上到下的顺序运行代码块。

如果使用 Google Colab，可以先在代码单元里像下面这样准备 NumPy。

在 Colab 代码单元运行 `%pip install numpy`，会把 NumPy 安装到当前内核中。

```python
# 这条命令是在 Colab/Jupyter 代码单元里安装 NumPy。
%pip install numpy
```

如果使用本地 PC，可以在自己的终端里使用下面的命令。

```bash
python -m pip install numpy
```

本节完整示例代码也可以在下面这个文件中查看。

- [p2_5_4_small_statistics.py](/AiBook/assets/part-02/chapter-05/p2_5_4_small_statistics.py)

如果从项目根目录运行，可以使用下面的命令。

```bash
python docs/assets/part-02/chapter-05/p2_5_4_small_statistics.py
```

## 创建分数数组

先用一组小数据列表开始计算。

把八个分数放入数组 `data`，打印数值和元素个数 `8`。此数组是后续均值与方差计算的输入。

```python
# 这个例子导入 NumPy，为小数据的平均值、中位数和方差计算做准备。
import numpy as np

# data 是用来确认平均值、中位数和方差的小型分数数据。
data = np.array([42, 55, 48, 63, 52, 50, 47, 70])

print(data)

# size 表示这个数据里有多少个值。
print(data.size)
```

输出可以像下面这样阅读。

```text
[42 55 48 63 52 50 47 70]
8
```

这里的 `data` 不是现实的全部。它只是我们观察到的一小组数据。用前一节的说法，它可以被读成一个 `样本(sample)`。

在这一步，最重要的问题是：这些数字记录的是什么、它们是通过什么方式收集来的、以及它们能不能代表整体。

代码会帮你计算，但数据究竟意味着什么，仍然要由人来决定。

## 计算均值

`均值(mean)` 会把数据的中心总结成一个数字。

对 `data` 应用 `np.mean`，得到均值 `53.375`。

```python
# mean_value 是把 data 中所有值概括成一个中心值的平均值。
mean_value = np.mean(data)
print(mean_value)
```

输出是 `53.375`。

这个数字代替的是下面这个计算。

\[
\frac{42 + 55 + 48 + 63 + 52 + 50 + 47 + 70}{8} = 53.375
\]

均值很方便，但只看一个均值并不能把数据的全部形状都讲出来。均值告诉我们中心，但数值分散得有多开，还得另外看。

而且，均值会被一个特别大或特别小的值拉动。这时可以一起看的一个代表值就是 `中位数(median)`。

## 极端值与中位数

`中位数(median)` 是数值按大小排序后的中间值。数值个数为偶数时，取中间两个值的平均。

下面这组数据里，有一个值特别大。

在 `skewed_data` 中放入大值 `100`，比较均值与中位数。预期结果分别为 `30.0` 和 `13.0`。

```python
# skewed_data 包含极端值 100，用来比较平均值和中位数的反应差异。
skewed_data = np.array([10, 12, 13, 15, 100])

print(np.mean(skewed_data))
print(np.median(skewed_data))
```

输出是 `30.0`、`13.0`。

均值因为受到 `100` 的强烈影响而变成 `30.0`。但中位数是排好序后正中间的 `13.0`。

均值要把所有值都加起来再计算中心，所以容易被一个特别大或特别小的值拉动。相比之下，中位数只看排序后的中间位置，因此对 `极端值(outlier)` 相对不那么敏感。

在现实数据里，经常会出现一边拖得很长的分布。像用户使用时长、等待时间、响应延迟、收入这类数据里，有些值可能特别大。如果只看均值，就很容易误读数据“通常是什么样子”。

## 偏差、平方偏差与方差

`方差(variance)` 是用来观察数值在均值周围扩散了多少的数字。

先从每个值里减去均值。

打印 `data` 减去均值后的偏差，保留三位小数。这些值表示各个数值高于或低于中心多少。

```python
# centered 表示每个值距离平均值有多远。
centered = data - np.mean(data)
print(np.round(centered, 3))
```

输出可以像下面这样阅读。

```text
[-11.375   1.625  -5.375   9.625  -1.375  -3.375  -6.375  16.625]
```

这些值告诉我们，每个数据离均值有多远。比如 42 比均值低 11.375，70 比均值高 16.625，55 比均值高 1.625。

接下来把这些距离平方。

将偏差数组 `centered` 平方。平方偏差使正负差值不会互相抵消。

```python
# squared_deviations 会把偏差平方，让负向和正向差距都作为离散程度来读。
squared_deviations = centered ** 2
print(np.round(squared_deviations, 3))
```

输出可以像下面这样阅读。

```text
[129.391   2.641  28.891  92.641   1.891  11.391  40.641 276.391]
```

方差可以看作这些平方距离再取平均之后得到的值。

用 `np.var(data)` 计算平方偏差的均值，得到方差 `72.984375`。

```python
# np.var(data) 会把 data 的离散程度概括成一个方差值。
print(np.var(data))
```

输出是 `72.984375`。

## 方差分母与 ddof

NumPy 的 `np.var(data)` 默认会把整组数据当作一个总体来计算方差。这时，它是用 \(N\) 这个值的个数去做除法。

但在统计里，当我们用样本去估计总体方差时，经常会使用除以 \(N - 1\) 的 `样本方差(sample variance)`。在 NumPy 里，可以通过指定 `ddof=1` 来检查。

对同一个 `data` 使用默认设置和 `ddof=1`，分别得到 `72.984375` 和 `83.41071428571429`，可比较分母变化的影响。

```python
# ddof=1 是计算样本方差时使用的设置。
print(np.var(data))
print(np.var(data, ddof=1))
```

输出是 `72.984375`、`83.41071428571429`。

两个值会不同。这并不表示代码错了，而是说明：`我们把这组数据看成整体，还是看成样本`，会影响计算设置。

| 计算 | 代码 | 工作性解释 |
| --- | --- | --- |
| 总体方差 | `np.var(data)` | 把这组数据当作整体来计算扩散。 |
| 样本方差 | `np.var(data, ddof=1)` | 把这组数据当作样本，用来估计总体的扩散。 |

`np.var` 的分母是 `N − ddof`。应根据计算的是数据本身的离散程度，还是从样本估计总体方差，选择设置。

## 比较样本均值

把 `population_like` 中的 12 个值视为一个小总体。将选出的三个样本 `samples` 的均值与总体均值 `54.75` 比较。

```python
# 本例把 population_like 中的 12 个值视为一个小总体。
population_like = np.array([42, 45, 47, 48, 50, 52, 55, 58, 61, 63, 66, 70])

# samples 是用来模拟只观察到 population_like 一部分的样本集合。
samples = np.array([
    [42, 47, 50, 55],
    [48, 52, 63, 70],
    [45, 55, 58, 66],
])

print(np.mean(population_like))

# 依次确认每个样本的平均值是否会变化。
for sample in samples:
    print(sample, np.mean(sample))
```

输出可以像下面这样阅读。

```text
54.75
[42 47 50 55] 48.5
[48 52 63 70] 58.25
[45 55 58 66] 56.0
```

本例的总体均值为 `54.75`。但根据选取的样本不同，样本均值分别为 `48.5`、`58.25`、`56.0`。

这三个样本是为了比较而手动选取的，并非随机抽样结果。总体均值只有一个，但样本均值会随样本而变化，因此样本均值是总体均值的估计值。

## 计算结果与样本代表性

代码可以很快算出均值和方差。但怎样解释这些数字，是另一件事。

例如，看到均值是 `53.375`，如果马上下结论说“这个服务全部用户的平均值就是 53.375”“这组数据完美代表整体”“方差大，所以数据不好”，就会很危险。

更谨慎的说法会更接近：“在这组数据里，均值是 53.375”“这些值在均值周围有一定程度的扩散”“这组数据能否代表整体，还要结合收集方式和样本构成一起看”。

AI 数据也需要同样的态度。训练数据的均值，是在训练数据集内部算出来的摘要值；测试数据的分数，是从测试样本上得到的评估值；而现实表现，则要通过另外的样本、部署后的观察、持续评估来确认。

## 改变极端值进行比较

把 `skewed_data` 的最后一个值从 `100` 改为 `1000`，再次打印均值与中位数。均值增大到 `(10 + 12 + 13 + 15 + 1000) / 5 = 210`，中位数仍为 `13`。

再把最后一个值改为 `14`。排序后为 `10, 12, 13, 14, 15`，均值为 `12.8`，中位数为 `13`。比较这两次输出，可看出一个大值把均值拉高了多少。

## 检查清单

- 能把一组小数据做成 NumPy `array`。
- 能用 `np.mean` 计算 `均值(mean)`。
- 能用 `np.median` 计算 `中位数(median)`。
- 能说明均值会被 `极端值(outlier)` 拉动。
- 能检查每个值离均值有多远。
- 能用 `np.var` 计算 `方差(variance)`。
- 能说明 `ddof=1` 可以用于样本方差计算。
- 能说明 `样本均值(sample mean)` 会随着样本变化而变化。
- 能把代码输出和数据收集方式、样本代表性、解释问题区分开来看。
- 能把均值、中位数和方差的定义与实际数字和代码输出联系起来解释。

## 来源与参考资料

- NumPy Developers, [numpy.array](https://numpy.org/doc/stable/reference/generated/numpy.array.html){: target="_blank" rel="noopener noreferrer" }, NumPy Reference, 确认日期: 2026-07-20。用于确认把小型数字列表创建成 NumPy 数组的示例。
- NumPy Developers, [numpy.ndarray.size](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.size.html){: target="_blank" rel="noopener noreferrer" }, NumPy Reference, 确认日期: 2026-07-20。用于确认通过 `data.size` 读取数组元素个数的示例。
- NumPy Developers, [numpy.mean](https://numpy.org/doc/stable/reference/generated/numpy.mean.html){: target="_blank" rel="noopener noreferrer" }, NumPy Reference, 确认日期: 2026-07-20。用于确认算术均值和数组均值计算。
- NumPy Developers, [numpy.median](https://numpy.org/doc/stable/reference/generated/numpy.median.html){: target="_blank" rel="noopener noreferrer" }, NumPy Reference, 确认日期: 2026-07-20。用于确认中位数是排序副本的中间值，或在偶数个值时取中间两个值的平均。
- NumPy Developers, [numpy.var](https://numpy.org/doc/stable/reference/generated/numpy.var.html){: target="_blank" rel="noopener noreferrer" }, NumPy Reference, 确认日期: 2026-07-20。用于确认方差、`ddof`、总体方差与样本方差计算设置的差异。
- Barbara Illowsky, Susan Dean, [Introductory Statistics, 1.2 Data, Sampling, and Variation in Data and Sampling](https://openstax.org/books/introductory-statistics/pages/1-2-data-sampling-and-variation-in-data-and-sampling){: target="_blank" rel="noopener noreferrer" }, OpenStax, 确认日期: 2026-07-20。用于确认样本应代表总体，以及抽样方式可能带来波动这一统计背景。
