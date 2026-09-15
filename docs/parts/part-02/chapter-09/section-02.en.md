# P2-9.2 Intuition for Arrays, Tables, Trees, and Graphs

> Section ID: `P2-9.2`
> Version: `v2026.09.15`

## Positions, Rows and Columns, Hierarchies, and Connections

Arrays emphasize positions and axes; tables emphasize rows and columns; trees emphasize hierarchies; graphs emphasize connections.

![Arrays, tables, trees, and graphs answer different data questions](/AiBook/assets/part-02/chapter-09/data-structure-four-views-en.svg)

| Structure | Main question | Basic units | AI examples |
| --- | --- | --- | --- |
| Array | Which position holds a value? | Index, axis, value | Vectors, matrices, image pixels, embeddings |
| Table | Which row and column? | Row, column, cell | CSV datasets, training data, evaluations |
| Tree | How are upper and lower levels organized? | Root, parent, child | Contents, folders, taxonomies, decisions |
| Graph | What connects to what? | Node, edge | Links, recommendations, knowledge graphs, search |

These views overlap. A table column can be computed with as an array, a tree is a special kind of graph, and a graph can be represented with Python dictionaries and lists.

Calculating means, comparing student attributes, finding membership, and finding friends require different information.

![Choose a structure according to the question](/AiBook/assets/part-02/chapter-09/question-to-structure-map-en.svg)

## Arrays: Positions and Axes

An array accesses values by index. NumPy defines `ndarray` as a multidimensional container of items with the same type and size. Numerical arrays arrange numbers at specified positions along axes.

A one-dimensional numerical array is a row of numbers.

Retrieving indices `0` and `2` from `[0.12, -0.03, 0.44, 0.18]` prints `0.12` and `0.44`.

```python
import numpy as np

embedding = np.array([0.12, -0.03, 0.44, 0.18])

print(embedding[0])
print(embedding[2])
```

A two-dimensional array resembles a numerical grid of rows and columns.

In this 2-by-3 array, the first row's third value is `40`, and the second row's second value is `30`. Zero-based indexing reads them as `[0, 2]` and `[1, 1]`.

```python
import numpy as np

image_patch = np.array([
    [0, 20, 40],
    [10, 30, 50],
])

print(image_patch[0, 2])
print(image_patch[1, 1])
```

Position matters as well as value. Rearranging pixels changes an image, and embedding coordinates must retain their intended order for computation.

Array thinking appears in these AI tasks:

- Convert a sentence to a sequence of token IDs.
- Represent words, sentences, or images as embedding vectors.
- Batch samples into a matrix.
- Represent images along height, width, and channel axes.

NumPy arrays can apply the same operation to many numbers.

For example, calculating a mean can be simpler after extracting scores from the full table.

Scores `[82, 75, 45]` total 202 across 3 items, giving a mean of about 67.33. The code prints `67.33333333333333`.

```python
import numpy as np

scores = np.array([82, 75, 45])

average = scores.mean()
print(average)
```

The mean does not need names or labels. Reordering scores leaves the mean unchanged, but student lookup still requires the correspondence between students and array positions.

## Array Shape and Axis-Based Calculations

A 2-row, 3-column array has shape `(2, 3)`. Axis 0 runs across rows and axis 1 across columns; a mean combines values along the specified axis.

```python
import numpy as np

patch = np.array([[0, 20, 40], [10, 30, 50]])
print(patch.shape)
print(patch.mean(axis=0).tolist())
print(patch.mean(axis=1).tolist())
```

The outputs are `(2, 3)`, `[5.0, 25.0, 45.0]`, and `[20.0, 30.0]`. `axis=0` combines the two rows into three column means; `axis=1` combines the three values in each row into two row means. Identify which values are grouped instead of merely memorizing axis numbers.

`patch.reshape(3, 2)` preserves six elements while regrouping them into 3 rows and 2 columns. It does not understand pixel locations or student attributes. `reshape(2, 2)` needs four elements and raises `ValueError`. A valid shape and preserved data meaning are separate checks.

## Tables: Rows and Columns

