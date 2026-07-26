<a id="hnsw-hierarchical-navigable-small-world"></a>

## HNSW，hierarchical navigable small world

- 含义：HNSW 是一种基于图的向量搜索索引方法，通过在邻近向量之间的连接中导航，快速寻找近似最近邻。
- 为什么重要：它说明大规模向量搜索不只是逐一比较向量，还会预先建立索引路径，让系统更快到达邻近候选。这里不需要实现 HNSW，但这个术语能解释为什么图式 ANN 经常出现在向量数据库中。
- 相关概念：`graph-based search`，`ANN, approximate nearest neighbor`，`search index`，`vector database`
- 核心 Section：`P1-13.4`
- 出现 Section：`P6-3.4`

