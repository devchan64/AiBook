# P2-11.3 广播与向量化

> Section ID: `P2-11.3`
> Version: `v2026.07.11`

在 P2-11.1 中，我们检查了 NumPy array 的 `shape`、`ndim`、`dtype`。在 P2-11.2 中，我们用 indexing、slicing、axis 来决定从数组的哪一部分读取，以及沿哪个方向计算。

现在再往前走一步。在 NumPy 代码里，经常会看到没有直接写循环，却对整个数组都施加了计算。

例如，下面的代码把一个数字加到整个数组上。

问题场景：用最小例子确认，不写循环时是否也能把同一个值加到整个数组上。
输入(input)：一个包含三个分数的数组，以及标量 `10`。
期待输出(output)：打印一个新数组，其中每个值都加上了 10。
要确认的概念：看到广播的第一层直觉，是把一个标量应用到数组的每个位置。

```python
import numpy as np

scores = np.array([82, 75, 45])
print(scores + 10)
```

输出如下。

```text
[92 85 55]
```

代码里没有 `for`。但从结果看，每个值都加上了 10。要理解这种计算，需要把 broadcasting 和 vectorization 一起看。

本节说明 `broadcasting` 与 `vectorization` 的基本区分。`NumPy`、`shape`、`axis` 的代表性说明仍放在 P2-11.1、P2-11.2 和 [概念词汇表](../../../reference/concept-glossary.md)，这里专注于：计算是怎样扩散到整个数组上的。

## 本节范围

本节讨论 NumPy 把计算应用到整个数组上的基本方式。

这里回答以下问题。

- broadcasting 让什么东西匹配起来？
- scalar 是怎样和 array 一起计算的？
- 为什么形状 `(4, 3)` 的数组可以和形状 `(3,)` 的数组相加？
- 为什么 `(4, 3)` 与 `(4,)` 不容易直接相加？
- vectorization 是消除了重复，还是把重复移动到了别的位置？
- 为什么在 AI 实践里，normalization、weight calculation、按 feature 运算，经常写成数组级别的代码？

本节不深入 advanced broadcasting、`np.newaxis` 的细节用法、`reshape`、stride、memory view、性能基准或 GPU tensor computation。`np.newaxis` 和 shape 变化会在 P2-11.4 的补充学习里再出现。这里的重点是先建立一种直觉：`只要 shape 合适，重复计算就可以按数组级别来读`。如果 broadcasting 的例子大体能读懂，但 `(3,)`、`(3, 1)`、`(1, 3)` 的区别或 slicing 之后与原数组共享的关系仍然混乱，就先暂停这一节，转去 P2-11.4，再回来。

## 本节目标

- 能把 broadcasting 解释为：较小数组像是被匹配到较大数组的 shape 上来进行计算的规则。
- 能把 scalar 与 array 的计算读成逐位置计算。
- 能说明把形状 `(m,)` 的向量加到或减去形状 `(n, m)` 的数据矩阵的例子。
- 能说明 shape 不匹配时会出现 broadcasting 错误。
- 能把 vectorization 解释为：不是“重复消失了”，而是“Python 循环被表达成了一次数组运算”。

## 三个标准

| 标准 | 为什么重要 | 本节需要达到的理解程度 |
| --- | --- | --- |
| broadcasting 是什么 | 它解释了为什么整数组计算能用一行读出来 | 理解为把较小数组自然铺开后应用到较大数组计算中的方式 |
| vectorization 是什么 | 它明确说明重复并没有消失，只是改变了表达位置 | 理解为把原本循环写的事改写成一次数组运算 |
| 先要注意什么 | 它让你同时看到便利性和 shape 出错的可能 | 理解为语法看起来再方便，也要先检查 `shape` |

| 术语 | 本节先抓住的含义 |
| --- | --- |
| broadcasting | 把较小数组或 scalar 应用到较大数组计算中的规则 |
| vectorization | 用一次数组运算来表达重复计算的方法 |
| element-wise operation | 对对应位置上的值应用同样规则的计算 |
| shape compatibility | 判断两个数组能否一起计算的形状条件 |
| scalar | 对整个数组应用同一规则时所用的单个数字 |

