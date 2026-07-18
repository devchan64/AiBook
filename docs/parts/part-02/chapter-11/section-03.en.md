# P2-11.3 Broadcasting and Vectorization

> Section ID: `P2-11.3`
> Version: `v2026.07.12`

In P2-11.1, we checked the `shape`, `ndim`, and `dtype` of NumPy arrays. In P2-11.2, we used indexing, slicing, and axis to decide which part of an array to read and in which direction to calculate.

Now we go one step further. In NumPy code, you often see calculations applied across a whole array even though no loop is written directly.

For example, the following code adds one number to an entire array.

Problem situation: We check with the smallest example whether the same value can be added across a whole array without a loop.
Input: An array containing three scores and the scalar `10`.
Expected output: A new array is printed with 10 added to each value.
Concept to check: See that the first intuition of broadcasting is that a scalar is applied to each position in the array.

```python
import numpy as np

scores = np.array([82, 75, 45])
print(scores + 10)
```

The output is as follows.

```text
[92 85 55]
```

There is no `for` in the code. But from the result, we can see that 10 was added to every value. To understand this kind of calculation, we need to look at broadcasting and vectorization together.

This Section explains the basic distinction between `broadcasting` and `vectorization`. The representative explanations of `NumPy`, `shape`, and `axis` remain in P2-11.1, P2-11.2, and the [Concept Glossary](/AiBook/reference/concept-glossary/). Here the focus is on how calculation spreads across the whole array.

## Scope of This Section

This Section deals with the basic way NumPy applies calculations across an entire array.

Here we answer the following questions.

- What does broadcasting make match?
- How is a scalar calculated together with an array?
- Why can an array of shape `(4, 3)` be added to an array of shape `(3,)`?
- Why is it hard to directly add an array of shape `(4, 3)` and an array of shape `(4,)`?
- Does vectorization remove repetition, or does it move repetition to a different place?
- Why are normalization, weight calculation, and feature-wise operations often written at the array level in AI practice?

This Section does not go deeply into advanced broadcasting, the detailed use of `np.newaxis`, `reshape`, stride, memory views, performance benchmarks, or GPU tensor computation. `np.newaxis` and shape changes return in the supplementary learning of P2-11.4. Here the focus is on building the intuition that `if the shape fits, repeated calculation can be read at the array level`. If broadcasting examples mostly make sense but the difference among `(3,)`, `(3, 1)`, and `(1, 3)` or the sharing of originals after slicing is still confusing, pause this Section briefly, move to P2-11.4, and then return.

## Goals of This Section

- You can explain broadcasting as the rule by which a smaller array is calculated as if it were matched to the shape of a larger array.
- You can read scalar-array calculation as element-wise calculation.
- You can explain examples that add or subtract a vector of shape `(m,)` to a data matrix of shape `(n, m)`.
- You can explain that a broadcasting error can occur when shapes do not match.
- You can explain vectorization not as `repetition disappeared`, but as `a Python loop was expressed as one array operation`.

## Three Criteria

| Criterion | Why it matters | Level of understanding needed in this Section |
| --- | --- | --- |
| What broadcasting is | It explains why whole-array calculation can be read in one line. | Understand it as a way of naturally spreading and applying a smaller array in a larger-array calculation. |
| What vectorization is | It makes clear that repetition did not vanish, but changed where it is expressed. | Understand it as a way of expressing what was written as a loop through one array operation. |
| What to watch first | It lets you see convenience and the possibility of shape errors together. | Understand that even if the syntax looks convenient, `shape` must be checked first. |

| Term | Meaning to capture first in this Section |
| --- | --- |
| broadcasting | The rule that applies a smaller array or scalar to a larger-array calculation. |
| vectorization | A way of expressing repeated calculation through one array operation. |
| element-wise operation | A calculation that applies the same rule to values at corresponding positions. |
| shape compatibility | The shape condition used to judge whether two arrays can be calculated together. |
| scalar | One number that serves as the same rule applied across a whole array. |

## Broadcasting Lets Calculation Proceed by Matching Shape

The official NumPy documentation introduces broadcasting as a term explaining how arithmetic operations handle arrays with different shapes. A smaller array is treated as if it had a shape compatible with the larger array during the calculation.

Here, understand broadcasting as `the rule that repeatedly applies a small value or small array to fit the shape of a larger array`.

The easiest example is a scalar calculated with an array.

Problem situation: We compare what happens when a scalar is added to or multiplied with the whole array.
Input: The score array `scores` and the scalars `10` and `2`.
Expected output: The result of `+10` and the result of `*2` are each printed.
Concept to check: Confirm that a scalar operation applies the same rule to each position in the array.

```python
scores = np.array([82, 75, 45])

print(scores + 10)
print(scores * 2)
```

The output is as follows.

```text
[92 85 55]
[164 150  90]
```

