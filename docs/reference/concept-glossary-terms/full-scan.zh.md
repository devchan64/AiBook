<a id="full-scan"></a>

## 全量比较

- 含义：全量比较是在搜索时不跳过任何候选，逐一比较所有候选向量来寻找最近项目的方式。
- 为什么重要：候选数少时，全量比较简单而安全；候选数变大时，比较成本和延迟会一起增长。理解它，才能把 ANN 读成减少全量比较成本的折中，而不是随便搜索。
- 相关概念：`nearest neighbor`，`ANN, approximate nearest neighbor`，`recall`
- 核心 Section：`P6-3.4`
- 出现 Section：`P6-3.4`

