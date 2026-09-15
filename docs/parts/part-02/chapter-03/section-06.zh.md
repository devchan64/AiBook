# P2-3.6 用 NumPy 确认线性代数

> Section ID: `P2-3.6`
> Version: `v2026.09.14`

NumPy 是用于创建数组和进行数组计算的 Python 库。我们可以用代码计算上一节的向量比较，并改变输入与权重的形状，观察输出如何变化。数组的 `shape` 表示每个轴的长度。

## 运行环境

安装位置遵循 [P2-3.5 的说明](/AiBook/zh/parts/part-02/chapter-03/section-05/#_2)。在 Colab/Jupyter 中，将以下命令输入代码单元。

```text title="IPython · 笔记本代码单元"
%pip install numpy
```

在本地 PC 上，将以下命令输入终端。

```bash
python -m pip install numpy
```

在同一会话中从上到下执行以下 Python 代码块。后面的代码块使用前面定义的变量和 `np`。要一次运行全部代码，请使用以下文件。

[p2_3_6_numpy_linear_algebra.py](/AiBook/assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py)

以下命令在仓库根目录运行。如果只下载了文件，则在保存文件的目录中运行 `python p2_3_6_numpy_linear_algebra.py`。

```bash
python docs/assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py
```

## 数组的 shape 与输出

`import numpy as np` 将 NumPy 导入为简短名称 `np`。向 `np.array` 传入数值列表会创建一维数组，传入按行组织的列表则会创建二维数组。

```python
import numpy as np

x = np.array([2, 3])
W = np.array([[4, 1], [5, 2]])
print(x.shape)
print(W.shape)
print(x @ W)
```

```text title="文本 · 运行结果"
(2,)
(2, 2)
[23  8]
```

`x.shape` 中的 `(2,)` 表示有两个分量的一维数组。它与 `(1, 2)` 这样只有一行的二维数组不同。`W.shape` 中的 `(2, 2)` 表示两行两列。`x @ W` 将 `x` 与 `W` 的每一列相乘并求和，输出为 `[2×4+3×5, 2×1+3×2] = [23, 8]`。

## `*` 与 `@` 的区别

对于 shape 相同的数组，`+` 和 `*` 分别对对应位置的分量进行计算。乘以一个数时，每个分量都乘以这个数。对两个一维向量使用 `@`，会将分量的乘积相加，得到一个内积数值。

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(a + b)
print(2 * a)
print(a * b)
print(a @ b)
```

```text title="文本 · 运行结果"
[5 7 9]
[2 4 6]
[ 4 10 18]
32
```

`a * b` 保留各乘积，得到 `[4, 10, 18]`；`a @ b` 则把它们加起来，得到 `4+10+18=32`。前面的 `x @ W` 返回向量，这里的 `a @ b` 返回一个数。`@` 的输出形状取决于输入数组的维数。对于 shape 不同的数组，`*` 还会应用广播规则，因此逐元素乘法并不总是要求形状完全相同。

## 比较购买量向量

沿用 P2-3.4 的 `[咖啡购买量, 茶购买量]` 向量。`np.linalg.norm(v)` 计算这个一维向量的 2-范数。`v-q` 是两组购买量之差，其范数就是欧氏距离。

```python
q = np.array([1, 1])
candidates = {
    "a": np.array([2, 2]),
    "b": np.array([1, 0]),
    "c": np.array([10, 10]),
}
for name, v in candidates.items():
    dot = q @ v
    norm = np.linalg.norm(v)
    distance = np.linalg.norm(v - q)
    cosine = dot / (np.linalg.norm(q) * norm)
    print(f"{name}: dot={dot}, norm={norm:.3f}, "
          f"distance={distance:.3f}, cosine={cosine:.3f}")
```

```text title="文本 · 运行结果"
a: dot=4, norm=2.828, distance=1.414, cosine=1.000
b: dot=1, norm=1.000, distance=1.000, cosine=0.707
c: dot=20, norm=14.142, distance=12.728, cosine=1.000
```

`dot`、`norm`、`distance`、`cosine` 分别表示内积、长度、距离和余弦相似度。输出格式 `:.3f` 表示显示小数点后三位，并不把计算本身限制在这一精度。按距离比较，`b` 最近；按余弦相似度比较，`a` 和 `c` 并列。购买量更大的 `c` 得到最大的内积。这一余弦计算要求两个向量的长度都非零。

将 `candidates` 中的 `a` 改为 `[4, 4]` 后再次运行。内积变为 `8`，长度约为 `5.657`，距离约为 `4.243`，余弦相似度仍为 `1.000`。这是购买量增加而购买比例不变的结果。

## 样本数、输入分量数与输出分量数

将三个输入按行组合，把每个输入的两个分量变为四个输出分量。下面的权重是为演示计算而手动指定的，并非通过训练得到。

```python
X = np.array([
    [2, 3],
    [1, 4],
    [0, 1],
])
W = np.array([
    [4, 1, 1, 0],
    [5, 2, 0, 1],
])
Y = X @ W
print(X.shape, W.shape, Y.shape)
print(Y)
```

```text title="文本 · 运行结果"
(3, 2) (2, 4) (3, 4)
[[23  8  2  3]
 [24  9  1  4]
 [ 5  2  0  1]]
```

| 数组 | shape | 行与列的含义 |
| --- | --- | --- |
| `X` | `(3, 2)` | 三个样本，每个样本有两个输入分量 |
| `W` | `(2, 4)` | 对应两个输入分量、四个输出分量的权重 |
| `Y` | `(3, 4)` | 三个样本，每个样本有四个输出分量 |

在 `(3, 2) @ (2, 4) → (3, 4)` 中，中间的两个 `2` 必须相等才能计算。结果保留样本数 `3` 和输出分量数 `4`。`W` 的前两列保留前面的 `[23, 8]` 计算，后两列分别原样输出第一个和第二个输入分量。每个样本都应用同一个 `W`，因此一行输出对应一行输入。

## 维度错误与增加权重行

将具有三个分量的输入乘以当前只有两行的 `W` 会出错。下面的代码捕获错误，并输出输入分量数和权重行数。完整错误消息可能因 NumPy 版本而不同。

```python
bad_x = np.array([2, 3, 4])
try:
    bad_x @ W
except ValueError:
    print("ValueError: input components = 3, weight rows = 2")
```

```text title="文本 · 运行结果"
ValueError: input components = 3, weight rows = 2
```

要使用第三个输入分量，就需要对应的一行权重。为了匹配形状而随意删除输入分量，会改变数据的含义。新增一行 `[1, 0, 0, 1]`，让第三个输入以系数 1 分别加到第一个和第四个输出中。`np.vstack` 沿行方向纵向堆叠数组。

```python
W_fixed = np.vstack([W, [1, 0, 0, 1]])
print(W_fixed.shape)
print(bad_x @ W_fixed)
```

```text title="文本 · 运行结果"
(3, 4)
[27  8  2  7]
```

第三个输入 `4` 在 `[2, 3]` 原有的输出 `[23, 8, 2, 3]` 上加上 `[4, 0, 0, 4]`，得到 `[27, 8, 2, 7]`。匹配 shape 与确定新输入的作用必须同时进行。

## 练习：再增加一个样本

在批量输入 `X` 的最后添加一行 `[2, 0]`，保持 `W` 不变。运行前，先预测 `X`、`Y` 的 shape 和新增的输出行。

??? note "计算与解析"
    `X.shape` 变为 `(4, 2)`，`Y.shape` 变为 `(4, 4)`。新增输出行为 `[8, 2, 2, 0]`。每个样本仍然只有两个输入分量，因此增加样本不需要改变 `W`。前面三个输出行也保持不变。

## 检查清单

- 能否解释 `(2,)` 与 `(1, 2)` 为什么是不同的数组形状？
- 能否解释对向量应用 `*` 和 `@` 为什么分别得到数组和一个数？
- 能否将内积、范数、距离和余弦相似度的计算与上一节的购买量比较联系起来？
- 能否在运行前预测 `(3, 2) @ (2, 4)` 的结果 shape？
- 能否解释增加样本与增加输入分量对权重的影响有何不同？

## 来源与参考资料

- NumPy Developers, [NumPy documentation](https://numpy.org/doc/){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-19.
- NumPy Developers, [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-19.
- NumPy Developers, [`numpy.array`](https://numpy.org/doc/stable/reference/generated/numpy.array.html){: target="_blank" rel="noopener noreferrer" }。可以确认数组创建 API 的参数和示例。确认日期: 2026-07-19.
- NumPy Developers, [`numpy.ndarray.shape`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.shape.html){: target="_blank" rel="noopener noreferrer" }。可以确认把数组维度作为元组读取的 `shape` 属性。确认日期: 2026-07-19.
- NumPy Developers, [`numpy.matmul`](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html){: target="_blank" rel="noopener noreferrer" }。可以确认矩阵乘法以及 shape 不匹配时的错误条件。确认日期: 2026-07-19.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, 确认日期: 2026-07-19.
- [numpy.linalg.norm](https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html){: target="_blank" rel="noopener noreferrer" }, 查阅日期: 2026-09-14.
- [cosine_similarity](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html){: target="_blank" rel="noopener noreferrer" }, 查阅日期: 2026-09-14.
- [Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html){: target="_blank" rel="noopener noreferrer" }, 查阅日期: 2026-09-14.