Here, `10` and `2` are scalars. NumPy applies the scalar to every position in the array.

The diagram below shows a scalar being repeatedly applied across the whole array. It is safer to understand this not as physically copying the same value many times, but as applying the same calculation rule at each position.

![A scalar is applied across an array by broadcasting](/AiBook/assets/part-02/chapter-11/broadcast-scalar-array-en.svg)

## When Arrays Are Calculated Together, Check Shape First

Broadcasting is not a feature that forcefully makes any arrays fit together. The shapes must be compatible.

For example, look at the following arrays.

Problem situation: We check together the `shape` and the result to see whether a feature-wise offset vector can be added to a feature matrix.
Input: `features` of shape `(4, 3)` and `feature_offset` of shape `(3,)`.
Expected output: The `shape` of both arrays and the adjusted matrix are printed.
Concept to check: See that a length-3 vector can be broadcast across the three features of each row.

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

The output is as follows.

```text
(4, 3)
(3,)
[[1.1 0.4 7.3]
 [0.9 0.6 6.8]
 [0.4 1.1 8.4]
 [0.6 0.3 6.1]]
```

The shape of `features` is `(4, 3)`. It can be read as 4 samples and 3 features.

The shape of `feature_offset` is `(3,)`. It can be read as one value to add for each of the 3 features.

NumPy judges that the array of shape `(3,)` can be applied to each row. So the same offset is added to the three features of every sample.

The diagram below shows a vector of shape `(3,)` being applied row by row to a data matrix of shape `(4, 3)`.

![A row-shaped vector is broadcast across each row of a feature matrix](/AiBook/assets/part-02/chapter-11/broadcast-row-vector-en.svg)

## Incompatible Shapes Produce an Error

Broadcasting is convenient, but if the shapes do not fit, an error occurs.

Problem situation: We check why shapes that look somewhat similar still produce an error when they do not match.
Input: The matrix `features` of shape `(4, 3)` and the vector `bad_offset` of length 4.
Expected output: The two shapes are printed, and then a broadcasting error occurs.
Concept to check: See that broadcasting does not make arbitrary arrays fit, and that compatibility from the last dimension matters.

```python
bad_offset = np.array([10, 20, 30, 40])

print(features.shape)
print(bad_offset.shape)
print(features + bad_offset)
```

This code raises an error.

```text
ValueError: operands could not be broadcast together with shapes (4,3) (4,)
```

Why?

`features` is `(4, 3)`. Each row has 3 features. But `bad_offset` is `(4,)`. These 4 values may look as if they match the number of rows, but they do not match the 3 columns inside each row.

Remember the following standard first.

| Calculation | How to read it | Result |
| --- | --- | --- |
| `(4, 3) + scalar` | Apply the same value to every position | possible |
| `(4, 3) + (3,)` | Apply a length-3 vector to each row | possible |
| `(4, 3) + (4,)` | Does not match the row length 3 | error |

The exact rule is more complex, but at this stage the important intuition is `check whether they match from the last dimension`.

## Vectorization Means Expressing Repetition as an Array Operation

Vectorization is a way of expressing a calculation through array operations without writing an explicit Python loop.

For example, adding 10 to each score with a Python loop can be written like this.

Problem situation: Before comparing it with an array operation, we write the same work directly with a loop.
Input: A Python list containing three scores.
Expected output: A list is printed with 10 added to each score.
Concept to check: See that vectorization is a way of expressing this repeated calculation more compactly as an array operation.

```python
scores = [82, 75, 45]

adjusted = []
for score in scores:
    adjusted.append(score + 10)

print(adjusted)
```

With a NumPy array, it can be written like this.

Problem situation: We rewrite the work just done with a loop as one line of NumPy array calculation.
Input: The score array `scores` and the scalar `10`.
Expected output: The adjusted score array is printed.
Concept to check: Confirm that vectorization does not mean repetition vanished, but that it was expressed in array-level syntax.

```python
scores = np.array([82, 75, 45])
adjusted = scores + 10

print(adjusted)
```

Both versions add 10 to each score. The difference is in how the idea is expressed.

| Method | Structure visible in code | Perspective the reader should hold |
| --- | --- | --- |
| Python loop | Pull out one value at a time and process it | The procedure is written directly |
| NumPy vectorization | Apply the operation to the whole array | The same calculation is expressed at the array level |

The official NumPy documentation explains that broadcasting provides a means of vectorizing array operations and helps repetition happen at the C level instead of in Python. So it would be misleading to understand vectorization as `the repetition disappeared`.

A safer expression is to view vectorization as `a way of expressing repeated calculation not with Python's for loop, but with array operations`.

The diagram below shows the same calculation expressed differently as a loop and as an array operation.

```mermaid
--8<-- "assets/part-02/chapter-11/loop-to-vectorization-flow-en.mmd"
```