## Broadcasting 通过匹配 Shape 来完成计算

NumPy 官方文档把 broadcasting 介绍为：在算术运算中，如何处理不同 shape 的数组。较小数组会在计算时被视为与较大数组兼容的形状。

这里把 broadcasting 理解为 `把较小的值或较小的数组，按较大数组的形状重复应用的规则`。

最容易的例子，是 scalar 与 array 的计算。

问题场景：比较标量加到或乘到整个数组上时，结果怎样变化。
输入(input)：分数数组 `scores`，以及标量 `10`、`2`。
期待输出(output)：分别打印 `+10` 的结果和 `*2` 的结果。
要确认的概念：确认标量运算会把同样的规则应用到数组每个位置。

```python
scores = np.array([82, 75, 45])

print(scores + 10)
print(scores * 2)
```

输出如下。

```text
[92 85 55]
[164 150  90]
```

这里的 `10` 和 `2` 就是 scalar。NumPy 会把这个 scalar 应用到数组的每个位置。

下面的图示展示了：一个 scalar 如何被重复应用到整个数组。更安全的理解方式，不是把同一个值真的复制很多次，而是理解成“同一条计算规则应用到了每个位置”。

![A scalar is applied across an array by broadcasting](../../../assets/part-02/chapter-11/broadcast-scalar-array-en.svg)

## 数组一起计算时，要先看 Shape

broadcasting 不是强行让任意数组都匹配的功能。shape 必须兼容。

例如，看下面这些数组。

问题场景：一起查看 `shape` 和结果，确认 feature-wise offset 向量能否加到 feature matrix 上。
输入(input)：形状为 `(4, 3)` 的 `features` 和形状为 `(3,)` 的 `feature_offset`。
期待输出(output)：打印两个数组的 `shape` 以及调整后的矩阵。
要确认的概念：看到长度为 3 的向量可以广播到每一行的 3 个 feature 上。

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

输出如下。

```text
(4, 3)
(3,)
[[1.1 0.4 7.3]
 [0.9 0.6 6.8]
 [0.4 1.1 8.4]
 [0.6 0.3 6.1]]
```

`features` 的 shape 是 `(4, 3)`，可以读成 4 个 sample、3 个 feature。

`feature_offset` 的 shape 是 `(3,)`，可以读成对 3 个 feature 分别要加的值。

NumPy 会判断：形状 `(3,)` 的数组可以作用到每一行上。所以同样的 offset 会加到每个 sample 的三个 feature 上。

下面的图示展示了：形状 `(3,)` 的向量如何逐行应用到 `(4, 3)` 的数据矩阵。

![A row-shaped vector is broadcast across each row of a feature matrix](../../../assets/part-02/chapter-11/broadcast-row-vector-en.svg)

## 不兼容的 Shape 会导致错误

broadcasting 很方便，但如果 shape 不匹配，就会报错。

问题场景：确认为什么看上去有点像的 shape，仍然会因为不匹配而报错。
输入(input)：形状 `(4, 3)` 的矩阵 `features` 和长度为 4 的向量 `bad_offset`。
期待输出(output)：先打印两个 shape，然后出现 broadcasting 错误。
要确认的概念：看到 broadcasting 不会让任意数组都匹配起来，而且从最后一个维度开始的兼容性很重要。

```python
bad_offset = np.array([10, 20, 30, 40])

print(features.shape)
print(bad_offset.shape)
print(features + bad_offset)
```

这段代码会报错。

```text
ValueError: operands could not be broadcast together with shapes (4,3) (4,)
```

为什么？

`features` 是 `(4, 3)`。每一行有 3 个 feature。可 `bad_offset` 是 `(4,)`。这 4 个值看上去像是能对应 4 行，但它并不能对应每行内部的 3 列。

先记住下面这个标准。

| 计算 | 读取方式 | 结果 |
| --- | --- | --- |
| `(4, 3) + scalar` | 对每个位置应用同一个值 | 可以 |
| `(4, 3) + (3,)` | 对每一行应用长度为 3 的向量 | 可以 |
| `(4, 3) + (4,)` | 和每行内部长度 3 不匹配 | 错误 |

