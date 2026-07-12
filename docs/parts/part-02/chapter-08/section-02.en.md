# P2-8.2 Lists: Ordered Groups of Values

> Section ID: `P2-8.2`
> Version: `v2026.07.12`

In P2-8.1, we looked at values, variables, and types. Now we look at the first structure for handling several values at once: the list.

A list is a data structure that gathers values of the same purpose or context in order. You often encounter it in situations such as a score list, a sentence list, a file-name list, or a model-output list, where you want to `look at several things in order`.

Here, we explain the basic distinction between a `list` and an `index`. The representative explanation of `value`, `variable`, and `type` is placed in P2-8.1 and in the [Concept Glossary](../../../reference/concept-glossary.md), and here we focus on why, once values become several, an ordered group is needed first.

If the previous section dealt with `how a single value exists with a name and a type`, here we look at why, once there are several such values, an ordered group becomes necessary first. If this criterion is established, then even the dictionary in the very next section becomes easier to read not as `another piece of syntax`, but as `a structure for finding by name instead of by order`.

| What to establish in this section | Question that follows immediately | Where it is used again later |
| --- | --- | --- |
| The idea that a list is an ordered group of values | This leads to how it differs from a dictionary, which finds by name, in P2-8.3. | It repeats later when reading NumPy arrays, file lists, and groups of model outputs. |
| The idea that an index is the way to take a value out again by position | This leads to scenes in P2-8.4 where several values are processed in order by iteration. | It reconnects later to slicing, reading array axes, and checking part of a DataFrame. |
| The idea that a list is a mutable value and can therefore change together | This leads to the distinction between reference and copy in the supplementary section P2-8.7. | It continues to matter in preprocessing examples, storing intermediate results, and debugging. |

| Term | Meaning to establish first in this section |
| --- | --- |
| list | An ordered group of values. |
| index | A number indicating a position inside the group. |
| item | An individual value inside the list. |
| mutable value | A value structure in which items can be added or changed. |
| nested list | A structure where a list contains another list inside it. |

## Scope of This Section

Here, we cover the basic structure and initial state of lists. The central question is: `When handling several values in order, by what criteria should they be grouped, taken out, and changed?`

Here, we answer the following questions.

- For what kind of data group is a list suitable?
- In what shapes can a list first be created?
- How is the position of a list read?
- Why must we be careful because a list is a mutable value?
- In what forms do we meet lists in AI practice?

Dictionaries are handled separately in P2-8.3, and the pattern of collecting or changing values with iteration is handled separately in P2-8.4. The distinction between reference and copy is recovered again in the supplementary section P2-8.7.

## Goal of This Section

- You can explain a list as an ordered group of values.
- You can explain that an index starts from 0.
- You can distinguish a list that begins with known values, an empty list, and a list filled with the same value.
- You can explain that a list is a mutable value.
- You can read scores, sentences, model outputs, and file-name lists as lists in AI practice.

## Criteria to Hold First

The criterion you should hold first in this section is that `a list is an ordered group of values`.

| Scene now being seen | Question to recall first |
| --- | --- |
| `[82, 75, 91, 68]` | Which value number matters? |
| `scores[0]` | Is it taking a value out again by position? |
| `scores.append(68)` | Is it changing the existing group itself? |
| `rows = [[1, 2], [3, 4]]` | Even if it looks two-dimensional, is it still a list inside a list? |

In other words, the first feeling that must be established is that a list is `a structure that stores in order, takes out by position, and changes when needed`.

## Three Criteria

Here, rather than Python syntax, we first look at `how should several values be handled together?` The following three criteria become the foundation of later explanations of dictionaries, iteration, and arrays.

| Criterion | Why it matters | Level of understanding needed in this section |
| --- | --- | --- |
| A list is an ordered group of values | It becomes the starting point for grasping the difference from a dictionary | Understand it as a structure where which value is first, second, and so on matters |
| An index is a position number | It connects later to slices, arrays, and reading DataFrames | Read with the rule that the first value starts from `0` |
| A list is a mutable value | It explains why values change together in preprocessing and example code | Remember that two names can be looking at the same list together |

