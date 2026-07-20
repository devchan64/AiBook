# P2-2.2 Sigma（Σ）与重复计算

> Section ID: `P2-2.2`
> Version: `v2026.07.20`

在 P2-2.1，我们重新阅读了变量（variable）、函数（function）和表达式（expression）。现在，我们来看一种在公式里非常常见的重复计算记法。

\[
\sum
\]

Sigma 看起来可能陌生，但核心很简单。它表示：把多个值重复地相加。在 AI 文档里，当解释很多数据的总和、平均值（mean）、损失和（loss sum）、批次级（batch-level）计算时，它会经常出现。

这里要展示的是：sigma 是一种 `把重复加法压缩起来的记法`，并说明它怎样连接到代码中的循环（loop）、数组计算（array computation）和平均损失计算。

这里会重新整理 `sigma`、`索引（index）`、`平均值（mean）`、`重复计算（repeated computation）`、`损失聚合（loss aggregation）`。如果 2.1 读的是变量、函数、表达式的最小语法，那么这一节整理的就是：当这种语法要对很多数据重复时，会变成怎样的压缩记法。

一旦理解了 sigma，后面的很多内容就会更容易读。尤其是 `当数据很多时，同一个计算会被反复执行，然后结果再被聚合起来` 这个结构会开始变得明显。

- 更容易读统计记法，例如平均值、方差、标准差这类把很多值总结起来的公式。
- 更容易理解为什么损失（loss）和平均损失（mean loss）都是对很多数据一起计算的。
- 更容易跟上向量、矩阵和 batch 计算里“许多分量或样本一起处理”的流程。
- 学梯度（gradient）和优化（optimization）时，更容易接受“很多项的影响会被合在一起”这种解释。
- 能为之后把 Python 循环（loop）、NumPy 数组计算（array computation）、深度学习框架中的张量运算（tensor operation）读成“同一个重复结构的不同表达”做好准备。

## 本节目标

- 能把 sigma 读成重复加法的压缩记法。
- 能区分索引、起始值、结束值和要相加的项。
- 能从 sigma 和代码两个角度解释平均值。
- 能直观读懂对很多数据的损失进行求和或求平均的流程。
- 当 sigma 出现时，能先问“在加什么、加多少次？”
- 能把 sigma 记法拆成上面、下面和右侧的项来读。
- 能说明为什么 sigma 之后会继续连接到统计、损失计算、批次计算和优化。
- 能把一个简单的 sigma 式展开并算出真实总和。

## 三个判断标准

阅读正文时起标准作用的三个视角如下。

| 标准 | 为什么重要 | 本节需要达到的理解程度 |
| --- | --- | --- |
| Sigma 是在要求重复“同样形状的加法”的压缩记法 | 它让你把陌生符号重新读成计算结构。 | 理解看到 sigma 时，要问“在加什么、加多少次”。 |
| 索引是区分“当前加的是第几个对象”的名字 | 它让你不会丢掉重复位置。 | 理解要把下标和重复索引连起来读。 |
| Sigma 在 AI 文档里常见，是因为许多数据会被聚合成总和、平均值和损失 | 它展示了为什么统计和损失聚合会共用同一种记法。 | 理解平均值和损失聚合都属于重复加法结构。 |

## 从数学教育视角读取 Sigma

在数学教育中，sigma 往往被介绍为“求和符号”。但第一次重新阅读时，比起停留在“它是求和符号”的定义，更有帮助的是把这个记法里的角色拆开来看。

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

但这并不意味着 sigma 和代码循环完全相同。数学记法会把计算结构压缩展示，而代码会把它展开成真实执行步骤。这里的连接只是：二者在用不同方式展示同一个重复结构。

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

即使只会做到这个程度，也已经足够让你准备去读 AI 文档中像平均损失（mean loss）、批次损失（batch loss）、全数据总和这类记法。重要的不是背公式，而是形成这样的习惯：看到 sigma，先把它展开再算。

## Sigma 会把重复加法缩短写下

假设存在下面这些数据。

\[
x_1 = 1,\quad x_2 = 2,\quad x_3 = 3,\quad x_4 = 4
\]

如果直接把它们全部相加，就是下面这样。

\[
x_1 + x_2 + x_3 + x_4
\]

Sigma 会把这种重复更简短地写出来。

\[
\sum_{i=1}^{4}x_i
\]

这行可以这样读。

1. 让 `i` 从 1 变到 4。
2. 一个一个地取出 `x_i`。
3. 把它们全部加起来。

也就是说，它和下面这个计算是一样的。

\[
x_1 + x_2 + x_3 + x_4
\]

看到 sigma 时，第一眼不要只看符号长相，而要先看重复结构。先看：加什么、从哪里开始、在哪里结束、用哪个名字表示重复位置。

## 索引会标记重复位置

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

问题情境：把 sigma 的重复加法结构翻译成代码循环。
输入（input）：包含四个值的列表 `values`。
期望输出（output）：打印总和 `10`。
要确认的概念：sigma 记法中的重复结构，在代码里会表现成循环和累积总和。

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

## 平均值就是总和除以个数

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

问题情境：不只从 sigma 记法，而是通过代码的 `sum` 和 `len` 来计算平均值公式。
输入（input）：包含四个值的列表 `values`。
期望输出（output）：打印平均值 `2.5`。
要确认的概念：平均值属于一种重复结构：先把很多值加起来，再除以个数。

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

问题情境：用 NumPy 数组方法把同一个平均值计算写得更短。
输入（input）：包含四个值的 NumPy 数组 `values`。
期望输出（output）：打印平均值 `2.5`。
要确认的概念：即使不直接写 sigma，同样的重复结构依然藏在数组计算里。