精确规则会更复杂，但在这个阶段，重要直觉是：`先看最后一个维度是否匹配`。

## Vectorization 是把重复写成数组运算

vectorization 是一种表达方式：不直接写 Python 循环，而是用数组运算来表达计算。

例如，用 Python 循环给每个分数加 10，可以这样写。

问题场景：在和数组运算比较之前，先直接用循环写出同样的工作。
输入(input)：一个包含三个分数的 Python list。
期待输出(output)：打印一个每个分数都加了 10 的列表。
要确认的概念：看到 vectorization 就是把这样的重复计算更紧凑地写成数组运算。

```python
scores = [82, 75, 45]

adjusted = []
for score in scores:
    adjusted.append(score + 10)

print(adjusted)
```

换成 NumPy array，可以写成这样。

问题场景：把刚才用循环做的事，改写成一行 NumPy 数组运算。
输入(input)：分数数组 `scores` 和标量 `10`。
期待输出(output)：打印调整后的分数数组。
要确认的概念：确认 vectorization 不等于重复消失，而是把重复写成了数组级语法。

```python
scores = np.array([82, 75, 45])
adjusted = scores + 10

print(adjusted)
```

两种写法都在给每个分数加 10。区别在于表达方式。

| 方式 | 代码里可见的结构 | 读者应抓住的视角 |
| --- | --- | --- |
| Python loop | 一个个取值再处理 | 过程被直接写出来 |
| NumPy vectorization | 对整个数组施加运算 | 同一个计算被表达成数组级别的操作 |

NumPy 官方文档说明，broadcasting 提供了 vectorizing array operations 的手段，并让重复发生在 C 层而不是 Python 层。因此，把 vectorization 理解成“重复消失了”并不准确。

更安全的表达是，把 vectorization 看成 `不是用 Python 的 for，而是用数组运算来表达重复计算的方法`。

下面的图示展示了：同一个计算如何分别以循环和数组运算的形式表达。

```mermaid
--8<-- "assets/part-02/chapter-11/loop-to-vectorization-flow/zh.mmd"
```

## 按 Feature 减去平均值的例子

在 AI 数据处理中，一个常见例子是减去每个 feature 的平均值。可以把它读成“让平均值更靠近 0”的预处理起点。

先创建数据矩阵。

问题场景：在按 feature 减平均值的预处理中，一起查看平均值向量和中心化结果。
输入(input)：形状为 `(4, 3)` 的 feature matrix `features`。
期待输出(output)：打印按列求出的平均值向量，以及减去平均值后的矩阵。
要确认的概念：看到 `mean(axis=0)` 结果 `(3,)` 会广播到每一行，从而形成中心化。

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

输出大致如下。

```text
[0.65 0.4  6.85]
[[ 0.35 -0.2   0.15]
 [ 0.15  0.   -0.35]
 [-0.35  0.5   1.25]
 [-0.15 -0.3  -1.05]]
```

这里，`features.mean(axis=0)` 计算的是每一列的平均值，结果 shape 是 `(3,)`。`features` 的 shape 是 `(4, 3)`。

`features - column_mean` 是从 `(4, 3)` 中减去 `(3,)` 的计算。NumPy 会把这个平均值向量应用到每一行。

这个例子直接连到 P2-11.2 里 axis 的说明。

| 代码 | shape | 含义 |
| --- | --- | --- |
| `features` | `(4, 3)` | 4 个 sample，3 个 feature |
| `features.mean(axis=0)` | `(3,)` | 按 feature 求平均值 |
| `features - column_mean` | `(4, 3)` | 从每个 sample 中减去各 feature 平均值后的结果 |

重要的不只是“算出一个平均值”，而是要一起读出：平均值是沿哪个轴算的、结果 shape 是什么、以及它如何应用回原数组。

## Broadcasting 很方便，但并不总是最好

broadcasting 和 vectorization 可以让代码更短，也常常更容易读。但这不等于它们永远是更好的方法。

要注意三件事。

第一，如果不检查 shape，就可能做出和原意不同的计算。

第二，复杂的 broadcasting 会让代码变得难读。

