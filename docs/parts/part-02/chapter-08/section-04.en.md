# P2-8.4 Loops: Processing Iterables One Item at a Time

> Section ID: `P2-8.4`
> Version: `v2026.09.15`

Applying the same criterion to four scores requires retrieving and comparing each score. A loop repeats this processing to print results, collect selected values, or calculate totals and counts.

## for and Item Processing

`for score in scores:` retrieves values from `scores` one at a time under the name `score`. The indented code below the colon (`:`) runs for each item. This code prints `82`, `75`, `91`, and `68` on separate lines.

```python
scores = [82, 75, 91, 68]

for score in scores:
    print(score)
```

`print(score)` executes four times, producing four lines. Indentation determines which code belongs to the loop.

You can retrieve the same values by position. `len(scores)` is the count `4`, and `range(4)` supplies `0` through `3`. The output matches the preceding example.

```python
scores = [82, 75, 91, 68]

for i in range(len(scores)):
    print(scores[i])
```

When you only need values, use `for score in scores` directly. Use `enumerate()` when both positions and values are needed.

## Positions, Keys, and Paired Lists

### Positions and Values: enumerate

`enumerate(scores)` provides both positions and values. The output is `0 82`, `1 75`, `2 91`, and `3 68`.

```python
scores = [82, 75, 91, 68]

for index, score in enumerate(scores):
    print(index, score)
```

`index, score` receives the two members of each pair. This helps when recording a faulty sample's position alongside its value.

### Keys and Values: items

A dictionary's `.items()` provides keys and values together. The code prints metric names and values as `accuracy 0.91` and `loss 0.32`.

```python
metrics = {"accuracy": 0.91, "loss": 0.32}

for name, value in metrics.items():
    print(name, value)
```

`for name in metrics` retrieves only keys. Using `.items()` also retrieves their associated values.

### Two Lists: zip

`zip()` takes one item at a time from multiple iterables and groups them together. The code pairs sentences and labels, printing `good positive`, `bad negative`, and `great positive`.

```python
texts = ["good", "bad", "great"]
labels = ["positive", "negative", "positive"]

for text, label in zip(texts, labels):
    print(text, label)
```

Pairing is by position. `zip()` does not find the label that matches a sentence's meaning.

By default, `zip()` stops when the shorter list ends. Shortening `labels` to `["positive", "negative"]` prints only two pairs, leaving `great` unprocessed. For data that must have equal lengths, use `zip(texts, labels, strict=True)`. It processes the first two pairs, then raises `ValueError` on encountering the mismatch.

## Iterables and Iterators

An iterable is an object that supports iteration. Lists, strings, dictionaries, file objects, and generators that produce values on demand can all be iterated. Files yield lines and dictionaries yield keys, so not every iterable needs integer indexing.

An iterator provides the next item and retains progress. Create one with `iter()` and retrieve values with `next()`. This example retrieves `82` and `75` from `[82, 75]`, then prints the supplied default `end` when exhausted.

```python
scores = [82, 75]
iterator = iter(scores)

print(next(iterator))
print(next(iterator))
print(next(iterator, "end"))
```

Calling `next(iterator)` again without a default raises `StopIteration`. A `for` loop receives items from an iterator and stops when it signals exhaustion.

| Term | Role | Example |
| --- | --- | --- |
| Iterable | Object to iterate over | `scores` |
| Iterator | Supplies next items and retains progress | Result of `iter(scores)` |
| Loop | Processes retrieved values | `for score in scores` |

PEP 234, written in 2001 around Python 2.2, proposed an interface through which objects provide iteration. It helped extend `for` beyond sequences to many kinds of objects.

## An Iterator After Consumption

A fresh iteration over a list can start at its first item again, but an exhausted iterator does not rewind. `zip()` also returns an iterator.

```python
texts = ["good", "bad"]
labels = ["positive", "negative"]
pairs = zip(texts, labels)

print(list(pairs))
print(list(pairs))
```

The first output is `[('good', 'positive'), ('bad', 'negative')]`; the second is `[]`. The data did not vanish: `pairs` was consumed. Replacing its assignment with `pairs = list(zip(texts, labels))` stores the pairs in a list, so both outputs match. This also keeps all pairs in memory.

