# P2-13.2 基本图表与公式形状检查

> Section ID: `P2-13.2`
> Version: `v2026.07.09`

P2-13.2 继续坚持“先问题，后图表”。这里把 line plot、scatter plot、histogram、loss curve 连到“同一个学习场景被不同问题重新读取”的做法上。

## 本节范围

本节介绍 line plot、scatter plot、histogram、loss curve 的基础选择标准。

## 中心问题

当问题从趋势、关系切换到分布时，图表选择为什么也必须改变？

![Function shape of y = x squared](../../../assets/part-02/chapter-13/basic-line-function-shape.png)

![Scatter plot with a noisy relationship](../../../assets/part-02/chapter-13/basic-scatter-relationship.png)

![Histogram showing where values cluster](../../../assets/part-02/chapter-13/basic-hist-distribution.png)

![Comparing a stable and unstable loss curve](../../../assets/part-02/chapter-13/basic-loss-curve-comparison.png)

## 记住的视角

- 当顺序或变化过程重要时，用 line plot。
- 当两组值之间的关系重要时，用 scatter plot。
- 当一个变量的分布重要时，用 histogram。
- 标题与轴标签不是装饰，而是解释的一部分。

## 简短检查

- 能说明为什么同一个学习场景会因为问题不同而换图。
- 能说明 histogram 与 scatter plot 回答的不是同一种问题。
- 能说明为什么 loss curve 更像监控工具，而不是成功证明。

## 来源与参考资料

- Matplotlib, [Plot types](https://matplotlib.org/stable/plot_types/index.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
