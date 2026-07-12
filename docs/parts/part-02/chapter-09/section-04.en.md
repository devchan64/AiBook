# P2-9.4 Supplemental Learning: How to First Read Traditional Data Structure Names

> Section ID: `P2-9.4`
> Version: `v2026.07.12`

In P2-9.1, we viewed a data structure as the shape that holds data and the way that data is handled. But once you start studying data structures, many unfamiliar names suddenly appear.

Arrays, linked lists, stacks, queues, trees, graphs, hash tables.

This supplement explains `the standard for reading traditional data-structure names`. It organizes a way of rereading names such as arrays, linked lists, stacks, queues, trees, graphs, and hash tables through questions rather than through implementation first.

If you try to memorize these names from the start through implementation details, they feel difficult. In this supplement, we first look at `what problem each structure appeared to solve`.

If you learned basic programming long ago, or if you first encountered Python as a practice tool, these data-structure names may feel even more unfamiliar. Because Python lists and dictionaries handle many things conveniently, it is natural to wonder whether old names such as arrays, linked lists, stacks, and queues are really necessary.

But once AI practice expands even a little, these names return. Datasets look like tables, tokens are handled as ordered sequences, labels are managed as key-value mappings, and search and recommendation use relationships and index structures. Traditional data structures are not `old syntax`. They are closer to a basic language for reading data.

This Section first organizes `what question does this name make easier` for the moment when names such as array, stack, queue, and graph all feel unfamiliar at once.

## What to Take First

This Section places required review and extended background in one place. On a first read, it is enough to hold the five `essential` items below first, and return to the rest later.

| Division | What to take first |
| --- | --- |
| essential | The point that an array is a structure that reads values by position |
| essential | The point that a stack is a rule where the last inserted item comes out first |
| essential | The point that a queue is a rule where the first inserted item comes out first |
| essential | The point that a tree expresses hierarchy and a graph expresses relationships |
| essential | The point that behind Python lists and dictionaries there are still more general data-structure questions |
| extended | The connection intuition of a linked list |
| extended | The internal organization intuition of a hash table |
| extended | Later learning topics such as implementation details, complexity, and memory layout |

| Term | Meaning to capture first in this Section |
| --- | --- |
| array | A structure that reads numbered value slots in order |
| linked list | A structure where each item continues by pointing to the next item |
| stack | A rule-centered structure where the last inserted item comes out first |
| queue | A rule-centered structure where the first inserted item comes out first |
| hash table | A structure organized to find values quickly by key |

## Scope of This Supplement

This Section is supplemental learning for first reading traditional data-structure names. The purpose is not to implement data structures completely, but to prevent confusion later when arrays, tables, trees, graphs, dictionaries, and search structures appear again in later documents. It does not handle implementation details or complexity analysis here. The focus is on reinforcing the question-centered reading standard formed in P2-9.1 through P2-9.3.

This Section answers the following questions.

- Why does an array make you think about position and order?
- Why does a linked list have the idea that one item points to the next?
- Why are stacks and queues explained through rules for putting in and taking out?
- Why do trees and graphs lead to structures that express relationships?
- Why is a hash table connected to a structure that finds values by key?
- Why do we still need to know traditional data-structure names even after learning Python lists and dictionaries?

This Section does not go deeply into time complexity, memory layout, pointers, hash collisions, or graph traversal algorithms. In the current main text, the priority is the sense for reading data-structure names. Implementation details and complexity analysis are left for later algorithm and systems study.

## Goals of This Supplement

- You can read traditional data-structure names by connecting them to problem-solving questions.
- You can distinguish linear structures, non-linear structures, and key-based structures at an introductory level.
- You can explain that Python lists and dictionaries are not exactly the same thing as traditional data-structure explanations, but can still be understood by borrowing that intuition.
- You can explain that in AI practice, structures such as datasets, token lists, label maps, document relationships, and search indices require different data-structure intuitions.