## A List Is an Ordered Group of Values

In general, an ordered group is a structure that places several values in a fixed order and takes them out again by position. Such a structure is needed when `which numbered value it is` has meaning, as in a score list, sentence list, or file list.

In Python, this kind of structure is often expressed with a list.

Problem situation: I first want to see the most basic shape that expresses several scores as one ordered group.
Input: four scores, `82, 75, 91, 68`.
Expected output: the score list and its type are printed.
Concept to check: a list is the basic structure that stores several values in order.

```python
scores = [82, 75, 91, 68]

print(scores)
print(type(scores))
```

Each value inside a Python list can be called an item or an element.

Because a Python list has order, you can take a value out by position.

Problem situation: I want to check how to take out the first and second values by position from a list.
Input: the score list `scores`.
Expected output: the values of `scores[0]` and `scores[1]` are printed.
Concept to check: values in a list are accessed by index, and in Python counting usually starts from 0.

```python
scores = [82, 75, 91, 68]

print(scores[0])
print(scores[1])
```

In Python, an index usually starts from 0. So `scores[0]` is the first value. What matters is that `values are placed in some order, and can be taken out again by that position`.

| Expression | Meaning | Value |
| --- | --- | --- |
| `scores[0]` | first item | `82` |
| `scores[1]` | second item | `75` |
| `scores[-1]` | last item | `68` |

This rule of starting from 0 can feel unfamiliar. But counting from 0 appears often in Python strings, lists, and later NumPy indexing as well. What matters here is not to call a list an array, but to have the sense that `an ordered structure may need position numbers`.

| Perspective | General explanation | In Python |
| --- | --- | --- |
| ordered group | A structure that places several values in order | Uses a list |
| position | The number used to find a value in the group | Usually starts from 0 |
| item | An individual value in the group | Can be taken out like `scores[0]` |

## A List Is Not Just Another Word for Array

A person who learned another language first may immediately understand a list as an array. That is because both have order and allow values to be taken out by position.

But in this section, we do not use list and array as the same word. A Python list is closer to a general-purpose container that stores several values and handles them in order. By contrast, an array in AI numerical computation usually means a data structure for placing numbers of the same kind in a fixed structure and computing on them quickly.

The official Python documentation supports this distinction. `list` is described as a mutable sequence, while the `array` module in the standard library separately provides arrays that efficiently store numeric values. An `array` behaves like a list in some ways, but the kinds of values it can store are limited by a type code fixed at creation.

The confusion can become greater when you look at a multidimensional array. In Python too, if you put lists inside a list, you can make a structure that looks like a table.

Problem situation: I first want to see that putting lists inside a list makes a structure that looks like a table.
Input: two row lists, `[1, 2, 3]` and `[4, 5, 6]`.
Expected output: the nested list `rows`.
Concept to check: a nested list may look two-dimensional, but it is still a structure where a list contains lists.

```python
rows = [
    [1, 2, 3],
    [4, 5, 6],
]
```

This shape looks like a matrix or a two-dimensional array. But it is still simply `a structure where lists are inside a list`. A NumPy multidimensional array (`ndarray`) is a computation structure that has information such as shape, axis, and dtype, and NumPy documentation also describes `ndarray` as an N-dimensional array. Therefore, `a nested list looks like a matrix` and `a nested list is a multidimensional array for numerical computation` must be distinguished.

| Perspective | Python list | Array perspective in numerical computation |
| --- | --- | --- |
| central idea | ordered group of values | a computation target that structurally stores numbers of the same kind |
| main use | storing several targets such as sample lists, file names, or text lists | performing numerical computation on vectors, matrices, model input, and so on |
| kind of values | can hold different types, though usually values of the same purpose are grouped | usually expects the same numeric type |
| way of changing | easy to add or remove values | size, axis, and operation method become more important |
| place in this section | recovery of basic Python syntax | handled separately in Part 2 Chapter 3 and Part 2 Chapter 11 |

