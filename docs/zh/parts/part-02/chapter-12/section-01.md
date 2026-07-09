# P2-12.1 Pandas DataFrame 表达什么

> Section ID: `P2-12.1`
> Version: `v2026.07.07`

P2-12.1 从 NumPy 数组转向带标签的表。重点不是说 DataFrame 取代数组，而是说 row、column、label 让我们更直接地读案例与变量。

## 本节范围

本节把 DataFrame 介绍为带标签的二维表，并区分 row、column、index 的读取角色。

## 中心问题

为什么在把数据变成模型输入数组之前，DataFrame 往往是读取数据集的自然第一结构？

## 记住的视角

- DataFrame 是带标签的表，不只是原始数值矩阵。
- 一行常被读成一个案例，一列常被读成一个变量。
- index 可以只是位置，也可以是有意义的标签。
- 数组与 DataFrame 不是竞争关系，而是在回答不同问题。

## 简短检查

- 能说明为什么读取真实数据集时标签很重要。
- 能说明 row、column、index 之间的区别。
- 能说明为什么混合类型列会自然地放进 DataFrame。

## 来源与参考资料

- pandas, [DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
