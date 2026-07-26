<a id="histogram-binning"></a>

## 直方图分箱

- 含义：直方图分箱不是逐个检查所有原始连续值，而是先把数值归入若干区间(bin)再计算。 在 boosting 里，它常用于让 split 候选计算更快、更省内存。
- 为什么重要：梯度提升会在很多 stage 中反复搜索 split，所以数据越大，计算成本越容易上升。 histogram binning 接受一定近似，换取更快的重复计算，是理解 LightGBM 等实现的重要抓手。
- 相关概念：`直方图(histogram)`，`LightGBM`，`梯度提升(gradient boosting)`
- 中心 Section：`P4-16.3`
- 出现 Section：`P4-16.3`