A table represents data through rows and columns. pandas describes a DataFrame as two-dimensional, size-mutable, potentially heterogeneous tabular data with labeled row and column axes.

A table places one case in each row and one attribute in each column.

| name | age | score | label |
| --- | ---: | ---: | --- |
| Kim | 21 | 82 | pass |
| Lee | 20 | 75 | pass |
| Park | 22 | 45 | fail |

Small tables can be represented with Python lists and dictionaries.

Represent each row as a dictionary and collect them in a list. The code prints `Kim 82`, `Lee 75`, and `Park 45`.

```python
students = [
    {"name": "Kim", "age": 21, "score": 82, "label": "pass"},
    {"name": "Lee", "age": 20, "score": 75, "label": "pass"},
    {"name": "Park", "age": 22, "score": 45, "label": "fail"},
]

for student in students:
    print(student["name"], student["score"])
```

A table's meaning depends on what one row and one column represent.

Table thinking appears in these AI tasks:

- Read a CSV file as a dataset.
- Separate input features from target labels.
- Compare results across models or experiments.
- Inspect missing values, outliers, and data types.

Tables organize cases and attributes. They can become arrays for numerical computation, while remaining easier for people to review and explain.

Selecting students who passed is often more natural with records than with a score array alone.

Using the earlier `students`, collect names whose label is `"pass"`. The output is `['Kim', 'Lee']`.

```python
passed_students = []

for student in students:
    if student["label"] == "pass":
        passed_students.append(student["name"])

print(passed_students)
```

Here the question involves several attributes of each case, not just arithmetic. Rows and columns preserve those associations.

## Trees: Parents and Children

A rooted tree descends from a root through parent-child relationships. NIST describes a tree as accessed through a root node, with internal nodes having one or more children.

In a rooted tree, every node other than the root has one parent.

```text
study-book
├─ Part 1. Introduction
│  ├─ Chapter 1
│  └─ Chapter 2
└─ Part 2. Foundations
   ├─ Chapter 8
   └─ Chapter 9
```

Python dictionaries and lists can represent a small tree.

Place two topic groups under root `study-course`. The code prints the immediate children's titles, `Foundations` and `Data Work`.

```python
course_tree = {
    "title": "study-course",
    "children": [
        {"title": "Foundations", "children": ["Variables", "Functions"]},
        {"title": "Data Work", "children": ["Tables", "Graphs"]},
    ],
}

for part in course_tree["children"]:
    print(part["title"])
```

Hierarchy and paths matter: which item belongs under another, and how to descend from a starting point.

Tree thinking appears in these AI and service tasks:

- Read document contents and section hierarchies.
- Work with folders and file paths.
- Build taxonomies or categories.
- Understand decision trees.
- Read nested JSON or HTML structures.

Trees organize relationships hierarchically. They cannot represent every relationship, but suit data with clear upper and lower levels.

A tree asks what lies beneath an item, such as which chapters belong to a given Part.

Finding `"Data Work"` in the earlier `course_tree` and printing its children gives `['Tables', 'Graphs']`.

```python
for item in course_tree["children"]:
    if item["title"] == "Data Work":
        print(item["children"])
```

The key idea here is the path from the root to a location, rather than numerical size or a table column.

## Graphs: Nodes and Connections

Graphs represent connections between objects. NIST describes them as items connected by edges, with each item called a vertex or node.

Nodes are objects; edges are connections.

```text
Kim -- Lee
Kim -- Park
Lee -- Choi
Park -- Choi
```

A small Python graph can be represented as an adjacency list.

Store each person's neighbors in a list. Traversing Kim's neighbors prints `Kim is connected to Lee` and `Kim is connected to Park`.

```python
friends = {
    "Kim": ["Lee", "Park"],
    "Lee": ["Kim", "Choi"],
    "Park": ["Kim", "Choi"],
    "Choi": ["Lee", "Park"],
}

for person in friends["Kim"]:
    print("Kim is connected to", person)
```

Graphs emphasize connections rather than order or hierarchy: who connects to whom and which paths are available.

Graph thinking appears in these AI and service tasks:

