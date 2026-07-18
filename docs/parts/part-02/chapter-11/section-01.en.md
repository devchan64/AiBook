# P2-11.1 Building Vectors and Matrices with NumPy Arrays

> Section ID: `P2-11.1`
> Version: `v2026.07.12`

Part 2 Chapter 3 introduced scalars, vectors, and matrices through mathematical notation and small code examples. Part 2 Chapter 8 looked at Python lists and dictionaries, Part 2 Chapter 9 distinguished arrays, tables, trees, and graphs as different data-structure viewpoints, and Part 2 Chapter 10 organized notebooks as rerunnable learning records.

Now we return to NumPy. NumPy comes from "Numerical Python." It is a widely used open-source library for creating numeric arrays in Python and carrying out vector and matrix calculations with fast, consistent syntax.

This Section explains the basic distinctions among `NumPy`, `shape`, `ndim`, and `dtype`. The point of this chapter is not to memorize a large amount of NumPy syntax. It is to learn how vectors, matrices, and bundles of data appear in code in AI practice. When you meet arrays, axes, and broadcasting again later, the [Concept Glossary](/AiBook/reference/concept-glossary/) is also a useful anchor.

When you study AI, data quickly turns into numeric arrays. Sentences become arrays of token IDs, images become arrays of pixels, tabular data becomes feature matrices, and embeddings become vectors. You can handle those bundles of numbers with Python lists alone, but NumPy arrays are much more natural when you need to add, multiply, average, or multiply matrices across many values in the same way.

If the previous Python-syntax and data-structure chapters focused on what values are written and in what kinds of sentences, this chapter focuses on how those values are handled in vector and matrix shapes that can actually be used for computation. The next chapters move the question toward reading those numeric shapes as tables, checking them with plots, and finally leaving them as records.

| What to capture in this Section now | The question that follows immediately next | Where it appears again later |
| --- | --- | --- |
| The point that NumPy is a tool for making computable numeric shapes | It leads to how those arrays should be read as tables with rows and columns in Part 2 Chapter 12. | It repeats later in every machine-learning input matrix, embedding, and prediction calculation. |
| The point that `shape`, `ndim`, and `dtype` must be checked first | It leads to the standard for not confusing axes and table structure in P2-11.2 and Part 2 Chapter 12. | It stays important later in preprocessing, model-input checks, and error diagnosis. |
| The point that NumPy is the first stage of the `calculation -> table -> plot -> record` flow | It leads to what to inspect and what to leave as a record in Part 2 Chapters 13 and 14. | It becomes the starting point for experiment interpretation and result reproduction after Part 3. |

| Term | Meaning to capture first in this Section |
| --- | --- |
| NumPy | The representative Python library for numeric arrays and vector or matrix calculation. |
| `shape` | Shape information showing how many dimensions an array has and how long each axis is. |
| `ndim` | The number of dimensions in an array. |
| `dtype` | The data type of the numbers inside an array. |
| `ndarray` | The multidimensional array data structure NumPy uses by default. |

## Scope of This Section

This Section covers how to create NumPy arrays and how to inspect their shape, number of dimensions, and data type. It also goes as far as examples that build vectors and matrices and compute a small weighted sum.

Here we answer the following questions.

- Why are Python lists and NumPy arrays used differently?
- How do we build vectors and matrices with NumPy arrays?
- What do `shape`, `ndim`, and `dtype` tell us?
- Why should we check the shape of numbers first when building vectors and matrices?
- Why do input data and weights appear as arrays in AI practice?

This Section does not cover broadcasting, advanced indexing, performance optimization, memory layout, GPU computation, or the internal implementation of linear-algebra algorithms. Axes and slicing are covered in more detail in P2-11.2, and advanced indexing and shape changes are revisited in the supplementary learning of P2-11.4.

## Goals of This Section

- You can explain a NumPy array in contrast with a Python list.
- You can read a one-dimensional array as a vector and a two-dimensional array as a matrix.
- You can explain an array's shape and character by checking `.shape`, `.ndim`, and `.dtype`.
- You can explain that even the same bundle of numbers is used differently in computation when it is a list versus an array.
- You can read the flow that produces a small prediction score by multiplying an input matrix and a weight vector.

## Three Criteria

| Criterion | Why it matters | Level of understanding needed in this Section |
| --- | --- | --- |
| What a NumPy array is | It helps you read NumPy not as new syntax, but as a structure of computable numeric shapes. | Understand it as a structure for holding numbers in a fixed shape for calculation. |
| Why it should be viewed differently from a list | It makes the difference between a storage structure and a computation structure clear. | Understand that both hold values, but an array is aimed more directly at numeric computation. |
| What should be checked first | It creates the starting point for later reading indexing and broadcasting. | Understand that `shape` and dimension should be checked before values. |