第三，在某些情况下，可能会创建过大的中间数组，消耗很多内存。NumPy 官方文档也提醒：broadcasting 通常高效，但某些算法里可能会低效地使用内存。

所以入门阶段一个好的习惯是下面这样。

问题场景：检查在做 broadcasting 计算之前，应该先打印哪些 shape。
输入(input)：原始矩阵 `features` 与列平均值向量 `column_mean`。
期待输出(output)：打印这两个数组的 shape。
要确认的概念：看到 broadcasting 看起来再方便，也应该先检查 shape。

```python
print(features.shape)
print(column_mean.shape)
```

计算之前先看 shape。

## 示例代码文件

本节示例代码也可以在下面这个文件中查看。

- [p2_11_3_broadcast_vectorization.py](../../../assets/part-02/chapter-11/p2_11_3_broadcast_vectorization.py)

在本地 PC 上，可以在项目根目录这样运行。

```bash
python docs/assets/part-02/chapter-11/p2_11_3_broadcast_vectorization.py
```

在 Colab 里，可以把文件内容贴进代码单元后执行。

输出中包含 scalar broadcasting、row vector broadcasting、shape mismatch 错误例子，以及按 feature 去均值的例子。

## 结合案例来看

### 案例 1. 为什么要一次性给所有学生加上修正分数

学习者想给每个学生的分数加上修正值时，很自然会想用 `for` 循环一个个处理。这种方式对理解过程有帮助，但当 feature 变多、sample 变多后，同样的计算就要一遍遍写，代码会变长。

在 NumPy array 里，同样的计算可以通过 `scores + 10`，或者把形状 `(3,)` 的向量加到 `(4, 3)` 的矩阵上，一次性表达出来。这里重要的不是 NumPy 在“魔法般地替你算”，而是把人原本重复做的同一运算，改写成了数组级语法。

例如，如果你要给每个有三个 feature 的学生都加上 `[0.1, 0.2, 0.3]` 这样的 feature-wise offset，那么同一个长度为 3 的向量会应用到 `(4, 3)` 矩阵的每一行。相反，如果你想加一个 `(4,)` 的向量，就会因为 shape 不匹配而报错。所以最先要检查的永远是 `shape`，而不是方便不方便。

这个案例把 broadcasting 和 vectorization 重新绑回真实计算场景。重复并没有被删除，而是改写成了数组计算。要让这种表达安全工作，就必须先读出：较小数组和较大数组各自对应的到底是什么问题。

## 本节要记住的视角

broadcasting 是让较小的值或较小数组按较大数组 shape 参与计算的规则。

scalar 可以应用到数组的每个位置。

形状 `(4, 3)` 的数组和形状 `(3,)` 的数组能够一起计算，因为长度 3 能匹配每一行。

形状 `(4, 3)` 和 `(4,)` 看上去像是对上了行数，但从最后一个维度看并不匹配，所以可能会报错。

vectorization 是用数组运算来表达重复计算的方法。

使用 broadcasting 与 vectorization 时，要在计算前后检查 `shape`。

## 简短检查

- 能把 scalar 与 array 的计算解释成 broadcasting。
- 能说明为什么 `(4, 3) + (3,)` 可行。
- 能说明为什么 `(4, 3) + (4,)` 可能立即失败。
- 能说明 Python loop 与 NumPy vectorized expression 的差别。
- 能说明 `features.mean(axis=0)` 的结果 shape。
- 能说明在按 feature 去均值的计算里，broadcasting 发生在什么地方。
- 能说明 broadcasting 不总是最佳选择，而且需要检查 shape 与内存使用。

## 什么时候应先想起这个视角

- 当你想在不写循环时把同样计算施加到整个数组上，或想一起计算 shape 不同的数组时，先想起 broadcasting 与 vectorization 的视角。
- 当你需要解释为什么 `(4, 3) + (3,)` 可以，而 `(4, 3) + (4,)` 不行时，就回到本节的 shape 规则。
- 当你需要把 axis 统计和自动扩展一起用在减均值、normalization、按 feature 计算等场景时，再检查本节。

## 来源与参考资料

- NumPy Developers, [Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-25.
- NumPy Developers, [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-25.
- NumPy Developers, [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-25.
