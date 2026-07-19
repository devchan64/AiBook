# P2-9.1 Why Are Data Structures Needed?

> Section ID: `P2-9.1`
> Version: `v2026.07.20`

In P2-8, we looked at Python values, lists, dictionaries, loops, functions, and classes. Now we step back and change the question.

What shape should we use to hold data?

That question is the starting point of the data structure. A data structure is not just the name of syntax. Depending on how data is organized and which operations you do frequently, the shape of code and the way computation proceeds both change.

This Section explains the basic distinctions among `data structure`, `abstract data type`, `linear structure`, and `non-linear structure`. Even when later Sections separate arrays, tables, trees, and graphs again, the reason we should first read data structure as a question reconnects to the standard here. When those structure names repeat later, also check the [Concept Glossary](/AiBook/reference/concept-glossary/).

Instead of adding new Python syntax, this Section re-bundles the syntax learned earlier from the viewpoint of data organization. If Chapter 8 was a stage for learning executable statements such as values, groups, repetition, and functions, this Section looks again at what data shapes those statements had been assuming. Read this way, it becomes easier to connect lists and dictionaries not as syntax items but as different data-structure choices.

| What to capture in this Section now | The question that continues immediately next | Where this appears again later |
| --- | --- | --- |
| The point that a data structure is a perspective that looks at both the shape of holding data and the way operations happen | It leads to the question in P2-9.2 of how to distinguish arrays, tables, trees, and graphs | It repeats later in NumPy, Pandas, graph representation, and project data design |
| The point that even the same data can be stored differently as a list, dictionary, or graph depending on the purpose | It leads to criteria for deciding which structure is more natural | It is used again later in preprocessing, label maps, relational data, and document-structure representation |
| The point that the syntax Sections of Chapter 8 and the data-structure Sections of Chapter 9 are not the same content | It makes clear that the question has shifted from syntax review to data-structure intuition | It becomes the criterion for reading Python basics and data-structure learning without mixing them |

| Term | Meaning to capture first in this Section |
| --- | --- |
| data structure | A way of deciding how to organize and handle data |
| operation | A task often done on a structure, such as search, insertion, deletion, or traversal |
| abstract data type | A frame from the viewpoint of behavior that defines what can be done |
| linear structure | A structure where data is understood as continuing in one ordered line |
| non-linear structure | A structure that is not read only as one line, such as hierarchy or relationships |

For example, even the same student-score data can take different structures depending on the purpose.

Problem situation: You want to see the simplest structure first when you only want to process scores in order.
Input: Three student scores, `82, 75, 91`.
Expected output: A score list, `scores`.
Concept to check: A list is a basic data structure that is good for handling values in order.

```python
scores = [82, 75, 91]
```

This structure is good for processing scores in order.

Problem situation: You want to see that a different structure is needed when you want to find a score directly by student name.
Input: `score_by_name`, where names are keys and scores are values.
Expected output: A dictionary map of scores by name.
Concept to check: Even with the same data, a dictionary is more natural when name-based lookup matters.

```python
score_by_name = {
    "Kim": 82,
    "Lee": 75,
    "Park": 91,
}
```

This structure is good for finding a score by name.

Even with the same data, the appropriate structure changes depending on whether you want to look in order, find by name, or follow relationships.

## Goals of This Section

- You can explain a data structure as a way of organizing data.
- You can explain the difference between linear and non-linear structures at an introductory level.
- You can explain that data structures connect to operations such as search, insertion, deletion, and traversal.
- You can explain that even the same data can be represented differently as a list, dictionary, table, or graph depending on the purpose.
- You can distinguish an abstract data type and a concrete implementation at an introductory level.
- You can explain that in AI practice, datasets, token lists, label maps, and relational data may require different structures.

## Three Criteria

This Section is not for memorizing data-structure names. It is a Section that asks, `What shape should we use to hold data?` The three criteria below become the basis for reading the explanations of arrays, tables, trees, and graphs in later Sections.

