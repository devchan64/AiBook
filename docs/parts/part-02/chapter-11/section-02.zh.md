# P2-11.2 索引、切片与轴

> Section ID: `P2-11.2`
> Version: `v2026.07.20`

在 P2-11.1 中，我们创建了 NumPy array，并检查了 `shape`、`ndim`、`dtype`。现在继续看：该从数组里读哪一个值、切出哪一段、以及计算沿哪个方向进行。

在读取 NumPy array 时，最常遇到的有三个词。

indexing、slicing、axis。

这三个词看起来相近，但角色不同。indexing 选位置，slicing 选区间，axis 决定计算方向。

本节说明 `indexing`、`slicing`、`axis` 的基本区分。`NumPy` 与数组基本属性可以回到 P2-11.1 和 [概念词汇表](/AiBook/reference/concept-glossary/) 再看，这里专注于：从数组里选什么、按哪个方向去读。

## 核心判断标准：索引、切片与轴

- 能把 `x[0]`、`x[1, 2]` 这样的 indexing 解释成位置选择。
- 能把 `x[1:3]`、`x[:, 0]`、`x[0:2, 1:3]` 这样的 slicing 解释成区间选择。
- 在二维数组中，能把第一个轴 (`axis 0`) 读成行方向，把第二个轴 (`axis 1`) 读成列方向。
- 能说明为什么 `sum(axis=0)` 与 `sum(axis=1)` 的结果 shape 不同。
- 能说明在数据集中，行常常被读成 sample，列常常被读成 feature。

## 先抓住的一个画面

本节最先要抓住的画面如下。

| 数组表达式 | 像数据集一样去读时，先要问的问题 |
| --- | --- |
| `shape = (4, 3)` | 是 4 个 sample、3 个 feature 吗？ |
| `x[1, :]` | 是在选第二个 sample 吗？ |
| `x[:, 2]` | 是在选整个第三个 feature 列吗？ |
| `sum(axis=0)` | 是在留下按 feature 汇总的结果吗？ |
| `sum(axis=1)` | 是在留下按 sample 汇总的结果吗？ |

也就是说，`indexing`、`slicing`、`axis` 不是分开背的语法，而是把“现在是在看一个 sample、一个完整 feature，还是在按某个方向做汇总”明确写到数组上的方法。

## 三个标准

| 标准 | 为什么重要 | 本节需要达到的理解程度 |
| --- | --- | --- |
| indexing 是什么 | 它能避免把位置选择与区间选择混在一起 | 理解成选择一个准确位置 |
| slicing 是什么 | 它能帮助区分单个值与部分数组 | 理解成保留一个区间，而不是一个点 |
| 为什么 axis 重要 | 它会成为后面读取聚合与 broadcasting 方向的标准 | 理解成决定数组计算方向的标准 |

| 术语 | 本节先抓住的含义 |
| --- | --- |
| indexing | 选择一个准确位置的读取方式 |
| slicing | 指定起点与终点，保留一个区间的读取方式 |
| axis | 决定数组计算沿哪个方向进行的标准 |
| row | 二维数组中的一条横线 |
| column | 二维数组中的一条竖线 |

## Indexing 就是选择位置

NumPy 官方文档说明，`ndarray` 可以用标准 Python 形式 `x[obj]` 进行 indexing。它也说明：和 Python 一样，索引从 0 开始。

先看一维数组。

问题场景：确认一维数组中“选第几个值”的基本 indexing。
输入(input)：一个包含四个分数的一维数组 `scores`。
期待输出(output)：打印第一个值 `82` 和第三个值 `45`。
要确认的概念：看到 indexing 是选择一个准确位置，而且位置编号从 0 开始。

```python
# 这个例子按位置、切片和轴选择并汇总 NumPy 数组中的值。
import numpy as np

scores = np.array([82, 75, 45, 90])

print(scores[0])
print(scores[2])
```

输出如下。

