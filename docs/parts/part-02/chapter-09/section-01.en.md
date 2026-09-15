# P2-9.1 Why Does Choosing a Data Structure Matter?

> Section ID: `P2-9.1`
> Version: `v2026.09.15`

## Organizing Data and Performing Operations

A data structure organizes data. NIST defines it in terms of organizing information for algorithmic efficiency. The same student information can be represented differently for calculating scores, finding a student, or following friendships.

| Perspective | Main question | Example |
| --- | --- | --- |
| Order | Which position? | List |
| Named lookup | Which key? | Dictionary |
| Membership | Is it present? | Set |
| Hierarchy | What is above or below? | Tree |
| Relationships | What connects to what? | Graph |

Frequent operations matter when choosing a structure. These include search, insertion, deletion, and traversal—visiting all items.

## Ordered, Hierarchical, and Key-Based Structures

| Traditional structure | Introductory question | Intuition |
| --- | --- | --- |
| Array | Handle similar values at consecutive positions? | Numbered slots |
| Linked list | Have each item point to the next? | Linked items |
| Stack | Retrieve the newest item first? | Stacked plates |
| Queue | Retrieve the oldest item first? | A waiting line |
| Tree | Represent parent-child relationships? | Folders |
| Graph | Connect multiple objects? | A relationship network |
| Hash table | Find values quickly by key? | Labeled storage |

These structures can broadly be viewed as linear or nonlinear.

Linear structures arrange data in a single sequence. Arrays, lists, stacks, and queues fit this view.

Nonlinear structures do not arrange everything in one sequence. Trees represent hierarchies, while graphs represent connections in multiple directions.

| Category | Main feature | Examples |
| --- | --- | --- |
| Linear | Sequential order matters | Arrays, linked lists, stacks, queues |
| Nonlinear | Hierarchy or relationships matter | Trees, graphs |
| Key-based | Lookup by key matters | Dictionaries, hash tables |

These categories can overlap. Python dictionaries map keys to values and preserve insertion order. A graph can be represented using dictionaries and lists together.

## Abstract Data Types and Implementations

An abstract data type (ADT) describes the values and operations that are supported.

An implementation determines how that concept is realized in memory and code.

A stack, for example, returns the most recently inserted item first. This specifies behavior.

- `push`: insert a value.
- `pop`: retrieve the newest value.
- The last value inserted is the first retrieved.

Internally, a stack may use a Python list or a linked list. The same ADT can have multiple implementations.

This distinction also helps when reading Python.

| Perspective | Question | Example |
| --- | --- | --- |
| ADT | What behavior is promised? | A stack returns the newest item first |
| Implementation | How is it stored? | A list or linked structure can implement it |
| Python interface | Which objects and methods provide it? | `list.append()`, `list.pop()` |

Push `A`, then `B`, and one pop must return `B`. A Python list can implement this with `append("A")`, `append("B")`, and `pop()`. Changing storage must preserve the retrieval rule to retain stack behavior.

## Traversal, Lookup, and Relationships

Kim, Lee, and Park scored 82, 75, and 91. Different structures can hold the information needed for score lookup and friendship relationships.

### Traversing Every Record

Store student dictionaries in a list to traverse them all. The code prints `Kim 82`, `Lee 75`, and `Park 91` in order.

```python
students = [
    {"name": "Kim", "score": 82},
    {"name": "Lee", "score": 75},
    {"name": "Park", "score": 91},
]

for student in students:
    print(student["name"], student["score"])
```

The scores total 248 and average about 82.67. A mean needs all scores, unlike looking up one name.

### Lookup by Name

Using names as keys gives direct access to a student's score. `student_by_name["Kim"]["score"]` prints `82`.

```python
student_by_name = {
    "Kim": {"score": 82},
    "Lee": {"score": 75},
    "Park": {"score": 91},
}

print(student_by_name["Kim"]["score"])
```

This structure suits finding an individual student by name.

### Friendships

