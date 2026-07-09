# P2-9.3 How Does a Graph Represent Relationships?

> Section ID: `P2-9.3`
> Version: `v2026.07.09`

In P2-9.2, we compared arrays, tables, trees, and graphs as different views of data. Among them, graphs can feel especially unfamiliar.

A graph does not mean only a chart or a statistical graph. In the context of data structures and mathematics, a graph is a structure that expresses relationships between objects.

This Section explains the basic distinctions among `graph`, `node`, `edge`, `direction`, and `weight`. The representative explanation that reads `data structure` as a question is placed in P2-9.1, and the comparison among the four structures is placed in P2-9.2 and the [Concept Glossary](../../../reference/concept-glossary.md). Here the focus is on what question lets us read relational data.

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

## Scope of This Section

This Section treats graphs from the viewpoint of relationship representation. The central question is, `How do we express connections between one object and another as data?`

This Section answers the following questions.

- What are nodes and edges?
- Why are graphs good for expressing relationships?
- How are undirected graphs and directed graphs different?
- What information does weight add to a relationship?
- How can a graph be expressed simply in Python?
- Where does graph intuition appear again in AI, search, recommendation, and RAG?

This Section does not go deeply into graph search algorithms, shortest paths, centrality, graph neural networks, or graph database implementation. Data-structure names and reading standards are organized again in the P2-9.4 supplement. The scene where graph intuition appears again as search structure continues in P1-13.4. The implementation of graph neural networks and graph databases stays outside the current scope of the main text.

## Goals of This Section

- You can explain a graph as a structure of nodes and edges.
- You can explain that a graph can handle connection relationships that are hard to express through tables or trees alone.
- You can explain the difference between an undirected graph and a directed graph at an introductory level.
- You can explain that weight can represent information such as the strength, distance, or cost of a relationship.
- You can express a small graph in Python through the adjacency-list style.

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

![A graph can be shown as nodes and edges or as an adjacency list](../../../assets/part-02/chapter-09/graph-node-edge-adjacency-en.svg)

In the picture, `Kim`, `Lee`, `Park`, and `Choi` are nodes.

A line connecting two nodes, such as `Kim -- Lee`, is an edge.

In a Python dictionary, we can express which neighbors each node has.

Problem situation: When representing human relations as a graph adjacency list, you want to pull out the neighbors directly connected to one person.
Input: A dictionary whose keys are person names and whose values are lists of neighbors.
Expected output: The list of neighbors directly connected to `Kim` is printed.
Concept to check: Confirm the adjacency-list intuition of storing a graph as a neighbor list for each node.

```python
friends = {
    "Kim": ["Lee", "Park"],
    "Lee": ["Kim", "Park"],
    "Park": ["Kim", "Lee", "Choi"],
    "Choi": ["Park"],
}

print(friends["Kim"])
```

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

![The same relationship records can be read as a table or a graph](../../../assets/part-02/chapter-09/table-to-graph-reading-en.svg)

To handle table data as a graph in Python, you can first convert the relationship list into an adjacency list.

Problem situation: You want to convert a friendship list written like the rows of a table into a graph structure and then read the neighbors of `Kim`.
Input: A list of `(person, friend)` pairs.
Expected output: After the relationship list is converted into an adjacency list, the list of neighbors of `Kim` is printed.
Concept to check: Confirm the flow of converting the same data from a relationship-row list into a graph adjacency list.

```python
friend_pairs = [
    ("Kim", "Lee"),
    ("Kim", "Park"),
    ("Lee", "Park"),
    ("Park", "Choi"),
]

friends = {}

for person, friend in friend_pairs:
    friends.setdefault(person, []).append(friend)
    friends.setdefault(friend, []).append(person)

print(friends["Kim"])
```

Here, `friend_pairs` is closer to table rows, while `friends` is closer to a graph adjacency list. Even with the same data, the structure that is easier to read changes depending on what question you ask.

The difference between a table and a graph can be viewed as follows.

| Viewpoint | Question it asks well | Example |
| --- | --- | --- |
| table | Which row has which value? | a list of `person` and `friend` |
| graph | What is connected to what? | Kim's neighbors, a path through Park |

It is not that the table is bad and the graph is good. Tables are good for storing relationships as lists, while graphs are good when you need to move through relationships or inspect the connection structure.

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

Problem situation: You want to express a symmetric friendship relation like an undirected graph.
Input: A short adjacency list where `Kim` and `Lee` are connected to each other.
Expected output: There is no printed output, but you confirm the structure where both nodes contain each other's names.
Concept to check: In an undirected graph, the relationship is written on both nodes.