```text
82
45
```

`scores[0]` 是第一个值，`scores[2]` 是第三个值。在 Python 与 NumPy 中，通常不是从 1 开始数，而是从 0 开始。

这一点很容易混淆。

| 表达式 | 读取方式 | 结果 |
| --- | --- | --- |
| `scores[0]` | 位置 0 | `82` |
| `scores[1]` | 位置 1 | `75` |
| `scores[2]` | 位置 2 | `45` |
| `scores[-1]` | 最后一个位置 | `90` |

indexing 问的是：`这个位置上的值是什么？`

## 在二维数组里，要同时选行与列

在二维数组里，通常会同时指定 row 与 column。

问题场景：在二维数组中，同时指定行和列的位置来选一个值。
输入(input)：3 行 4 列数组 `data`，以及位置 `[1, 2]`。
期待输出(output)：打印完整 `shape` 和被选中的值 `22`。
要确认的概念：确认 `data[row, column]` 是选择一个值的基本语法。

```python
# 这个例子按位置、切片和轴选择并汇总 NumPy 数组中的值。
data = np.array([
    [10, 11, 12, 13],
    [20, 21, 22, 23],
    [30, 31, 32, 33],
])

print(data.shape)
print(data[1, 2])
```

输出如下。

```text
(3, 4)
22
```

`data[1, 2]` 选择的是第 1 行、第 2 列的值。

这里索引同样从 0 开始。

| 表达式 | 读取方式 | 结果 |
| --- | --- | --- |
| `data[0, 0]` | 第 0 行，第 0 列 | `10` |
| `data[0, 3]` | 第 0 行，第 3 列 | `13` |
| `data[1, 2]` | 第 1 行，第 2 列 | `22` |
| `data[2, 1]` | 第 2 行，第 1 列 | `31` |

在二维数组里，逗号可以理解为维度之间的分隔。所以可以直接读成 `data[row, column]`。

## Slicing 就是保留区间

slicing 选的不是一个位置，而是一段区间。

问题场景：我们想只保留一维数组中间的一段。
输入(input)：一个包含四个分数的数组，以及切片 `1:3`。
期待输出(output)：打印只包含第二和第三个值的数组。
要确认的概念：看到 slicing 会保留从起点到终点之前的区间，而不包含 stop 位置。

```python
# 这个例子按位置、切片和轴选择并汇总 NumPy 数组中的值。
scores = np.array([82, 75, 45, 90])

print(scores[1:3])
```

输出如下。

```text
[75 45]
```

`1:3` 的意思是从位置 1 开始，到位置 3 之前结束。所以会选中位置 1 和 2。

这里可以这样记。

| 表达式 | 含义 |
| --- | --- |
| `start:stop` | 从 start 到 stop 之前 |
| `:` | 整段 |
| `:3` | 从开头到 3 之前 |
| `1:` | 从 1 到结尾 |
| `::2` | 每隔一个位置选一次 |

slicing 问的是：`要保留哪一段区间？`

下面的图示展示了一维数组里 `start:stop:step` 的读取方式。

![Slice notation selects a range from start to stop before the stop position](/AiBook/assets/part-02/chapter-11/slice-start-stop-step-zh.svg)

这里重要的是：`stop` 位置上的值不会被选中。`scores[1:5:2]` 的意思是从位置 1 开始，到位置 5 之前结束，并且每次走两步。

问题场景：一次比较多种 `start:stop:step` 组合如何得到不同结果。
输入(input)：一个包含六个分数的数组和若干切片表达式。
期待输出(output)：依次打印连续区间、每隔一项的区间、前半段、后半段。
要确认的概念：看到 slicing 能同时控制区间的起点、终点和步长。

```python
# 这个例子按位置、切片和轴选择并汇总 NumPy 数组中的值。
scores = np.array([82, 75, 45, 90, 61, 70])

print(scores[1:5])
print(scores[1:5:2])
print(scores[:3])
print(scores[-2:])
```

