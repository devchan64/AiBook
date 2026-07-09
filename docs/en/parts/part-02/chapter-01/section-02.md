# P2-1.2 Where Formulas, Code, and Data Meet

> Section ID: `P2-1.2`
> Version: `v2026.07.09`

P2-1.1 framed math as the language for reading AI computation. Now we look at where that language actually sits during learning. In AI, formulas, code, and data are not separate things. They are closer to three faces of the same calculation.

1. Formulas compress computational structure.
2. Code executes computational procedure.
3. Data provides the object of the computation and the result to inspect.

## One Shared Scene to Hold First

We carry over the same small table from the previous Section.

| Student | Study time `x` | Quiz score `y` |
| --- | --- | --- |
| A | 1 hour | 55 |
| B | 2 hours | 65 |
| C | 3 hours | 80 |
| D | 4 hours | 90 |

This table is the smallest Chapter 1 scene where formulas, code, and data meet.

- As data, it is a small table with two columns, `x` and `y`.
- As formulas, it is material for writing down a mean, a function, and an error.
- As code, it is input that can be translated into lists, arrays, and variables.

## Scope of This Section

The question to solve right now is this: when the formula in a document comes down into a code cell and real data, what stays the same and what changes only in shape?

So this Section fixes only four places first.

- What is the formula saying?
- How does the code execute that formula?
- What shape does the data take?
- How should the result be interpreted afterward?

## Three Criteria

| Criterion | Why it matters | Understanding needed here |
| --- | --- | --- |
| The same calculation can appear differently as a formula, code, and data | It gives the feeling that you are reading the same thing on different surfaces | Understand that one mean can be explained in three ways |
| A formula compresses structure while code unfolds execution order | It explains why documents and example code look different | Understand what gets added, divided, and executed in what order |
| The result still has to be interpreted back in context | It connects directly to how you will later read metrics and loss | Understand that a number such as 72.5 still needs explanation |

## The Same Calculation Seen in Three Ways

Take the mean as the simplest example. If we pull out only the score column from the table, the data is `55, 65, 80, 90`.

Written as a formula:

\[
\mathrm{mean} = \frac{55 + 65 + 80 + 90}{4}
\]

Written as code:

```python
scores = [55, 65, 80, 90]
mean = sum(scores) / len(scores)

print(mean)
```

Example output:

```text
72.5
```

These three expressions look different, but they do the same thing.

- Data: the score bundle `55, 65, 80, 90`
- Formula: the compressed structure
- Code: the executable procedure
- Output: the result checked afterward

## Formulas Name Things and Compress Relationships

\[
y = f(x)
\]

This simple line is one of the most important structures in AI documents.

- `x`: the input
- `f`: the function or model
- `y`: the output

In machine learning contexts, you can read this as “input data `x` passes through `f` and becomes output `y`.”

In code, the same relation may appear as:

```python
y = model(x)
```

The grammar is not identical, but the structure is the same: input, transformation, output.

## Data Enters in a Computable Shape

Real-world data is usually turned into computable forms such as arrays, vectors, matrices, and tensors.

```python
import numpy as np

one_value = np.array(3)
vector = np.array([1, 2, 3])
matrix = np.array([[1, 2, 3], [4, 5, 6]])

print(one_value.shape)
print(vector.shape)
print(matrix.shape)
```

Example output:

```text
()
(3,)
(2, 3)
```

The point here is not advanced NumPy technique. It is just to see that the same numbers can belong to objects with different computational shapes.

## Code Turns Formulas into Executable Procedure

A mean is short to write as notation:

\[
\mathrm{mean} = \frac{\sum_{i=1}^{n}x_i}{n}
\]

But code still needs to expose the actual steps.

```python
scores = [55, 65, 80, 90]
n = len(scores)
total = sum(scores)
mean = total / n

print(n)
print(total)
print(mean)
```

Example output:

```text
4
290
72.5
```

Code can be longer than the formula, but it makes the execution order visible.

## Results Still Need Interpretation

Even when the calculation ends, understanding does not end automatically.

- If the mean is 72.5, it means the center of the four scores is roughly around 72.5.
- If a loss is 0.2, it means the prediction and the reference value differ by 0.2 under a particular loss definition.
- If accuracy is 90%, it still matters which cases were wrong.

So numeric output does not become meaning by itself. You still need to check what data produced it, what formula defined it, and what code executed it.

## Perspective to Keep from This Section

Formulas, code, and data are not competing things. They explain one computation from different positions. Formulas are closer to the blueprint, code is closer to the execution procedure, data is both the material and the object of verification, and the result still has to be interpreted back in the original context.

## Short Check

- You can explain that formulas, code, and data can express the same calculation in different ways.
- You can read `y = f(x)` as the relation among input, function, and output.
- You can explain that the shape of data changes the form of the computation.
- You can explain that code turns formulas into executable procedure.

## Sources and References

This Section organizes the internal reading stance of Part 2 and does not directly quote external material.
