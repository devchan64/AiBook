<a id="multinomial-logistic-regression"></a>

### 多类别逻辑回归(multinomial logistic regression)

- 含义：multinomial logistic regression 是 logistic regression 在三个或更多 class 中选择一个 class 的扩展。它会为每个 class 生成 score，再把这些 score 转成 probability distribution。
- 为什么重要：它把二元分类里的 `score -> probability -> class selection` 直觉扩展到 multiclass comparison。多类别场景通常要看完整 probability distribution 和 argmax 选择，而不是只看一个 0.5 threshold。
- 相关概念：`logistic regression`, `softmax`, `classification`
- 中心 Section：`P4-11.4`
