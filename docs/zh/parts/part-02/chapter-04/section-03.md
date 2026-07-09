# P2-4.3 导数与梯度

> Section ID: `P2-4.3`
> Version: `v2026.07.09`

P2-4.2 先读了变化率与斜率。这里把这条线继续接到 AI 文档里最常见的两个词：`derivative` 与 `gradient`。

## 本节范围

本节入门区分 derivative、derivative function、partial derivative、gradient、nabla。

## 记住的结构

- 导数：一个输入方向上的局部变化率
- 偏导数：多个输入里，只看其中一个输入变化时的变化率
- 梯度：把多个偏导数按顺序收集成一个向量

AI 学习里之所以反复出现梯度，是因为模型通常有很多参数，我们需要同时知道多个方向上的变化信息。

## 记住的视角

- 导数对应“一个输入”的局部变化。
- 偏导数对应“多个输入中挑一个来看”。
- 梯度对应“把多个方向的变化率合在一起”。

## 简短检查

- 能说明导数是一输入的局部变化率。
- 能说明为什么多输入函数需要偏导数。
- 能说明为什么梯度会在模型学习里反复出现。

## 来源与参考资料

- OpenStax, [Calculus Volume 3](https://openstax.org/details/books/calculus-volume-3){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
