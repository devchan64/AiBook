# P2-11.3 广播与向量化

> Section ID: `P2-11.3`
> Version: `v2026.09.15`

## 标量与数组计算

NumPy 将广播描述为不同形状数组参与算术运算的规则。计算时，较小数组被视为具有与较大数组兼容的形状。

广播让不同形状的数组应用共同的计算规则。

给 `[82, 75, 45]` 中每个分数加 10 或乘 2，分别得到 `[92, 85, 55]` 与 `[164, 150, 90]`。

```python
import numpy as np

scores = np.array([82, 75, 45])

print(scores + 10)
print(scores * 2)
```

输出：

```text
[92 85 55]
[164 150  90]
```

`10` 和 `2` 是标量。NumPy 将标量应用到数组的每个位置。

下图展示标量如何应用到整个数组。这是计算规则，不意味着必须在物理内存中复制多份标量。

```mermaid
--8<-- "assets/part-02/chapter-11/broadcast-scalar-array-zh.mmd"
```

## 添加各特征偏移量

广播不能强行匹配任意数组，形状必须兼容。

把四个样本各自的三个特征放进矩阵，按特征加上 `[0.1, 0.2, 0.3]`。第一个样本从 `[1.0, 0.2, 7.0]` 变成 `[1.1, 0.4, 7.3]`。

```python
features = np.array([
    [1.0, 0.2, 7.0],
    [0.8, 0.4, 6.5],
    [0.3, 0.9, 8.1],
    [0.5, 0.1, 5.8],
])

feature_offset = np.array([0.1, 0.2, 0.3])

print(features.shape)
print(feature_offset.shape)
print(features + feature_offset)
```

输出：

```text
(4, 3)
(3,)
[[1.1 0.4 7.3]
 [0.9 0.6 6.8]
 [0.4 1.1 8.4]
 [0.6 0.3 6.1]]
```

本例以行为样本、列为特征，所以 `(4, 3)` 表示四个样本、三个特征。

`feature_offset` 的形状为 `(3,)`，表示每个特征对应一个加数。

NumPy 把 `(3,)` 数组应用到每一行，让各样本的三个特征加上相同的偏移量。

下图展示 `(3,)` 向量如何逐行应用到 `(4, 3)` 矩阵。

```mermaid
--8<-- "assets/part-02/chapter-11/broadcast-row-vector-zh.mmd"
```

## 形状兼容性

给同一矩阵加长度为四的向量，会产生 `ValueError`。虽然行数为四，但最后一个维度的列数是三。

```python
bad_offset = np.array([10, 20, 30, 40])

print(features.shape)
print(bad_offset.shape)
print(features + bad_offset)
```

这段代码会报错：

```text
ValueError: operands could not be broadcast together with shapes (4,3) (4,)
```

`features` 的形状为 `(4, 3)`，每行三个特征；`bad_offset` 为 `(4,)`。长度虽然与行数相同，却与每行的三列不匹配。

| 计算 | 读法 | 结果 |
| --- | --- | --- |
| `(4, 3) + scalar` | 所有位置应用同一个值 | 可行 |
| `(4, 3) + (3,)` | 每行应用长度为三的向量 | 可行 |
| `(4, 3) + (4,)` | 长度四与三列不匹配 | 错误 |

广播从最后一个维度开始比较。对应大小必须相等，或其中一个为 1；缺少的前导维度视为 1。`(4, 3)` 与 `(3,)` 的末尾大小相同，而 `(4, 3)` 与 `(4,)` 在 3 和 4 处冲突。

## 循环与数组运算

向量化用数组运算表达计算，而不在代码中显式写出逐项循环。

例如，用 Python 循环给每个分数加 10：

```python
scores = [82, 75, 45]

adjusted = []
for score in scores:
    adjusted.append(score + 10)

print(adjusted)
```

循环输出 `[92, 85, 55]`。换成 NumPy 数组后，`scores + 10` 计算相同的三个值。

```python
scores = np.array([82, 75, 45])
adjusted = scores + 10

print(adjusted)
```

两者都给每个分数加 10，区别在于表达方式。

| 方法 | 代码结构 | 理解方式 |
| --- | --- | --- |
| Python 循环 | 逐个取出并处理数值 | 显式写出过程 |
| NumPy 向量化 | 对整个数组应用运算 | 用数组表达同一计算 |

NumPy 文档说明，广播支持向量化，使循环在 C 层而非 Python 层进行。向量化不等于重复运算消失。

下图比较同一计算的循环表达与数组表达。

```mermaid
--8<-- "assets/part-02/chapter-11/loop-to-vectorization-flow-zh.mmd"
```

## 减去各特征平均值

减去各特征的平均值，是 AI 数据处理中常见的操作，也是让特征均值接近零的中心化步骤。

四个样本的各列均值为 `[0.65, 0.4, 6.85]`。从每行减去它们后，第一行变为 `[0.35, -0.2, 0.15]`。

```python
features = np.array([
    [1.0, 0.2, 7.0],
    [0.8, 0.4, 6.5],
    [0.3, 0.9, 8.1],
    [0.5, 0.1, 5.8],
])

column_mean = features.mean(axis=0)
centered = features - column_mean

print(column_mean)
print(centered)
```

