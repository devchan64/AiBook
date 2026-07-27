<a id="margin"></a>

## 间隔(margin)

- 含义: classification boundary 和离它最近的数据案例之间留下的安全余量。在 SVM 语境里，它常被读成：在多个候选 boundary 中，要让最近点到 boundary 的最小距离尽量变大。
- 为什么重要: 同一批数据可能有多条 boundary 都能分开，只看是否分开并不足以判断哪条更稳定。margin 可以帮助读者检查 boundary 是否过度贴近某一侧 class，以及 boundary 附近的小扰动是否容易改变 prediction。
- 相关概念: `SVM`, `决策边界(decision boundary)`, `分类(classification)`, `超参数(hyperparameter)`
- 中心 Section: `P4-13.1`
- 出现 Section: `P4-13.1`
