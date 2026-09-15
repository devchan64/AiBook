# P2-8.2 Lists: Ordered Groups of Values

> Section ID: `P2-8.2`
> Version: `v2026.09.15`

## Order and Indices

A list is a data structure that holds values in order. An index lets you retrieve a particular value from scores, sentences, or file names.

Place `82, 75, 91, 68` inside square brackets and name the list `scores`. The code prints `[82, 75, 91, 68]` and `<class 'list'>`.

```python
scores = [82, 75, 91, 68]

print(scores)
print(type(scores))
```

Each value in a Python list is called an item or element.

The first index is `0`. The code prints `82` and `75`, the values at indices `0` and `1`.

```python
scores = [82, 75, 91, 68]

print(scores[0])
print(scores[1])
```

Negative indices count from the end. `-1` refers to the last item.

| Expression | Meaning | Value |
| --- | --- | --- |
| `scores[0]` | First item | `82` |
| `scores[1]` | Second item | `75` |
| `scores[-1]` | Last item | `68` |

## Out-of-Range Indices and Empty Lists

A list of length 4 has nonnegative indices 0 through 3. `scores[4]` requests a fifth item and raises `IndexError`. A slice, however, returns the available portion even if its end exceeds the list length.

| Expression | Result for `scores = [82, 75, 91, 68]` |
| --- | --- |
| `scores[3]` | `68` |
| `scores[4]` | `IndexError` |
| `scores[2:10]` | `[91, 68]` |
| `scores[4:10]` | `[]` |

Both `len([])` and `sum([])` are 0, but an empty list does not have mean 0. `sum([]) / len([])` divides by zero and raises `ZeroDivisionError`. Check that at least one item was collected before computing a mean.

## Lists and Arrays

Readers familiar with another language may equate lists with arrays: both have an order and support indexed access.

A Python list is a general-purpose container for ordered values. In AI numerical computing, an array usually means a structure for arranging numbers of the same kind and computing with them efficiently.

Python documents `list` as a mutable sequence. Its standard-library `array` module separately provides efficient arrays of numeric values. Although an `array` behaves like a list in some respects, its element types are constrained by the type code chosen at creation.

Multidimensional arrays can make this distinction harder to see. Lists inside a list can also form a table-like structure.

Putting the rows `[1, 2, 3]` and `[4, 5, 6]` inside one list creates a nested list. The code prints the full structure and `4`, the first value of the second row.

```python
rows = [
    [1, 2, 3],
    [4, 5, 6],
]

print(rows)
print(rows[1][0])
```

This resembles a matrix or two-dimensional array, but it remains a list containing lists. NumPy's `ndarray` is a computational structure with information such as shape, axis, and dtype; its documentation calls it an N-dimensional array. Looking like a matrix does not make a nested list a numerical multidimensional array.

| Aspect | Python list | Array in numerical computing |
| --- | --- | --- |
| Main idea | Ordered group of values | Structured numbers used for computation |
| Typical use | Store samples, file names, or texts | Calculate with vectors, matrices, or model inputs |
| Value types | May mix types, usually grouped for one purpose | Usually expects one numerical type |
| Changes | Easy to add or remove items | Size, axes, and operations matter more |

## Choosing a Data Structure

A Python list is a mutable sequence designed to hold ordered values, support adding or removing items at the end, and make iteration convenient. The official tutorial separately discusses list methods, stacks, limitations as queues, dictionaries, sets, and tuples.

A list does not replace every kind of collection. Choose a structure according to how you need to handle its values.

| Structure | Main question | Difference from a list |
| --- | --- | --- |
| List | Store and process values in order? | Index and order matter; items can be added or changed |
| Tuple | Keep a fixed grouping? | An immutable sequence, often used for fixed groups |
| Dictionary | Find values by name or key? | Access by key rather than position |
| Set | Need unique elements and membership tests? | Uniqueness and membership matter more than order |
| Deque | Frequently add and remove at both ends? | `collections.deque` suits frequent removal from the front better |
| Array | Compute with structured numerical values? | Numerical type, shape, axes, and operations matter |

## Mutation and References

Lists are mutable sequences: their items can be added or changed.

Append `68` to the scores and change the second score from `75` to `77`. The result is `[82, 77, 91, 68]`.

```python
scores = [82, 75, 91]

scores.append(68)
scores[1] = 77

print(scores)
```

`append()` adds a value at the end. `scores[1] = 77` changes the second item.

