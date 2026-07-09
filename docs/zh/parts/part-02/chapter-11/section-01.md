# P2-11.1 用 NumPy 数组构建向量与矩阵

> Section ID: `P2-11.1`
> Version: `v2026.07.09`

在 Part 2 Chapter 3 中，我们用数学符号和小段代码确认了 scalar、vector、matrix。Part 2 Chapter 8 看过 Python 的 list 与 dictionary，Part 2 Chapter 9 从不同数据结构视角区分了 array、table、tree、graph，Part 2 Chapter 10 又说明了如何把 notebook 整理成可重新执行的学习记录。

现在我们重新回到 NumPy。NumPy 这个名字来自 "Numerical Python"。它是 Python 里广泛使用的开源库，用来创建数值数组，并以快速且一致的语法执行向量与矩阵计算。

本节说明 `NumPy`、`shape`、`ndim`、`dtype` 的基本区分。这一章的重点不是背很多 NumPy 语法，而是学会在 AI 实践里把 vector、matrix、数据成组的形状读出来。以后再次遇到 array、axis、broadcasting 时，也可以把 [概念词汇表](../../../reference/concept-glossary.md) 当作回返点。

学习 AI 时，数据很快就会变成数值数组。句子会变成 token ID 的数组，图像会变成 pixel 数组，表格数据会变成 feature matrix，embedding 会变成 vector。你当然也可以只用 Python list 处理这些数值集合，但当你需要对许多值按同一种方式加、乘、求平均、做矩阵乘法时，NumPy 数组会自然得多。

如果前面的 Python 语法与数据结构章节更关注“把什么值用什么句式写出来”，这一章则转向“怎样把这些值读成真正可用于计算的向量与矩阵形状”。接下来的章节会把问题继续推进到：把这些数字形状读成表、用图看它们、最后再把结果留下成记录。

| 现在这节要先抓住什么 | 紧接着会连到什么问题 | 之后会再次出现在哪里 |
| --- | --- | --- |
| NumPy 是制造“可计算数值形状”的工具 | 它会连到 Part 2 Chapter 12：这些数组该怎样被读成有行有列的表 | 之后所有机器学习输入矩阵、embedding、预测计算都会反复出现 |
| `shape`、`ndim`、`dtype` 必须先看 | 它会连到 P2-11.2 和 Part 2 Chapter 12：避免把 axis 和表结构混淆 | 之后在预处理、模型输入检查、错误诊断里都持续重要 |
| NumPy 是 `计算 -> 表 -> 图 -> 记录` 流程的第一步 | 它会连到 Part 2 Chapter 13 和 14：该看什么、该留下什么记录 | Part 3 之后的实验解读与结果复现都会从这里出发 |

| 术语 | 本节先抓住的含义 |
| --- | --- |
| NumPy | Python 中处理数值数组与向量、矩阵计算的代表性库 |
| `shape` | 显示数组有几个维度、每个 axis 多长的形状信息 |
| `ndim` | 数组的维度数 |
| `dtype` | 数组里数字的数据类型 |
| `ndarray` | NumPy 默认使用的多维数组数据结构 |

## 本节范围

本节讲如何创建 NumPy array，以及如何查看 shape、维度数 `ndim`、数据类型 `dtype`。范围还会延伸到构建向量、矩阵，以及计算一个小型 weighted sum 的例子。

这里回答以下问题。

- 为什么 Python list 和 NumPy array 会被不同地使用？
- 怎样用 NumPy array 构建 vector 与 matrix？
- `shape`、`ndim`、`dtype` 会告诉我们什么？
- 为什么在构建 vector 和 matrix 时，要先看数字的形状？
- 为什么在 AI 实践里，输入数据和权重会以数组形式出现？

本节不展开 broadcasting、advanced indexing、性能优化、内存布局、GPU 计算、线性代数算法的内部实现。axis 与 slicing 会在 P2-11.2 进一步讲，advanced indexing 与 shape 变化会在 P2-11.4 的补充学习里再整理。

## 本节目标

