# P2-11.4 补充学习：在 NumPy 中一起读取 shape 与原数组共享

> Section ID: `P2-11.4`
> Version: `v2026.07.11`

在 P2-11.2 中，我们看了 indexing、slicing、axis；在 P2-11.3 中，我们看了 broadcasting 和 vectorization。但在真正读 NumPy 代码时，后面常常还会卡在几个问题上。

`这个选择还在看原数组吗？`
`还是说它新建了一个数组？`
`为什么 shape 会突然从 (3,) 变成 (3, 1)？`

这篇补充学习就是把这些问题绑在一起处理。

这里提供一个基础说明，把 `boolean mask`、`fancy indexing`、`np.newaxis`、`shared view` 放在同一条线上来看。即使前面几节里的 indexing、slicing、broadcasting 大体已经能读懂，这里仍然要重新接上：选择方式和 shape 变化是怎样连到原数组共享问题上的。

## 本补充学习的范围

本节以入门层级整理：在 NumPy 中，slicing、boolean mask、fancy indexing、`np.newaxis` 会怎样影响数组的 `shape` 与是否共享原数组。

这里回答以下问题。

- basic slicing 和 fancy indexing 有什么不同？
- boolean mask 选的是什么？
- 为什么有些选择会和原数组一起变化，有些却分开变化？
- 为什么要用 `np.newaxis`？
- 在读 broadcasting 时，为什么要把 shape 与原数组共享一起看？

本节不深入 NumPy 的内部内存布局、stride 计算细节、完整的高级 broadcasting 规则、性能基准，或大型 tensor 库的内部实现。这里只回收一个标准：`选择方式不同，shape 与是否共享原数组也会跟着不同`。

## 本补充学习的目标

- 能说明 basic slicing 常常可以读成“在看原数组的一部分”。
- 能说明 fancy indexing 与 boolean mask 常常可以读成“创建了一个新数组”。
- 能说明即使 shape 看起来相似，是否共享原数组也可能不同。
- 能把 `np.newaxis` 解释成“增加一个长度为 1 的轴”的写法。
- 能说明在读 broadcasting 代码时，要把 `值`、`shape`、`是否共享原数组` 一起检查。

## 先抓住的一个画面

这篇补充学习里最先要抓住的画面是：`怎样选择` 与 `怎样改变 shape`，会一起改变“是否共享原数组”和“计算沿哪个方向对齐”。

| 代码场景 | 先读什么问题 | 现在要抓住的关键 |
| --- | --- | --- |
| `x[1:4]` | 是不是还在原样看这一段区间？ | 很可能仍共享原数组 |
| `x[[1, 3, 4]]` | 是不是把分散的位置单独收集起来？ | 更安全地把它读成新数组 |
| `x[x >= 80]` | 是不是只筛出满足条件的值？ | 更安全地把它读成新数组 |
| `x[:, np.newaxis]` | 是不是又加了一个轴？ | `shape` 会变化，broadcasting 的读取也会变化 |

也就是说，在 NumPy 里，只说“选了一部分”是不够的。必须先区分 `看区间`、`收集位置`、`按条件筛选`、`添加轴`，这样才能把 view/copy、shape、broadcasting 一起读懂。

## 背景

在 P2-8.7 的补充学习里，我们通过 Python list 与复制先看过一个问题：`原对象会不会一起变？` NumPy 里同样会回到这个问题。但在 NumPy 中，只问“有没有复制”还不够，还要一起问 `shape 是怎么变的？`

例如，`x[1:4]` 与 `x[[1, 3, 4]]` 看起来都像“只选出部分值”，但前者可能还在看原数组，后者则可能已经创建了一个新数组。而 `x[:, np.newaxis]` 即使值没有变化，也会改变整个 broadcasting 的方式。

当 P2-11.2 里的 slicing 与 axis 已经大体能读懂，但你仍会卡在“这个选择会不会把原数组一起改掉”；或者当 P2-11.3 里的 broadcasting 已经能读懂，但碰到 `(3, 1)` 和 `(1, 3)` 突然出现就停住时，就来看这一节。抓住这个标准后，你就能把 slicing、axis、broadcasting 连同 `shape` 与 `是否共享原数组` 一起读。

## 三个标准

| 标准 | 为什么重要 | 本节需要达到的理解程度 |
| --- | --- | --- |
| 选了什么 | 它能避免把 slicing、fancy indexing、mask 混成同一种选择 | 先分清是切区间，还是单独收集某些位置 |
| `shape` 怎么变了 | 它揭示了为什么值看起来相同，计算方式却会变 | 理解 `(3,)`、`(3, 1)`、`(1, 3)` 的差异会改变计算方向 |
| 是否仍共享原数组 | 它能避免后面改值时意外改变实验结果 | 如果可能修改值，就先检查是否需要 copy |