## The Standard to Hold First

The first standard to hold in this supplement is that `a data-structure name is a label attached to a representative question`.

| Name | Question to hold first |
| --- | --- |
| array | What is the value at a certain position? |
| stack | Does the last inserted item come out first? |
| queue | Does the first inserted item come out first? |
| tree | Is there a parent-child relationship? |
| graph | What is connected to what? |
| hash table | Do we want to find a value quickly by key? |

In other words, this Section first reads `what problem does this name make easy`, rather than implementation detail.

## Background

Traditional data structures are sometimes learned before Python syntax, but in a relearning path it can feel more natural to look at them again later. After you have already used lists and dictionaries, reading arrays, stacks, queues, trees, and graphs again makes it easier to hold `what question does this name make easier`.

That is why this Section is organized to ask first `why is this structure needed`, rather than to begin with implementation detail. The goal is not to memorize a list of names, but to read how they connect to scenes in AI practice.

## Three Criteria

| Criterion | Why it matters | Level of understanding needed in this Section |
| --- | --- | --- |
| Why traditional data structures are revisited | It helps recover the more general way of thinking behind Python syntax | Hold the point that data-structure names are not old syntax but a language of questions |
| What data-structure names represent | It helps you look first at what problem is made easier, rather than memorizing storage methods | Understand that each name has a different representative question |
| Their relation to Python data types | It helps connect lists and dictionaries you already learned to a broader structural intuition | Understand that lists and dictionaries too continue older data-structure thinking |

## Main Learning Content

### Why do we revisit traditional data structures later?

In P2-8, we looked at Python syntax first. That order was intentional. If we begin with data-structure theory immediately, implementation detail becomes heavy and the path can drift away from the purpose of AI relearning.

But Python syntax alone has difficulty answering the following questions.

- Why is a list good for processing in order?
- Why is a dictionary good for finding values by name or ID?
- Why should some data be seen as a table, while other data is seen as a graph?
- Why does the structure change depending on whether the purpose is search, recommendation, classification, or visualization, even over the same data?

Traditional data structures are background knowledge that answers these questions. This Section is not an implementation class. It is a supplement that creates the minimum map to call up when reading data-structure names.

### Data-structure names represent questions

If you memorize data structures as a list of names, confusion comes quickly. Instead, look first at the question each name represents.

| Data structure | Representative question | Scene to imagine first |
| --- | --- | --- |
| array | What is the value at a certain position? | numbers laid out in order, vectors, pixels |
| linked list | Where is the next value? | a structure where items point to the next item |
| stack | Does the last inserted item come out first? | undo, call flow, temporary storage |
| queue | Is the first inserted item handled first? | job queue, request processing |
| tree | Is there a parent-child relationship? | folders, classification systems, decision flow |
| graph | What is connected to what? | friendships, links, knowledge graphs |
| hash table | Do we want to find a value immediately by key? | finding a user by ID, counting word frequency |

This table is not a strict classification chart. It is a beginner's map. The data structures in an actual programming language are more complex internally. For example, a Python dictionary is a mapping from the usage viewpoint, where a key finds a value, but from the implementation viewpoint it connects to a hash table.

When reading data structures, look at the operation before the name.

| Frequent operation | Question | Connected data-structure intuition |
| --- | --- | --- |
| access | Do we want to see the value at a certain position or key immediately? | array, dictionary |
| insert | Do we insert values often? | list, linked list, queue |
| delete | Do we remove values often? | list, linked list, stack, queue |
| search | Do we need to find the wanted value? | array, hash table, tree |
| traversal | Do we need to scan the whole structure in sequence? | list, tree, graph |
| relation movement | Do we need to move to the next connected target? | tree, graph |

This table is not an absolute answer either. Even for the same data structure, actual performance changes with implementation method and data size. Here the focus is on `what question is useful to recall`.

### Three questions for choosing a data structure

When choosing a data structure, first check the following three questions.