- 能把 NumPy array 与 Python list 区分开来说明。
- 能把一维数组读成 vector，把二维数组读成 matrix。
- 能通过 `.shape`、`.ndim`、`.dtype` 说明数组的形状与性质。
- 能说明即使是同一组数字，list 与 array 在计算里的用法也不同。
- 能读懂“输入矩阵乘以权重向量，生成一个小预测分数”的流程。

## 三个标准

| 标准 | 为什么重要 | 本节需要达到的理解程度 |
| --- | --- | --- |
| NumPy array 到底是什么 | 它能让你把 NumPy 读成“可计算数值形状的结构”，而不只是新语法 | 理解为把数字按固定形状放好以便计算的结构 |
| 为什么要和 list 分开看 | 它能清楚区分“存储结构”与“计算结构” | 理解两者都能装值，但 array 更直接面向数值计算 |
| 应该先检查什么 | 它为后面理解 indexing 与 broadcasting 建立起点 | 理解在看值之前，应先看 `shape` 与维度 |

## NumPy 是为数值数组计算准备的工具

NumPy 官方文档把 NumPy 介绍为科学与工程领域广泛使用的开源 Python 库，也说明它提供了多维数组数据结构 `ndarray`，以及能在该数组上高效运行的函数。

这里先把 NumPy 数组理解成 `把数字放在固定 shape 中用于计算的集合`。

Python list 当然也可以把值放在一起。

问题场景：在使用 NumPy 之前，先确认数值集合本来也能保存在 Python list 中。
输入(input)：一个包含三个分数的 Python list。
期待输出(output)：没有打印输出，但它展示了数字集合最简单的形态。
要确认的概念：看到 list 是通用的值容器，还不是面向计算的数组。

```python
scores = [82, 75, 45]
```

但 list 是通用的值集合。它可以只放数字，也可以混合字符串和对象。NumPy 文档同样把 Python list 视为优秀的通用容器，同时说明：当数据类型一致、数量较大、且要执行共同计算时，NumPy 更合适。

相比之下，NumPy 数组更接近一种“把同类数字放进固定形状里并用来计算”的结构。

问题场景：把同一组数字转成 NumPy array，确认它作为计算结构时是什么样子。
输入(input)：一个包含三个分数的一维数组。
期待输出(output)：没有打印输出，但准备好了通过 `np.array(...)` 创建的计算型数组。
要确认的概念：看到 NumPy array 是为了用一致形状处理同类数字的结构。

```python
import numpy as np

scores = np.array([82, 75, 45])
```

这个差别在 AI 实践里很重要。model input、feature、weight、embedding、image pixel，通常都是作为数值数组来计算的。

## 为什么在 AI 学习里先遇到 NumPy

你并不需要从一开始就手写实现 AI 模型的所有内部计算。真实的深度学习工作流可能会用到 PyTorch、TensorFlow、JAX 等工具。但这些工具同样建立在“数值数组、shape、axis、矩阵乘法、按位置运算”的直觉之上。

我们先看 NumPy，原因如下。

| 原因 | 学习中得到什么 |
| --- | --- |
| 可以直接看到 array 的 shape | 可以用 `shape` 检查输入与输出结构 |
| 可以小规模重现 vector 和 matrix 计算 | 能看到公式如何在代码中运行 |
| 可以比较 Python list 与面向计算的 array | 能区分数据结构与计算结构 |
| 机器学习例子经常使用 NumPy array | 读官方示例和教程会更轻松 |
| 能和 pandas、scikit-learn、可视化工具连接 | 更容易过渡到后续数据处理工具 |

因此 NumPy 不是“AI 本身”，但它很像一门用来读取 AI 计算的基础语言。本节不是深入教 NumPy，而是先建立这种最小直觉。

如果把 Part 2 Chapter 11 到 14 放在一条流程里，NumPy负责 `创建可计算的数字形状`，Pandas负责 `把这些形状读成案例与变量的表`，Matplotlib负责 `把表里不易直接看到的变化与关系读成图形`，Git负责 `把这些计算与解释连同变更原因留下成记录`。Chapter 11 正是这条流程最前面的位置，用来建立 vector、matrix、`shape` 这些可计算数字形状。

## List 与 Array 看起来相似，但目的不同

Python list 和 NumPy array 在外观上可能很像。

