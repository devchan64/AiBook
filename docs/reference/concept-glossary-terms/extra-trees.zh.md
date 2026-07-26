<a id="extra-trees"></a>

## Extra Trees

- 含义: Extra Trees，也叫 Extremely Randomized Trees，是把多棵决策树的预测做平均的树集成。它很接近随机森林，但会用更随机的方式抽取 split threshold。
- 为什么重要: 它是随机森林旁边很近的比较候选。默认设置下 `bootstrap=False`，所以 OOB 不会自动跟上来。
- 相关概念: `随机森林(random forest)`, `best split`, `random threshold`, `bootstrap`, `oob_score`
- 中心 Section: `P4-15.4`
- 出现 Section: `P4-15.4`
