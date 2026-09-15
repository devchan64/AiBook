# P2-3.6 Checking Linear Algebra with NumPy

> Section ID: `P2-3.6`
> Version: `v2026.09.14`

NumPy is a Python library for creating and calculating with arrays. We can calculate the vector comparisons from the preceding section and change input and weight shapes to see how the outputs change. An array's `shape` gives the length of each axis.

## Execution Environment

Follow the installation locations explained in [P2-3.5](/AiBook/en/parts/part-02/chapter-03/section-05/#_2). In Colab/Jupyter, enter this command in a code cell.

```text title="IPython · Notebook code cell"
%pip install numpy
```

On a local PC, enter this command in a terminal.

```bash
python -m pip install numpy
```

Run the Python blocks below in order in the same session. Later blocks use variables and `np` defined earlier. To run all the code at once, use the following file.

[p2_3_6_numpy_linear_algebra.py](/AiBook/assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py)

This command runs from the repository root. If you downloaded only the file, run `python p2_3_6_numpy_linear_algebra.py` from the folder where you saved it.

```bash
python docs/assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py
```

## Array Shapes and Outputs

`import numpy as np` imports NumPy under the short name `np`. Passing a list of values to `np.array` creates a one-dimensional array; passing lists of rows creates a two-dimensional array.

```python
import numpy as np

x = np.array([2, 3])
W = np.array([[4, 1], [5, 2]])
print(x.shape)
print(W.shape)
print(x @ W)
```

```text title="Text · Output"
(2,)
(2, 2)
[23  8]
```

The `(2,)` in `x.shape` denotes a one-dimensional array with two components. It differs from a two-dimensional array with one row, such as `(1, 2)`. The `(2, 2)` in `W.shape` means two rows and two columns. `x @ W` multiplies and sums `x` with each column of `W`, producing `[2×4+3×5, 2×1+3×2] = [23, 8]`.

## The Difference Between `*` and `@`

For arrays of the same shape, `+` and `*` operate on corresponding components. Multiplying by a single number multiplies every component by that number. Applying `@` to two one-dimensional vectors sums their component products, giving a single dot-product value.

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(a + b)
print(2 * a)
print(a * b)
print(a @ b)
```

```text title="Text · Output"
[5 7 9]
[2 4 6]
[ 4 10 18]
32
```

`a * b` leaves the products as `[4, 10, 18]`, whereas `a @ b` sums them to `4+10+18=32`. The earlier `x @ W` returns a vector; `a @ b` here returns a single number. The output shape of `@` depends on the dimensions of its inputs. Broadcasting rules also apply to `*` between differently shaped arrays, so element-wise multiplication does not require identical shapes in every case.

## Comparing Purchase Vectors

Use the same `[coffee quantity, tea quantity]` vectors as in P2-3.4. `np.linalg.norm(v)` calculates the 2-norm of this one-dimensional vector. `v-q` is the difference in purchase quantities, and its norm is the Euclidean distance.

```python
q = np.array([1, 1])
candidates = {
    "a": np.array([2, 2]),
    "b": np.array([1, 0]),
    "c": np.array([10, 10]),
}
for name, v in candidates.items():
    dot = q @ v
    norm = np.linalg.norm(v)
    distance = np.linalg.norm(v - q)
    cosine = dot / (np.linalg.norm(q) * norm)
    print(f"{name}: dot={dot}, norm={norm:.3f}, "
          f"distance={distance:.3f}, cosine={cosine:.3f}")
```

```text title="Text · Output"
a: dot=4, norm=2.828, distance=1.414, cosine=1.000
b: dot=1, norm=1.000, distance=1.000, cosine=0.707
c: dot=20, norm=14.142, distance=12.728, cosine=1.000
```

`dot`, `norm`, `distance`, and `cosine` denote the dot product, length, distance, and cosine similarity. The `:.3f` format displays three decimal places without limiting the calculation itself to that precision. By distance, `b` is closest; by cosine similarity, `a` and `c` tie. The dot product is largest for `c`, with its larger quantities. This cosine calculation requires both vectors to have nonzero length.

Change `a` in `candidates` to `[4, 4]` and run it again. The dot product becomes `8`, the norm approximately `5.657`, and the distance approximately `4.243`, but cosine similarity stays at `1.000`. The purchase quantities increased while the ratio stayed the same.

## Samples, Input Components, and Output Components

Group three inputs as rows and transform each input's two components into four output components. The weights below are chosen manually to demonstrate the calculation; they were not learned from data.

```python
X = np.array([
    [2, 3],
    [1, 4],
    [0, 1],
])
W = np.array([
    [4, 1, 1, 0],
    [5, 2, 0, 1],
])
Y = X @ W
print(X.shape, W.shape, Y.shape)
print(Y)
```

```text title="Text · Output"
(3, 2) (2, 4) (3, 4)
[[23  8  2  3]
 [24  9  1  4]
 [ 5  2  0  1]]
```

| Array | Shape | Meaning of rows and columns |
| --- | --- | --- |
| `X` | `(3, 2)` | Three samples, two input components per sample |
| `W` | `(2, 4)` | Weights for two input components and four output components |
| `Y` | `(3, 4)` | Three samples, four output components per sample |

In `(3, 2) @ (2, 4) → (3, 4)`, the two inner dimensions, both `2`, must match. The result retains the sample count `3` and output component count `4`. The first two columns of `W` preserve the earlier `[23, 8]` calculation; the last two pass through the first and second input components, respectively. Applying the same `W` to each sample makes each output row correspond to one input row.

## Dimension Errors and Adding a Weight Row

Multiplying an input with three components by the current two-row `W` raises an error. The following code catches the error and prints the input component count and weight row count. The full error message can differ between NumPy versions.

```python
bad_x = np.array([2, 3, 4])
try:
    bad_x @ W
except ValueError:
    print("ValueError: input components = 3, weight rows = 2")
```

```text title="Text · Output"
ValueError: input components = 3, weight rows = 2
```

Using a third input component requires a corresponding row of weights. Arbitrarily deleting input components just to match shapes changes the meaning of the data. Add `[1, 0, 0, 1]` as a new row so that the third input contributes once to the first and fourth outputs. `np.vstack` stacks arrays vertically, along the row direction.

```python
W_fixed = np.vstack([W, [1, 0, 0, 1]])
print(W_fixed.shape)
print(bad_x @ W_fixed)
```

```text title="Text · Output"
(3, 4)
[27  8  2  7]
```

The third input, `4`, adds `[4, 0, 0, 4]` to the original output `[23, 8, 2, 3]` for `[2, 3]`, giving `[27, 8, 2, 7]`. Matching shapes and deciding the role of the new input must go together.

## Exercise: Adding One More Sample

Add `[2, 0]` as the last row of the batch input `X`, leaving `W` unchanged. Predict the shapes of `X` and `Y` and the new output row before running the calculation.

??? note "Calculation and explanation"
    `X.shape` becomes `(4, 2)` and `Y.shape` becomes `(4, 4)`. The new output row is `[8, 2, 2, 0]`. Each sample still has two input components, so adding samples does not require changing `W`. The first three output rows also remain unchanged.

## Checklist

- Can you explain why `(2,)` and `(1, 2)` are different array shapes?
- Can you explain why applying `*` and `@` to vectors gives an array and a single number, respectively?
- Can you connect the dot product, norm, distance, and cosine calculations to the purchase comparison in the preceding section?
- Can you predict the output shape of `(3, 2) @ (2, 4)` before running it?
- Can you explain how adding samples and adding input components affect the weights differently?

## Sources and References

- NumPy Developers, [NumPy documentation](https://numpy.org/doc/){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-19.
- NumPy Developers, [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-19.
- NumPy Developers, [`numpy.array`](https://numpy.org/doc/stable/reference/generated/numpy.array.html){: target="_blank" rel="noopener noreferrer" }. It provides the array-creation API and examples. Checked: 2026-07-19.
- NumPy Developers, [`numpy.ndarray.shape`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.shape.html){: target="_blank" rel="noopener noreferrer" }. It documents the `shape` attribute as the tuple of array dimensions. Checked: 2026-07-19.
- NumPy Developers, [`numpy.matmul`](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html){: target="_blank" rel="noopener noreferrer" }. It documents matrix multiplication and the shape-mismatch error condition. Checked: 2026-07-19.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, checked 2026-07-19.
- [numpy.linalg.norm](https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html){: target="_blank" rel="noopener noreferrer" }, Accessed: 2026-09-14.
- [cosine_similarity](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html){: target="_blank" rel="noopener noreferrer" }, Accessed: 2026-09-14.
- [Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html){: target="_blank" rel="noopener noreferrer" }, Accessed: 2026-09-14.
