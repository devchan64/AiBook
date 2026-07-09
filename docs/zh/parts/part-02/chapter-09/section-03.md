# P2-9.3 图如何表达关系

> Section ID: `P2-9.3`
> Version: `v2026.07.09`

P2-9.2 比较了数组、表、树、图。其中图往往最陌生，因为这里的核心问题不再是位置或层级，而是连接。

## 本节范围

本节通过关系阅读场景，入门介绍 `graph`、`node`、`edge`、`direction`、`weight`，不展开完整图算法。

## 中心问题

怎样把“谁和谁连接”当成数据来保存和阅读？

![A graph can be shown as nodes and edges or as an adjacency list](../../../assets/part-02/chapter-09/graph-node-edge-adjacency-en.svg)

![The same relationship records can be read as a table or a graph](../../../assets/part-02/chapter-09/table-to-graph-reading-en.svg)

![Direction and weight change what a graph edge means](../../../assets/part-02/chapter-09/directed-weighted-graph-en.svg)

![A graph distinguishes direct neighbors and two-hop neighbors](../../../assets/part-02/chapter-09/graph-neighbor-hop-en.svg)

## 记住的视角

- graph 把对象读成 node，把关系读成 edge。
- direction 会改变 edge 的含义。
- weight 会给 edge 再加上一层含义，比如成本、距离、相似度。
- 图的问题常常会从“直接相邻”扩展到“路径和可达性”。

## 简短检查

- 能分别解释 node 和 edge。
- 能说明为什么关系表和图可以表示同样的数据，却支持不同的问题。
- 能说明为什么 direction 和 weight 会改变解读方式。

## 来源与参考资料

- NIST, [graph](https://xlinux.nist.gov/dads/HTML/graph.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