问题场景：我们想把同一组数字同时准备成 list 和 array，以便并排比较。
输入(input)：由同一份分数数据构成的两个变量，一个是 Python list，一个是 NumPy array。
期待输出(output)：没有打印输出，但已经准备好后面比较同一运算。
要确认的概念：看到即使外形相似，list 与 array 在计算里的含义也可能不同。

```python
python_scores = [82, 75, 45]
numpy_scores = np.array([82, 75, 45])
```

但一旦执行相同运算，差别就会显现出来。

问题场景：直接比较同一个 `+` 运算符在 list 和 array 中是怎样被读取的。
输入(input)：前面创建的 `python_scores` 与 `numpy_scores`。
期待输出(output)：list 会被拼接，array 会输出按位置相加的结果。
要确认的概念：确认 NumPy array 同时是存储结构与计算结构。

```python
print(python_scores + python_scores)
print(numpy_scores + numpy_scores)
```

在 list 中，`+` 表示把两个列表接在一起。

```text
[82, 75, 45, 82, 75, 45]
```

在 NumPy array 中，`+` 表示把相同位置的数字相加。

```text
[164 150  90]
```

这个差别必须记住。

| 结构 | 主要目的 | `+` 的代表性含义 |
| --- | --- | --- |
| Python list | 按顺序存放多个值的通用容器 | 列表拼接 |
| NumPy array | 让一组数字以同样形状参与计算 | 按位置加法 |

NumPy array 既是 `存放资料的结构`，也是 `执行计算的结构`。

下面的图示展示了同一个 `+` 符号在 list 与 NumPy array 中被不同地读取。

![Python list and NumPy array use the plus sign differently](../../../assets/part-02/chapter-11/list-vs-numpy-array-en.svg)

这个差别看起来可能不大，但在 AI 代码里很重要。你到底是想保存一组数字，还是想把同样的计算施加到整组数字上，问题是不同的。

## 构建向量

vector 可以读成“数字排成一行”的结构。

问题场景：创建一个看起来像 embedding 的一维 NumPy 数组，并检查它的基本属性。
输入(input)：包含四个实数的数组 `embedding`。
期待输出(output)：依次打印数组值、`shape`、`ndim`、`dtype`。
要确认的概念：看到把一维数组读成 vector，并把形状与维度一起检查的习惯。

```python
import numpy as np

embedding = np.array([0.12, -0.03, 0.44, 0.18])

print(embedding)
print(embedding.shape)
print(embedding.ndim)
print(embedding.dtype)
```

输出大致如下。

```text
[ 0.12 -0.03  0.44  0.18]
(4,)
1
float64
```

这里每一项信息表示如下。

| 表达 | 含义 | 在本例中的意思 |
| --- | --- | --- |
| `shape` | 数组的形状 | 有 4 个值的一维数组 |
| `ndim` | 维度数 | 一维 |
| `dtype` | 值的数据类型 | 实数 |

在数学上，你也可以把它与下面这个向量对应起来看。

\[
\mathbf{x} = [0.12,\ -0.03,\ 0.44,\ 0.18]
\]

这里把 vector 读成 `有顺序的数字集合`。但在 NumPy 里，更重要的是这组数字是“可计算的数组”。

## 构建矩阵

matrix 可以读成带有行(row)与列(column)的二维数组。

问题场景：创建一个看起来像多名学生分数表的二维数组，并检查它的属性。
输入(input)：2 行 3 列的整数数组 `scores`。
期待输出(output)：依次打印矩阵值、`shape`、`ndim`、`dtype`。
要确认的概念：看到怎样把二维数组读成 matrix，并通过 `shape` 确认行数与列数。

```python
scores = np.array([
    [82, 75, 45],
    [90, 61, 70],
])

print(scores)
print(scores.shape)
print(scores.ndim)
print(scores.dtype)
```

输出大致如下。

```text
[[82 75 45]
 [90 61 70]]
(2, 3)
2
int64
```

`(2, 3)` 的意思是 2 行 3 列。

\[
S =
\begin{bmatrix}
82 & 75 & 45 \\
90 & 61 & 70
\end{bmatrix}
\]

这里“2 行 3 列”不只是形状说明。你还必须决定每个 axis 代表什么。