First, does the data have order?

If order and position matter, as with tokens in a sentence, logs arriving in time order, or image pixels, then you need the intuition of lists, arrays, or sequences.

Second, do you need to find by name or ID?

If you need to find user information by user ID, label names by label number, or count word frequencies, then you need the intuition of dictionaries, mappings, and hash tables.

Third, do you need to follow relationships among objects?

If you need to follow links among documents, relations among people, or connections among concepts, then you need the intuition of trees or graphs.

These three questions appear often in AI practice too.

| Question | AI practice example | Structure to recall first |
| --- | --- | --- |
| Does order matter? | token lists, time-series data, image pixels | list, array, sequence |
| Do we need to find by key? | label map, word frequency, configuration values | dictionary, hash table |
| Do we need to follow relationships? | document links, knowledge graph, recommendation relation | tree, graph |

If these three questions are grouped more briefly again:

| Question to ask first | Why it is needed |
| --- | --- |
| Does order matter? | To choose linear-structure intuition |
| Do we find by name or ID? | To choose key-based-structure intuition |
| Do we need to follow relationships? | To choose non-linear-structure intuition |

## Detailed Learning Content

### Linear structures: Thinking in one line

A linear structure is a structure that sees data in one line of order. Arrays, linked lists, stacks, and queues are close to this.

When looking at a linear structure, ask the following questions first.

- Does order matter?
- Does the position number matter?
- Is it processed from the front?
- Is it taken out from the back?
- Is there frequent insertion or removal in the middle?

### Array

An array is a structure that handles values of the same kind through positions. Position intuition matters when looking at vectors in mathematics, and position intuition also matters when looking at pixels in image processing.

Here, think of an array as `numbered slots`.

| position | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| value | 10 | 20 | 30 | 40 |

An array gives the intuition of accessing by position. That is why it appears again when learning NumPy arrays, vectors, and matrices.

What matters when understanding an array is that `position has meaning`. For example, each slot of an embedding vector holds one number, but the positional relationship among those numbers is used in model computation. An image also stops being an image if pixel values scatter in arbitrary order. Which position a value belongs to matters.

A Python list can also take out values by position, so it looks array-like.

Problem situation: In a structure where position matters like an array, you want to immediately pull out the value of a specific slot.
Input: A list holding four numbers in order and the index `2`.
Expected output: The value `30` at the third position is printed.
Concept to check: See that the core of array intuition lies in accessing by position rather than in the value alone.

```python
values = [10, 20, 30, 40]
print(values[2])
```

But it would be a mistake to treat a Python list and a traditional array as exactly the same thing. A Python list is a dynamic structure that holds references to objects, while a NumPy array is a structure designed to hold same-type numbers densely for computation. For now, it is enough to take away the shared intuition of `access by position`.

### Linked list

From here, the section on linked lists and the later section on hash tables are closer to `extended` reading. If the representative questions of arrays, stacks, queues, trees, and graphs are already in place, it is fine to postpone this part to later study.

A linked list is a structure where each item points to the next item. Rather than thinking that every slot exists in consecutive positions like an array, it thinks in terms of `after this item comes that item`.

Understand it here like this.

```text
Kim -> Lee -> Park -> None
```

This example does not mean it is the same implementation as a real Python list. It shows the idea that a node storing a value points to the next item.

A linked list is also helpful later when understanding graphs. That is because the intuition that `values point to one another` continues into relational structures.

What matters about a linked list is that it opens the thought that `data does not have to be in consecutive slots`. If data can point to the next object, then even one line of order can be expressed as connection.

However, at the beginner stage of using Python, you often do not need to implement a linked list directly. Here it is placed more as background so that words like pointer, node, and link do not feel frightening.

### Stack

A stack is a structure where the last inserted item comes out first. It is usually called LIFO.

For example, if you stack plates, you take out the plate placed at the top first.

```text
push A
push B
push C
pop  -> C
pop  -> B
```