A `for` loop over an empty list never executes its body. Initializing `total = 0` outside the loop leaves a zero total for empty input. If a name is first assigned only inside the loop, that assignment never happens for empty input.

## Filtering and Transformation

### Selecting Matching Values

Assume `0` denotes a missing score in this dataset. `score != 0` checks for a nonzero score. Appending only matching values to an empty list prints `[82, 75, 91]`.

```python
scores = [82, 0, 75, 0, 91]
valid_scores = []

for score in scores:
    if score != 0:
        valid_scores.append(score)

print(valid_scores)
```

The `append()` indented under `if` runs only when the condition is true. If real scores can be zero, this would remove valid scores too; missing values need a different marker.

### Applying One Transformation to Every Value

Dividing scores out of 100 by 100 expresses them between 0 and 1. Transforming `[82, 75, 91, 68]` prints `[0.82, 0.75, 0.91, 0.68]`.

```python
scores = [82, 75, 91, 68]
normalized_scores = []

for score in scores:
    normalized_scores.append(score / 100)

print(normalized_scores)
```

The original scores remain unchanged while `normalized_scores` collects the results. Similar loops lowercase strings or remove surrounding whitespace.

## Comprehensions

A comprehension is a compact expression for building a new data structure through iteration. `[expression for variable in iterable]` creates a new list.

Squaring the values `0` through `4` from `range(5)` prints `[0, 1, 4, 9, 16]`.

```python
squares = [number * number for number in range(5)]

print(squares)
```

A condition at the end includes only matching items. This prints `[82, 75, 91]`, just like the earlier missing-score filter.

```python
scores = [82, 0, 75, 0, 91]

valid_scores = [score for score in scores if score != 0]

print(valid_scores)
```

The loop that divides scores by 100 can also be shortened. Transforming `[82, 75, 91]` prints `[0.82, 0.75, 0.91]`.

```python
scores = [82, 75, 91]

normalized_scores = [score / 100 for score in scores]

print(normalized_scores)
```

| Part | Meaning |
| --- | --- |
| `scores` | Input list |
| `score` | One retrieved score |
| `score / 100` | Value placed in the new list |

Using `key: value` inside braces creates a dictionary. The result is `{'negative': 0, 'positive': 1, 'neutral': 2}`.

```python
labels = ["negative", "positive", "neutral"]

label_to_id = {label: index for index, label in enumerate(labels)}

print(label_to_id)
```

Use a normal `for` loop when conditions and intermediate calculations deserve separate steps. Only `82` and `91` pass the threshold `60`, so this code prints `[0.82, 0.91]`.

```python
items = [{"score": 82}, {"score": 55}, {"score": 91}]
results = []

for item in items:
    if item["score"] >= 60:
        normalized_score = item["score"] / 100
        results.append(normalized_score)

print(results)
```

## Totals and Counts by Key

### Accumulating a Total

Accumulation updates a running result with each new value. Starting at `total = 0`, adding `[82, 75, 91, 68]` prints the final total `316`.

```python
scores = [82, 75, 91, 68]
total = 0

for score in scores:
    total = total + score

print(total)
```

`total = total + score` adds the current score to the previous total and assigns the result back to `total`.

| Current score | total before addition | total after addition |
| --- | --- | --- |
| 82 | 0 | 82 |
| 75 | 82 | 157 |
| 91 | 157 | 248 |
| 68 | 248 | 316 |

### Splitting by a Condition

Split `[82, 55, 91, 42, 68]` into scores at least `60` and scores below it. The outputs are passed `[82, 91, 68]` and failed `[55, 42]`.

```python
scores = [82, 55, 91, 42, 68]
passed = []
failed = []

for score in scores:
    if score >= 60:
        passed.append(score)
    else:
        failed.append(score)

print(passed)
print(failed)
```

When the `if` condition is false, the `else` block runs. Raising the threshold to `70` moves `68` to the failed list, producing `[82, 91]` and `[55, 42, 68]`.

### Counts by Label

A dictionary can accumulate occurrences per label. This list has three `positive` labels and one each of `negative` and `neutral`, yielding `{'positive': 3, 'negative': 1, 'neutral': 1}`.