| Criterion | Why it matters | The level of understanding needed in this Section |
| --- | --- | --- |
| The point that a data structure is `a way of organizing data` | It lets you read from the viewpoint of purpose rather than memorizing syntax names | This is a Section that asks whether order, labels, hierarchy, or relationships matter most |
| The point that even the same data may need a different structure depending on the `operations done often` | It helps you understand why more structures are learned after lists and dictionaries | The structure changes depending on whether you look in order or search by name |
| The point that an abstract data type and an implementation are not `the same thing` | It lets you read stacks, queues, and graphs more safely later | Rules of behavior and the actual storage method must be distinguished |

## A Data Structure Is a Way of Organizing Information

The NIST Dictionary of Algorithms and Data Structures explains a data structure as a way of organizing information for algorithmic efficiency. Here, understand a data structure as follows.

A data structure is a concept that thinks together about the shape that holds data and the way to handle that data.

A list holds ordered values.

A dictionary finds values by keys.

A set checks membership without duplicates.

A tree represents hierarchy.

A graph represents relationships among objects.

| Data-structure sense | Central question | Example |
| --- | --- | --- |
| order | Which value is at what position? | list |
| label | Which key do we use to find it? | dictionary |
| membership | Is it included? | set |
| hierarchy | Is there a parent and child relationship? | tree |
| relationship | What is connected to what? | graph |

Choosing a data structure is not about choosing `which syntax feels familiar`. It is about choosing what work you do more often.

## What Does a Traditional Introduction to Data Structures Show First?

Traditional introductions to data structures usually introduce several large flows of shapes for holding data. Not every textbook follows the same order, but early on you often meet structures such as arrays, linked lists, stacks, queues, trees, graphs, and hash tables.

These names are not a list to memorize. They represent types of problems in handling data.

| Traditional data structure | Introductory question | Intuition |
| --- | --- | --- |
| array | Will we handle values of the same kind through consecutive positions? | numbered cells |
| linked list | Will values point to the next value? | items connected in a chain |
| stack | Will we take out the last thing put in first? | stacking dishes |
| queue | Will we take out the first thing that came in first? | standing in line |
| tree | Is there a parent-child relationship? | folder structure |
| graph | Are multiple objects connected to one another? | relationship network |
| hash table | Will we find values quickly by key? | a storage box searched by label |

These structures can again be divided broadly into linear structures and non-linear structures.

A linear structure is a structure where data continues in one ordered line. Arrays, lists, stacks, and queues are close to this.

A non-linear structure is a structure where data does not continue only in one line. Trees and graphs are representative. A tree represents hierarchy, and a graph represents relationships in many directions.

| Division | Characteristic | Example |
| --- | --- | --- |
| linear structure | front-back order matters | array, linked list, stack, queue |
| non-linear structure | hierarchy or relationship matters | tree, graph |
| key-based structure | finding values by key matters | dictionary, hash table |

This classification is less a strict academic classification than a map that helps a beginner get direction. Actual structures can overlap. For example, from the usage viewpoint a Python dictionary is a key-based mapping, while from the implementation viewpoint it connects to hashing. A graph can also be represented simply by combining dictionaries and lists.

Therefore, in this Section, accept traditional data-structure names as follows.

- Arrays and lists make you think about order and position.
- Stacks and queues make you think about rules for putting in and taking out.
- Trees make you think about hierarchy.
- Graphs make you think about relationships.
- Hash tables and dictionaries make you think about finding by key.

This map continues into P2-9.2, P2-9.3, and P2-9.4. In P2-9.2, arrays, tables, trees, and graphs are compared broadly. In P2-9.3, graphs are examined separately from the viewpoint of relationship representation. In P2-9.4, traditional data-structure names are read slowly as supplemental learning.

## Data Structures Are Considered Together with Operations

The shape used to hold data connects to the operations used to handle that data.

For example, if you want to look through all scores in order, a list is natural.

Problem situation: You want to see the operation of checking all scores in order from beginning to end.
Input: The score list `scores`.
Expected output: Each score is printed one line at a time.
Concept to check: Work centered on traversal matches well with the list structure.

```python
scores = [82, 75, 91]

for score in scores:
    print(score)
```

