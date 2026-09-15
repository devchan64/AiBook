# P2-9.3 图如何表示关系？

> Section ID: `P2-9.3`
> Version: `v2026.09.15`

## 节点与边

NIST《算法与数据结构词典》将图描述为通过边连接的项集合，每项称为顶点或节点。

图用节点表示对象，用边表示对象之间的关系。

下图同时用图形与邻接表表示同一个图。

![节点与边及其对应的邻接表](/AiBook/assets/part-02/chapter-09/graph-node-edge-adjacency-zh.svg)

`Kim`、`Lee`、`Park`、`Choi` 是节点。

`Kim -- Lee` 这样的节点连线就是边。

同一关系也可写成每个节点的邻居列表。

| 节点 | 邻居列表 |
| --- | --- |
| Kim | Lee, Park |
| Lee | Kim, Park |
| Park | Kim, Lee, Choi |
| Choi | Park |

这就是邻接表表示：每个节点都保存与其连接的邻居列表。

## 关系行与邻居列表

相同朋友数据也可存入表格，每一行记录一条关系。

| person | friend |
| --- | --- |
| Kim | Lee |
| Kim | Park |
| Lee | Park |
| Park | Choi |

“谁与 Kim 相连？”或“能否经 Park 到达 Choi？”等沿连接查询的问题，更适合图的视角。

下图比较同一关系记录作为表和图时，关注的问题如何变化。

![同一关系记录的表格与图视角](/AiBook/assets/part-02/chapter-09/table-to-graph-reading-zh.svg)

要从图的视角读取表格，可以按节点将关系行重新组成邻居列表。

## 使用 NetworkX 查询邻居

NetworkX 是构建图、查询邻居和路径的 Python 库。代码输入上述四条朋友关系和三条页面链接。Kim 的直接邻居为 Lee、Park，Choi 的最短距离为两步。页面链接中，`page_b` 指向 `page_c`，但没有反向链接。

```python
# weight 是示例关系强度，不参与下面的步数计算。
import networkx as nx

friend_relationships = [
    ("Kim", "Lee", {"weight": 1.0}),
    ("Kim", "Park", {"weight": 0.9}),
    ("Lee", "Park", {"weight": 0.8}),
    ("Park", "Choi", {"weight": 0.7}),
]

friend_graph = nx.Graph()
friend_graph.add_edges_from(friend_relationships)

friend_edges = sorted(tuple(sorted(edge)) for edge in friend_graph.edges())
distances = nx.single_source_shortest_path_length(friend_graph, "Kim", cutoff=2)
two_hop_neighbors = sorted(
    node for node, distance in distances.items() if distance == 2
)

print("friend nodes:", sorted(friend_graph.nodes()))
print("friend edges:", friend_edges)
print("Kim neighbors:", sorted(friend_graph.neighbors("Kim")))
print("Kim two-hop neighbors:", two_hop_neighbors)
print("Kim-Park weight:", friend_graph["Kim"]["Park"]["weight"])

page_graph = nx.DiGraph()
page_graph.add_edge("page_a", "page_b")
page_graph.add_edge("page_a", "page_c")
page_graph.add_edge("page_b", "page_c")

print("page_b links to:", list(page_graph.successors("page_b")))
print("page_c links back to page_b:", page_graph.has_edge("page_c", "page_b"))
```

预期输出：

```text
friend nodes: ['Choi', 'Kim', 'Lee', 'Park']
friend edges: [('Choi', 'Park'), ('Kim', 'Lee'), ('Kim', 'Park'), ('Lee', 'Park')]
Kim neighbors: ['Lee', 'Park']
Kim two-hop neighbors: ['Choi']
Kim-Park weight: 0.9
page_b links to: ['page_c']
page_c links back to page_b: False
```

`nx.Graph()` 创建朋友关系这样的无向连接，`nx.DiGraph()` 创建网页链接这样的有向连接。`neighbors()` 查询直接邻居，`single_source_shortest_path_length()` 计算从起点出发的步数。这里 `weight` 是示例关系强度，步数函数不使用它，每条边计一步。

## 树与环

树是图的一种特殊形式，NIST 的图定义也提到这一关系。

这里按以下方式区分。

无向树是连通且无环的图。指定根后，就能按父子层级读取。

书籍目录通常适合用树来理解。

