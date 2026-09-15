# P2-11.2 索引、切片与轴

> Section ID: `P2-11.2`
> Version: `v2026.09.15`

## 选择位置

NumPy 数组使用标准 Python 索引语法 `x[obj]`，与 Python 一样从零开始编号。

先看一维数组。

在 `[82, 75, 45, 90]` 中，索引 `0` 和 `2` 选择第一个值 `82` 与第三个值 `45`。

```python
import numpy as np

scores = np.array([82, 75, 45, 90])

print(scores[0])
print(scores[2])
```

输出：

```text
82
45
```

`scores[0]` 是第一个值，`scores[2]` 是第三个值。Python 和 NumPy 的第一个位置编号为 0，而不是 1。

| 表达式 | 读法 | 结果 |
| --- | --- | --- |
| `scores[0]` | 位置 0 | `82` |
| `scores[1]` | 位置 1 | `75` |
| `scores[2]` | 位置 2 | `45` |
| `scores[-1]` | 最后一个位置 | `90` |

索引回答选择哪个位置的问题。

## 行与列的位置

二维数组通常同时指定行与列。

在三行四列数组中，`[1, 2]` 选择第二行的第三个值。下面代码输出形状 `(3, 4)` 和数值 `22`。

```python
data = np.array([
    [10, 11, 12, 13],
    [20, 21, 22, 23],
    [30, 31, 32, 33],
])

print(data.shape)
print(data[1, 2])
```

输出：

```text
(3, 4)
22
```

`data[1, 2]` 选择行索引 1、列索引 2 的值。

这里的索引也从零开始。

| 表达式 | 读法 | 结果 |
| --- | --- | --- |
| `data[0, 0]` | 行 0，列 0 | `10` |
| `data[0, 3]` | 行 0，列 3 | `13` |
| `data[1, 2]` | 行 1，列 2 | `22` |
| `data[2, 1]` | 行 2，列 1 | `31` |

逗号分隔不同维度，二维选择可以读作 `data[行, 列]`。

## 区间与步长

切片选择区间，而不是单个位置。

从四个分数中选择 `1:3`，保留位置 1 和 2，得到 `[75 45]`。

```python
scores = np.array([82, 75, 45, 90])

print(scores[1:3])
```

输出：

```text
[75 45]
```

`1:3` 从位置 1 开始，到位置 3 之前结束，选择位置 1 和 2。

区间记法：

| 表达式 | 含义 |
| --- | --- |
| `start:stop` | 从 start 到 stop 之前 |
| `:` | 全部位置 |
| `:3` | 从开头到 3 之前 |
| `1:` | 从 1 到末尾 |
| `::2` | 每次移动两个位置 |

切片回答保留哪个区间的问题。

下图展示 `start:stop:step` 如何在一维数组中进行选择。

```mermaid
--8<-- "assets/part-02/chapter-11/slice-start-stop-step-zh.mmd"
```

`stop` 位置的值不包含在结果内。`scores[1:5:2]` 从 1 开始，每次移动两个位置，在 5 之前停止。

对六个分数，分别选择连续区间、间隔两个位置、前三项和后两项，输出为 `[75 45 90 61]`、`[75 90]`、`[82 75 45]`、`[61 70]`。

```python
scores = np.array([82, 75, 45, 90, 61, 70])

print(scores[1:5])
print(scores[1:5:2])
print(scores[:3])
print(scores[-2:])
```

输出：

```text
[75 45 90 61]
[75 90]
[82 75 45]
[61 70]
```

## 整行与整列

在二维数组中，用 `:` 选择整行或整列。

选择同一个 `(3, 4)` 数组的第三行和第四列，结果是 `[30 31 32 33]` 与 `[13 23 33]`。

```python
data = np.array([
    [10, 11, 12, 13],
    [20, 21, 22, 23],
    [30, 31, 32, 33],
])

print(data[2, :])
print(data[:, 3])
```

输出：

```text
[30 31 32 33]
[13 23 33]
```

`data[2, :]` 选择行 2 的所有列。

`data[:, 3]` 从所有行中选择列 3。

下图比较从同一数组中选择单值、整行与整列。

```mermaid
--8<-- "assets/part-02/chapter-11/index-slice-axis-map-zh.mmd"
```

这些选择来自同一个原数组，但会产生不同的结果形状。

## 整数选择与保留轴

`data[1, :]` 选择一行并删除行轴；`data[1:2, :]` 保留只有一行的区间，因此保留长度为 1 的行轴。值看似相同，传给后续运算的形状却不同。

```python
print(data[1, :].shape)
print(data[1:2, :].shape)
print(data[:, 2].shape)
print(data[:, 2:3].shape)
```

输出是 `(4,)`、`(1, 4)`、`(3,)` 和 `(3, 1)`。后续运算需要同时保留行列轴时，可以用长度为 1 的切片代替整数选择。

`data[99, :]` 因该行不存在而产生 `IndexError`；`data[99:, :]` 则返回形状为 `(0, 4)` 的空数组。切片边界会限制在可用范围内，因此没有报错不代表结果中仍有数据。

## 子数组

同时指定行列区间，可以得到较小的子数组。

从 `data` 中选择行 `0:2`、列 `1:3`，得到二行二列数组 `[[11, 12], [21, 22]]`。

```python
print(data[0:2, 1:3])
```

输出：

```text
[[11 12]
 [21 22]]
```

`data[0:2, 1:3]` 表示从行 0 到行 2 之前，从列 1 到列 3 之前。

保留行 0、1 和列 1、2。

基本切片返回与原数组共享数据的视图。修改这个子数组也会影响原数组。需要独立数组时，对切片结果调用 `.copy()`。

