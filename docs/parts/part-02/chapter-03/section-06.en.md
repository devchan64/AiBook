# P2-3.6 Checking Linear Algebra with NumPy

> Section ID: `P2-3.6`
> Version: `v2026.09.08`

NumPy is a Python library for creating and calculating with arrays. An array’s `shape` gives the length of each axis; `*` computes element-wise multiplication and `@` computes matrix multiplication.

## Runtime Environment

The code in this section can run in any Python environment where NumPy is installed.

First check the execution environment according to P2-3.5 [Where Commands Run](section-05.en.md#_2). If Python is not installed yet, you can run the examples in a Google Colab code cell. If you use a local PC, you can run them from your own terminal.

In a Colab code cell, NumPy can be prepared like this.

```python
# This command installs NumPy inside a Colab/Jupyter code cell.
%pip install numpy
```

In a local PC terminal, use the following command.

```bash
python -m pip install numpy
```

Then, inside Python code, import NumPy like this.

```python
# This imports installed NumPy into Python code under the short name np.
import numpy as np
```

Here, `np` is the conventional alias used to call NumPy briefly.

The complete example code of this section can also be downloaded as the following file.

- [p2_3_6_numpy_linear_algebra.py](/AiBook/assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py)

If you run it from the project root, you can use the following command in your personal-PC terminal.

```bash
python docs/assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py
```

This file prints vector addition, scalar multiplication, element-wise multiplication, matrix multiplication, and batch calculation together.

## Creating Vectors and Matrices

A vector can be created as a list of values.

```python
import numpy as np

# x is an input vector with two components.
x = np.array([2, 3])

print(x)

# shape confirms that this vector is a one-dimensional array with two components.
print(x.shape)
```

The output can be read like this.

```text
[2 3]
(2,)
```

`(2,)` means a one-dimensional array with 2 values. In formula form, it corresponds to:

\[
\mathbf{x} = [2,\ 3]
\]

A matrix can be created as a two-dimensional array with rows and columns.

```python
# W is a 2x2 weight matrix that transforms the input vector into another output.
W = np.array([
    [4, 1],
    [5, 2],
])

print(W)

# W's shape is the check point for whether matrix multiplication dimensions match.
print(W.shape)
```

The output can be read like this.

```text
[[4 1]
 [5 2]]
(2, 2)
```

`(2, 2)` means 2 rows and 2 columns.

\[
W =
\begin{bmatrix}
4 & 1 \\
5 & 2
\end{bmatrix}
\]

## Shape and Multiplication Requirements

When an AI calculation does not work in code, it is often necessary to check shape before values.

In `x @ W`, the length of vector `x` must equal the number of rows in matrix `W`.

```python
# x is the input vector, and W is the weight matrix to multiply it by.
x = np.array([2, 3])
W = np.array([
    [4, 1],
    [5, 2],
])

# Reading both shapes side by side helps decide whether x @ W is possible.
print("x shape:", x.shape)
print("W shape:", W.shape)
```

The output is: `x shape: (2,)`, `W shape: (2, 2)`.

This information lets us answer the questions `how many values does x have`, `how many inputs and outputs does W connect`, and `do these two have shapes that can be multiplied`.

`x` is a vector with 2 input values, and `W` is a weight matrix that receives 2 inputs and makes 2 outputs.

## Vector Addition and Scalar Multiplication

Vector addition adds values at the same positions.

```python
# a and b are two vectors with the same shape.
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# This checks that components in the same positions are added.
print(a + b)
```

The output is:

```text
[5 7 9]
```

In formula form:

\[
[1,\ 2,\ 3] + [4,\ 5,\ 6] = [5,\ 7,\ 9]
\]

Scalar multiplication multiplies the same number into each value of the array.

```python
# This multiplies every component of the earlier vector a by the same scalar 2.
print(2 * a)
```

The output is:

```text
[2 4 6]
```

In formula form:

\[
2[1,\ 2,\ 3] = [2,\ 4,\ 6]
\]

## `*`: Element-Wise Multiplication

In NumPy, using `*` between arrays usually becomes element-wise multiplication.

```python
# a and b are the two vectors used to compare element-wise multiplication.
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# * multiplies components in the same positions.
print(a * b)
```

The output is:

```text
[ 4 10 18]
```

In formula form:

\[
[1,\ 2,\ 3] \odot [4,\ 5,\ 6] = [4,\ 10,\ 18]
\]

The important point here is that `*` is not matrix multiplication. It is the calculation that multiplies matching positions. In short, `*` is element-wise multiplication and `@` is matrix multiplication.

## `@`: Matrix Multiplication

In NumPy, `@` is used for matrix multiplication.

```python
# x is the input vector, and W is the weight matrix that creates output components.
x = np.array([2, 3])
W = np.array([
    [4, 1],
    [5, 2],
])

# y is the output vector produced by matrix multiplication between x and W.
y = x @ W

print(y)
print(y.shape)
```

The output is:

```text
[23  8]
(2,)
```

This calculation is the same weighted-sum structure seen in `P2-3.3`.

\[
[2,\ 3]
\begin{bmatrix}
4 & 1 \\
5 & 2
\end{bmatrix}
=
[23,\ 8]
\]

The first output is:

\[
2 \times 4 + 3 \times 5 = 23
\]

The second output is:

\[
2 \times 1 + 3 \times 2 = 8
\]

So `@` is `a calculation that multiplies and adds to make a new vector`.

## Batch Matrix Calculation

If several input samples are grouped into a matrix, the same weight matrix can be applied all at once.

```python
# X is an input matrix with two samples as rows.
X = np.array([
    [2, 3],
    [1, 4],
])

# W is the weight matrix that turns each input sample into an output vector.
W = np.array([
    [4, 1],
    [5, 2],
])

# Y is the output matrix after applying W to the whole input batch X.
Y = X @ W

print(X.shape)
print(W.shape)
print(Y)
print(Y.shape)
```

The output is:

```text
(2, 2)
(2, 2)
[[23  8]
 [24  9]]
(2, 2)
```

In formula form:

\[
X =
\begin{bmatrix}
2 & 3 \\
1 & 4
\end{bmatrix}
\]

\[
W =
\begin{bmatrix}
4 & 1 \\
5 & 2
\end{bmatrix}
\]

\[
XW =
\begin{bmatrix}
23 & 8 \\
24 & 9
\end{bmatrix}
\]

Here, the first row is the output of the first sample, and the second row is the output of the second sample. In other words, there are 2 input samples, each sample has 2 values, the same `W` is applied, and then we obtain 2 output samples, each of which also has 2 values.

This is the smallest example of batch calculation.

## Mismatched Input Length

The following calculation does not match immediately.

```python
# bad_x has three components, so its dimension does not match the two-row W.
bad_x = np.array([2, 3, 4])
W = np.array([
    [4, 1],
    [5, 2],
])

bad_y = bad_x @ W
```

The shape of `bad_x` is `(3,)`, and the shape of `W` is `(2, 2)`. The input has 3 values, but the weight matrix is shaped to receive 2 input values. In other words: `bad_x shape: (3,)`, `W shape: (2, 2)`.

So it does not align which input values should be multiplied with which weights. In a real NumPy run, an error appears saying that the shapes do not match.

To use the third input in the calculation, `W` needs a corresponding row of weights. To retain two outputs, `W` must have shape `(3, 2)`. Deleting an input arbitrarily just to match shapes changes the meaning of the data supplied to the model.

## Checklist

- Can you create vectors and matrices as NumPy arrays?
- Can you check vector and matrix shape with `.shape`?
- Can you connect vector addition and scalar multiplication in code and in formulas?
- Can you explain that NumPy’s `*` is element-wise multiplication?
- Can you explain that NumPy’s `@` is matrix multiplication?
- Can you read input shape, weight shape, and output shape in `x @ W`?
- Can you explain batch calculation that groups several samples into a matrix and applies the same weight matrix?
- Can you explain the habit of checking formula, shape, and output together in NumPy rather than looking at syntax alone?
- Can you distinguish `*` and `@` and apply the standard of checking shape before values?

## Sources and References

- Example code of this section: [p2_3_6_numpy_linear_algebra.py](/AiBook/assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py)
- NumPy Developers, [NumPy documentation](https://numpy.org/doc/){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-19.
- NumPy Developers, [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-19.
- NumPy Developers, [`numpy.array`](https://numpy.org/doc/stable/reference/generated/numpy.array.html){: target="_blank" rel="noopener noreferrer" }. It provides the array-creation API and examples. Checked: 2026-07-19.
- NumPy Developers, [`numpy.ndarray.shape`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.shape.html){: target="_blank" rel="noopener noreferrer" }. It documents the `shape` attribute as the tuple of array dimensions. Checked: 2026-07-19.
- NumPy Developers, [`numpy.matmul`](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html){: target="_blank" rel="noopener noreferrer" }. It documents matrix multiplication and the shape-mismatch error condition. Checked: 2026-07-19.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, checked 2026-07-19.
