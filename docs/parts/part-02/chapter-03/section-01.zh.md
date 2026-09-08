# P2-3.1 标量(scalar)、向量(vector)、矩阵(matrix)

> Section ID: `P2-3.1`
> Version: `v2026.09.08`

AI 数据可以表示成一个数字、一组值的列表，或带有行列的表，分别对应标量、向量和矩阵。

## 数字、列表与表

| 基准 | 为什么重要 |
| --- | --- |
| 标量就是一个数字 | 因为它是读取损失、概率、学习率这类单个值的基本单位。 |
| 向量是有顺序的值列表 | 因为这是用多个特征表示一个对象时最常见的形状。 |
| 矩阵是把多个向量放在一起的表 | 因为同时计算多个样本和多个特征时，需要行列结构。 |

## 数据的数值表示

AI 模型不会直接拿现实里的句子、图像、声音、表格来计算。多数情况下，它们会先被变成数字，再以数组(array)的形式处理。

1. 句子会通过 token 变成数字 ID 和向量。
2. 图像会变成保存像素值的数组。
3. 表格数据会被读成带行列结构的矩阵或 dataframe。

可以用下面的问题区分数值数组的形状。

1. 是不是只有一个值？
2. 这些值是不是排成一行？
3. 这些值是不是排成了行和列？
4. 是不是有多份数据被一起打包了？

这些问题在实际代码里也同样重要。AI 代码出错的常见原因之一，不是误解了值的意义，而是误解了它的 shape。

## 标量：一个数字

标量(scalar)就是一个数字。比如下面这些值都可以看成标量。

\[
3
\]

\[
0.8
\]

\[
-1.2
\]

在 AI 语境里，标量会出现在很多地方。

- 一个温度值
- 一个概率(probability)
- 一个损失(loss)
- 一个准确率(accuracy)
- 一个学习率(learning rate)

例如，如果某个模型的平均损失是 0.25，那么这个值本身就是标量。

\[
\mathrm{loss} = 0.25
\]

标量看起来很小，但它非常重要。评估模型时，我们经常会把很多计算结果压缩成一个数字。不过一个数字也会压缩掉很多信息。只知道损失是 0.25，并不能告诉我们模型在哪些数据上做得好、在哪些数据上做错了。

## 逐位置相加与标量乘法

标量、向量、矩阵的差异不只是形状不同。从数学上看，真正变化的是 `可以做什么计算`。

因为标量是一个数字，所以我们可以立刻想到普通四则运算。

\[
2 + 3 = 5
\]

\[
2 \times 3 = 6
\]

向量可以把相同位置上的值相加。

\[
[1,\ 2,\ 3] + [4,\ 5,\ 6] = [5,\ 7,\ 9]
\]

如果标量乘到向量上，就是把同一个数字乘到向量的每个值上。

\[
2[1,\ 2,\ 3] = [2,\ 4,\ 6]
\]

矩阵在 shape 相同的时候，也可以逐位置相加。

\[
\begin{bmatrix}
1 & 2 \\
3 & 4
\end{bmatrix}
+
\begin{bmatrix}
5 & 6 \\
7 & 8
\end{bmatrix}
=
\begin{bmatrix}
6 & 8 \\
10 & 12
\end{bmatrix}
\]

这些计算与其说是复杂的线性代数，不如说更接近 `相同位置上的值进行计算` 这条规则。也正因为这样，shape 才会变得重要。长度不同的向量，或者行列数量不同的矩阵，不能直接逐位置计算。

1. shape 相同，就可以逐位置计算。
2. shape 不同，就必须先决定哪些值应该配对。

## 向量：有顺序的值

向量(vector)可以读成有顺序的值列表。

\[
\mathbf{x} = [1,\ 2,\ 3]
\]

这里的 \(\mathbf{x}\) 是一个包含 3 个值的向量。

例如，假设我们用三个值来表示一个人：`年龄: 30`、`身高: 172`、`每月访问次数: 5`。

写成向量，就会像这样。

\[
\mathbf{x} = [30,\ 172,\ 5]
\]

这个向量把一个人的特征(feature)表示成了数字列表。机器学习里，经常会把多个特征这样收集起来，当成一个输入(input)。

向量里的顺序很重要。必须先固定第一个值表示年龄、身高、还是访问次数。

```text
[30, 172, 5]
-> [年龄, 身高, 每月访问次数]
```

如果顺序改变，即使数字一样，意义也会变。

```text
[172, 30, 5]
-> [身高, 年龄, 每月访问次数]
```

所以，向量不是随便堆在一起的一堆数字，而是每个位置都带有意义的一组数字。

## 矩阵：行与列

矩阵(matrix)是把数字排成行(row)和列(column)的结构。

\[
X =
\begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & 6
\end{bmatrix}
\]

这个矩阵有 2 行 3 列。通常会把它叫作一个 \(2 \times 3\) 矩阵。这里，行(row)是横向的一整行，列(column)是纵向的一整列，而 shape 指的就是行数和列数。

在 AI 数据里，一行通常可以读成一个数据样本(sample)，一列可以读成一个特征(feature)。

例如，如果把 3 个人的数据用年龄、身高、访问次数来表示，就会得到下面这个矩阵。

\[
X =
\begin{bmatrix}
30 & 172 & 5 \\
24 & 165 & 2 \\
41 & 180 & 7
\end{bmatrix}
\]