Friendships can be represented by a friend list for each name. Kim's list here is `['Lee', 'Park']`.

```python
friends = {
    "Kim": ["Lee", "Park"],
    "Lee": ["Kim"],
    "Park": ["Kim"],
}

print(friends["Kim"])
```

This is a graph of students and friendship connections. Each mutual relationship is recorded in both lists. Removing Kim–Lee requires removing `"Lee"` from Kim's list and `"Kim"` from Lee's list.

The same people can require different structures for different purposes. That is why data structures matter.

## Structures in AI Data

Sentence inputs, label mappings, and document links need different lookup and processing operations.

| AI situation | Common structure | Reading perspective |
| --- | --- | --- |
| Multiple sentences | List | Process sentences individually |
| Label IDs and names | Dictionary | Find names by key |
| Duplicate-token checks | Set | Test membership |
| Tabular data | Table, DataFrame | Access rows and columns |
| Token flow in a sentence | Sequence | Process in order |
| Document links | Graph | Follow relationships |

## Case: Students with the Same Name

Suppose two students named Kim scored `82` and `91`. A list preserves both records, but using the name as a dictionary key overwrites the earlier score. This prints both records, then `{'Kim': 91}`.

```python
students = [
    {"id": "s001", "name": "Kim", "score": 82},
    {"id": "s002", "name": "Kim", "score": 91},
]
score_by_name = {}

for student in students:
    score_by_name[student["name"]] = student["score"]

print(students)
print(score_by_name)
```

Key choice determines what information is preserved. Unique student IDs distinguish the two scores. With the same input, the next code prints `{'s001': 82, 's002': 91}`.

```python
students = [
    {"id": "s001", "name": "Kim", "score": 82},
    {"id": "s002", "name": "Kim", "score": 91},
]
score_by_id = {}

for student in students:
    score_by_id[student["id"]] = student["score"]

print(score_by_id)
```

Changing the second ID to `"s001"` again leaves only one key. Besides shortening lookup, verify that keys really distinguish students. To group multiple scores by name, use lists as dictionary values.

## Information Lost When Changing Structures

A set suits deduplication but does not preserve occurrence counts. A name list containing Kim twice and Lee once has length 3 but only 2 unique names.

```python
names = ["Kim", "Kim", "Lee"]
unique_names = set(names)
print(len(names))
print(len(unique_names))
print("Kim" in unique_names)
```

The outputs are `3`, `2`, and `True`. Keeping only the set loses Kim's count and the original order. A count dictionary can retain frequencies, and a list can retain original records. Do not assume set output follows input order.

A lookup dictionary must first be built by reading the source and needs extra memory. This helps repeated ID lookups, but a single overall mean only requires traversing the scores. If original scores change while copied lookup values do not, they can disagree; decide which data drives updates.

## Checklist

- Explain a data structure as a way to organize data.
- Explain the questions represented by arrays, linked lists, stacks, queues, trees, graphs, and hash tables.
- Distinguish linear and nonlinear structures at an introductory level.
- Connect structures with search, insertion, deletion, and traversal.
- Explain how order, keys, and relationships produce different representations.
- Distinguish abstract data types and implementations.
- Explain the different questions answered by lists, dictionaries, sets, tables, and graphs in AI work.
- Choose structures by the questions the data must answer, not merely by how it is collected.
- Explain order and duplicate information lost in set conversion and the need to update lookup copies.

## Sources and References

- Paul E. Black, [data structure](https://xlinux.nist.gov/dads/HTML/datastructur.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures, NIST, checked on 2026-07-20. Used to confirm the definition that describes a data structure as a way to organize data.
- Paul E. Black, [abstract data type](https://xlinux.nist.gov/dads/HTML/abstractDataType.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures, NIST, checked on 2026-07-20. Used as the basis for distinguishing an abstract data type as a behavior-centered frame rather than an implementation.
- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, checked on 2026-07-20. Used to connect Python list and dictionary examples to the explanation of choosing data structures.