But if you need to find one student's score by name, a dictionary is more direct.

Problem situation: You want to see the operation of finding one specific student's score directly by name.
Input: The dictionary `score_by_name` that uses names as keys.
Expected output: The score `82` for `"Kim"`.
Concept to check: Work centered on search reveals intent more directly with a key-based structure.

```python
score_by_name = {
    "Kim": 82,
    "Lee": 75,
    "Park": 91,
}

print(score_by_name["Kim"])
```

Both structures hold scores, but the frequently used operations are different.

| Frequent task | Structure to think of first |
| --- | --- |
| process everything in order | list |
| find by name or ID | dictionary |
| remove duplicates or check membership | set |
| represent parent-child relationships | tree |
| represent connections among many objects | graph |

When learning data structures, it is better to ask first not `What is the name of this structure?` but `What operation was this structure made to make easy?`

## Distinguish the Abstract Data Type and the Implementation

As you learn data structures, you meet names such as stack, queue, dictionary, and set. Here there is a distinction that is easy to confuse.

An abstract data type is a concept that explains what values and operations are possible.

An implementation is how that concept was actually built in real memory and code.

For example, a stack can be explained as a structure that takes out the last thing put in first. That is a rule of behavior.

- `push`: put in a value
- `pop`: take out the most recently inserted value
- the last value put in comes out first

But this stack can be implemented internally with a list or with a linked list. The same abstract data type can be implemented in multiple ways.

This distinction is important even when reading Python.

| Viewpoint | Question | Example |
| --- | --- | --- |
| abstract data type (ADT) | What behavior is promised? | A stack takes out the last inserted value first |
| implementation | How is it actually stored? | It can be implemented with a list or with a linked structure |
| Python usage viewpoint | Through which objects and methods is it provided? | `list.append()`, `list.pop()` |

In this Section, we look at the usage viewpoint before implementation details. When performance or algorithms are covered later, we will see again why the implementation method matters.

## Even the Same Data Changes Structure Depending on the Purpose

The following examples show the same student data represented in three different ways.

### When You Want to Process in Order

Problem situation: You want to see a structure for processing all students one by one in order.
Input: The list `students` containing student dictionaries.
Expected output: Each student's name and score are printed in sequence.
Concept to check: When sequential processing of the same type of record is needed, a list of dictionaries is a natural structure.

```python
students = [
    {"name": "Kim", "score": 82},
    {"name": "Lee", "score": 75},
    {"name": "Park", "score": 91},
]

for student in students:
    print(student["name"], student["score"])
```

This structure is good for processing all students one by one.

### When You Want to Find Directly by Name

Problem situation: You want to see a structure for finding a score directly from one student name.
Input: The dictionary `student_by_name` of student scores by name.
Expected output: The score `82` for `"Kim"`.
Concept to check: When name lookup is central, it is easier to read if the outer structure is a dictionary.

```python
student_by_name = {
    "Kim": {"score": 82},
    "Lee": {"score": 75},
    "Park": {"score": 91},
}

print(student_by_name["Kim"]["score"])
```

This structure is good for finding a specific student by name.

### When You Want to Represent Relationships

Problem situation: You want to see a structure that represents connections such as friendships among students.
Input: `friends`, which uses student names as keys and friend lists as values.
Expected output: The list of friends connected to `"Kim"`.
Concept to check: When relationship representation is central, graph intuition is needed first.

```python
friends = {
    "Kim": ["Lee", "Park"],
    "Lee": ["Kim"],
    "Park": ["Kim"],
}

print(friends["Kim"])
```

This structure expresses who is connected to whom. We have not learned graphs in depth yet, but the sense of `connections between objects` is already present.

Even with the same people data, the structure changes when the purpose changes. That is why data structures are needed.

## Why a Sense for Data Structures Is Needed in AI Practice

In AI practice, you keep meeting multiple structures even if you do not study data structures explicitly.

