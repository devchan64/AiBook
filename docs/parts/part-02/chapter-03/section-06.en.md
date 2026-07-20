# P2-3.6 Checking Linear Algebra with NumPy

> Section ID: `P2-3.6`
> Version: `v2026.07.20`

In P2-3.1, we looked at the shapes of scalar, vector, and matrix. In P2-3.2, we looked at the intuition of vector space and position. In P2-3.3, we read matrix multiplication as the reuse of weighted sums. In P2-3.5, we separated Python runtime environments into Google Colab and a local PC.

Now we check the same content with small pieces of code. Here we use NumPy. NumPy is the representative library in Python for creating arrays and calculating with them.

1. Look at it as a formula.
2. Build it as an array.
3. Check the `shape`.
4. Check the calculation result.

Here we focus less on memorizing lots of NumPy syntax and more on checking what the linear algebra notation looks like when it appears in code.

Here we reorganize `NumPy`, `array`, `shape`, `element-wise multiplication`, and `matrix multiplication`. If 3.1 was about reading data shape and 3.3 was about reading the structure of matrix multiplication, now this section organizes how that calculation looks in code and printed output.

Rather than learning all of NumPy, we focus on rechecking in code and shape the linear-algebra structure already seen in formulas. If we confirm vectors, matrices, `*`, `@`, and batch calculation through real output, then later, when reading Pandas data and model-input arrays, it becomes easier to see that formulas and code share the same structure.

From the reader’s point of view, it is easy to feel `the code runs, but which earlier concept is this section actually confirming?` So in this section, we read each example together with whether it is checking the shape from `P2-3.1`, the vector comparison idea from `P2-3.2`, or the matrix multiplication structure from `P2-3.3`.

| What to fix in this section now | Question that follows immediately | Where it reappears later |
| --- | --- | --- |
| The intuition that formulas and NumPy arrays correspond | In later chapters, we examine how table data and model-input arrays connect. | It returns when reading `X`, `y`, and train/test split results by shape in Part 3. |
| The habit of separating `*` and `@` together with shape | In `P2-12.1`, `P2-12.3`, and `P2-13.1`, we also check output shape in data-processing and visualization practice. | It reappears when reading linear layers in Part 4 and embedding/logit calculations in Part 5. |
| The view that batch calculation is read at matrix level | It continues into rate-of-change and probability explanations in `P2-4.1` and `P2-5.1`, and then into later array-transformation flows. | It becomes a foundation when following machine-learning input matrices and mini-batch explanations. |

## A Concept Mapping Table to See First

The examples in this section recheck the ideas of earlier sections in the following way.

| Code scene | Earlier concept being rechecked | What the reader should inspect first |
| --- | --- | --- |
| Creating vectors and checking `shape` | scalar/vector/matrix shape from `P2-3.1` | Do you see the shape before the values? |
| Comparing vectors `a`, `b` | position and nearness intuition from `P2-3.2` | Are the vectors of the same length? |
| `a + b`, `2 * a` | minimum operations of vector space from `P2-3.2` | How do addition and scalar multiplication look in code? |
| Distinguishing `*` and `@` | matrix multiplication and weighted sum from `P2-3.3` | Is it a same-position calculation, or a multiply-and-add calculation? |
| Batch matrix calculation | the view of processing several vectors at once from `P2-3.3` | How does the shape change from input matrix to output matrix? |

If we hold this table first, each code block becomes clearer as `a place that rechecks an earlier idea`, rather than a mere syntax example.

## Core Criteria: Checking Linear Algebra with NumPy

- You can create vectors and matrices as NumPy arrays.
- You can check data shape with `.shape`.
- You can verify vector addition and scalar multiplication in code.
- You can explain the difference between `*` and `@`.
- You can read the calculation that groups several samples into a matrix and applies the same weight matrix.
- You can build the habit of reading formulas, shape, and code results together.

## Three Criteria

| Criterion | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| NumPy carries the array structure of formulas into code | Because only by creating and printing vectors and matrices directly can we verify the difference between shape and operations. | Understand NumPy as a tool for array calculation. |
| Look at shape before values | Because it is the fastest way to check calculation possibility and input/output structure. | Understand that `.shape` is read first to inspect length, row count, and column count. |
| Distinguish `*` from `@` | Because if element-wise multiplication and matrix multiplication are confused, the reading of formulas and code goes wrong together. | Understand `*` as element-wise calculation and `@` as matrix multiplication. |