```python
friends = {
    "Kim": ["Lee"],
    "Lee": ["Kim"],
}
```

A directed graph is used when the direction of the relationship matters.

For example, a web link has direction. If document A links to document B, that does not mean document B links back to document A.

Problem situation: You want to write a directed relationship such as web-document links as a graph.
Input: A dictionary showing where each page links.
Expected output: There is no printed output, but you confirm the structure where only the outgoing side of the relationship is stored.
Concept to check: In a directed graph, the connection is not assumed to be bidirectional.

```python
links = {
    "page_a": ["page_b", "page_c"],
    "page_b": ["page_c"],
    "page_c": [],
}
```

In AI and search contexts, direction is often important. Cases such as a document citing another document, a workflow moving to the next step, or a user clicking an item can all be viewed as directed graphs.

The diagram below shows how direction and weight change the meaning of an edge.

![Direction and weight change what a graph edge means](../../../assets/part-02/chapter-09/directed-weighted-graph-en.svg)

When expressing a directed graph in code, we do not put the relationship on both sides. We record only the side toward which the relationship actually points.

Problem situation: In a directed graph, you want to check only where a specific page actually points.
Input: A dictionary containing outgoing-link lists by page.
Expected output: The list of next pages pointed to by `page_b` is printed.
Concept to check: Confirm that a directed graph reads connections from the viewpoint of the source node.

```python
page_links = {
    "page_a": ["page_b", "page_c"],
    "page_b": ["page_c"],
    "page_c": [],
}

print(page_links["page_b"])
```

In this example, `page_b` links to `page_c`, but we cannot say that `page_c` links back to `page_b`.

## Weight Attaches Numbers to Relationships

Not every connection has the same strength. Some relationships are close, some are far, and some are costly.

At that point, a number can be attached to the edge. That number is called a weight.

For example, distances between cities can be expressed as a graph.

Problem situation: You want to read the cost between two cities by attaching distance numbers to the connections between cities.
Input: A nested-dictionary structure that uses city names as keys and stores neighboring cities together with distance values.
Expected output: The distance value from `Seoul` to `Busan` is printed.
Concept to check: See that by attaching weights to graph edges, the strength or cost of the connection can be read numerically.

```python
distances = {
    "Seoul": {"Daejeon": 160, "Busan": 325},
    "Daejeon": {"Seoul": 160, "Busan": 200},
    "Busan": {"Seoul": 325, "Daejeon": 200},
}

print(distances["Seoul"]["Busan"])
```

Here, `325` is the number attached to the relationship between Seoul and Busan. In a recommendation system, that number may be similarity. In search, it may be a score. In a network, it may be a cost.

What matters is that weight is not the answer itself. It is a number used to interpret the relationship.

Once weight is attached, the question no longer ends with `Are they connected?` It can extend to `How close are they?`, `How much does it cost?`, or `How strongly are they related?`

Problem situation: You want to select only relationships above a threshold from relation scores between a query and recommendation or search candidates.
Input: A dictionary containing similarity scores between a query and documents.
Expected output: Only documents with scores of `0.7` or higher, together with their scores, are printed.
Concept to check: Confirm that in a weighted graph, connections can be interpreted by a score threshold.

```python
similarity = {
    "query": {"doc_a": 0.91, "doc_b": 0.72, "doc_c": 0.18},
}

for document, score in similarity["query"].items():
    if score >= 0.7:
        print(document, score)
```

This code does not implement a search system. It only shows in a small form the intuition used in AI search or recommendation, where numbers are attached to relationships and candidates are compared.

## Following a Graph in Small Python Steps

The following example is not code that fully implements a graph-search algorithm. It is only a small example for confirming the sense that a graph means `following connected neighbors`.

Problem situation: You want to follow only one step from one person and inspect the directly connected neighbors.
Input: A dictionary writing human relations as an adjacency list, and the start node `Kim`.
Expected output: The names of Kim's direct neighbors are printed in order.
Concept to check: See that in a graph, you can take out the neighbor list from a start node and move one step.

```python
friends = {
    "Kim": ["Lee", "Park"],
    "Lee": ["Kim", "Park"],
    "Park": ["Kim", "Lee", "Choi"],
    "Choi": ["Park"],
}

start = "Kim"

print("Neighbors of Kim:")
for neighbor in friends[start]:
    print("-", neighbor)
```

If you go one step further, you can also see the friends of Kim's friends.

Problem situation: You want to gather not direct friends but also friends of friends by extending one more step.
Input: The friendship dictionary above and the start node `Kim`.
Expected output: The set of friends of friends except `Kim` is printed.
Concept to check: Confirm that by following the neighbors of a node again, you can collect two-step connections.

