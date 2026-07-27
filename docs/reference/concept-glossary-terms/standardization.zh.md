<a id="standardization"></a>

## 标准化(standardization)

- 含义：standardization 会从每个 feature 中减去 mean，再除以 standard deviation，让不同单位和不同分散程度的数值进入更可比较的范围。在基于 distance 的模型里，它可以读成重新平衡各个 feature 对 distance 影响的 preprocessing。
- 为什么重要：如果不做 standardization，取值范围很大的 feature 可能支配 distance 计算。standardization 之后，小范围 feature 也可能重新影响 neighbor 选择，所以需要比较前后哪些 neighbor 进来、哪些出去。
- 相关概念：`feature`, `distance`, `preprocessing`
- 核心 Section：`P4-12.2`
- 出现 Section：`P4-12.2`