输出如下。

```text
[75 45 90 61]
[75 90]
[82 75 45]
[61 70]
```

## 怎样切行与列

在二维数组里，使用 `:` 可以选整行或整列。

问题场景：在同一个二维数组里，分别选出一整行和一整列。
输入(input)：3 行 4 列数组 `data`，以及 `data[2, :]`、`data[:, 3]`。
期待输出(output)：打印第三整行和第四整列。
要确认的概念：看到 `:` 表示该轴上的完整区间，并且行选择与列选择要分开理解。

```python
# 这个例子按位置、切片和轴选择并汇总 NumPy 数组中的值。
data = np.array([
    [10, 11, 12, 13],
    [20, 21, 22, 23],
    [30, 31, 32, 33],
])

print(data[2, :])
print(data[:, 3])
```

输出如下。

```text
[30 31 32 33]
[13 23 33]
```

`data[2, :]` 会选择第 2 行的全部列。

`data[:, 3]` 会从所有行里选择第 3 列。

下面的图示展示了：同一个数组，如何通过 indexing、行 slicing、列 slicing 读出不同部分。

![Indexing, slicing, and axis read different parts of the same array](/AiBook/assets/part-02/chapter-11/index-slice-axis-map-zh.svg)

在这张图里，蓝色强调一个值，绿色强调一行，橙色强调一列。它们都来自同一个数组。

## 也可以切出一个小区域

如果同时指定行区间和列区间，就能得到一个小的 sub-array。

问题场景：在二维数组中，同时指定行区间和列区间，只保留一个小矩形区域。
输入(input)：数组 `data` 和切片 `data[0:2, 1:3]`。
期待输出(output)：打印一个 2 行 2 列的部分数组。
要确认的概念：看到 slicing 可以同时跨多个轴选择区间。

```python
# 这个例子按位置、切片和轴选择并汇总 NumPy 数组中的值。
print(data[0:2, 1:3])
```

输出如下。

```text
[[11 12]
 [21 22]]
```

`data[0:2, 1:3]` 可以读成：`从第 0 行到第 2 行之前`，以及 `从第 1 列到第 3 列之前`。

所以最终留下的是第 0、1 行和第 1、2 列。

一开始可以先把 slicing 理解为“读取需要的范围”，而不是“改变整个原始数组”。至于 slicing 结果如何与原始数组保持连接，会在 P2-11.4 的补充学习里再看。

## Axis 决定计算方向

NumPy glossary 把 axis 解释为数组的一个维度。轴从左到右编号，`axis 0` 是 shape 元组中的第一个元素。在二维数组里，`axis 0` 通常表示行方向，`axis 1` 表示列方向。

这里可以这样理解。

问题场景：看二维数组的 `shape`，确认轴编号分别代表什么。
输入(input)：3 行 4 列数组 `data` 的 `shape`。
期待输出(output)：打印 `(3, 4)`。
要确认的概念：看到把 `axis=0` 读成第一维、`axis=1` 读成第二维，这种解释与 `shape` 是连在一起的。

```python
# 这个例子按位置、切片和轴选择并汇总 NumPy 数组中的值。
data.shape
```

如果结果是 `(3, 4)`，就可以这样读。

| 轴 | 在 shape 中的位置 | 本例中的含义 |
| --- | --- | --- |
| `axis=0` | 第一个数字 `3` | 3 行 |
| `axis=1` | 第二个数字 `4` | 4 列 |

axis 在 `sum`、`mean` 这类汇总计算里尤其重要。

问题场景：比较对同一个数组沿不同 axis 求和时，结果如何变化。
输入(input)：3 行 4 列数组 `data`，以及 `sum(axis=0)`、`sum(axis=1)`。
期待输出(output)：分别打印按列求和的数组与按行求和的数组。
要确认的概念：看到 axis 不是位置编号，而是计算方向，而且结果 `shape` 也会变化。

