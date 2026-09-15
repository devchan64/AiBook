# P2-5.4 用小数据确认概率与统计

> Section ID: `P2-5.4`
> Version: `v2026.09.15`

计算不低于 60 分的观测比例，再检查八个分数的均值、中位数和方差。改变极端值并比较不同样本的均值，区分计算值与对总体的估计。

![在小数据上区分原始数据、中心、离散程度与样本估计的流程](/AiBook/assets/part-02/chapter-05/small-data-statistics-check-zh.svg)

## 执行环境

本节代码使用 NumPy。

笔记本代码单元与终端的区别参见[命令的执行位置](../chapter-03/section-05.zh.md#_2)。按从上到下的顺序运行代码块。

如果使用 Google Colab，可以先在代码单元里像下面这样准备 NumPy。

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

## 不低于 60 分的比例

`data >= 60` 检查每个分数是否不低于 60。`True` 表示满足条件，`False` 表示不满足条件。用 `np.count_nonzero` 统计为真的元素，可以得到 2，对应分数 63 和 70。

```python
at_least_60 = data >= 60
count_at_least_60 = np.count_nonzero(at_least_60)
observed_ratio = count_at_least_60 / data.size
print(at_least_60)
print(count_at_least_60)
print(observed_ratio)
```

```text
[False False False  True False False False  True]
2
0.25
```

观测到的 8 个分数中，不低于 60 分的比例为 `2 / 8 = 0.25`，即 25%。如果等概率地从这 8 个分数中选一个，不低于 60 分的概率就恰好是 0.25。对于更大的总体，这个比例只是相应概率的估计值，还要检查样本收集方式与代表性。

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

将原来的 8 个分数排序后，中间两个值是 50 和 52。中位数为 `(50 + 52) / 2 = 51`，与开头图示中的中位数一致。

```python
print(np.sort(data))
print(np.median(data))
```

```text
[42 47 48 50 52 55 63 70]
51.0
```

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

`方差(variance)` 是用来观察数值在均值周围离散程度了多少的数字。

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

`np.var(data)` 将观测值的平方偏差之和除以个数 `N`。即使数据来自样本，在描述这组数据本身的离散程度时，也可以使用这个计算。

用来估计总体方差的常见样本方差，则将同一个和除以 `N − 1`。在 NumPy 中指定 `ddof=1` 即可。对于从同一分布独立抽取的样本，这项修正可减小使用样本均值计算平方偏差时造成的方差低估偏差。

```python
print(np.var(data))
print(np.var(data, ddof=1))
```

```text
72.984375
83.41071428571429
```

两种计算使用相同的数据与平方偏差之和 `583.875`。第一个值是 `583.875 / 8`，第二个值是 `583.875 / 7`。数据没有改变，只是根据计算目的选择了不同分母。

| 计算目的 | 代码 | 分母 |
| --- | --- | --- |
| 描述观测数据本身的离散程度 | `np.var(data)` | `N = 8` |
| 用样本估计总体方差 | `np.var(data, ddof=1)` | `N − 1 = 7` |

`np.var` 的分母是 `N − ddof`。`ddof=1` 无法解决某些群体被遗漏或过度收集的问题。分母修正与检查样本收集方式是两回事。

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

更谨慎的说法会更接近：“在这组数据里，均值是 53.375”“这些值在均值周围有一定程度的离散程度”“这组数据能否代表整体，还要结合收集方式和样本构成一起看”。

AI 数据也需要同样的态度。训练数据的均值，是在训练数据集内部算出来的摘要值；测试数据的分数，是从测试样本上得到的评估值；而现实表现，则要通过另外的样本、部署后的观察、持续评估来确认。

## 改变极端值进行比较

把 `skewed_data` 的最后一个值从 `100` 改为 `1000`，再次打印均值与中位数。均值增大到 `(10 + 12 + 13 + 15 + 1000) / 5 = 210`，中位数仍为 `13`。

再把最后一个值改为 `14`。排序后为 `10, 12, 13, 14, 15`，均值为 `12.8`，中位数为 `13`。比较这两次输出，可看出一个大值把均值拉高了多少。

用 `copy()` 复制数组以保留原始数据，再只修改最后一个元素 `[-1]`。每行输出依次为修改后的值、均值和中位数。

```python
for last_value in [1000, 14]:
    changed_data = skewed_data.copy()
    changed_data[-1] = last_value
    print(last_value, np.mean(changed_data), np.median(changed_data))
```

```text
1000 210.0 13.0
14 12.8 13.0
```

## 检查清单

- 能区分观测比例与总体概率的估计值。
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

- NumPy Developers, [numpy.count_nonzero](https://numpy.org/doc/stable/reference/generated/numpy.count_nonzero.html){: target="_blank" rel="noopener noreferrer" }, NumPy Reference，确认日期：2026-09-15。用于核对布尔数组中满足条件的元素计数。
