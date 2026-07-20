# P2-11.4 Supplemental: How to Read Shape and Shared Origins Together in NumPy

> Section ID: `P2-11.4`
> Version: `v2026.07.20`

In P2-11.2, we looked at indexing, slicing, and axis. In P2-11.3, we looked at broadcasting and vectorization. But when reading actual NumPy code, the next questions often remain.

`Is this selection still looking at the original array?`
`Or did it create a new array?`
`Why did the shape suddenly change from (3,) to (3, 1)?`

This supplemental learning gathers those questions together.

Here, we provide a basic explanation that groups together `boolean mask`, `fancy indexing`, `np.newaxis`, and `shared view`. Even if indexing, slicing, and broadcasting from the previous Sections already make sense, this is the place to reconnect how selection style and shape change relate to shared origin.

## First Reading Criteria: How to Read Shape and Shared Origins Together in NumPy

- You can explain that basic slicing is often read as a way of looking at part of the original array.
- You can explain that fancy indexing and boolean masks are often read as ways of creating a new array.
- You can explain that even if shapes look similar, shared-origin status may still differ.
- You can explain `np.newaxis` as notation that adds a length-1 axis.
- You can explain that when reading broadcasting code, `value`, `shape`, and `shared origin` should be checked together.

## One Scene to Hold First

The first scene to hold in this supplemental learning is that `how you selected` and `how you changed the shape` together change both shared origin and the direction of calculation.

| Code scene | The first question to read | The key point to hold now |
| --- | --- | --- |
| `x[1:4]` | Are we still looking at the range as-is? | There is a high chance it shares the original |
| `x[[1, 3, 4]]` | Are we gathering separate positions? | It is safer to read it as a new array |
| `x[x >= 80]` | Are we filtering only values that meet a condition? | It is safer to read it as a new array |
| `x[:, np.newaxis]` | Are we adding one more axis? | The `shape` changes and broadcasting is read differently |

In other words, in NumPy it is not enough to say only `some part was selected`. You should first separate `viewing a range`, `gathering positions`, `filtering by condition`, and `adding an axis` in order to understand view or copy, shape, and broadcasting together.

## Background

In the supplemental learning of P2-8.7, we first looked at `does the original change together with it?` through Python lists and copying. The same question returns in NumPy. But in NumPy, it is not enough to ask only `was it copied?`; you also need to ask `how did the shape change?`

For example, `x[1:4]` and `x[[1, 3, 4]]` both look as if they selected only some values, but one may still look at the original while the other may create a new array. And `x[:, np.newaxis]` changes the whole broadcasting pattern even when the values do not change.

Read this Section when slicing and axis from P2-11.2 make sense but you still get confused about whether `this selection changes the original too`, or when broadcasting from P2-11.3 makes sense but you stop when `(3, 1)` and `(1, 3)` suddenly appear. Once you hold this standard, you can read slicing, axis, and broadcasting together with `shape` and `shared origin`.

## Three Criteria

| Criterion | Why it matters | Level of understanding needed in this Section |
| --- | --- | --- |
| What was selected | It keeps you from mistaking slicing, fancy indexing, and masks as the same kind of selection. | First distinguish whether it cut a range or gathered only certain positions. |
| How the `shape` changed | It reveals why the calculation changes even if the values look the same. | Understand that the difference among `(3,)`, `(3, 1)`, and `(1, 3)` changes calculation direction. |
| Whether the original is still shared | It prevents later value edits from changing experiment results unexpectedly. | If values may be modified, first check whether a copy is needed. |

| Term | Meaning to capture first in this Section |
| --- | --- |
| boolean mask | A selection style that leaves only the values whose condition is true. |
| fancy indexing | A selection style that gathers values by specifying several positions like a list. |
| `np.newaxis` | Notation that changes array shape by adding an axis of length 1. |
| shared view | A state where the selection result is connected to the original array and may change together with it. |
| copy | A way of creating a new array separated from the original. |

## Basic Slicing Is Often Read as Looking at Part of the Original

In P2-11.2, slicing was introduced as notation that leaves a range. In NumPy, this basic slicing often works as a way of looking at part of the original array together.

