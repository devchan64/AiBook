# P2-11.3 Broadcasting and Vectorization

> Section ID: `P2-11.3`
> Version: `v2026.09.15`

## Scalars and Arrays

NumPy describes broadcasting as the rules for arithmetic on arrays with different shapes. A smaller array is treated as having a shape compatible with the larger one for the calculation.

Broadcasting applies a common calculation rule across arrays of different shapes.

Add 10 to or multiply by 2 each score in `[82, 75, 45]`. The results are `[92, 85, 55]` and `[164, 150, 90]`.

```python
import numpy as np

scores = np.array([82, 75, 45])

print(scores + 10)
print(scores * 2)
```

Output:

```text
[92 85 55]
[164 150  90]
```

`10` and `2` are scalars. NumPy applies each scalar at every array position.

The diagram shows a scalar applied across an array. This is a calculation rule, not a requirement to physically copy the scalar many times.

```mermaid
--8<-- "assets/part-02/chapter-11/broadcast-scalar-array-en.mmd"
```

## Adding Feature Offsets

Broadcasting cannot force arbitrary arrays to fit. Their shapes must be compatible.

Put four samples with three features each into a matrix and add `[0.1, 0.2, 0.3]` by feature. The first sample changes from `[1.0, 0.2, 7.0]` to `[1.1, 0.4, 7.3]`.

```python
features = np.array([
    [1.0, 0.2, 7.0],
    [0.8, 0.4, 6.5],
    [0.3, 0.9, 8.1],
    [0.5, 0.1, 5.8],
])

feature_offset = np.array([0.1, 0.2, 0.3])

print(features.shape)
print(feature_offset.shape)
print(features + feature_offset)
```

Output:

```text
(4, 3)
(3,)
[[1.1 0.4 7.3]
 [0.9 0.6 6.8]
 [0.4 1.1 8.4]
 [0.6 0.3 6.1]]
```

Here rows are samples and columns are features, so `(4, 3)` means four samples and three features.

`feature_offset` has shape `(3,)`: one value to add to each feature.

NumPy applies the `(3,)` array to each row, adding the same three offsets to every sample.

The diagram shows a `(3,)` vector applied row by row to a `(4, 3)` matrix.

```mermaid
--8<-- "assets/part-02/chapter-11/broadcast-row-vector-en.mmd"
```

## Shape Compatibility

Adding a length-four vector to this matrix raises `ValueError`. Four rows do not help: the trailing dimension has three columns.

```python
bad_offset = np.array([10, 20, 30, 40])

print(features.shape)
print(bad_offset.shape)
print(features + bad_offset)
```

This code raises an error:

```text
ValueError: operands could not be broadcast together with shapes (4,3) (4,)
```

`features` has shape `(4, 3)` with three features per row. `bad_offset` has shape `(4,)`. Its length matches the row count, but not the three columns within each row.

| Calculation | Reading | Result |
| --- | --- | --- |
| `(4, 3) + scalar` | Apply one value everywhere | Valid |
| `(4, 3) + (3,)` | Apply a length-three vector to every row | Valid |
| `(4, 3) + (4,)` | Length four does not match three columns | Error |

Broadcasting compares dimensions from the end. Corresponding sizes must be equal or one must be 1; absent leading dimensions count as 1. `(4, 3)` and `(3,)` match at the end, while `(4, 3)` and `(4,)` conflict at sizes 3 and 4.

## Loops and Array Operations

Vectorization expresses calculation through array operations instead of explicit loops in the code.

For example, a Python loop can add 10 to every score:

```python
scores = [82, 75, 45]

adjusted = []
for score in scores:
    adjusted.append(score + 10)

print(adjusted)
```

The loop prints `[92, 85, 55]`. With a NumPy array, `scores + 10` calculates the same three values.

```python
scores = np.array([82, 75, 45])
adjusted = scores + 10

print(adjusted)
```

Both add 10 per score; their expressions differ.

| Method | Visible code structure | Interpretation |
| --- | --- | --- |
| Python loop | Retrieve and process values individually | Write the procedure explicitly |
| NumPy vectorization | Apply an operation to the array | Express the calculation at array level |

NumPy's documentation explains that broadcasting supports vectorization with looping at the C level instead of Python. Vectorization does not mean that repetition disappears.

This diagram compares the loop and array expressions for the same calculation.

```mermaid
--8<-- "assets/part-02/chapter-11/loop-to-vectorization-flow-en.mmd"
```

## Subtracting Feature Means

Subtracting each feature's mean is common in AI data processing. It is a starting point for centering features near zero.

The four samples have column means `[0.65, 0.4, 6.85]`. Subtracting them from each row makes the first row `[0.35, -0.2, 0.15]`.

