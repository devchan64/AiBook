# P2-3.6 用 NumPy 确认线性代数

> Section ID: `P2-3.6`
> Version: `v2026.09.08`

NumPy 是 Python 中用于创建数组和进行数组计算的库。数组的 `shape` 表示每个轴的长度，`*` 计算逐位置乘法，`@` 计算矩阵乘法。

## 运行环境

这一节的代码可以在任何安装了 NumPy 的 Python 环境里运行。

先按照 P2-3.5 的 [命令的执行位置](section-05.zh.md#_2) 来确认执行位置。如果还没有安装 Python，可以在 Google Colab 代码单元里运行；如果使用本地 PC，也可以在自己的终端里运行。

在 Colab 代码单元里，可以这样准备 NumPy。

```python
# 这条命令是在 Colab/Jupyter 代码单元里安装 NumPy。
%pip install numpy
```

在本地 PC 终端里，则使用下面的命令。

```bash
python -m pip install numpy
```

然后，在 Python 代码里，用下面这种方式导入 NumPy。

```python
# 这一行把已安装的 NumPy 用 np 这个短名字导入 Python 代码。
import numpy as np
```

这里的 `np` 是对 NumPy 的惯例性简写别名(alias)。

本节完整的示例代码也可以通过下面这个文件获得。

- [p2_3_6_numpy_linear_algebra.py](/AiBook/assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py)

如果从项目根目录运行，可以在个人电脑终端里使用下面的命令。

```bash
python docs/assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py
```

这个文件会把向量加法、标量乘法、逐位置乘法、矩阵乘法、batch 计算一起打印出来。

## 创建向量与矩阵

向量(vector)可以作为值的列表来创建。

```python
import numpy as np

# x 是一个有两个成分的输入向量。
x = np.array([2, 3])

print(x)

# shape 用来确认这个向量是包含两个成分的一维数组。
print(x.shape)
```

输出可以读成：

```text
[2 3]
(2,)
```

`(2,)` 表示“一个含有 2 个值的一维数组”。对应到公式里就是：

\[
\mathbf{x} = [2,\ 3]
\]

矩阵(matrix)则可以创建成带有行(row)和列(column)的二维数组。

```python
# W 是把输入向量变成另一个输出的 2x2 权重矩阵。
W = np.array([
    [4, 1],
    [5, 2],
])

print(W)

# W 的 shape 是判断矩阵乘法维度是否匹配的依据。
print(W.shape)
```

输出可以读成：

```text
[[4 1]
 [5 2]]
(2, 2)
```

`(2, 2)` 表示 2 行 2 列。

\[
W =
\begin{bmatrix}
4 & 1 \\
5 & 2
\end{bmatrix}
\]

## shape 与乘法条件

当 AI 代码里的计算不工作时，往往应该先看 shape，再看数值。

在 `x @ W` 中，向量 `x` 的长度必须等于矩阵 `W` 的行数。

```python
# x 是输入向量，W 是要与它相乘的权重矩阵。
x = np.array([2, 3])
W = np.array([
    [4, 1],
    [5, 2],
])

# 把两个 shape 并排输出，可以先判断 x @ W 是否可行。
print("x shape:", x.shape)
print("W shape:", W.shape)
```

输出会是：`x shape: (2,)`，`W shape: (2, 2)`。

这些信息能帮助我们回答：`x 有多少个值`、`W 接收多少输入并产生多少输出`、`它们两者能不能相乘`。

`x` 是一个含有 2 个输入值的向量，而 `W` 是一个接收 2 个输入并产生 2 个输出的权重矩阵(weight matrix)。

## 向量加法与标量乘法

向量加法(vector addition)会把相同位置上的值相加。

```python
# a 和 b 是两个 shape 相同的向量。
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# 这里确认相同位置的成分会相加。
print(a + b)
```

输出是：

```text
[5 7 9]
```

对应到公式里：

\[
[1,\ 2,\ 3] + [4,\ 5,\ 6] = [5,\ 7,\ 9]
\]

标量乘法(scalar multiplication)则是把同一个数字乘到数组的每个位置上。

```python
# 这里把前面创建的向量 a 的每个成分都乘以同一个标量 2。
print(2 * a)
```

输出是：

```text
[2 4 6]
```

对应到公式里：

\[
2[1,\ 2,\ 3] = [2,\ 4,\ 6]
\]

## `*`：逐位置乘法

在 NumPy 里，数组之间的 `*` 通常表示逐位置乘法(element-wise multiplication)。

```python
# a 和 b 是用来比较逐元素乘法的两个向量。
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# * 会把相同位置的成分相乘。
print(a * b)
```

输出是：

```text
[ 4 10 18]
```

对应到公式里：

\[
[1,\ 2,\ 3] \odot [4,\ 5,\ 6] = [4,\ 10,\ 18]
\]

这里最重要的是：`*` 不是矩阵乘法。它只是把相同位置的值相乘。换句话说，`*` 是逐位置乘法，`@` 才是矩阵乘法。

## `@`：矩阵乘法

在 NumPy 里，`@` 用来做矩阵乘法(matrix multiplication)。

```python
# x 是输入向量，W 是生成输出成分的权重矩阵。
x = np.array([2, 3])
W = np.array([
    [4, 1],
    [5, 2],
])

# y 是 x 和 W 做矩阵乘法后得到的输出向量。
y = x @ W

print(y)
print(y.shape)
```

输出是：

```text
[23  8]
(2,)
```

这个计算正是 `P2-3.3` 里看过的加权求和结构。

\[
[2,\ 3]
\begin{bmatrix}
4 & 1 \\
5 & 2
\end{bmatrix}
=
[23,\ 8]
\]

第一个输出是：

\[
2 \times 4 + 3 \times 5 = 23
\]

第二个输出是：

\[
2 \times 1 + 3 \times 2 = 8
\]

所以，`@` 就是 `乘并相加、做出新向量的计算`。

## 批量矩阵计算

如果把多个输入样本(sample)收集成一个矩阵，就可以把同一个权重矩阵一次性应用上去。

```python
# X 是把两个样本放在行里的输入矩阵。
X = np.array([
    [2, 3],
    [1, 4],
])

# W 是把每个输入样本变成输出向量的权重矩阵。
W = np.array([
    [4, 1],
    [5, 2],
])

# Y 是把 W 应用于整个输入批次 X 后得到的输出矩阵。
Y = X @ W

print(X.shape)
print(W.shape)
print(Y)
print(Y.shape)
```

输出是：

```text
(2, 2)
(2, 2)
[[23  8]
 [24  9]]
(2, 2)
```

对应到公式里：

\[
X =
\begin{bmatrix}
2 & 3 \\
1 & 4
\end{bmatrix}
\]

\[
W =
\begin{bmatrix}
4 & 1 \\
5 & 2
\end{bmatrix}
\]

\[
XW =
\begin{bmatrix}
23 & 8 \\
24 & 9
\end{bmatrix}
\]

这里，第一行是第一个样本的输出，第二行是第二个样本的输出。也就是说：有 2 个输入样本，每个样本有 2 个值，应用同一个 `W` 之后，得到 2 个输出样本，而每个输出也有 2 个值。

这就是 batch 计算最小的例子。

## 输入长度不匹配

下面这个计算就不能直接对上。

```python
# bad_x 有 3 个成分，因此和只有 2 行的 W 做矩阵乘法时维度不匹配。
bad_x = np.array([2, 3, 4])
W = np.array([
    [4, 1],
    [5, 2],
])

bad_y = bad_x @ W
```

`bad_x` 的 shape 是 `(3,)`，而 `W` 的 shape 是 `(2, 2)`。输入有 3 个值，但权重矩阵只接收 2 个输入。也就是：`bad_x shape: (3,)`，`W shape: (2, 2)`。

因此，它无法对齐到底哪些输入值该与哪些权重相乘。在真实的 NumPy 运行中，就会报出 shape 不匹配的错误。

要让第三个输入也参与计算，`W` 需要增加与它对应的一行权重。如果保持两个输出，`W` 的 shape 应为 `(3, 2)`。为了匹配 shape 而任意删除输入值，会改变提供给模型的数据含义。

## 检查清单

- 能用 NumPy 数组(array)创建向量和矩阵吗？
- 能用 `.shape` 检查向量与矩阵的形状吗？
- 能把向量加法和标量乘法连回代码与公式吗？
- 能说明 NumPy 的 `*` 是逐位置乘法(element-wise multiplication)吗？
- 能说明 NumPy 的 `@` 是矩阵乘法(matrix multiplication)吗？
- 能读懂 `x @ W` 里的输入 shape、权重 shape、输出 shape 吗？
- 能说明“把多个样本收集成矩阵，再应用同一个权重矩阵”的 batch 计算吗？
- 能说明在 NumPy 里，比起单独记语法，更重要的是把公式、shape、输出一起阅读的习惯吗？
- 能区分 `*` 和 `@`，并应用“先看 shape、再看值”的标准吗？

## 来源与参考资料

- 本节示例代码：[p2_3_6_numpy_linear_algebra.py](/AiBook/assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py)
- NumPy Developers, [NumPy documentation](https://numpy.org/doc/){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-19.
- NumPy Developers, [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-19.
- NumPy Developers, [`numpy.array`](https://numpy.org/doc/stable/reference/generated/numpy.array.html){: target="_blank" rel="noopener noreferrer" }。可以确认数组创建 API 的参数和示例。确认日期: 2026-07-19.
- NumPy Developers, [`numpy.ndarray.shape`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.shape.html){: target="_blank" rel="noopener noreferrer" }。可以确认把数组维度作为元组读取的 `shape` 属性。确认日期: 2026-07-19.
- NumPy Developers, [`numpy.matmul`](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html){: target="_blank" rel="noopener noreferrer" }。可以确认矩阵乘法以及 shape 不匹配时的错误条件。确认日期: 2026-07-19.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, 确认日期: 2026-07-19.