- Follow document links.
- Represent conceptual relationships in a knowledge graph.
- Examine user-item connections in recommendations.
- Connect documents, keywords, and sources in search.
- Represent relationships between chunks and metadata in RAG.

## Case: Data Before and After a Class Transfer

Consider the same student data from four perspectives.

The diagram shows scores as an array, records as a table, school membership as a hierarchy, and friendships as a graph.

![The same student data represented in four structures](/AiBook/assets/part-02/chapter-09/same-data-four-structures-en.svg)

Kim and Lee belong to class A, and Park to B. They scored 82, 75, and 45; Kim–Lee and Lee–Park are friends. The code derives a score array, passing names, class membership, and friendships from these records.

```python
import numpy as np

students = [
    {"name": "Kim", "class": "A", "score": 82, "label": "pass", "friends": ["Lee"]},
    {"name": "Lee", "class": "A", "score": 75, "label": "pass", "friends": ["Kim", "Park"]},
    {"name": "Park", "class": "B", "score": 45, "label": "fail", "friends": ["Lee"]},
]

scores = np.array([student["score"] for student in students])
passed_names = [student["name"] for student in students if student["label"] == "pass"]
names_by_class = {}
friends = {}

for student in students:
    class_name = student["class"]
    if class_name not in names_by_class:
        names_by_class[class_name] = []
    names_by_class[class_name].append(student["name"])
    friends[student["name"]] = student["friends"]

print("mean:", round(float(scores.mean()), 2))
print("passed:", passed_names)
print("classes:", names_by_class)
print("Kim's friends:", friends["Kim"])
```

```text
mean: 67.33
passed: ['Kim', 'Lee']
classes: {'A': ['Kim', 'Lee'], 'B': ['Park']}
Kim's friends: ['Lee']
```

`names_by_class` represents classes and their students beneath a school. `friends` represents connections across classes. Since Lee in A and Park in B are friends, the membership tree alone cannot reveal friendships.

Change Park's `"class"` to `"A"` and rerun: membership becomes `{'A': ['Kim', 'Lee', 'Park']}`, while the mean, passing names, and friendships stay unchanged. Changing only Park's score to `60` instead makes the mean `72.33`, but the stored `"label": "fail"` does not update automatically. If scores determine labels, update the label by that rule too.

## Checklist

- Explain arrays through indices, axes, and numerical computation.
- Explain tables through rows, columns, and datasets.
- Explain trees through roots, parents, children, and hierarchies.
- Explain graphs through nodes, edges, and relationships.
- Explain how different questions lead to different views of the same data.
- Connect tokens, embeddings, datasets, document structures, and knowledge links to these views.
- Identify whether a question concerns arrays, records, hierarchies, or relationships.
- Calculate which values a mean combines and its output shape from shape and axis.

## Sources and References

- NumPy Developers, [The N-dimensional array (`ndarray`)](https://numpy.org/doc/stable/reference/arrays.ndarray.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, checked on 2026-07-20. Used as the basis for array intuition by confirming `ndarray` dimensions, shape, dtype, indexing, and slicing.
- pandas, [pandas.DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, checked on 2026-07-20. Used as the basis for explaining a DataFrame as a two-dimensional structure with rows and columns.
- Paul E. Black, [tree](https://xlinux.nist.gov/dads/HTML/tree.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures, NIST, checked on 2026-07-20. Used as the basis for explaining a tree as a hierarchical structure with root and parent-child relationships.
- Paul E. Black, [graph](https://xlinux.nist.gov/dads/HTML/graph.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures, NIST, checked on 2026-07-20. Used as the basis for explaining a graph as a structure that represents relationships with nodes and edges.
- NumPy Developers, [numpy.mean](https://numpy.org/doc/stable/reference/generated/numpy.mean.html){: target="_blank" rel="noopener noreferrer" }, checked on 2026-09-15. Confirms axis-wise means and result shapes.
- NumPy Developers, [numpy.reshape](https://numpy.org/doc/stable/reference/generated/numpy.reshape.html){: target="_blank" rel="noopener noreferrer" }, checked on 2026-09-15. Confirms shape changes that preserve element count.