A stack appears often in programming examples such as undo, function call flow, and parenthesis checking. For now, remember the rule `the last inserted item comes out first` rather than the implementation.

In AI practice too, stack intuition appears indirectly. For example, when an error occurs during code execution, a traceback shows the function call flow from top to bottom. At that point, the sense that `one function called another, and the later call finishes first` connects to the stack.

### Queue

A queue is a structure where the first inserted item is handled first. It is usually called FIFO.

It is similar to people waiting in line, where the first person to arrive is handled first.

```text
enqueue A
enqueue B
enqueue C
dequeue -> A
dequeue -> B
```

A queue appears often in request handling, job queues, message processing, and data streaming. In AI services too, it connects to cases where user requests are handled in order or background jobs are placed into a waiting line.

A queue is especially important from the service viewpoint. If model calls take a long time, or requests such as image generation take a long time to finish, those requests may be placed into a job queue instead of being processed immediately. In that case, queue is not only a data-structure name. It connects to the operational question `In what order will requests be processed?`

### Non-linear structures: Seeing through relationships rather than one line

A non-linear structure does not see data only as one ordered line. Trees and graphs are the representative examples.

When looking at a non-linear structure, ask the following questions first.

- Is there a parent-child relationship?
- Are multiple objects connected to one another?
- Is there only one path, or many paths?
- Do we need to move by following relationships?

### Tree

A tree is a structure that expresses hierarchy. It is explained as starting from one root and branching downward.

The folder structure is an easy example.

```text
book
├─ part-01
│  └─ chapter-01
└─ part-02
   └─ chapter-09
```

A tree appears often when explaining classification systems, file systems, decision trees, and document structure. The table of contents of one learning document is also close to a tree structure that goes down as Part, Chapter, and Section.

When viewing a tree, the intuition that `one object has several lower objects beneath it` is important. For example, a book's table of contents has Chapters under a Part, and Sections under a Chapter. In this structure, the scope narrows as you go down from the top.

In AI, there are also models such as decision trees that divide judgment processes, and there are tasks that read the title and subtitle structure of documents as hierarchy. In search systems too, tree intuition is used for category classification and document-structure understanding.

### Graph

A graph expresses connections among objects. In a graph, the objects are called nodes and the connections are called edges.

A tree can be viewed as a more restricted structure than a graph. A tree usually has clear hierarchy, while a graph allows connections in many directions.

```text
Kim -- Lee
Kim -- Park
Lee -- Choi
Park -- Choi
```

Graphs are important for understanding friendships, web links, transportation networks, knowledge graphs, recommendation systems, and search structures. In P2-9.3, graphs are treated separately from the viewpoint of relationship representation.

Graphs are needed `when relationships cannot be organized only as one line or one hierarchy`. In friendships, one person can connect to many others, and document links can also continue in many directions. A knowledge graph expresses relations among concepts, objects, and attributes through nodes and edges.

Once you understand graphs, questions such as `Why does search expand by following links?`, `Why does recommendation look at similar users or items?`, and `Why can document chunks have relationships in RAG?` become easier to see.

### Key-based structures: Finding by label

A key-based structure is one where `By which key do we find it?` matters more than `At what position is the value?`

The most familiar Python example is a dictionary.

Problem situation: You want to find a score not by its ordinal position but directly through a key like a name label.
Input: A dictionary with names as keys and scores as values.
Expected output: The score `82` corresponding to the key `Kim` is printed.
Concept to check: See that the core of a key-based structure is finding values by key rather than by position.

```python
score_by_name = {
    "Kim": 82,
    "Lee": 75,
    "Park": 91,
}

print(score_by_name["Kim"])
```

This code finds a score using a name as a key.

In traditional data structures, the hash table is often connected to key-based search. A hash table can be explained as a structure that turns a key into some position in order to find the value. But the real implementation includes detailed topics such as collision handling, memory layout, and resizing, so we do not go deeply into that here.