| 术语 | 本节先抓住的含义 |
| --- | --- |
| boolean mask | 只保留条件为真的值的选择方式 |
| fancy indexing | 用一个位置列表指定多个位置，再把值单独收集起来的选择方式 |
| `np.newaxis` | 通过增加长度为 1 的轴来改变数组 shape 的写法 |
| shared view | 选择结果仍和原数组相连，可能一起变化的状态 |
| copy | 创建一个和原数组分离的新数组的方式 |

## Basic Slicing 常常可以读成在看原数组的一部分

在 P2-11.2 中，slicing 被介绍为“保留一个区间”的写法。在 NumPy 里，这种 basic slicing 常常会表现成“仍在看原数组的一部分”。

问题场景：确认当我们修改 slicing 选出的部分时，原数组会不会一起变化。
输入(input)：一维数组 `scores` 与切片 `scores[1:4]`。
期待输出(output)：通过切片改掉的值，会反映回原数组。
要确认的概念：看到 basic slicing 看起来像新数组，但仍可能与原数组相连。

```python
import numpy as np

scores = np.array([82, 75, 45, 90, 61])
middle = scores[1:4]

middle[0] = 999

print(scores)
print(middle)
```

输出如下。

```text
[ 82 999  45  90  61]
[999  45  90]
```

这里可以这样读。

- 只把 `scores[1:4]` 看成“复制出来的三个值”是有风险的。
- basic slicing 常常可以读成仍在看原数组的一部分。
- 所以后面改值时，原数组也可能跟着变。

这种直觉直接连到 P2-8.7 里那个问题：`原对象和复制结果什么时候会一起变化？`

## Fancy Indexing 和 Boolean Mask 会把选中的值重新收集成新结果

现在看一些虽然也像“选一部分”，但工作方式不同的例子。

问题场景：比较“单独挑出几个位置”的 fancy indexing，和“按条件筛选”的 boolean mask，它们与原数组有什么不同。
输入(input)：数组 `scores`、位置列表 `[1, 3, 4]`、条件 `scores >= 80`。
期待输出(output)：即使修改 fancy indexing 和 boolean mask 的结果，原数组 `scores` 也保持不变。
要确认的概念：看到按位置收集或按条件筛选出来的结果，更安全地应读成新数组。

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

输出如下。

```text
[82 75 45 90 61]
[500  90  61]
[700  90]
```

这里，`scores[[1, 3, 4]]` 是把位置 1、3、4 的值单独收集起来。这种方式叫 fancy indexing。

`scores[scores >= 80]` 是只保留条件为真的值。这种方式叫 boolean mask。

这里两者都可以这样理解。

- basic slicing 更接近 `原样查看一段区间`。
- fancy indexing 与 boolean mask 更接近 `把选中的值重新收集起来`。

因此，改值时是否会连动原数组，也会不同。

## 即使都叫“选一部分”，问题本身也不同

slicing、fancy indexing、boolean mask 虽然都像是在“只选一部分值”，但它们实际上回答的是不同问题。

| 表达式 | 先读什么问题 | 入门阶段更安全的解释 |
| --- | --- | --- |
| `x[1:4]` | 要保留哪一段区间？ | 查看区间 |
| `x[[1, 3, 4]]` | 要把哪些位置单独取出来？ | 收集位置 |
| `x[x >= 80]` | 要保留哪些满足条件的值？ | 按条件筛选 |

先把这个区别分开，NumPy 代码就会少很多混乱。

## `np.newaxis` 会增加一个长度为 1 的轴

现在看的是：不是选值，而是改变 `shape` 的写法。

问题场景：仅通过改变 shape，区分同一个一维数组该被看成更像一行还是更像一列。
输入(input)：一维数组 `scores`，以及 `scores[:, np.newaxis]`、`scores[np.newaxis, :]`。
期待输出(output)：打印 `(3,)`、`(3, 1)`、`(1, 3)` 三种 shape。
要确认的概念：看到 `np.newaxis` 不会改变值本身，而是通过增加一个长度为 1 的轴来改变计算方向。

```python
scores = np.array([82, 75, 45])

print(scores.shape)
print(scores[:, np.newaxis].shape)
print(scores[np.newaxis, :].shape)
```

输出如下。

```text
(3,)
(3, 1)
(1, 3)
```

这三个数组看上去装的数字相似，但读取方式不同。

| 表达式 | shape | 读取方式 |
| --- | --- | --- |
| `scores` | `(3,)` | 长度为 3 的一维数组 |
| `scores[:, np.newaxis]` | `(3, 1)` | 像 3 行 1 列的列向量一样去读 |
| `scores[np.newaxis, :]` | `(1, 3)` | 像 1 行 3 列的行向量一样去读 |

所以 `np.newaxis` 不是在创造新数字，而是在整理数组该沿哪个方向去适配计算。

## `np.newaxis` 常用来有意制造 Broadcasting

在 P2-11.3 中，我们看过像 `(4, 3)` 与 `(3,)` 这种本来就兼容的 shape。但有些计算，必须故意多加一个轴，才更容易读。

