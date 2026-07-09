# P2-11.4 补充学习：在 NumPy 中一起读取 shape 变化与原数组共享

> Section ID: `P2-11.4`
> Version: `v2026.07.09`

P2-11.4 是给这样一种情况准备的回返点：基础 indexing 与 broadcasting 例子能读懂，但遇到 `view`、`copy`、fancy indexing、boolean mask、`np.newaxis` 时又会卡住。

## 本节范围

本补充节聚焦“选择方式、shape 变化、是否仍共享原数组”三者之间的关系。

## 中心问题

当数组在选择或重塑后看起来变了，我们怎样判断这只是换了读取路径，还是重新收集出了一个结果？

## 记住的视角

- 基本 slicing 常被读成对原数组的一个视图。
- fancy indexing 与 boolean mask 常会把值重新收集成新结果。
- `np.newaxis` 会有意加入一个长度为 1 的轴。
- 在实际代码里，shape 变化与共享来源问题应该一起检查。

## 简短检查

- 能说明为什么两种看起来相似的选择方式，在后续修改时会表现不同。
- 能说明 `np.newaxis` 即使不改数字，也改变了什么。
- 能说明为什么这一节更适合作为回返点，而不是第一次进入 NumPy 的入口。

## 来源与参考资料

- NumPy Developers, [Indexing on ndarrays](https://numpy.org/doc/stable/user/basics.indexing.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
- NumPy Developers, [Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
