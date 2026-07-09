# P2-11.2 索引、切片与轴

> Section ID: `P2-11.2`
> Version: `v2026.07.09`

P2-11.2 从“创建数组”转向“在数组里怎么读”。这里把三件事分开：选一个位置、保留一个区间、决定计算沿哪个方向进行。

## 本节范围

本节用一维与二维数组介绍基本 indexing、slicing 与 `axis` 的读取方式。

## 中心问题

为什么 indexing、slicing、axis 会对同一个数组提出不同问题？

![Slice notation selects a range from start to stop before the stop position](../../../assets/part-02/chapter-11/slice-start-stop-step-en.svg)

![Indexing, slicing, and axis read different parts of the same array](../../../assets/part-02/chapter-11/index-slice-axis-map-en.svg)

![Axis controls the direction of reduction](../../../assets/part-02/chapter-11/axis-reduction-en.svg)

![Rows often represent samples and columns often represent features](../../../assets/part-02/chapter-11/dataset-row-column-selection-en.svg)

## 记住的视角

- indexing 选一个精确位置。
- slicing 保留一个区间，而不是一个值。
- `axis=0` 与 `axis=1` 描述的是归约方向，不只是屏幕方向。
- 在数据集式读取里，row 常表示 sample，column 常表示 feature。

## 简短检查

- 能说明 `x[1, 2]`、`x[1, :]`、`x[:, 2]` 的区别。
- 能说明为什么 `sum(axis=0)` 与 `sum(axis=1)` 会留下不同的结果 shape。
- 能说明为什么在模型训练例子之前，行列读取已经很重要。

## 来源与参考资料

- NumPy Developers, [Indexing on ndarrays](https://numpy.org/doc/stable/user/basics.indexing.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