```python
labels = ["positive", "negative", "positive", "neutral", "positive"]
label_counts = {}

for label in labels:
    label_counts[label] = label_counts.get(label, 0) + 1

print(label_counts)
```

For a new label, `get(label, 0)` returns `0` and the count is stored as `1`. Each subsequent occurrence adds `1` to the existing count.

## Case: Collecting the Names of Students Who Passed

Kim scored 82.5, Lee 55, and Park 91. Each student is a dictionary, and the three students form a list. Collecting names with scores at least `60` prints `['Kim', 'Park']`.

```python
students = [
    {"name": "Kim", "score": 82.5},
    {"name": "Lee", "score": 55.0},
    {"name": "Park", "score": 91.0},
]

passed_students = []

for student in students:
    if student["score"] >= 60:
        passed_students.append(student["name"])

print(passed_students)
```

The loop receives each student dictionary, checks `student["score"]`, and appends the matching student's `"name"`. Changing the threshold to `90` leaves only `['Park']`.

## Deleting Items During Iteration

Deleting items while iterating shifts later items forward and can skip some. This code attempts to remove all zeros but leaves one of the consecutive zeros, printing `[82, 0, 91]`.

```python
scores = [82, 0, 0, 91]

for score in scores:
    if score == 0:
        scores.remove(score)

print(scores)
```

Removing the first zero pulls the next zero into its position. Iteration advances and does not inspect that shifted zero. Collecting a new result while preserving the original avoids this problem; the following code prints `[82, 91]`.

```python
scores = [82, 0, 0, 91]
filtered_scores = []

for score in scores:
    if score != 0:
        filtered_scores.append(score)

print(filtered_scores)
print(scores)
```

The second output, the original list, stays `[82, 0, 0, 91]`. As in the filtering example, zero is assumed to mark missing input.

## Calculating Sentence Lengths

Applying `len()` to each sentence creates a list of character counts. Including spaces, this example prints `[12, 15, 12]`.

```python
texts = ["AI is useful", "Models can fail", "Data matters"]
lengths = []

for text in texts:
    lengths.append(len(text))

print(lengths)
```

Lengths follow input order. The `15` in `lengths[1]` is the length of the second sentence, `"Models can fail"`.

## Checklist

- Read `for item in items` and explain its execution flow.
- Distinguish iterables from iterators at an introductory level.
- Explain why iterable includes dictionaries, files, and generators as well as sequences.
- Use `enumerate()` when positions are needed.
- Use `.items()` for dictionary keys and values together.
- Recognize `zip()` for pairing collections.
- Distinguish item processing, transformation, accumulation, and conditional splitting.
- Read list and dictionary comprehensions as iteration that builds new structures.
- Explain when a normal `for` loop is clearer than a complex comprehension.
- Explain why mutating original data during iteration can cause problems.

- Explain why reading an exhausted iterator again produces no items.

## Sources and References


- Python Software Foundation, [More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, checked on 2026-09-15. Used as the official basis for `for`, `range()`, function-definition examples, and control-flow descriptions.
- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, checked on 2026-07-20. Used to confirm list comprehensions, dictionary iteration, `items()` examples, and cautions about modifying a collection while iterating.
- Python Software Foundation, [Glossary: iterable, iterator](https://docs.python.org/3/glossary.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, checked on 2026-07-20. Used as the basis for distinguishing iterable and iterator at an introductory level.
- Python Software Foundation, [The for statement](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, checked on 2026-07-20. Used to confirm that a `for` statement assigns items one by one from an iterator over an iterable expression.
- Ka-Ping Yee, Guido van Rossum, [PEP 234 -- Iterators](https://peps.python.org/pep-0234/){: target="_blank" rel="noopener noreferrer" }, Python Enhancement Proposals, 2001, checked on 2026-07-20. Used to confirm the historical background in which Python's iteration interface moved beyond sequence-centered iteration toward objects providing their own iteration behavior.

- Python Software Foundation, [Built-in Functions: iter, next, zip](https://docs.python.org/3/library/functions.html){: target="_blank" rel="noopener noreferrer" }, 2026-09-15. Iterator exhaustion, defaults, and zip length checks including strict.