Problem situation: We check whether the original also changes when we modify part of an array selected through slicing.
Input: The one-dimensional array `scores` and the slice `scores[1:4]`.
Expected output: A value changed through the slice is reflected back in the original array.
Concept to check: See that basic slicing may look like a new array but can still be read as connected to the original.

```python
# This supplemental example checks NumPy array shape changes together with whether data is shared with the original.
import numpy as np

scores = np.array([82, 75, 45, 90, 61])
middle = scores[1:4]

middle[0] = 999

print(scores)
print(middle)
```

The output is as follows.

```text
[ 82 999  45  90  61]
[999  45  90]
```

Read it here like this.

- It is risky to think of `scores[1:4]` only as `three copied values gathered separately`.
- Basic slicing is often read as a way of looking at part of the original array.
- So if the value is changed later, the original may change too.

This intuition connects directly to the question from P2-8.7: `when do the original and the copied result change together?`

## Fancy Indexing and Boolean Masks Gather Chosen Values into a New Result

Now look at cases that still seem like `partial selection` but work differently.

Problem situation: We compare how fancy indexing, which picks separate positions, and a boolean mask, which filters by condition, differ from the original.
Input: The array `scores`, the position list `[1, 3, 4]`, and the condition `scores >= 80`.
Expected output: Even if the fancy-indexing result and the boolean-mask result are modified, the original `scores` remains unchanged.
Concept to check: See that results gathered by specific positions or by filtering are safer to read as new arrays.

```python
# This supplemental example checks NumPy array shape changes together with whether data is shared with the original.
scores = np.array([82, 75, 45, 90, 61])

picked = scores[[1, 3, 4]]
high_scores = scores[scores >= 80]

picked[0] = 500
high_scores[0] = 700

print(scores)
print(picked)
print(high_scores)
```

The output is as follows.

```text
[82 75 45 90 61]
[500  90  61]
[700  90]
```

Here, `scores[[1, 3, 4]]` gathers the values at positions 1, 3, and 4 separately. This style is called fancy indexing.

`scores[scores >= 80]` leaves only values whose condition is true. This style is called a boolean mask.

Understand both here as follows.

- Basic slicing is closer to `viewing the range as it is`.
- Fancy indexing and boolean masks are closer to `gathering the chosen values separately`.

So shared-origin behavior can differ when values are changed.

## Even if They Both Select Part of the Array, the Question Is Different

Slicing, fancy indexing, and boolean masks all look similar in the sense that they select only some values. But in practice they answer different questions.

| Expression | The first question to read | Safer beginner interpretation |
| --- | --- | --- |
| `x[1:4]` | Which range should remain? | Viewing a range |
| `x[[1, 3, 4]]` | Which positions should be pulled out separately? | Gathering positions |
| `x[x >= 80]` | Which values that satisfy the condition should remain? | Filtering by condition |

If you distinguish this difference first, NumPy code becomes much less confusing.

## `np.newaxis` Adds an Axis of Length 1

Now look at notation that changes `shape` rather than choosing values.

Problem situation: We distinguish whether to view the same one-dimensional array as a row-like shape or a column-like shape only by changing its shape.
Input: The one-dimensional array `scores`, plus `scores[:, np.newaxis]` and `scores[np.newaxis, :]`.
Expected output: The three shapes `(3,)`, `(3, 1)`, and `(1, 3)` are printed.
Concept to check: See that `np.newaxis` does not change the values themselves, but adds a length-1 axis and changes the calculation direction.

```python
# This supplemental example checks NumPy array shape changes together with whether data is shared with the original.
scores = np.array([82, 75, 45])

print(scores.shape)
print(scores[:, np.newaxis].shape)
print(scores[np.newaxis, :].shape)
```

The output is as follows.

```text
(3,)
(3, 1)
(1, 3)
```

These three arrays may look as if they hold similar numbers, but they are read differently.

| Expression | shape | How to read it |
| --- | --- | --- |
| `scores` | `(3,)` | A one-dimensional array of length 3 |
| `scores[:, np.newaxis]` | `(3, 1)` | Read like a 3-row, 1-column column vector |
| `scores[np.newaxis, :]` | `(1, 3)` | Read like a 1-row, 3-column row vector |

So `np.newaxis` does not create new numbers. It is notation for organizing in which direction an array should fit a calculation.

## `np.newaxis` Is Often Used to Intentionally Create Broadcasting

