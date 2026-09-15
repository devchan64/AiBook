# P2-11.1 用 NumPy 数组创建向量与矩阵

> Section ID: `P2-11.1`
> Version: `v2026.09.15`

## 列表连接与数组加法

NumPy 是提供多维 `ndarray` 和数组运算的 Python 库。列表与数组可以保存相同数字，但运算规则不同。

把 `[82, 75, 45]` 分别准备为 Python 列表和 NumPy 数组。这些赋值只保存数值，不产生输出。

```python
import numpy as np

python_scores = [82, 75, 45]
numpy_scores = np.array([82, 75, 45])
```

执行相同运算就能看出差异。

将每个集合与自身相加。列表连接成六项，数组则把对应位置相加，得到 `[164 150 90]`。

```python
print(python_scores + python_scores)
print(numpy_scores + numpy_scores)
```

列表中的 `+` 连接两个序列。

```text
[82, 75, 45, 82, 75, 45]
```

NumPy 数组中的 `+` 把相同位置的数字相加。

```text
[164 150  90]
```

| 结构 | 主要用途 | `+` 的典型含义 |
| --- | --- | --- |
| Python 列表 | 按顺序存放多个值的通用容器 | 列表连接 |
| NumPy 数组 | 按一定形状计算一组数值 | 对应元素相加 |

NumPy 数组既组织数据存储，也组织计算。

下图比较同一个 `+` 在列表和 NumPy 数组中的含义。

```mermaid
--8<-- "assets/part-02/chapter-11/list-vs-numpy-array-zh.mmd"
```

这种区别在 AI 代码中很重要：存放一组数值，与对整组数值执行同一计算，是不同的任务。

## 创建向量

向量可以看作排成一行的数字。

用四个浮点数创建一维数组。输出包括数值、形状 `(4,)`、维数 `1` 和数据类型 `float64`。

```python
import numpy as np

embedding = np.array([0.12, -0.03, 0.44, 0.18])

print(embedding)
print(embedding.shape)
print(embedding.ndim)
print(embedding.dtype)
```

预期输出：

```text
[ 0.12 -0.03  0.44  0.18]
(4,)
1
float64
```

这些属性表示：

| 属性 | 含义 | 本例含义 |
| --- | --- | --- |
| `shape` | 数组形状 | 包含四个值的一维数组 |
| `ndim` | 维数 | 一维 |
| `dtype` | 元素数据类型 | 浮点数 |

在数学上，可以对应以下向量：

\[
\mathbf{x} = [0.12,\ -0.03,\ 0.44,\ 0.18]
\]

`(4,)` 中的逗号表示单元素元组。数组有一个轴，该轴上有四个值。

## 创建矩阵

矩阵可以看作具有行和列的二维数组。

把两名学生的三科分数存成二维数组。输出包括数值、形状 `(2, 3)`、维数 `2` 和整数类型。显式指定 `dtype=np.int64` 后，类型为 `int64`。

```python
scores = np.array([
    [82, 75, 45],
    [90, 61, 70],
], dtype=np.int64)

print(scores)
print(scores.shape)
print(scores.ndim)
print(scores.dtype)
```

预期输出：

```text
[[82 75 45]
 [90 61 70]]
(2, 3)
2
int64
```

`(2, 3)` 表示两行三列。

\[
S =
\begin{bmatrix}
82 & 75 & 45 \\
90 & 61 & 70
\end{bmatrix}
\]

形状本身不规定轴的含义，需要明确各轴代表什么。

例如，可以这样解释矩阵：

| 轴 | 解释 |
| --- | --- |
| 行 | 学生或样本 |
| 列 | 科目或特征 |

AI 示例常把样本放在行、特征放在列，但并非总是如此。创建数组后，应检查 `shape` 并记录各轴的含义。

## dtype 与小数保留

数组的 `dtype` 决定各元素的存储方式。把小数赋给整数数组，不会自动把整个数组变成浮点类型。

```python
integer_scores = np.array([82, 75, 45], dtype=np.int64)
float_scores = integer_scores.astype(np.float64)
integer_scores[1] = 75.5
float_scores[1] = 75.5

print(integer_scores.tolist())
print(float_scores.tolist())
```

输出是 `[82, 75, 45]` 和 `[82.0, 75.5, 45.0]`。向整数数组赋值 75.5 会丢失小数部分，先转成浮点类型则能保留。已经存成 75 后再转浮点，不能恢复丢失的 0.5。创建数组时就应决定是否需要保留小数。

## 矩阵乘法的形状

`shape` 是 NumPy 计算规则的一部分，决定哪些运算可以进行。

有三个样本，每个样本两个特征。特征矩阵和权重向量的形状是 `(3, 2)` 与 `(2,)`。

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

输出：

```text
(3, 2)
(2,)
```

可以这样理解这些形状：

| 数组 | 形状 | 含义 |
| --- | --- | --- |
| `features` | `(3, 2)` | 三个样本、两个特征 |
| `weights` | `(2,)` | 对应两个特征的权重 |

矩阵乘法运算符 `@` 可以计算每个样本的分数。

将 `features` 与 `weights` 相乘，得到 `[0.68 0.64 0.54]`，结果形状为 `(3,)`。

```python
scores = features @ weights
print(scores)
print(scores.shape)
```