```python
# 这个例子按位置、切片和轴选择并汇总 NumPy 数组中的值。
print(data.sum(axis=0))
print(data.sum(axis=1))
```

输出如下。

```text
[60 63 66 69]
[ 46  86 126]
```

`sum(axis=0)` 是沿着行方向向下相加，因此会为每一列留下一个和。

`sum(axis=1)` 是沿着列方向横向相加，因此会为每一行留下一个和。

下面的图示展示了：根据 axis 的不同，哪个方向会被折叠，最终留下什么结果。

![Axis controls the direction of reduction](/AiBook/assets/part-02/chapter-11/axis-reduction-zh.svg)

重要的是，`axis=0` 并不表示 `选择第 0 行`。在 indexing 中，`0` 是选择位置的数字；但在 `axis=0` 中，它表示计算沿哪一个维度进行。

## 行常常读成 Sample，列常常读成 Feature

在 AI 实践里，二维数组经常会这样读。

| 方向 | 常见解读 |
| --- | --- |
| row | sample，一条数据 |
| column | feature，变量 |

例如，看下面这个数组。

问题场景：在一个可以按数据集来读的数组里，分别取出一个 sample 和一个 feature 列。
输入(input)：可以读成 3 个 sample、2 个 feature 的 `features` 数组。
期待输出(output)：没有打印输出，但已经准备好一个 sample-feature 结构的例子。
要确认的概念：看到二维数组常常是把行读成 sample，把列读成 feature。

```python
# 这个例子按位置、切片和轴选择并汇总 NumPy 数组中的值。
features = np.array([
    [1.0, 0.2],
    [0.8, 0.4],
    [0.3, 0.9],
])
```

这个数组可以读成 3 个 sample 和 2 个 feature。

问题场景：在这个类似数据集的数组里，立即取出一个 sample 和一个 feature 列。
输入(input)：3 行 2 列的 `features` 数组，以及 `features[0, :]` 和 `features[:, 1]`。
期待输出(output)：打印完整第一个 sample，以及完整第二个 feature 列。
要确认的概念：看到即使是同一个数组，选行与选列对应的也是不同问题。

```python
# 这个例子按位置、切片和轴选择并汇总 NumPy 数组中的值。
print(features[0, :])
print(features[:, 1])
```

第一行代码取出的是第一个 sample。

第二行代码取出的是所有 sample 的第二个 feature。

这种直觉在后面处理 dataset 时很重要。送入模型之前，必须先决定：`哪一行是一条案例？`、`哪一列是一个 feature？`

再简短地收束一次，就是下面这样。

| 在 NumPy array 里看到的东西 | 换成数据集语言再读时 |
| --- | --- |
| 一行 | 一个 sample |
| 一列 | 一个完整 feature |
| `shape[0]` | sample 数 |
| `shape[1]` | feature 数 |

先抓住这张表，后面在 Pandas 与机器学习文档里看到 `X.shape`、`sample`、`feature matrix` 这类表达时，就会少很多陌生感。

下面的图示把同样的视角呈现得更像一个数据集。

![Rows often represent samples and columns often represent features](/AiBook/assets/part-02/chapter-11/dataset-row-column-selection-zh.svg)

这里 `features[1, :]` 的代码，是取出一个 sample 的全部 feature。相反，`features[:, 1]` 是从所有 sample 中取出同一个 feature。

问题场景：在更接近真实数据集的形状中，依次确认一个 sample、一个 feature 列以及它们的平均值。
输入(input)：4 行 3 列的 `features` 数组，以及 `features[1, :]`、`features[:, 1]`、`mean()`。
期待输出(output)：打印第二个 sample、完整第二个 feature 列，以及它的平均值。
要确认的概念：看到选一行表示一条案例，选一列表示一个完整 feature，并且这会直接连接到后面的统计计算。