问题场景：把列方向和行方向分开，一次性计算两个集合之间的差。
输入(input)：长度为 3 的数组 `a` 和长度为 2 的数组 `b`。
期待输出(output)：形状 `(3, 1)` 与 `(1, 2)` 相遇后，产生 `(3, 2)` 的结果。
要确认的概念：看到 `np.newaxis` 是用于 broadcasting 的 shape 对齐工具。

```python
a = np.array([10, 20, 30])
b = np.array([1, 2])

diff = a[:, np.newaxis] - b[np.newaxis, :]

print(a[:, np.newaxis].shape)
print(b[np.newaxis, :].shape)
print(diff)
```

输出如下。

```text
(3, 1)
(1, 2)
[[ 9  8]
 [19 18]
 [29 28]]
```

这个例子的关键不在值，而在 `shape`。

- `a[:, np.newaxis]` 是 `(3, 1)`。
- `b[np.newaxis, :]` 是 `(1, 2)`。
- 两者通过 broadcasting 产生 `(3, 2)` 的结果。

这里可以把 `np.newaxis` 理解成：为了 broadcasting，让行和列角色更明确的写法。

## 在实务代码里，要一起看 Shape 与原数组共享

NumPy 代码之所以容易让人混乱，是因为 `选了什么`、`shape 怎样变化`、`原数组会不会一起变`，常常同时出现在同一行。

因此，更安全的读取习惯如下。

1. 这段代码是在切区间、收集位置，还是按条件筛选？
2. 结果的 `shape` 是什么？
3. 后面会不会修改这个值？
4. 如果必须保留原数组，是否需要 `.copy()`？

这个判断在数据预处理中尤其重要。因为“只是从部分 sample 创建了新数据集”，还是“直接改了原数组的一部分”，会影响你怎样解释实验结果。

把这个流程一次性绑起来，可以得到下面的图。

```mermaid
--8<-- "assets/part-02/chapter-11/shape-view-broadcast-flow-en.mmd"
```

读者在这里至少要留下这句话。

- `怎样选择，会改变是否共享原数组；怎样改变 shape，会改变 broadcasting 的方向。`

## 应该回到哪里去读

读完这一节后，应重新接回下面这些正文。

| 现在重新要读的问题 | 优先回去看的正文 |
| --- | --- |
| 选中的到底是哪一个值或区间？ | P2-11.2 Indexing, Slicing, and Axis |
| 为什么整数组计算会随着 shape 变化？ | P2-11.3 Broadcasting and Vectorization |
| 如果“共享原数组”的直觉本身还陌生 | P2-8.7 references, shallow copy, deep copy |

## 本补充学习要记住的视角

- 在 NumPy 里，是否共享原数组可能会随着选择方式而变化。
- 更安全的读法是：basic slicing 先读成查看区间，fancy indexing 先读成收集位置，boolean mask 先读成按条件筛选。
- `np.newaxis` 是通过增加长度为 1 的轴来显露 broadcasting 方向的写法。
- 读 NumPy 代码时，不要只看值，还要一起看 `shape` 和是否共享原数组。

## 简短复归表

| 卡住的场景 | 先回哪里 |
| --- | --- |
| indexing、slicing、axis 本身还混乱 | `P2-11.2` |
| broadcasting 方向为什么变了仍然模糊 | `P2-11.3` |
| 为什么原数组和复制结果会一起变化仍然陌生 | `P2-8.7` |

## 简短检查

- 能说明 `x[1:4]` 与 `x[[1, 3, 4]]` 的差别吗？
- 能说明 boolean mask 选的是什么吗？
- 能说明 `(3,)`、`(3, 1)`、`(1, 3)` 的差别吗？
- 能说明为什么 `np.newaxis` 和 broadcasting 连在一起吗？
- 还记得在“保留原数组”很重要时，要先检查 `.copy()` 吗？

## 什么时候应先想起这个视角

- 当你不确定 slicing 结果是仍共享原数组，还是已经创建新数组时，就重新想起 shape 与原数组共享的直觉。
- 当你需要检查为什么 `(3,)`、`(3, 1)`、`(1, 3)` 看起来相似却会产生不同计算结果时，就把这一补充节当作标准。
- 当改值意外把原数组也改掉，或在 broadcasting 前需要确认准备好的 shape 时，就回到这里。

## 来源与参考资料

- NumPy documentation, ["Copies and views"](https://numpy.org/doc/stable/user/basics.copies.html){: target="_blank" rel="noopener noreferrer" } (确认日期: 2026-07-01)
- NumPy documentation, ["Indexing on ndarrays"](https://numpy.org/doc/stable/user/basics.indexing.html){: target="_blank" rel="noopener noreferrer" } (确认日期: 2026-07-01)
- NumPy documentation, ["Broadcasting"](https://numpy.org/doc/stable/user/basics.broadcasting.html){: target="_blank" rel="noopener noreferrer" } (确认日期: 2026-07-01)
