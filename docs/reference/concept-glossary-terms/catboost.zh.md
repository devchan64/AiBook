<a id="catboost"></a>

## CatBoost

- 含义：CatBoost 是强调类别特征处理和 ordered boosting 的梯度提升库。 它常围绕 categorical data processing 与 target leakage 缓和来讨论。
- 为什么重要：CatBoost 说明选择 boosting 实现时，`怎样更安全地处理类别数据` 也可以成为单独标准。 当类别列很多，或者担心 target encoding 泄漏时，它会成为特别相关的候选。
- 相关概念：`梯度提升(gradient boosting)`，`类别特征(categorical feature)`，`泄漏(leakage)`
- 中心 Section：`P4-16.3`
- 出现 Section：`P4-16.3`
