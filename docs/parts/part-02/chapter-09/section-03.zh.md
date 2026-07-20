# P2-9.3 图(graph)如何表达关系

> Section ID: `P2-9.3`
> Version: `v2026.07.20`

在 P2-9.2 中，我们把数组、表、树、图作为不同的数据视角进行了比较。其中图尤其容易让人感到陌生。

图并不只意味着图表或统计折线图。在数据结构和数学语境里，图是一种表达对象之间关系的结构。

这里说明 `graph`、`node`、`edge`、`direction`、`weight` 的基本区分。把 `data structure` 读成“一个问题”的代表性说明放在 P2-9.1，四种结构的比较放在 P2-9.2 和[概念词汇表](/AiBook/en/reference/concept-glossary/)中，而这里专注于：我们该用什么问题来阅读关系数据。

本节通过 node 和 edge 这两个最小概念来读图。

本节的重点不是图算法本身，而是该用什么结构来阅读关系数据。如果前一节是广泛比较数组、表、树、图，那么这里就是单独抓住那些“必须沿着连接往前走”的场景。这样读，图就不会和统计图表混淆，也能自然连接到后面的搜索、推荐和知识连接话题。

| 本节现在要抓住的内容 | 紧接着会延伸到的问题 | 之后再次出现的位置 |
| --- | --- | --- |
| 图是表达对象与对象之间连接的结构 | 会延伸到在 P2-9.4 补充学习里再次看传统数据结构名称时，图该放在什么位置 | 之后会在搜索结构、推荐关系、链接结构、知识图谱的说明中反复出现 |
| 表和图即使面对同一份数据，也是在问不同的问题 | 会延伸到判断该存成关系列表，还是按连接去阅读的标准 | 之后会在 RAG 连接结构、文档链接、用户-项目关系说明中再次使用 |
| 方向和权重会改变关系的含义 | 会延伸到如何读取不只是简单连接，还包括代价、距离和相似度 | 它会成为之后路径、推荐分数、搜索连接强度说明的基础 |

| 术语 | 本节先要抓住的含义 |
| --- | --- |
| graph | 一种把对象放成节点，再用边连接关系的结构 |
| node | 图中表示一个对象或一个位置的单位 |
| edge | 一个节点和另一个节点之间的连接 |
| direction | 表示连接朝向哪一边的性质 |
| weight | 附着在连接上的数值，用来表达强度、距离、代价等额外信息 |

## 本节的目标

- 能把图解释成节点与边构成的结构。
- 能说明图可以处理那些只靠表或树难以表达的连接关系。
- 能在入门层面解释无向图和有向图的区别。
- 能说明 weight 可以表达关系的强度、距离或代价等信息。
- 能把邻接表(adjacency list)解释成每个节点的邻居列表。
- 能读懂 Python 图工具如何通过 API 处理节点、边、邻居、方向和权重。

## 三个标准

| 标准 | 为什么重要 | 本节需要达到的理解程度 |
| --- | --- | --- |
| 图究竟表达什么 | 它帮助你把图读成关系结构，而不是统计图表 | 把它理解成表达对象之间连接关系的结构 |
| 表和图的区别 | 它能明确说明：即使是同一份数据，记录问题和连接问题也不同 | 只要抓住“表适合看记录，图适合沿连接前进”就够了 |
| direction 和 weight 的意义 | 它展示：连接性质一旦改变，关系解释也会跟着变化 | 只要能读出连接朝向哪边、强度有多大就足够了 |

## 图用点和线来表达关系

NIST 的 Dictionary of Algorithms and Data Structures 把图解释成“由边连接起来的一组项目”，并把每个项目解释成顶点(vertex)或节点(node)。

这里把它理解成下面这样。

图是一种把对象放成节点，再用边把对象之间关系连接起来的结构。

下面这张图同时用示意图和邻接表展示同一个图。

![A graph can be shown as nodes and edges or as an adjacency list](/AiBook/assets/part-02/chapter-09/graph-node-edge-adjacency-zh.svg)

图里的 `Kim`、`Lee`、`Park`、`Choi` 是节点。

像 `Kim -- Lee` 这样连接两个节点的线，就是边。

同样的关系也可以写成每个节点的邻居列表。

| 节点 | 邻居列表 |
| --- | --- |
| Kim | Lee, Park |
| Lee | Kim, Park |
| Park | Kim, Lee, Choi |
| Choi | Park |

