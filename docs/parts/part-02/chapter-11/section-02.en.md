# P2-11.2 Indexing, Slicing, and Axes

> Section ID: `P2-11.2`
> Version: `v2026.09.15`

## Selecting a Position

NumPy arrays use the standard Python indexing syntax `x[obj]`. Indices start at zero, as in Python.

Start with a one-dimensional array.

Indices `0` and `2` in `[82, 75, 45, 90]` select the first value `82` and third value `45`.

```python
import numpy as np

scores = np.array([82, 75, 45, 90])

print(scores[0])
print(scores[2])
```

Output:

```text
82
45
```

`scores[0]` is the first value and `scores[2]` the third. Python and NumPy count the first position as 0, not 1.

| Expression | Reading | Result |
| --- | --- | --- |
| `scores[0]` | Position 0 | `82` |
| `scores[1]` | Position 1 | `75` |
| `scores[2]` | Position 2 | `45` |
| `scores[-1]` | Last position | `90` |

Indexing asks which position to select.

## Row and Column Positions

In a two-dimensional array, specify row and column together.

In a three-row, four-column array, `[1, 2]` selects the second row’s third value. This code prints shape `(3, 4)` and value `22`.

```python
data = np.array([
    [10, 11, 12, 13],
    [20, 21, 22, 23],
    [30, 31, 32, 33],
])

print(data.shape)
print(data[1, 2])
```

Output:

```text
(3, 4)
22
```

`data[1, 2]` selects row index 1 and column index 2.

These indices also start at zero.

| Expression | Reading | Result |
| --- | --- | --- |
| `data[0, 0]` | Row 0, column 0 | `10` |
| `data[0, 3]` | Row 0, column 3 | `13` |
| `data[1, 2]` | Row 1, column 2 | `22` |
| `data[2, 1]` | Row 2, column 1 | `31` |

The comma separates dimensions. Read a two-dimensional selection as `data[row, column]`.

## Ranges and Steps

Slicing selects a range rather than one position.

Selecting `1:3` from four scores keeps positions 1 and 2, producing `[75 45]`.

```python
scores = np.array([82, 75, 45, 90])

print(scores[1:3])
```

Output:

```text
[75 45]
```

`1:3` starts at position 1 and stops before position 3, selecting positions 1 and 2.

Range notation:

| Expression | Meaning |
| --- | --- |
| `start:stop` | From start to before stop |
| `:` | All positions |
| `:3` | From the beginning to before 3 |
| `1:` | From 1 to the end |
| `::2` | Step by two positions |

Slicing asks which range to retain.

The diagram shows how `start:stop:step` selects from a one-dimensional array.

```mermaid
--8<-- "assets/part-02/chapter-11/slice-start-stop-step-en.mmd"
```

The value at `stop` is excluded. `scores[1:5:2]` starts at 1, moves two positions at a time, and stops before 5.

For six scores, select a continuous interval, every second position, the first three, and the last two. Outputs are `[75 45 90 61]`, `[75 90]`, `[82 75 45]`, and `[61 70]`.

```python
scores = np.array([82, 75, 45, 90, 61, 70])

print(scores[1:5])
print(scores[1:5:2])
print(scores[:3])
print(scores[-2:])
```

Output:

```text
[75 45 90 61]
[75 90]
[82 75 45]
[61 70]
```

## Whole Rows and Columns

Use `:` to select a whole row or column in a two-dimensional array.

Select the third row and fourth column of the same `(3, 4)` array. The results are `[30 31 32 33]` and `[13 23 33]`.

```python
data = np.array([
    [10, 11, 12, 13],
    [20, 21, 22, 23],
    [30, 31, 32, 33],
])

print(data[2, :])
print(data[:, 3])
```

Output:

```text
[30 31 32 33]
[13 23 33]
```

`data[2, :]` selects every column in row 2.

`data[:, 3]` selects column 3 from every row.

This diagram contrasts selecting a value, a row, and a column from the same array.

```mermaid
--8<-- "assets/part-02/chapter-11/index-slice-axis-map-en.mmd"
```

These selections produce different result shapes, even though all use the same original array.

## Integer Selection and Retained Axes

`data[1, :]` selects one row and removes the row axis. `data[1:2, :]` keeps a one-row interval, retaining a row axis of length 1. The values can look the same while later operations receive different shapes.

```python
print(data[1, :].shape)
print(data[1:2, :].shape)
print(data[:, 2].shape)
print(data[:, 2:3].shape)
```

Outputs are `(4,)`, `(1, 4)`, `(3,)`, and `(3, 1)`. Use a length-one slice instead of an integer selection when later calculations need both axes.

`data[99, :]` raises `IndexError` because that row does not exist. `data[99:, :]` instead returns an empty array of shape `(0, 4)`. Slice bounds are clipped to available positions, so successful execution does not guarantee that any data remains.

## Subarrays

Specify row and column intervals together to obtain a smaller subarray.

Selecting rows `0:2` and columns `1:3` from `data` produces the two-by-two array `[[11, 12], [21, 22]]`.

```python
print(data[0:2, 1:3])
```

Output:

```text
[[11 12]
 [21 22]]
```

Read `data[0:2, 1:3]` as rows from 0 to before 2, and columns from 1 to before 3.

Rows 0 and 1, and columns 1 and 2 remain.

