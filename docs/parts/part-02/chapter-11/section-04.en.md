# P2-11.4 Supplemental: Shape and Shared Data in NumPy

> Section ID: `P2-11.4`
> Version: `v2026.09.15`

## Slices and Shared Data

Basic slicing creates a view sharing the original array's data. Setting the first value of `scores[1:4]` to 999 also changes position 1 in the original to 999.

```python
import numpy as np

scores = np.array([82, 75, 45, 90, 61])
middle = scores[1:4]

middle[0] = 999

print(scores)
print(middle)
```

Output:

```text
[ 82 999  45  90  61]
[999  45  90]
```

## Position and Condition Selection as Copies

Fancy indexing with a position list and boolean indexing with a mask copy data when retrieving values. Changing the first value of `picked` to 500 and `high_scores` to 700 leaves the original `[82, 75, 45, 90, 61]` unchanged.

```python
scores = np.array([82, 75, 45, 90, 61])

picked = scores[[1, 3, 4]]
high_scores = scores[scores >= 80]

picked[0] = 500
high_scores[0] = 700

print(scores)
print(picked)
print(high_scores)
```

Output:

```text
[82 75 45 90 61]
[500  90  61]
[700  90]
```

`scores[[1, 3, 4]]` gathers values at positions 1, 3, and 4. This is fancy indexing.

`scores[scores >= 80]` selects values where the condition is true, using a boolean mask.

## Adding an Axis of Length One

`np.newaxis` adds a length-one axis at the specified position. A `(3,)` score array can be viewed as `(3, 1)` or `(1, 3)`. These results also share data with the original.

```python
scores = np.array([82, 75, 45])

print(scores.shape)
print(scores[:, np.newaxis].shape)
print(scores[np.newaxis, :].shape)
```

Output:

```text
(3,)
(3, 1)
(1, 3)
```

The values remain the same, but dimensionality and shape differ.

| Expression | Shape | Reading |
| --- | --- | --- |
| `scores` | `(3,)` | One-dimensional array of length three |
| `scores[:, np.newaxis]` | `(3, 1)` | Three-row, one-column vector-like view |
| `scores[np.newaxis, :]` | `(1, 3)` | One-row, three-column vector-like view |

`np.newaxis` does not create new numbers; it organizes how the array aligns in a calculation.

## Differences for Every Pair

Subtracting both 1 and 2 from each of `[10, 20, 30]` requires a three-by-two result. Changing the input shapes to `(3, 1)` and `(1, 2)` allows broadcasting over all six pairs.

```python
a = np.array([10, 20, 30])
b = np.array([1, 2])

diff = a[:, np.newaxis] - b[np.newaxis, :]

print(a[:, np.newaxis].shape)
print(b[np.newaxis, :].shape)
print(diff)
```

Output:

```text
(3, 1)
(1, 2)
[[ 9  8]
 [19 18]
 [29 28]]
```

The first row `[9, 8]` subtracts 1 and 2 from 10; the last row `[29, 28]` subtracts them from 30. Changing `b` to `[1, 5]` changes only the second column to `[5, 15, 25]`. Without the added axes, `a - b` fails because `(3,)` and `(2,)` are incompatible.

## Reshape and Transpose

`reshape` groups elements into a new shape; `.T` swaps the row and column axes of a two-dimensional array. Both can produce `(3, 2)` while arranging values differently.

```python
matrix = np.array([[10, 11, 12], [20, 21, 22]])
print(matrix.reshape(3, 2))
print(matrix.T)
```

```text
[[10 11]
 [12 20]
 [21 22]]
[[10 20]
 [11 21]
 [12 22]]
```

If original rows represent students, columns represent students after transposition. `reshape(3, 2)` does not preserve that meaning automatically. A one-dimensional `(3,)` array still has shape `(3,)` after `.T`. Use `[:, np.newaxis]` to create a column-vector shape.

`reshape` returns a view when possible, but memory layout can require a copy. This small example checks actual data sharing.

```python
matrix = np.array([[10, 11, 12], [20, 21, 22]])
reshaped = matrix.reshape(3, 2)
transposed_flat = matrix.T.reshape(-1)

print(np.shares_memory(matrix, reshaped))
print(np.shares_memory(matrix, transposed_flat))
```

Outputs are `True` and `False`. A `-1` dimension asks NumPy to infer that length from the element count. Flattening this transposed array in the default order requires copying. Do not assume every reshape is a view or every reshape a copy. Use `.copy()` explicitly when editing must preserve the original.

## Case: Adjusting Only Selected Scores

Select positions 1 through 3 from `[82, 75, 45, 90, 61]` and add 10. Editing a slice directly also changes the original. Copy the selection with `.copy()` to compare original and adjusted values independently.

```python
scores = np.array([82, 75, 45, 90, 61])
adjusted = scores[1:4].copy()
adjusted += 10

print(scores)
print(adjusted)
```

```text
[82 75 45 90 61]
[ 85  55 100]
```

Remove `.copy()` and rerun the whole example: the original becomes `[82, 85, 55, 100, 61]`. If the intended “before” data changes too, a before-and-after comparison no longer uses the original baseline.

Condition selection produces a copy when **reading into a new variable**. Direct assignment such as `scores[scores < 60] = 60` changes those positions in the original. Reading `low = scores[scores < 60]` and then assigning `low[:] = 60` leaves the original unchanged.

```mermaid
--8<-- "assets/part-02/chapter-11/shape-view-broadcast-flow-en.mmd"
```

## Example Code File

Run the examples in order to compare changes to the original array and its shape.

- [p2_11_4_views_shapes.py](/AiBook/assets/part-02/chapter-11/p2_11_4_views_shapes.py)

```bash
python docs/assets/part-02/chapter-11/p2_11_4_views_shapes.py
```

## Checklist

- Can you distinguish `x[1:4]` from `x[[1, 3, 4]]`?
- Can you explain what a boolean mask selects?
- Can you distinguish `(3,)`, `(3, 1)`, and `(1, 3)`?
- Can you explain how `np.newaxis` supports broadcasting?
- Do you check whether a copy is needed to preserve original data?
- Can you inspect both shape and data sharing when reading NumPy code?
- Can you distinguish reshape from transpose and check shared storage with `np.shares_memory`?

## Sources and References

- NumPy Developers, [Copies and views](https://numpy.org/doc/stable/user/basics.copies.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, checked on 2026-07-20. Used as the basis for the difference between views and copies, basic-indexing views, advanced-indexing copies, and `.base` checks.
- NumPy Developers, [Indexing on ndarrays](https://numpy.org/doc/stable/user/basics.indexing.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, checked on 2026-07-20. Used to confirm that selection method affects shape and whether original data is shared.
- NumPy Developers, [Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, checked on 2026-07-20. Used as the basis for connecting `np.newaxis` and shape adjustment to broadcasting.
- NumPy Developers, [numpy.shares_memory](https://numpy.org/doc/stable/reference/generated/numpy.shares_memory.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, accessed: 2026-09-15. shared-memory checks for the small array examples.
