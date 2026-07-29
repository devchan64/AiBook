# P2-11.2 Indexing, Slicing, and Axis

> Section ID: `P2-11.2`
> Version: `v2026.07.26`

In P2-11.1, we created NumPy arrays and checked `shape`, `ndim`, and `dtype`. Now we move on to which value to read from an array, which range to cut out, and which direction to calculate along.

Three terms appear often when reading NumPy arrays.

Indexing, slicing, and axis.

These three can look similar, but their roles are different. Indexing chooses a position. Slicing chooses a range. Axis decides the direction of a calculation.

This Section explains the basic distinctions among `indexing`, `slicing`, and `axis`. You can revisit `NumPy` and the basic properties of arrays in P2-11.1 and P2-11.2. Here the focus is on what to choose from an array and in which direction to read it.

## Core Criteria: Indexing, Slicing, and Axis

- You can explain indexing such as `x[0]` and `x[1, 2]` as position selection.
- You can explain slicing such as `x[1:3]`, `x[:, 0]`, and `x[0:2, 1:3]` as range selection.
- In a two-dimensional array, you can read the first axis (`axis 0`) as the row direction and the second axis (`axis 1`) as the column direction.
- You can explain why the result shapes of `sum(axis=0)` and `sum(axis=1)` are different.
- You can explain the viewpoint that, in datasets, rows are often read as samples and columns as features.

## One Scene to Hold First

The first scene to hold in this Section is the following.

| Array expression | The first question to ask when reading it like a dataset |
| --- | --- |
| `shape = (4, 3)` | Are there 4 samples and 3 features? |
| `x[1, :]` | Does it choose only the second sample? |
| `x[:, 2]` | Does it choose the entire third feature column? |
| `sum(axis=0)` | Does it leave a summary by feature? |
| `sum(axis=1)` | Does it leave a summary by sample? |

In other words, `indexing`, `slicing`, and `axis` are not separate syntaxes to memorize. They are ways to write clearly on top of an array whether you are looking at one sample, looking at one whole feature, or summarizing in a certain direction.

## Three Criteria

| Criterion | Why it matters | Level of understanding needed in this Section |
| --- | --- | --- |
| What indexing is | It keeps you from mixing up position selection and range selection in array reading. | Understand it as choosing one exact position. |
| What slicing is | It helps you distinguish a single value from a partial array. | Understand it as leaving a range, not a point. |
| Why axis matters | It becomes the standard for reading the direction of later aggregation and broadcasting. | Understand it as the standard that decides the direction of array calculation. |

| Term | Meaning to capture first in this Section |
| --- | --- |
| indexing | A way of reading that chooses one exact position. |
| slicing | A way of reading that leaves a range by specifying a start and an end. |
| axis | The standard that decides the direction in which array calculation proceeds. |
| row | One horizontal line in a two-dimensional array. |
| column | One vertical line in a two-dimensional array. |

## Indexing Means Choosing a Position

The official NumPy documentation explains that an `ndarray` can be indexed with the standard Python form `x[obj]`. It also explains that, as in Python, indices start from 0.

First, look at a one-dimensional array.

Problem situation: We check the basic indexing that chooses which value in a one-dimensional array to read.
Input: A one-dimensional array `scores` containing four scores.
Expected output: The first value `82` and the third value `45` are printed.
Concept to check: See that indexing chooses one exact position and that position numbering starts from 0.

```python
# This example selects and summarizes NumPy array values by position, slice, and axis.
import numpy as np

scores = np.array([82, 75, 45, 90])

print(scores[0])
print(scores[2])
```

The output is as follows.

```text
82
45
```

`scores[0]` is the first value. `scores[2]` is the third value. In Python and NumPy, the first position is usually counted as 0 rather than 1.

This point is often confusing.

| Expression | How to read it | Result |
| --- | --- | --- |
| `scores[0]` | position 0 | `82` |
| `scores[1]` | position 1 | `75` |
| `scores[2]` | position 2 | `45` |
| `scores[-1]` | last position | `90` |

Indexing is the act of asking, `Which value is at this position?`

## in a Two-Dimensional Array, Choose Rows and Columns Together

In a two-dimensional array, you usually specify a row and a column together.

Problem situation: We choose one value in a two-dimensional array by specifying both row and column positions.
Input: The array `data` with 3 rows and 4 columns, and the position `[1, 2]`.
Expected output: The full `shape` and the selected value `22` are printed.
Concept to check: Confirm that the notation `data[row, column]` is the basic syntax for choosing one value.

