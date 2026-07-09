# P2-9.3 How Does a Graph Represent Relationships?

> Section ID: `P2-9.3`
> Version: `v2026.07.09`

P2-9.2 compared arrays, tables, trees, and graphs. Among them, graphs often feel the most unfamiliar because the key question is no longer position or hierarchy, but connection.

## Scope of This Section

This Section introduces `graph`, `node`, `edge`, `direction`, and `weight` through relationship-reading scenes rather than full algorithm study.

## Central Question

How do we store and read “who is connected to whom” as data?

![A graph can be shown as nodes and edges or as an adjacency list](../../../assets/part-02/chapter-09/graph-node-edge-adjacency-en.svg)

![The same relationship records can be read as a table or a graph](../../../assets/part-02/chapter-09/table-to-graph-reading-en.svg)

![Direction and weight change what a graph edge means](../../../assets/part-02/chapter-09/directed-weighted-graph-en.svg)

![A graph distinguishes direct neighbors and two-hop neighbors](../../../assets/part-02/chapter-09/graph-neighbor-hop-en.svg)

## Perspective to Keep

- A graph reads objects as nodes and relationships as edges.
- Direction changes what an edge means.
- Weight adds another layer of meaning such as cost, distance, or similarity.
- Graph questions often extend from direct neighbors to paths and reachable nodes.

## Short Check

- Can you explain node and edge separately?
- Can you explain why a relationship table and a graph can encode the same data but support different questions?
- Can you explain why direction and weight change interpretation?

## Sources and References

- NIST, [graph](https://xlinux.nist.gov/dads/HTML/graph.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
