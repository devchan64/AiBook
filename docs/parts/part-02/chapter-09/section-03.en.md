# P2-9.3 How Does a Graph Represent Relationships?

> Section ID: `P2-9.3`
> Version: `v2026.07.20`

In P2-9.2, we compared arrays, tables, trees, and graphs as different views of data. Among them, graphs can feel especially unfamiliar.

A graph does not mean only a chart or a statistical graph. In the context of data structures and mathematics, a graph is a structure that expresses relationships between objects.

This Section explains the basic distinctions among `graph`, `node`, `edge`, `direction`, and `weight`. The representative explanation that reads `data structure` as a question is placed in P2-9.1, and the comparison among the four structures is placed in P2-9.2 and the [Concept Glossary](/AiBook/reference/concept-glossary/). Here the focus is on what question lets us read relational data.

This Section reads graphs through the minimum concepts of node and edge.

Rather than focusing on graph algorithms themselves, this Section focuses on what structure should be used to read relational data. If the previous Section compared arrays, tables, trees, and graphs broadly, here we isolate only the scenes where the question of following connections is especially needed. Read this way, graphs do not get confused with statistical charts, and the discussion also connects naturally to later topics such as search, recommendation, and knowledge links.

| What to capture in this Section now | The question that follows immediately next | Where it appears again later |
| --- | --- | --- |
| The point that a graph is a structure expressing connections between one object and another | It leads to where graphs should be placed when looking again at traditional data-structure names in the P2-9.4 supplement | It repeats later in explanations of search structure, recommendation relations, link structure, and knowledge graphs |
| The point that tables and graphs ask different questions even over the same data | It leads to the criterion for deciding whether to store a relationship list or read by following connections | It is used again later in explanations of RAG connection structure, document links, and user-item relations |
| The point that direction and weight change the meaning of a relationship | It leads to the standard for reading not only simple connection but also cost, distance, and similarity | It becomes the basis later for path, recommendation-score, and search-link-strength explanations |

| Term | Meaning to capture first in this Section |
| --- | --- |
| graph | A structure that places objects as nodes and connects relationships as edges |
| node | A unit representing one object or point in a graph |
| edge | A connection between one node and another |
| direction | A property that shows toward which side a connection points |
| weight | A value attached to a connection to represent extra information such as strength, distance, or cost |

## Goals of This Section

- You can explain a graph as a structure of nodes and edges.
- You can explain that a graph can handle connection relationships that are hard to express through tables or trees alone.
- You can explain the difference between an undirected graph and a directed graph at an introductory level.
- You can explain that weight can represent information such as the strength, distance, or cost of a relationship.
- You can explain an adjacency list as a list of neighbors for each node.
- You can read how a Python graph tool handles nodes, edges, neighbors, direction, and weight through its API.

## Three Criteria

| Criterion | Why it matters | Level of understanding needed in this Section |
| --- | --- | --- |
| What a graph represents | It helps you read a graph as a relationship structure rather than a statistical chart | Understand it as a structure expressing connections between one object and another |
| The difference between a table and a graph | It makes clear that even over the same data, the storage question and the connection question are different | It is enough to hold the distinction that tables are good for viewing records, while graphs are good for following connections |
| The meaning of direction and weight | It shows that once the nature of the connection changes, the interpretation of the relationship changes too | It is enough if you can read which way a connection points and how strong it is |

## A Graph Expresses Relationships with Points and Lines

The NIST Dictionary of Algorithms and Data Structures explains a graph as a set of items connected by edges, and explains each item as a vertex or node.

Understand it here as follows.

A graph is a structure that places objects as nodes and connects the relationships between objects as edges.

The diagram below shows the same graph both as a picture and as an adjacency list.

![A graph can be shown as nodes and edges or as an adjacency list](/AiBook/assets/part-02/chapter-09/graph-node-edge-adjacency-en.svg)

In the picture, `Kim`, `Lee`, `Park`, and `Choi` are nodes.

A line connecting two nodes, such as `Kim -- Lee`, is an edge.

The same relationship can also be written as a neighbor list for each node.

