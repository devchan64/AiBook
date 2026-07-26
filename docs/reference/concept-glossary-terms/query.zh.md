<a id="query"></a>

## 查询(query)

- 含义：query 是现在要比较或预测的新输入。在 k-NN 中，它会和已保存的 training examples 计算距离，用来寻找附近的 neighbors；在搜索中，它是用来取回候选项的基准表达。
- 为什么重要：query 可以把 `现在要判断的新案例` 和 `已经存好的参考案例` 分开。同一批 training data 下，只要 query 的位置或表示方式改变，被选中的 neighbors 和结果就可能改变。
- 相关概念：`最近邻`, `距离`, `搜索`
- 核心 Section：`P4-12.1`
- 出现 Section：`P4-12.1`