So in this section, read a list only as `an ordered group of values`. Arrays, vectors, and matrices for fast numerical computation are handled separately in Part 2 Chapter 3 and Part 2 Chapter 11.

This distinction is important. A Python list is convenient for gathering several samples, but when quickly computing a large amount of numbers in model computation, a separate structure such as a NumPy array is usually used. Therefore, `a list can hold numbers` and `a list is a numerical-computation array` are not the same statement.

## A List Has a Different Role from Other Data Structures

The design of a Python list can be understood as `a mutable sequence that stores ordered values, can add to the end or take them out when needed, and is easy to process repeatedly`. The official Python tutorial also separately explains list methods, the way of using a list like a stack, the limits of using it like a queue, dictionaries, sets, and tuples.

In other words, a list is not a structure that stands in for every kind of grouping. Different structures are chosen depending on what criterion is used to handle values.

| Structure | Central question | Difference from a list |
| --- | --- | --- |
| list | Should several values be stored in order and processed one by one? | Position and order matter, and values can be added or changed |
| tuple | Should it remain as an unchanging group? | A tuple is an immutable sequence, used more like a fixed group of values |
| dictionary | Should a value be found by name or key? | Accesses values by key rather than by position |
| set | Are duplicate-free elements and membership important? | Uniqueness and membership test matter more than order |
| deque | Will values be added and removed often at both ends? | If something must often be taken from the front like a queue, `collections.deque` fits better than a list |
| array | Should numbers of the same kind be computed structurally? | Numeric type, shape, axis, and computation method matter |

Therefore, when looking at a list, it is better to ask first not `is it an array?`, but `is it an ordered general-purpose group?` A list is the most frequently encountered basic structure in Python code, but once the computation purpose becomes clearer, thought has to move toward other structures such as dictionaries, sets, deques, and NumPy arrays.

To summarize this difference again briefly:

| Question needed now | Structure to recall first |
| --- | --- |
| Which numbered value is it? | list |
| Is it found by name? | dictionary |
| Are numbers of the same kind being computed? | array, NumPy |

## A List Can Add and Change Values

A list is a mutable value. If you first understand this point, it becomes easier to read more carefully the pattern of gathering values into an empty list and the pattern of preparing a length with the same value.

Problem situation: I want to directly check that a list can have values added and changed even after it is created.
Input: an initial score list, `append`, and index assignment.
Expected output: a list where a value was added and some items were changed.
Concept to check: a list is a mutable value, and both appending at the end and changing by position are possible.

```python
scores = [82, 75, 91]

scores.append(68)
scores[1] = 77

print(scores)
```

`append()` adds a value to the end of a list. `scores[1] = 77` changes the second item.

In P2-8.1, we said that `a variable is a name attached to a value`. In lists, this perspective becomes even more important.

Problem situation: I want to see whether, when the same list is pointed to by two names, a change through one name is also visible through the other.
Input: `scores` and `other_scores`, both pointing to the same list.
Expected output: the same changed result is printed through both names.
Concept to check: assigning a list to another variable does not always automatically create a copy.

```python
scores = [82, 75, 91]
other_scores = scores

other_scores.append(68)

print(scores)
print(other_scores)
```

`scores` and `other_scores` are not copies of different lists. They point to the same list. So if you add a value through one name, the same change is visible through the other name too.

In this section, we keep only the following criteria.

- The sense of changing one number or string and the sense of changing a list can be different.
- Assigning a list to another name does not automatically create a new copy.
- If the original must be preserved in data preprocessing, whether it is copied must be treated carefully.

Shallow copy and deep copy are not handled deeply here. This difference is reorganized immediately afterward in the supplementary section P2-8.7 through the criterion `when do the original and the copy change together?`

## A List Can Be Joined, Sliced, and Changed with Compact Syntax

When reading Python lists, symbols and square-bracket syntax often appear before function names. Actions that in other languages were encountered with names such as `concat`, `join`, `slice`, and `splice` are sometimes expressed in Python through operators, slices, assignment statements, and the `del` statement.

What matters here is not that `Python list has functions with all of those names`. Python provides a common syntax for handling sequences, and lists use that syntax often.

