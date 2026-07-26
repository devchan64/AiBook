<a id="oob-score"></a>

## oob_score

- 含义：`oob_score` 是随机森林中的一个设置，用没有参与某棵树训练的 out-of-bag 样本来计算内部评价信号。
- 为什么重要：OOB 可以提供一部分接近验证的感觉，但不能替代所有评价流程。它应该被读成 bootstrap 抽样自然带来的辅助检查手柄。
- 相关概念：`bootstrap`，`随机森林(random forest)`，`验证(validation)`，`测试(test)`
- 中心 Section：`P4-15.3`
- 出现 Section：`P4-15.1`, `P4-15.3`