| Node | Neighbor List |
| --- | --- |
| Kim | Lee, Park |
| Lee | Kim, Park |
| Park | Kim, Lee, Choi |
| Choi | Park |

This representation can be seen as an adjacency list. The core point is that each node holds a list of connected neighbors.

## Tables and Graphs Ask Different Questions

The same friendship data can also be written as a table. A table is good for writing one relationship record as one row.

| person | friend |
| --- | --- |
| Kim | Lee |
| Kim | Park |
| Lee | Park |
| Park | Choi |

But for questions such as `Who is connected to Kim?` or `Can we get to Choi through Park?`, the graph viewpoint is more natural because you need to follow the connections.

The diagram below shows how the question changes when the same relational data is read as a table and when it is read as a graph.

![The same relationship records can be read as a table or a graph](/AiBook/assets/part-02/chapter-09/table-to-graph-reading-en.svg)

To read table data through a graph viewpoint, you can regroup relationship rows into a neighbor list for each node.

| Relationship Rows | Read Again as an Adjacency List |
| --- | --- |
| Kim - Lee | Kim: Lee, Park |
| Kim - Park | Lee: Kim, Park |
| Lee - Park | Park: Kim, Lee, Choi |
| Park - Choi | Choi: Park |

Here, the left side is closer to table rows, while the right side is closer to a graph adjacency list. Even with the same data, the structure that is easier to read changes depending on what question you ask.

The difference between a table and a graph can be viewed as follows.

| Viewpoint | Question it asks well | Example |
| --- | --- | --- |
| table | Which row has which value? | a list of `person` and `friend` |
| graph | What is connected to what? | Kim's neighbors, a path through Park |

It is not that the table is bad and the graph is good. Tables are good for storing relationships as lists, while graphs are good when you need to move through relationships or inspect the connection structure.

## Trying Relationships with a Python Graph Tool

When handling graph relationships in Python, you can build the structure directly with dictionaries and loops, but in real analysis or practice it is often more natural to use a graph-specific tool. A representative Python graph library is NetworkX.

The purpose of the example below is not to implement graph algorithms in depth. It is an explanatory example that shows how to check nodes, edges, neighbors, two-hop neighbors, direction, and weight after placing the same relationship data into NetworkX `Graph` and `DiGraph` objects.

Problem situation: Build friendship relationships and page-link relationships as an undirected graph and a directed graph, then check the basic APIs used to read the relationships.

Input: a friendship edge list and a page-link edge list.

Expected output: confirm the node list, edge list, Kim's direct neighbors, Kim's two-hop neighbors, the weight of the Kim-Park relationship, the next link from `page_b`, and whether `page_c` links back to `page_b`.

Concept to check: a graph tool lets you turn relationship data into an object with nodes and edges, then ask graph questions through APIs for neighbors, direction, and weight.

```python
# This example checks how a graph represents relationships with nodes, edges, direction, and weight.
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

The expected output is as follows.

```text
friend nodes: ['Choi', 'Kim', 'Lee', 'Park']
friend edges: [('Choi', 'Park'), ('Kim', 'Lee'), ('Kim', 'Park'), ('Lee', 'Park')]
Kim neighbors: ['Lee', 'Park']
Kim two-hop neighbors: ['Choi']
Kim-Park weight: 0.9
page_b links to: ['page_c']
page_c links back to page_b: False
```

What matters in this example is not the output format. `nx.Graph()` creates a connection that can be read both ways, such as a friendship relationship, while `nx.DiGraph()` creates a connection that is read in one direction, such as a web link. `neighbors()` finds the direct neighbors of one node, and `single_source_shortest_path_length()` calculates how many steps away each node is from the start node. The `weight` attached to an edge can be read again as a number such as relationship strength or cost.

So this Python example is not code that prepares the answer in advance and merely changes the printed output. It is an example for checking how to use a tool that handles graph relationships.

## How Are Trees and Graphs Different?

A tree can be explained as a special form of graph. NIST's graph explanation also mentions trees as one kind of graph.

Distinguish them here like this.

A tree is a strongly hierarchical relationship.

A graph is a more general connection relationship.

For example, a book's table of contents is usually read well as a tree.

```text
study-book
└─ Part 2
   └─ Chapter 9
      └─ Section 9.3
