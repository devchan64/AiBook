# P2-9.2 数组、表、树、图的直觉

> Section ID: `P2-9.2`
> Version: `v2026.07.09`

P2-9.1 把数据结构先看成组织形状的问题。这里比较 AI 实践里最常见的四种大形状：array、table、tree、graph。

## 本节范围

本节重点是“问题怎么读”，而不是完整实现。

## 中心问题

为什么当我们看的是位置、行列、层级、关系时，自然的结构也会跟着改变？

![Array, table, tree, and graph compare different data questions](../../../assets/part-02/chapter-09/data-structure-four-views-en.svg)

![Choose array, table, tree, or graph by the question](../../../assets/part-02/chapter-09/question-to-structure-map-en.svg)

![The same student data can become an array, table, tree, or graph](../../../assets/part-02/chapter-09/same-data-four-structures-en.svg)

## 记住的视角

- array 强调位置与轴。
- table 强调行列与案例比较。
- tree 强调层级。
- graph 强调关系。

## 简短检查

- 能说明为什么问题一变，同一份数据也能重新组织。
- 能按“更容易回答的问题”区分这四种结构。
- 能说明为什么“选哪种结构”往往其实是在问“先看哪种问题”。

## 来源与参考资料

- NumPy Developers, [ndarray](https://numpy.org/doc/stable/reference/arrays.ndarray.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