这种表示方式可以看成邻接表(adjacency list)。核心点在于：每个节点都持有自己连接到的邻居列表。

## 表和图问的是不同的问题

同样的朋友关系数据，也可以写成一张表。表适合把“一条关系记录”写成一行。

| person | friend |
| --- | --- |
| Kim | Lee |
| Kim | Park |
| Lee | Park |
| Park | Choi |

但像 `谁和 Kim 相连？`、`能不能通过 Park 到 Choi？` 这样的问题，需要沿着连接往前走，因此图的视角更自然。

下面这张图展示了：同样的关系数据，在按表来读和按图来读时，问题会怎样变化。

![The same relationship records can be read as a table or a graph](/AiBook/assets/part-02/chapter-09/table-to-graph-reading-zh.svg)

如果想从图视角阅读表数据，可以把关系行重新整理成每个节点的邻居列表。

| 关系行列表 | 重新读成邻接表 |
| --- | --- |
| Kim - Lee | Kim: Lee, Park |
| Kim - Park | Lee: Kim, Park |
| Lee - Park | Park: Kim, Lee, Choi |
| Park - Choi | Choi: Park |

这里左边更接近表的行，右边更接近图的邻接表。即使是同样的数据，只要你提出的问题不同，更容易阅读的结构也会变化。

表和图的区别可以这样看。

| 视角 | 擅长提出的问题 | 例子 |
| --- | --- | --- |
| 表(table) | 哪一行有什么值？ | `person` 与 `friend` 的列表 |
| 图(graph) | 什么和什么相连？ | Kim 的邻居、经过 Park 的路径 |

并不是表不好、图才好。把关系存成列表时，表很好；当你需要沿着关系移动或观察连接结构时，图就更好。

## 用 Python 图工具处理关系

在 Python 中处理图关系时，也可以用字典和循环直接构造结构。但在实际分析或练习中，使用图专用工具通常更自然。NetworkX 是一个有代表性的 Python 图库。

下面这个例子的目的不是深入实现图算法，而是说明：把同一份关系数据放进 NetworkX 的 `Graph` 和 `DiGraph` 对象后，如何确认 node、edge、neighbor、two-hop neighbor、direction 和 weight。

问题场景：把朋友关系和页面链接关系分别做成无向图和有向图，再确认读取关系的基本 API。

输入(input)：朋友关系的 edge 列表，以及页面链接的 edge 列表。

期望输出(output)：确认节点列表、边列表、Kim 的直接邻居、Kim 的两跳邻居、Kim-Park 关系的权重、`page_b` 的下一条链接，以及 `page_c` 是否链接回 `page_b`。

要确认的概念：图工具会先把关系数据变成拥有节点和边的对象，然后通过 API 来询问邻居、方向、权重等图问题。

```python
# 这个例子用来确认图如何用节点、边、方向和权重来表示关系。
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

预期输出如下。

```text
friend nodes: ['Choi', 'Kim', 'Lee', 'Park']
friend edges: [('Choi', 'Park'), ('Kim', 'Lee'), ('Kim', 'Park'), ('Lee', 'Park')]
Kim neighbors: ['Lee', 'Park']
Kim two-hop neighbors: ['Choi']
Kim-Park weight: 0.9
page_b links to: ['page_c']
page_c links back to page_b: False
```

这个例子里，重要的不是输出格式。`nx.Graph()` 会创建像朋友关系那样可以双向阅读的连接，`nx.DiGraph()` 会创建像网页链接那样只能按一个方向阅读的连接。`neighbors()` 找出一个节点的直接邻居，`single_source_shortest_path_length()` 计算从起点到其他节点相隔几步。附在 edge 上的 `weight` 可以再次读成关系强度或代价等数字。

因此，这个 Python 例子不是“先把答案做好，只改变输出”的代码，而是用来确认图关系工具使用方式的例子。

## 树和图有什么不同

树可以被解释成图的一种特殊形式。NIST 对图的说明里，也把树提作图的一种。

这里这样区分。

树是层级很强的关系。

图是更一般的连接关系。

例如，一本书的目录通常更适合按树来读。

```text
study-book
└─ Part 2
   └─ Chapter 9
      └─ Section 9.3
