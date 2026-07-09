# P2-11.3 广播与向量化

> Section ID: `P2-11.3`
> Version: `v2026.07.09`

P2-11.3 解释为什么很多数组运算看起来没有写 `for`，却仍然作用到了整个数组。入口很小：先看一个标量加到数组上，再看一个行形向量作用到矩阵上。

## 本节范围

本节只介绍 broadcasting 与 vectorized array computation 的基础直觉，不深入 `reshape`、`np.newaxis` 或性能基准。

## 中心问题

一个小值或一个小向量，是怎样作用到更大的数组上的，这又和 `shape` 兼容性有什么关系？

![A scalar is applied across an array by broadcasting](../../../assets/part-02/chapter-11/broadcast-scalar-array-en.svg)

![A row-shaped vector is broadcast across each row of a feature matrix](../../../assets/part-02/chapter-11/broadcast-row-vector-en.svg)

## 记住的视角

- broadcasting 关心的是 shape 是否兼容，而不是看起来像不像。
- vectorization 是把重复工作改写成数组运算。
- 在假设广播会成功之前，应先检查 `shape`。
- 按特征归一化、重复偏移量应用，都是 AI 里常见的例子。

## 简短检查

- 能说明为什么 `scores + 10` 在没有显式循环时仍会改变每个元素。
- 能说明为什么 `(4, 3) + (3,)` 比 `(4, 3) + (4,)` 更自然。
- 能说明为什么 broadcasting 虽然方便，但仍需要 shape 纪律。

## 来源与参考资料

- NumPy Developers, [Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