例如，可以这样来读这个 matrix。

| axis | 解读 |
| --- | --- |
| row | student 或 sample |
| column | subject 或 feature |

在 AI 实践里，row 常常被读成 sample，column 常常被读成 feature。但并不总是如此。所以一旦创建数组，应该先检查 `shape`，再写下每个 axis 代表什么。

## Shape 是计算的语法

在 NumPy 代码里，`shape` 不是附带信息，而是判断什么计算可行的基础语法。

看下面这些数组。

问题场景：先检查 feature matrix 和 weight vector 是否具备可计算的匹配形状。
输入(input)：形状为 `(3, 2)` 的矩阵 `features`，以及长度为 2 的向量 `weights`。
期待输出(output)：打印两个数组的 `shape`。
要确认的概念：看到在计算前，应先确认形状是否匹配，而不是先看值本身。

```python
features = np.array([
    [1.0, 0.2],
    [0.8, 0.4],
    [0.3, 0.9],
])

weights = np.array([0.6, 0.4])

print(features.shape)
print(weights.shape)
```

输出如下。

```text
(3, 2)
(2,)
```

这些形状可以这样读。

| 数组 | shape | 含义 |
| --- | --- | --- |
| `features` | `(3, 2)` | 3 个 sample，2 个 feature |
| `weights` | `(2,)` | 对应 2 个 feature 的权重 |

现在就可以使用矩阵乘法运算符 `@` 来为每个 sample 计算一个分数。

问题场景：把每个 sample 的两个 feature 与权重相乘，算出按 sample 生成的分数。
输入(input)：前面的 `features` 矩阵与 `weights` 向量。
期待输出(output)：打印每个 sample 的分数数组以及结果 `shape`。
要确认的概念：确认只要内侧维度匹配，feature matrix 与 weight vector 就能生成按 sample 的分数。

```python
scores = features @ weights
print(scores)
print(scores.shape)
```

输出大致如下。

```text
[0.68 0.64 0.54]
(3,)
```

这个计算就是把每个 sample 的两个 feature 与权重相乘，再汇成一个分数。

\[
\begin{bmatrix}
1.0 & 0.2 \\
0.8 & 0.4 \\
0.3 & 0.9
\end{bmatrix}
\begin{bmatrix}
0.6 \\
0.4
\end{bmatrix}
=
\begin{bmatrix}
0.68 \\
0.64 \\
0.54
\end{bmatrix}
\]

这里重要的不是背公式，而是理解：`features` 的列数必须和 `weights` 的长度匹配，这个计算才能成立。

下面的图示从 shape 视角重新整理了同一个计算。

![Feature matrix times weight vector produces one score per sample](../../../assets/part-02/chapter-11/feature-weight-shape-flow-en.svg)

左边的 `features` 是一个有 3 个 sample、2 个 feature 的矩阵。中间的 `weights` 是对应这 2 个 feature 的权重向量。因为两个数组的内侧大小 2 一致，所以每个 sample 都会得到一个 score。

## 数组展示了小型模型计算的形状

上面的例子可以读成一个非常小的 model calculation。

真实的机器学习模型要复杂得多，但基础直觉相似：把多个 sample 的 feature 放进数值数组，准备一个 weight 数组，再把输出读成数组计算产生的结果。

这种结构会在 Part 3 的机器学习与 Part 4 的深度学习里不断重复。因此学习 NumPy array 的目的，不只是“会用一个库”，而是建立阅读模型计算的眼睛。

## 创建数组时先检查三件事

创建 NumPy array 后，先检查三件事。

问题场景：检查遇到一个新数组时，最先应该打印什么。
输入(input)：任意 NumPy 数组变量 `array`。
期待输出(output)：依次打印 `shape`、`ndim`、`dtype`。
要确认的概念：看到在逐个看值之前，先看数组形状、维度、类型的习惯。

```python
print(array.shape)
print(array.ndim)
print(array.dtype)
```

每一项都连到下面的问题。

| 检查项 | 问题 | 为什么重要 |
| --- | --- | --- |
| `shape` | 它是什么形状？ | 检查这个形状是否适合计算 |
| `ndim` | 它有几个维度？ | 区分 vector、matrix 和更高维结构 |
| `dtype` | 它是什么类型？ | 减少把整数、实数、字符串混在一起的误读 |