```text
study-book
└─ Part 2
   └─ Chapter 9
      └─ Section 9.3
```

人与人的关系则较难整理成树。

```text
Kim -- Lee
Kim -- Park
Lee -- Park
Park -- Choi
```

这些朋友关系包含 `Kim → Lee → Park → Kim` 这样的环，会回到同一节点，因此不是树。

## 连接的方向

图的边可以无向，也可以有向。

关系在两个方向具有相同含义时，使用无向图。

简化的朋友关系可写成 `Kim -- Lee`：Kim 是 Lee 的朋友，也意味着 Lee 是 Kim 的朋友。

无向图中的同一连接应能从两端节点读取。

| 节点 | 邻居 |
| --- | --- |
| Kim | Lee |
| Lee | Kim |

关系的方向重要时，使用有向图。

网页链接有方向。文档 A 链接到 B，并不意味着 B 也链接到 A。

有向图中记录连接所指向的节点。

| 起点 | 指向的节点 |
| --- | --- |
| page_a | page_b, page_c |
| page_b | page_c |
| page_c | 无 |

AI 与搜索中，方向往往很重要。例如文档引用另一文档、工作流进入下一步、用户点击物品，都可用有向图表示。

下图显示方向与权重如何改变边的含义。

![方向与权重改变边的含义](/AiBook/assets/part-02/chapter-09/directed-weighted-graph-zh.svg)

不要假定有向关系也存在反向连接，应只按已记录的方向读取。

| 问题 | 回答 |
| --- | --- |
| `page_b` 指向哪个页面？ | `page_c` |
| `page_c` 是否反向指向 `page_b`？ | 在此表中没有 |

本例给出 `page_b` 到 `page_c` 的链接，没有给出反向链接。

## 权重的含义

连接的强度不一定相同。有些关系近，有些远，有些成本高。

附加在边上的数值称为权重。

假设 A、B、C 之间具有以下移动成本。这些是比较用数值，不是真实地理距离。

| 起点 | 终点 | 权重 |
| --- | --- | ---: |
| A | B | 160 |
| A | C | 325 |
| B | C | 200 |

A 直接到 C 成本为 325，经 B 则为 160 + 200 = 360。最小化成本会选择直连；将 A–C 改为 400 后，经 B 更便宜。

如果权重表示相似度，值越大可能表示关系越近。较大还是较小更好，取决于数值含义。

权重让问题不只停留在是否相连，还能询问有多近、成本多大或关联多强。

搜索或推荐候选的关系分数也适用同一视角。下面将已经计算好的关系分数与阈值比较。

| 候选文档 | 与查询的关系分数 | 与 `0.7` 比较 | 解读 |
| --- | ---: | --- | --- |
| `doc_a` | 0.91 | 不低于阈值 | 优先检查的强候选 |
| `doc_b` | 0.72 | 不低于阈值 | 一同检查的候选 |
| `doc_c` | 0.18 | 低于阈值 | 当前标准下暂缓的候选 |

将阈值提高到 `0.8`，`doc_b` 的 0.72 不再通过，只剩 `doc_a`。关系分数用于选择候选，并不保证文档内容准确。

## 更少步数与更低成本

最短路径的选择取决于距离是边数还是总成本。下面验证前面 A–C 成本改为 400 的情况。

```python
import networkx as nx

routes = nx.Graph()
routes.add_edge("A", "B", cost=160)
routes.add_edge("A", "C", cost=400)
routes.add_edge("B", "C", cost=200)

print(nx.shortest_path(routes, "A", "C"))
print(nx.shortest_path(routes, "A", "C", weight="cost"))
print(nx.shortest_path_length(routes, "A", "C", weight="cost"))
```

输出为 `['A', 'C']`、`['A', 'B', 'C']`、`360`。不指定权重时选择一步直连；`weight="cost"` 累加边成本，选择更便宜的路线。把直连成本降至 325 后，成本计算也返回直连路径和 `325`。

直接把相似度当成本，可能偏向相似度较小的路径。算法不会自行判断数值表示相似度还是移动成本，应先确定要最小化什么。

## 直接邻居与两跳邻居

从 Kim 出发，按最短路径上的边数计距离。直接邻居与最短距离为两步的节点如下。

| 标准 | 节点 | 解读 |
| --- | --- | --- |
| 直接邻居 | Lee、Park | 与 Kim 直接连接 |
| 两跳候选 | Choi | Kim → Park → Choi，最短距离为 2 |