输出如下，可能有浮点显示差异：

```text
[0.65 0.4  6.85]
[[ 0.35 -0.2   0.15]
 [ 0.15  0.   -0.35]
 [-0.35  0.5   1.25]
 [-0.15 -0.3  -1.05]]
```

`features.mean(axis=0)` 计算各列均值，形状为 `(3,)`；原数组 `features` 的形状为 `(4, 3)`。

`features - column_mean` 从 `(4, 3)` 中减去 `(3,)`，把均值向量应用到每一行。

| 代码 | 形状 | 含义 |
| --- | --- | --- |
| `features` | `(4, 3)` | 四个样本、三个特征 |
| `features.mean(axis=0)` | `(3,)` | 各特征均值 |
| `features - column_mean` | `(4, 3)` | 从每个样本减去各特征均值 |

中心化后的各列均值在浮点误差范围内为零。改用 `axis=1` 会生成形状为 `(4,)` 的四个行均值，使同一减法失败。

## 行均值与 keepdims

要从每名学生的科目分数中减去该学生的平均分，需把行均值保留为 `(学生数, 1)`。`keepdims=True` 把归约轴保留为长度 1，而不是删除它。

```python
marks = np.array([[80, 70, 90], [60, 90, 75]])
row_mean = marks.mean(axis=1, keepdims=True)
row_centered = marks - row_mean

print(row_mean.shape)
print(row_centered)
print(row_centered.mean(axis=1))
```

```text
(2, 1)
[[  0. -10.  10.]
 [-15.  15.   0.]]
[0. 0.]
```

省略 `keepdims` 后，均值形状为 `(2,)`，不能直接从 `(2, 3)` 中相减。三行三列的方阵减去 `(3,)` 可能成功，但这些值按列位置而非按行应用。没有报错不能证明计算沿预期轴进行；行中心化后，还应确认各行均值接近零。

## 中间数组与内存

广播可以避免重复复制输入，但结果数组仍需内存。`(10000, 1)` 与 `(1, 10000)` 相加，结果为 `(10000, 10000)`。仅保存一亿个 `float64` 元素就需要约 800 MB。因此不仅要看输入大小，还要检查结果形状。

## 示例代码文件

这些示例也可以通过下面文件查看：

- [p2_11_3_broadcast_vectorization.py](/AiBook/assets/part-02/chapter-11/p2_11_3_broadcast_vectorization.py)

在本地，从项目根目录运行：

```bash
python docs/assets/part-02/chapter-11/p2_11_3_broadcast_vectorization.py
```

在 Colab 中，将文件内容粘贴到代码单元。

输出包含标量广播、行向量广播、形状不匹配以及减去特征均值的示例。

## 案例：按科目与按学生调整

两名学生的语文、数学、英语分数为 `[80, 70, 90]` 与 `[60, 90, 75]`。按科目分别加 5、10、0，使用长度三的向量，结果为 `[85, 80, 90]` 与 `[65, 100, 75]`。

```python
marks = np.array([[80, 70, 90], [60, 90, 75]])
subject_bonus = np.array([5, 10, 0])
student_bonus = np.array([[5], [10]])

print(marks + subject_bonus)
print(marks + student_bonus)
```

```text
[[ 85  80  90]
 [ 65 100  75]]
[[ 85  75  95]
 [ 70 100  85]]
```

给第一名学生各科加 5、第二名学生各科加 10，需使用 `(2, 1)` 形状。每行的调整值应用到全部三科。写成 `[5, 10]` 则为 `(2,)`，与最后维度 3 不兼容。

把 `subject_bonus` 第二个值从 10 改为 0，第一组输出中只有数学恢复为 70 和 90。把 `student_bonus` 第二个值改为 0，第二组输出中第二名学生的三科都恢复原值。相同的加法，会因调整值的布局而影响不同对象。

## 检查清单

- 能用广播解释标量与数组计算。
- 能解释 `(4, 3) + (3,)` 为何可行。
- 能解释 `(4, 3) + (4,)` 为何失败。
- 能区分 Python 循环与 NumPy 向量化表达。
- 能解释 `features.mean(axis=0)` 的结果形状。
- 能指出减去特征均值时的广播。
- 能解释广播为何需要检查形状与内存。
- 能否解释逐行中心化为何使用 `keepdims=True`，以及如何检查结果？

## 来源与参考资料

- NumPy Developers, [Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual，确认日期：2026-07-20。作为 broadcasting rules、维度比较和 shape mismatch 错误说明的核心依据。
- NumPy Developers, [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual，确认日期：2026-07-20。用于确认 array arithmetic、universal functions 和基本 axis calculation 示例。
- NumPy Developers, [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual，确认日期：2026-07-20。作为把 Python 循环读成数组级计算并先检查 shape 的入门流程依据。
- NumPy Developers, [numpy.mean](https://numpy.org/doc/stable/reference/generated/numpy.mean.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, 查阅日期: 2026-09-15. 沿轴归约及 keepdims 保留轴.
