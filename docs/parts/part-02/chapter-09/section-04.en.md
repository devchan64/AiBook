# P2-9.4 Supplementary Learning: Reading Traditional Data Structures

> Section ID: `P2-9.4`
> Version: `v2026.09.15`

Arrays find values by position; linked lists follow references to subsequent items. Stacks and queues define insertion and retrieval order, while trees and graphs represent relationships. Structure names distinguish storage arrangements or operation rules.

| Structure | Main property | Example use |
| --- | --- | --- |
| Array | Indexed access | Vectors, image pixels |
| Linked list | Order through node links | Changing connections between items |
| Stack | Newest input retrieved first | Undo, function calls |
| Queue | Oldest input retrieved first | Task queues |
| Tree | Parent-child hierarchy | Contents, taxonomies |
| Graph | Connections between nodes | Friendships, document links |
| Hash table | Key lookup using hashes | ID lookup, word counts |

Stack and queue retrieval rules describe ADT behavior. The storage and execution implementation may vary. Appending to and popping from the end of a Python list implements a stack.

## Arrays and Indexed Access

Arrays read values by index. Index 2 of `[10, 20, 30, 40]` holds `30`. In images and vectors, changing positions may change the meaning of the computation.

Python lists also use indices. This prints the first value `10`, the third `30`, then `[10, 25, 30, 40]` after changing the second value to `25`.

```python
values = [10, 20, 30, 40]

print(values[0])
print(values[2])

values[1] = 25
print(values)
```

Python lists contain object references and can change length. NumPy arrays interpret items through one dtype for numerical work. Both provide indexed access, but they are different types.

## Linked Lists and Next Nodes

A singly linked list stores a value and a reference to the next node in each node. The last link marks the end.

```text
Kim → Lee → Park → None
```

This code uses three dictionaries as nodes. Each `next` stores a reference to the following node. Traversal starts at the first and prints `Kim`, `Lee`, and `Park`.

```python
third = {"value": "Park", "next": None}
second = {"value": "Lee", "next": third}
first = {"value": "Kim", "next": second}

node = first
while node is not None:
    print(node["value"])
    node = node["next"]
```

`while node is not None` repeats while a node remains. `node = node["next"]` advances, and reaching `None` ends the loop.

Insert `first["next"] = third` after creating the nodes to print `Kim` and `Park`. Lee's node still exists but is no longer reached from the first node. Links determine logical order.

Finding a value in a linked list requires following links from the start. Once a node or its predecessor is known, links can be changed, but finding that position is not necessarily fast. Connecting the last node's `next` to the first creates a cycle, so the earlier `while` loop never reaches `None` and does not terminate.

## Stacks: Newest First

A stack follows LIFO (last in, first out), like taking the top plate from a stack of plates.

Append A, B, and C, then pop twice: C and B come out, leaving A. `append()` adds at the end, and argument-free `pop()` removes from the end.

```python
stack = []

stack.append("A")
stack.append("B")
stack.append("C")

print(stack.pop())
print(stack.pop())
print(stack)
```

The outputs are `C`, `B`, and `['A']`. Edits A, B, C can be undone in reverse order C, B. Nested function calls similarly finish the later call first, a structure known as the call stack.

## Queues: Oldest First

A queue follows FIFO (first in, first out). `collections.deque` supports insertion and removal at both ends; adding at the back and removing at the front implements a queue.

This code appends A, B, and C, then removes twice from the front. It prints `A`, `B`, and `deque(['C'])`.

```python
from collections import deque

queue = deque()

queue.append("A")
queue.append("B")
queue.append("C")

print(queue.popleft())
print(queue.popleft())
print(queue)
```

`append()` adds at the back; `popleft()` removes from the front. Requests arriving A, B, C are dequeued starting with A. In a service executing jobs concurrently, retrieval order and completion order can differ.

## Removing from an Empty Structure

Calling `pop()` on an empty list or `popleft()` on an empty deque raises `IndexError`. This code retrieves requests until none remain.

```python
from collections import deque

queue = deque(["A", "B"])
while queue:
    request = queue.popleft()
    print(request)
print("remaining:", len(queue))
```

The outputs are `A`, `B`, and `remaining: 0`. Starting with `deque()` skips the loop and prints only the final line. List `pop(0)` also removes the first item but shifts subsequent positions, so a deque suits frequent front removals. This example handles one execution flow; it does not implement synchronization for concurrent queue access.

## Trees: Parents and Children

In a rooted tree, every non-root node has one parent. A contents hierarchy can place Parts beneath a book and Chapters beneath Parts.

The code prints the book title, two Parts, and their Chapters. The outer loop reads Parts; the inner loop reads each Part's Chapters.