At the beginner stage, a hash can be understood roughly as `the process of turning a key into a value used to find a storage location`. For example, instead of comparing the name `Kim` from beginning to end until it is found, the basic intuition of a hash table is to transform that name into some numeric position and find the value there.

A real hash table must handle collisions where the same position appears, and must also adjust its internal size as data grows. This Section does not deal with those implementation details. In the current main text, collision handling and resizing are not expanded separately. What matters is the point that behind a structure like a dictionary, which finds values by key, there is hash-table intuition.

Remember roughly the following here.

- A list is good for processing in order.
- A dictionary is good for finding by key.
- A hash table connects to an implementation method for finding values by key.

## Cases and Examples

### How do Python lists and dictionaries connect to traditional data structures?

When you learn Python first, lists and dictionaries feel very convenient. So it is easy to think, `Isn't it enough to know just these two?`

But once you know traditional data-structure names, you can read the intent of code more accurately.

| Code seen in Python | Data-structure intuition | Way to read it |
| --- | --- | --- |
| `items = []` | list, sequence | collect multiple items in order |
| `items.append(x)` | stack intuition is also possible | add a value to the back |
| `items.pop()` | stack intuition | take out the last value |
| `collections.deque()` | queue, deque | put in and take out from both ends |
| `{key: value}` | mapping, hash-table intuition | find a value by key |
| `{node: [neighbors]}` | graph adjacency-list intuition | hold the connected targets by node |

Python objects are not completely one-to-one with traditional data structures. But traditional data-structure intuition helps when reading Python code by showing `what kind of processing method is this code intending?`

### Case 1. If I know Python lists and dictionaries, is data structure finished?

Suppose a learner has become familiar with Python lists and dictionaries and starts to think, `Do I really need names like array, stack, queue, tree, and graph?` In small practice work, it may genuinely feel that way.

But when the work becomes larger, the questions change. Tokens must be processed in order. Job requests must be handled like a waiting queue. Label names are found by key. Document links and recommendation relations must be read as connection structures. In other words, even while using Python's basic data types, the data-structure intuition behind them keeps working.

That is also why this supplement brings back the traditional names. The goal is not an implementation class, but to read `what problem was this name created to solve?` Once you do that, even the lists and dictionaries you already see in Python code can be understood as part of a larger map.

The checkable result is whether you can turn AI practice scenes back into structure questions. If you can distinguish `Is this an order problem?`, `Is this a key lookup problem?`, and `Is this a relationship-tracking problem?`, then you have started using data-structure names not as a mere term list but as an interpretation tool.

### Storing the same material differently

The following data shows the same student scores stored from three viewpoints.

If you want to process them in order, a list is convenient.

Problem situation: You want to first see the simplest structure that stores student scores only in order.
Input: A list containing the scores of three students in order.
Expected output: There is no output, but you confirm what an order-centered structure looks like.
Concept to check: See that a list is closer to the intuition of handling values in order than to the intuition of labels.

```python
scores = [82, 75, 91]
```

If you want to find by name, a dictionary is convenient.

Problem situation: You want to find scores not by order but by student name.
Input: A dictionary whose keys are names and whose values are scores.
Expected output: There is no output, but you confirm what a key-based structure looks like.
Concept to check: See that even with the same data, if labels matter, a dictionary structure becomes more natural.

```python
score_by_name = {
    "Kim": 82,
    "Lee": 75,
    "Park": 91,
}
```

If you want to express friendships, a graph-like structure is needed.

Problem situation: You want to express not a list of students or a score table, but the connections among people.
Input: A dictionary whose keys are person names and whose values are friend lists.
Expected output: There is no output, but you confirm how a relationship-centered structure is written.
Concept to check: See that in graph intuition, connection matters more than order.

```python
friends = {
    "Kim": ["Lee", "Park"],
    "Lee": ["Kim"],
    "Park": ["Kim"],
}
```

