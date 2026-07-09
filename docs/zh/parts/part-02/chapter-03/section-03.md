# P2-3.3 矩阵乘法到底在复用什么

> Section ID: `P2-3.3`
> Version: `v2026.07.09`

矩阵乘法第一次看时很容易显得神秘。在 AI 阅读里，更有用的入口是：矩阵乘法在反复复用同一种“加权求和”结构。

## 本节范围

本节入门介绍 `matrix multiplication`、`weighted sum`、`weight matrix`、`linear transformation`、`input/output dimension`。

## 先固定的术语

| 术语 | 很短的意思 | 本节中的作用 |
| --- | --- | --- |
| matrix multiplication | 通过行列组合生成新值的计算 | 本节核心 |
| weighted sum | 输入乘权重再相加 | 形成一个输出的最小单位 |
| weight matrix | 多个输出对应的权重表 | 把输入变成新表示 |
| linear transformation | 向量到向量的变化 | 解释矩阵乘法的框架 |
| input/output dimension | 输入长度与输出长度 | 为什么 shape 重要 |

## 位置对应相乘不是矩阵乘法

矩阵乘法不是“每个位置直接相乘”。它更像是：

1. 把多个输入按权重相乘并相加
2. 得到一个输出
3. 把这个结构对多个输出重复使用

![矩阵乘法改变向量位置的示意](../../../assets/part-02/chapter-03/matrix-multiplication-position-change-en.svg)

## 为什么 shape 先出现

如果内侧维度对不上，就不知道该把哪些输入和哪些权重对应起来。因此矩阵乘法问题往往会先变成 shape 问题。

## 记住的视角

- 矩阵乘法是在复用加权求和。
- 它不同于位置对应相乘。
- 权重矩阵可以把一种表示变成另一种表示。
- `shape` 决定这个计算是否成立。

## 简短检查

- 能说明矩阵乘法为什么不是逐位置相乘。
- 能说明一个输出为什么可以看成加权求和。
- 能说明矩阵乘法为什么会被读成表示变换。

## 来源与参考资料

- NumPy Developers, [Array objects](https://numpy.org/doc/stable/reference/arrays.ndarray.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
