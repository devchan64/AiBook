<a id="penalty"></a>

## 惩罚项(penalty)

- 含义：penalty 是加到 objective function 里的额外成本，让 model 不那么偏好某些解。在 logistic regression 设置中，它通常指 L1、L2、Elastic-Net 这类 regularization 形式，用来控制 coefficient 要怎样保持得更保守。
- 为什么重要：penalty 一变，model 避免大 coefficient 的方式、是否把一部分 coefficient 推向 0、以及支持的 solver 组合都可能改变。因此比较性能或 coefficient 时，必须单独记录 penalty 设置。
- 相关概念：`regularization`, `objective function`, `solver`
- 核心 Section：`P4-11.5`
- 出现 Section：`P4-11.5`
