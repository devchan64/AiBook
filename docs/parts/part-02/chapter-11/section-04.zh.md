# P2-11.4 补充学习：同时理解 NumPy 的形状与数据共享

> Section ID: `P2-11.4`
> Version: `v2026.09.15`

## 切片与数据共享

基本切片创建与原数组共享数据的视图。把 `scores[1:4]` 的第一个值改为 999，原数组的位置 1 也会变成 999。

```python
import numpy as np

scores = np.array([82, 75, 45, 90, 61])
middle = scores[1:4]

middle[0] = 999

print(scores)
print(middle)
```

输出：

```text
[ 82 999  45  90  61]
[999  45  90]
```

## 位置、条件选择与复制

用位置列表进行花式索引、用布尔掩码按条件读取时，都会复制数据。把 `picked` 第一个值改为 500、`high_scores` 第一个值改为 700，原数组仍是 `[82, 75, 45, 90, 61]`。

```python
scores = np.array([82, 75, 45, 90, 61])

picked = scores[[1, 3, 4]]
high_scores = scores[scores >= 80]

picked[0] = 500
high_scores[0] = 700

print(scores)
print(picked)
print(high_scores)
```

输出：

```text
[82 75 45 90 61]
[500  90  61]
[700  90]
```

`scores[[1, 3, 4]]` 收集位置 1、3、4 的值，称为花式索引。

`scores[scores >= 80]` 使用布尔掩码，选择条件为真的值。

## 添加长度为一的轴

`np.newaxis` 在指定位置添加长度为一的轴。形状为 `(3,)` 的分数数组可以视为 `(3, 1)` 或 `(1, 3)`，结果也与原数组共享数据。

```python
scores = np.array([82, 75, 45])

print(scores.shape)
print(scores[:, np.newaxis].shape)
print(scores[np.newaxis, :].shape)
```

输出：

```text
(3,)
(3, 1)
(1, 3)
```

数值相同，但维数与形状不同。

| 表达式 | 形状 | 读法 |
| --- | --- | --- |
| `scores` | `(3,)` | 长度为三的一维数组 |
| `scores[:, np.newaxis]` | `(3, 1)` | 三行一列，类似列向量 |
| `scores[np.newaxis, :]` | `(1, 3)` | 一行三列，类似行向量 |

`np.newaxis` 不生成新的数值，而是组织数组在计算中的对齐方式。

## 计算所有组合的差

要从 `[10, 20, 30]` 的每个值分别减去 1 和 2，需要三行二列的结果。把输入形状改成 `(3, 1)` 和 `(1, 2)`，即可通过广播计算全部六种组合。

```python
a = np.array([10, 20, 30])
b = np.array([1, 2])

diff = a[:, np.newaxis] - b[np.newaxis, :]

print(a[:, np.newaxis].shape)
print(b[np.newaxis, :].shape)
print(diff)
```

输出：

```text
(3, 1)
(1, 2)
[[ 9  8]
 [19 18]
 [29 28]]
```

第一行 `[9, 8]` 是 10 减去 1 和 2，最后一行 `[29, 28]` 是 30 减去两值。把 `b` 改成 `[1, 5]`，只会把第二列改为 `[5, 15, 25]`。不添加轴而直接计算 `a - b`，会因 `(3,)` 与 `(2,)` 不兼容而失败。

## reshape 与转置

`reshape` 把元素重新组织成新形状；二维数组的 `.T` 交换行轴与列轴。两者都能得到 `(3, 2)`，但数值排列不同。

```python
matrix = np.array([[10, 11, 12], [20, 21, 22]])
print(matrix.reshape(3, 2))
print(matrix.T)
```

```text
[[10 11]
 [12 20]
 [21 22]]
[[10 20]
 [11 21]
 [12 22]]
```

如果原来的行代表学生，转置后就是列代表学生。`reshape(3, 2)` 不会自动保留这一含义。一维 `(3,)` 数组经 `.T` 后仍为 `(3,)`；需要列向量形状时，应使用 `[:, np.newaxis]`。

`reshape` 尽可能返回视图，但内存布局可能要求复制。下面的小例子检查实际数据共享情况。

```python
matrix = np.array([[10, 11, 12], [20, 21, 22]])
reshaped = matrix.reshape(3, 2)
transposed_flat = matrix.T.reshape(-1)

print(np.shares_memory(matrix, reshaped))
print(np.shares_memory(matrix, transposed_flat))
```

输出为 `True`、`False`。`-1` 表示根据元素数量推断该轴长度。按默认顺序展平这个转置数组需要复制。不能认定所有 reshape 都是视图或都是副本；需要保留原数组再修改时，应显式使用 `.copy()`。

## 案例：只调整选中的分数

从 `[82, 75, 45, 90, 61]` 中选择位置 1 到 3，各加 10。直接修改切片也会改变原数组。需要独立比较调整前后的值时，用 `.copy()` 复制选中区间。

```python
scores = np.array([82, 75, 45, 90, 61])
adjusted = scores[1:4].copy()
adjusted += 10

print(scores)
print(adjusted)
```

```text
[82 75 45 90 61]
[ 85  55 100]
```

去掉 `.copy()` 并重跑整个示例，原数组也会变成 `[82, 85, 55, 100, 61]`。如果作为“调整前”基准的数据也改变了，前后比较就不再使用原始基准。

条件选择返回副本，是指**读取并存入新变量**时。`scores[scores < 60] = 60` 这类直接赋值会修改原数组相应位置；先读取 `low = scores[scores < 60]`，再执行 `low[:] = 60`，则不会改变原数组。

```mermaid
--8<-- "assets/part-02/chapter-11/shape-view-broadcast-flow-zh.mmd"
```

## 示例代码文件

依次运行示例，比较不同选择方式对原数组和形状的影响。

- [p2_11_4_views_shapes.py](/AiBook/assets/part-02/chapter-11/p2_11_4_views_shapes.py)

```bash
python docs/assets/part-02/chapter-11/p2_11_4_views_shapes.py
```

## 检查清单

- 能否区分 `x[1:4]` 与 `x[[1, 3, 4]]`？
- 能否解释布尔掩码选择什么？
- 能否区分 `(3,)`、`(3, 1)` 和 `(1, 3)`？
- 能否解释 `np.newaxis` 与广播的关系？
- 保留原数据时，是否检查需要复制？
- 阅读 NumPy 代码时，能否同时检查形状与数据共享？
- 能否区分 reshape 与转置的值排列，并用 `np.shares_memory` 检查内存共享？

## 来源与参考资料

- NumPy Developers, [Copies and views](https://numpy.org/doc/stable/user/basics.copies.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual，确认日期：2026-07-20。作为区分 view 与 copy、basic indexing views、advanced indexing copies 和 `.base` 检查的依据。
- NumPy Developers, [Indexing on ndarrays](https://numpy.org/doc/stable/user/basics.indexing.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual，确认日期：2026-07-20。用于确认 selection method 会影响 shape 以及是否共享原始数据。
- NumPy Developers, [Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual，确认日期：2026-07-20。作为把 `np.newaxis` 和 shape adjustment 连接到 broadcasting 的依据。
- NumPy Developers, [numpy.shares_memory](https://numpy.org/doc/stable/reference/generated/numpy.shares_memory.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, 查阅日期: 2026-09-15. 小数组示例中的内存共享检查.