## NumPy Is a Tool for Numeric Array Computation

The official NumPy documentation introduces NumPy as an open-source Python library widely used in science and engineering. It also explains that NumPy provides the `ndarray`, a multidimensional array data structure, and functions that operate efficiently on that array.

Here, understand a NumPy array as `a computation-oriented bundle in which numbers are placed in a fixed shape`.

Python lists can also group values.

Problem situation: Before using NumPy, we first confirm that a bundle of numbers can already be stored in a Python list.
Input: A Python list containing three scores.
Expected output: There is no printed output, but it shows the simplest form of a bundle of numbers.
Concept to check: See that a list is a general-purpose container for holding values, not yet a computation-oriented array.

```python
scores = [82, 75, 45]
```

But a list is a general-purpose bundle of values. It can contain only numbers, or mix strings and objects. The NumPy documentation also describes Python lists as excellent general-purpose containers, while explaining that NumPy is a better fit when the data has the same type, the amount is large, and common calculations must be performed.

By contrast, a NumPy array is closer to a structure for arranging the same kind of numbers in a fixed shape and calculating with them.

Problem situation: We check how the same bundle of numbers looks when turned into a NumPy array for computation.
Input: A one-dimensional array containing three scores.
Expected output: There is no printed output, but a computation-oriented array created with `np.array(...)` is prepared.
Concept to check: See that a NumPy array is a structure for handling the same kind of numbers in a consistent shape.

```python
import numpy as np

scores = np.array([82, 75, 45])
```

This difference matters in AI practice. Model inputs, features, weights, embeddings, and image pixels are usually calculated as numeric arrays.

## Why We Meet NumPy Early in AI Learning

You do not need to implement every internal AI-model calculation by hand from the start. Real deep-learning workflows may use tools such as PyTorch, TensorFlow, or JAX. But those tools also stand on intuitions about numeric arrays, shape, axes, matrix multiplication, and position-wise operations.

We look at NumPy first for the following reasons.

| Reason | What it gives in learning |
| --- | --- |
| You can inspect array shape directly | You check input and output structure through `shape` |
| You can reproduce vector and matrix calculations on a small scale | You see how formulas run in code |
| You can compare Python lists with computation-oriented arrays | You distinguish data structure from computation structure |
| Machine-learning examples often use NumPy arrays | Official examples and tutorials become easier to read |
| It connects with pandas, scikit-learn, and visualization tools | It becomes easier to move on to later data-processing tools |

So NumPy is not "AI itself." But it is close to a basic language for reading AI computation. This Section builds that minimum intuition rather than teaching NumPy in depth.

If you place Part 2 Chapters 11 through 14 in one flow, NumPy handles `making computable numeric shapes`, Pandas handles `reading those shapes as tables of cases and variables`, Matplotlib handles `checking changes and relationships that are not immediately visible in the table as shapes`, and Git handles `leaving those calculations and interpretations as records together with the reason for change`. Chapter 11 is the very front of that flow, where you build computable numeric shapes such as vectors, matrices, and `shape`.

## Lists and Arrays Look Similar but Have Different Purposes

Python lists and NumPy arrays can look similar on the surface.

Problem situation: We want to prepare the same bundle of numbers both as a list and as an array to compare them side by side.
Input: Two variables built from the same score data, one as a Python list and one as a NumPy array.
Expected output: There is no printed output, but the setup is ready for comparing the same operation later.
Concept to check: See that even if they look similar, a list and an array can have different meanings in computation.

```python
python_scores = [82, 75, 45]
numpy_scores = np.array([82, 75, 45])
```

But the difference appears when you try the same operation.

Problem situation: We directly compare how the same `+` operator is read differently for a list and for an array.
Input: `python_scores` and `numpy_scores` from above.
Expected output: The list is concatenated, while the array prints the result of position-wise addition.
Concept to check: Confirm that a NumPy array is both a storage structure and a computation structure.

```python
print(python_scores + python_scores)
print(numpy_scores + numpy_scores)
```

For a list, `+` joins two lists together.

```text
[82, 75, 45, 82, 75, 45]
```

For a NumPy array, `+` adds numbers at the same positions.

```text
[164 150  90]
```

This difference needs to be remembered.