`other_scores = scores` adds another name for the same list; it does not copy it. Appending `68` through `other_scores` makes both outputs `[82, 75, 91, 68]`.

```python
scores = [82, 75, 91]
other_scores = scores

other_scores.append(68)

print(scores)
print(other_scores)
```

`scores` and `other_scores` refer to the same list, not separate copies. A change through either name is visible through the other.

## Return Values of Mutating Methods

`append()` changes the original list and returns `None`. This code prints `[82, 75, 91]` and `None`.

```python
scores = [82, 75]
result = scores.append(91)
print(scores)
print(result)
```

`result` is not the modified list. With `scores = scores.append(91)`, the item is appended, but the name `scores` then refers to `None`. To keep using the list, call the mutation alone: `scores.append(91)`.

## Concatenation, Slicing, and Deletion

Python list code often uses symbols and square brackets rather than named functions. Operations called `concat`, `join`, `slice`, or `splice` elsewhere may appear as operators, slices, assignments, or `del` statements in Python.

### Concatenation

Use `+` to combine two lists into a new list. Use `extend()` to add values to the end of an existing list.

`[1, 2] + [3, 4]` creates `[1, 2, 3, 4]` while `front` stays `[1, 2]`. In contrast, `extend()` changes the existing `scores` to `[82, 75, 91, 68]`.

```python
front = [1, 2]
back = [3, 4]

combined = front + back
print("combined:", combined)
print("front after +:", front)

scores = [82, 75]

scores.extend([91, 68])
print("scores after extend:", scores)
```

`+` creates a new concatenated result; `extend()` changes the original list.

### Slicing

A slice retrieves a range of items from a list.

Retrieve a middle range, the first two items, and the trailing range from five scores. The outputs are `[75, 91, 68]`, `[82, 75]`, and `[68, 88]`.

```python
scores = [82, 75, 91, 68, 88]

print(scores[1:4])
print(scores[:2])
print(scores[3:])
```

`scores[1:4]` includes indices from 1 up to, but not including, 4. It returns `[75, 91, 68]`; the value `88` at index 4 is excluded.

Slicing a list creates a new list containing the selected items.

### Deleting and Replacing a Range

Python has no separate list `splice()` method for deleting or replacing a middle range. Similar operations use `del`, `insert()`, or slice assignment.

Deleting indices 1 up to, but not including, 3 from `["A", "B", "C", "D"]` prints `['A', 'D']`.

```python
items = ["A", "B", "C", "D"]

del items[1:3]

print(items)
```

`del items[1:3]` removes that range, leaving `["A", "D"]`.

Replace the middle items `"B"`, `"C"` with `"X"`, `"Y"`, `"Z"`. The result is `['A', 'X', 'Y', 'Z', 'D']`, increasing the length from 4 to 5.

```python
items = ["A", "B", "C", "D"]

items[1:3] = ["X", "Y", "Z"]

print(items)
```

### Joining Strings: join

`join` is common in Python but is not a list method. It is a string method that joins a collection of strings into one string.

Joining `["AI", "needs", "data"]` with spaces prints `AI needs data`. The space string in `" ".join(words)` is the separator.

```python
words = ["AI", "needs", "data"]

sentence = " ".join(words)

print(sentence)
```

The result is `"AI needs data"`. The operation belongs to the string `" "`, which joins the strings in `words` with spaces between them.

| Goal | Common Python expression | Note |
| --- | --- | --- |
| Combine two lists | `front + back` | Creates a new list |
| Extend an existing list | `items.extend(values)` | Mutates the list |
| Read a range | `items[1:4]` | Excludes the end index |
| Delete a range | `del items[1:4]` | Mutates the list |
| Replace a range | `items[1:4] = values` | Replacement length may differ |
| Join strings into one string | `" ".join(words)` | `join()` is a string method |

## Initializing Lists

Initialization creates a data structure. Choose its initial form according to whether values are already available or will be collected later.

### When Values Are Known

Write known values directly inside brackets. The code prints lists of scores, labels, and Boolean values in their original order.

```python
scores = [82, 75, 91, 68]
labels = ["positive", "negative", "neutral"]
flags = [True, False, True]

print(scores)
print(labels)
print(flags)
```

This makes the contents explicit for small learning examples or configuration lists.

### Starting with an Empty List

Adding `82` and `75` to `[]` one at a time prints `[82, 75]`. Each new value is collected with `append()`.