```python
# This example selects and summarizes NumPy array values by position, slice, and axis.
data = np.array([
    [10, 11, 12, 13],
    [20, 21, 22, 23],
    [30, 31, 32, 33],
])

print(data.shape)
print(data[1, 2])
```

The output is as follows.

```text
(3, 4)
22
```

`data[1, 2]` chooses the value at row 1, column 2.

Here as well, indexing starts from 0.

| Expression | How to read it | Result |
| --- | --- | --- |
| `data[0, 0]` | row 0, column 0 | `10` |
| `data[0, 3]` | row 0, column 3 | `13` |
| `data[1, 2]` | row 1, column 2 | `22` |
| `data[2, 1]` | row 2, column 1 | `31` |

In a two-dimensional array, the comma can be read as a separator between dimensions. So you can read it as `data[row, column]`.

## Slicing Means Leaving a Range

Slicing chooses a range instead of one position.

Problem situation: We want to keep only a middle range from a one-dimensional array.
Input: An array containing four scores and the slice `1:3`.
Expected output: An array containing only the second and third values is printed.
Concept to check: See that slicing leaves the range from the start position up to, but not including, the stop position.

```python
# This example selects and summarizes NumPy array values by position, slice, and axis.
scores = np.array([82, 75, 45, 90])

print(scores[1:3])
```

The output is as follows.

```text
[75 45]
```

`1:3` means from position 1 up to the position before 3. So positions 1 and 2 are selected.

Remember it here like this.

| Expression | Meaning |
| --- | --- |
| `start:stop` | from start up to before stop |
| `:` | the whole range |
| `:3` | from the beginning up to before 3 |
| `1:` | from 1 to the end |
| `::2` | skip every other position |

Slicing is the act of asking, `Which range should remain?`

The diagram below shows how the notation `start:stop:step` is read on a one-line array.

![Slice notation selects a range from start to stop before the stop position](/AiBook/assets/part-02/chapter-11/slice-start-stop-step-en.svg)

The important point here is that the value at the `stop` position is not selected. `scores[1:5:2]` starts from position 1, looks up to before position 5, and moves by two steps at a time.

Problem situation: We compare at once how different `start:stop:step` combinations produce different results.
Input: An array containing six scores and several slice expressions.
Expected output: A continuous range, a range with two-step gaps, a front part, and a back part are printed.
Concept to check: See that slicing lets you control the start, stop, and interval of a range together.

```python
# This example selects and summarizes NumPy array values by position, slice, and axis.
scores = np.array([82, 75, 45, 90, 61, 70])

print(scores[1:5])
print(scores[1:5:2])
print(scores[:3])
print(scores[-2:])
```

The output is as follows.

```text
[75 45 90 61]
[75 90]
[82 75 45]
[61 70]
```

## How to Slice Rows and Columns

In a two-dimensional array, `:` lets you choose a whole row or a whole column.

Problem situation: In the same two-dimensional array, we choose one full row and one full column separately.
Input: The 3-row, 4-column array `data`, and the selections `data[2, :]` and `data[:, 3]`.
Expected output: The entire third row and the entire fourth column are printed.
Concept to check: See that `:` means the full range of that axis, and that row selection and column selection should be read separately.

```python
# This example selects and summarizes NumPy array values by position, slice, and axis.
data = np.array([
    [10, 11, 12, 13],
    [20, 21, 22, 23],
    [30, 31, 32, 33],
])

print(data[2, :])
print(data[:, 3])
```

The output is as follows.

```text
[30 31 32 33]
[13 23 33]
```

`data[2, :]` chooses all columns of row 2.

`data[:, 3]` chooses column 3 from all rows.

The diagram below shows the same array being read differently through indexing, row slicing, and column slicing.

![Indexing, slicing, and axis read different parts of the same array](/AiBook/assets/part-02/chapter-11/index-slice-axis-map-en.svg)

In this diagram, blue highlights one value, green highlights one row, and orange highlights one column. All of them are selections from the same array.

## You Can Also Cut Out a Small Region

When you specify both a row range and a column range, you can make a small sub-array.

Problem situation: In a two-dimensional array, we specify a row range and a column range together so that only a small rectangular area remains.
Input: The array `data` and the slice `data[0:2, 1:3]`.
Expected output: A 2-by-2 sub-array is printed.
Concept to check: See that slicing can choose ranges across several axes at once.