## Runtime Environment

The code in this section can run in any Python environment where NumPy is installed.

First check the execution environment according to P2-3.5 [First Separate the Runtime Environment](section-05.md#first-separate-the-runtime-environment). If Python is not installed yet, you can run the examples in a Google Colab code cell. If you use a local PC, you can run them from your own terminal.

In a Colab code cell, NumPy can be prepared like this.

Problem situation: Before running the NumPy examples in Colab, prepare the package.
Input: The `%pip install numpy` command in a notebook code cell.
Expected output: NumPy is installed into the current Colab kernel.
Concept to check: Installation commands in a Colab code cell and execution of Python code are different stages.

```python
# This command installs NumPy inside a Colab/Jupyter code cell.
%pip install numpy
```

In a local PC terminal, use the following command.

```bash
python -m pip install numpy
```

Then, inside Python code, import NumPy like this.

Problem situation: After preparing the package, actually import NumPy inside Python code.
Input: The statement `import numpy as np`.
Expected output: There is no printed output, but the name `np` becomes ready for later examples.
Concept to check: Installation commands and import statements differ in execution place and role.

```python
# This imports installed NumPy into Python code under the short name np.
import numpy as np
```

Here, `np` is the conventional alias used to call NumPy briefly.

The complete example code of this section can also be downloaded as the following file.

- [p2_3_6_numpy_linear_algebra.py](../../../assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py)

If you run it from the project root, you can use the following command in your personal-PC terminal.

```bash
python docs/assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py
```

This file prints vector addition, scalar multiplication, element-wise multiplication, matrix multiplication, and batch calculation together.

## Creating Vectors and Matrices

A vector can be created as a list of values.

This example is the place where we confirm in code what `P2-3.1` said: `a vector can be read like a one-dimensional array`.

Problem situation: Create in NumPy the vector seen in the formula and check its shape.
Input: The array `x` containing two values.
Expected output: The vector value and `shape (2,)` are printed.
Concept to check: A vector appears in NumPy as a one-dimensional array, and its length can be checked through `shape`.

```python
# This example imports NumPy to prepare vector and matrix calculations for linear algebra examples.
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

This example is the place where we recheck the explanation from `P2-3.1` that `a matrix is a two-dimensional structure that gathers several vectors`.

Problem situation: Create in NumPy the weight matrix seen in the formula and check its shape.
Input: The `W` array with 2 rows and 2 columns.
Expected output: The matrix values and `shape (2, 2)` are printed.
Concept to check: A matrix appears in NumPy as a two-dimensional array, and the number of rows and columns is read through `shape`.

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

## Check Shape First

When an AI calculation does not work in code, it is often necessary to check shape before values.

This habit translates the standard from `P2-3.2` that said `comparison works only inside the same space` into code level. If lengths and forms differ, comparison or multiplication itself may not hold.

Problem situation: Check first whether the input vector and weight matrix have shapes that allow calculation.
Input: The vector `x` and the matrix `W`.
Expected output: The shapes of `x` and `W` are printed.
Concept to check: When moving linear-algebra calculations into code, shape should be checked before values.

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

Read from the perspective of P2-3.3, `x` is a vector with 2 input values, and `W` is a weight matrix that receives 2 inputs and makes 2 outputs.

## Checking Vector Addition and Scalar Multiplication

Vector addition adds values at the same positions.

This example is where we recheck in code the minimum operations of vector space from `P2-3.2`. In other words, a vector is not only a target for comparison, but also a target for calculation that can be added and rescaled into a new representation.

Problem situation: Confirm the basic calculation that adds two vectors position by position.
Input: The length-3 vectors `a` and `b`.
Expected output: The position-wise sum `[5 7 9]` is printed.
Concept to check: Vector addition is a calculation that adds values at the same positions.

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

Problem situation: Confirm the calculation that multiplies one scalar value into an entire vector.
Input: The vector `a` and the scalar `2`.
Expected output: `[2 4 6]` is printed.
Concept to check: Scalar multiplication applies the same number to each position of a vector.

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

These two calculations connect directly to the minimum calculations of vector space described in P2-3.2.

## `*` Means Element-Wise Multiplication

In NumPy, using `*` between arrays usually becomes element-wise multiplication.

This example also connects to the comparison questions that will return in `P2-3.4`. For now, we first become familiar with the shape of the operation that multiplies matching positions, and later we distinguish that from dot product or similarity calculations.

Problem situation: Confirm an example where the `*` operator behaves not as matrix multiplication but as element-wise multiplication.
Input: The length-3 vectors `a` and `b`.
Expected output: The element-wise product `[ 4 10 18]` is printed.
Concept to check: NumPy’s `*` is an element-wise calculation between matching positions.

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

## `@` Means Matrix Multiplication

In NumPy, `@` is used for matrix multiplication.

This example is where the core of `P2-3.3` is restored in code. `@` is not a calculation that multiplies matching positions. It is a weighted-sum structure that multiplies and adds to make a new vector.

Problem situation: Calculate weighted-sum-based matrix multiplication using an input vector and a weight matrix.
Input: The length-2 vector `x` and the `2 x 2` matrix `W`.
Expected output: The output vector `y` and its `shape` are printed.
Concept to check: `@` is not element-wise multiplication, but matrix multiplication that multiplies and adds to make a new vector.

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

## Calculating Several Samples at Once

If several input samples are grouped into a matrix, the same weight matrix can be applied all at once.

Problem situation: Confirm batch calculation where several samples are grouped into a matrix and the same weight matrix is applied at once.
Input: The `2 x 2` input matrix `X` and the `2 x 2` weight matrix `W`.
Expected output: The shapes of `X`, `W`, and `Y`, plus the batch-calculation result matrix, are printed.
Concept to check: Even when calculating several samples together, the core issue is still matrix-shape compatibility.

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

## Intentionally Thinking Through a Shape Error

The following calculation does not match immediately.

Problem situation: Confirm what kind of problem happens when the input-vector length and the input-side size of the weight matrix are different.
Input: The length-3 vector `bad_x` and the `2 x 2` matrix `W`.
Expected output: A shape mismatch error occurs when matrix multiplication is attempted.
Concept to check: Linear algebra code runs only when the shapes match, not merely when the values look reasonable.

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

More important than memorizing the exact error message is asking whether the last size on the left matches the input-side size on the right, whether the intended operation is element-wise multiplication or matrix multiplication, and what the output shape ought to be.

## Looking Through a Case

### Case 1. Why Does the Same-Looking Code Suddenly Stop Working If We Do Not Check Shape?

Many learners, while following NumPy examples, mix `*` and `@`, or fail to match vector length and matrix size, and then run into errors. Even if the numbers look similar, NumPy decides first whether the calculation is possible by checking whether the shape matches.

For example, the vector `x` of length 2 and the `2 x 2` matrix `W` can be multiplied as `x @ W`. But if the input-vector length changes to 3 while the weight matrix stays the same, the calculation stops because it can no longer decide which values should be combined with which weights.

This case shows why the instruction `look at shape before values` keeps being repeated. Linear-algebra formulas may look simple in symbols, but in code we must check how many values each vector and matrix actually contains before we can reproduce the same calculation.

So the core of NumPy practice is less about memorizing syntax and more about rechecking the structure of a formula through shape. The standards for reading whether `*` is element-wise multiplication, whether `@` is matrix multiplication, and how input and output dimensions connect continue directly into later model calculations.

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

- Example code of this section: [p2_3_6_numpy_linear_algebra.py](../../../assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py)
- NumPy Developers, [NumPy documentation](https://numpy.org/doc/){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-19.
- NumPy Developers, [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-19.
- NumPy Developers, [`numpy.array`](https://numpy.org/doc/stable/reference/generated/numpy.array.html){: target="_blank" rel="noopener noreferrer" }. It provides the array-creation API and examples. Checked: 2026-07-19.
- NumPy Developers, [`numpy.ndarray.shape`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.shape.html){: target="_blank" rel="noopener noreferrer" }. It documents the `shape` attribute as the tuple of array dimensions. Checked: 2026-07-19.
- NumPy Developers, [`numpy.matmul`](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html){: target="_blank" rel="noopener noreferrer" }. It documents matrix multiplication and the shape-mismatch error condition. Checked: 2026-07-19.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, checked 2026-07-19.