| Structure | Main purpose | Representative meaning of `+` |
| --- | --- | --- |
| Python list | General-purpose container that stores several values in order | List concatenation |
| NumPy array | Calculating with bundles of numbers in the same shape | Position-wise addition |

A NumPy array is both `a structure that holds data` and `a structure that performs computation`.

The diagram below shows how the same `+` symbol is read differently in lists and NumPy arrays.

![Python list and NumPy array use the plus sign differently](/AiBook/assets/part-02/chapter-11/list-vs-numpy-array-en.svg)

This difference may look small, but it matters in AI code. The question changes depending on whether you want to store a bundle of numbers or apply the same computation to the whole bundle.

## Building a Vector

A vector can be read as a structure in which numbers are arranged in one line.

Problem situation: We create a one-dimensional NumPy array that looks like an embedding and inspect its basic properties.
Input: An array `embedding` containing four real numbers.
Expected output: The array value, `shape`, `ndim`, and `dtype` are printed in order.
Concept to check: See the habit of reading a one-dimensional array as a vector and checking its shape and number of dimensions together.

```python
import numpy as np

embedding = np.array([0.12, -0.03, 0.44, 0.18])

print(embedding)
print(embedding.shape)
print(embedding.ndim)
print(embedding.dtype)
```

The output will look roughly like this.

```text
[ 0.12 -0.03  0.44  0.18]
(4,)
1
float64
```

Each piece of information here means the following.

| Expression | Meaning | Meaning in this example |
| --- | --- | --- |
| `shape` | The shape of the array | A one-dimensional array with four values |
| `ndim` | Number of dimensions | One dimension |
| `dtype` | Data type of the values | Real-valued numbers |

Mathematically, you can connect it to the following vector.

\[
\mathbf{x} = [0.12,\ -0.03,\ 0.44,\ 0.18]
\]

Here, read a vector as `an ordered bundle of numbers`. In NumPy, what matters is that this bundle of numbers is a computable array.

## Building a Matrix

A matrix can be read as a two-dimensional array with rows and columns.

Problem situation: We create a two-dimensional array that looks like a score table for several students and inspect its properties.
Input: The integer array `scores` with 2 rows and 3 columns.
Expected output: The matrix value, `shape`, `ndim`, and `dtype` are printed in order.
Concept to check: See how a two-dimensional array is read as a matrix and how the number of rows and columns is checked through `shape`.

```python
scores = np.array([
    [82, 75, 45],
    [90, 61, 70],
])

print(scores)
print(scores.shape)
print(scores.ndim)
print(scores.dtype)
```

The output will look roughly like this.

```text
[[82 75 45]
 [90 61 70]]
(2, 3)
2
int64
```

`(2, 3)` means 2 rows and 3 columns.

\[
S =
\begin{bmatrix}
82 & 75 & 45 \\
90 & 61 & 70
\end{bmatrix}
\]

Here, the phrase "2 rows and 3 columns" is not only a shape description. You also need to decide what each axis means.

For example, you can read this matrix in the following way.

| Axis | Interpretation |
| --- | --- |
| row | student or sample |
| column | subject or feature |

In AI practice, rows are often read as samples and columns as features. But that is not always the case. So once you create an array, you should first check `shape` and then write down what each axis means.

## Shape Is the Grammar of Computation

In NumPy code, `shape` is not simple extra information. It is the basic grammar for deciding what computation is possible.

Look at the following arrays.

Problem situation: We first check whether a feature matrix and a weight vector have compatible shapes for computation.
Input: `features`, a matrix of shape `(3, 2)`, and `weights`, a vector of length 2.
Expected output: The `shape` of both arrays is printed.
Concept to check: See that before computation, you should check whether the shapes fit before looking at the values.

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

The output is as follows.

```text
(3, 2)
(2,)
```

These shapes can be read like this.

| Array | shape | Meaning |
| --- | --- | --- |
| `features` | `(3, 2)` | 3 samples, 2 features |
| `weights` | `(2,)` | Weights to multiply the 2 features |

Now you can use the matrix-multiplication operator `@` to calculate one score for each sample.

Problem situation: We multiply the two features of each sample by weights to compute a score per sample.
Input: The `features` matrix and `weights` vector above.
Expected output: A score array for each sample and the result `shape` are printed.
Concept to check: Confirm that when the inner dimensions match, a feature matrix and weight vector can produce a score for each sample.

```python
scores = features @ weights
print(scores)
print(scores.shape)
```

The output will look roughly like this.

```text
[0.68 0.64 0.54]
(3,)
```

This computation multiplies the two features of each sample by weights and turns them into one score.

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

