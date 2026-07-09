# P2-2.2 sigma(sigma)与重复计算

> Section ID: `P2-2.2`
> Version: `v2026.07.09`

P2-2.1 重新阅读了变量、函数与表达式。现在要看的，是公式里最常见的重复计算记号之一：

\[
\sum
\]

sigma 看起来可能陌生，但核心意思很简单：把重复出现的项不断加起来。AI 文档里，只要出现“很多数据的和”“平均值”“损失聚合”“batch 级计算”，它就很容易登场。

## 本节范围

这里首先要解决的问题是：当一行公式里出现 sigma 时，怎样立刻看出“加的是什么、加了多少次”？

所以这里只先固定四个位置。

- sigma 让你重复相加的到底是什么？
- index 怎样标出重复位置？
- 为什么平均值与损失计算里这么常见 sigma？
- sigma 记号怎样在代码里变成循环与数组计算？

## 三个基准

| 基准 | 为什么重要 | 本节所需理解水平 |
| --- | --- | --- |
| sigma 是重复加法的压缩记号 | 能把陌生符号重新读成计算结构 | 理解看到 sigma 时，先问“加什么、加多少次” |
| index 标出当前正在加哪一项 | 能帮助你追踪重复位置 | 理解下标和重复位置的连接 |
| sigma 在 AI 里常见，是因为平均值与损失都要对多个数据做汇总 | 能看懂统计与损失聚合为什么共用一种记号 | 理解两者都是“重复再汇总”的结构 |

## sigma 把重复加法压缩起来

假设有下面几个值：

\[
x_1 = 1,\quad x_2 = 2,\quad x_3 = 3,\quad x_4 = 4
\]

直接写开来就是：

\[
x_1 + x_2 + x_3 + x_4
\]

用 sigma 写，则会压缩成：

\[
\sum_{i=1}^{4}x_i
\]

读法是：

1. 让 `i` 从 1 走到 4。
2. 每次取出 `x_i`。
3. 把它们全部加起来。

## index 标出重复位置

在 sigma 里，`i` 就是 index，它告诉你“现在在看第几个位置”。

\[
\sum_{i=1}^{n}x_i
\]

代码里，类似的结构会像这样出现：

```python
values = [1, 2, 3, 4]
total = 0

for value in values:
    total = total + value

print(total)
```

示例输出：

```text
10
```

## 平均值就是先求和再除以个数

\[
\mathrm{mean} = \frac{1}{n}\sum_{i=1}^{n}x_i
\]

代码里可以写成：

```python
values = [1, 2, 3, 4]
mean = sum(values) / len(values)

print(mean)
```

示例输出：

```text
2.5
```

如果用 NumPy 数组，还可以写得更短：

```python
import numpy as np

values = np.array([1, 2, 3, 4])
mean = values.mean()

print(mean)
```

示例输出：

```text
2.5
```

## 损失也会对多个数据重复计算

单个样本的损失可以写成：

\[
\mathrm{loss} = (\mathrm{prediction} - \mathrm{target})^2
\]

但真实学习里有很多样本，所以同一个计算会重复很多次：

\[
\mathrm{total\_loss} = \sum_{i=1}^{n}\mathrm{loss}_i
\]

\[
\mathrm{mean\_loss} = \frac{1}{n}\sum_{i=1}^{n}\mathrm{loss}_i
\]

代码里可以这样看：

```python
predictions = [2.8, 4.1, 5.0]
targets = [3.0, 4.0, 4.5]

losses = []
for prediction, target in zip(predictions, targets):
    loss = (prediction - target) ** 2
    losses.append(loss)

mean_loss = sum(losses) / len(losses)
print(mean_loss)
```

示例输出：

```text
0.09999999999999998
```

## 本节要记住的视角

sigma 是把重复加法写短的记号。index 标出现在正在读哪一项。平均值与损失聚合都常用 sigma，因为它们本质上都在做“重复计算后再汇总”。

## 简短检查

- 能把 sigma 读成重复加法。
- 能指出被重复的项、起点、终点与 index。
- 能从 sigma 和记代码两边解释平均值。
- 能说明为什么学习时要对多个损失求和或求平均。

## 来源与参考资料

本节整理的是 Part 2 中重新阅读重复计算所需的记号，没有直接引用外部资料。