```

但人与人之间的关系就很难整理成树。

```text
Kim -- Lee
Kim -- Park
Lee -- Park
Park -- Choi
```

在人际关系里，一个人可以连接很多人，连接也可能彼此回到对方。这种结构更适合图的视角。

## 无向图和有向图

图中的边可以没有方向，也可以有方向。

无向图在关系两边含义相同时使用。

当我们简单地看朋友关系时，可以写成 `Kim -- Lee`。如果 Kim 是 Lee 的朋友，那么也把 Lee 看成 Kim 的朋友。

在无向图里，同一个连接应该能从两个节点都读到。

| 节点 | 邻居 |
| --- | --- |
| Kim | Lee |
| Lee | Kim |

有向图在关系方向重要时使用。

例如网页链接就有方向。A 文档链接到 B 文档，不意味着 B 文档也会链接回 A 文档。

在有向图里，只写连接真正指向的一侧。

| 出发节点 | 指向节点 |
| --- | --- |
| page_a | page_b, page_c |
| page_b | page_c |
| page_c | 无 |

在 AI 和搜索语境里，方向往往非常重要。比如文档引用另一篇文档、工作流流向下一步，或用户点击一个项目，这些都可以看作有向图。

下面这张图展示了方向和权重会怎样改变边的意义。

![Direction and weight change what a graph edge means](/AiBook/assets/part-02/chapter-09/directed-weighted-graph-zh.svg)

阅读有向图时，不要假定关系在两边都存在。只读取关系真实指向的那一侧。

| 问题 | 回答 |
| --- | --- |
| `page_b` 指向的下一页是什么 | `page_c` |
| `page_c` 是否再次指向 `page_b` | 只看这张表，答案是否定的 |

在这个例子里，`page_b` 会链接到 `page_c`，但我们不能因此说 `page_c` 也会链接回 `page_b`。

## weight 会给关系附上数字

并不是所有连接都有同样的强度。有些关系更近，有些更远，有些代价更高。

这时，可以在边上附一个数字。这个数字就叫 weight。

例如，城市之间的距离可以用图来表达。

城市之间的距离也可以读成节点和边。

| 出发节点 | 到达节点 | 权重 |
| --- | --- | ---: |
| Seoul | Daejeon | 160 |
| Seoul | Busan | 325 |
| Daejeon | Busan | 200 |

这里的 `325` 就是附着在 Seoul 与 Busan 关系上的数字。在推荐系统里，这个数字可能是相似度；在搜索里，可能是分数；在网络里，可能是代价。

重要的是，weight 不是答案本身。它是用来解释关系的数字。

一旦附上 weight，问题就不会停在 `它们有没有连接？`，还会继续变成 `有多近？`、`成本有多大？`、`相关性有多强？`

在阅读搜索候选或推荐候选之间的关系分数时，也可以使用同样的视角。下面的场景只是把已经计算好的关系分数与基准线进行比较。

| 候选文档 | 与 query 的关系分数 | 与基准 `0.7` 比较 | 解释 |
| --- | ---: | --- | --- |
| `doc_a` | 0.91 | 高于基准 | 优先查看的强候选 |
| `doc_b` | 0.72 | 高于基准 | 可以一起查看的候选 |
| `doc_c` | 0.18 | 低于基准 | 在当前基准下可以后移的候选 |

这张表并没有实现搜索系统。它只是用一个很小的例子展示：在 AI 搜索或推荐里，会给关系附上数字，再按这些数字比较候选对象。

## 一步一步沿着连接前进

即使不实现图搜索算法，也可以通过表格确认图的直觉是 `沿着已连接的邻居往前走`。如果起点节点是 `Kim`，直接连接和再往外一步的连接会这样不同。

| 标准 | 包含的节点 | 阅读方式 |
| --- | --- | --- |
| 直接邻居 | Lee, Park | 与 Kim 直接相连的节点 |
| 两跳候选 | Choi | 沿着 Kim 的邻居再走一步时新遇到的节点 |

这里重要的不是循环本身，而是在图里，你可以从一个节点走向它连接的邻居，再从那些邻居走向它们的邻居。

沿着关系前进之后，就能分出 `直接连接` 和 `经过一步的连接`。

下面这张图展示了如何以 Kim 为中心区分直接邻居和两跳邻居。

![A graph distinguishes direct neighbors and two-hop neighbors](/AiBook/assets/part-02/chapter-09/graph-neighbor-hop-zh.svg)

这里的 `direct_neighbors` 是与 Kim 直接相连的节点，`two_hop_neighbors` 则是再往外走一步得到的节点，例如朋友的朋友。学习图，正是为了把这类连接问题当成数据来处理。

## 图的直觉会在 AI 实践里的哪些地方再次出现

图的直觉会在 P1-13.4 的向量搜索实现、P5-13 的向量数据库和索引说明，以及 Part 6 的工作流和搜索项目语境里再次出现。

| 场景 | 图的视角 |
| --- | --- |
| knowledge graph | 把概念、人物、地点、事件表达成节点，把关系表达成边 |
| recommender system | 表达用户与项目之间、项目与项目之间的连接 |
| search | 表达文档、链接、关键词、来源之间的连接 |
| RAG | 表达文档片段、元数据、来源、问题之间的关系 |
| workflow | 表达任务步骤和下一步骤之间的连接 |

本节不会深入解释每个领域的实现。向量搜索和索引会在 P1-13.4 与 P5-13 再次出现，工作流和搜索项目的连接会在 Part 6 再次出现。现在更重要的是先抓住：图是一种用于表达“关系很重要的数据”的方式。

## 容易误解的点

图并不只意味着统计图表或折线图。

在数据结构语境里，图是一种用节点和边来表达关系的结构。

图并不总是意味着复杂算法。

一个小图只用每个节点的邻居列表也能表达。

图并不一定比树更好。

如果层级很清楚，树更容易读；如果多方向连接更重要，图就更自然。

图中节点的位置只是帮助说明的可视化。

大多数情况下，节点在图里摆在哪里并不是关键。关键在于哪些节点通过边连接在一起。

## 通过案例来看

### 案例 1. 当我们想在推荐里看到“朋友的朋友”时，需要什么？

假设一个服务在做推荐时，不只想参考 `我直接看过的项目`，还想参考 `相似用户看过的项目`，甚至还想参考 `朋友的朋友经常看过的项目`。人一开始可能会觉得，把用户-项目记录存成一张表就足够了。

但这类问题要求的是沿着连接往前走，而不只是列出记录。因为你需要看到谁和谁相连、一跳邻居和两跳邻居分别是谁，以及关系的方向和强度如何。

图正是为这种场景准备的结构。节点会变成用户或文档，边会变成点击、朋友关系、链接或相似度这种连接。因此，像 `直接连接`、`经过一步的连接`、`高权重连接` 这样的问题，就能更自然地表达出来。

可检查的结果是：你能不能从一个节点开始往外跟着邻居走。例如，如果你能在代码里区分 Kim 的直接邻居和两跳邻居，那就说明你正在用图的视角来阅读原本存成表的关系。

## 检查清单

- 能把图解释成节点与边构成的结构。
- 能把邻接表解释成“每个节点对应一份邻居列表”。
- 能说明表和图回答的是不同的问题。
- 能在入门层面说明树是图的一种特殊形式。
- 能说明无向图和有向图的区别。
- 能说明 weight 会给关系加上数值信息。
- 能用节点邻居列表表示一个小图，并区分直接邻居和两跳邻居。
- 能读懂 NetworkX 这样的 Python 图工具如何处理 node、edge、neighbor、direction 和 weight。
- 当核心问题变成“沿着连接往前走”时，能先想起图的视角。

## 来源与参考资料

- Paul E. Black and Paul J. Tanenbaum, [graph](https://xlinux.nist.gov/dads/HTML/graph.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures, NIST，确认日期：2026-07-20。作为把 graph 说明为由 vertices/nodes 与 edges/arcs 构成的结构的依据。
- NetworkX Developers, [Graph - Undirected graphs with self loops](https://networkx.org/documentation/stable/reference/classes/graph.html){: target="_blank" rel="noopener noreferrer" }, NetworkX 3.6.1 documentation，确认日期：2026-07-20。用于从 Python 代码视角确认小型无向图、nodes、edges 和 adjacency relations。
- NetworkX Developers, [DiGraph - Directed graphs with self loops](https://networkx.org/documentation/stable/reference/classes/digraph.html){: target="_blank" rel="noopener noreferrer" }, NetworkX 3.6.1 documentation，确认日期：2026-07-20。用于确认 directed graphs 和 successor relationships。