What matters here is not memorizing the formula. The key point is that the number of columns in `features` must match the length of `weights` for the computation to work.

The diagram below reorganizes the same computation from the viewpoint of shape.

![Feature matrix times weight vector produces one score per sample](/AiBook/assets/part-02/chapter-11/feature-weight-shape-flow-en.svg)

On the left, `features` is a matrix with 3 samples and 2 features. In the middle, `weights` is a weight vector corresponding to those 2 features. Because the inner size 2 matches between the arrays, one score is produced for each sample.

## Arrays Show the Shape of Small Model Calculations

The example above can be read like a very small model calculation.

Real machine-learning models are much more complex, but the basic intuition is similar. You place features for several samples into a numeric array, prepare a weight array, and read the output as something produced by array computation.

This structure repeats throughout Part 3 on machine learning and Part 4 on deep learning. So the purpose of learning NumPy arrays goes beyond "how to use a library." It is about building the eye needed to read model computation.

## Three Things to Check When You Create an Array

When you create a NumPy array, check three things first.

Problem situation: We inspect what should be printed first when we meet a newly created array.
Input: Any NumPy array variable `array`.
Expected output: `shape`, `ndim`, and `dtype` are printed in order.
Concept to check: See the habit of checking an array's shape, dimension, and type before looking at its values one by one.

```python
print(array.shape)
print(array.ndim)
print(array.dtype)
```

Each one connects to the following question.

| Check | Question | Why it matters |
| --- | --- | --- |
| `shape` | What shape is it? | It checks whether the shape is computable |
| `ndim` | How many dimensions does it have? | It distinguishes a vector, a matrix, and higher dimensions |
| `dtype` | What type is it? | It reduces confusion among integers, real numbers, and strings |

At the beginner stage, when an error occurs, it is usually better to check `shape` first rather than trying to inspect values one by one. In AI code, many errors happen because array shapes do not fit, not because individual values are too large or too small.

## Example Code File

You can also inspect the example code from this Section in the following file.

- [p2_11_1_numpy_arrays.py](/AiBook/assets/part-02/chapter-11/p2_11_1_numpy_arrays.py)

In Colab, you can paste the code into a cell and run it. On a local PC, you can run it from the project root like this.

```bash
python docs/assets/part-02/chapter-11/p2_11_1_numpy_arrays.py
```

This command prints the `shape`, `ndim`, and `dtype` of a vector, a matrix, a feature matrix, and a weight vector, and shows a small weighted-sum calculation.

The output also includes how `+` works differently for a Python list and a NumPy array. It is an example meant to let you check directly that the same symbol can change meaning when the data structure changes.

## Reading It as a Case

### Case 1. Why does a student score table suddenly start looking like a numeric matrix?

When a learner looks at a score table by student and then meets a NumPy array example, it is natural to think, "Why did this suddenly become a matrix?" People usually read names and subjects first in a table, but in the computation stage, each student's bundle of scores is read as one row, and each subject is read as one column.

For example, a table of four students with scores in three subjects can appear in NumPy as an array of shape `(4, 3)`. The important point is not memorizing many numbers. It is first capturing the correspondence that `4 rows means four students` and `3 columns means three subjects`. Only then can you interpret what later calculations such as averages, weighted sums, and matrix multiplication mean.

This case also shows why `shape` must be checked before values. Even with the same numbers, the meaning of each axis changes depending on whether you read them as `(4, 3)` or `(3, 4)`, and the interpretation of later calculations changes as well.

In other words, an introduction to NumPy is less about memorizing new syntax than about `practicing how to read real data in computable shapes`. You need this intuition so that feature matrices and weight calculations after Part 3 feel less unfamiliar.

## Checklist

- You can explain the difference in purpose between a Python list and a NumPy array.
- You can build vectors and matrices with `np.array()`.
- You can explain what `.shape`, `.ndim`, and `.dtype` tell you.
- You can distinguish a one-dimensional array from a two-dimensional array.
- You can read a matrix in the form `(number of samples, number of features)`.
- You can explain the input and output shapes in a small calculation such as `features @ weights`.
- You can explain that NumPy arrays arrange numbers in fixed shapes for calculation, and that `shape` works like the grammar of array computation.

## Sources and References

- NumPy Developers, [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-06-25.
- NumPy Developers, [The N-dimensional array](https://numpy.org/doc/stable/reference/arrays.ndarray.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-06-25.
- NumPy Developers, [Array creation](https://numpy.org/doc/stable/user/basics.creation.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-06-25.