```python
friends_of_friends = set()

for neighbor in friends["Kim"]:
    for next_neighbor in friends[neighbor]:
        if next_neighbor != "Kim":
            friends_of_friends.add(next_neighbor)

print(friends_of_friends)
```

What matters in this example is not the loop itself. It is the fact that in a graph, you can move from one node to its connected neighbors, and then move again to those neighbors' neighbors.

When you follow relationships, you can distinguish `direct connection` from `connection through one step`.

The diagram below shows the distinction between direct neighbors and two-hop neighbors around Kim.

![A graph distinguishes direct neighbors and two-hop neighbors](../../../assets/part-02/chapter-09/graph-neighbor-hop-en.svg)

Problem situation: You want to compare direct connections and two-step connections separately.
Input: The direct neighbors of `Kim` and the neighbors of those neighbors in the friendship dictionary.
Expected output: A direct-neighbor set and a two-hop-neighbor set are printed separately.
Concept to check: Confirm that in a graph, a one-step difference in connection distance divides the result into different sets.

```python
direct_neighbors = set(friends["Kim"])
two_hop_neighbors = set()

for neighbor in direct_neighbors:
    two_hop_neighbors.update(friends[neighbor])

two_hop_neighbors.discard("Kim")
two_hop_neighbors = two_hop_neighbors - direct_neighbors

print("direct:", direct_neighbors)
print("two hop:", two_hop_neighbors)
```

Here, `direct_neighbors` are the nodes directly connected to Kim, while `two_hop_neighbors` are the nodes reached one step further, such as friends of friends. The reason for learning graphs is to be able to handle these connection questions as data.

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

A small graph can be expressed even with only Python dictionaries and lists.

Graph is not unconditionally better than a tree.

If the hierarchy is clear, a tree is easier to read. If connections in many directions matter, a graph is more natural.

The placement of nodes in a graph picture is only a visualization to help explanation.

In most cases, where a node is placed in the drawing is not the key point. What matters is which nodes are connected by edges.

## Perspectives to Remember from This Section

Graphs are structures for expressing relationships.

Nodes are objects.

Edges are the connections between objects.

An adjacency list is a way of writing which neighbors each node is connected to.

Direction expresses the flow of a relationship, and weight expresses the strength or cost of a relationship.

In AI practice, graphs appear again when understanding knowledge, recommendation, search, document links, and workflows.

## Case Study

### Case 1. What is needed when we want to see friends of friends in recommendation?

Suppose a service wants to use not only `items I directly viewed`, but also `items viewed by similar users` or even `items often viewed by friends of friends` when making recommendations. At first, a person may feel that storing user-item records in a table is enough.

But questions like these require following connections rather than merely listing records. You need to see who is connected to whom, who the one-step and two-step neighbors are, and what the direction or strength of the relationships is.

Graphs are exactly the structure for reading such scenes. Nodes become users or documents, and edges become connections such as clicks, friendships, links, or similarity. That is why questions such as `direct connection`, `connection through one step`, and `high-weight connection` can be expressed more naturally.

The checkable result is whether you can follow neighbors from one node. For example, if you can distinguish Kim's direct neighbors and two-step neighbors in code, then you are reading the table-stored relationships from the graph viewpoint.

## Short Check

- You can explain a graph as a structure of nodes and edges.
- You can explain an adjacency list as the list of neighbors of each node.
- You can explain that a table and a graph answer different questions.
- You can explain at an introductory level that a tree is a special form of graph.
- You can explain the difference between an undirected graph and a directed graph.
- You can explain that weight adds numerical information to a relationship.
- You can express a small graph with Python dictionaries and lists and follow neighbors.

## When Should You Recall This Perspective First?

- Recall the graph viewpoint first when you need to explain that the core of the data lies not in the items themselves but in the connections among items.
- When you meet problems such as recommendation, path finding, or knowledge links, where you need to follow neighbors and relationships, return to the node-edge explanation in this Section.
- Check again here when you want to express connection structures that tables do not reveal well or when you want to verify a small example directly in Python.

## Sources and References

- Paul E. Black and Paul J. Tanenbaum, [graph](https://xlinux.nist.gov/dads/HTML/graph.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures, NIST, checked 2026-06-25.
- NetworkX Developers, [Graph - Undirected graphs with self loops](https://networkx.org/documentation/stable/reference/classes/graph.html){: target="_blank" rel="noopener noreferrer" }, NetworkX documentation, checked 2026-06-25.