下图区分 Kim 的直接邻居与两跳邻居。

![Kim 的直接邻居与两跳邻居](/AiBook/assets/part-02/chapter-09/graph-neighbor-hop-zh.svg)

Lee 也能经 Kim → Park → Lee 两步到达，但直连使其最短距离为 1，因此不包含在代码的两跳邻居中。

## AI 中的关系表示

| 场景 | 图的视角 |
| --- | --- |
| 知识图谱 | 概念、人物、地点、事件为节点，关系为边 |
| 推荐系统 | 用户与物品、物品与物品的连接 |
| 搜索 | 文档、链接、关键词、来源之间的连接 |
| RAG | 片段、元数据、来源与问题的关系 |
| 工作流 | 任务与后续步骤的连接 |

## 案例：增加一条朋友关系

在 NetworkX 示例中增加 Kim–Choi 直连。在 `friend_graph.add_edges_from(friend_relationships)` 后插入 `friend_graph.add_edge("Kim", "Choi", weight=0.6)` 并重新运行。

Kim 的直接邻居变为 `['Choi', 'Lee', 'Park']`，两跳列表变为 `[]`，因为 Choi 的最短距离从 2 降为 1。强度 `0.6` 不参与此次步数计算。

去掉新增行，再从输入中删除 `("Park", "Choi", {"weight": 0.7})`。Choi 从输入边中消失；代码按边创建节点，因此节点列表变为 `['Kim', 'Lee', 'Park']`。若要保留孤立的 Choi，应在创建图后显式调用 `friend_graph.add_node("Choi")`。这样 Choi 存在，但从 Kim 无法到达。

改变图中节点位置不同于增删边。只移动位置而保留连接，邻居与路径不会改变。

## 再次输入同一连接

`nx.Graph()` 不会在同一对节点间累计多条边。调用 `friend_graph.add_edge("Kim", "Park", weight=0.5)`，原权重从 `0.9` 变为 `0.5`，边数不增加。要分别保留点击或交易事件，需要事件表或支持多重边的结构。

孤立节点存在与节点不存在不同。显式添加的孤立 Choi 不会出现在 Kim 的可达距离结果中，这不表示距离为 0：0 表示起点本身，无路径是另一种状态。

## 检查清单

- 能用节点与边解释图。
- 能将邻接表解释为每个节点的邻居列表。
- 能说明表与图强调的不同问题。
- 能初步解释树是图的特殊形式。
- 能区分无向图与有向图。
- 能解释权重为关系附加数值信息。
- 能用邻居列表表示小型图并沿连接移动。
- 能读懂 NetworkX 如何处理节点、边、邻居、方向与权重。
- 能识别连接关系重要的数据，并采用图视角。
- 能区分最少步数与最低成本路径，以及边的更新与新连接的添加。

## 来源与参考资料

- Paul E. Black and Paul J. Tanenbaum, [graph](https://xlinux.nist.gov/dads/HTML/graph.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures, NIST，确认日期：2026-07-20。作为把 graph 说明为由 vertices/nodes 与 edges/arcs 构成的结构的依据。
- NetworkX Developers, [Graph - Undirected graphs with self loops](https://networkx.org/documentation/stable/reference/classes/graph.html){: target="_blank" rel="noopener noreferrer" }, NetworkX 3.6.1 documentation，确认日期：2026-07-20。用于从 Python 代码视角确认小型无向图、nodes、edges 和 adjacency relations。
- NetworkX Developers, [DiGraph - Directed graphs with self loops](https://networkx.org/documentation/stable/reference/classes/digraph.html){: target="_blank" rel="noopener noreferrer" }, NetworkX 3.6.1 documentation，确认日期：2026-07-20。用于确认 directed graphs 和 successor relationships。
- NetworkX Developers, [shortest_path](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.generic.shortest_path.html){: target="_blank" rel="noopener noreferrer" }, 核对日期：2026-09-15。用于区分无权最短路径与成本总和最小的路径。
- NetworkX Developers, [Graph.add_edge](https://networkx.org/documentation/stable/reference/classes/generated/networkx.Graph.add_edge.html){: target="_blank" rel="noopener noreferrer" }, 核对日期：2026-09-15。确认重复添加已有边会更新其属性。
