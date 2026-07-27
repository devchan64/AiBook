<a id="distributed-training"></a>

## 分布式训练

- 含义：分布式训练把一个训练任务拆到多个计算资源或 worker 上执行。 在 boosting 里，当数据很大、stage 很多、验证组合很多时，它会经常被提到。
- 为什么重要：分布式训练主要不是改变模型哲学，而是让长时间重复和大数据变得可运营。 在 boosting 中，数据切分、stage 记录、失败重启规则必须保持一致，比较结果才有意义。
- 相关概念：`GPU`，`训练(training)`，`验证数据(validation data)`
- 中心 Section：`P4-16.3`
- 出现 Section：`P4-16.3`