```python
# This example selects and summarizes NumPy array values by position, slice, and axis.
print(data[0:2, 1:3])
```

The output is as follows.

```text
[[11 12]
 [21 22]]
```

`data[0:2, 1:3]` is read as `from row 0 up to before row 2`, and `from column 1 up to before column 3`.

So rows 0 and 1 remain, and columns 1 and 2 remain.

At first, it is enough to understand slicing not as changing the entire original array, but as a way of reading the range you need. How a slicing result stays connected to the original is revisited in the supplementary learning of P2-11.4.

## Axis Decides the Direction of Calculation

The NumPy glossary explains axis as a term that refers to a dimension of an array. Axes are numbered from left to right, and `axis 0` is the first element in the shape tuple. In a two-dimensional array, `axis 0` is explained as the row direction and `axis 1` as the column direction.

Understand it here like this.

Problem situation: We look at the `shape` of a two-dimensional array and check what the axis numbers mean.
Input: The `shape` of the 3-row, 4-column array `data`.
Expected output: `(3, 4)` is printed.
Concept to check: See that interpreting `axis=0` as the first dimension and `axis=1` as the second dimension is connected to `shape`.

```python
# This example selects and summarizes NumPy array values by position, slice, and axis.
data.shape
```

If the result is `(3, 4)`, read it like this.

| Axis | Position in shape | Meaning in this example |
| --- | --- | --- |
| `axis=0` | first number `3` | 3 rows |
| `axis=1` | second number `4` | 4 columns |

Axis becomes especially important in summary calculations such as `sum` and `mean`.

Problem situation: We compare how the result changes depending on which axis of the same array we sum along.
Input: The 3-row, 4-column array `data`, plus `sum(axis=0)` and `sum(axis=1)`.
Expected output: An array of sums by column and an array of sums by row are printed.
Concept to check: See that axis is not a position number but a calculation direction, and that the result `shape` also changes.

```python
# This example selects and summarizes NumPy array values by position, slice, and axis.
print(data.sum(axis=0))
print(data.sum(axis=1))
```

The output is as follows.

```text
[60 63 66 69]
[ 46  86 126]
```

`sum(axis=0)` adds while moving down along the row direction. So one sum remains for each column.

`sum(axis=1)` adds horizontally along the column direction. So one sum remains for each row.

The diagram below shows which direction gets folded and what kind of result remains depending on the axis.

![Axis controls the direction of reduction](/AiBook/assets/part-02/chapter-11/axis-reduction-en.svg)

The important point is that `axis=0` does not mean `choose row 0`. In indexing, `0` is a number that chooses a position. But `axis=0` specifies the dimension along which calculation proceeds.

## Rows Are Often Read as Samples and Columns as Features

In AI practice, a two-dimensional array is often read in the following way.

| Direction | Common interpretation |
| --- | --- |
| row | sample, one data case |
| column | feature, variable |

For example, look at the following array.

Problem situation: In an array that can be read like a dataset, we pull out one sample and one feature column separately.
Input: The `features` array that can be read as 3 samples and 2 features.
Expected output: There is no printed output, but the example of a sample-feature structure is prepared.
Concept to check: See that a two-dimensional array is often read with rows as samples and columns as features.

```python
# This example selects and summarizes NumPy array values by position, slice, and axis.
features = np.array([
    [1.0, 0.2],
    [0.8, 0.4],
    [0.3, 0.9],
])
```

This array can be read as 3 samples and 2 features.

Problem situation: In the dataset-like array we prepared, we immediately pull out one sample and one feature column.
Input: The 3-row, 2-column `features` array and the selections `features[0, :]` and `features[:, 1]`.
Expected output: The full first sample and the full second feature column are printed.
Concept to check: See that, even in the same array, row selection and column selection correspond to different questions.

```python
# This example selects and summarizes NumPy array values by position, slice, and axis.
print(features[0, :])
print(features[:, 1])
```

The first line pulls out the first sample.

The second line pulls out the second feature from all samples.

This intuition matters later when you handle datasets. Before sending data into a model, you first need to decide, `Which row is one case?` and `Which column is one feature?`

To tie it up one more time briefly, it becomes the following.

| What you see in a NumPy array | When you read it again in dataset language |
| --- | --- |
| one row | one sample |
| one column | one full feature |
| `shape[0]` | number of samples |
| `shape[1]` | number of features |