```python
book = {
    "title": "study-book",
    "children": [
        {
            "title": "Part 1",
            "children": ["Chapter 1", "Chapter 2"],
        },
        {
            "title": "Part 2",
            "children": ["Chapter 8", "Chapter 9"],
        },
    ],
}

print(book["title"])
for part in book["children"]:
    print("-", part["title"])
    for chapter in part["children"]:
        print("  -", chapter)
```

```text
study-book
- Part 1
  - Chapter 1
  - Chapter 2
- Part 2
  - Chapter 8
  - Chapter 9
```

The path to `Chapter 9` is `study-book → Part 2 → Chapter 9`. Parent-child links identify membership.

## Graphs: Connections Between Objects

A graph represents relationships through nodes and edges. A tree is a connected, cycle-free kind of graph; general graphs can have cycles and multiple paths.

Kim's direct neighbors here are Lee and Park. The code first prints `['Lee', 'Park']`, then `Kim is connected to Lee` and `Kim is connected to Park`.

```python
graph = {
    "Kim": ["Lee", "Park"],
    "Lee": ["Kim", "Choi"],
    "Park": ["Kim"],
    "Choi": ["Lee"],
}

print(graph["Kim"])

for friend in graph["Kim"]:
    print("Kim is connected to", friend)
```

Choi is not a direct neighbor of Kim, but is connected by `Kim → Lee → Choi`. This follows friendship links rather than grouping people into a membership hierarchy.

## Hash Tables and Key Lookup

A hash table uses a key's hash value to locate storage. Different keys may map to the same location, a collision that requires a handling rule.

Python dictionaries map keys to values and use hash-based lookup. This prints Kim's score `82`, then adds `"Choi": 88`.

```python
score_by_name = {
    "Kim": 82,
    "Lee": 75,
    "Park": 91,
}

print(score_by_name["Kim"])

score_by_name["Choi"] = 88
print(score_by_name)
```

The second output is `{'Kim': 82, 'Lee': 75, 'Park': 91, 'Choi': 88}`. Dictionary syntax such as `score_by_name["Kim"]` and the internal hash-table lookup are different levels of explanation.

A hash collision means different keys share a hash value or candidate storage location. It does not automatically overwrite an existing value: the implementation distinguishes actual keys. Assigning a new value to the same key differs from resolving collisions between different keys.

## Case: Waiting Jobs and Undo

To execute requests A, B, C in arrival order, a queue retrieves A first. To undo completed actions A, B, C, a stack retrieves C first. The same items need different retrieval rules for different purposes.

| Insertion order | Two stack removals | Two queue removals |
| --- | --- | --- |
| A, B, C | C, B | A, B |
| A, B, C, D | D, C | A, B |

Add `append("D")` after `append("C")` in the earlier examples to verify the second row. The stack retains `['A', 'B']`; the queue retains `deque(['C', 'D'])`. Equal insertion order does not imply equal processing order.

## AI Tasks and Data Structures

| Task | Needed property | Example structure |
| --- | --- | --- |
| Preserve token order | Position and sequence | Array, sequence |
| Look up label names by ID | Key-value mapping | Dictionary |
| Deduplicate words | Membership | Set |
| Explore document links | Connections and paths | Graph |
| Retrieve requests in arrival order | FIFO | Queue |
| Find a document's parent heading | Parent-child hierarchy | Tree |

## Checklist

- Explain arrays as indexed values.
- Explain linked lists as items pointing to subsequent items.
- Explain stacks as LIFO and queues as FIFO.
- Distinguish tree hierarchies from general graph relationships.
- Connect dictionaries and hash tables with key-based lookup.
- Recognize traditional structures beneath convenient Python syntax.
- Run the array, linked-list, stack, queue, tree, graph, and dictionary examples and explain their outputs.
- Explain empty-queue termination, linked-list cycles, and hash collisions.

## Sources and References

- NIST, [Data structure](https://xlinux.nist.gov/dads/HTML/datastructur.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures, checked on 2026-07-20. Used to confirm the basic definition for reading traditional data-structure names as ways of organizing data.
- NIST, [Abstract data type](https://xlinux.nist.gov/dads/HTML/abstractDataType.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures, checked on 2026-07-20. Used as the basis for explaining structures such as stacks and queues by provided behavior rather than implementation.
- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, checked on 2026-07-20. Used to confirm how Python list and dictionary syntax connects to traditional data-structure intuition.
- Python Software Foundation, [deque objects](https://docs.python.org/3/library/collections.html#collections.deque){: target="_blank" rel="noopener noreferrer" }, checked on 2026-09-15. Confirms empty-deque errors and insertion/removal behavior at both ends.
- Paul E. Black, NIST, [collision](https://xlinux.nist.gov/dads/HTML/collision.html){: target="_blank" rel="noopener noreferrer" }, checked on 2026-09-15. Supports distinguishing different-key hash collisions from same-key value updates.
