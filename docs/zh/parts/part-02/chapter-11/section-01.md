# P2-11.1 用 NumPy 数组构建向量与矩阵

> Section ID: `P2-11.1`
> Version: `v2026.07.09`

P2-11.1 把 NumPy 放到 Part 2 的“数据计算入口”位置来读。这里重新连接 vector、matrix、`shape`、`ndim`、`dtype` 与后面会反复出现的小型模型计算。

## 本节范围

本节聚焦于创建数值数组并读取它们的形状，不展开高级 indexing、内存布局或 GPU 执行。

## 中心问题

当目标从“存值”转向“用值计算”时，为什么 AI 实践会从通用 Python list 转向 NumPy array？

![Python list and NumPy array use the plus sign differently](../../../assets/part-02/chapter-11/list-vs-numpy-array-en.svg)

![Feature matrix times weight vector produces one score per sample](../../../assets/part-02/chapter-11/feature-weight-shape-flow-en.svg)

## 记住的视角

- NumPy 是面向计算的数值数组库，不只是另一个容器。
- 在解释结果前，应先看 `shape`、`ndim`、`dtype`。
- 一维数组常被读成 vector，二维数组常被读成 matrix。
- 像 `features @ weights` 这样的例子能把公式与可运行代码重新连起来。

## 简短检查

- 能说明为什么 `list + list` 与 `array + array` 可能代表不同运算。
- 能说明 `shape`、`ndim`、`dtype` 在深入分析前先告诉了你什么。
- 能说明为什么特征矩阵和权重向量会自然地写成数组。

## 来源与参考资料

- NumPy Developers, [The NumPy ndarray](https://numpy.org/doc/stable/reference/arrays.ndarray.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
- NumPy Developers, [Array objects](https://numpy.org/doc/stable/reference/arrays.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