If you hold this table first, expressions such as `X.shape`, `sample`, and `feature matrix` will feel much less unfamiliar in later Pandas and machine-learning documents.

The diagram below shows the same viewpoint in a slightly more dataset-like way.

![Rows often represent samples and columns often represent features](/AiBook/assets/part-02/chapter-11/dataset-row-column-selection-en.svg)

Here, `features[1, :]` is code that pulls out all features of one sample. By contrast, `features[:, 1]` pulls out one same feature across all samples.

Problem situation: In a more realistic dataset shape, we check one sample, one feature column, and its mean in sequence.
Input: The 4-row, 3-column `features` array, plus `features[1, :]`, `features[:, 1]`, and `mean()`.
Expected output: The second sample, the full second feature column, and its mean value are printed.
Concept to check: See that choosing a row means one case, choosing a column means one whole feature, and this can lead to later statistical calculations.

```python
# This example selects and summarizes NumPy array values by position, slice, and axis.
features = np.array([
    [1.0, 0.2, 7.0],
    [0.8, 0.4, 6.5],
    [0.3, 0.9, 8.1],
    [0.5, 0.1, 5.8],
])

print(features[1, :])
print(features[:, 1])
print(features[:, 1].mean())
```

The output is as follows.

```text
[0.8 0.4 6.5]
[0.2 0.4 0.9 0.1]
0.4
```

In this example, the last line calculates the mean of the second feature. In other words, `choosing one column` can lead directly to later work such as mean, variance, normalization, and feature comparison.

## Example Code File

You can also check the example code from this Section in the following file.

- [p2_11_2_index_slice_axis.py](/AiBook/assets/part-02/chapter-11/p2_11_2_index_slice_axis.py)

On a local PC, you can run it from the project root like this.

```bash
python docs/assets/part-02/chapter-11/p2_11_2_index_slice_axis.py
```

In Colab, you can paste the file content into a code cell and run it.

The output also includes examples of one-dimensional slicing with `start:stop:step` and examples of row and column selection in dataset-shaped arrays.

## Reading It as a Case

### Case 1. Do you want to look at only one student's scores, the whole subject column, or a summary along an axis?

Suppose that, looking at a score matrix, the reading changes depending on whether you want to look only at the second student's scores, the whole math-score column, or a summary along an axis like a regional average. People do this naturally when scanning a table with their eyes, but in array computation you must state indexing, slicing, and axis explicitly.

`data[1, :]` chooses one row for the second student, and `data[:, 2]` chooses the entire third column. `sum(axis=0)` moves down along the row direction and leaves sums by column, while `sum(axis=1)` adds inside each row and leaves sums by student.

This case shows that axis is not a simple number, but a standard for deciding `in which direction to read and calculate`. Even with the same array, the code changes depending on whether the question is `do you want to look at one case`, `do you want to look at one whole variable`, or `do you want a summary by each direction`.

So read indexing and slicing not as simple syntax, but as ways of placing the question on top of the array. You need this intuition before Pandas row or column selection and NumPy axis calculations connect cleanly.

Especially before moving on to Part 3, you should be able to say the following sentence immediately.

- `A row usually means a sample, a column usually means a feature, and shape shows the number of samples and features together.`

## Checklist

- You can explain that NumPy indices start from 0.
- You can read `data[1, 2]` using rows and columns.
- You can explain the difference between `data[2, :]` and `data[:, 3]`.
- You can explain what sub-array `data[0:2, 1:3]` chooses.
- You can explain why the results of `sum(axis=0)` and `sum(axis=1)` are different.
- You can explain the dataset viewpoint that rows are samples and columns are features.
- When you see `shape = (4, 3)`, you can read it as something like `4 samples, 3 features`.
- You can explain that indexing chooses a position, slicing leaves a range, and axis decides the direction of calculation.

## Sources and References

- NumPy Developers, [Indexing on ndarrays](https://numpy.org/doc/stable/user/basics.indexing.html){: target="_blank" rel="noopener noreferrer" }, NumPy v2.5 Manual, checked on 2026-07-20. Used to confirm basic indexing, slicing, multidimensional indices, advanced indexing, and copy/view cautions.
- NumPy Developers, [NumPy glossary](https://numpy.org/doc/stable/glossary.html){: target="_blank" rel="noopener noreferrer" }, NumPy v2.5 Manual, checked on 2026-07-20. Used to align terms such as axis, broadcasting, copy, and view with the terminology in this section.
