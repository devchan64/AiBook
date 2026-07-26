<a id="support-vector-machine"></a>

## 支持向量机(SVM, support vector machine)

- 含义: 一种分类模型，会寻找能划分类别的 boundary，同时尽量让这条 boundary 和两边最近案例之间保留较大的 margin。它不只问两类能不能分开，还会问 boundary 周围能不能留下足够的安全间隔。
- 为什么重要: SVM 让读者看到，分类不只是画出一条分割线，还要一起考虑 boundary 的稳定性。这个概念有助于区分 `勉强切开 training data 的 boundary` 和 `在新数据上可能更稳的 boundary`，也让最靠近 boundary 的案例为什么会影响 generalization 感觉变得更自然。
- 相关概念: `间隔(margin)`, `决策边界(decision boundary)`, `支持向量(support vector)`, `核(kernel)`
- 中心 Section: `P4-13.1`
- 出现 Section: `P4-13.1`, `P4-13.2`