```python
passed_scores = []

passed_scores.append(82)
passed_scores.append(75)

print(passed_scores)
```

Lists can grow after creation. Data processing often uses a loop to collect matching values in an initially empty list.

### Filling a Known Length with One Value

`[0] * 5` repeats the initial value `0` five times, printing `[0, 0, 0, 0, 0]`.

```python
predictions = [0] * 5

print(predictions)
```

This creates `[0, 0, 0, 0, 0]`. It is straightforward for simple values such as numbers or strings, but nested lists need care.

`[[]] * 3` refers to one inner empty list in three positions. Appending `"A"` through the first position prints `[['A'], ['A'], ['A']]`.

```python
rows = [[]] * 3

rows[0].append("A")

print(rows)
```

Create the inner lists separately to change rows independently. With `rows = [[], [], []]`, the result becomes `[['A'], [], []]`: only the first row changes.

## Lists of Scores, Sentences, and Files

Use a list when values share a purpose or context and their positions or order matter.

### Multiple Scores

For `[82, 75, 91, 68]`, the maximum is `91`, minimum `68`, and mean `79.0`. `sum()` returns the total and `len()` the item count; dividing them gives the mean.

```python
scores = [82, 75, 91, 68]

print(max(scores))
print(min(scores))
print(sum(scores) / len(scores))
```

### Multiple Sentences

A `for` loop retrieves three sentences in order. `text` refers to each sentence in turn, and each is printed on its own line.

```python
texts = [
    "AI is useful.",
    "Data quality matters.",
    "Models can fail.",
]

for text in texts:
    print(text)
```

Sentence lists are common in LLM and text-classification exercises.

### Multiple Model Outputs

Compare `[0.92, 0.31, 0.77, 0.12]` against `0.8`. Only the first value passes, so the code prints `above threshold` once and `check` three times.

```python
probabilities = [0.92, 0.31, 0.77, 0.12]

for probability in probabilities:
    if probability >= 0.8:
        print("above threshold")
    else:
        print("check")
```

Changing the threshold to `0.7` also admits `0.77`, producing `above threshold` twice. Passing a chosen threshold does not guarantee a correct prediction.

### Multiple File Names

The code retrieves three file names and prints `train.csv`, `valid.csv`, and `test.csv` in order. It does not read the files themselves.

```python
file_names = [
    "train.csv",
    "valid.csv",
    "test.csv",
]

for file_name in file_names:
    print(file_name)
```

## Case: Inspecting the Third Prediction Score

Suppose `[0.92, 0.31, 0.77, 0.12]` stores predictions in input order. The third input's score is `0.77` at index `2`. Appending a new score `0.85` preserves the existing positions and increases the length to `5`.

```python
probabilities = [0.92, 0.31, 0.77, 0.12]
print(probabilities[2])

probabilities.append(0.85)
print(probabilities)
print(len(probabilities))
```

The outputs are `0.77`, `[0.92, 0.31, 0.77, 0.12, 0.85]`, and `5`. If inputs and predictions correspond by position, do not reorder only one list. Sorting only scores can make the third position refer to a different input.

## Checklist

- Explain a list as an ordered group of values.
- Explain `scores[0]` and `scores[-1]`.
- Distinguish known-value, empty, and repeated-value initialization.
- Read how `append()` adds an item.
- Distinguish `+`, `extend()`, slicing, `del`, and slice assignment.
- Explain that `join()` is a string method, not a list method.
- Explain how `del`, `insert()`, and slice assignment replace JavaScript-style `splice()` operations.
- Explain how multiple names can refer to one list.
- Explain the risk of repeating nested lists.

- Explain out-of-range indexing versus slicing, the empty-list mean error, and the return value of `append()`.

## Sources and References


- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, checked on 2026-07-20. Used to confirm list methods, examples of using lists as stacks, list comprehensions, and nested list examples.
- Python Software Foundation, [Built-in Types](https://docs.python.org/3/library/stdtypes.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, checked on 2026-09-15. Used to confirm sequence types, mutable sequence operations, indexing, and slicing behavior.
- Python Software Foundation, [array — Efficient arrays of numeric values](https://docs.python.org/3/library/array.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, checked on 2026-07-20. Used to confirm that the standard-library `array` stores values of the same basic type efficiently.
- NumPy Developers, [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, checked on 2026-07-20. Used to confirm that NumPy arrays are the core structure for handling large numeric data efficiently, unlike ordinary Python lists.