Basic slicing returns a view sharing data with the original. Editing this subarray also edits the original. Append `.copy()` when an independent array is required.

## Sums Along Axes

NumPy uses axis to mean an array dimension. Axes are numbered by position in the shape tuple, so axis 0 corresponds to its first entry. In two dimensions, axis 0 runs across rows and axis 1 across columns.

The earlier `data` has shape `(3, 4)`. Each shape entry gives an axis length.

```python
print(data.shape)
```

Interpret `(3, 4)` as follows:

| Axis | Position in shape | Meaning here |
| --- | --- | --- |
| `axis=0` | First number, `3` | Three rows |
| `axis=1` | Second number, `4` | Four columns |

Axes matter especially for reductions such as `sum` and `mean`.

Summing with `axis=0` gives column totals `[60 63 66 69]`; `axis=1` gives row totals `[46 86 126]`.

```python
print(data.sum(axis=0))
print(data.sum(axis=1))
```

Output:

```text
[60 63 66 69]
[ 46  86 126]
```

`sum(axis=0)` combines values down the rows, leaving one sum per column.

`sum(axis=1)` combines values across columns, leaving one sum per row.

The diagram shows which axis is reduced and which result shape remains.

```mermaid
--8<-- "assets/part-02/chapter-11/axis-reduction-en.mmd"
```

`axis=0` does not select row 0. An index identifies a position; an axis argument identifies the dimension over which a calculation proceeds.

## Samples and Features

AI examples often interpret two-dimensional arrays as follows:

| Direction | Common interpretation |
| --- | --- |
| Rows | Samples, individual records |
| Columns | Features, variables |

For example, put three samples with two features each into a matrix. Each row is a sample; this preparation code displays no output.

```python
features = np.array([
    [1.0, 0.2],
    [0.8, 0.4],
    [0.3, 0.9],
])
```

This array represents three samples and two features.

The first sample is `[1.0, 0.2]`; the second feature across samples is `[0.2, 0.4, 0.9]`. The code prints both arrays.

```python
print(features[0, :])
print(features[:, 1])
```

The first line selects the first sample.

The second selects the second feature across all samples.

Define which case each row and which feature each column represents. Shape alone cannot supply these meanings.

| NumPy view | Dataset interpretation |
| --- | --- |
| One row | One sample |
| One column | One feature across samples |
| `shape[0]` | Sample count |
| `shape[1]` | Feature count |

The diagram applies this view to a dataset-shaped array.

```mermaid
--8<-- "assets/part-02/chapter-11/dataset-row-column-selection-en.mmd"
```

`features[1, :]` retrieves every feature of one sample. `features[:, 1]` retrieves one feature across all samples.

From four samples with three features each, select the second sample and second feature column. The final output is that feature’s mean, `0.4`.

```python
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

Output:

```text
[0.8 0.4 6.5]
[0.2 0.4 0.9 0.1]
0.4
```

The final line computes the second feature’s mean. Selecting a column can lead to means, variances, normalization, or feature comparisons.

## Example Code File

The examples are also available in this file:

- [p2_11_2_index_slice_axis.py](/AiBook/assets/part-02/chapter-11/p2_11_2_index_slice_axis.py)

Locally, run from the project root:

```bash
python docs/assets/part-02/chapter-11/p2_11_2_index_slice_axis.py
```

In Colab, paste the file contents into a code cell.

Outputs also cover one-dimensional `start:stop:step` slicing and dataset-style row/column selection.

## Case: Student Totals and Subject Totals

Two students score `[80, 70, 90]` and `[60, 90, 75]` in Korean, mathematics, and English. Print the second student, mathematics column, subject totals, and student totals.

```python
import numpy as np

marks = np.array([[80, 70, 90], [60, 90, 75]])
print("second student:", marks[1, :])
print("math:", marks[:, 1])
print("subject totals:", marks.sum(axis=0))
print("student totals:", marks.sum(axis=1))
```

```text
second student: [60 90 75]
math: [70 90]
subject totals: [140 160 165]
student totals: [240 225]
```

Subject totals combine the student axis into shape `(3,)`; student totals combine the subject axis into `(2,)`. Raising the second student’s mathematics score from 90 to 100 changes the totals to `[140, 170, 165]` and `[240, 235]`. Only the mathematics total and second student’s total increase by 10.

## Checklist

- Explain zero-based NumPy indexing.
- Read `data[1, 2]` by row and column.
- Distinguish `data[2, :]` from `data[:, 3]`.
- Identify the subarray selected by `data[0:2, 1:3]`.
- Explain why `sum(axis=0)` and `sum(axis=1)` differ.
- Interpret rows as samples and columns as features when defined that way.
- Read shape `(4, 3)` as four samples and three features in that layout.
- Distinguish selecting a position, retaining a range, and choosing a reduction axis.
- Can you predict the shape difference between an integer index and a length-one slice?

## Sources and References

- NumPy Developers, [Indexing on ndarrays](https://numpy.org/doc/stable/user/basics.indexing.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, checked on 2026-07-20. Used to confirm basic indexing, slicing, multidimensional indices, advanced indexing, and copy/view cautions.
- NumPy Developers, [NumPy glossary](https://numpy.org/doc/stable/glossary.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, checked on 2026-07-20. Used to align terms such as axis, broadcasting, copy, and view with the terminology in this section.
