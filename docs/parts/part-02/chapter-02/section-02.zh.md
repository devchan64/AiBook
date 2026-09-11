# P2-2.2 Sigma（Σ）与重复计算

> Section ID: `P2-2.2`
> Version: `v2026.09.08`

Sigma（Σ）是将多个值相加的计算压缩写出的记法。

\[
\sum
\]

Sigma 看起来可能陌生，但核心很简单。它表示：把多个值重复地相加。在 AI 文档里，当解释很多数据的总和、平均值（mean）、损失和（loss sum）、批次级（batch-level）计算时，它会经常出现。

## 重复范围与相加的项

| 标准 | 为什么重要 |
| --- | --- |
| Sigma 是在要求重复“同样形状的加法”的压缩记法 | 它让你把陌生符号重新读成计算结构。 |
| 索引是区分“当前加的是第几个对象”的名字 | 它让你不会丢掉重复位置。 |
| Sigma 在 AI 文档里常见，是因为许多数据会被聚合成总和、平均值和损失 | 它展示了为什么统计和损失聚合会共用同一种记法。 |

## Sigma 的组成

Sigma 记法同时写出重复范围和每次相加的项。

\[
\sum_{i=1}^{n}x_i
\]

这一行里包含了四个信息。

- 大符号 \(\sum\)：要求你相加
- 下方 \(i=1\)：从哪里开始重复
- 上方 \(n\)：重复到哪里结束
- 右边 \(x_i\)：每次要加什么

像这样拆开看之后，sigma 就不再像是突然出现的困难符号，而更像是一句把重复加法简短写下来的句子。

1. 从 `i = 1` 开始。
2. 重复到 `i = n` 为止。
3. 每一次都把 `x_i` 加进去。

所以，sigma 并不只是表示“和”这个结果的符号，它也是把“聚合什么、按什么顺序、在什么范围内聚合”一起写出来的记法。这个视角在回想代码里的循环时也很有用。

但这并不意味着 sigma 和代码循环完全相同。数学记法会把计算结构压缩展示，而代码会把它展开成真实执行步骤。

## 展开一个简单的 Sigma 式

读 sigma 最好的方式，就是把一个短式子直接展开。

\[
\sum_{i=1}^{3} i
\]

这个式子表示：当 `i` 从 1 变到 3 时，把 `i` 本身相加。

```text
当 i = 1 时加的值：1
当 i = 2 时加的值：2
当 i = 3 时加的值：3
```

所以它可以展开成下面这样。

\[
\sum_{i=1}^{3} i = 1 + 2 + 3 = 6
\]

如果看一种更接近 AI 文档的形式，会是下面这样。

\[
\sum_{i=1}^{3}x_i
\]

如果 \(x_1=2\)、\(x_2=4\)、\(x_3=6\)，就会算成这样。

\[
\sum_{i=1}^{3}x_i = x_1 + x_2 + x_3 = 2 + 4 + 6 = 12
\]

如果再继续算平均值，就会变成下面这样。

\[
\frac{1}{3}\sum_{i=1}^{3}x_i = \frac{1}{3}(2 + 4 + 6) = 4
\]

## 索引与循环

在 sigma 里，`i` 就是索引（index）。索引是告诉你“现在看到的是第几个对象”的名字。

\[
\sum_{i=1}^{n}x_i
\]

这里每个部分可以这样读。

- `i`：表示重复位置的索引
- `1`：起始位置
- `n`：结束位置
- `x_i`：第 `i` 个值
- `Σ`：告诉你去改变 `i` 并把值加起来的记号

在代码里，大致会像下面这样。

包含四个值的列表 `values`。 打印总和 `10`。

```python
# values 是要反复相加的值列表。
values = [1, 2, 3, 4]

# total 会随着循环经过这些值而累积总和。
total = 0

for value in values:
    total = total + value

print(total)
```

示例运行结果：

```text
10
```

公式中的 `i` 和代码中的 `value` 并不完全相同，但它们的连接点在于：二者都指向重复过程中当前正在处理的对象。

## 总和与平均值

平均值（mean）是理解 sigma 的很好例子。把所有值加起来，再除以个数，就得到平均值。

\[
\mathrm{mean} = \frac{x_1 + x_2 + x_3 + x_4}{4}
\]

如果写成 sigma，就会压缩成下面这样。

\[
\mathrm{mean} = \frac{1}{n}\sum_{i=1}^{n}x_i
\]

这个式子可以这样读。

1. 让 `i` 从 1 变到 `n`，把所有 `x_i` 加起来。
2. 再把这个和除以 `n`。

在代码里，可以写成下面这样。

包含四个值的列表 `values`。 打印平均值 `2.5`。

```python
# values 是要计算平均值的数据，mean 是它的概括值。
values = [1, 2, 3, 4]
mean = sum(values) / len(values)

print(mean)
```

示例运行结果：

```text
2.5
```

如果用 NumPy 数组，还可以更短。

包含四个值的 NumPy 数组 `values`。 打印平均值 `2.5`。

```python
import numpy as np

# values 是被转换成 NumPy 数组的重复计算对象。
values = np.array([1, 2, 3, 4])

# mean 把整个数组聚合成一个平均值。
mean = values.mean()

print(mean)
```