All three examples are written in Python syntax, but each uses a different data-structure intuition. The first is order, the second is key-based lookup, and the third is relationship expression.

## Practice and Examples

### Minimal Python examples to run directly

The following examples are not code for fully implementing traditional data structures. They are small examples for confirming the kind of behavioral intuition each data structure has. They can be run as-is in a Colab code cell or a local Python file.

### Array intuition: Access by position

Python lists are not exactly the same as traditional arrays, but they are suitable for confirming the intuition of access by position.

Problem situation: You want to directly confirm the basic action of reading and changing values in array intuition.
Input: A list with four numbers, two index accesses, and one value update.
Expected output: The first value, the third value, and then the full list after modification are printed in order.
Concept to check: Confirm that in an array-like structure, values are read by position and changed by position.

```python
values = [10, 20, 30, 40]

print(values[0])
print(values[2])

values[1] = 25
print(values)
```

The important point in this example is that each value has a position, and the value can be taken out or changed through that position.

### Linked-list intuition: Follow the next item

A linked list shows the idea that an item points to the next item. Here we do not create a class, and instead use dictionaries only to confirm node intuition.

Problem situation: You want to see the flow of reading values by following the next item rather than by consecutive slots.
Input: Three node dictionaries that have `value` and `next`.
Expected output: `Kim`, `Lee`, and `Park` are printed in order.
Concept to check: See that linked-list intuition lies not in numbered positions but in the link pointing to the next node.

```python
third = {"value": "Park", "next": None}
second = {"value": "Lee", "next": third}
first = {"value": "Kim", "next": second}

node = first
while node is not None:
    print(node["value"])
    node = node["next"]
```

This example really follows the flow `Kim -> Lee -> Park -> None`. The key point is not whether the values sit in consecutive slots, but that there is a connection that lets you move to the next item.

### Stack intuition: The last inserted item comes out first

The intuition of a stack can be confirmed through `append()` and `pop()` on a Python list.

Problem situation: You want to directly see the stack rule that the last inserted value comes out first.
Input: Code that puts `"A"`, `"B"`, and `"C"` into an empty list and then removes two values.
Expected output: `"C"`, `"B"`, and then the remaining list are printed.
Concept to check: Confirm that the core rule of a stack is LIFO.

```python
stack = []

stack.append("A")
stack.append("B")
stack.append("C")

print(stack.pop())
print(stack.pop())
print(stack)
```

The last inserted `"C"` comes out first. That is the LIFO intuition.

### Queue intuition: The first inserted item is handled first

A queue has the flow of taking out from the front and putting in at the back. In Python, this intuition can be checked simply through `collections.deque`.

Problem situation: You want to directly see the queue rule that the first inserted value comes out first.
Input: Code that puts `"A"`, `"B"`, and `"C"` into a `deque` and then removes two values from the front.
Expected output: `"A"`, `"B"`, and then the remaining queue are printed.
Concept to check: Confirm that the core rule of a queue is FIFO.

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

The first inserted `"A"` comes out first. That is the FIFO intuition.

### Tree intuition: Going down through parent and child

A tree expresses parent-child relations. The following example expresses a book table of contents like a small tree.

Problem situation: You want to see a small data example of a hierarchy that goes from top to bottom like a book table of contents.
Input: A nested dictionary composed of `title` and `children`.
Expected output: The book title, each Part title, and the Chapter names below them are printed hierarchically.
Concept to check: Confirm that a tree is a hierarchical structure where children hang below a parent.

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

In the tree example, the scope narrows as you go down from top to bottom. This intuition is needed when reading data with clear hierarchy, such as book, Part, and Chapter.

### Graph intuition: Follow connected objects

A graph expresses connections among objects. The following example expresses relations among people like an adjacency list.