### Join Lists Together: Concatenation

When you join two lists and make a new list, you can use `+`.

Problem situation: I want to see the simplest example of making a new list by joining two lists.
Input: `front = [1, 2]` and `back = [3, 4]`.
Expected output: `result`, where the two lists are connected.
Concept to check: `+` makes a new joined list rather than changing the existing lists.

```python
front = [1, 2]
back = [3, 4]

result = front + back

print(result)
```

This code makes `[1, 2, 3, 4]`. At this point, `front` and `back` themselves are not changed; instead, a new list is made as the joined result.

If you want to attach other values to the end of an already existing list, you can use `extend()`.

Problem situation: I want to check how to attach values behind an existing list without creating a new list.
Input: the existing list `scores` and the values `[91, 68]` to be added.
Expected output: `scores` with values added to the end.
Concept to check: `extend()` changes the existing list itself.

```python
scores = [82, 75]

scores.extend([91, 68])

print(scores)
```

`+` creates a new joined result, while `extend()` changes the existing list. This difference matters later when distinguishing references from changes.

### Cut a List: Slice

When you want to take out only part of a list, you use a slice.

Problem situation: I want to see all at once how to cut out the front, middle, and back parts of a list.
Input: `scores` containing five scores.
Expected output: the middle part, the first two items, and the back part are each printed.
Concept to check: a slice is syntax for reading a partial range by specifying a start and end range.

```python
scores = [82, 75, 91, 68, 88]

print(scores[1:4])
print(scores[:2])
print(scores[3:])
```

`scores[1:4]` takes values from index 1 up to just before 4. So the result is `[75, 91, 68]`. The rule that `the ending number is not included` can feel unfamiliar, but it is a repeated pattern in Python strings and lists.

A slice is syntax for reading part of the original list.

### Delete or Replace Part of a List: Deletion and Slice Assignment

An action like `splice` from other languages, where a middle range of a list is deleted or replaced, is not provided in Python as a separate `splice()` method. A similar purpose is expressed through `del`, `insert()`, and slice assignment.

Problem situation: I want to check what remains if a middle range of a list is deleted.
Input: `items = ["A", "B", "C", "D"]` and the deletion range `1:3`.
Expected output: a list with the middle two items removed.
Concept to check: if you use `del` together with a slice, you can delete a specific range.

```python
items = ["A", "B", "C", "D"]

del items[1:3]

print(items)
```

`del items[1:3]` deletes from index 1 up to just before 3. The result is `["A", "D"]`.

You can also replace a range with other values.

Problem situation: I want to check whether part of a list can be replaced with a value group of a different length.
Input: the range `items[1:3]` and the new values `["X", "Y", "Z"]`.
Expected output: a list reflecting the changed range.
Concept to check: slice assignment can replace a range even when the length is not the same.

```python
items = ["A", "B", "C", "D"]

items[1:3] = ["X", "Y", "Z"]

print(items)
```

The result is `["A", "X", "Y", "Z", "D"]`. A range does not have to be replaced only with another range of the same length.

### `join` Is a String Action, Not a List Action

`join` appears often in Python, but it is not a list method. It is a method used by a string to connect a list of strings into a single string.

Problem situation: I want to see how `join` is used when combining a list of strings into a single sentence.
Input: the string list `words` and the separator `" "`.
Expected output: the sentence `sentence` connected by spaces.
Concept to check: `join()` belongs to the string side, not to the list side.

```python
words = ["AI", "needs", "data"]

sentence = " ".join(words)

print(sentence)
```

The result is `"AI needs data"`. Here, the subject of the action is not the list, but the string `" "`. This string connects the strings inside `words` by placing spaces between them.

Therefore, when reading lists in Python, it is safer to distinguish things like this.

| What you want to do | Expression often seen in Python | Point of caution |
| --- | --- | --- |
| Join two lists | `front + back` | Makes a new list |
| Attach things at the end of an existing list | `items.extend(values)` | Changes the existing list |
| Read a partial range | `items[1:4]` | The ending index is not included |
| Delete a partial range | `del items[1:4]` | Changes the existing list |
| Replace a partial range | `items[1:4] = values` | The replacement can have a different length |
| Combine a list of strings into one string | `" ".join(words)` | `join()` is a string method |