示例运行结果：

```text
2.5
```

这里的 `values.mean()` 会在内部执行平均值计算。它没有直接把 sigma 写出来，但“收集很多值并对其计算”的结构并没有变。

## 样本损失与平均损失

在机器学习中，损失（loss）会用数字表示模型输出和参考值之间的差距。如果只有一个数据点，那么只需要算一次损失。

\[
\mathrm{loss} = (\mathrm{prediction} - \mathrm{target})^2
\]

但在真实学习里，数据通常有很多个。对每个数据点，都有一个 prediction 和 target，对每个数据点，也都会产生一个 loss。

\[
\mathrm{loss}_1,\ \mathrm{loss}_2,\ \mathrm{loss}_3,\ \cdots,\ \mathrm{loss}_n
\]

如果把整个损失简单相加，就会变成下面这样。

\[
\mathrm{total\_loss} = \mathrm{loss}_1 + \mathrm{loss}_2 + \cdots + \mathrm{loss}_n
\]

写成 sigma 就变成下面这样。

\[
\mathrm{total\_loss} = \sum_{i=1}^{n}\mathrm{loss}_i
\]

平均损失（mean loss）就是再把这个和除以数据个数。

\[
\mathrm{mean\_loss} = \frac{1}{n}\sum_{i=1}^{n}\mathrm{loss}_i
\]

在代码里可以这样看。

预测列表 `predictions` 和答案列表 `targets`。 打印样本损失的平均值。

```python
# predictions 和 targets 是按样本配对比较的预测值与真实值列表。
predictions = [2.8, 4.1, 5.0]
targets = [3.0, 4.0, 4.5]

# losses 会按顺序收集每个样本的平方误差。
losses = []
for prediction, target in zip(predictions, targets):
    loss = (prediction - target) ** 2
    losses.append(loss)

# mean_loss 把多个样本的损失概括成一个平均损失。
mean_loss = sum(losses) / len(losses)
print(mean_loss)
```

示例运行结果：

```text
0.09999999999999999
```

这个例子把真实深度学习训练代码简化了。关键在于：因为数据很多，所以同一个计算会被重复，而重复的结果会被求和或求平均。

## 批次损失聚合

在深度学习里，通常不是一条一条地处理数据，而是按一个批次（batch）去处理很多数据。一个 batch 里有许多样本（sample），模型会对每个样本生成一个输出。这里，`batch` 是很多输入的组合，`prediction` 是对每个输入产生的模型输出，`loss` 是每个输出和参考值之间的差距，`mean_loss` 则是这个 batch 中所有损失的平均值。

即使在这里，sigma 的视角也不会变。你仍然是在看 batch 里的每个样本，分别算出每个样本的损失，然后把这些损失求和或求平均。

## 循环与数组运算

前面三个样本的平方误差分别约为 `0.04`、`0.01`、`0.25`，平均值为 `(0.04 + 0.01 + 0.25) / 3 = 0.1`。NumPy 在数组的每个位置执行减法和平方，再用 `mean()` 求平均。

输入是预测数组 `predictions` 和答案数组 `targets`，输出是平均损失。

```python
import numpy as np

# predictions 和 targets 是用于一次性比较的预测值与真实值数组。
predictions = np.array([2.8, 4.1, 5.0])
targets = np.array([3.0, 4.0, 4.5])

# losses 是逐样本平方误差数组，mean_loss 是它的平均值。
losses = (predictions - targets) ** 2
mean_loss = losses.mean()

print(mean_loss)
```

示例运行结果：

```text
0.09999999999999999
```

循环虽然不可见，但重复计算并没有消失。数组计算只是把表达方式改成了“一次处理很多值”。

## 检查清单

- 你能把 sigma 解释为“压缩重复加法的记法”吗？
- 你能区分索引、起始位置、结束位置和被加的项吗？
- 你能用 sigma 和代码两种方式解释平均值吗？
- 你能说明对很多数据的损失进行求和或求平均的流程吗？
- 你能说明循环和数组计算都能与 sigma 记法对应吗？
- 当 sigma 出现时，你能用“到底在加什么、加多少次？”去把它展开吗？
- 你能说明为什么 sigma 会帮助之后阅读统计、损失计算、批次计算和优化吗？
- 你能把一个简单的 sigma 式按项展开并算出总和或平均值吗？
- 你能用 sigma 和代码把平均值、损失、批次计算连接成同一种聚合结构吗？

## 来源与参考资料

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2020, 确认日期：2026-07-19.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, 确认日期：2026-07-19.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, 确认日期：2026-07-19.
- NumPy Developers, [numpy.sum](https://numpy.org/doc/stable/reference/generated/numpy.sum.html){: target="_blank" rel="noopener noreferrer" }, NumPy User Guide, 确认日期：2026-07-19. 这个官方参考资料说明了数组元素求和与按轴求和。
- NumPy Developers, [numpy.mean](https://numpy.org/doc/stable/reference/generated/numpy.mean.html){: target="_blank" rel="noopener noreferrer" }, NumPy User Guide, 确认日期：2026-07-19. 这个官方参考资料支持平均值计算和 `mean()` 示例。
