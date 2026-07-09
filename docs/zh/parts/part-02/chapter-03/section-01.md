# P2-3.1 标量、向量与矩阵

> Section ID: `P2-3.1`
> Version: `v2026.07.07`

Chapter 2 重新阅读了数学记号。现在问题变了：当 AI 数据被整理成可以计算的形状时，我们到底在看什么？

这里先固定三种基本形状：

1. 一个数字
2. 一串有顺序的值
3. 一张有行和列的表

这三种形状分别对应线性代数里的标量、向量、矩阵。本节目标不是完整理论，而是先建立“AI 文档里的数字、列表、表格分别意味着什么”的阅读感觉。

## 本节范围

本节入门介绍 `scalar`、`vector`、`matrix`、`shape`、`array`。不展开行列式、特征值、严格证明等主题。

## 先固定的术语

| 术语 | 很短的意思 | 本节中的作用 |
| --- | --- | --- |
| scalar | 一个数字 | 读取损失、概率、学习率这类单值 |
| vector | 有顺序的值列表 | 用多个特征描述一个对象 |
| matrix | 带行列的数字表 | 同时处理多个样本或多个向量 |
| shape | 数组形状信息 | 先判断能做什么计算 |
| array | 按顺序放数字的结构 | 公式和代码相接的地方 |

## 记住的视角

- 标量是一个值。
- 向量是“一个对象的多个值”。
- 矩阵是“多个向量放在一起”。
- `shape` 常常比具体数值更早决定计算规则。

## 简短检查

- 能把标量解释成一个数字。
- 能把向量解释成有顺序的值列表。
- 能把矩阵解释成多个向量组成的表。
- 能说明为什么 `shape` 会先影响计算。

## 来源与参考资料

- Python Software Foundation, [Built-in Types](https://docs.python.org/3/library/stdtypes.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
- NumPy Developers, [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
