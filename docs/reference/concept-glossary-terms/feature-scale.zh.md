<a id="feature-scale"></a>

## 特征尺度(feature scale)

- 含义：feature scale 是某个 feature 的单位、取值范围和分散程度。在 k-NN 这类基于 distance 判断的模型里，尺度很大的 feature 可能会支配“近不近”的计算。
- 为什么重要：两个 feature 都是数字，并不表示它们会以相同权重进入 distance。像 income 这样范围很大的 feature 如果盖住 late-payment count 这类小范围 feature，model 就可能过度跟随大数字轴，而不是数据真正有意义的差异。
- 相关概念：`distance`, `standardization`, `preprocessing`
- 核心 Section：`P4-12.2`
- 出现 Section：`P4-12.2`, `P4-12.3`