In this section, you do not need to memorize all of this syntax. It is enough to remember that `Python lists are often handled not only by named functions, but also by sequence syntax that joins, cuts, and changes them`.

## Basic Patterns for Creating a List at the Beginning

In general, to initialize a data structure means to create that structure for the first time. In Python, the way you start a list differs depending on whether values already exist, whether you will fill them later, or whether you first want to make space with the same value. At that time, remember together that a list is a mutable value.

Generalizing it, the ways to start a list divide into three questions. Do you already know the values, will you fill them later, or do you want to first create positions with the same value?

### When You Already Know the Values

If you already know the values that will go in from the beginning, write them inside square brackets (`[]`).

Problem situation: I want to see at once examples of creating different kinds of lists when the values are already known.
Input: a score list, a label list, and a boolean list.
Expected output: the three lists are each printed.
Concept to check: a list can directly initialize groups of numbers, strings, booleans, and other values.

```python
scores = [82, 75, 91, 68]
labels = ["positive", "negative", "neutral"]
flags = [True, False, True]

print(scores)
print(labels)
print(flags)
```

This method reveals the composition of values most directly when making learning examples or small setting lists.

### When Starting from an Empty List

If you do not yet have values but plan to put them in later, you can start with an empty list.

Problem situation: I want to check the basic pattern of starting with an empty list and gathering values one by one later.
Input: an empty list `passed_scores` and two `append` calls.
Expected output: a list containing the added values.
Concept to check: an empty list is often used as the starting point for building results later.

```python
passed_scores = []

passed_scores.append(82)
passed_scores.append(75)

print(passed_scores)
```

This example shows that values can be added even after the list is made. In actual data processing, it is common to gather values that match a condition into an empty list using iteration. That pattern is revisited in P2-8.4.

### When Starting by Filling with the Same Value

There are also times when you know the needed length and want to first fill it with the same value.

Problem situation: I want to see an example of quickly making a list of a fixed length with the same default value.
Input: the default value `0` and the repetition count `5`.
Expected output: a list containing five `0`s.
Concept to check: `[value] * count` can be used when quickly making a simple initial value list.

```python
predictions = [0] * 5

print(predictions)
```

This code makes `[0, 0, 0, 0, 0]`. But while this method is easy to understand for simple values such as numbers or strings, you must be careful when putting lists inside a list.

Problem situation: I want to check why code that looks like it duplicated the same inner list several times can be dangerous.
Input: `rows = [[]] * 3` and adding `"A"` to the first inner list.
Expected output: a result that looks as if all inner lists changed together.
Concept to check: in nested lists, initialization that points to the same object multiple times can create unexpected sharing.

```python
rows = [[]] * 3

rows[0].append("A")

print(rows)
```

This code can look different from what you expected. That is because each inner list was not newly created; instead, the same list is being pointed to multiple times. In this section, we keep the criterion of not creating nested lists in this way.

### When Making a New List by a Repetition Rule

It is also common to process existing values one by one and make a new list. But that is more the topic of iteration than of the list itself. In this section, we leave only the point that `a list is needed to hold a new result`, and actual iteration patterns are handled in P2-8.4.

In this section, choose the starting shape of a list by the following criteria.

| Situation | Initialization pattern |
| --- | --- |
| You already know the values | `scores = [82, 75, 91]` |
| You add values later | `results = []` |
| You fill with the same simple value | `predictions = [0] * 5` |
| You make a new list by a repetition rule | `for` and list comprehension in P2-8.4 |

## Situations Where Lists Are Used

Lists are used when values of the same purpose or context are gathered in order and that position or order has meaning.

### Several Scores

Problem situation: I want to see a basic example of using one score list to calculate several summary values.
Input: the score list `scores`.
Expected output: the calculation results of maximum, minimum, and average.
Concept to check: a list can gather several numeric values at once and serve as the input to summary computation.