```python
# 这个例子按位置、切片和轴选择并汇总 NumPy 数组中的值。
features = np.array([
    [1.0, 0.2, 7.0],
    [0.8, 0.4, 6.5],
    [0.3, 0.9, 8.1],
    [0.5, 0.1, 5.8],
])

print(features[1, :])
print(features[:, 1])
print(features[:, 1].mean())
```

输出如下。

```text
[0.8 0.4 6.5]
[0.2 0.4 0.9 0.1]
0.4
```

在这个例子里，最后一行是在计算第二个 feature 的平均值。也就是说，`选择一列` 会直接连到后面的平均值、方差、归一化、feature 比较等工作。

## 示例代码文件

本节示例代码也可以在下面这个文件里查看。

- [p2_11_2_index_slice_axis.py](/AiBook/assets/part-02/chapter-11/p2_11_2_index_slice_axis.py)

在本地 PC 上，可以在项目根目录这样运行。

```bash
python docs/assets/part-02/chapter-11/p2_11_2_index_slice_axis.py
```

在 Colab 里，可以把文件内容贴到代码单元里运行。

输出也包含一维 slicing 的 `start:stop:step` 例子，以及数据集形状中行列选择的例子。

## 结合案例来看

### 案例 1. 你是想看一个学生的分数、一整列科目，还是沿某个轴的汇总？

假设你在看一个成绩矩阵时，读取方式会因问题不同而变化：你可能只想看第二个学生的分数，想看整列数学成绩，或者想看像地区平均那样沿某个 axis 的汇总。人眼扫表时会自然这样做，但在数组计算里，必须把 indexing、slicing、axis 明确写出来。

`data[1, :]` 选的是第二个学生对应的一整行，`data[:, 2]` 选的是第三整列。`sum(axis=0)` 会沿着行方向向下累加，留下按列汇总的结果；`sum(axis=1)` 会在每一行内部相加，留下按学生汇总的结果。

这个案例说明，axis 不是简单的编号，而是决定 `沿哪个方向去读取和计算` 的标准。即使面对同一个数组，只要问题变成 `要看一个案例吗`、`要看一个完整变量吗`、`要看每个方向的汇总吗`，代码就会跟着变化。

所以 indexing 与 slicing 不只是语法，而是把问题放到数组上的方法。只有具备这种直觉，Pandas 的行列选择和 NumPy 的 axis 计算才能顺畅连起来。

尤其在进入 Part 3 之前，应该能马上说出下面这句话。

- `行(row)通常表示 sample，列(column)通常表示 feature，而 shape 会一起显示 sample 数与 feature 数。`

## 检查清单

- 能说明 NumPy 的索引从 0 开始。
- 能用行与列的方式读懂 `data[1, 2]`。
- 能说明 `data[2, :]` 与 `data[:, 3]` 的差别。
- 能说明 `data[0:2, 1:3]` 会选出哪一个部分数组。
- 能说明为什么 `sum(axis=0)` 与 `sum(axis=1)` 的结果不同。
- 能说明“行是 sample，列是 feature”的数据集视角。
- 看到 `shape = (4, 3)` 时，能把它读成类似 `4 个 sample、3 个 feature`。
- 能说明 indexing 选择位置、slicing 保留区间、axis 决定计算方向。

## 来源与参考资料

- NumPy Developers, [Indexing on ndarrays](https://numpy.org/doc/stable/user/basics.indexing.html){: target="_blank" rel="noopener noreferrer" }, NumPy v2.5 Manual，确认日期：2026-07-20。用于确认 basic indexing、slicing、多维索引、advanced indexing 以及 copy/view 注意点。
- NumPy Developers, [NumPy glossary](https://numpy.org/doc/stable/glossary.html){: target="_blank" rel="noopener noreferrer" }, NumPy v2.5 Manual，确认日期：2026-07-20。用于把 axis、broadcasting、copy、view 等术语与本节术语说明对齐。