```python
# 这个例子用 NumPy 数组计算检查 sigma 形式的重复求和和平均损失。
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

## 损失也会在很多数据上重复

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

问题情境：对很多数据点重复计算损失，再求平均损失。
输入（input）：预测列表 `predictions` 和答案列表 `targets`。
期望输出（output）：打印样本损失的平均值。
要确认的概念：损失也有“对很多数据反复做同一个计算，再对结果求平均”的结构。

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
0.09999999999999998
```

这个例子把真实深度学习训练代码简化了。关键在于：因为数据很多，所以同一个计算会被重复，而重复的结果会被求和或求平均。

## 批次计算也用同样的视角来读

在深度学习里，通常不是一条一条地处理数据，而是按一个批次（batch）去处理很多数据。一个 batch 里有许多样本（sample），模型会对每个样本生成一个输出。这里，`batch` 是很多输入的组合，`prediction` 是对每个输入产生的模型输出，`loss` 是每个输出和参考值之间的差距，`mean_loss` 则是这个 batch 中所有损失的平均值。

即使在这里，sigma 的视角也不会变。你仍然是在看 batch 里的每个样本，分别算出每个样本的损失，然后把这些损失求和或求平均。

## 用案例来看

### 案例 1. 为什么批次损失必须读成很多个样本的和，而不是单个样本

当一个学习者看到模型损失（loss）公式时，可能会想：“为什么这里还要加 sigma？” 如果只看一个样本的预测误差，它看起来很简单。但真实学习通常是一次看很多个数据，并把它们的损失汇总后再判断。

例如，如果四张图片被作为一个 batch 输入，那么每张图片都会各自产生一个损失。此时，sigma 压缩展示的是这样一种重复结构：`分别计算四张图片的损失，再把它们全部加起来`。而平均损失就是再把这个和除以数据个数。

这个案例揭示了 sigma 绝不是单纯的数学装饰。在几乎所有“把很多值一起总结起来”的场景中，例如平均值、方差、总损失和 batch 损失，sigma 都在负责 `重复同一个计算，并把结果聚合起来` 这个结构。

所以，当你看到 sigma 时，第一件事就是问：`到底在加什么、加多少次？` 只要抓住这个问题，复杂的损失公式和统计公式就会少很多陌生感。

库代码可能会把这种重复藏起来。

问题情境：用 NumPy 数组运算一次性表达前面的重复损失计算。
输入（input）：预测数组 `predictions` 和目标数组 `targets`。
期望输出（output）：打印平均损失值。
要确认的概念：即使看不到循环，同样的重复结构仍然是在数组计算内部执行的。

```python
# 这个例子用 NumPy 数组计算检查 sigma 形式的重复求和和平均损失。
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
0.09999999999999998
```

循环虽然不可见，但重复计算并没有消失。数组计算只是把表达方式改成了“一次处理很多值”。

## 阅读 Sigma 的顺序

当 sigma 出现时，可以按下面的顺序来读。

1. 被加的对象是什么？
2. 重复索引是什么？
3. 起点和终点在哪里？
4. 结果是总和，还是平均值？
5. 在代码里，它表现成循环还是数组计算？

例如，看下面这个式子。

\[
\frac{1}{n}\sum_{i=1}^{n}(\mathrm{prediction}_i - \mathrm{target}_i)^2
\]

这个式子可以读成：先对第 `i` 个 prediction 和第 `i` 个 target 求差，再把这个差平方，再让 `i` 从 1 变到 `n` 并全部加起来，最后除以 `n` 得到平均值。

这会继续通向平均平方误差（mean squared error, MSE）的直觉。但 MSE 本身可以在评价指标和损失函数那里的章节再处理。这里先只记住 sigma 会压缩重复计算。

## 为什么 Sigma 会让人觉得难

Sigma 之所以显得难，并不是因为“加法”本身难，而是因为“重复变量、重复范围、要加的项、总和、是否还要求平均”这些压缩信息都被塞在了一处。

当这么多信息同时出现在一行里时，它当然会显得陌生。但如果你把它展开成代码，它通常不过是一个循环或者一个数组计算。

Sigma 记法在代码里可以展开成循环、数组运算，以及最后的总和或平均值计算。

所以，与其背 sigma，不如先练习把它展开。

## 检查清单

- 你能把 sigma 解释为“压缩重复加法的记法”吗？
- 你能区分索引、起始位置、结束位置和被加的项吗？
- 你能用 sigma 和记码两种方式解释平均值吗？
- 你能说明对很多数据的损失进行求和或求平均的流程吗？
- 你能说明循环和数组计算都能与 sigma 记法对应吗？
- 当 sigma 出现时，你能用“到底在加什么、加多少次？”去把它展开吗？
- 你能说明为什么 sigma 会帮助之后阅读统计、损失计算、批次计算和优化吗？
- 你能把一个简单的 sigma 式按项展开并算出总和或平均值吗？
- 你能把 sigma 解释成“阅读重复与聚合的第一路标”，而不只是一个要背的符号吗？
- 你能用 sigma 和代码把平均值、损失、批次计算连接成同一种聚合结构吗？

## 来源与参考资料

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2020, 确认日期：2026-07-19.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, 确认日期：2026-07-19.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, 确认日期：2026-07-19.
- NumPy Developers, [numpy.sum](https://numpy.org/doc/stable/reference/generated/numpy.sum.html){: target="_blank" rel="noopener noreferrer" }, NumPy User Guide, 确认日期：2026-07-19. 这个官方参考资料说明了数组元素求和与按轴求和。
- NumPy Developers, [numpy.mean](https://numpy.org/doc/stable/reference/generated/numpy.mean.html){: target="_blank" rel="noopener noreferrer" }, NumPy User Guide, 确认日期：2026-07-19. 这个官方参考资料支持平均值计算和 `mean()` 示例。
