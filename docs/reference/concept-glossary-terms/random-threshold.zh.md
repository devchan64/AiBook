<a id="random-threshold"></a>

## 随机阈值(random threshold)

- 含义: 随机阈值是在分支时不只通过最优搜索来选 cutoff，而是先随机抽出候选阈值再使用。
- 为什么重要: 这是 Extra Trees 比随机森林更随机的核心原因。随机性不只来自 feature 选择，也来自节点到底从哪里切。
- 相关概念: `Extra Trees`, `best split`, `阈值(threshold)`, `方差(variance)`
- 中心 Section: `P4-15.4`
- 出现 Section: `P4-15.4`
