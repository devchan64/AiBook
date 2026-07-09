# P2-5.4 用小数据确认概率与统计

> Section ID: `P2-5.4`
> Version: `v2026.07.09`

P2-5.1 到 P2-5.3 先建立了概念语言，这一节用一小组数字和简单代码把这些概念再看一遍。

## 本节范围

本节用小数据确认均值、中位数、方差、样本均值变化，不展开完整统计库教程。

## 中心问题

前几节的概念在真实数字和输出里会怎样再次出现？

![用小数据区分原始数据、中心、扩散与样本估计的流程](../../../assets/part-02/chapter-05/small-data-statistics-check-en.svg)

本节示例代码文件是 [p2_5_4_small_statistics.py](../../../assets/part-02/chapter-05/p2_5_4_small_statistics.py)。

## 记住的视角

- 小数据也足够分别检查中心、扩散和样本波动。
- 代码让计算过程可见，但解释仍然重要。
- 这里的目标是恢复概念，不是死记库语法。

## 简短检查

- 能在一个小例子里说明 raw values、center、spread。
- 能说明为什么不同样本会得到不同的 sample mean。
- 能说明为什么代码输出仍需要解释。

## 来源与参考资料

- Python Software Foundation, [statistics — Mathematical statistics functions](https://docs.python.org/3/library/statistics.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
