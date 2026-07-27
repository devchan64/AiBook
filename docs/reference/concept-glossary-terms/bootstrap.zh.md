<a id="bootstrap"></a>

## bootstrap

- 含义：bootstrap 是从原始数据中有放回抽样的方法。在随机森林里，它让每棵树看到略有不同的训练样本组合。
- 为什么重要：bootstrap 让多棵树虽然来自同一份数据，却拥有不同的训练经验。这样可以减少所有树以同样方式记住同一个例外的风险，也会自然产生 OOB(out-of-bag) 检查的基础。
- 相关概念：`样本(sample)`，`集成(ensemble)`，`验证(validation)`
- 中心 Section：`P4-15.1`
- 出现 Section：`P4-15.1`, `P4-15.3`
