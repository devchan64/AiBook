# P2-3.6 用 NumPy 确认线性代数

> Section ID: `P2-3.6`
> Version: `v2026.07.09`

现在把前面的线性代数内容放到代码里看一遍。这里目标不是单独背 NumPy 语法，而是确认公式、数组、输出之间其实在讲同一件事。

## 本节范围

本节用 NumPy 检查向量、矩阵、`shape`、逐元素乘法、矩阵乘法，不展开完整 NumPy 教程。

## 先抓住的对应表

| 代码场景 | 回头确认的前文概念 | 先看什么 |
| --- | --- | --- |
| 创建向量和矩阵 | P2-3.1 的形状 | shape 是否符合预期 |
| 比较向量 | P2-3.2 的位置直觉 | 是否在同一空间里 |
| `a + b`, `2 * a` | 基本向量运算 | 代码里怎样呈现 |
| `*` 与 `@` | P2-3.3 的乘法区分 | 是逐元素还是矩阵乘法 |
| 批量矩阵计算 | 多个向量一起处理 | 输入输出 shape 如何变化 |

本节示例代码文件是 [p2_3_6_numpy_linear_algebra.py](../../../assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py)。

## 记住的视角

- NumPy 让数组结构变得可见。
- `shape` 往往比具体数值更早解释计算。
- `*` 与 `@` 不能混读。
- 矩阵能一次处理多个样本，这是 AI 代码里矩阵常见的重要原因。

## 简短检查

- 能说明为什么要先看 `.shape`。
- 能说明 `*` 与 `@` 的区别。
- 能说明为什么一个矩阵可以表示多个样本。

## 来源与参考资料

- NumPy Developers, [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