```python
scores = [82, 75, 91, 68]

print(max(scores))
print(min(scores))
print(sum(scores) / len(scores))
```

A score list can have order, and the whole thing can also be gathered to calculate an average.

### Several Sentences

Problem situation: I want to see an example of processing several sentences one by one in the same way.
Input: the list `texts` containing three sentences.
Expected output: each sentence is printed one after another in a loop.
Concept to check: a list is good for iterating over several items of the same kind, such as text, in order.

```python
texts = [
    "AI is useful.",
    "Data quality matters.",
    "Models can fail.",
]

for text in texts:
    print(text)
```

In LLM or text-classification practice, you often encounter lists of sentences.

### Several Model Outputs

Problem situation: I want to see an example of judging several probability scores one by one against a criterion.
Input: the probability list `probabilities` and the threshold `0.8`.
Expected output: `high confidence` or `check` is printed for each score.
Concept to check: a list can be used to evaluate multiple model output values in order.

```python
probabilities = [0.92, 0.31, 0.77, 0.12]

for probability in probabilities:
    if probability >= 0.8:
        print("high confidence")
    else:
        print("check")
```

If a model produced probability scores for several inputs, that result can also be seen as a list.

### Several File Names

Problem situation: I want to see the simplest example of processing several file names by the same procedure.
Input: the list containing `train.csv`, `valid.csv`, and `test.csv`.
Expected output: each file name is printed one after another.
Concept to check: a list is suitable for listing several work targets of the same kind in order.

```python
file_names = [
    "train.csv",
    "valid.csv",
    "test.csv",
]

for file_name in file_names:
    print(file_name)
```

In project practice, there are many cases where several files must be processed in the same way.

## Case Study

### Case 1. What Is Needed to Handle Several Prediction Scores at Once?

Suppose a model produced five probability scores for five samples. At first, a person may be able to look at values one by one such as `0.92`, `0.31`, and `0.77`, but soon the need appears: `I want to process the whole thing in order` and `I want to look again only at the third result`.

At that point, if the values are placed in separate variables like `score1`, `score2`, and `score3`, managing them becomes inconvenient very quickly. It becomes hard to handle several ordered values by the same criterion, and iteration or partial selection also becomes cumbersome.

The list is exactly the structure suited for this scene. When there are several values of the same purpose, such as scores, sentences, or file names, and order has meaning, once they are grouped in a list, it becomes easy to take them out by index, add a new one at the end when needed, and make a new list.

The confirmable result appears immediately through the index. If you can directly check a third value like `probabilities[2]`, and if you can attach a new result at the end with `append()`, then this is a situation where a list fits better than naming separate variables one by one.

## Checklist

- Can you explain a list as an `ordered group of values`?
- Can you read `scores[0]` and `scores[-1]`?
- Can you explain why it is dangerous to use list and NumPy array as the same word?
- Can you say that the same list can be pointed to by two names together?
- You can explain a list as an ordered group of values.
- You can explain the meaning of `scores[0]` and `scores[-1]`.
- You can distinguish a list that starts with known values, an empty list, and a list filled with the same value.
- You can read the flow of adding values with `append()`.
- You can roughly distinguish `+`, `extend()`, slice, `del`, and slice assignment.
- You can explain that `join()` is not a list method but a string method.
- You can explain that Python lists do not have a JavaScript-style `splice()` method, and that similar work is expressed through `del`, `insert()`, and slice assignment.
- You can explain that the same list can be pointed to by several names.
- You can explain that care is needed when creating a nested list by repeating the same value.
- Can you first distinguish whether the current question is about order, index, or mutability?

## Sources and References

- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-06-24.
- Python Software Foundation, [Built-in Types](https://docs.python.org/3/library/stdtypes.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-06-24.
- Python Software Foundation, [array — Efficient arrays of numeric values](https://docs.python.org/3/library/array.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-06-25.
- NumPy Developers, [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html){: target="_blank" rel="noopener noreferrer" }, NumPy documentation, checked on 2026-06-25.