在入门阶段，如果出现错误，通常先检查 `shape` 会比逐个查看值更有效。在 AI 代码里，很多错误不是因为值太大或太小，而是因为数组形状不匹配。

## 示例代码文件

本节示例代码也可以在下面这个文件中查看。

- [p2_11_1_numpy_arrays.py](../../../assets/part-02/chapter-11/p2_11_1_numpy_arrays.py)

在 Colab 里，可以把代码内容贴到 cell 中运行。在本地 PC 上，可以在项目根目录这样执行。

```bash
python docs/assets/part-02/chapter-11/p2_11_1_numpy_arrays.py
```

这个命令会打印 vector、matrix、feature matrix、weight vector 的 `shape`、`ndim`、`dtype`，并展示一个小型 weighted-sum 计算。

输出里也包含 Python list 的 `+` 与 NumPy array 的 `+` 有何不同。这个例子就是为了让你亲自确认：即使是同一个符号，只要数据结构变了，含义也会跟着变化。

## 结合案例来看

### 案例 1. 为什么学生分数表突然开始像数字矩阵

当学习者先看学生分数表，再遇到 NumPy 数组例子时，很自然会觉得：“为什么这突然变成矩阵了？” 人在看表时通常先读姓名和科目，但到了计算阶段，每个学生的一组分数会被读成一行，每个科目会被读成一列。

例如，一个包含 4 名学生、每人 3 门成绩的表，在 NumPy 中可以表现为形状 `(4, 3)` 的数组。重要的不是去背很多数字，而是先抓住 `4 行代表 4 名学生`、`3 列代表 3 门科目` 这种对应。只有这样，后面的平均值、weighted sum、matrix multiplication 才能被解释清楚。

这个案例也说明了为什么要先看 `shape` 再看值。即使是同一组数字，你把它读成 `(4, 3)` 还是 `(3, 4)`，每个 axis 的意义都会改变，后面计算的解释也会跟着变。

换句话说，NumPy 入门与其说是在背新语法，不如说是在 `练习把现实数据读成可计算形状`。有了这种直觉，Part 3 之后的 feature matrix 与 weight calculation 才不会那么陌生。

## 本节要记住的视角

NumPy array 是把数字放进固定 shape 中再进行计算的结构。

Python list 与 NumPy array 看起来相似，但在计算里的含义可能不同。

vector 可以读成一维数组，matrix 可以读成二维数组。

`shape` 是数组计算的语法。

在 AI 实践里，input、feature、weight、output 都可能以数组形状出现。

读完本节后，下面这条流程应当自然接上。

| 当前章节的把手 | 下一章继续检查什么 | 最后要留下什么记录 |
| --- | --- | --- |
| 读懂可计算数字形状与 `shape` | 把这些数字形状作为表和图继续检查与解释 | 通过 Git 留下记录，使所用数组与解释能再次被说明 |

## 简短检查

- 能说明 Python list 与 NumPy array 在目的上的差别。
- 能用 `np.array()` 构建 vector 与 matrix。
- 能说明 `.shape`、`.ndim`、`.dtype` 会告诉你什么。
- 能区分一维数组与二维数组。
- 能读懂 `(样本数, 特征数)` 形式的矩阵。
- 能说明像 `features @ weights` 这样的小计算里，输入与输出的 shape。

## 什么时候应先想起这个视角

- 当 Python list 已经不足以读出计算结构，而你必须按 vector 与 matrix 单位处理数据时，应先想起 NumPy array 视角。
- 当你需要开始把数据集读成 `(样本数, 特征数)` 这样的 shape 时，就回到本节的数组直觉。
- 当你需要解释一个简单线性代数计算会怎样随着输入输出 shape 而变化时，再回来检查本节。

## 来源与参考资料

- NumPy Developers, [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-25.
- NumPy Developers, [The N-dimensional array](https://numpy.org/doc/stable/reference/arrays.ndarray.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-25.
- NumPy Developers, [Array creation](https://numpy.org/doc/stable/user/basics.creation.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-25.