## 按轴求和

NumPy 用轴表示数组的维度。轴按 shape 元组中的位置编号，轴 0 对应第一项。在二维数组中，轴 0 对应行，轴 1 对应列。

前面的 `data` 形状为 `(3, 4)`。shape 的每一项表示对应轴的长度。

```python
print(data.shape)
```

可以这样理解 `(3, 4)`：

| 轴 | shape 中的位置 | 本例含义 |
| --- | --- | --- |
| `axis=0` | 第一个数 `3` | 三行 |
| `axis=1` | 第二个数 `4` | 四列 |

轴对于 `sum`、`mean` 等汇总运算尤其重要。

沿 `axis=0` 求和得到各列合计 `[60 63 66 69]`；沿 `axis=1` 求和得到各行合计 `[46 86 126]`。

```python
print(data.sum(axis=0))
print(data.sum(axis=1))
```

输出：

```text
[60 63 66 69]
[ 46  86 126]
```

`sum(axis=0)` 沿各行向下合并数值，每列留下一个合计。

`sum(axis=1)` 沿各列横向合并数值，每行留下一个合计。

下图展示被归约的轴与保留下来的结果形状。

```mermaid
--8<-- "assets/part-02/chapter-11/axis-reduction-zh.mmd"
```

`axis=0` 并非选择行 0。索引指定位置，axis 参数指定计算沿哪个维度进行。

## 样本与特征

AI 示例常这样理解二维数组：

| 方向 | 常用解释 |
| --- | --- |
| 行 | 样本，一条记录 |
| 列 | 特征，变量 |

例如，把三个样本各自的两个特征放进矩阵。每行代表一个样本，准备代码不显示输出。

```python
features = np.array([
    [1.0, 0.2],
    [0.8, 0.4],
    [0.3, 0.9],
])
```

这个数组可以解释为三个样本、两个特征。

第一个样本为 `[1.0, 0.2]`，所有样本的第二个特征为 `[0.2, 0.4, 0.9]`。下面代码输出这两个数组。

```python
print(features[0, :])
print(features[:, 1])
```

第一行代码取出第一个样本。

第二行代码取出所有样本的第二个特征。

模型输入必须定义每行代表哪个案例、每列代表哪个特征，形状本身不能提供这些含义。

| NumPy 视角 | 数据集解释 |
| --- | --- |
| 一行 | 一个样本 |
| 一列 | 所有样本的一个特征 |
| `shape[0]` | 样本数 |
| `shape[1]` | 特征数 |

下图将这一视角用于数据集形状的数组。

```mermaid
--8<-- "assets/part-02/chapter-11/dataset-row-column-selection-zh.mmd"
```

`features[1, :]` 取出一个样本的所有特征，`features[:, 1]` 取出所有样本的同一个特征。

从四个样本、每样本三个特征的数组中，选择第二个样本和第二个特征列。最后输出该特征的平均值 `0.4`。

```python
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

输出：

```text
[0.8 0.4 6.5]
[0.2 0.4 0.9 0.1]
0.4
```

最后一行计算第二个特征的平均值。选择一列之后，可以继续求平均、方差、归一化或比较特征。

## 示例代码文件

这些示例也可以通过下面文件查看：

- [p2_11_2_index_slice_axis.py](/AiBook/assets/part-02/chapter-11/p2_11_2_index_slice_axis.py)

在本地，从项目根目录运行：

```bash
python docs/assets/part-02/chapter-11/p2_11_2_index_slice_axis.py
```

在 Colab 中，把文件内容粘贴到代码单元执行。

输出还包括一维 `start:stop:step` 切片和数据集形式的行列选择。

## 案例：学生总分与科目合计

两名学生的语文、数学、英语分数分别为 `[80, 70, 90]` 和 `[60, 90, 75]`。下面代码输出第二名学生、数学列、各科合计和学生总分。

```python
import numpy as np

marks = np.array([[80, 70, 90], [60, 90, 75]])
print("second student:", marks[1, :])
print("math:", marks[:, 1])
print("subject totals:", marks.sum(axis=0))
print("student totals:", marks.sum(axis=1))
```

```text
second student: [60 90 75]
math: [70 90]
subject totals: [140 160 165]
student totals: [240 225]
```

科目合计沿学生轴求和，结果形状为 `(3,)`；学生总分沿科目轴求和，形状为 `(2,)`。把第二名学生的数学从 90 改为 100，合计分别变为 `[140, 170, 165]` 与 `[240, 235]`。只有数学合计和第二名学生总分增加 10。

## 检查清单

- 能解释 NumPy 索引从零开始。
- 能按行列理解 `data[1, 2]`。
- 能区分 `data[2, :]` 与 `data[:, 3]`。
- 能识别 `data[0:2, 1:3]` 选择的子数组。
- 能解释 `sum(axis=0)` 与 `sum(axis=1)` 为何不同。
- 在相应定义下，能把行理解为样本、列理解为特征。
- 能在该布局下把 `(4, 3)` 理解为四个样本、三个特征。
- 能区分位置选择、区间保留与归约轴选择。
- 能否预测整数索引与长度为 1 的切片在形状上的差异？

## 来源与参考资料

- NumPy Developers, [Indexing on ndarrays](https://numpy.org/doc/stable/user/basics.indexing.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual，确认日期：2026-07-20。用于确认 basic indexing、slicing、多维索引、advanced indexing 以及 copy/view 注意点。
- NumPy Developers, [NumPy glossary](https://numpy.org/doc/stable/glossary.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual，确认日期：2026-07-20。用于把 axis、broadcasting、copy、view 等术语与本节术语说明对齐。