Problem situation: You want to pull out the neighbors directly connected to a certain person from a graph structure.
Input: An adjacency-list dictionary containing friend lists by person.
Expected output: The neighbor list of `Kim` and then each connection sentence are printed.
Concept to check: See that in a graph, reading the list of connected objects matters more than order.

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

In a graph, `Who is connected to whom?` matters more than `Which position is it?` This intuition appears again when looking at recommendation, search, and link analysis.

### Hash-table intuition: Find a value by key

From the usage viewpoint, a Python dictionary is a structure that finds values by key. Even without explaining the internal implementation, it is good for confirming hash-table intuition.

Problem situation: You want to read a value and add a new value by using a label-like key instead of scanning in order.
Input: A dictionary holding names as keys and scores as values, plus the addition of a new item.
Expected output: The score of `Kim` and then the dictionary after adding a new item are printed.
Concept to check: Confirm that in a key-based structure, what matters is by which name you find it rather than at which position it sits.

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

The important point in this example is that the value is found by a key such as `"Kim"`, not by scanning in order.

### Data structures encountered again in AI practice

In AI practice, even when data-structure names do not appear directly, you keep meeting similar ideas.

| AI practice scene | Data-structure intuition |
| --- | --- |
| put several sentences in as input | list, sequence |
| process tokens in order | array, sequence |
| change label numbers into label names | dictionary, mapping |
| remove duplicate words | set |
| handle tabular data | table, DataFrame |
| follow links among documents | graph |
| gather embeddings for search | array, index, search structure |
| process job requests in order | queue |

This supplement does not try to make you implement every structure. Instead, it focuses on helping you distinguish ordered structures, key-based structures, and relationship-following structures when reading AI practice documents later.

### Points easy to misunderstand

First, a Python list is not exactly the same thing as a traditional array.

Both can take out values by position, but a Python list can change size dynamically and can also hold different kinds of objects. A NumPy array has a stricter structure suited to numerical computation. So it is safer to understand not `a list is an array`, but `a list provides array-like intuition of position-based access`.

Second, a dictionary connects to a hash table, but is not itself the full explanation of a hash table.

A Python dictionary is a mapping object that lets you find values by key. Its internal implementation connects to hash-table intuition, but usage explanation and implementation explanation should be distinguished.

Third, trees and graphs are not completely separate worlds.

A tree is a relationship structure with clear hierarchy, while a graph is a more general connection structure. Here the distinction is that a tree is `a structure with strong parent-child relations`, and a graph is `a structure that expresses connections among many objects`.

Fourth, data structures are not only for performance.

They also reveal the meaning of code. If you use a list, the intent `process in order` becomes visible. If you use a dictionary, the intent `find by key` becomes visible. If you use a graph structure, the intent `follow relationships` becomes visible.

## Checklist

- Can you explain arrays, stacks, queues, trees, graphs, and hash tables through representative questions?
- Can you explain why traditional data-structure names still need to be read again after Python syntax?
- Can you explain the intuition of choosing a structure depending on whether order, keys, or relationships matter?
- You can explain an array as a structure that handles values by position.
- You can explain a linked list as a structure where each item points to the next.
- You can explain a stack through the LIFO rule and a queue through the FIFO rule.
- You can distinguish a tree as a hierarchical structure and a graph as a relational structure.
- You can explain that dictionaries and hash tables connect to key-based lookup.
- You can explain that behind Python's convenient syntax, traditional data-structure intuition is still working.
- You can run Python examples of arrays, linked lists, stacks, queues, trees, graphs, and dictionaries, and explain the output flow.
- Can you first distinguish `is this an order problem`, `a key lookup problem`, or `a relationship-tracking problem`?

## Sources and References

- NIST, [Data structure](https://xlinux.nist.gov/dads/HTML/datastructur.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures, checked 2026-06-25.
- NIST, [Abstract data type](https://xlinux.nist.gov/dads/HTML/abstractDataType.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures, checked 2026-06-25.
- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python Documentation, checked 2026-06-25.