```python
features = np.array([
    [1.0, 0.2, 7.0],
    [0.8, 0.4, 6.5],
    [0.3, 0.9, 8.1],
    [0.5, 0.1, 5.8],
])

column_mean = features.mean(axis=0)
centered = features - column_mean

print(column_mean)
print(centered)
```

The output is approximately:

```text
[0.65 0.4  6.85]
[[ 0.35 -0.2   0.15]
 [ 0.15  0.   -0.35]
 [-0.35  0.5   1.25]
 [-0.15 -0.3  -1.05]]
```

`features.mean(axis=0)` computes one mean per column, with shape `(3,)`. The original `features` has shape `(4, 3)`.

`features - column_mean` subtracts `(3,)` from `(4, 3)`, applying the mean vector to every row.

| Code | Shape | Meaning |
| --- | --- | --- |
| `features` | `(4, 3)` | Four samples, three features |
| `features.mean(axis=0)` | `(3,)` | Feature means |
| `features - column_mean` | `(4, 3)` | Feature means subtracted from every sample |

The centered column means are zero within floating-point error. Switching to `axis=1` produces four row means of shape `(4,)`, making this subtraction fail.

## Row Means and keepdims

To subtract each student's mean from that student's subjects, retain row means as `(students, 1)`. `keepdims=True` keeps reduced axes with length 1 rather than removing them.

```python
marks = np.array([[80, 70, 90], [60, 90, 75]])
row_mean = marks.mean(axis=1, keepdims=True)
row_centered = marks - row_mean

print(row_mean.shape)
print(row_centered)
print(row_centered.mean(axis=1))
```

```text
(2, 1)
[[  0. -10.  10.]
 [-15.  15.   0.]]
[0. 0.]
```

Without `keepdims`, means have shape `(2,)` and cannot be subtracted directly from `(2, 3)`. For a three-by-three square array, subtracting `(3,)` may succeed but aligns those values with columns, not rows. Successful execution does not establish the intended axis semantics. For row centering, also check that resulting row means are near zero.

## Intermediate Arrays and Memory

Broadcasting can avoid repeating input data, but result arrays still need memory. Adding `(10000, 1)` and `(1, 10000)` produces `(10000, 10000)`. Its 100 million `float64` elements alone require about 800 MB. Check the output shape as well as input sizes.

## Example Code File

The examples are also available here:

- [p2_11_3_broadcast_vectorization.py](/AiBook/assets/part-02/chapter-11/p2_11_3_broadcast_vectorization.py)

Locally, run from the project root:

```bash
python docs/assets/part-02/chapter-11/p2_11_3_broadcast_vectorization.py
```

In Colab, paste the file into a code cell.

Outputs cover scalar broadcasting, row-vector broadcasting, a shape mismatch, and subtraction of feature means.

## Case: Subject and Student Adjustments

Two students score `[80, 70, 90]` and `[60, 90, 75]` in Korean, mathematics, and English. To add 5, 10, and 0 by subject, use a length-three vector. Results are `[85, 80, 90]` and `[65, 100, 75]`.

```python
marks = np.array([[80, 70, 90], [60, 90, 75]])
subject_bonus = np.array([5, 10, 0])
student_bonus = np.array([[5], [10]])

print(marks + subject_bonus)
print(marks + student_bonus)
```

```text
[[ 85  80  90]
 [ 65 100  75]]
[[ 85  75  95]
 [ 70 100  85]]
```

To add 5 to the first student's subjects and 10 to the second student's, use shape `(2, 1)`. Each row's adjustment applies to all three subjects. Writing `[5, 10]` instead gives `(2,)`, incompatible with the trailing dimension 3.

Changing the second `subject_bonus` from 10 to 0 restores only mathematics scores to 70 and 90 in the first output. Changing the second `student_bonus` to 0 restores every score of the second student in the second output. Placement determines what the addition affects.

## Checklist

- Explain scalar–array arithmetic through broadcasting.
- Explain why `(4, 3) + (3,)` works.
- Explain why `(4, 3) + (4,)` fails.
- Distinguish Python loops from NumPy vectorized expressions.
- Explain the shape of `features.mean(axis=0)`.
- Identify broadcasting when subtracting feature means.
- Explain why broadcasting requires attention to shapes and memory.
- Can you explain why row centering uses `keepdims=True` and how to check the result?

## Sources and References

- NumPy Developers, [Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, checked on 2026-07-20. Used as the core basis for broadcasting rules, dimension comparison, and shape mismatch errors.
- NumPy Developers, [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, checked on 2026-07-20. Used to confirm array arithmetic, universal functions, and basic axis-calculation examples.
- NumPy Developers, [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, checked on 2026-07-20. Used as the basis for the beginner-level flow of reading array-level computation instead of Python loops and checking shape first.
- NumPy Developers, [numpy.mean](https://numpy.org/doc/stable/reference/generated/numpy.mean.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, accessed: 2026-09-15. axis reduction and axis preservation with keepdims.