In P2-11.3, we looked at already compatible shapes such as `(4, 3)` and `(3,)`. But some calculations become easier to read only when one more axis is added on purpose.

Problem situation: We separate the column direction and the row direction so that the difference between two sets can be calculated at once.
Input: The length-3 array `a` and the length-2 array `b`.
Expected output: Shapes `(3, 1)` and `(1, 2)` meet and produce a `(3, 2)` result.
Concept to check: See that `np.newaxis` is a tool for shape alignment used in broadcasting.

```python
# This supplemental example checks NumPy array shape changes together with whether data is shared with the original.
a = np.array([10, 20, 30])
b = np.array([1, 2])

diff = a[:, np.newaxis] - b[np.newaxis, :]

print(a[:, np.newaxis].shape)
print(b[np.newaxis, :].shape)
print(diff)
```

The output is as follows.

```text
(3, 1)
(1, 2)
[[ 9  8]
 [19 18]
 [29 28]]
```

The key point of this example is shape more than value.

- `a[:, np.newaxis]` is `(3, 1)`.
- `b[np.newaxis, :]` is `(1, 2)`.
- Through broadcasting, the two arrays produce a `(3, 2)` result.

Here, understand `np.newaxis` as notation that makes the row and column roles more explicit for broadcasting.

## In Practical Code, Check Shape and Shared Origin Together

NumPy code becomes confusing because `what was selected`, `how the shape changed`, and `whether the original changes too` can all appear together on one line.

For example, the following reading habit is safer.

1. Did this code cut a range, gather positions, or filter by condition?
2. What is the resulting `shape`?
3. Is there any chance the values will be modified later?
4. If the original must be preserved, is `.copy()` needed?

This judgment matters especially in data preprocessing. Whether you created a new dataset from selected samples or directly modified part of an existing array can change how an experiment result should be interpreted.

If you tie this flow together at once, it becomes the following.

```mermaid
--8<-- "assets/part-02/chapter-11/shape-view-broadcast-flow-en.mmd"
```

The minimum sentence the reader should keep here is the following.

- `How it was selected changes shared origin, and how shape was changed changes broadcasting direction.`

## Where Should You Return?

After reading this Section, reconnect it to the following main text.

| Question to read again now | Main text to return to first |
| --- | --- |
| Which value or range was selected? | P2-11.2 Indexing, Slicing, and Axis |
| Why does whole-array calculation change according to shape? | P2-11.3 Broadcasting and Vectorization |
| If the intuition of shared origin itself still feels unfamiliar | P2-8.7 references, shallow copy, deep copy |

## Short Return Table

| When you get stuck | Where to return first |
| --- | --- |
| Indexing, slicing, and axis themselves are still confusing | `P2-11.2` |
| Why the broadcasting direction changes is still vague | `P2-11.3` |
| Why the original and the copied result can change together still feels unfamiliar | `P2-8.7` |

## Checklist

- Can you explain the difference between `x[1:4]` and `x[[1, 3, 4]]`?
- Can you explain what a boolean mask chooses?
- Can you explain the difference among `(3,)`, `(3, 1)`, and `(1, 3)`?
- Can you explain why `np.newaxis` is connected to broadcasting?
- Do you remember that when preserving the original matters, `.copy()` should be checked first?
- Can you explain that when reading NumPy code, you should check `shape` and shared-origin status together rather than only the values?

## Sources and References

- NumPy Developers, [Copies and views](https://numpy.org/doc/stable/user/basics.copies.html){: target="_blank" rel="noopener noreferrer" }, NumPy v2.5 Manual, checked on 2026-07-20. Used as the basis for the difference between views and copies, basic-indexing views, advanced-indexing copies, and `.base` checks.
- NumPy Developers, [Indexing on ndarrays](https://numpy.org/doc/stable/user/basics.indexing.html){: target="_blank" rel="noopener noreferrer" }, NumPy v2.5 Manual, checked on 2026-07-20. Used to confirm that selection method affects shape and whether original data is shared.
- NumPy Developers, [Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html){: target="_blank" rel="noopener noreferrer" }, NumPy v2.5 Manual, checked on 2026-07-20. Used as the basis for connecting `np.newaxis` and shape adjustment to broadcasting.
