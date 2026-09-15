# P2-11.1 Building Vectors and Matrices with NumPy Arrays

> Section ID: `P2-11.1`
> Version: `v2026.09.15`

## List Concatenation and Array Addition

NumPy provides multidimensional `ndarray` objects and array operations for Python. Lists and arrays can store the same numbers while following different operation rules.

Prepare `[82, 75, 45]` as a Python list and a NumPy array. These assignments store values without displaying output.

```python
import numpy as np

python_scores = [82, 75, 45]
numpy_scores = np.array([82, 75, 45])
```

Applying the same operation reveals the difference.

Add each collection to itself. The list concatenates into six items; the array adds matching positions to produce `[164 150 90]`.

```python
print(python_scores + python_scores)
print(numpy_scores + numpy_scores)
```

For lists, `+` joins the two sequences.

```text
[82, 75, 45, 82, 75, 45]
```

For NumPy arrays, `+` adds numbers at matching positions.

```text
[164 150  90]
```

| Structure | Main purpose | Typical meaning of `+` |
| --- | --- | --- |
| Python list | General container for ordered values | Concatenation |
| NumPy array | Computation over shaped collections | Element-wise addition |

A NumPy array organizes both data storage and calculation.

This diagram compares the meaning of `+` for a list and a NumPy array.

```mermaid
--8<-- "assets/part-02/chapter-11/list-vs-numpy-array-en.mmd"
```

This distinction matters in AI code: storing a collection and applying one calculation across it are different tasks.

## Building a Vector

A vector can be viewed as numbers arranged in one line.

Create a one-dimensional array of four floating-point values. The output includes its values, shape `(4,)`, dimension count `1`, and dtype `float64`.

```python
import numpy as np

embedding = np.array([0.12, -0.03, 0.44, 0.18])

print(embedding)
print(embedding.shape)
print(embedding.ndim)
print(embedding.dtype)
```

Expected output:

```text
[ 0.12 -0.03  0.44  0.18]
(4,)
1
float64
```

These attributes mean:

| Attribute | Meaning | In this example |
| --- | --- | --- |
| `shape` | Array shape | One-dimensional array with four values |
| `ndim` | Number of dimensions | One dimension |
| `dtype` | Stored element type | Floating-point numbers |

Mathematically, it corresponds to this vector:

\[
\mathbf{x} = [0.12,\ -0.03,\ 0.44,\ 0.18]
\]

The comma in `(4,)` denotes a one-item tuple. There is one axis, containing four values.

## Building a Matrix

A matrix can be viewed as a two-dimensional array with rows and columns.

Store two students' scores in three subjects as a two-dimensional array. The output shows values, shape `(2, 3)`, dimension count `2`, and an integer type. Explicit `dtype=np.int64` makes the type `int64`.

```python
scores = np.array([
    [82, 75, 45],
    [90, 61, 70],
], dtype=np.int64)

print(scores)
print(scores.shape)
print(scores.ndim)
print(scores.dtype)
```

Expected output:

```text
[[82 75 45]
 [90 61 70]]
(2, 3)
2
int64
```

`(2, 3)` means two rows and three columns.

\[
S =
\begin{bmatrix}
82 & 75 & 45 \\
90 & 61 & 70
\end{bmatrix}
\]

The shape does not define what the axes mean; you must assign those meanings.

For example, interpret the matrix as follows:

| Axis | Interpretation |
| --- | --- |
| Rows | Students or samples |
| Columns | Subjects or features |

AI examples often put samples in rows and features in columns, but this is not universal. Check `shape` and record each axis's meaning when creating an array.

## dtype and Fractional Values

An array's `dtype` determines how each element is stored. Assigning a fractional value to an integer array does not automatically turn the whole array into floating point.

```python
integer_scores = np.array([82, 75, 45], dtype=np.int64)
float_scores = integer_scores.astype(np.float64)
integer_scores[1] = 75.5
float_scores[1] = 75.5

print(integer_scores.tolist())
print(float_scores.tolist())
```

The outputs are `[82, 75, 45]` and `[82.0, 75.5, 45.0]`. Assigning 75.5 to the integer array loses the fraction; converting to floating point first preserves it. Converting an already stored 75 to floating point cannot recover the lost 0.5. Decide whether fractions are needed when creating the array.

## Matrix Multiplication Shapes

`shape` is part of the grammar of NumPy calculation: it determines which operations are possible.

There are three samples with two features each. The feature matrix and weight vector have shapes `(3, 2)` and `(2,)`.

```python
features = np.array([
    [1.0, 0.2],
    [0.8, 0.4],
    [0.3, 0.9],
])

weights = np.array([0.6, 0.4])

print(features.shape)
print(weights.shape)
```

Output:

```text
(3, 2)
(2,)
```

Read these shapes as follows:

| Array | Shape | Meaning |
| --- | --- | --- |
| `features` | `(3, 2)` | Three samples, two features |
| `weights` | `(2,)` | Weights for two features |

The matrix multiplication operator `@` computes one score per sample.

Multiplying `features` by `weights` gives `[0.68 0.64 0.54]` with output shape `(3,)`.

```python
scores = features @ weights
print(scores)
print(scores.shape)
```

