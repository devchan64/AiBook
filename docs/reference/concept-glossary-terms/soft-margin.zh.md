<a id="soft-margin"></a>

## 软间隔(soft margin)

- 含义: SVM 的一种观点：不再只坚持把每个 training case 都完美分开，而是允许一部分错误或 boundary 侵入，同时仍然寻找整体上有意义的 margin。
- 为什么重要: 真实数据常有噪声、例外和重叠。如果强行要求完美分离，boundary 可能会变得过度紧绷。soft margin 能帮助读者读取 `留有余量的 boundary` 和 `可接受错误` 之间的平衡。
- 相关概念: `间隔(margin)`, `SVM`, `超参数(hyperparameter)`, `C`
- 中心 Section: `P4-13.1`
- 出现 Section: `P4-13.1`