输出如下：

```text
[0.68 0.64 0.54]
(3,)
```

每个样本的两个特征分别乘以权重，再合成一个分数。

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

第一个分数是 1.0 × 0.6 + 0.2 × 0.4 = 0.68。`features` 的列数和 `weights` 的长度都必须为 2，才能让每个特征对应一个权重。

下图从形状角度整理这一计算。

```mermaid
--8<-- "assets/part-02/chapter-11/feature-weight-shape-flow-zh.mmd"
```

`features` 有三个样本、两个特征，`weights` 为每个特征提供一个权重。内部大小 2 相匹配，因此每个样本得到一个分数。

## 逐元素乘法与矩阵乘法

`features * weights` 保留各特征乘权重后的值；`features @ weights` 则把同一样本的乘积相加。输入相同，结果形状也可能不同。

```python
weighted = features * weights
print(weighted)
print(weighted.sum(axis=1))
```

```text
[[0.6  0.08]
 [0.48 0.16]
 [0.18 0.36]]
[0.68 0.64 0.54]
```

逐元素乘积的形状为 `(3, 2)`，沿特征轴求和后为 `(3,)`。本例中，`weighted.sum(axis=1)` 与 `features @ weights` 计算相同的加权和。`*` 本身不会自动把乘积合成样本分数。

## 检查数组属性

创建 NumPy 数组时，检查三个属性。

特征矩阵的 `shape`、`ndim` 和 `dtype` 分别为 `(3, 2)`、`2` 和 `float64`。

```python
print(features.shape)
print(features.ndim)
print(features.dtype)
```

各属性回答不同的问题：

| 属性 | 问题 | 为什么重要 |
| --- | --- | --- |
| `shape` | 什么形状？ | 检查运算是否兼容 |
| `ndim` | 多少维？ | 区分向量、矩阵和更高维数组 |
| `dtype` | 什么类型？ | 减少整数、浮点数和字符串混淆 |

数组运算失败时，检查形状通常比逐个查看数值更有帮助。形状不匹配时，无论数值大小如何，都可能无法计算。

## 示例代码文件

这些示例也可以通过下面的文件查看：

- [p2_11_1_numpy_arrays.py](/AiBook/assets/part-02/chapter-11/p2_11_1_numpy_arrays.py)

在 Colab 中，可把代码粘贴到单元中；在本地，从项目根目录执行：

```bash
python docs/assets/part-02/chapter-11/p2_11_1_numpy_arrays.py
```

脚本输出向量、矩阵、特征矩阵和权重向量的 `shape`、`ndim`、`dtype`，并演示小型加权和计算。

它也比较 Python 列表的 `+` 与 NumPy 数组的 `+`，展示相同符号如何随数据结构改变含义。

## 案例：调换权重顺序

前面两个特征列的权重原本为 0.6 和 0.4。改成 `[0.4, 0.6]` 后，结果为 `[0.52, 0.56, 0.66]`。最高分从第一个样本变成第三个样本。

形状仍为 `(3, 2) @ (2,)`，所以计算成功。仅检查形状，不能确认列与权重的含义是否对应。若改为 `[0.6, 0.3, 0.1]`，长度变为 3，矩阵乘法会产生 `ValueError`。

| 修改 | 结果 | 检查要点 |
| --- | --- | --- |
| 权重 `[0.6, 0.4]` | `[0.68, 0.64, 0.54]` | 特征与权重的对应 |
| 权重 `[0.4, 0.6]` | `[0.52, 0.56, 0.66]` | 形状相同也会改变分数与排序 |
| 权重 `[0.6, 0.3, 0.1]` | 形状不匹配错误 | 特征数与权重数不同 |

## 检查清单

- 能解释 Python 列表与 NumPy 数组的用途差异。
- 能用 `np.array()` 创建向量与矩阵。
- 能解释 `.shape`、`.ndim` 和 `.dtype`。
- 能区分一维与二维数组。
- 能理解 `(样本数, 特征数)` 形式的矩阵。
- 能解释 `features @ weights` 的输入输出形状。
- 能把 NumPy 数组理解为按形状组织数字并计算的结构。
- 能否解释向整数数组赋小数值时的信息丢失，以及 `*` 与 `@` 的结果差异？

## 来源与参考资料

- NumPy Developers, [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual，确认日期：2026-07-20。用于确认 NumPy array 的 homogeneous N-dimensional `ndarray`、shape、dtype，以及与 Python list 的差异。
- NumPy Developers, [The N-dimensional array](https://numpy.org/doc/stable/reference/arrays.ndarray.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual，确认日期：2026-07-20。作为 vector 与 matrix 示例中 `ndarray` 属性和 array object 结构的依据。
- NumPy Developers, [Array creation](https://numpy.org/doc/stable/user/basics.creation.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual，确认日期：2026-07-20。用于确认 `np.array`、`zeros`、`ones`、`arange`、`linspace` 等基本 array creation 方式。
- NumPy Developers, [numpy.ndarray.astype](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.astype.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, 查阅日期: 2026-09-15. 数据类型转换与复制.
- NumPy Developers, [numpy.matmul](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, 查阅日期: 2026-09-15. 矩阵向量乘法的维度及其与逐元素乘法的区别.