The output is approximately:

```text
[0.68 0.64 0.54]
(3,)
```

Each sample's two features are weighted and combined into one score.

\[
\begin{bmatrix}
1.0 & 0.2 \\
0.8 & 0.4 \\
0.3 & 0.9
\end{bmatrix}
\begin{bmatrix}
0.6 \\
0.4
\end{bmatrix}
=
\begin{bmatrix}
0.68 \\
0.64 \\
0.54
\end{bmatrix}
\]

The first score is 1.0 × 0.6 + 0.2 × 0.4 = 0.68. The column count in `features` and length of `weights` must both be 2 to pair each feature with a weight.

The diagram summarizes this calculation through its shapes.

```mermaid
--8<-- "assets/part-02/chapter-11/feature-weight-shape-flow-en.mmd"
```

`features` has three samples and two features. `weights` supplies one weight for each feature. Their matching inner size of 2 produces one score per sample.

## Element-Wise and Matrix Products

`features * weights` retains each weighted feature; `features @ weights` sums those products within each sample. Their result shapes differ even with the same inputs.

```python
weighted = features * weights
print(weighted)
print(weighted.sum(axis=1))
```

```text
[[0.6  0.08]
 [0.48 0.16]
 [0.18 0.36]]
[0.68 0.64 0.54]
```

The element-wise product has shape `(3, 2)`; summing the feature axis gives `(3,)`. Here `weighted.sum(axis=1)` computes the same weighted sums as `features @ weights`. The `*` operation alone does not sum the products into sample scores.

## Inspecting Array Attributes

Check three attributes when creating a NumPy array.

For the feature matrix, `shape`, `ndim`, and `dtype` are `(3, 2)`, `2`, and `float64`.

```python
print(features.shape)
print(features.ndim)
print(features.dtype)
```

Each attribute answers a different question:

| Attribute | Question | Why it matters |
| --- | --- | --- |
| `shape` | What is the shape? | Check operation compatibility |
| `ndim` | How many dimensions? | Distinguish vectors, matrices, and higher dimensions |
| `dtype` | What is the type? | Avoid confusing integers, floats, and strings |

When an array operation fails, checking shapes is often more useful than inspecting every value. A shape mismatch can prevent calculation regardless of the values' magnitudes.

## Example Code File

The examples are also available in this file:

- [p2_11_1_numpy_arrays.py](/AiBook/assets/part-02/chapter-11/p2_11_1_numpy_arrays.py)

In Colab, paste the code into a cell. Locally, run this command from the project root:

```bash
python docs/assets/part-02/chapter-11/p2_11_1_numpy_arrays.py
```

The script prints `shape`, `ndim`, and `dtype` for vectors, matrices, features, and weights, and demonstrates a small weighted sum.

It also compares Python list `+` with NumPy array `+`, showing how the same symbol changes meaning with the data structure.

## Case: Reordering Weights

The first and second feature columns initially use weights 0.6 and 0.4. Changing them to `[0.4, 0.6]` produces `[0.52, 0.56, 0.66]`. The third sample now ranks highest instead of the first.

The shapes remain `(3, 2) @ (2,)`, so calculation succeeds. Shape alone cannot verify the semantic pairing of columns and weights. Changing the weights to `[0.6, 0.3, 0.1]` instead gives length 3 and raises `ValueError` during multiplication.

| Change | Result | What to check |
| --- | --- | --- |
| Weights `[0.6, 0.4]` | `[0.68, 0.64, 0.54]` | Feature–weight correspondence |
| Weights `[0.4, 0.6]` | `[0.52, 0.56, 0.66]` | Same shapes can produce different scores and rankings |
| Weights `[0.6, 0.3, 0.1]` | Shape mismatch error | Different feature and weight counts |

## Checklist

- Explain how Python lists and NumPy arrays differ in purpose.
- Create vectors and matrices with `np.array()`.
- Explain `.shape`, `.ndim`, and `.dtype`.
- Distinguish one- and two-dimensional arrays.
- Read matrices organized as `(samples, features)`.
- Explain input and output shapes for `features @ weights`.
- Explain NumPy arrays as numbers organized into shapes for calculation.
- Can you explain fractional loss on assignment to an integer array and the difference between `*` and `@`?

## Sources and References

- NumPy Developers, [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, checked on 2026-07-20. Used to confirm homogeneous N-dimensional `ndarray`, shape, dtype, and differences from Python lists.
- NumPy Developers, [The N-dimensional array](https://numpy.org/doc/stable/reference/arrays.ndarray.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, checked on 2026-07-20. Used as the basis for `ndarray` attributes and array-object structure in vector and matrix examples.
- NumPy Developers, [Array creation](https://numpy.org/doc/stable/user/basics.creation.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, checked on 2026-07-20. Used to confirm basic array creation methods such as `np.array`, `zeros`, `ones`, `arange`, and `linspace`.
- NumPy Developers, [numpy.ndarray.astype](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.astype.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, accessed: 2026-09-15. dtype conversion and copying.
- NumPy Developers, [numpy.matmul](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, accessed: 2026-09-15. matrix–vector dimensions and the distinction from elementwise multiplication.