| AI practice situation | Structure often seen | Viewpoint for reading |
| --- | --- | --- |
| multiple sentence inputs | list | process sentences one by one |
| linking label numbers and names | dictionary | find label names by key |
| checking duplicate tokens | set | check whether it is included |
| table-form data | table, DataFrame | access by rows and columns |
| token flow inside a sentence | sequence | process in order |
| links among documents | graph | move along relationships |

What matters in this Section is not memorizing every structure. It is seeing what question the data demands.

- Does order matter?
- Do we need to find by name?
- Do we need to remove duplicates?
- Is there hierarchy?
- Do we need to follow relationships?
- Do we need fast search?

When the question changes, the data structure changes too.

## Choosing a Data Structure Is Not Only a Performance Problem

When you learn data structures, performance discussions follow. Questions like whether search is fast, whether insertion is fast, and how much memory is used matter. This is important.

But here we do not look only at performance. We also look at readability, the possibility of mistakes, and the meaning of the data.

For example, when the data is small, scanning through a list may still be enough.

Problem situation: You want to see that when data is small, finding the needed student by scanning a list is also possible.
Input: The list `students` containing student dictionaries.
Expected output: The score of the student whose name is `"Kim"`.
Concept to check: Data-structure choice should consider not only performance but also data size and readability.

```python
students = [
    {"name": "Kim", "score": 82},
    {"name": "Lee", "score": 75},
]

for student in students:
    if student["name"] == "Kim":
        print(student["score"])
```

If the data becomes larger and you need to find by name frequently, a dictionary is more natural.

Problem situation: You want to see an example of doing the same lookup more directly in a name-based structure.
Input: `student_by_name`, which uses student names as keys.
Expected output: The score `82` for `"Kim"`.
Concept to check: When the structure itself reveals the frequently used operation, the code's intent becomes clearer too.

```python
student_by_name = {
    "Kim": {"score": 82},
    "Lee": {"score": 75},
}

print(student_by_name["Kim"]["score"])
```

This difference is not only about speed. The second code lets the structure itself reveal the purpose: `find by name`.

A good data structure also reveals the code's intent.

## Case Study

### Case 1. Why should the structure be chosen again for the same student data?

Suppose a learner wants to do three things with student-score data. They want to compute the overall average, immediately find the score of a specific name, and also view friendship relationships together.

At first, a person may think, `Since it is the same data anyway, can't I just put it all into one structure?` But computing an average is easier when you look through numbers in order, name lookup is easier when you search by key, and friendship relationships are more natural when you follow connections.

This is why this Section explains a data structure as `a way of organizing data`. Choosing a structure is not choosing a syntax preference. It is deciding which questions should be answered more easily.

The checkable result is that even from the same source data, the representation changes when the task changes. If a score list for average calculation, a dictionary of scores by name, and a graph of friendships each become easier to read, then the data-structure choice has already affected the way computation proceeds.

## Checklist

- You can explain a data structure as a way of organizing data.
- You can explain which questions arrays, linked lists, stacks, queues, trees, graphs, and hash tables represent in a traditional introduction to data structures.
- You can explain the difference between linear and non-linear structures at an introductory level.
- You can explain that data structures connect to operations such as search, insertion, deletion, and traversal.
- You can explain that even the same data can be represented differently depending on order, keys, and relationships.
- You can distinguish an abstract data type and an implementation at an introductory level.
- You can explain that in AI practice, lists, dictionaries, sets, tables, and graphs are structures for answering different kinds of questions.
- You can connect data-structure choice to deciding not just where to place data, but what question it should answer.

## Sources and References

- Paul E. Black, [data structure](https://xlinux.nist.gov/dads/HTML/datastructur.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures, NIST, checked on 2026-07-20. Used to confirm the definition that describes a data structure as a way to organize data.
- Paul E. Black, [abstract data type](https://xlinux.nist.gov/dads/HTML/abstractDataType.html){: target="_blank" rel="noopener noreferrer" }, Dictionary of Algorithms and Data Structures, NIST, checked on 2026-07-20. Used as the basis for distinguishing an abstract data type as a behavior-centered frame rather than an implementation.
- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-07-20. Used to connect Python list and dictionary examples to the explanation of choosing data structures.