在这里，有 3 行 3 列。也就是说，3 行代表 3 个人，3 列代表年龄、身高、每月访问次数。

这个视角在阅读机器学习数据集(dataset)时非常重要。在很多入门材料里，\(X\) 表示完整输入数据，\(y\) 表示与每一行对应的目标值(target)或标签(label)。

## shape 与计算条件

shape 就是数据的形状。它告诉我们，当前看到的是一个值、一个值列表，还是带行和列的数组。

用 NumPy 创建一个数字、三个值和一个 2 行 3 列的数组，并输出它们的 `shape`。

```python
import numpy as np

# scalar、vector、matrix 是用来比较数据存放形状的三个数组。
scalar = np.array(3)
vector = np.array([1, 2, 3])
matrix = np.array([[1, 2, 3], [4, 5, 6]])

# shape 表示每个轴的长度。
print(scalar.shape)
print(vector.shape)
print(matrix.shape)
```

这段代码在检查三个值的形状。结果可以读成：标量 `()`、向量 `(3,)`、矩阵 `(2, 3)`。

根据库或设置不同，标量的显示方式可能会略有差别，但核心不变。标量就是一个数字，向量是数字列表，矩阵是带行和列的数字数组。

shape 之所以重要，是因为能不能计算会随着 shape 改变。例如，长度不同的向量很难逐位置相加。

\[
[1,\ 2,\ 3] + [4,\ 5]
\]

这个式子无法对齐到底哪些值应该相加。在代码里也是一样，如果 shape 对不上，就可能报错，或者以并非你原本打算的方式继续计算。

## 行与列的意义

矩阵是数字数组，但这些数字的意义由问题定义来决定。即使是同一个 \(3 \times 3\) 矩阵，在表格数据里，行可以表示人、列可以表示特征；在图像的一部分里，行和列可以表示像素位置；在句子数据里，行可以表示 token、列可以表示 embedding 维度；在 batch 数据里，行可以表示样本、列可以表示特征。

因此，阅读矩阵时不能只看数字的形状，还要检查：这一行表示什么，这一列表示什么，每个值的单位是什么，行和列的顺序是不是固定的。

当你在 AI 文档里看到 `输入矩阵`、`特征矩阵`、`嵌入矩阵` 这类表达时，第一步应该先确认行和列的意义。

## AI 计算中的数据形状

在 AI 计算中，相同的数组形状也会承担不同的作用。

- embedding：把文本或条目表示成向量
- feature：把一个数据样本表示成由多个值组成的向量
- batch：把多个样本打包成矩阵或更高维数组
- loss：把多个计算结果汇总成一个标量
- model parameter：权重(weight)可以呈现为向量或矩阵
- matrix multiplication：它会成为同时计算多个输入与权重的基本工具

## 学生数与特征数

假设我们有下面这组数据。

\[
X =
\begin{bmatrix}
2 & 8 \\
4 & 6 \\
5 & 9
\end{bmatrix}
\]

假设在这个矩阵里，行(row)表示学生，列(column)表示 `[学习时间, 测验分数]`。

那么这个矩阵表示：第一个学生的学习时间是 2、测验分数是 8；第二个学生的学习时间是 4、测验分数是 6；第三个学生的学习时间是 5、测验分数是 9。

这里，一个学生的数据就是一个向量。

\[
\mathbf{x}_1 = [2,\ 8]
\]

如果把三个学生的数据收集在一起，它就成为一个矩阵。

\[
X =
\begin{bmatrix}
\mathbf{x}_1 \\
\mathbf{x}_2 \\
\mathbf{x}_3
\end{bmatrix}
\]

这个矩阵的 shape 是 `(3, 2)`：共有 3 名学生，每人有学习时间和测验分数两个特征。第二名学生的测验分数是第 2 行第 2 列的 `6`。增加一名学生后，shape 变为 `(4, 2)`；增加一个特征后，变为 `(3, 3)`。

## 检查清单

- 能把标量(scalar)解释成一个数字吗？
- 能把向量(vector)解释成有顺序的值列表吗？
- 能把矩阵(matrix)解释成带有行(row)和列(column)的数字数组吗？
- 能说明 shape 会影响计算是否可行、是否会出错吗？
- 能说明行和列的意义会随着问题定义而改变吗？
- 能把一个样本(sample)读成向量，把多个样本读成矩阵吗？
- 能说明为什么标量、向量、矩阵会在 embedding、feature、batch、loss、parameter 里再次出现吗？
- 能说明 shape 相同的向量和矩阵可以逐位置相加，而标量乘法是把同一个数字乘到每个值上吗？
- 当 `X` 的 shape、样本数、特征数混在一起时，能用 shape 直觉重新把它们分开吗？

## 来源与参考资料

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2020, 确认日期: 2026-07-19.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, 确认日期: 2026-07-19.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, 确认日期: 2026-07-19.
- NumPy Developers, [numpy.ndarray.shape](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.shape.html){: target="_blank" rel="noopener noreferrer" }, NumPy User Guide, 确认日期：2026-07-19. 这个官方参考资料支持把 `shape` 读成数组维度信息，并在代码中检查它。
- scikit-learn developers, [Glossary of Common Terms and API Elements](https://scikit-learn.org/stable/glossary.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn User Guide, 确认日期：2026-07-19. 这是确认把 `X` 读作输入数据矩阵、把 `y` 读作 target 这一惯例的参考资料。