```

But relationships among people are difficult to organize as a tree.

```text
Kim -- Lee
Kim -- Park
Lee -- Park
Park -- Choi
```

In human relationships, one person can connect to many people, and connections can return to one another. For such structures, the graph viewpoint is more natural.

## Undirected Graphs and Directed Graphs

A graph's edge may have no direction, or it may have direction.

An undirected graph is used when the relationship has the same meaning in both directions.

When we view friendship simply, we can write `Kim -- Lee`. If Kim is a friend of Lee, then Lee is also treated as a friend of Kim.

In an undirected graph, the same connection should be readable from both nodes.

| Node | Neighbor |
| --- | --- |
| Kim | Lee |
| Lee | Kim |

A directed graph is used when the direction of the relationship matters.

For example, a web link has direction. If document A links to document B, that does not mean document B links back to document A.

In a directed graph, you write only the side toward which the connection points.

| Source Node | Points To |
| --- | --- |
| page_a | page_b, page_c |
| page_b | page_c |
| page_c | none |

In AI and search contexts, direction is often important. Cases such as a document citing another document, a workflow moving to the next step, or a user clicking an item can all be viewed as directed graphs.

The diagram below shows how direction and weight change the meaning of an edge.

![Direction and weight change what a graph edge means](/AiBook/assets/part-02/chapter-09/directed-weighted-graph-en.svg)

When reading a directed graph, we do not assume that the relationship exists on both sides. We read only the side toward which the relationship actually points.

| Question | Answer |
| --- | --- |
| What next page does `page_b` point to? | `page_c` |
| Does `page_c` point back to `page_b`? | Not from this table |

In this example, `page_b` links to `page_c`, but we cannot say that `page_c` links back to `page_b`.

## Weight Attaches Numbers to Relationships

Not every connection has the same strength. Some relationships are close, some are far, and some are costly.

At that point, a number can be attached to the edge. That number is called a weight.

For example, distances between cities can be expressed as a graph.

Distances between cities can also be read as nodes and edges.

| Source Node | Target Node | Weight |
| --- | --- | ---: |
| Seoul | Daejeon | 160 |
| Seoul | Busan | 325 |
| Daejeon | Busan | 200 |

Here, `325` is the number attached to the relationship between Seoul and Busan. In a recommendation system, that number may be similarity. In search, it may be a score. In a network, it may be a cost.

What matters is that weight is not the answer itself. It is a number used to interpret the relationship.

Once weight is attached, the question no longer ends with `Are they connected?` It can extend to `How close are they?`, `How much does it cost?`, or `How strongly are they related?`

The same viewpoint can be used when reading relationship scores among search or recommendation candidates.

| Candidate Document | Relationship Score to Query | Compared with `0.7` | Interpretation |
| --- | ---: | --- | --- |
| `doc_a` | 0.91 | Above threshold | Strong candidate to inspect first |
| `doc_b` | 0.72 | Above threshold | Candidate to inspect together |
| `doc_c` | 0.18 | Below threshold | Candidate to defer under the current threshold |

This table does not implement a search system. It only shows the intuition used in AI search or recommendation, where numbers are attached to relationships and candidates are compared against a baseline.

## Following Connections One Step at a Time

Even without implementing a graph-search algorithm, the sense that a graph means `following connected neighbors` can be checked in a table. If the start node is `Kim`, direct connections and one-step-further connections differ like this.

| Criterion | Included Nodes | How to Read It |
| --- | --- | --- |
| Direct neighbors | Lee, Park | Nodes directly connected to Kim |
| Two-hop candidates | Choi | New node reached by following Kim's neighbors one more step |

What matters in this example is not the loop itself. It is the fact that in a graph, you can move from one node to its connected neighbors, and then move again to those neighbors' neighbors.

When you follow relationships, you can distinguish `direct connection` from `connection through one step`.

The diagram below shows the distinction between direct neighbors and two-hop neighbors around Kim.

![A graph distinguishes direct neighbors and two-hop neighbors](/AiBook/assets/part-02/chapter-09/graph-neighbor-hop-en.svg)

Here, direct neighbors are the nodes directly connected to Kim, while two-hop neighbors are nodes reached one step further, such as friends of friends. The reason for learning graphs is to be able to handle these connection questions as data.

## Where Graph Intuition Appears Again in AI Practice

Graph intuition appears again in the vector-search implementation of P1-13.4, the vector-database and index explanation of P5-13, and the workflow and search project contexts of Part 6.

| Scene | Graph viewpoint |
| --- | --- |
| knowledge graph | express concepts, people, places, and events as nodes and relationships as edges |
| recommender system | express connections between users and items, and between items and items |
| search | express connections among documents, links, keywords, and sources |
| RAG | express relations among document chunks, metadata, sources, and questions |
| workflow | express connections between task steps and next steps |

This Section does not explain the implementation of each field in depth. Vector search and indices appear again in P1-13.4 and P5-13, and workflow and search-project connections appear again in Part 6. For now, what matters is capturing the sense that a graph is a way of representing data where relationships matter.

## Points Easy to Misunderstand

Graph does not mean only a statistical chart or a line graph.

In the data-structure context, a graph is a structure that expresses relationships with nodes and edges.

Graph does not always mean complicated algorithms.

A small graph can be expressed as neighbor lists for each node.

Graph is not unconditionally better than a tree.

If the hierarchy is clear, a tree is easier to read. If connections in many directions matter, a graph is more natural.

The placement of nodes in a graph picture is only a visualization to help explanation.

In most cases, where a node is placed in the drawing is not the key point. What matters is which nodes are connected by edges.

## Case Study

### Case 1. What is needed when we want to see friends of friends in recommendation?

Suppose a service wants to use not only `items I directly viewed`, but also `items viewed by similar users` or even `items often viewed by friends of friends` when making recommendations. At first, a person may feel that storing user-item records in a table is enough.

But questions like these require following connections rather than merely listing records. You need to see who is connected to whom, who the one-step and two-step neighbors are, and what the direction or strength of the relationships is.

Graphs are exactly the structure for reading such scenes. Nodes become users or documents, and edges become connections such as clicks, friendships, links, or similarity. That is why questions such as `direct connection`, `connection through one step`, and `high-weight connection` can be expressed more naturally.

The checkable result is whether you can follow neighbors from one node. For example, if you can distinguish Kim's direct neighbors and two-step neighbors, then you are reading the table-stored relationships from the graph viewpoint.

## Checklist

- You can explain a graph as a structure of nodes and edges.
- You can explain an adjacency list as the list of neighbors of each node.
- You can explain that a table and a graph answer different questions.
- You can explain at an introductory level that a tree is a special form of graph.
- You can explain the difference between an undirected graph and a directed graph.
- You can explain that weight adds numerical information to a relationship.
- You can express a small graph as neighbor lists and follow neighbors.
- You can read how a Python graph tool such as NetworkX handles nodes, edges, neighbors, direction, and weight.
- You can recall the graph viewpoint first when the core question is about following connections.

## Sources and References

- Paul E. Black and Paul J. Tanenbaum, [graph](https://xlinux.nist.gov/dads/HTML/graph.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures, NIST, checked on 2026-07-20. Used as the basis for explaining a graph as a structure made of vertices/nodes and edges/arcs.
- NetworkX Developers, [Graph - Undirected graphs with self loops](https://networkx.org/documentation/stable/reference/classes/graph.html){: target="_blank" rel="noopener noreferrer" }, NetworkX 3.6.1 documentation, checked on 2026-07-20. Used to confirm small undirected graphs, nodes, edges, and adjacency relations.
- NetworkX Developers, [DiGraph - Directed graphs with self loops](https://networkx.org/documentation/stable/reference/classes/digraph.html){: target="_blank" rel="noopener noreferrer" }, NetworkX 3.6.1 documentation, checked on 2026-07-20. Used to confirm directed graphs and successor relationships.