## An Example of Subtracting the Mean by Feature

One example that appears often in AI data processing is subtracting the mean of each feature. You can read it as the starting point of preprocessing that moves the mean closer to 0.

First, create the data matrix.

Problem situation: In preprocessing that subtracts the feature-wise mean, we check the mean vector and the centered result together.
Input: The feature matrix `features` with shape `(4, 3)`.
Expected output: The mean vector by column and the matrix after subtracting the mean are printed.
Concept to check: See that the result of `mean(axis=0)` with shape `(3,)` is broadcast to each row and produces centering.

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

The output will look roughly like this.

```text
[0.65 0.4  6.85]
[[ 0.35 -0.2   0.15]
 [ 0.15  0.   -0.35]
 [-0.35  0.5   1.25]
 [-0.15 -0.3  -1.05]]
```

Here, `features.mean(axis=0)` calculates the mean of each column. The result shape is `(3,)`. The shape of `features` is `(4, 3)`.

`features - column_mean` is a calculation that subtracts `(3,)` from `(4, 3)`. NumPy applies the mean vector of shape `(3,)` to each row.

This example connects directly to the explanation of axis in P2-11.2.

| Code | shape | Meaning |
| --- | --- | --- |
| `features` | `(4, 3)` | 4 samples, 3 features |
| `features.mean(axis=0)` | `(3,)` | Mean by feature |
| `features - column_mean` | `(4, 3)` | Result after subtracting the mean of each feature from each sample |

What matters is not simply `one mean was calculated`. You should read together which axis the mean was taken across, what shape that result has, and how it is applied back to the original array.

## Broadcasting Is Convenient, but Not Always Best

Broadcasting and vectorization can shorten code and often make it easier to read. But that does not mean they are always the better choice.

There are three things to watch.

First, if you do not check shape, you can end up with a calculation different from what you intended.

Second, complex broadcasting can become hard-to-read code.

Third, in some cases, a very large intermediate array can be created and use a lot of memory. The official NumPy documentation also warns that broadcasting is usually efficient, but in certain algorithms it can use memory inefficiently.

So a good beginner habit is the following.

Problem situation: We check which shapes should be printed first before a broadcasting calculation.
Input: The original matrix `features` and the column-mean vector `column_mean`.
Expected output: The shapes of the two arrays are printed.
Concept to check: See that even if broadcasting looks convenient, it is safer to check the shapes first.

```python
print(features.shape)
print(column_mean.shape)
```

Before calculating, check the shape.

## Example Code File

You can also inspect the example code from this Section in the following file.

- [p2_11_3_broadcast_vectorization.py](/AiBook/assets/part-02/chapter-11/p2_11_3_broadcast_vectorization.py)

On a local PC, you can run it from the project root like this.

```bash
python docs/assets/part-02/chapter-11/p2_11_3_broadcast_vectorization.py
```

In Colab, you can paste the file content into a code cell and run it.

The output includes scalar broadcasting, row-vector broadcasting, a shape-mismatch error example, and an example that removes the mean by feature.

## Reading It as a Case

### Case 1. Why add adjusted scores for every student at once?

When a learner wants to add an adjustment value to each student's score, it is natural to want to process them one by one with a `for` loop. This is good for understanding procedure, but as the number of features and samples grows, the same calculation has to be written again and again and the code becomes long.

With NumPy arrays, the same calculation can be expressed all at once through something like `scores + 10` or by adding a vector of shape `(3,)` to a matrix of shape `(4, 3)`. The important point is not that NumPy magically calculates for you, but that the same repeated operation previously done by a person is rewritten in array-level syntax.

For example, if you add an offset `[0.1, 0.2, 0.3]` by feature to every student with three features, the same length-3 vector is applied to each row of the `(4, 3)` matrix. By contrast, if you try to add a vector of shape `(4,)`, the shape does not match and an error occurs. So the first thing to check is always `shape`, not convenience.

This case ties broadcasting and vectorization back to an actual calculation scene. Repetition was not removed. It was expressed as array calculation, and for that expression to work safely, you must first read what question the smaller array and the larger array correspond to.

## Checklist

- You can explain scalar-array calculation as broadcasting.
- You can explain why `(4, 3) + (3,)` is possible.
- You can explain why `(4, 3) + (4,)` can fail immediately.
- You can explain the difference between a Python loop and a NumPy vectorized expression.
- You can explain the result shape of `features.mean(axis=0)`.
- You can explain where broadcasting occurs in the calculation that subtracts the mean by feature.
- You can explain that broadcasting is not always the best choice and that shape and memory use should be checked.
- You can explain that broadcasting is the rule that lets a small value or array participate in calculation by fitting the shape of a larger array.

## Sources and References

- NumPy Developers, [Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-06-25.
- NumPy Developers, [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-06-25.
- NumPy Developers, [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-06-25.
